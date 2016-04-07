__all__ = ['detect']

import json
import requests

import text_sentiment


#From https://cloud.google.com/vision/reference/rest/v1/images/annotate#Likelihood
#UNKNOWN 	Unknown likelihood.
#VERY_UNLIKELY 	The image very unlikely belongs to the vertical specified.
#UNLIKELY 	The image unlikely belongs to the vertical specified.
#POSSIBLE 	The image possibly belongs to the vertical specified.
#LIKELY 	The image likely belongs to the vertical specified.
#VERY_LIKELY 	The image very likely belongs to the vertical specified.

likelihood_map = {
    u'UNKNOWN': 0.5,
    u'VERY_UNLIKELY': 0.0,
    u'UNLIKELY': 0.25,
    u'POSSIBLE': 0.6,
    u'LIKELY': 0.75,
    u'VERY_LIKELY': 1.0,
}

emotions = {
    u'joyLikelihood': u'pos',
    u'sorrowLikelihood': u'neg',
    u'angerLikelihood': u'neg',
}


def face_sentiment(face):
    sentiments = {}
    for emotion, sentiment in emotions.iteritems():
        emotion_likelihood = likelihood_map.get(face.get(emotion))
        if sentiment not in sentiments or sentiments[sentiment] < emotion_likelihood:
            sentiments[sentiment] = emotion_likelihood
    likelihood_sum = sum(likelihood for likelihood in sentiments.itervalues())
    return sorted([
            {
                u'label': label,
                u'confidence': confidence / likelihood_sum
                    if likelihood_sum != 0.0
                    else 0.0,
            } for label, confidence in sentiments.iteritems()
        ], key=lambda d: d.get(u'confidence'), reverse=True)


def likelySentiment(response, args):
    annotations = response.json().get('responses')[0]
    faces = None
    text = None
    face_count = 0
    try:
        faces = annotations.get('faceAnnotations')
        face_count = len(faces)
    except TypeError:
        pass  # no faces
    try:
        text = annotations.get(u'textAnnotations')[0].get(u'description')
    except:
        pass  # no OCR text
    rv = [None, None]
    if face_count != 1 and text is None:
        print('Rejecting image containing %d faces and no text' % face_count)
    else:
        if face_count == 1:
            rv[0] = face_sentiment(faces[0])
        if text is not None:
            print('OCR: %s' % text.encode('utf-8'))
            rv[1] = text_sentiment.detect(text, args)
    return tuple(rv)


def detect(image, args):
    """
    Return sentiment based on the face in a base64-encoded image, or
    None if there is no face.
    """
    data = {
        'requests':[
            {
                'image': {'content': image},
                'features':[
                    {
                        'type': 'FACE_DETECTION',
                        'maxResults': 2,
                    },
                    {
                        'type': 'TEXT_DETECTION',
                        'maxResults': 1,
                    },
                ]
            }
        ]
    }
    r = requests.post('https://vision.googleapis.com/v1/images:annotate?key=' + args.g,
                      data=json.dumps(data))

    if r.status_code != 200:
        print 'error status ' + str(r.json())
        return None
    else:
        return likelySentiment(r, args)

