# import pymupdf4llm

# from models.relational import ScientificArticle
from models.mongo import ScientificArticle as MongoArticle, Author as MongoAuthor

# from mongoengine import DoesNotExist
from bs4 import BeautifulSoup


# def save_article(article: ScientificArticle) -> MongoArticle | None:
#     try:
#         m_author = MongoAuthor(
#             db_id=article.author.id,
#             full_name=article.author.full_name,
#             title=article.author.title,
#         )

#         m_text = pymupdf4llm.to_markdown(article.file_path)

#         kwargs = dict(
#             db_id=article.id,
#             title=article.title,
#             summary=article.summary,
#             file_path=article.file_path,
#             created_at=article.created_at,
#             arxiv_id=article.arxiv_id,
#             author=m_author,
#             text=m_text,
#         )

#         try:
#             m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
#             m_article.update(**kwargs)
#         except DoesNotExist:
#             m_article = MongoArticle(**kwargs)
#             m_article.save()

#         print(f"Success: {article.arxiv_id}")
#         return m_article

#     except Exception as e:
#         print(f"Failure: {e}")
#         return None


# def export_from_db(sql_articles: list[ScientificArticle]) -> list[MongoArticle]:
#     new_articles = []
#     for article in sql_articles:
#         m_article = save_article(article)
#         if m_article:
#             new_articles.append(m_article)
#     return new_articles


def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")


def pandas_export_to_mongodb(df):
    mongo_articles = []

    for _, row in df.iterrows():
        m_author = MongoAuthor(full_name=row["author_full_name"], title=row["author_title"])

        processed_content = extract_text_from_html(row["content"])

        m_article = MongoArticle(
            title=row["title"],
            summary=row["summary"],
            arxiv_id=row["arxiv_id"],
            author=m_author,
            text=processed_content,
        )

        m_article.save()
        mongo_articles.append(m_article)

    return mongo_articles
