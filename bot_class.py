import requests
import re
from bs4 import BeautifulSoup

class HtmlNon200Error(Exception):
	"""Non 200 error"""
	def __str__(self):
		return "Request status code is not 200"

class SiteConf:
	"""docstring for Bot """
	def __init__(self,name,sitemap,re_title=None,re_content=None):
		self.name = name
		self.sitemap = sitemap
		self.re_title = re_title
		self.re_content = re_content

class Bot:
	def __init__(self, link):
		headers = {'User-Agent': 'Haberolog/Bot',}
		self.r = requests.get(link,headers=headers)
		self.r.encoding = 'utf-8'


class ContentBot(Bot):
	"""docstring for ClassName"""
	def __init__(self, link):
		super().__init__(link)
		self.soup = BeautifulSoup(self.r.text, 'html.parser')
		self.title = self.soup.title.text
		self.content = ""
		self.soup = self.soup.body
		if self.r.status_code != 200:
			raise HtmlNon200Error

	def extract_tag(self,tag):
		[s.extract() for s in self.soup.findAll(tag)]

	def extract_tag_class(self,tag,_class):
		[s.extract() for s in self.soup.findAll(tag, {"class": _class})]

	def find_duplicates(self,tag,attr):
		exd = re.findall(r"<{}.+{}=\"(.*?)\"".format(tag,attr),str(self.soup),re.MULTILINE)
		exd = set([x for x in exd if exd.count(x) > 1])
		return exd

	def div_find(self,soup):
		while True:
			div = [s for s in soup.findAll('div')]
			if len(div) != 0:
				break
			soup = div[0]
		return div

	def set_title(self):
		pass

	def set_content(self):
		pass

	def get_title(self):
		return self.title

	def set_content_none(self):
		for ex in ['script','ul','li','noscript','img','style','input','select','iframe','footer']:
			self.extract_tag(ex)

		for tag,_class in [['div','footer']]:
			self.extract_tag_class(tag,_class)

		for exd in self.find_duplicates("div","class"):
			print(exd)
			try:
				if list(self.soup.find('div', {"class": exd}).children)[0].name == "a":
					self.extract_tag_class("div",exd)
			except AttributeError as e:
				print(e)
				print(self.soup.find('div', {"class": exd}))
			except IndexError as e2:
				print(e2)
				print(self.soup.find('div', {"class": exd}))

			print("------------------")


		c = set()
		for tx in self.div_find(self.soup):
			t = tx.get_text()

			if len(t.split()) > 0:
				c.add(len(t.split()))
				print(len(t.split()))

		print(sorted(c,reverse=True))

		pre = first = sorted(c,reverse=True)[0]
		for i in sorted(c,reverse=True):
			diff = pre - i
			ten = i // 10
			if (diff + ten) > i: 
				break
			pre = i

		print(pre)
		print(self.title)
		for tx in self.div_find(self.soup):

			t = tx.get_text()
			if len(t.split()) == pre:
				self.content = t
				return print(t)
		return ""

class SitemapBot(Bot):
	"""docstring for SitemapLinks"""
	def __init__(self, link):
		super().__init__(link)
		self.soup = BeautifulSoup(self.r.text, 'html.parser')

	def loc(self):
		links = self.soup.findAll('loc')
		return links
	def link(self):
		regex = r"\<link\>(.*?)\<\/link\>"
		m = re.findall(regex, self.r.text, re.MULTILINE)
		m2=[]
		for x in m:
			x = x.replace("<![CDATA[","")
			x = x.replace("]]>","")
			m2.append(x)
		return m2
	def list_all(self):
		if len(self.loc()) > 0:
			return [x.text for x in self.loc()]
		else:
			return self.link()

			
if __name__ == '__main__':

	link = 'https://www.ntv.com.tr/turkiye/hasere-ilaclama-huzurevi-sakinlerini-zehirledi,OFllOSXde0KvKPz9dkzsmg'
	
	try:
		bot = ContentBot(link)
		bot.set_content_none()
	except HtmlNon200Error as e:
		print(e)
