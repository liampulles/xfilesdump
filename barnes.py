#!/usr/bin/python

import urllib.request

#Ask for url
url = input("Barnes & Noble URL? ")
page = urllib.request.urlopen(url).read().decode("utf-8")

#start = page.find(r'<h2>Scene Index</h2>')
#line = page.find(r'<article>',start)
#endline = page.find(r'</article>',line)
rawchaps = page.split(r'<h2>Scene Index</h2>')[1].split('<article>')[1].split(r'</article>')[0][1:]
chapslist = rawchaps.split('<br>')
print(chapslist)
