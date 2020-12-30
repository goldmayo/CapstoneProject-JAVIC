FROM ubuntu:latest
MAINTAINER inyeongkim (hacerrumbo@gmail.com)

# no interactive
ARG DEBIAN_FRONTEND=noninteractive
#####

RUN apt-get update -y && apt-get install -y python3-pip python3-dev build-essential default-jre default-jdk

COPY ./javic-final /chatbot-new

WORKDIR /chatbot-new

RUN pip3 install -U pip setuptools six numpy wheel mock && pip3 install -r pip3_requirements.txt --ignore-installed

RUN pip install --user --upgrade pip && pip install -r requirements.txt --ignore-installed

RUN chmod +x run.sh

# port 7070
EXPOSE 7070
CMD ./run.sh
