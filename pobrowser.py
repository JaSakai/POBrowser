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

Base = declarative_base()
engine = create_engine('mysql://root:edurs6k@localhost/test?charset=utf8', echo=True)

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
    __tablename__ = 'pos'
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


@get('/pobrowser')
def index():
    form = SearchForm()
    return template('top', form=form, request=request)

@post('/pobrowser/search')
def do_search(db):

    filters_msgid = []
    filters_msgstr = []
    filters_oss = []
    osss = []
    
    form = SearchForm(request.forms.decode())

    keywords=form.word.data
    for keyword in keywords.split():
        filters_msgid.append(Pos.msgid.like('%'+keyword+'%'))

    jkeywords=form.jword.data    
    for jkeyword in jkeywords.split():
        filters_msgstr.append(Pos.msgstr.like('%'+jkeyword+'%' ))

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
        strip_tags(row.msgid)
        strip_tags(row.msgstr)
        polist[i].msgid = add_red(keywords.split(),row.msgid) 
        polist[i].msgstr = add_red(jkeywords.split(),row.msgstr)

    return template('index', form=form, polist=polist, request=request)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)


