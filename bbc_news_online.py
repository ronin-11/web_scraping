import scrapy
from ..items import ScrapenewsItem

class ScrapeNews(scrapy.Spider):
    name = 'news_bbc'
    start_urls = [
        'https://www.bbc.com/business'
    ]

    def parse(self, response):
        category = response.url.split('/')[-1]

        all_news = response.css(".lx-stream__post-container")

        for news in all_news:
            item = ScrapenewsItem()

            title = news.css('.qa-heading-link::text').get()
            content = news.css('.lx-stream-post-body::text').get()
            source = 'BBC'
            relative_link = news.css('a.qa-heading-link::attr(href)').get()
            link = response.urljoin(relative_link)

            item['title'] = title
            item['category'] = category
            item['content'] = content
            item['source'] = source
            item['link'] = link

            yield item
