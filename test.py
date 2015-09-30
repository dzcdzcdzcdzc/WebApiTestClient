import urllib.request
httpHandler = urllib.request.HTTPHandler(1)
httpsHandler = urllib.request.HTTPSHandler(1)
opener = urllib.request.build_opener(httpHandler, httpsHandler)
urllib.request.install_opener(opener)
response = urllib.request.urlopen('http://www.sina.com.cn')
print(response.info())
print(dir(response))
