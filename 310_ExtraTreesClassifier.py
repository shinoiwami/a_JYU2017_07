#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import LabelEncoder

import math
import os
import random


input_dir="mid_country_data"
output_dir="out_fi_etc"
#target_country=["USA","CHN","JPN","DEU","GBR","FRA","IND","ITA","BRA","CAN","KOR","RUS","ESP","AUS","MEX","IDN","TUR","NLD","CHE","SAU","FIN","SGP"]
#target_country=["USA","JPN","DEU","RUS","BRA","LUX","IRL","CHE","NOR"]
target_country=["USA","JPN","DEU","RUS","BRA","GBR","FRA","ITA","MEX","TUR"]
except_inds=["TAXREV(TOT/USD_CAP)","TAXINCOME(TOT/PC_GDP)","TAXCORP(TOT/PC_GDP)","TAXSS(TOT/PC_GDP)","TAXPAYROLL(TOT/PC_GDP)","TAXPROPERTY(TOT/PC_GDP)","TAXGOODSERV(TOT/PC_GDP)","GNI(TOT/USD_CAP)","NNI(TOT/MLN_USD)"]

start_year=1980
loop=1000	# to prevent infinite loop

l=0
loop_flag=0
#random.shuffle(target_country)
for cu in target_country:
	print cu
	fw = open(output_dir+"/"+cu+".tsv", 'w')
	input_file=input_dir+"/"+cu+".csv"
	data0=pd.read_csv(input_file)

	##################################################
	### period loop
	k=0
	for j in range(0,len(data0.index)):
		if math.isnan(data0.at[j,'GDP(TOT/MLN_USD)']):
			continue
		if int(data0.at[j,'Year']) < start_year:
			continue
		k+=1
		if k == 1:
			n=j
		if k <= 10:
			continue
	
		data1=data0[n:j]
		data1=data1.dropna(axis=1)
		
		cols_list=list(data1.columns)
		cols_list.remove('Year')
		cols_list.remove('GDP(TOT/MLN_USD)')
		for ex in except_inds:
			if ex in cols_list:
				cols_list.remove(ex)

		
		x=data1[cols_list]
		y=data1['GDP(TOT/MLN_USD)']
		ynp=np.asarray(y,dtype="|S6")
		clf=ExtraTreesClassifier(n_estimators=100,random_state=0)

		try:
			clf.fit(x,ynp)
			r2=clf.score(x,ynp)
			importances=clf.feature_importances_
		
		except ValueError as e:
			print j, data0.at[j,'Year'], cols_list
#			print("type:{0}".format(type(e)))
#			print("args:{0}".format(e.args))
#			print("message:{0}".format(e.message))
			print("{0}".format(e))
			continue
		
		for i in range(0,len(cols_list)):
			line=cu
			line+="\t"+str(importances[i])
			line+="\t"+str(data0.at[n,'Year'])
			line+="\t"+str(data0.at[j,'Year'])
			line+="\t"+str(cols_list[i])
			fw.write(line+"\r\n")

		l+=1

	if l > loop:
		break

	fw.close()

