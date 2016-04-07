FROM python:2.7
MAINTAINER Fiona Hasanaj
        
RUN apt-get -y update && apt-get install -y vim  && apt-get install -y git && pip install rosette_api && pip install -U pip && pip install TwitterSearch

# copy over the necessary files
COPY run_python.sh /python-dev/run_python.sh
RUN chmod 755 /python-dev/run_python.sh
WORKDIR /python-dev

# allow interactive bash inside docker container
CMD ./run_python.sh

VOLUME ["/source"]