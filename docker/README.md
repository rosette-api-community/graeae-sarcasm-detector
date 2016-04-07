---
# Docker Image for Graeae Project
---
### Summary
To simplify the running of the project and test any local changes to development source.

### Basic Usage
Build the docker image, e.g. `docker build -t basistech/graeae .`

Run it as `docker run -e j=JSON -e q=QUERY -e g=GOOGLE_VISION_KEY -e r=ROSETTE_API_KEY -e tk=TWITTER_API_KEY -e ts=TWITTER_API_SECRET -e tt=TWITTER_TOKEN -e tts=TWITTER_TOKEN_SECRET -v "path-to-local-graeae-dir:/source" basistech/graeae` Remember to provide either a local Twitter file in JSON format or a query to search in Twitter.