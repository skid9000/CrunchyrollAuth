import cfscrape
import http.cookiejar
from bs4 import BeautifulSoup
import sys
import requests

headers = {
	'Host': 'www.crunchyroll.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': '*',
	'Referer': 'https://www.crunchyroll.com/login',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Connection': 'keep-alive'
}

sess = requests.session()
sess = cfscrape.create_scraper(sess)

username = sys.argv[1]
password = sys.argv[2]
cpath = sys.argv[3]

response = sess.get("https://www.crunchyroll.com/login", headers=headers)
cj = http.cookiejar.MozillaCookieJar(cpath)
for c in sess.cookies:
	cj.set_cookie(c)

soup = BeautifulSoup(response.text,features="html.parser")
token = soup.find('input', {'name':'login_form[_token]'})['value']

payload = {
	"login_form[name]": username,
	"login_form[password]": password,
	"login_form[redirect_url]": "/",
	"login_form[_token]": token
}

sess.post(url="https://www.crunchyroll.com/login", cookies=cj, data=payload, headers=headers)
for c in sess.cookies:
	cj.set_cookie(c)

cj.save(cpath, True, True)