from newspaper import Article

def scrape(url):
	a = Article(url)
	a.download()
	a.parse()
	print(a.title)
	return a.title, a.text