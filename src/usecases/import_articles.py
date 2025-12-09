import csv
from pathlib import Path
from sqlalchemy.exc import IntegrityError

from models.relational import ScientificArticle, Author
from storage.relational_db import Session


def save_article(line: dict[str, str]) -> ScientificArticle | None:
    with Session() as session:
        try:
            author = Author(
                full_name=line["author_full_name"],
                title=line["author_title"],
            )

            article = ScientificArticle(
                title=line["title"],
                summary=line["summary"],
                file_path=line["file_path"],
                arxiv_id=line["arxiv_id"],
                author=author,
            )

            session.add(article)
            session.commit()
            print(f"Success: {article.arxiv_id}")
            return article

        except IntegrityError as e:
            print(f"Failure: {e}")
            return None


def load_data_from_csv(path: Path) -> list[ScientificArticle]:
    articles: list[ScientificArticle] = []

    with open(path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for line in reader:
            article = save_article(line)
            if article:
                articles.append(article)

    return articles


if __name__ == "__main__":
    new_articles = load_data_from_csv(Path("data/articles.csv"))
    print(f"Imported {len(new_articles)} articles")
