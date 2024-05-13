import requests
from bs4 import BeautifulSoup
import csv

def fetch_page(url):
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def parse_homepage(url):
    html_content = fetch_page(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        all_articles = soup.select("div.wide-tease-item__info-wrapper")
        for article in all_articles:
            links = article.find_all('a')
            if len(links) > 1:
                title_tag = links[1].find('h2')
                title = title_tag.get_text(strip=True) if title_tag else "No title found"
                relative_link = links[1].get('href')
                if relative_link:
                    full_link = requests.compat.urljoin(url, relative_link)
                    yield {'title': title, 'link': full_link}

def parse_article(article_url):
    html_content = fetch_page(article_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        content = ' '.join([p.get_text(strip=True) for p in soup.select('div.article-body__content p')])
        return content

def write_to_csv(file_path, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Category', 'Content', 'Link', 'Source', 'Title'])
        for news_item in data:
            writer.writerow([news_item['category'], news_item['content'], news_item['link'], 'NBC', news_item['title']])

def main():
    url = 'https://www.nbcnews.com/business'
    category = url.split('/')[-1] if 'culture-matters' not in url else 'entertainment'

    news_data = []
    for news_item in parse_homepage(url):
        article_content = parse_article(news_item['link'])
        news_data.append({
            'category': category,
            'title': news_item['title'],
            'content': article_content,
            'link': news_item['link']
        })

    write_to_csv('nbcnews_business_data.csv', news_data)

if __name__ == "__main__":
    main()
