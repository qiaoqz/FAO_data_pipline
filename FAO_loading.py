from elasticsearch import Elasticsearch,helpers
import datetime
import re
import requests, os, sys
import pandas as pd
from time import time
# please change the root path and csv_filename
root_path = "/Users/QiaoQiao/Desktop/summer_internship/Assignment4_FAO/"
csv_filename = "FAOSTAT_data_11-2-2018_2015.csv"
file = root_path+csv_filename

chunksize = 2500
col_names =["domain_code","domain","area_code","area","element_code","element","item_code","item","year_code","year","unit","value","flag","flag_description"]
csvfile = pd.read_csv(file,header=0,iterator = True, chunksize = chunksize,names=col_names)
index_name = "faostat"

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
try:
    es.indices.delete(index = index_name)
except:
    pass

       
mapping = {"index_patterns":"faostat",
		"settings": {"number_of_shards": 1,"number_of_replicas": 0,	
		"index": {"query": {"default_field": "id"}}},
		"mappings": {"type_name" : {"properties": 
		{"@domain_code": {"type": "keyword"},"@domain": {"type": "keyword"},"@area_code": {"type": "integer"},
          "@area": {"type": "keyword"},"@element_code": {"type": "integer"},"@element": {"type": "keyword"},
          "@item_code": {"type": "integer"},"@item": {"type": "keyword"},"@year_code": {"type": "integer"},
          "@year": {"type": "integer"},"@unit": {"type": "keyword"},"@value": {"type": "integer"},
          "@flag": {"type": "keyword"},"@flag_description":{"type": "keyword"}
          }}}}
es.indices.create(index=index_name,body=mapping)

for i,df in enumerate(csvfile): 
    records=df.where(pd.notnull(df),None).T.to_dict()
    list_records=[records[it] for it in records]
    try :
        helpers.bulk(es,list_records,index=index_name,doc_type="type_name")
    except :
        print ("error!, skiping some FAO data")
        pass
print("done")