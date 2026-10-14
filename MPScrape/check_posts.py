import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://www.mountainproject.com/forum/topic/125395711/new-edelrid-belay-device-the-pinch'
headers = {'User-Agent': 'Mozilla/5.0'}

posts_with_bq = []
posts_without_bq = []

for page in range(1, 12):
    url = f'{base_url}?page={page}' if page > 1 else base_url
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for row in soup.select('tr.message-row'):
        post_id = row.get('id', '')
        user = row.get('data-user-name', '')
        fr = row.select_one('.fr-view')
        if not fr:
            continue
        
        # version with quotes stripped
        fr_no_bq = BeautifulSoup(str(fr), 'html.parser')
        for bq in fr_no_bq.find_all('blockquote'):
            bq.decompose()
        # also decompose cite or script if any
        for tag in fr_no_bq.find_all(['script', 'style']):
            tag.decompose()
        
        text_clean = fr_no_bq.get_text(separator=' ', strip=True)
        # normalize whitespace
        text_clean = re.sub(r'\s+', ' ', text_clean).strip()
        
        # text with quotes
        text_with = re.sub(r'\s+', ' ', fr.get_text(separator=' ', strip=True)).strip()
        
        posts_without_bq.append((page, post_id, user, text_clean, text_with))

print(f'Total posts extracted: {len(posts_without_bq)}')
empty_without = [p for p in posts_without_bq if not p[3]]
print(f'Empty posts if blockquote removed: {len(empty_without)}')
for p in empty_without:
    print(f'Empty post on page {p[0]}, ID: {p[1]}, User: {p[2]}')
    print('  Original text was:', p[4][:100])

