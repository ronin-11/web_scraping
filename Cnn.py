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
        all_news = soup.select("div.container_list-headlines__field-wrapper a")
        for news in all_news:
            title_element = news.find('span', class_='container__headline-text')
            title = title_element.get_text(strip=True) if title_element else None
            relative_link = news.get('href')
            if relative_link:
                full_link = requests.compat.urljoin(url, relative_link)
                yield {'title': title, 'link': full_link}

def parse_article(article_url):
    html_content = fetch_page(article_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        content = ' '.join([p.get_text(strip=True) for p in soup.select('div.article__content p')])
        return content

def main():
    url = 'https://edition.cnn.com/business'
    category = url.split('/')[-1]

    with open('cnn_business.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Category', 'Title', 'Content', 'Link', 'Source'])  # Changed the order of CSV headers

        for news_item in parse_homepage(url):
            article_content = parse_article(news_item['link'])
            writer.writerow([category, news_item['title'], article_content, news_item['link'], 'CNN'])

if __name__ == "__main__":
    main()
