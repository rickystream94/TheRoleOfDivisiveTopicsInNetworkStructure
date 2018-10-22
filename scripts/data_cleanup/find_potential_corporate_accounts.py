import tweepy
import os
import json
import sys
import time

def read_large_file(file_object, start_from_line):
    chunk = []
    count = 0
    while True:
        data = file_object.readline()
        if count < start_from_line:
            count += 1
            continue
        if not data:
            if len(chunk) != 0:
                yield chunk
            break
        if len(chunk) != 100:
            chunk.append(data.rstrip('\n'))
        else:
            yield chunk
            chunk = []

def get_verified_accounts(start_from_line=0):
    companies_filename = "../../data/found_companies.csv"
    output_filename = "../../data/potential_companies.csv"
    
    # Setup tweepy API
    with open("../lib/GetOldTweets-python/twitter_credentials.json") as credentials_file:
        credentials = json.load(credentials_file)

    auth = tweepy.AppAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
    auth.secure = True
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    with open(companies_filename) as companies_f:
        with open(output_filename, "a") as out_f:
            count = start_from_line
            print("Starting from line {0}".format(start_from_line))
            for chunk in read_large_file(companies_f, start_from_line):
                success = False
                while not success: 
                    try:
                        users = api.lookup_users(screen_names=[el.split(',')[0] for el in chunk])
                        success = True
                    except tweepy.TweepError as ex:
                        print("Twitter error: '{0}', sleeping for 300 seconds...".format(ex.args[0][0]['message']))
                        time.sleep(300)
                verified_lines = [el for el in chunk for user in users if el.split(',')[0] == user._json["screen_name"].lower() and user._json["verified"]]
                for verified_line in verified_lines:
                    out_f.write(verified_line + "\n")
                count +=len(chunk)
                if count % 5000000 == 0:
                    print("Currently processed {0} usernames...".format(count))
    print("Done! Processed {0} usernames.".format(count))

if __name__ == '__main__':
    start_from_line = sys.argv[1]
    get_verified_accounts(int(start_from_line))