"""
Item pipeline code for processing items retrieved from MetaCritic
"""

from __future__ import print_function
import re
import os
import trello
import configparser

def get_trello_properties():
    """
    Read trello connection properties from the config file or environment variables

    :return: Dictionary with trello connection parameters
    """
    config = {}
    # Read properties from trello_config.ini if it is available
    config = configparser.ConfigParser()
    config.read('trello_config.ini')

    if 'Trello API Keys' not in config:
        config['Trello API Keys'] = {}
    if 'Trello Board Settings' not in config:
        config['Trello Board Settings'] = {}

    # If Environment variables are set, they override the trello_config.json
    if os.environ.get('TRELLO_API_KEY') is not None:
        config['Trello API Keys']['trello_api_key'] = os.environ.get('TRELLO_API_KEY')
    if os.environ.get('TRELLO_API_SECRET') is not None:
        config['Trello API Keys']['trello_api_secret'] = os.environ.get('TRELLO_API_SECRET')
    if os.environ.get('TRELLO_BOARD_ID') is not None:
        config['Trello Board Settings']['trello_board_id'] = os.environ.get('TRELLO_BOARD_ID')

    return config


class TrelloWrapper(object):
    """
    Used to wrap trello cards interactions for common functions
    """
    def __init__(self):
        """
        Initialization needs to connect to trello, and pull a dictionary of all titles/cards.
        This makes it easy for process_item to update card titles and create new cards
        """
        self._board_dict = {}
        self._config = get_trello_properties()
        self._initialize_connection()
        self._initialize_card_collection()
        self._initialize_board_list()

    def _initialize_connection(self):
        """
        This connects to trello, and searches for the specified board.

        It raises an exception of the connection is not successful.
        If no board is specified it prints a list of boards and their ids.

        :return:
        """
        # Initialize trello client
        print("Inside Init")
        self._client = trello.TrelloClient(
            api_key=self._config['Trello API Keys']['trello_api_key'],
            api_secret=self._config['Trello API Keys']['trello_api_secret'],
            # token='your-oauth-token',
            # token_secret='your-oauth-token-secret'
        )

        # Ensure that authorization passed, and that we can retrieve the board
        try:
            self._game_board = self._client.get_board(self._config['Trello Board Settings']['trello_board_id'])
        except trello.Unauthorized:
            print("Trello authorization failed.  Check api key and api secret.")
            raise
        except trello.ResourceUnavailable:
            print("Trello couldn't retrieve the board.",
                  "Board id needs to be set to an existing board:")
            print(' ', 'Board ID'.ljust(24), 'Board Name')
            for board in self._client.list_boards():
                print(' ', board.id.rjust(24), board.name)
            raise

    def _initialize_card_collection(self):
        """
        Retrieves all the cards on the current board,
        and stores them in a dictionary for easy lookup
        :return:
        """
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

    def _initialize_board_list(self):
        print(self._game_board.all_lists())
        for board in self._game_board.all_lists():
            #print(board, board.pos)

            if board.name == "Owned":
                self._board_dict["Owned"] = board
            if board.name == "Playing":
                self._board_dict["Playing"] = board
            if board.name == "Completed":
                self._board_dict["Completed"] = board


    def add_game_or_update_score(self, game_name, score):
        """
        Update
        :param game_name: game_name (with score stripped off)
        :param score:     Metacritic critic score
        :return:
        """
        new_title = game_name + ' [' + score + ']'

        #Update the game card if it exists (regardless of score)
        if game_name in self._card_collection:
            # Update title with Metascore if it already exists (might be same as previous)
            if self._card_collection[game_name].name != new_title:
                self._card_collection[game_name].set_name(new_title)

        if int(score) >= 80 and game_name not in self._card_collection:
            # Create a new card if MetaCritic > 80 and card isn't already on the board
            self._new_card_list.add_card(new_title)

    def update_game_status(self, game_name, percentage):
        """

        :param game_name:
        :param percentage:
        :return:
        """
        if game_name in self._card_collection:
            game_list_position = self._card_collection[game_name].get_list().pos
            if int(percentage) == 100 and game_list_position < self._board_dict["Completed"].pos:
                self._card_collection[game_name].change_list(self._board_dict["Completed"].id)
            elif int(percentage) > 0 and game_list_position < self._board_dict["Playing"].pos:
                self._card_collection[game_name].change_list(self._board_dict["Playing"].id)
            elif game_list_position < self._board_dict["Owned"].pos:
                self._card_collection[game_name].change_list(self._board_dict["Owned"].id)

        #if game_name in self._card_collection: