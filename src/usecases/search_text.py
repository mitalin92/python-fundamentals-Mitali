import storage.mongo  # noqa: F401
from models.mongo import ScientificArticle


def search_text(keyword: str):
    query = ScientificArticle.objects(text__icontains=keyword)
    return query


def search_text_index(articles, keyword: str):
    all_ids = [a.id for a in articles]

    query = ScientificArticle.objects.filter(id__in=all_ids).search_text(keyword)

    return query
