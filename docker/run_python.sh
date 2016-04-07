#!/bin/bash

#Gets called when the user doesn't provide any args
function HELP {
    echo -e "\nusage: graeae.py [-j JSON]  [-q QUERY] -g GOOGLE_VISION_KEY -r ROSETTE_API_KEY --tk TWITTER_API_KEY --ts TWITTER_API_SECRET --tt TWITTER_TOKEN --tts TWITTER_TOKEN_SECRET"
    echo "  j    - File containing a Twitter API response in JSON format (optional)"
    echo "  q    - String to search for (optional)"
    echo "  g    - Google Vision API key (required)"
    echo "  r    - Rosette API key (required)"
    echo "  tk   - Twitter API key (required)"
    echo "  ts   - Twitter API secret (required)"
    echo "  tt   - Twitter API access token (required)"
    echo "  tts  - Twitter API access token secret (required)"
    exit 1
}

#Gets API_KEY, FILENAME and ALT_URL if present
while getopts ":j:q:g:r:tk:ts:tt:tts" arg; do
    case "${arg}" in
    	j)
            j=${OPTARG}
            usage
            ;;
        q)
            q=${OPTARG}
            usage
            ;;
        g)
            g=${OPTARG}
            usage
            ;;
        r)
            r=${OPTARG}
            usage
            ;;
        tk)
        	tk={OPTARG}
            usage
            ;;
        ts)
        	ts={OPTARG}
            usage
            ;;
        tt)
        	tt={OPTARG}
            usage
            ;;
        tts)
        	tts={OPTARG}
            usage
            ;;
    esac
done

ping_url="https://api.rosette.com/rest/v1"

#Checks if Rosette API key is valid
function checkAPI {
    match=$(curl "${ping_url}/ping" -H "X-RosetteAPI-Key: ${r}" |  grep -o "forbidden")
    if [ ! -z $match ]; then
        echo -e "\nInvalid Rosette API Key"
        exit 1
    fi  
}

#Copy the mounted content in /source to current WORKDIR
cp -r -n /source/* .

#Run the examples
if [ ! -z ${r} ]; then
    checkAPI
    cd /python-dev
    if [ ! -z ${q} ]; then
    	python graeae.py -g ${g} -q ${q} -r ${r} --tk ${tk} --ts ${ts} --tt ${tt} --tts ${tts}
    elif [ ! -z ${j} ]; then
    	python graeae.py -g ${g} -j ${j} -r ${r} --tk ${tk} --ts ${ts} --tt ${tt} --tts ${tts}
    else
    	echo -e "\nPlease provide a Twitter search query or a local Twitter JSON file!"
    fi
else 
    HELP
fi
