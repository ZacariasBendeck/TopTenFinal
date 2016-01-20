# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 02:37:47 2016

@author: Z
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import csv
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Owner, Lists, Items
import time
from datetime import datetime


engine = create_engine('sqlite:///finalProject.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


## Define these variables for filenames
data_file1 = 'data/someitems.json'
#data_file2 = 'data/newerlists.json'
#data_file3 = 'data/newitems.json'

key = 'Items'

wkdir = os.getcwd()
print wkdir

##create dataframes
owner_data = pd.read_json(wkdir + '/' + data_file1)
#lists_data = pd.read_json(wkdir + '/' + data_file2)
#items_data = pd.read_json(wkdir + '/' + data_file3)

pd.set_option('display.max_colwidth', -1) #so filenames don't get truncated

print owner_data.columns
#print lists_data.columns
#print items_data.columns

for index, row in owner_data.iterrows():
    print 'into ownerloop'
    newItem = Items(
        name = row[key]['name'],
        description = row[key]['description'],
        pic_url = row[key]['url'],
        rank = row[key]['rank'],
        published = datetime.today(),
        updated = datetime.today())
    print 'owner' + newItem.name + ' added'
    session.add(newItem)
    session.commit()