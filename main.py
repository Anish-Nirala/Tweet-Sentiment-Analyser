import collections
import tweepy
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import cleanTweets
import Lemmatizer
import Polarity

credential = collections.defaultdict(str)
with open('credentials.txt', 'r') as f:
    for line in f.readlines():
        key, value = line.split("=")
        credential[key.strip()] += value.strip()

auth = tweepy.OAuthHandler(
    credential['consumerKey'], credential['consumerSecret'])
auth.set_access_token(credential['accessToken'],
                      credential['accessTokenSecret'])
api = tweepy.API(auth)


searchTerm = input("Enter Keyword/Tag to search about: ")
NoOfTerms = int(input("Enter how many tweets to search: "))

tweets = []
tweetText = []
tweets = tweepy.Cursor(api.search, q=searchTerm +
                       " -filter:retweets", lang="en").items(NoOfTerms)

tweet_list = [tweet.text for tweet in tweets]
tweet_df = pd.DataFrame(tweet_list)

tweet_df['cleaned_tweet'] = tweet_df[0].apply(cleanTweets().clean_text)

tweet_df['cleaned_tweet'] = tweet_df['cleaned_tweet'].apply(
    cleanTweets().drop_numbers)

tweet_df['cleaned_tweet'] = tweet_df['cleaned_tweet'].apply(
    Lemmatizer().lemmatise)

tweet_df['cleaned_tweet'] = tweet_df['cleaned_tweet'].apply(
    Lemmatizer().remove_stopword)

tweet_df['polarity'] = tweet_df['cleaned_tweet'].apply(Polarity().get_polarity)

neutral_tweets = 0
weakly_positive_tweets = 0
strongly_positive_tweets = 0
positive_tweets = 0
negative_tweets = 0
weakly_negative_tweets = 0
strongly_negative_tweets = 0
polarity = 0

for i in range(0, NoOfTerms):
    textblob = TextBlob(str(tweet_df['cleaned_tweet'][i]))
    polarity += textblob.sentiment.polarity
    pol = textblob.sentiment.polarity
    if (pol == 0):
        neutral_tweets += 1
    elif (pol > 0 and pol <= 0.3):
        weakly_positive_tweets += 1
    elif (pol > 0.3 and pol <= 0.6):
        positive_tweets += 1
    elif (pol > 0.6 and pol <= 1):
        strongly_positive_tweets += 1
    elif (pol > -0.3 and pol <= 0):
        weakly_negative_tweets += 1
    elif (pol > -0.6 and pol <= -0.3):
        negative_tweets += 1
    elif (pol > -1 and pol <= -0.6):
        strongly_negative_tweets += 1


def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')


positive_tweets = percentage(positive_tweets, NoOfTerms)
weakly_positive_tweets = percentage(weakly_positive_tweets, NoOfTerms)
strongly_positive_tweets = percentage(strongly_positive_tweets, NoOfTerms)
negative_tweets = percentage(negative_tweets, NoOfTerms)
weakly_negative_tweets = percentage(weakly_negative_tweets, NoOfTerms)
strongly_negative_tweets = percentage(strongly_negative_tweets, NoOfTerms)
neutral_tweets = percentage(neutral_tweets, NoOfTerms)


print("How people are reacting on " + searchTerm +
      " by analyzing " + str(NoOfTerms) + " tweets.")
print()
print("-----------------------------------------------------------------------------------------")
print()
print("General Report: ")

if (polarity == 0):
    print("Neutral")
elif (polarity > 0 and polarity <= 0.3):
    print("Weakly Positive")
elif (polarity > 0.3 and polarity <= 0.6):
    print("Positive")
elif (polarity > 0.6 and polarity <= 1):
    print("Strongly Positive")
elif (polarity > -0.3 and polarity <= 0):
    print("Weakly Negative")
elif (polarity > -0.6 and polarity <= -0.3):
    print("Negative")
elif (polarity > -1 and polarity <= -0.6):
    print("Strongly Negative")

print()
print("------------------------------------------------------------------------------------------")
print()
print("Detailed Report: ")
print(str(positive_tweets) + "% people thought it was positive")
print(str(weakly_positive_tweets) + "% people thought it was weakly positive")
print(str(strongly_positive_tweets) +
      "% people thought it was strongly positive")
print(str(negative_tweets) + "% people thought it was negative")
print(str(weakly_negative_tweets) + "% people thought it was weakly negative")
print(str(strongly_negative_tweets) +
      "% people thought it was strongly negative")
print(str(neutral_tweets) + "% people thought it was neutral")


sizes = [positive_tweets, weakly_positive_tweets, strongly_positive_tweets,
         neutral_tweets, negative_tweets, weakly_negative_tweets, strongly_negative_tweets]
colors = ['yellowgreen', 'lightgreen', 'darkgreen',
          'gold', 'red', 'lightsalmon', 'darkred']
labels = ['Positive [' + str(positive_tweets) + '%]', 'Weakly Positive [' + str(weakly_positive_tweets) + '%]',
          'Strongly Positive [' + str(strongly_positive_tweets) +
          '%]', 'Neutral [' + str(neutral_tweets) + '%]',
          'Negative [' + str(negative_tweets) + '%]', 'Weakly Negative [' +
          str(weakly_negative_tweets) + '%]',
          'Strongly Negative [' + str(strongly_negative_tweets) + '%]']

plt.pie(sizes, labels=labels, colors=colors)
plt.legend(labels, loc="best")
plt.title('How people are reacting on ' + searchTerm +
          ' by analyzing ' + str(NoOfTerms) + ' Tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show()
