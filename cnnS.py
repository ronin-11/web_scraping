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
        all_news_divs = soup.select("div.container_lead-plus-headlines-with-images__item--type-section")
        for div in all_news_divs:
            links = div.find_all('a')
            if len(links) > 1:
                news = links[1]
                title_tag = news.find('span', class_='container__headline-text')
                title = title_tag.get_text(strip=True) if title_tag else None
                relative_link = news.get('href')
                if relative_link:
                    full_link = requests.compat.urljoin(url, relative_link)
                    yield {'title': title, 'link': full_link}

def parse_article(article_url):
    html_content = fetch_page(article_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        content = ' '.join([p.get_text(strip=True) for p in soup.select('div.article__content p.paragraph.inline-placeholder.vossi-paragraph-primary-core-light')])
        return content

def save_to_csv(file_path, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Category', 'Title', 'Content', 'Link', 'Source'])  # Writing the headers of CSV
        for news_item in data:
            writer.writerow([news_item['category'], news_item['title'], news_item['content'], news_item['link'], 'CNN'])

def main():
    url = 'https://edition.cnn.com/sport'
    category = url.split('/')[-1]

    news_data = []
    for news_item in parse_homepage(url):
        article_content = parse_article(news_item['link'])
        news_data.append({
            'category': category,
            'title': news_item['title'],
            'content': article_content,
            'link': news_item['link']
        })

    save_to_csv('cnn_sports.csv', news_data)

if __name__ == "__main__":
    main()
