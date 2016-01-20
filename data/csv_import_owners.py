# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import csv
import pandas as pd
import numpy as np




## Define these variables for filenames
report_filename = 'owner.json'

wkdir = os.getcwd()
print wkdir

##create dataframe
report_df = pd.read_json(wkdir + '/' + report_filename)
pd.set_option('display.max_colwidth', -1) #so filenames don't get truncated

print report_df.columns

for index, row in report_df.iterrows():
    print row['Owner']['name']
    print row['Owner']['id']
    print row['Owner']['description']
    print row['Owner']['pic_url']


"""
for i in report_df.columns:
    print i
for index, row in report_df.iterrows():
    print row['name'][3:-1]
    print row['description'][3:-1]
    print row['pic_url'][3:-1]
    print row['slogan'][3:-1]
    print row['id'][1:-1]
    newOwner = Owner(name = row['name'][3:-1], description = row['description'][3:-1],
        pic_url = row['pic_url'][3:-1], slogan = row['slogan'][3:-1],
        id = row['id'][1:-1], email = row['name'][3:-1] + '@gmail.com')
    session.add(newOwner)
    session.commit()
"""
