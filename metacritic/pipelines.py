# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
Item pipeline code for processing items retrieved from MetaCritic
"""

from __future__ import print_function
from trello_helpers.utils import TrelloWrapper


class MetacriticPipeline(object):
    """
    Metacritic Pipeline class that scrapy invokes for all items found by the metacritic spider
    """
    def __init__(self):
        """
        Initialization needs to connect to trello, and pull a dictionary of all titles/cards.
        This makes it easy for process_item to update card titles and create new cards
        """
        self._trello_wrapper = TrelloWrapper()

    def process_item(self, item, spider):
        """
        Method to handle items found by the spider
        :param item:   item found by the spider
        :param spider:
        :return:       item if criteria is met (in this case >= Critic Score 80)
        """
        self._trello_wrapper.add_game_or_update_score(item['title'], item['platform'], item['cscore'])
        return item
