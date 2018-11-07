from __future__ import print_function
import sys
import os
import logging
import argparse
import got3 as got
import datetime
import json
import tweepy
import re
import time
from urllib.error import HTTPError

# Set global variables and settings
script_dir = os.path.dirname(os.path.realpath(__file__))
output_filename_format = "tweets_{0}_{1}_{2}.json"
output_folder_name = "out"
log_filename = "log.txt"
date_format = "%Y-%m-%d"
logging.basicConfig(
    format='%(asctime)s  %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(script_dir,log_filename),mode="a")
    ]
)
logging.getLogger('requests').setLevel(logging.ERROR) # Hides tweepy informational output

def iterchunks(stuff, chunksize):
    i = 0
    while i < len(stuff):
        yield stuff[i: i+chunksize]
        i += chunksize

def smartquery(term, before, after, n_tweets=30):
    n_hits = 0

    # Earliest allowed datetime
    earliest_dt = datetime.datetime.strptime(after, date_format)

    # Setting interval to look within
    b = datetime.datetime.strptime(before, date_format)
    if b - TIME_WINDOW < earliest_dt:
        a = earliest_dt
    else:
        a = b - TIME_WINDOW

    keep_looking = True
    while keep_looking:
        # search only between times a and b
        astring = a.strftime(date_format)
        bstring = b.strftime(date_format)
        tweets_to_go = n_tweets - n_hits
        if tweets_to_go <= 0:
            logging.info("Reached max number of tweets.")
            return

        logging.info("Searching between {0} and {1} for maximum {2} tweets.".format(astring, bstring, tweets_to_go))
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(term).setSince(astring).setUntil(bstring).setMaxTweets(tweets_to_go)

        try:
            # If any hits, iterate through them and get full tweets from api
            hits = got.manager.TweetManager.getTweets(tweetCriteria)[:tweets_to_go]
            logging.info("Found {0} tweets in period, {1} in total.\n".format(len(hits), n_hits))
            for tweetchunk in iterchunks(hits, chunksize=100):
                tweetIDs = [int(t.id) for t in tweetchunk]
                tweets = api.statuses_lookup(tweetIDs)
                for tweet in tweets:
                    n_hits += 1
                    tweet = tweet_cleaner(tweet)
                    yield tweet
                    
            # New time interval to look into
            if a - TIME_WINDOW < earliest_dt:
                a = earliest_dt
            else:
                a -= TIME_WINDOW
            if b - TIME_WINDOW < a:
                keep_looking = False
                logging.info("Reached end of timeframe.")
            else:
                b -= TIME_WINDOW
        except HTTPError as ex:
            logging.info("HTTP ERROR: {0}. Sleeping for 300 seconds before trying again...".format(ex))
            time.sleep(300)
        except Exception as ex:
            logging.info("UNEXPECTED EXCEPTION: {0}. Shutting down.".format(ex))
            sys.exit(1)

    return

# Function used to clean the tweets prior to saving them to disk (save disk space and remove unneeded fields)
def tweet_cleaner(tweet):
    # Transform object to dict
    if not isinstance(tweet, dict):
        tweet = tweet._json

    # Clean tweet (and recursively clean all existing Tweet objects referenced by the Tweet)
    cleaned_tweet = {attr:tweet[attr] for attr in tweet_attrs if attr in tweet}
    if "retweeted_status" in tweet:
        cleaned_tweet["retweeted_status"] = tweet_cleaner(tweet["retweeted_status"])
    if "quoted_status" in tweet:
        cleaned_tweet["quoted_status"] = tweet_cleaner(tweet["quoted_status"])
    cleaned_tweet["user"] = {attr:tweet["user"][attr] for attr in user_attrs if attr in tweet["user"]}
    cleaned_tweet["entities"] = {attr:tweet["entities"][attr] for attr in entities_attrs if attr in tweet["entities"]}
    cleaned_tweet["entities"]["hashtags"] = [hashtag["text"] for hashtag in tweet["entities"]["hashtags"] if "text" in hashtag]
    cleaned_tweet["entities"]["user_mentions"] = [{attr:user_mention[attr] for attr in user_mention if attr in user_mention_attrs} for user_mention in tweet["entities"]["user_mentions"]]

    # Strip URLs from the tweet text
    cleaned_tweet["text"] = re.sub(r'https?://\S*', '', tweet["text"]).strip()
    cleaned_tweet["text"] = re.sub(r'pic\.twitter\.com/\S*', '', cleaned_tweet["text"]).strip()
    return cleaned_tweet

