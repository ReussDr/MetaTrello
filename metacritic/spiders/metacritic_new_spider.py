"""
Spider class for scraping metacritic pages (from XBox One games, sorted by Metacritic scores)
"""

from scrapy.spider import BaseSpider
from scrapy import Selector
from metacritic.items import MetacriticItem


# TODO Change this to automatically pull more pages, instead of just the first 3

class MetacriticSpider(BaseSpider):
    """
    Spider class for walking through metacritic pages (as required by scrapy)
    """
    name = "metacriticnew" # Name of the spider, to be used when crawling
    allowed_domains = ["metacritic.com"] # Where the spider is allowed to go
    start_urls = [
        "http://www.metacritic.com/browse/games/score/metascore/all/xboxone/filtered?sort=desc&page=0",
        "http://www.metacritic.com/browse/games/score/metascore/all/xboxone/filtered?sort=desc&page=1",
        "http://www.metacritic.com/browse/games/score/metascore/all/xboxone/filtered?sort=desc&page=2"
    ]

    def parse(self, response):
        """
        Function to scrape pulled documents and create Metacritic item records

        :param response: html page to scrape
        :return:         list of items found on page
        """
        sel = Selector(response)
        sites = sel.css("div.product_row")
        items = []
        for site in sites:
            item = MetacriticItem()
            item['title'] = ''.join(site.css("div.product_title a::text").extract()).strip()
            item['link'] = ''.join(site.css("div.product_title a::attr(href)").extract())
            item['cscore'] = ''.join(site.css("div.metascore_w::text").extract())
            item['uscore'] = ''.join(site.css("span.textscore_favorable::text").extract())
            item['date'] = ''.join(site.css("div.product_date::text").extract()).strip()
            item['platform'] = "Xbox One"
            items.append(item)

        return items
