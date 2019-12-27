#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch,helpers
import datetime
import re
import requests, os, sys
import pandas as pd
import FAO_scraping as fs

fs.FAO_scraping()
date_now = datetime.datetime.now()
csv_filename = "FAOSTAT_data_" +str(date_now.month)+"-"+str(date_now.day)+"-"+str(date_now.year)+".csv"
index_name = "faostat"
root_path = "/Users/QiaoQiao/Desktop/summer_internship/Assignment4_FAO/"
file = root_path+csv_filename

try:
    col_names =["domain_code","domain","area_code","area","element_code","element","item_code","item","year_code","year","unit","value","flag","flag_description"]
    csvfile = pd.read_csv(file,header=0,names=col_names)
except:
    print("No file named "+csv_filename)
    raise
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

if es.indices.exists(index = index_name):
    years = csvfile['year'].unique()
    for year in years:
        result = es.search(index=index_name, doc_type="type_name", body = {"query": {"term" : {"year":'{}'.format(year)}}})
        if result['hits']['hits']:
            print("Data of" +year + "exist")
        else:
            mydf = csvfile[csvfile.year==year]
            records=mydf.where(pd.notnull(mydf),None).T.to_dict()
            list_records=[records[it] for it in records]
            helpers.bulk(es,list_records,index=index_name,doc_type="type_name")
            print("done")
else:
    print("index does not exist")
    