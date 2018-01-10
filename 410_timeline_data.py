#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


input_dir="out_fi_etc"
output_dir="print_fi_etc"

rank=200
rank_s=1
except_inds=[]

total_inds=[]
files = os.listdir(input_dir)
for file in files:
	filepart=file.split(".")
	data={}
	target_inds=[]

	precen_all={}
	last_all={}
	for i in range(1,rank+2):
		precen_all.setdefault(i,{})
		precen_all[i].setdefault('r2',0.0)
		precen_all[i].setdefault('ind',"")
		last_all.setdefault(i,{})
		last_all[i].setdefault('r2',0.0)
		last_all[i].setdefault('ind',"")

	f = open(input_dir+"/"+file, 'r')
	for line in f.readlines():
		line = line.rstrip()
		cell = line.split('\t')
		
		except_flag=0
		for ex in except_inds:
			if ex in cell[4]:
				except_flag=1
		if except_flag==1:
			continue
		
		data.setdefault(cell[3],{})
		data[cell[3]].setdefault(cell[4],0.0)
		data[cell[3]][cell[4]]=float(cell[1])

		# extract max score of all
		if int(cell[3]) < 2001:
			for i in range(1,rank+1):
				if precen_all[i]['r2'] < float(cell[1]):
					precen_all[i+1]['r2']=precen_all[i]['r2']
					precen_all[i+1]['ind']=precen_all[i]['ind']
					precen_all[i]['r2']=float(cell[1])
					precen_all[i]['ind']=cell[4]
					break

		# extract score of last year
		elif int(cell[3]) < 2015:
			for i in range(1,rank+1):
				if last_all[i]['r2'] < float(cell[1]):
					last_all[i+1]['r2']=last_all[i]['r2']
					last_all[i+1]['ind']=last_all[i]['ind']
					last_all[i]['r2']=float(cell[1])
					last_all[i]['ind']=cell[4]
					break

	f.close()

###	inds=[precen_all[i]['ind'] for i in range(rank_s,rank+1)]
	inds=[]

	inds2=[last_all[i]['ind'] for i in range(rank_s,rank+1)]
	print filepart[0], len(set(inds2)),
	for tmp in set(inds2):
		tmp_inds=tmp.split("(")
		print tmp_inds[0],
	print

	total_inds.extend(set(inds2))
	inds.extend(inds2)
	inds=list(set(inds))

	fw = open(output_dir+"/"+filepart[0]+"_timeline.tsv", 'w')
	line=""
	for ind in inds:
		line+="\t"+ind
	fw.write(line+"\r\n")
	for yr in sorted(data.keys()):
		line=yr
		for ind in inds:
			if data[yr].has_key(ind):
				line+="\t"+str(data[yr][ind])
			else:
				line+="\t"
		fw.write(line+"\r\n")
	fw.close()

print
print len(set(total_inds)),
for tmp in set(total_inds):
	tmp_inds=tmp.split("(")
	print tmp_inds[0],
print

