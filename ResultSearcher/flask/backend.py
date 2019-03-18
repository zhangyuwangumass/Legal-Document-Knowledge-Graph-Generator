#coding=utf-8
import sys
reload(sys) # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
import ctypes
import json

#so = ctypes.cdll.LoadLibrary
#lib = so("./libpycallsearch.so")
#lib.init()

app = Flask(__name__)



@app.route('/')
def main():
	print "I worked!"
	return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search():
	print "I received Message"
	if request.method == 'POST':
		print "I received POST"
		#quest = request.form.get('quest','NULL')
		#f = open('resources/quest.txt', 'w')
		#f.write(quest)
		#f.close()
		#lib.search()
		return 'yyy'
	elif request.args.has_key('keyword'):
		print 'I received GET'
		print request.args['keyword']
		return "['A', 'B', 'C', 'D', 'E']"
	#return render_template('result.html')

@app.route('/result')
def result():
	return (open('resources/result.txt', 'r').readline())

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)
