import tweepy
import time

from environtment import *

print("Bot is running....")

FILE_NAME           = 'last_seen_id.txt'
default_tweet_id    = 1111
sleep_time          = 30


# NOTE: authentication user twitter (BOT)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def checking_file(file_name):
    # NOTE: checking file exist or not. if exist will create one
    try:
        f_write = open('last_seen_id/' + file_name, 'w')
        f_write.write(str(default_tweet_id))
        f_write.close()
    except tweepy.TweepError:
        print('\talready exists !')
    return default_tweet_id

def retrieve_last_seen_id(file_name):
    f_read = open('last_seen_id/' + file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open('last_seen_id/' + file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def retweet(tweet):
    if not tweet.retweeted:
        try:
            tweet.retweet()
            print("\tRetweeted")
        except tweepy.TweepError:
            print('\tAlready Retweeted')
    return


def find_tweet_from(username):
    tweet_count = 0
    print('retrieving tweets...', flush=True)

    try:
        last_seen_id = retrieve_last_seen_id(username+'.txt')
    except:
        last_seen_id =  checking_file(username+'.txt')

    tweets = api.user_timeline(screen_name = username_targeted, since_id = last_seen_id)
    for tweet in reversed(tweets):
        last_seen_id = tweet.id
        store_last_seen_id(last_seen_id, username+'.txt')

        if str(tweet.in_reply_to_screen_name) != "None" and str(tweet.in_reply_to_screen_name) == username:
            tweet_count += 1
            retweet(tweet)

    print(str(tweet_count) + ' times reply tweets from ' + username)


while True:
    for username in usernames:
        find_tweet_from(username)
        time.sleep(5)

    print('sleeping for ' + str(sleep_time) + 's')
    time.sleep(sleep_time)
