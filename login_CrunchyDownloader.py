import cfscrape
import http.cookiejar
from bs4 import BeautifulSoup
import sys

scraper = cfscrape.create_scraper()

try:
	import config
	scraper.headers["User-Agent"] = config.UA
except:
	pass

username = sys.argv[1]
password = sys.argv[2]
cpath = 'C:\\ProgramData\\Crunchy-DL\\cookies.txt'

response = scraper.get("https://www.crunchyroll.com/login")

cj = http.cookiejar.MozillaCookieJar(cpath)
for c in scraper.cookies:
	cj.set_cookie(c)

soup = BeautifulSoup(response.text)
token = soup.find('input', {'name':'login_form[_token]'})['value']

payload = {
	"login_form[name]": username,
	"login_form[password]": password,
	"login_form[redirect_url]": "/",
	"login_form[_token]": token
}

scraper.post("https://www.crunchyroll.com/login", cookies=cj, data=payload)
for c in scraper.cookies:
	cj.set_cookie(c)

print(cj)
print(scraper.headers["User-Agent"])
cj.save(cpath, True, True)