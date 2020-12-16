FROM python:3.8-slim

COPY . /code
WORKDIR /code

RUN apt-get clean \
  && apt-get -y update

RUN apt-get -y install nginx \
  && apt-get -y install python3-dev \
  && apt-get -y install build-essential

RUN pip install pip --upgrade
RUN pip install pipenv
RUN pipenv install --system

COPY ./var/nginx.conf /etc/nginx
RUN chmod +x ./var/start.sh
CMD ["./var/start.sh"]