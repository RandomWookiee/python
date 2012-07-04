import sys
from pyquery import PyQuery as pq
import urllib



class Element(object):
	
	def __init__(self, name, obj):
		self.name = name
		self.obj = obj
		self.tags = []

	def process(self):
		pass

	def __str__(self):
		s  = ["element.name -> ", self.name, "\nNumber tags -> %s"%len(self.tags)]
		return "".join(s)
		

class PageViewer(object):
	def __init__(self, url):
		self.load_page(url)

	def load_page(self, url):
		self.url = url
		self.page = pq(url=self.url, opener=lambda url: urllib.urlopen(url).read())
		self.title = self.page('title').text()
		self.head = Element('head', self.page('head'))
		self.body = Element('body', self.page('body'))


	def __str__(self):
		s = ["Title -> ", self.title,
		"\nURL -> ", self.url, 
		"\nPage Length -> ", "%s"%len(self.page.text())]
		return "".join(s)

p = PageViewer('http://www.google.com')

print p

print p.head
print p.body

