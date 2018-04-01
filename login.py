import cookielib, urllib2, urllib, fileinput, sys, re, os

def login(username,password):
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
	opener.addheaders =[('Referer', 'https://www.crunchyroll.com/login'),
						('User-Agent','Mozilla/5.0 (Windows NT 6.3; rv:58.0) Gecko/20100101 Firefox/58.0'),
						('Content-Type','application/x-www-form-urlencoded')]

	url = 'https://www.crunchyroll.com/?a=formhandler'
	data = {'formname' : 'RpcApiUser_Login', 'fail_url' : 'http://www.crunchyroll.com/login', 'name' : username, 'password' : password}
	req = urllib2.Request(url, urllib.urlencode(data))
	res = opener.open(req)
try:
	path = sys.argv[3]
	with open(path): pass
except IOError:
	path = sys.argv[3]
	cookie_jar = cookielib.MozillaCookieJar(path)
	cookie_jar.save()
try:
	path = sys.argv[3]
	cookie_jar = cookielib.MozillaCookieJar(path)
	cookie_jar.load()
	username = sys.argv[1]
	password = sys.argv[2]
	login(username,password)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
	opener.addheaders =[('User-Agent','Mozilla/5.0 (Windows NT 6.3; rv:58.0) Gecko/20100101 Firefox/58.0'),
						('Connection','keep-alive')]
	url = 'http://www.crunchyroll.com/'
	req = opener.open(url)
	site = req.read()

	if re.search(username+'(?i)',site):
		print 'Login successful.'
		cookie_jar.save()
		for line in fileinput.input(path,inplace =1):
			line = line.strip()
			if not 'c_visitor' in line:
				print line
except IOError:
	path = sys.argv[3]
	print 'Login failed.'
	os.remove(path)
	sys.exit()