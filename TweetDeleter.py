#!/usr/bin/env python
 
import tweepy
from datetime import datetime, timedelta
 
## OPTIONS
test_mode = False # Setting this to False will actually undertake the actions
verbose = False
delete_tweets = True # Do we want to delete tweets?
delete_favs = True # Do we want to delete favorites
days_to_keep = 7 # How many days tweets to keep?

# Enter IDs of tweets you want to preserve here
tweets_to_save = [
]

# Enter IDS of favorites you want to preserve here
favs_to_save = [
]
 
# Fill in the keys for your Twitter app
consumer_key = 'XXXXXXXX'
consumer_secret = 'XXXXXXXX'
access_token = 'XXXXXXXX'
access_token_secret = 'XXXXXXXX'

## OPTIONS END HERE

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
 
# Set cut off date for deleting tweets and use UTC to match Twitter
cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
 
# If selected, delete old tweets
if delete_tweets:
    # Pull in all tweets from the users timeline
    print "Retrieving timeline tweets"
    timeline = tweepy.Cursor(api.user_timeline).items()
    deletion_count = 0
    ignored_count = 0
 
    for tweet in timeline:
        # Where tweets are not in save list and older than cutoff date
        if tweet.id not in tweets_to_save and tweet.created_at < cutoff_date:
	    # Are we being chatty?
            if verbose:
                print "Deleting %d: [%s] %s" % (tweet.id, tweet.created_at, tweet.text)
	    # If we're not in test mode, actually delete the tweet
            if not test_mode:
                api.destroy_status(tweet.id)           
            deletion_count += 1
        else:
            ignored_count += 1

    # Advise how many tweets have been deleted, and ignored.
    print "Deleted %d tweets, ignored %d" % (deletion_count, ignored_count)
else:
    print "Not deleting tweets"
     
# If selected, delete old favorites
if delete_favs:
    # Get all favorites
    print "Retrieving favorite tweets"
    favorites = tweepy.Cursor(api.favorites).items()
    unfav_count = 0
    kept_count = 0
 
    for tweet in favorites:
        # Where tweets are not in save list and older than cutoff date
        if tweet.id not in favs_to_save and tweet.created_at < cutoff_date:
            if verbose:
                print "Unfavoring %d: [%s] %s" % (tweet.id, tweet.created_at, tweet.text)
            if not test_mode:
                api.destroy_favorite(tweet.id)
           unfav_count += 1
        else:
            kept_count += 1

    # Advise how many favorites have been removed, and kept.
    print "Unfavored %d tweets, ignored %d" % (unfav_count, kept_count)
else:
    print "Not unfavoring tweets"
