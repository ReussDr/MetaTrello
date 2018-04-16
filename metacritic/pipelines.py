# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
Item pipeline code for processing items retrieved from MetaCritic
"""

from __future__ import print_function
import json
import re
import os
import trello
from scrapy.exceptions import DropItem
from trello_helpers.utils import get_trello_properties





class MetacriticPipeline(object):
    """
    Metacritic Pipeline class that scrapy invokes for all items found by the metacritic spider
    """
    def __init__(self):
        """
        Initialization needs to connect to trello, and pull a dictionary of all titles/cards.
        This makes it easy for process_item to update card titles and create new cards
        """
        config = get_trello_properties()
        # TODO Remove debug printing
        for item in config:
            print(item, config[item])

        # Initialize trello client
        print("Inside Init")
        self._client = trello.TrelloClient(
            api_key=config['trello_api_key'],
            api_secret=config['trello_api_secret'],
            # token='your-oauth-token',
            # token_secret='your-oauth-token-secret'
        )

        # Ensure that authorization passed, and that we can retrieve the board
        try:
            self._game_board = self._client.get_board(config['trello_board_id'])
        except trello.Unauthorized:
            print("Trello authorization failed.  Check api key and api secret.")
            raise
        except trello.ResourceUnavailable:
            print("Trello couldn't retrieve the board.  Board id needs to be set to an existing board:")
            print(' ', 'Board ID'.ljust(24), 'Board Name')
            for board in self._client.list_boards():
                print(' ', board.id.rjust(24), board.name)
            raise

        # Retrieve all the cards, and create a dictionary with all of the game titles and cards
        self._card_collection = {}
        for card in self._game_board.all_cards():
            game_title = card.name
            re_var = re.search('(.*) \\[\\d+\\]', card.name)
            if re_var is not None:
                game_title = re_var.group(1)
            self._card_collection[game_title] = card

        # Get the list to add new cards to
        try:
            self._new_card_list = self._game_board.open_lists()[0]
        except IndexError:
            print("Trello board doesn't have any lists.  Create at least one list")
            raise

    def process_item(self, item, spider):
        """
        Method to handle items found by the spider
        :param item:   item found by the spider
        :param spider:
        :return:       item if criteria is met (in this case >= Critic Score 80)
        """
        new_title = item['title'] + ' [' + item['cscore'] + ']'

        if item['title'] in self._card_collection:
            # Update title with Metascore if it already exists (might be same as previous)
            self._card_collection[item['title']].set_name(new_title)
        if int(item['cscore']) >= 80:
            if item['title'] not in self._card_collection:
                # Create a new card if MetaCritic > 80 and card isn't already on the board
                self._new_card_list.add_card(new_title)
            return item
        raise DropItem("Critic score too low for %s" % item)

        #TODO Create new cards for games not already added
