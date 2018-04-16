"""
Item pipeline code for processing items retrieved from MetaCritic
"""

from __future__ import print_function
import json
#import re
import os
import trello

def get_trello_properties():
    """
    Read trello connection properties from the config file or environment variables

    :return: Dictionary with trello connection parameters
    """
    config = {}
    # Read properties from trello_config.json if it is available
    # TODO Change the file format to something other than json (that allows comments)
    try:
        with open('trello_config.json', 'r') as config_file:
            config = json.load(config_file)
    except IOError:
        print("Failed to read config file trello_config.json.  Falling back to reading environment variables")

    # If Environment variables are set, they override the trello_config.json
    if os.environ.get('TRELLO_API_KEY') is not None:
        config['trello_api_key'] = os.environ.get('TRELLO_API_KEY')
    if os.environ.get('TRELLO_API_SECRET') is not None:
        config['trello_api_secret'] = os.environ.get('TRELLO_API_SECRET')
    if os.environ.get('TRELLO_BOARD_ID') is not None:
        config['trello_board_id'] = os.environ.get('TRELLO_BOARD_ID')

    return config