if __name__ == '__main__':
    logging.info("Launching {0} with {1} arguments: {2}".format(sys.argv[0], len(sys.argv)-1, str(sys.argv[1:])))

    # Parsing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="The term to query for in the tweets text")
    parser.add_argument("maxTweets", help="Maximum number of tweets to download", type=int)
    parser.add_argument("startDate", help="The earliest date to look into for matching tweets (in yyyy-mm-dd format)")
    parser.add_argument("-endDate", help="The latest date to look into for matching tweets (in yyyy-mm-dd format). Default is today")
    parser.add_argument("-timeWindow", help="The whole period from startDate to endDate will be split in time windows of 'timeWindow' days. Default is 7 days.")
    args = parser.parse_args()
    EARLIEST = datetime.datetime.strptime(args.startDate, date_format).strftime(date_format) # Validate date format
    if args.endDate != None:
        LATEST = datetime.datetime.strptime(args.endDate, date_format).strftime(date_format) # Validate date format
    else:
        LATEST = datetime.datetime.now().strftime(date_format)
    if args.timeWindow != None:
        TIME_WINDOW = datetime.timedelta(days=int(args.timeWindow))
    else:
        TIME_WINDOW = datetime.timedelta(days=7)
    TERM = args.term
    N_TWEETS = args.maxTweets
    tab_format = "{0: <30}: {1}"
    logging.info(tab_format.format("Term to query for",TERM))
    logging.info(tab_format.format("Max number of tweets", N_TWEETS))
    logging.info(tab_format.format("Earliest date", EARLIEST))
    logging.info(tab_format.format("Latest date", LATEST))
    logging.info(tab_format.format("Time window (days)", TIME_WINDOW))

    # Set dynamic output folder and filename
    output_folder_path = os.path.join(script_dir, output_folder_name)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    output_filename = output_filename_format.format(TERM,EARLIEST,LATEST)
    output_filepath = os.path.abspath(os.path.join(output_folder_path, output_filename))
    logging.info("Tweets will be saved in {0}.".format(output_filepath))

    # Setup tweepy API
    with open(os.path.join(script_dir,"twitter_credentials.json")) as credentials_file:
        credentials = json.load(credentials_file)

    auth = tweepy.AppAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
    auth.secure = True
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # For each Twitter API object, get the list of relevant attributes to keep
    with open(os.path.join(script_dir,"twitter_object_dictionaries.json")) as twitter_dictionaries_file:
        twitter_dicts = json.load(twitter_dictionaries_file)
    tweet_attrs = twitter_dicts["tweet"]
    user_attrs = twitter_dicts["user"]
    entities_attrs = twitter_dicts["entities"]
    user_mention_attrs = twitter_dicts["user_mention"]

    # Start main program
    logging.info("=== Looking for maximum {0} tweets matching <{1}>. ===\n".format(N_TWEETS, TERM))
    n_hits = 0
    with open(output_filepath, "a") as f:
        for tweet in smartquery(term=TERM, before=LATEST, after=EARLIEST, n_tweets=N_TWEETS):
            line = json.dumps(tweet)
            f.write(line+"\n")
            n_hits += 1
    logging.info("Done - found {0} tweets.\nSaved tweets in {1}".format(n_hits, output_filepath))
