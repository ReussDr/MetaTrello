# MetaTrello
Do you have more games than freetime?  Do you have an interest in playing some of the best reviewed games, but keep forgetting what to play next?  Do you enjoy using Trello to organize other aspects of your life?

If so, this is for you.  I got tired of diving into free-to-p[l]ay games instead of diving into many of the high rated games I already owned.  So I wrote this to help me organize my time.

This is run in 2 main passes.  In the first you populate a Trello board with all of the XBox One titles with a metacritic score >= 80.  (Note: other platforms, customizable score threshold and genre selection will be coming later).  In the second, you provide a csv file from TrueAchievements and it will move the cards into different lists based on what you've already played.

## Setup
What you'll need
  * Python and pip
  * A Trello account
  * [optional] A TrueAchievements account

First git clone this project.  Then browse to this page:

   [https://trello.com/app-key]

You'll need both the key and the token.  Edit trello_config.ini and change the trello_api_key and trello_api_secret to the key and token contents.  You will also want to have lists that match the `trello_list_todo`, `trello_list_owned`, `trello_list_started`, `trello_list_completed`, and generally these should be organized left to right. 

You may need to install some pip modules.  In particular py-trello and scrapy.

```
pip install py-trello
pip install scrapy```

Note: If you are on a Mac, you may need to run `sudo -H pip <module_name>`

At this point you should run it once: `scrapy crawl metacriticnew`

The first time you run it, it won't know which board to write the cards to.  It'll print a list, and you need to set the `trello_board_id` in the trello_config.ini to the board id (something like 5ad6b2aeefe4420d0283eff0).  

## Populating from Metacritic

Once setup is done run `scrapy crawl metacriticnew` from the root directory of this repo.  You should see a bunch of scrapy output and cards should start showing up on your trello board.  When it is complete you'll have a full list of cards

## Updating status based on TrueAchievements collection

Once the board is populated, you can update the status of cards using your existing TrueAchievements account.  First download a csv file of your game collection and then run `python apply_true_achievements_status.py <PathTo_MyGameCollectionFile.csv>`  This will move the cards to different columns based on whether you own the game, have played the game, and have completed the game.  It will update cards by moving them to new lists based on whether they are in your collection, and have >0% of the achievements and 100% of the achievements.  It will only move cards to the right, and only to columns specified in the trello_config.ini file.  So you can have multiple _playing_ lists, with the one specified in the trello_config.ini to the left of the other _playing_ lists.

## TODO

Features I plan to add:
  * Automatic download of the collection file from TrueAchievements
  * Sales tracking (using StoreParser or other sites)
  * XBox 360 and other platforms
  * Fuzzy matching of game titles (currently it's exact match only)