from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.request import urlopen
import pandas as pd
import random as r
import time
from os import listdir
import pickle
import numpy as np

URL = 'https://clerk.house.gov/Votes'
VOTECODES = {
    'Yea': 1,
    'Aye': 1,
    'Nay': 0,
    'No': 0,
    "Present": 2,
    'Not Voting': 3,
    'Missing Data': 4,}
NEXTENSIONS = {
        1: '1st',
        2: '2nd',
        3: '3rd',
        4: '4th',
        5: '5th',
        6: '6th',}

class CallError(Exception):
    '''error for if url calls fail'''
    def __init__(self, message):
        super().__init__(message)

def billlist(congress, session):
    '''returns an iterator of bill numbers for the session'''

    # get url
    url = URL + f'?CongressNum={congress}&Session={NEXTENSIONS[session]}'
    response = HTMLSession().get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # extract year

    # extract total number of bills
    #pagination = soup.find('div', class_='pagination_info').text

    print(response.content)
    # return iterator of bill ids to fetch in getvotes
    pass

def getvotes(id) -> pd.DataFrame:
    '''returns a dataframe of reps ids and their votes on a roll call vote for a year'''
    url = URL + f'/{id}'
    # try to call 3 times
    ntries = 0
    page = 0
    while ntries <3:
        try:
            # exit loop if success
            page = urlopen(url)
            break
        except:
            print(f'Fetching {id} failed')
            ntries += 1
            time.sleep(1)
    if ntries == 3:
        raise CallError(f'Failed to call {id}')

    # now do the processing
    soup = BeautifulSoup(page.read().decode('utf-8'), 'html.parser')
    table = soup.find(id="member-votes")
    rows = table.find_all('tr')
    # create blank lists to hold data
    nvoters = len(rows)
    ids = ['A000000'] * nvoters
    votes = [0] * nvoters
    # start processing
    for i, row in enumerate(rows):
        try:
            # get rep id
            ids[i] = row.find('td', attrs={"data-label": "member"}).find('a').get('href')[-7:]
            # get vote status and convert into integer
            votes[i] = VOTECODES[row.find(attrs={"data-label": "vote"}).text]
        except:
            # account for missing rows; fucking george santos
            ids[i] = 'Missing'
            votes[i] = 5
    # combine lists into dataframe and return
    df = pd.DataFrame()
    df['ids'] = ids
    df['votes'] = votes
    return df

def getreps():
    '''returns a dataframe of reps ids, party, and state'''
    # yes, this is hacky, or just find another source, yk?
    pass

def fetchbills(year):
    '''fetches and saves all roll call votes in a congressional session'''
    # define wait in seconds
    wait = 3600/1000
    # counter for bill indices
    n = 1
    while True:
        tstart = time.time()

        id = f'{year}{n}'
        # try, and if it doesn't work (presumably because we ran out of votes), get out of the loop
        try:
            # make dataframe and save to disk
            getvotes(id).to_csv(f'data/{id}.csv')
            print(f'vote {id} saved')
        except CallError:
            break
        
        tend = time.time()
        # wait until the time is up so the server doesnt think youre ddossing, plus some randomness
        dtime = tend - tstart
        waittime = wait - dtime + r.uniform(-0.5, 0.5) + 1.5
        time.sleep(waittime)

        n += 1

    pass

def coallate(folder: str) -> pd.DataFrame:
    '''coallates all roll call votes into a single dataframe, where 
    index is roll call number and column is representative'''
    df = pd.DataFrame()
    # establish index column
    df['voteid'] = []
    df.set_index('voteid')

    for i, file in enumerate(listdir(folder)):
        # transpose table
        data = pd.read_csv(folder + file).transpose()
        # add actual index
        data.index = (range(len(data)))
        # set column names
        data.columns = data.iloc[1]
        # drop accessory index row
        data = data.drop([0, 1])
        # drop 'Missing' column
        data = data.drop(['Missing'], axis='columns')
        # add voteid column
        data['voteid'] = [file[0:-4]]



        df = df.merge(data, how='outer')
                
    
    return df

def normalize(votepath: str, namepath:str):
    '''cross checks with the name database and coalesces columns that change or dissapear in the dataset'''
    pass

def fixfives(path:str):
    '''replaces fives (not voting) with nan'''
    df = pd.read_csv(path, dtype=pd.Int32Dtype(), index_col='voteid').replace(to_replace=5, value=None)
    # also fix the fact that the vodeid isnt a string
    # df['voteid'] = df['voteid'].astype("string")
    # df.set_index('voteid')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    # pickle.dump(df, open(path + '.pyc', 'wb'))
    df.to_csv(path + '.fixed')


if __name__ == '__main__':
    fixfives("/media/snowdaere/9befb33c-94f9-4276-8567-cbe1c53b9f35/projects/blog/congress/data/2022.csv")