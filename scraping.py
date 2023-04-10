
# this code scrapes twitter using snscraper
# it searches for all tweets with the conditions specified in the query variable
 
from sys import argv
from time import time
import pandas as pd
import snscrape.modules.twitter as sntwitter

start = time()

if len(argv) != 4:
    print("Error! Command must be:", argv[0],"<query> <upper bound> <output_filename>") 
    exit()
query = argv[1]
n_tweets = int(argv[2]) # upper bound of tweets to be scraped
output_filename = argv[3]

## scraping

tweets = []
tweet_scraper = sntwitter.TwitterSearchScraper(query)
for i, tweet in enumerate(tweet_scraper.get_items()):
    data = [
        tweet.date,
        tweet.id,
        tweet.rawContent,
        tweet.user.username,
        tweet.place,
        tweet.replyCount,
        tweet.likeCount,
        tweet.retweetCount,
        tweet.retweetedTweet
    ]
    tweets.append(data)
    if i > n_tweets:
        break

## putting data into a dataframe

df = pd.DataFrame(
    tweets, columns=['date','id','content','user','place_id','reply_count','like_count','retweet_count','retweeted_tweet']
)

## exporting data

df.to_csv(output_filename, index=False)

end = time()
total_time = end-start
print("Execution time:"+str(total_time))