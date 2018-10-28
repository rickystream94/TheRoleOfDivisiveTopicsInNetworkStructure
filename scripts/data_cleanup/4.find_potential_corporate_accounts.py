import tweepy
import os
import json
import sys
import time
import nltk
import string
import re

# Global variables
companies_filename = "../../data/data_cleanup/found_companies.csv"
output_filename = "../../data/data_cleanup/found_companies_metadata.csv"
with open("../../data/data_cleanup/twitter_description_keywords.txt") as keywords_f:
    keywords = [k.strip('\n').lower() for k in keywords_f]

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

def find_potential_corporate_accounts(start_from_line=0):
    
    # Setup tweepy API
    with open("../../lib/GetOldTweets-python/twitter_credentials.json") as credentials_file:
        credentials = json.load(credentials_file)

    auth = tweepy.AppAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
    auth.secure = True
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    count = start_from_line
    skipped = 0 # Keep track of how many users were not found
    with open(companies_filename) as companies_f:
        with open(output_filename, "a") as out_f:
            print("Starting from line {0}".format(start_from_line))
            for chunk in read_large_file(companies_f, start_from_line):
                success = False
                while not success:
                    try:
                        users = api.lookup_users(screen_names=[el.split(',')[0] for el in chunk])
                        skipped += len(chunk) - len(users)
                        success = True
                    except tweepy.TweepError as ex:
                        if ex.api_code == 17:
                            skipped += len(chunk)
                            #for el in chunk:
                            #    out_f.write(",".join([el,str(False),str(0),str(0)]))
                            continue
                        print("Twitter error: '{0}', sleeping for 300 seconds...".format(ex.args[0][0]['message']))
                        time.sleep(300)
                for el in chunk:
                    username = el.split(',')[0]
                    for user in users:
                        if username == user._json["screen_name"].lower():
                            is_user_verified = user._json["verified"]
                            user_description = user._json["description"]
                            statuses_count = user._json["statuses_count"]
                            num_matching_keywords = get_num_matching_keywords(user_description)
                            out_f.write(",".join([el,str(is_user_verified),str(statuses_count),str(num_matching_keywords)]) + "\n")
                count +=len(chunk)
                if count % 500 == 0:
                    print("Currently processed {0} usernames...".format(count))
    print("Done! Processed {0} usernames.\nSkipped {1} usernames (not found).".format(count, skipped))

def get_num_matching_keywords(description):
    if description is None or description == "":
        return 0
    description = description.translate(str.maketrans('','',string.punctuation)) # Python 3 version to remove punctuation
    all_words = nltk.tokenize.word_tokenize(description) # Tokenize text
    all_words_dist = nltk.FreqDist(w.lower() for w in all_words) # Compute word frequency distribution
    matching_keywords = 0
    for keyword in keywords:
        if keyword in all_words_dist:
            matching_keywords += all_words_dist[keyword] # Count how many total keywords are used in the description text
     
    # Special case: sometimes there are opening hours with AM/PM suffixes:
    for word in all_words_dist:
        if re.match(r'.*\d+[aApP][mM]', word):
            matching_keywords += all_words_dist[word]
    
    return matching_keywords
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        start_from_line = sys.argv[1]
    else:
        start_from_line = 0
    find_potential_corporate_accounts(int(start_from_line))