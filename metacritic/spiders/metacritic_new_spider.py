from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
from metacritic.items import MetacriticItem


class MetacriticSpider(BaseSpider):
    name = "metacriticnew" # Name of the spider, to be used when crawling
    allowed_domains = ["metacritic.com"] # Where the spider is allowed to go
    start_urls = [
        "http://www.metacritic.com/browse/games/score/metascore/all/xboxone/filtered?sort=desc&page=0"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.css("div.product_row")
        items = []
        for site in sites:
            item = MetacriticItem()
            item['title'] = ''.join(site.css("div.product_title a::text").extract()).strip()
            item['link'] = ''.join(site.css("div.product_title a::attr(href)").extract())
            #item['cscore'] = site.select('div[@class="basic_stat product_score brief_metascore"]/div[contains( @class , "metascore_w small game positive")] / text()').extract()
            #item['uscore'] = site.select('div[@class="more_stats condensed_stats"]/ul/li/span[contains( @class , "data textscore textscore")] / text()').extract()
            item['cscore'] = ''.join(site.css("div.metascore_w::text").extract())
            item['uscore'] = ''.join(site.css("span.textscore_favorable::text").extract())
            item['date'] = ''.join(site.css("div.product_date::text").extract()).strip()
            items.append(item)

        #for game in response.css("div.game"):
        #    print game
        #    print game.css("div.product_title")

        #hxs = HtmlXPathSelector(response)  # The XPath selector
        #sites = hxs.select('//li[contains(@class, "product game_product")]/div[@class="product_wrap"]')
        #items = []
        #for site in sites:
        #    item = MetacriticItem()
        #    item['title'] = site.select('div[@class="basic_stat product_title"]/a/text()').extract()
        #    item['link'] = site.select('div[@class="basic_stat product_title"]/a/@href').extract()
        #    #item['cscore'] = site.select('div[@class="basic_stat product_score brief_metascore"]/div/div/span[contains( @class , "data metascore score")] / text()').extract()
        #    item['cscore'] = site.select('div[@class="basic_stat product_score brief_metascore"]/div[contains( @class , "metascore_w small game positive")] / text()').extract()
        #    item['uscore'] = site.select('div[@class="more_stats condensed_stats"]/ul/li/span[contains( @class , "data textscore textscore")] / text()').extract()
        #    item['date'] = site.select('div[@class="more_stats condensed_stats"]/ul/li/span[@ class ="data"] / text()').extract()
        #    items.append(item)
        return items