from subprocess import Popen, PIPE

SCRIPT_NAME = "get_old_tweets.py"
MAX_TWEETS = 10000000
FROM = "2013-09-01"
TO = "2016-12-31"

with open("hashtags.txt") as hashtags:
    for h in hashtags:
        print("=== DOWNLOADING TWEETS FOR HASHTAG {0} ===".format(h))
        p = Popen([SCRIPT_NAME, h, MAX_TWEETS, FROM, "-endDate", TO], stdout=PIPE)
        print(p.communicate())
print("=== COMPLETED ===")
