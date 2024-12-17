from bs4 import BeautifulSoup
import requests


subreddit_url = 'https://www.reddit.com/r/ChronicPain/'

response = requests.get(subreddit_url)

soup = BeautifulSoup(response.text, 'html.parser')
post_links = soup.select('shreddit-post a[slot="full-post-link"]')
urls = [link['href'] for link in post_links]

print(f"Number of URLs found: {len(urls)}")
if urls:
    print("URLs found:")
    for i, url in enumerate(urls):
        print(f"{i+1}. {url}")
else:
    print("No URLs found.")