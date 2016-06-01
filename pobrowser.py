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

# プラグインのインストール
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

def add_red(keyword,word):
    import re
    if (len(word) != 0 and len(keyword) != 0):

        header = "<font color='red'>"
        trailer = "</font>"
        outs = []
        s=''
        e=''
        r = re.compile(keyword, re.IGNORECASE)
        matches = re.finditer(r, word)
        for i, m in enumerate(matches):
            s = m.start()
            e = m.end()

            if i == 0:
                outs.append(word[:s])
            else:
                outs.append(word[e_before:s])
            outs.append(header + word[s:e] + trailer)
            e_before = e
        outs.append(word[e:])
        out = "".join(outs)
    else:
        out = word
    return out    

@get('/pobrowser')
def index():
    form = SearchForm()
    return template('top', form=form, request=request)

@post('/pobrowser/search')
def do_search(db):

    filters = []
    filters1 = []
    osss = []
    
    form = SearchForm(request.forms.decode())
    keyword=form.word.data
    jkeyword=form.jword.data

    sw_sakai=form.sakai.data
    sw_moodle=form.moodle.data
    sw_mahara=form.mahara.data

    word = '%'+keyword+'%'
    jword = '%'+jkeyword+'%'   

    filters.append(Pos.msgid.like(word))
    filters.append(Pos.msgstr.like(jword))

    if sw_sakai == True:
        osss = osss + ['sakai']
    if sw_moodle == True:
        osss = osss + ['moodle']
    if sw_mahara == True:
        osss = osss + ['mahara']

    filters1 = []
    for oss in osss:
        filters1.append(Pos.oss.like(oss))

    poquery = db.query(Pos).filter(*filters).filter(or_(*filters1))
    polist = poquery.all()
    for i, row in enumerate(polist):
        polist[i].msgid = add_red(keyword,escape(row.msgid))
        polist[i].msgstr = add_red(jkeyword,escape(row.msgstr))

    return template('index', form=form, polist=polist, request=request)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)


