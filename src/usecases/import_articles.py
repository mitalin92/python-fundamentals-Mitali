# import csv
from models.mongo import ScientificArticle as MongoArticle, Author as MongoAuthor
from pathlib import Path
from sqlalchemy.exc import IntegrityError
import pandas as pd

from models.relational import ScientificArticle, Author
from storage.relational_db import Session

# def save_article(line: dict[str, str]) -> ScientificArticle | None:
#     with Session() as session:
#         try:
#             author = Author(
#                 full_name=line["author_full_name"],
#                 title=line["author_title"],
#             )

#             article = ScientificArticle(
#                 title=line["title"],
#                 summary=line["summary"],
#                 file_path=line["file_path"],
#                 arxiv_id=line["arxiv_id"],
#                 author=author,
#             )

#             session.add(article)
#             session.commit()
#             print(f"Success: {article.arxiv_id}")
#             return article

#         except IntegrityError as e:
#             print(f"Failure: {e}")
#             return None


def load_data_from_csv(path: str | Path) -> pd.DataFrame:
    file_path = Path(path)
    df = pd.read_csv(file_path, delimiter=";", dtype="string")
    return df


def insert_article(row: pd.Series) -> pd.Series:
    with Session() as session:
        try:
            author = Author(full_name=row["author_full_name"], title=row["author_title"])
            session.add(author)
            session.commit()

            article = ScientificArticle(
                title=row["title"],
                summary=row["summary"][:500],
                file_path=row["file_path"],
                arxiv_id=row["arxiv_id"],
                author_id=author.id,
            )

            session.add(article)
            session.commit()
            session.refresh(article)

            print("Inserted:", article.arxiv_id)
            return pd.Series([article.id, author.id], index=["db_id", "author_db_id"])

        except IntegrityError as err:
            print("Duplicate or error:", err)
            return pd.Series([0, 0], index=["db_id", "author_db_id"])


def create_in_relational_db(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(insert_article, axis=1)
    return pd.concat([df, ids], axis=1)


def insert_article_mongo(row: pd.Series) -> pd.Series:
    m_author = MongoAuthor(
        db_id=row["author_db_id"],
        full_name=row["author_full_name"],
        title=row["author_title"],
    )

    m_article = MongoArticle(
        db_id=row["db_id"],
        title=row["title"],
        summary=row["summary"],
        file_path=row["file_path"],
        arxiv_id=row["arxiv_id"],
        author=m_author,
    )

    m_article.save()

    print("Inserted into MongoDB:", row["arxiv_id"])

    return pd.Series({"mongo_id": str(m_article.id)})


def create_in_mongodb(df: pd.DataFrame) -> pd.DataFrame:
    mongo_ids = df.apply(insert_article_mongo, axis=1)
    return pd.concat([df, mongo_ids], axis=1)


# def load_data_from_csv(path: Path) -> list[ScientificArticle]:
# articles: list[ScientificArticle] = []

# with open(path, "r") as f:
#     reader = csv.DictReader(f, delimiter=";")
#     for line in reader:
#         article = save_article(line)
#         if article:
#             articles.append(article)

# return articles


if __name__ == "__main__":
    new_articles = load_data_from_csv(Path("data/articles.csv"))
    print(f"Imported {len(new_articles)} articles")
