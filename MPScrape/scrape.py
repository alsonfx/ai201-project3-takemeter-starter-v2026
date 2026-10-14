import csv
import html
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

BASE_URL = "https://www.mountainproject.com/forum/topic/125395711/new-edelrid-belay-device-the-pinch"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
OUTPUT_CSV = Path(r"d:\Codepath\ai201-project3-takemeter-starter-v2026\labels.csv")

def clean_post_text(fr_elem):
    soup = BeautifulSoup(str(fr_elem), "html.parser")

    # Remove quoted text from other users
    for bq in soup.find_all("blockquote"):
        bq.decompose()

    # Remove any scripts or styles
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()

    # Extract text with space separation
    text = soup.get_text(separator=" ", strip=True)

    # Decode HTML entities (e.g. &quot;, &amp;, &#39;)
    text = html.unescape(text)

    # Replace non-breaking spaces
    text = text.replace("\xa0", " ")

    # Normalize whitespace to single spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

def scrape_forum():
    posts = []
    page = 1
    max_pages = 11

    print(f"Scraping {max_pages} pages from Mountain Project...")
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}?page={page}" if page > 1 else BASE_URL
        print(f"  Fetching page {page}/{max_pages}: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.content, "html.parser")
        message_rows = soup.select("tr.message-row")
        print(f"    Found {len(message_rows)} message rows.")

        for row in message_rows:
            fr = row.select_one(".fr-view")
            if not fr:
                continue

            cleaned_text = clean_post_text(fr)
            if cleaned_text:
                posts.append(cleaned_text)

    print(f"\nScraping complete! Total valid posts extracted: {len(posts)}")

    # Build DataFrame
    df = pd.DataFrame({
        "text": posts,
        "label": ["" for _ in posts],
        "note": ["" for _ in posts]
    })

    # Save to labels.csv
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8", quoting=csv.QUOTE_MINIMAL)
    print(f"Saved {len(df)} rows to {OUTPUT_CSV}")

    # Verify
    df_loaded = pd.read_csv(OUTPUT_CSV)
    print(f"Verification: Loaded {len(df_loaded)} rows from {OUTPUT_CSV}")
    print(f"Columns: {list(df_loaded.columns)}")
    print(f"Empty text rows: {df_loaded['text'].isna().sum() + (df_loaded['text'].astype(str).str.strip() == '').sum()}")
    print(f"Duplicate text rows: {df_loaded['text'].duplicated().sum()}")
    print("\nSample first 3 rows:")
    for i, row in df_loaded.head(3).iterrows():
        print(f"  Row {i+1}: {row['text'][:120]}...")

if __name__ == "__main__":
    scrape_forum()

