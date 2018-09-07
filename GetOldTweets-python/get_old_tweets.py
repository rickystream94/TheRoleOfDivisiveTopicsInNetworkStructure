from __future__ import print_function
import sys
import argparse
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

import datetime
import json
import tweepy

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
    if b - time_window < earliest_dt:
        a = earliest_dt
    else:
        a = b - time_window

    keep_looking = True
    while keep_looking:
        # search only between times a and b
        astring = a.strftime(date_format)
        bstring = b.strftime(date_format)
        tweets_to_go = n_tweets - n_hits
        if tweets_to_go <= 0:
            print("Reached max number of tweets.")
            return

        print("Searching between %s and %s for maximum %d tweets." % (astring, bstring, tweets_to_go))
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(term).setSince(astring).setUntil(bstring).setMaxTweets(tweets_to_go)

        # If any hits, iterate through them and get full tweets from api
        hits = got.manager.TweetManager.getTweets(tweetCriteria)[:tweets_to_go]
        print("  Found %d tweets in period, %d in total." % (len(hits), n_hits))
        for tweetchunk in iterchunks(hits, chunksize=100):
            tweetIDs = [int(t.id) for t in tweetchunk]
            tweets = api.statuses_lookup(tweetIDs)
            for tweet in tweets:
                n_hits += 1
                yield tweet

        # New time interval to look into
        one_day = datetime.timedelta(days=1)
        if a - (time_window + one_day) < earliest_dt:
            a = earliest_dt
        else:
            a -= time_window + one_day
        if b - (time_window + one_day) <= a:
            keep_looking = False
            print("Reached end of timeframe.")
        else:
            b -= time_window + one_day

    return

# TODO
def tweet_cleaner(tweet):
    return tweet

if __name__ == '__main__':
    print("Launching %s with %d arguments: %s" %(sys.argv[0], len(sys.argv)-1, str(sys.argv[1:])))

    # Set additional global variables
    output_filename = "tweets.json"
    date_format = "%Y-%m-%d"
    time_window = datetime.timedelta(days=7)

    # Parsing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="The term to query for in the tweets text")
    parser.add_argument("maxTweets", help="Maximum number of tweets to download", type=int)
    parser.add_argument("startDate", help="The earliest date to look into for matching tweets (in yyyy-mm-dd format)")
    parser.add_argument("-endDate", help="The latest date to look into for matching tweets (in yyyy-mm-dd format). Default is today")
    args = parser.parse_args()
    EARLIEST = datetime.datetime.strptime(args.startDate, date_format).strftime(date_format) # Validate date format
    if args.endDate != None:
        LATEST = datetime.datetime.strptime(args.endDate, date_format).strftime(date_format) # Validate date format
    else:
        LATEST = datetime.datetime.now().strftime(date_format)
    TERM = args.term
    N_TWEETS = args.maxTweets
    print("Term to query for: %s" % TERM)
    print("Max number of tweets: %d" % N_TWEETS)
    print("Earliest date: %s" % EARLIEST)
    print("Latest date: %s" % LATEST)

    # Setup tweepy API
    with open("twitter_credentials.json") as credentials_file:
        credentials = json.load(credentials_file)

    auth = tweepy.AppAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
    auth.secure = True
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Start main program
    print("=== Looking for maximum %d tweets matching <%s>. ===" % (N_TWEETS, TERM))
    n_hits = 0
    with open(output_filename, "w") as f:
        for tweet in smartquery(term=TERM, before=LATEST, after=EARLIEST, n_tweets=N_TWEETS):
            line = json.dumps(tweet._json)
            f.write(line+"\n")
            n_hits += 1

    print("Done - found %d tweets.\nSaved tweets in %s" %(n_hits, output_filename))