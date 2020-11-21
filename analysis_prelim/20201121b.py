#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 18:07:49 2020

@author: balab
"""

#%%
rawtweet = 'hello @KingJulien did you win the race?'
rawtweet = re.sub(r'[^A-Za-z@$# ]+', '', rawtweet)
print(rawtweet)
# metapy
doc = metapy.index.Document()
doc.content(rawtweet)
tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
#tok = metapy.analyzers.LowercaseFilter(tok)
#tok = metapy.analyzers.LengthFilter(tok, min=2, max=10)
#tok = metapy.analyzers.Porter2Filter(tok)
#tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
tok.set_content(doc.content())
print(' '.join([t for t in tok]))
