from usecases.import_articles import load_data_from_csv
from usecases.export_to_mongo import export_from_db
from usecases.search_text import search_text_index


if __name__ == "__main__":
    new_articles_sqla = load_data_from_csv("data/articles.csv")
    print("len new articles sqla:", len(new_articles_sqla))

    mongo_articles = export_from_db(new_articles_sqla)
    print("len mongo articles:", len(mongo_articles))

    results = search_text_index(mongo_articles, "Hubble tension")
    print("len results:", len(results))

    for article in results:
        print(f"{article.arxiv_id}: {article.title}")
