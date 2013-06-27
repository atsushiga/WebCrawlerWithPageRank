#coding: UTF-8

#ページの一番先頭にあるリンクを取得
def get_next_target(page):
	start_link = page.find('href=')
	if start_link == -1:
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1:end_quote]
	print url
	return url, end_quote

#ページに含まれるリンクをすべて取得
def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links

def union(p,q):
	for e in q:
		if e not in p:
			p.append(e)

#クローリング
def crawl_web(seed):
	tocrawl = [seed]
	crawled = []
	index = {}
	graph = {}
	while tocrawl and len(crawled) < 100:
		page = tocrawl.pop()
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			graph[page] = outlinks
			union(tocrawl, outlinks)
			crawled.append(page)
	return index, graph

#URLからページをしゅとく
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

#ページに含まれる単語に、urlを関連付ける
def add_page_to_index(index, url, content):
	words = content.split()
	for word in words:
		add_to_index(index, word, url)

def add_to_index(index,keyword,url):
	if keyword in index:
		index[keyword].append(url)
	else:
		index[keyword] = [url]

#単語からURLを取得
def lookup(index, keyword):
	if keyword in index:
		return index[keyword]
	else:
		return None

#ページランクを取得
def compute_ranks(graph):
	d = 0.8 #dumping factor
	numloops = 10

	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0 / npages

	for i in range(0, numloops):
		newranks = {}
		for page in graph:
			newrank = (1-d) / npages

			for node in graph:
				if page in graph[node]:
					newrank = newrank + d * (ranks[node] / len(graph[node]))
			newranks[page] = newrank
		ranks = newranks
	return ranks


if __name__ == '__main__':
	#元となるページ
	seed = 'http://yahoo.co.jp/'
	index, graph =  crawl_web(seed)
	ranks = compute_ranks(graph)

	print '-------------------------index-----------------------------'
	for word in index.keys():
		print '【' + word + '】', index[word]
	print''
	
	print '-------------------------search-----------------------------'
	print '【geisha】', lookup(index, 'geisha')
	print '【sushi】', lookup(index, 'sushi')
	print''
	
	print '-------------------------graph---------------------------'
	for url in graph.keys():
		print url, graph[url]
	print''
	
	print '-------------------------ranks---------------------------'
	for key in ranks.keys():
		print key, ranks[key]


