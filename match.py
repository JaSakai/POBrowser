#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

header = "<font color='red'>"
trailer = "</font>"

outs = []
keyword = "This"
word = "This is a pen"
# word = "oh... This is a pen, this is a pencil, this is a ink"
r = re.compile(keyword, re.IGNORECASE)
#r = keyword
matches = re.finditer(r, word)

#temp = list(matches)
#print "**len",len(temp)

length = len(list(matches))

print "**len",length
#print "**len",len(word)

# if len(list(matches)) == 1:
if length != 0:
	print "Matches"



"""
for i, m in enumerate(matches):
	s = m.start()
	e = m.end()

	print s
	print e

	if i == 0:
		outs.append(word[:s])
	else:
		outs.append(word[e_before:s])
	outs.append(header + word[s:e] + trailer)
	e_before = e

outs.append(word[e:])

print outs

"""