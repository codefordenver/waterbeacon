
from waterquality.celery import app
from datetime import datetime, timedelta
from utils.log import log
from news import models
from annoying.functions import get_object_or_None
import feedparser
from utils.utils import (
    remove_stopwords,
)
from utils.log import log

import tweepy


def save_twitter_data(tweet, location  ):
    # ref: https://dev.twitter.com/overview/api/tweets

    tw = models.tweet()
    tw.location = location
    tw.text = tweet.text
    tw.sourceId = tweet.id_str

    #tw.url =
    tw.created =  tweet.created_at
    tw.save()

    if tweet.entities.get('urls'):
        for item in tweet.entities['urls']:
            url = models.url()
            url.tweet = tw
            url.link = item['url']
            url.save()

    print tweet.text
    #log(tweet.text, 'success')

@app.task
def TweetWaterAdvisoryReader(
            consumer_key = 'JCoLgJS4SFK4ErLyTPxrshzdJ',
            consumer_secret = 'ZgEM4iw6YOX2B11k7d7QPYIHshivaXr9ZJUYaeZ4jh7LYCCJed',
            access_token = '2438688577-F9iaLScxyvm4Bq6irsCOdX95gPMsJc4KRA0c1V8',
            access_token_secret = 'D5RIThJdgipTejcp3GQ4RVdPhnbiiy2IAN4AZDrYy7QtS',
            frequency_minutes = 5,
            max_tweets = 100,
            days_ago = 5):

    WATER_ADVISORY_KEYWORDS = [
        'boil advisory',
        'do not drink',
        'do not use',
        'informational'
    ]

    # get today's date
    today = datetime.now().date()

    # get the date of days ago
    past = datetime.today() - timedelta(days = days_ago)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    for advisory in WATER_ADVISORY_KEYWORDS:
        for location in models.location.objects.all():
            query = "%s %s %s" % (advisory, location.city, location.keywords)
            geocode = location.geocode

            for tweet in tweepy.Cursor(api.search,q=query.strip(),geocode = geocode, since= past.strftime('%Y-%m-%d'), lang='en').items(max_tweets):
                save_twitter_data(tweet, location)
