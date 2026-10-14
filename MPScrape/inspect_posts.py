import requests
from bs4 import BeautifulSoup

base_url = 'https://www.mountainproject.com/forum/topic/125395711/new-edelrid-belay-device-the-pinch'
headers = {'User-Agent': 'Mozilla/5.0'}

resp = requests.get(base_url, headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')

for row in soup.select('tr.message-row'):
    fr = row.select_one('.fr-view')
    if not fr: continue
    if fr.find('blockquote'):
        print('=== POST WITH BLOCKQUOTE ===')
        user = row.get('data-user-name')
        print('User:', user)
        # With blockquote:
        text_with = fr.get_text(separator=' ', strip=True)
        print('WITH quote:\n', text_with[:300])
        # Without blockquote:
        fr_copy = BeautifulSoup(str(fr), 'html.parser')
        for bq in fr_copy.find_all('blockquote'):
            bq.decompose()
        text_without = fr_copy.get_text(separator=' ', strip=True)
        print('WITHOUT quote:\n', text_without[:300])
        print()

