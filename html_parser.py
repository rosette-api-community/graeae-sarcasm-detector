__all__ = ['split']

from TwitterSearch import *
import base64
import io
import json
import urllib


def process_tweets(tweet_iter):
    rv = []
    for tweet in tweet_iter:
        try:
            text = tweet[u'text']
            image_url = tweet[u'entities'][u'media'][0][u'media_url_https']
            image = urllib.urlopen(image_url)
            image_base64 = base64.encodestring(image.read())
            tweet_url = u'https://twitter.com/statuses/' + tweet[u'id_str']
            rv.append((text, image_base64, tweet_url))
        except KeyError:
            pass
    return rv


def search_twitter(args):
    try:
        # create a TwitterSearchOrder object
        tso = TwitterSearchOrder()
        # let's define all words we would like to have a look for
        tso.set_keywords(args.query.split())
        # we want to see English tweets only
        tso.set_language('en')
        # and don't give us all those entity information
        #tso.set_include_entities(False)

        # it's about time to create a TwitterSearch object with our secret tokens

        ts = TwitterSearch(
            consumer_key = args.tk,
            consumer_secret = args.ts,
            access_token = args.tt,
            access_token_secret = args.tts)

        # this is where the fun actually starts :)
        return ts.search_tweets_iterable(tso)
    # take care of all those ugly errors if there are some
    except TwitterSearchException as e:
         print(e)
         return []


def split(args):
    """
    Split tweets matching a query into list of 2-tuples of string and
    base64-encoded images.
    """
    tweet_iter = None
    if args.query:
        tweet_iter = search_twitter(args)
    else:
        with io.open(args.json, 'r', encoding='utf-8') as f:
            tweet_iter = [json.loads(f.read())]
    return process_tweets(tweet_iter)

