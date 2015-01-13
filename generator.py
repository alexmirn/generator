#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, time, atexit
import psycopg2
import pprint

class Generator(object):

    def __init__(self, connection="dbname='generator' user='generator' host='127.0.0.1' password='generator'", \
    file_name='schema.sql'):
        self.connection = connection
        self.file_name = file_name