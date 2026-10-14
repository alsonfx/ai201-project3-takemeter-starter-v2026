import requests
from bs4 import BeautifulSoup
import html
import re

base_url = 'https://www.mountainproject.com/forum/topic/125395711/new-edelrid-belay-device-the-pinch'
headers = {'User-Agent': 'Mozilla/5.0'}

posts = []

def clean_post_text(fr_elem):
    # Make a copy so we don't mutate
    soup_copy = BeautifulSoup(str(fr_elem), 'html.parser')
    
    # Remove blockquotes (quoted previous posts)
    for bq in soup_copy.find_all('blockquote'):
        bq.decompose()
        
    # Remove scripts, styles
    for tag in soup_copy.find_all(['script', 'style']):
        tag.decompose()
        
    # Get text
    text = soup_copy.get_text(separator=' ', strip=True)
    
    # Unescape HTML entities
    text = html.unescape(text)
    
    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')
    
    # Replace common mojibake / corrupted quotes
    # Mountain project has \ufffd where smart quotes or dashes were
    # Let's inspect how \ufffd appears
    text = re.sub(r'(\w)[\ufffd](\w)', r"\1'\2", text) # dont -> don't
    text = text.replace('\ufffd', "'")
    
    # Normalize whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

for page in range(1, 12):
    url = f'{base_url}?page={page}' if page > 1 else base_url
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    for row in soup.select('tr.message-row'):
        fr = row.select_one('.fr-view')
        if not fr:
            continue
        cleaned = clean_post_text(fr)
        if cleaned:
            posts.append({
                'page': page,
                'post_id': row.get('id', ''),
                'user': row.get('data-user-name', ''),
                'text': cleaned
            })

print(f'Total cleaned non-empty posts: {len(posts)}')
print('\n--- First 5 posts ---')
for p in posts[:5]:
    print(f"[{p['user']}]: {p['text']}")
    print()

print('\n--- 5 Random / middle posts (posts 50 to 55) ---')
for p in posts[50:55]:
    print(f"[{p['user']}]: {p['text']}")
    print()

print('\n--- Last 5 posts ---')
for p in posts[-5:]:
    print(f"[{p['user']}]: {p['text']}")
    print()

