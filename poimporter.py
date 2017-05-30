#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PO処理関連モジュールの定義
import polib
import os

# ORM関連モジュールの定義
from sqlalchemy import create_engine, Column, Integer, Unicode, UnicodeText, DateTime
from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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

engine = create_engine(getconf()['mysql'])
Base = declarative.declarative_base()

class Po(Base):
 	__tablename__ = getconf()['table']	
	id = Column(Integer, primary_key = True)
	oss = Column(Unicode(255,convert_unicode=False))
	comment = Column(Unicode(255,convert_unicode=False))	
	module = Column(Unicode(255,convert_unicode=False))
	msgctxt = Column(Unicode(4095,convert_unicode=False))	
	msgid = Column(Unicode(4095,convert_unicode=False))
	msgstr = Column(Unicode(4095,convert_unicode=False))
	date = Column(DateTime, default=datetime.now())
	def __repr__(self):
		return

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# 初期設定パラメータ
# msgidおよびmsgstrがmax_lengthを越えたらそのレコードはスキップする。
max_length = 400

# for oss in ['sakai','moodle','mahara','tecfolio']:
for oss in ['sakai','moodle','mahara']:
	po_dir = 'pos/' + oss + '/'

	# ディレクトリ内のファイルをリストする
	files = os.listdir(po_dir)

	# リストされたファイルのうちpoファイルのみを処理対象とする
	for file in files:
		if file.rpartition('.')[2] == 'po':
			pofile = polib.pofile(po_dir + file)

		# POの#:レコードはentry.occurenceとして取り出せるが、1変数のTupleになっているのでlistに変換する。
		# POの#:レコード事例；#: access/access-impl/impl/src/bundle/access.properties:1
		# /をセパレータとして取り出される先頭にモジュール名があるので、それをmodule_nameとする。

			for entry in pofile:
				module_name = list(entry.occurrences)[0][0].split("/")[0]

				if (len(entry.msgid) < max_length) and (len(entry.msgstr) < max_length):
					if oss == "tecfolio":
						entry.comment=""
						entry.msgctxt=""
						podata = Po(oss=oss, comment=entry.comment, module=module_name, msgctxt=entry.msgctxt, msgid=entry.msgstr, msgstr=entry.msgid)
					else:
						podata = Po(oss=oss, comment=entry.comment, module=module_name, msgctxt=entry.msgctxt, msgid=entry.msgid, msgstr=entry.msgstr)
					session.add(podata)

				else:
					print module_name, "\n", entry.msgid[0:30], "\n", entry.msgstr[0:30], "\n"
			# エントリーごとに書き込む		
			session.commit()
