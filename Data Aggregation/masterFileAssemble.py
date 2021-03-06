# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 10:24:20 2017

@author: Reed S. Thunstrom
"""


from __future__ import division, print_function
import pandas as pd
from datetime import timedelta

###################
###################
### IMPORT DATA ###
###################
###################

# Read in tickers to initialize dataset
rdd = pd.read_excel('/Users/z013nx1/Documents/proj15aoutputCS.xlsx') #import text file with pipe delimiter
df_init = pd.DataFrame(rdd) #convert to pandas df
df_init['File Date'] = pd.to_datetime(df_init['File Date']) #convert date to timedate

#####################
#####################
### FILE ASSEMBLY ###
#####################
#####################

# create a unique list of tickers
tickers = df_init['Ticker'].drop_duplicates()
tickers2 = tickers.reset_index()
Master_File = tickers2.sort().drop('index', axis = 1)

# Initialize similarity numbers
Master_File['month_cosine_similarity'] = 1.0
Master_File['month_jaccard_similarity'] = 1.0
Master_File['month_simple_similarity'] = 1.0

# end_date = df_init['File Date'].min()
# print(end_date) #2004-08-13

start_date = pd.to_datetime('2007-12-12 00:00:00') #4 weeks before first file
    
# create file for the first month
# since we don't have the similarity metrics before the first month
# we need to initialize the similarity metrics and then update with changes in month 1


### FIRST MONTH ###

for i in range(0, 4, 4):
    
    end_date = start_date + timedelta(weeks = i +4) # ending current month
    path = ("/Users/z013nx1/Documents/" + end_date.strftime("%B %d %Y") + ".txt") # path for input
    File = pd.read_csv(path, sep = ',')
    col_name = end_date.strftime("%B %d %Y") # column name for scoring
    File[col_name] = 1 # assign boolean
    new = pd.merge(File, Master_File, how = 'outer', on = 'Ticker') # merge new file with master file
    
    # create month specific similarity columns
    columnNameCS = col_name + ' cosine_similarity'
    columnNameJS = col_name + ' jaccard_similarity'
    columnNameSS = col_name + ' simple_similarity'
    
    # update similarity column if the information is new
    # persist similairty column if the information is old
    for i in range(len(new)):
        if new.ix[i, col_name] == 1.0:
            new.ix[i, columnNameCS] = new.ix[i, 'cosine_similarity']
            new.ix[i, columnNameJS] = new.ix[i, 'jaccard_similarity']
            new.ix[i, columnNameSS] = new.ix[i, 'simple_similarity']
        else:
            new.ix[i, columnNameCS] = new.ix[i, 'month_cosine_similarity']
            new.ix[i, columnNameJS] = new.ix[i, 'month_jaccard_similarity']
            new.ix[i, columnNameSS] = new.ix[i, 'month_simple_similarity']
            
    # cosine similarity quintile values
    # quantile set to 0.20 for quintile
    cos_quintile1 = new[columnNameCS].quantile(0.2)
    cos_quintile2 = new[columnNameCS].quantile(0.4)
    cos_quintile3 = new[columnNameCS].quantile(0.6)
    cos_quintile4 = new[columnNameCS].quantile(0.8)
    
    # function for determining quintile
    def cos_quintile_rank (row):
        if row[columnNameCS] <= cos_quintile1:
            return 1
        if row[columnNameCS] <= cos_quintile2:
            return 2
        if row[columnNameCS] <= cos_quintile3:
            return 3
        if row[columnNameCS] <= cos_quintile4:
            return 4
        if row[columnNameCS] > cos_quintile4:
            return 5
    
    # apply quintile based on each rows value
    columnNameCSQuintile = col_name + ' cosine_quintile'
    new[columnNameCSQuintile] = new.apply(lambda row: cos_quintile_rank(row), axis = 1)
    
    # jacaard similarity quintile values
    # quantile set to 0.20 for quintile
    jac_quintile1 = new[columnNameJS].quantile(0.2)
    jac_quintile2 = new[columnNameJS].quantile(0.4)
    jac_quintile3 = new[columnNameJS].quantile(0.6)
    jac_quintile4 = new[columnNameJS].quantile(0.8)
    
    # function for determining quintile
    def jac_quintile_rank (row):
        if row[columnNameJS] <= jac_quintile1:
            return 1
        if row[columnNameJS] <= jac_quintile2:
            return 2
        if row[columnNameJS] <= jac_quintile3:
            return 3
        if row[columnNameJS] <= jac_quintile4:
            return 4
        if row[columnNameJS] > jac_quintile4:
            return 5
    
    # apply quintile based on each rows value
    columnNameJSQuintile = col_name + ' jaccard_quintile'
    new[columnNameJSQuintile] = new.apply(lambda row: jac_quintile_rank(row), axis = 1)
    
    # simple similarity quintile values
    # quantile set to 0.20 for quintile
    simple_quintile1 = new[columnNameSS].quantile(0.2)
    simple_quintile2 = new[columnNameSS].quantile(0.4)
    simple_quintile3 = new[columnNameSS].quantile(0.6)
    simple_quintile4 = new[columnNameSS].quantile(0.8)
    
    # function for determining quintile
    def simple_quintile_rank (row):
        if row[columnNameSS] <= simple_quintile1:
            return 1
        if row[columnNameSS] <= simple_quintile2:
            return 2
        if row[columnNameSS] <= simple_quintile3:
            return 3
        if row[columnNameSS] <= simple_quintile4:
            return 4
        if row[columnNameSS] > simple_quintile4:
            return 5
    
    # apply quintile based on each rows value
    columnNameSSQuintile = col_name + ' simple_quintile'
    new[columnNameSSQuintile] = new.apply(lambda row: simple_quintile_rank(row), axis = 1)
    
    # drop similarity columns so we can ingest new ones
    new = new.drop(['month_cosine_similarity', 'month_jaccard_similarity', 'month_simple_similarity', \
    'cosine_similarity', 'jaccard_similarity', 'simple_similarity', 'cosine_quintile', 'jaccard_quintile', 'simple_quintile', \
    'duplicate', col_name], axis =1)
    
# run the same loop for the rest of the months         
# loop uses file created from above, but need to create the first file seperately given that we had to
# initialize similairty measures

# validate output    
# spit out similarity metrics to make sure that we are only updating tickers with new information
# new[['Ticker', 'July 20 2011','July 20 2011 cosine_similarity',
# 'July 20 2011 jaccard_similarity',
# 'July 20 2011 simple_similarity',
# 'July 20 2011 cosine_quintile',
# 'July 20 2011 jaccard_quintile',
# 'July 20 2011 simple_quintile']]

### REMAINING  MONTHS ###

for i in range(4, 520, 4):
    
    end_date = start_date + timedelta(weeks = i+4) # ending current month
    previous_date = start_date + timedelta(weeks = i) # ending previous month
    path = ("/Users/z013nx1/Documents/" + end_date.strftime("%B %d %Y") + ".txt") 
    File = pd.read_csv(path, sep = ',')
    col_name = end_date.strftime("%B %d %Y") # column for current month metrics
    prev_col_name = previous_date.strftime("%B %d %Y") # column for previous month metrics
    File[col_name] = 1
    new = pd.merge(new, File, how = 'outer', on='Ticker') # merge new data with the existing data
    
    # create current month specific similarity columns 
    columnNameCS = col_name + ' cosine_similarity'
    columnNameJS = col_name + ' jaccard_similarity'
    columnNameSS = col_name + ' simple_similarity'

    # create previous month specific similarity columns 
    prevColumnNameCS = prev_col_name + ' cosine_similarity'
    prevColumnNameJS = prev_col_name + ' jaccard_similarity'
    prevColumnNameSS = prev_col_name + ' simple_similarity'
    
    # update similarity column if the information is new
    # persist similairty column if the information is old
    for i in range(len(new)):
        if new.ix[i, col_name] == 1.0:
            new.ix[i, columnNameCS] = new.ix[i, 'cosine_similarity']
            new.ix[i, columnNameJS] = new.ix[i, 'jaccard_similarity']
            new.ix[i, columnNameSS] = new.ix[i, 'simple_similarity']
        else:
            new.ix[i, columnNameCS] = new.ix[i, prevColumnNameCS]
            new.ix[i, columnNameJS] = new.ix[i, prevColumnNameJS]
            new.ix[i, columnNameSS] = new.ix[i, prevColumnNameSS]
            
    # cosine similarity quintile values
    # quantile set to 0.20 for quintile
    cos_quintile1 = new[columnNameCS].quantile(0.2)
    cos_quintile2 = new[columnNameCS].quantile(0.4)
    cos_quintile3 = new[columnNameCS].quantile(0.6)
    cos_quintile4 = new[columnNameCS].quantile(0.8)
    
    # apply quintile based on each rows value
    columnNameCSQuintile = col_name + ' cosine_quintile'
    new[columnNameCSQuintile] = new.apply(lambda row: cos_quintile_rank(row), axis = 1)
    
    # jacaard similarity quintile values
    # quantile set to 0.20 for quintile
    jac_quintile1 = new[columnNameJS].quantile(0.2)
    jac_quintile2 = new[columnNameJS].quantile(0.4)
    jac_quintile3 = new[columnNameJS].quantile(0.6)
    jac_quintile4 = new[columnNameJS].quantile(0.8)
    
    # apply quintile based on each rows value
    columnNameJSQuintile = col_name + ' jaccard_quintile'
    new[columnNameJSQuintile] = new.apply(lambda row: jac_quintile_rank(row), axis = 1)
    
    # simple similarity quintile values
    # quantile set to 0.20 for quintile
    simple_quintile1 = new[columnNameSS].quantile(0.2)
    simple_quintile2 = new[columnNameSS].quantile(0.4)
    simple_quintile3 = new[columnNameSS].quantile(0.6)
    simple_quintile4 = new[columnNameSS].quantile(0.8)
    
    # apply quintile based on each rows value
    columnNameSSQuintile = col_name + ' simple_quintile'
    new[columnNameSSQuintile] = new.apply(lambda row: simple_quintile_rank(row), axis = 1)
    
    # drop similarity columns so we can ingest new ones
    new = new.drop(['cosine_similarity', 'jaccard_similarity', 'simple_similarity', \
    'cosine_quintile', 'jaccard_quintile', 'simple_quintile', 'duplicate', col_name], axis =1)
            
# validate output
# new[['Ticker', 'August 17 2011','August 17 2011 cosine_similarity',
# 'August 17 2011 jaccard_similarity',
# 'August 17 2011 simple_similarity',
# 'August 17 2011 cosine_quintile',
# 'August 17 2011 jaccard_quintile',
# 'August 17 2011 simple_quintile']]            
            
#############
#############
#############
# FILE EXPORT
#############
#############
#############

# drop nasty columns
new = new.drop(['Unnamed: 0_y', 'Unnamed: 0_x''Unnamed: 0', 'File Date_y', 'index_y', 'CIK_y', \
'Report Type_y', 'Report URL_y', 'index_x', 'CIK_x', 'Report Type_x', 'Report URL_x', \
'File Date_x'], axis =1)

# comma delimited file export
path = path = '/Users/z013nx1/Documents/master_file_final_full.txt'
new.to_csv(path, sep = ",")

# pipe delimited file export
path = path = '/Users/z013nx1/Documents/master_file_final_full_pipe.txt'
new.to_csv(path, sep = "|")
