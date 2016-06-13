import os
import re
import json

curl_arg = "testetes"

global_uid=0

def get(curl_arg):
	lines = os.system(curl_arg+' > temp.json')
	with open('temp.json','r') as f:
		res = f.read()
	return res

def store(res,page):
	with open(str(global_uid)+'/'+str(page)+'.json', 'w') as f:
		f.write(res)

def mkdir(uid):
	os.system('mkdir '+str(uid))

def parse(res):
	res_json = json.loads(res)
	max_page = res_json['maxPage']
	return res_json,max_page

def replace(curl_arg, page_at):
	url ,uid,page = match_url(curl_arg)
	url_with_page = url[:len(url)-1]+str(page_at)
	replace_page=curl_arg.replace(url,url_with_page)
	return replace_page

def match_url(curl_arg):
	r = r'http://m.weibo.cn/msg/messages\?uid=(\d+)&page=(\d+)'
	martchs = re.search(r,curl_arg)
	url= martchs.group(0)
	uid = martchs.group(1)
	global_uid= uid
	page = martchs.group(2)
	return url, uid, page

def get_arg():
	curl_arg=raw_input('Please input the message page curl arg:')
	return curl_arg

if __name__ == '__main__':
	curl_arg = get_arg()
	res = get(curl_arg)
	res_json, max_page = parse(res)
	global_uid = match_url(curl_arg)[1]
	mkdir(global_uid)
	for x in range(max_page):
		x=x+1
		curl_arg_page = replace(curl_arg,x)
		print '>>>>>>>> get url '+match_url(curl_arg_page)[0]
		res = get(curl_arg_page)
		print '>>>>>>>> page (%s/%s) saved'%(str(x),str(max_page))
		store(res,x)

if __name__ != '__main__':
	res = open('temp.json','r').read()
	print parse(res)