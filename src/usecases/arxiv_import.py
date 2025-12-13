import requests
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm

tqdm.pandas()


def fetch_arxiv_data(query: str, max_results: int = 10) -> str:
    url = "http://export.arxiv.org/api/query"
    params: dict[str, str] = {
        "search_query": query,
        "start": "0",
        "max_results": str(max_results),
    }

    response = requests.get(url, params=params)
    return response.text


# type: ignore[union-attr]
def parse_arxiv_xml(xml_data: str) -> pd.DataFrame:
    root = ET.fromstring(xml_data)
    ns = {"a": "http://www.w3.org/2005/Atom"}

    rows = []

    for entry in root.findall("a:entry", ns):
        arxiv_id = entry.find("a:id", ns).text.split("/")[-1]  # type: ignore[union-attr]
        title = entry.find("a:title", ns).text.strip()  # type: ignore[union-attr]
        summary = entry.find("a:summary", ns).text.strip()  # type: ignore[union-attr]

        author = entry.find("a:author/a:name", ns)
        author_full_name = author.text if author is not None else "Unknown"

        rows.append(
            {
                "title": title,
                "summary": summary,
                "file_path": f"papers/{arxiv_id}.pdf",
                "arxiv_id": arxiv_id,
                "author_full_name": author_full_name,
                "author_title": "Researcher",
            }
        )

    return pd.DataFrame(rows, dtype="string")


def fetch_arxiv_to_dataframe(query: str, max_results: int = 10) -> pd.DataFrame:
    xml_data = fetch_arxiv_data(query, max_results)
    df = parse_arxiv_xml(xml_data)
    return df


# Download HTML content for an article


def download_content(arxiv_id: str) -> str | None:
    url = f"https://arxiv.org/abs/{arxiv_id}"
    response = requests.get(url)
    return response.text if response.ok else None


def add_content_to_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df["content"] = df["arxiv_id"].progress_apply(download_content)
    df = df[df["content"].notna()].copy()  # keep only successful downloads
    return df
