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

    def insert(self):
        conn = psycopg2.connect(self.connection)
        cur = conn.cursor()
        insert_storage = ''

        file = open(self.file_name)
        while 1:
            char = file.read(1)
            if not char: 
                break
            if char == '\"':
                insert_storage += "\""
            else:
                insert_storage += char
        file.close()

        try:
            cur.execute(insert_storage)
        except Exception, err:
            print err
        print "---===---"
        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    generator = Generator()
    generator.insert()
