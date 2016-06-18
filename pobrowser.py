#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import bottle
from bottle import get, post, run
from bottle import request, template, redirect
from bottle import HTTPError
from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, UnicodeText, func, or_, and_
from sqlalchemy.ext.declarative import declarative_base

from bottle.ext import sqlalchemy

from wtforms.form import Form
from wtforms import validators
from wtforms import StringField, IntegerField, TextAreaField, BooleanField

from xml.sax.saxutils import *

import ConfigParser

def getconf():
    config = ConfigParser.ConfigParser()
    config.read("pobrowser.conf")

    user = config.get("mysql", "user")
    password = config.get("mysql", "password")
    server = config.get("mysql", "server")
    database = config.get("mysql", "database")

    table = config.get("misc", "table")

    return {'mysql':"mysql://%s:%s@%s/%s?charset=utf8" % (user, password, server, database),'table':table}

Base = declarative_base()
engine = create_engine(getconf()['mysql'], echo=True)

plugin = sqlalchemy.Plugin(
    engine,
    Base.metadata,
    keyword='db',
    create=False,
    commit=False,
    use_kwargs=True
)

bottle.install(plugin)

Base.metadata.reflect(engine)
class Pos(Base):
    __tablename__ = getconf()['table']
    __table_args__ = {'autoload':True}

class SearchForm(Form):
    word = StringField(u'Search Term')
    jword = StringField(u'検索語')
    sakai = BooleanField(u'Sakai')
    moodle = BooleanField(u'Moodle')
    mahara = BooleanField(u'Mahara')

def span(a, b):

    # detect a correlation for two spans by keyword 
    # a: tuple: start and end positions in byte for 1st kwyword
    # b: tuple: start and end positions in byte for 2nd kwyword 
    # to be used with finction "tab"

    if a[1] < b[0]:
        x = [a,b]
    elif b[0]<=a[1]< b[1]:
        x = (a[0],b[1])
    else:
        x  = a
    return x

def tag(ls):

    # correct duplicated spans by plural keywords 
    # ls: list: spans detected :by finditer

    if len(ls) > 1 :
        ls.sort(key=lambda x:(x[0],x[1]))
        len_ls = len(ls)
        rs = []
        for i, l in enumerate(ls):
            if i==0: a=l
            else:
                r = span(a,l)
                if isinstance(r, list):
                    rs.append(r[0])
                    if i == len_ls-1:
                        rs.append(r[1])
                    else:
                        a=r[1]
                else:
                    if i == len_ls-1:
                        rs.append(r)
                    else:
                        a=r
    else:
        rs = ls
    return rs

def insert(pos, s, x):
  return x.join([s[:pos], s[pos:] ])

def add_red(keywords,string):

    # keywords: list, input keyword
    # string: string to be added by keywords in red

    import re
    out = string

    pos = []
    for keyword in keywords:
        if (len(string) != 0 and len(keyword) != 0):
 
            if keyword[0] in ["="]:
                keyword = keyword[1:]
            r = re.compile(keyword, re.IGNORECASE)
            matches = re.finditer(r, string)
            for m in matches:
                pos.append(m.span())

    header = "<font color='red'>"
    trailer = "</font>"
    for m in reversed(tag(pos)):
        s = m[0]
        e = m[1]
        out = insert(e,out,trailer)
        out = insert(s,out,header)
    return out
  
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def user_auth(username, password):
    return username == "tmx" and password == "kakenhi"

@get('/pobrowser')

# If authorization will be required, enable following line
# @bottle.auth_basic(user_auth)

def index(db):
    form = SearchForm()
    return template('top', form=form, request=request)

@post('/pobrowser/search')
def do_search(db):

    filters_msgid = []
    filters_msgstr = []
    filters_oss = []
    osss = []
    
    form = SearchForm(request.forms.decode())

    # For both keuwords and jkeywords
    # when first word is !, "not like %keyword%" operation will be executed
    # otherwise, "like %keyword%" operation will be executed

    keywords=form.word.data
    for keyword in keywords.split():
        if keyword[0] == "!":
            keyword = keyword[1:]
            filters_msgid.append(Pos.msgid.notlike('%'+keyword+'%'))
        else:
            if keyword[0] == "=":
                keyword_exe = keyword[1:]
            else:
                keyword_exe = '%'+keyword+'%'

            filters_msgid.append(Pos.msgid.like(keyword_exe))

    jkeywords=form.jword.data    
    for jkeyword in jkeywords.split():
        if jkeyword[0] == "!":
            jkeyword = jkeyword[1:]
            filters_msgstr.append(Pos.msgstr.notlike('%'+jkeyword+'%'))
        else:
            if jkeyword[0] == "=":
                jkeyword_exe = jkeyword[1:]
            else:
                jkeyword_exe = '%'+jkeyword+'%'

            filters_msgstr.append(Pos.msgstr.like(jkeyword_exe))

    sw_sakai=form.sakai.data
    sw_moodle=form.moodle.data
    sw_mahara=form.mahara.data

    if sw_sakai == True:
        osss = osss + ['sakai']
    if sw_moodle == True:
        osss = osss + ['moodle']
    if sw_mahara == True:
        osss = osss + ['mahara']

    for oss in osss:
        filters_oss.append(Pos.oss.like(oss))

    poquery = db.query(Pos).filter(and_(*filters_msgid)).filter(and_(*filters_msgstr)).filter(or_(*filters_oss))
    polist = poquery.all()
    for i, row in enumerate(polist):
        row.msgid = strip_tags(row.msgid)
        row.msgstr = strip_tags(row.msgstr)
        polist[i].msgid = add_red(keywords.split(),row.msgid) 
        polist[i].msgstr = add_red(jkeywords.split(),row.msgstr)

    return template('index', form=form, polist=polist, request=request)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)


