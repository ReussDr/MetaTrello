# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MetacriticItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # Game title
    platform = scrapy.Field() # Game platform
    link = scrapy.Field()  # Link to individual game page
    cscore = scrapy.Field()  # Critic score
    uscore = scrapy.Field()  # User score
    date = scrapy.Field()  # Release date
    desc = scrapy.Field()  # Description of game
