from usecases.arxiv_import import (
    fetch_arxiv_to_dataframe,
    add_content_to_dataframe,
)

from usecases.import_articles import create_in_relational_db
from usecases.export_to_mongo import pandas_export_to_mongodb
from models.mongo import ScientificArticle as MongoArticle

# from usecases.import_articles import load_data_from_csv
# from usecases.export_to_mongo import export_from_db
# from usecases.search_text import search_text_index


# if __name__ == "__main__":
#     new_articles_sqla = load_data_from_csv("data/articles.csv")
#     print("len new articles sqla:", len(new_articles_sqla))

#     mongo_articles = export_from_db(new_articles_sqla)
#     print("len mongo articles:", len(mongo_articles))

#     results = search_text_index(mongo_articles, "Hubble tension")
#     print("len results:", len(results))

#     for article in results:
#         print(f"{article.arxiv_id}: {article.title}")


def complete_pandas_pipeline(query: str, max_results: int = 20):
    print("1. Fetching ArXiv data...")
    df = fetch_arxiv_to_dataframe(query, max_results)

    print("2. Downloading content...")
    df = add_content_to_dataframe(df)

    print("3. Loading to MariaDB...")
    df = create_in_relational_db(df)

    print("4. Exporting to MongoDB...")
    mongo_articles = pandas_export_to_mongodb(df)

    return {
        "dataframe_size": len(df),
        "mariadb_count": df["db_id"].astype(bool).sum(),
        "mongodb_count": len(mongo_articles),
    }


def verify_mongo(keyword: str):
    results = MongoArticle.objects(title__icontains=keyword)
    print(f"Found {len(results)} articles matching '{keyword}'")
    for art in results:
        print(art.title)


if __name__ == "__main__":
    result = complete_pandas_pipeline("all:quantum", 10)
    print("Pipeline completed:", result)

    verify_mongo("quantum")
