FROM python:3.10

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV APP_HOME /usr/src/app

WORKDIR /$APP_HOME

COPY ./source/ $APP_HOME/
COPY ./.env $APP_HOME/

RUN apt-get -y update

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD tail -f /dev/null
# CMD python3 main.py