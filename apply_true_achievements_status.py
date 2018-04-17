"""
Used to move cards on a board (populated by MetaTrello) to have
their status reflect play status (per TrueAchievements)
"""
from __future__ import print_function
import argparse
import sys
import csv
from trello_helpers.utils import TrelloWrapper

def create_parser():
    """
    Create an argument parser to be used by this script
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with csv downloaded from TrueAchievements")
    return parser


def main():
    """
    Main script that reads through the collection file and updates the status of the games

    :return:
    """
    parser = create_parser()
    args = parser.parse_args()
    print("Reading TrueAchievement collection from:", args.filename)

    trello = TrelloWrapper()
    with open(args.filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row[' Game name'], row['My Completion Percentage'])
            trello.update_game_status(row[' Game name'], row['My Completion Percentage'])

if __name__ == "__main__":
    sys.exit(main())
