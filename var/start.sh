#!/usr/bin/env bash
service nginx start
uwsgi --ini var/uwsgi.ini