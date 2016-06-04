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
    __tablename__ = 'po_test'
    __table_args__ = {'autoload':True}

class SearchForm(Form):
    word = StringField(u'Search Term')
    jword = StringField(u'検索語')
    sakai = BooleanField(u'Sakai')
    moodle = BooleanField(u'Moodle')
    mahara = BooleanField(u'Mahara')    

def add_red(keyword,string):
    import re
    if (len(string) != 0 and len(keyword) != 0):
        header = "<font color='red'>"
        trailer = "</font>"
        outs = []
        s=''
        e=''
        # Temporary fix for keyword with underscore
        keyword_re = keyword.replace("_","")
        r = re.compile(keyword_re, re.IGNORECASE)
        matches = re.finditer(r, string)
        for i, m in enumerate(matches):
            s = m.start()
            e = m.end()

            if i == 0:
                outs.append(string[:s])
            else:
                outs.append(string[e_before:s])
            outs.append(header + string[s:e] + trailer)
            e_before = e
        outs.append(string[e:])
        out = "".join(outs)
    else:
        out = string
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
        for keyword in keywords.split():
            polist[i].msgid = add_red(keyword,row.msgid)   
        for jkeyword in jkeywords.split():
            polist[i].msgstr = add_red(jkeyword,row.msgstr)

    return template('index', form=form, polist=polist, request=request)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)


