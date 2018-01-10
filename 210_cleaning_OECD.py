#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pandas as pd


input_dir="in_oecd_data"
output_dir="mid_country_data"

record={}	#['LOCATION','INDICATOR','TIME']='Value'
year_max=0
year_min=0
ind_list=[]

files = os.listdir(input_dir)
for file in files:
	df=pd.read_csv(input_dir+'/'+file)
	for i in range(len(df.index)):
		loc=df.at[i,'LOCATION']
		ind=df.at[i,'INDICATOR']+"("+df.at[i,'SUBJECT']+"/"+df.at[i,'MEASURE']+")"
		year=int(df.at[i,'TIME'])
		val=df.at[i,'Value']

		if year_max < year:
			year_max=year
		if year_min == 0 or year_min > year:
			year_min=year
		ind_list.append(ind)

		record.setdefault(loc,{})
		record[loc].setdefault(year,{})
		record[loc][year].setdefault(ind,val)

ind_list=sorted(set(ind_list), key=ind_list.index)
header="Year"
for ind in ind_list:
	header+=","+ind
header+="\r\n"

for loc in record.keys():
	fw = open(output_dir+"/"+loc+".csv", 'w')
	fw.write(header)

	for year in range(year_min,year_max+1):
		record[loc].setdefault(year,{})
		line = str(year)
		
		for ind in ind_list:
			record[loc][year].setdefault(ind,"")
			line+=","+str(record[loc][year][ind])

		fw.write(line+"\r\n")
	fw.close()
