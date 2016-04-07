#!/usr/bin/env python

import argparse

import html_parser
import text_sentiment as ts
import face_sentiment as fs


def get_confidence(item, key):
    if item[u'label'] == key:
        return item[u'confidence']


def negative(sentiment, limit = 0.50):
    if type(sentiment) is list:
        return sentiment[0][u'label'] == u'neg'
    else:
        return sentiment[u'label'] == u'neg'
    #return get_confidence(sentiment, 'neg') > limit

def positive(sentiment, limit = 0.50):
    if type(sentiment) is list:
        return sentiment[0][u'label'] == u'pos'
    else:
        return sentiment[u'label'] == u'pos'
    #return get_confidence(sentiment, 'pos') > limit

def detect_sarcasm(text_sentiment, face_sentiment, ocr_sentiment):
    result = False
    if text_sentiment is None:
        return False
    if face_sentiment is None and ocr_sentiment is None:
        return False
    if positive(text_sentiment[u'document']):
        if ocr_sentiment is not None:
            if negative(ocr_sentiment[u'document'], 0.55):
                result = True
        elif negative(face_sentiment):
            result = True
    else: # negative(text_sentiment)
        if ocr_sentiment is not None:
            if positive(ocr_sentiment[u'document'], 0.55):
                result = True
        elif positive(face_sentiment):
            result = True
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', required=True, help='the Google Vision API key',
                        metavar='GOOGLE_VISION_KEY')
    parser.add_argument('-j', '--json',
                        help='a file containing a Twitter API response in JSON format')
    parser.add_argument('-q', '--query', help='a string to search for')
    parser.add_argument('-r', required=True, help='the Rosette API key',
                        metavar='ROSETTE_API_KEY')
    parser.add_argument('--tk', required=True, help='the Twitter API key',
                        metavar='TWITTER_API_KEY')
    parser.add_argument('--ts', required=True, help='the Twitter API secret',
                        metavar='TWITTER_API_SECRET')
    parser.add_argument('--tt', required=True,
                        help='the Twitter API access token', metavar='TWITTER_TOKEN')
    parser.add_argument('--tts', required=True,
                        help='the Twitter API access token secret',
                        metavar='TWITTER_TOKEN_SECRET')
    args = parser.parse_args()
    tweets = html_parser.split(args)
    sarcastic_tweet_urls = []
    for tweet in tweets:
        text_sentiment = ts.detect(tweet[0], args)
        face_sentiment, ocr_sentiment = fs.detect(tweet[1], args)

        print('TWEET: ' + tweet[2].encode('utf-8') + ': ' + tweet[0].encode('utf-8'))
        print('TEXT SENTIMENT: ' + str(text_sentiment))
        print('FACE SENTIMENT: ' + str(face_sentiment))
        print('OCR SENTIMENT: ' + str(ocr_sentiment))
        if detect_sarcasm(text_sentiment, face_sentiment, ocr_sentiment):
            print('Sarcastic!')
            sarcastic_tweet_urls.append(tweet[2])

    print('\nSarcastic tweets:')
    for sarcastic_tweet_url in sarcastic_tweet_urls:
        print(sarcastic_tweet_url)

if __name__ == '__main__':
    main()

