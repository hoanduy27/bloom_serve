# FROM ubuntu:20.04
FROM python:3.10.13-slim

LABEL DUY <hoanduy27@gmail.com>

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Ho_Chi_Minh
RUN apt-get update && apt-get -y install locales && locale-gen en_US.UTF-8 && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# RUN apt-get update && \
#     apt-get install curl wget -y && \
#     apt-get install -y lsb-release && \
#     apt-get install -y gnupg2 && \
#     apt-get install -y python3-cffi && 
# RUN pip install --trusted-host pypi.python.org wheel


RUN apt-get update && apt-get install -y libmagic1

# RUN apt-get update && apt-get install -y --no-install-recommends locales && \
#   apt-get -y install --no-install-recommends build-essential && \
#   apt -y install make cmake gcc g++ && \
#   apt -y install libsndfile1-dev && \
#   pip3 install --upgrade pip && \
#   locale-gen en_US.UTF-8  && \
#   rm -rf /var/lib/apt/lists/*

COPY  ./requirements.txt /requirements.txt
RUN   pip3 install -r /requirements.txt && \
	  rm -rf /root/.cache/pip

COPY  . /src

COPY .env.development /src/.env

EXPOSE 5000

WORKDIR /src

# RUN chmod +x /src/run.sh

ENTRYPOINT 	["python", "server.py"]