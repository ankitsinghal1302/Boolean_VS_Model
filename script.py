import re
import json
import os
import time
import math
from operator import itemgetter
import operator
from collections import defaultdict

dictionary = defaultdict(int)
files_list = defaultdict(int)
docwordlist = defaultdict(int)
invdocfreq = defaultdict(int)
#punctreg = re.compile("[A-Za-z0-9]")


punctreg = re.compile("\b[a-z0-9]+\b")

def getfileslist(path_rep):
	
	i = 1
	for root, dirs, files in os.walk(path_rep):
		for file in files:
			if file.endswith(".txt"):
				#name =  os.path.realpath(os.path.join(root,str(file)))
				files_list.update({ i: os.path.realpath(os.path.join(root,str(file))) })
				i = i+1
				 
				 
	
		

def fileread(name):
	with open(name,"r") as tf:
		
		filedata = tf.read();
		#index = re.findall(punctreg,filedata.lower())     re.findall(r"\b[a-z]+\b', text, re.I)
		index = re.findall(r"\b[a-z0-9]+\b",filedata.lower(),re.I)
		return index;
	
		
def buildIndex(path):		
	
	start_time = time.time()
	getfileslist(path)
	#files_list.update({ 1: "newfile1.txt"})
	#files_list.update({ 2 : "newfile2.txt"})
	#files_list.update({ 3 : "newfile3.txt"})
	#file_list.update({"check.txt", "r"})
	for k, v in files_list.iteritems():
		builddict(getwordlist(fileread(v)),k)
	
	for k, v in dictionary.iteritems():	
		invdocfreq.update({k : math.log10(float(len(files_list))/len(v))})
		
		#print str(k) + " : " + str(v)
	print "Total time for Indexing " + str(time.time() - start_time) + '\n'
	return	
	
def getwordlist(all_list):
	word_freq = {}
	for w in all_list:
		if w not in word_freq :
			word_freq.update({w :1+ math.log10(all_list.count(w))})

	return word_freq	
	
def builddict(lwords,docId):
	docwordlist.update({str(docId) : lwords})
	for k, v in lwords.iteritems():
		if k not in dictionary:
			dictionary.update({ k : {docId:v}})
			
		else :
			#plist = dictionary[k]
			#plist.append([docId,v])
			dictionary[k].update({docId:v})
	#print dictionary
			
def booleanSearch(query):
	wl = re.findall(r"\b[a-z0-9]+\b",query.lower(),re.I)
	plist = []
	
	
	for w in wl:
		l = dictionary.get(w,"None")
		
		if l == "None":
			print "Sorry no documents matches your query"
			return
		plist = commonPostingsdictionary(plist,l)
	if not plist:
		print "Sorry no documents matches your query"
	else:
		getdocs(plist)
	
def getdocs(list):
	for w in list:
		s = files_list.get(w)
		print s[s.rfind("\\")+1 : ]
		
def commonPostings(list1,list2):
	if not list1:
		return list2
	n2 = len(list2)
	n1 = len(list1)
	print
	clist = []
	k1 = 0
	k2 = 0
	while n1 > k1 and n2 > k2 :		
		if list1[k1][0] == list2[k2][0]:
			clist.append(list1[k1])
			k2 = k2 + 1
			k1 = k1 + 1
		elif list1[k1][0] > list2[k2][0]:
			k2 = k2 + 1
		else :
			k1 = k1 + 1
	
	return clist		

def commonPostingsdictionary(list1,list2):
	if not list1:
		return list2
	n2 = len(list2)
	n1 = len(list1)
	print
	clist = []
	k1 = 0
	k2 = 0
	for k,v in list1.iteritems():
		if k in list2:
			clist.append(k)
	return clist	
	
def buildVSM():
	for k,v in docwordlist.iteritems():
		for k1,v1 in v.iteritems():
			v.update({k1: v1*invdocfreq.get(str(k1))})
		
	return
			
def VSMSearch(query):
	wl = re.findall(r"\b[a-z0-9]+\b",query.lower(),re.I)	
	ql = getwordlist(wl)	
	value = 0
	dlist = {}
	querymag = 0
	docmag = 0
	#
	
	#
	for k1,v1 in ql.iteritems():
		querymag = querymag + math.pow(v1,2) 
	querymag = math.sqrt(querymag)
	
	
	for k,v in docwordlist.iteritems():
		
		value = 0
		docmag = 0
		for kd,vd in v.iteritems():
			docmag = docmag + math.pow(vd,2) 
		docmag = math.sqrt(docmag)
		#print docmag
		
		for k1,v1 in ql.iteritems():
			wordval = v.get(k1,'None')
			if wordval != 'None':
				value = value + (wordval * v1)
		value = value/(docmag*querymag)
		
		
		dlist.update({k : value})
		
		
	
	score = sorted(dlist.items(), key=itemgetter(1),reverse = True)
	
	VSMdocs(score)
	#print score
		
def VSMdocs(dlist):
	n = 0
	for d in dlist:
		
		if n >= 50 or d[1] == 0:
			if n == 0:
				print "Sorry no documents"
			break
		else:
			s = files_list.get(int(d[0]))
			print str(s[s.rfind("\\")+1 : ]) + "[ " + str(d[1]) + " ]"
			n = n+1
			
			
def Bool_VSM():
	path = raw_input("Please enter the path of repository ")
	print "Building Index ... Please Wait...." + '\n'
	buildIndex(str(path))			
	buildVSM()
	print "We are ready to go...." + '\n'
	input_var = 1
	while input_var == 1 or input_var == 2:
		input_var = input("Enter 1 for Boolean Retrieval and 2 for Ranked Retrieval and 3 to exit :")
		if input_var == 1:
			search = raw_input("Enter the query ")
			booleanSearch(str(search))
		elif input_var == 2:
			search = raw_input("Enter the query ")
			VSMSearch(str(search))
		else: 
			break
			
			
Bool_VSM()			
			
			
			