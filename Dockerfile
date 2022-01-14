FROM ubuntu:20.04

ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD requirements/main.txt /app/requirements.txt

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install -y --no-install-recommends \
    libpq-dev python3-dev libffi-dev python3-pip \
    wget pkg-config openssl libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade setuptools

WORKDIR /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN export LC_ALL=en_US.UTF-8
RUN export LANG=en_US.UTF-8
RUN export PYTHONPATH=$PWD

RUN adduser --disabled-password --gecos '' app
RUN chown -R app:app /app && chmod -R 755 /app

ENV HOME /home/app
USER app
