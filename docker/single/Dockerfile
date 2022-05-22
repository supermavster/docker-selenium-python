FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

ENV DISPLAY=:99
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PYTHON_VERSION_PROJECT 3.10
ENV APP_HOME /usr/src/app

WORKDIR /$APP_HOME

COPY ./source/ $APP_HOME/
COPY .env $APP_HOME/
RUN [ -f /$APP_HOME/.env ] || cp .env /$APP_HOME/
ENV $(cat .env | xargs)

# Install Python Version 3.10
RUN apt-get update -y

RUN apt-get install -y software-properties-common curl unzip wget
RUN apt-add-repository ppa:deadsnakes/ppa
RUN apt-get update -y

RUN apt-get install -y python3.10 
RUN apt-get install -y python3.10-distutils

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2
RUN update-alternatives --config python3

RUN python3 --version

RUN apt-get install -y python3-pip
RUN apt-get install -y curl

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# Install Browser
RUN apt-get install --no-install-recommends -yqq \
    ca-certificates \
    gnupg2 \
    software-properties-common

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN chmod +x /usr/local/bin/chromedriver
RUN rm /tmp/chromedriver.zip

RUN apt-get install --no-install-recommends -y \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 libgbm1 \
    xvfb 

# set display port to avoid crash
CMD ["python3", "main.py"]