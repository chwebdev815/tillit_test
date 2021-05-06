import os
import requests
from bs4 import BeautifulSoup
import gevent
# from gevent.threadpool import ThreadPool
from gevent import pool
import urllib.parse

base_url = "https://news.ycombinator.com/"
# p = pool.Pool(os.cpu_count())
p = pool.Pool(20)
entire_paths = []
COUNT = 0

def crawl(url):
	global COUNT
	# Get Page Content From URL
	main_page = requests.get(url)
	soup = BeautifulSoup(main_page.content, 'html.parser')

	# Get Child URLs
	child_urls = soup.find_all('a', href=True)

	lpaths = []
	for link in child_urls:
		# Extract Actual Link From URL
		href = urllib.parse.urlparse(link.get('href'))
		# Check Same Domain Or Different Domain
		if not href.hostname:
			lpaths.append(link.get('href'))

	if(len(lpaths) != 0):
		for path in lpaths:
			if not path in entire_paths:
				entire_paths.append(path)
				print("{}, {} -> {}".format(COUNT, url, base_url + path))
				COUNT += 1
				p.spawn(crawl, base_url + path)

def main():
	crawl(base_url)
	gevent.wait()

if __name__ == "__main__":
  main()