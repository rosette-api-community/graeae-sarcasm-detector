# hackathon-graeae
2016 Rosette API Hackathon - Team Graeae

##Prerequisites 

* A valid Rosette API key (if you don't have one, you can get one [here](https://developer.rosette.com/signup))
* A Cloud Vision API key (you can find instructions on how to get started [here](https://cloud.google.com/vision/docs/getting-started))
* Twitter Keys and Access Tokens (including all of the following: API Key, API Secret, Access Token, Access Token Secret which can be obtained [here](https://apps.twitter.com/app))

##Installation

1. Check out this repo to your machine.
2. The project can be run in Docker by following the instructions inside the 'docker' directory or by setting up a developer's environment locally and can be run from there.

##How it Works

The TwitterSearch library iterates throughout all tweets reachable via the Twitter API that match the provided query. The data collected from each tweet is processed through the Rosette API sentiment analyzer and Google Vision simultaneously in order to detect sarcastic tweets. 
