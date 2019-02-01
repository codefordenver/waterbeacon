import requests
from lxml import html
from datetime import datetime, timedelta
from waterquality.celery import app
from datetime import datetime, timedelta
from utils.log import log
from news import models
from annoying.functions import get_object_or_None
import feedparser
from utils.utils import (
    remove_stopwords, cleanhtml
)
from utils.log import log

import tweepy

def status(text):

    if 'lift' in text:
        return 'safe'
    elif 'do not use' in text:
        return 'notuse'
    elif 'do not drink' in text:
        return 'notdrink'
    elif 'boil' in text:
        return 'boil'

    return 'unknown'

def save_twitter_data(tweet, location = None ):
    # https://www.ewg.org/tapwater/index.php#results-by-state-map
    # ref: https://dev.twitter.com/overview/api/tweets

    if models.alert.objects.filter(sourceId = tweet.id_str ).exists():
        print "%s - exists" % ( tweet.text )
        #log(tweet.text, 'success')
        return

    tw = models.alert()

    tw.text = tweet.text
    tw.text_wo_stopwords =  remove_stopwords( tweet.text )
    tw.sourceId = tweet.id_str
    tw.source = 'twitter'
    tw.status = status(tweet.text)
    tw.save()

    if location:
        tw.location = location
        location.status = tw.status
        location.save()

    if tweet.entities.get('urls'):
        for item in tweet.entities['urls']:
            url = models.url()
            url.alert = tw
            url.link = item['url']
            url.save()

    print tweet.text
    #log(tweet.text, 'success')

def save_feed_data(item, location = None):

    sourceId = item['id']
    if models.alert.objects.filter(sourceId = sourceId ).exists():
        print "%s - exists" % ( sourceId )
        #log(sourceId, 'success')
        return

    title = cleanhtml(item['title'])
    summary = cleanhtml(item['summary'])

    published = datetime.strptime(item['published'], '%Y-%m-%dT%H:%M:%SZ')
    link = item['link']

    concat_text = "%s :: %s" % (title, summary )

    alert = models.alert()
    alert.source = 'goog'
    alert.text = concat_text
    alert.text_wo_stopwords =  remove_stopwords( concat_text )
    alert.sourceId = sourceId
    alert.status = status(concat_text)
    alert.save()

    url = models.url()
    url.alert = alert
    url.link = link
    url.save()

    print sourceId
    #log(sourceId, 'success')

@app.task
def NewsFeedReader():

    for advisory in models.advisory_feed.objects.all():
        for item in feedparser.parse(advisory.feed)['entries']:
            save_feed_data(item)

@app.task
def TweetWaterAdvisoryReader(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret,
            max_tweets = 100,
            days_ago = 5,
            skip_locations=False
            ):

    # get today's date
    today = datetime.now().date()

    # get the date of days ago
    past = datetime.today() - timedelta(days = days_ago)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    for advisory in models.advisory_keyword.objects.filter( source = 'twitter'):

        # search for advisory in locations
        if not skip_locations:
            for location in models.location.objects.all():
                query = "\"%s\" %s %s" % (advisory.keyword, location.city, location.keywords)
                geocode = location.geocode

                for tweet in tweepy.Cursor(api.search,q=query.strip(),geocode = geocode, since= past.strftime('%Y-%m-%d'), lang='en').items(max_tweets):
                    save_twitter_data(tweet, location)

        # search for advisory generally
        for tweet in tweepy.Cursor(api.search,q="\"%s\" near:\"United States\"" % (advisory.keyword.strip()), since= past.strftime('%Y-%m-%d'), lang='en').items(max_tweets):
            save_twitter_data(tweet)

@app.task
def EWG_TapwaterReader(stale_updated_days = 30):


    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    for state in states:

        response = requests.get('https://www.ewg.org/tapwater/state.php?stab=%s' % ( state ))
        if response.status_code != 200:
            return []

        parsed = html.fromstring(response.text)
        for utility in parsed.xpath('//div[@id="all-utilities-table"]/table/tbody/tr'):

            # save to database
            o_utility = models.utility()

            # parse utility data
            o_utility.name = utility.xpath('td[@data-label="Utility"]/a/text()')[0].strip()
            o_utility.link = utility.xpath('td[@data-label="Utility"]/a/@href')[0].strip()
            o_utility.location = utility.xpath('td[@data-label="Location"]/text()')[0].strip()
            o_utility.population = utility.xpath('td[@data-label="Population"]/text()')[0].strip()
            o_utility.violation_points = utility.xpath('td[@data-label="Violation Points"]/text()')[0].strip()
            o_utility.save()

            # delete all other utility last updated greater than

    #  utilities that haven't been updated since the stale_updated_days to violation as false
    past = datetime.now() - timedelta(days = stale_updated_days)
    models.utility.objects.filter(last_updated__lt = past).update(violation = False)
