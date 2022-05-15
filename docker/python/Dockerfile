FROM python:3.8

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY ./source/ $APP_HOME/

RUN mkdir __logger

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
#
## Message
#RUN echo "Installing geckodriver ..."
## Get last version
#RUN export GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
## Download last version
#wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz  && \
## Extract
#tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin  && \
## Set permissions
#chmod +x /usr/local/bin/geckodriver  && \
## Remove file
#rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
#
#
## Message
#RUN echo "Installing Firefox ..."
## Install Firefox
#ENV FIREFOX_SETUP="firefox-setup.tar.bz2"
## Clean Firefox in the system
#RUN apt-get purge firefox -y
## Download Firefox
#RUN wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64"
## Extract
#RUN tar -xjf $FIREFOX_SETUP -C /opt
## Lnk browoser
#RUN ln -s /opt/firefox/firefox /usr/bin/firefox
## Remove setup
#RUN rm $FIREFOX_SETUP
#
#RUN echo "Installing phantomjs ..."
## Download phantomjs
#RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
## Extract phantomjs file
#RUN tar -jxf phantomjs-2.1.1-linux-x86_64.tar.bz2
## Copy phantomjs to /usr/local/bin
#RUN cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs
## Remove phantomjs file
#RUN rm phantomjs-2.1.1-linux-x86_64.tar.bz2

# set display port to avoid crash
ENV DISPLAY=:99

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD tail -f /dev/null
# CMD python3 example.py