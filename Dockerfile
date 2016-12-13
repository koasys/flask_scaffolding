FROM ubuntu:16.04

## Install libraries
#
RUN apt-get update
RUN apt-get -y install python-pip python-dev build-essential 
RUN pip install --upgrade pip
RUN apt-get -y install sqlite3 libsqlite3-dev
RUN apt-get -y install apache2 libapache2-mod-wsgi

#
#RUN apt-get -y install git
#RUN git clone https://github.com/koasys/flask_scaffolding.git

RUN ls -al

ADD . /var/www/webapp

#RUN mv flask_scaffolding webapp
#RUN echo "Moved to webapp"
#RUN ls -al
WORKDIR /var/www/webapp
RUN echo "Current location"
RUN pwd
RUN pip install -r requirements.txt

RUN chmod -R a+rX *

## Initialize sqlite DB
#
RUN sqlite3 webapp.sqlite < schema_sqlite.sql

## Run webapp
#
#CMD python server.py

## Run Apache with config
RUN a2enmod wsgi
COPY __artifacts__/apache_configuration.txt /etc/apache2/sites-available/webserver.conf
RUN a2ensite webserver

#CMD  /usr/sbin/apache2ctl -D FOREGROUND
CMD service apache2 restart


