FROM ubuntu:18.04
MAINTAINER inyeongkim (hacerrumbo@gmail.com)

RUN apt-get update -y && apt-get install -y python3-pip python3-dev build-essential 

COPY ./handy_gw /handy
WORKDIR /handy

RUN pip3 install -r requirements.txt

EXPOSE 7000
ENTRYPOINT ["python3"]
CMD ["app.py"]
