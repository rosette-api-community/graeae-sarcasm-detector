__all__ = ['detect']

from rosette import api


ROSETTE_SERVICE_URL = 'https://api.rosette.com/rest/v1'

def detect(text, args):
    """
    Return the sentiment of a piece of text.
    """
    text = text or 'Rosette API is the best! #iloverosette'
    api_instance = api.API(args.r, ROSETTE_SERVICE_URL)
    params = api.DocumentParameters()
    params['content'] = text
    params['language'] = 'eng'
    return api_instance.sentiment(params)

