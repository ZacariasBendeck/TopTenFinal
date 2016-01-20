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


pd.set_option('display.max_colwidth', -1) #so filenames don't get truncated

## Define these variables for filenames
data_file1 = 'data/newowners.json'
data_file2 = 'data/newlists.json'
data_file3 = 'data/newitems.json'

wkdir = os.getcwd()
print wkdir

##create dataframes
owner_data = pd.read_json(wkdir + '/' + data_file1)
lists_data = pd.read_json(wkdir + '/' + data_file2)
items_data = pd.read_json(wkdir + '/' + data_file3)

pd.set_option('display.max_colwidth', -1) #so filenames don't get truncated

print owner_data.columns
print lists_data.columns
print items_data.columns

for index, row in owner_data.iterrows():
    print 'into ownerloop'
    newOwner = Owner(
        name = row['Owner']['name'],
        id = row['Owner']['id'],
        description = row['Owner']['description'],
        pic_url = row['Owner']['pic_url'],
        email = row['Owner']['email'],
        created = datetime.today(),
        updated = datetime.today())
    print 'owner' + newOwner.name + ' added'
    session.add(newOwner)
    session.commit()


for index, row in lists_data.iterrows():
    newList = Lists(
        name = row['Lists']['name'],
        id = row['Lists']['id'],
        description = row['Lists']['description'],
        pic_url = row['Lists']['pic_url'],
        owner_id = row['Lists']['owner_id'],
        published = datetime.today(),
        updated = datetime.today())
    session.add(newList)
    session.commit()

for index, row in items_data.iterrows():
    newItem = Items(
        name = row['Items']['name'],
        description = row['Items']['description'],
        rank = row['Items']['rank'],
        pic_url = row['Items']['url'],
        lists_id = row['Items']['lists_id'],
        published = datetime.today(),
        updated = datetime.today())
    print newItem.name + ' added to items'
    session.add(newItem)
    session.commit()

session.close()
engine.dispose()


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
