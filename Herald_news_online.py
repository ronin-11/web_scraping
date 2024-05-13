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
        articles = soup.select('h3 a')
        return [{'title': article.get_text(strip=True), 'link': article['href']} for article in articles if article['href']]
    else:
        return []

def fetch_article_content(article_url):
    html_content = fetch_page(article_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        content_section = soup.select_one('div.post--content')
        return content_section.get_text(strip=True) if content_section else "No content found"

def save_to_csv(file_path, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Category', 'Content', 'Link', 'Source', 'Title'])  # Writing the headers of the CSV file
        for article in data:
            writer.writerow([article['title'], article['link'], article['content']])

def main():
    url = 'https://www.herald.co.zw/category/articles/top-stories/'
    articles_info = parse_homepage(url)
    for article in articles_info:
        article['content'] = fetch_article_content(article['link'])

    save_to_csv('herald_news_articles.csv', articles_info)

if __name__ == "__main__":
    main()
