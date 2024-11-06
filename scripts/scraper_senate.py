from bs4 import BeautifulSoup
# from requests_html import HTMLSession
from urllib.request import urlopen
import pandas as pd
import random as r
import time
from os import listdir
import pickle
import numpy as np
import xml.etree.ElementTree as et

URL = 'https://www.senate.gov/legislative/LIS/roll_call_votes/'
VOTECODES = {
    'Yea': 1,
    'Aye': 1,
    'Nay': 0,
    'No': 0,
    "Present": 2,
    'Not Voting': 3,
    'Missing Data': 4,
    'Present, Giving Live Pair': 2,
    'Guilty': 1,
    'Not Guilty': 0}
NEXTENSIONS = {
        1: '1st',
        2: '2nd'}


class CallError(Exception):
    '''error for if url calls fail'''
    def __init__(self, message):
        super().__init__(message)


def getvotes(congress, session, votenumber):
    '''returns a dataframe of reps ids and their votes on a roll call vote for a year'''
    # the url extension is of the form https://www.senate.gov/legislative/LIS/roll_call_votes/vote1172/vote_117_2_00271.xml

    url = URL + f'vote{congress}{session}/vote_{congress}_{session}_{votenumber:05d}.xml'
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

    # parse resopnse as an xml tree
    
    root = et.parse(page).getroot()
    members = root[-1]
    votedate = root[4].text
    votedesc = root[6].text
    majorityreq = root[11].text
    result = root[12].text
    del page

    # and now read the tree to get the list of ids
    ids = [members[a][-1].text for a in range(len(members))]

    # extract the votes and code them
    votes = [members[i][-2].text for i in range(len(members))]
    votes = [VOTECODES[vote] for vote in votes]

    #... adn save into a dataframe
    df = pd.DataFrame()
    df['ids'] = ids
    df['votes'] = votes

    return df, pd.to_datetime(votedate), majorityreq, result, votedesc


def votesarray(congress: int, session: int, initialvotenumber=1, finalvotenumber=0) -> pd.DataFrame:
    '''fetches all senate roll call votes for a congress and session and returns a coallated dataframe of every vote'''

    # initiate dataframe to hold votes
    votearray = pd.DataFrame()
    # establish index column

    votearray['votenumber'] = []
    votearray['voteid'] = []
    votearray['votedate'] = []
    votearray['majorityreq'] = []
    votearray['result'] = []
    votearray['votedesc'] = []
    votearray.set_index('votenumber')

    
    # define wait in seconds
    wait = 1
    # counter for bill indices
    votenumber = initialvotenumber
    # start requesting votes, and stop when they stop appearing
    while True:

        # try, and if it doesn't work (presumably because we ran out of votes), get out of the loop
        try:

            # fetch roll call vote
            rollcall, votedate, majorityreq, result, votedesc = getvotes(congress, session, votenumber)
            rollcall = rollcall.transpose().replace(to_replace=4, value=None)

            # add actual index
            rollcall.index = (range(len(rollcall)))
            # set column names
            rollcall.columns = rollcall.iloc[0, :]
            # drop accessory index row
            rollcall = rollcall.drop(index=0)
            # add voteid column
            rollcall['voteid'] = f'{congress}-{session}-{votenumber}'
            # add dummy variable for proper sorting of votes later on
            rollcall['votenumber'] = votenumber
            # insert vote desc and date information
            rollcall['votedate'] = votedate
            rollcall['votedesc'] = votedesc
            rollcall['majorityreq'] = [majorityreq]
            rollcall['result'] = [result]
            
            # add new vote to master dataframe
            votearray = votearray.merge(rollcall, how='outer', sort='votenumber')
            # print notification of number called
            print(f'vote {votenumber} saved')
        except Exception as error:
            print(error)
            break
        # also check if the final votenumebr has arrived
        if votenumber == finalvotenumber:
            break
    
        # wait until the time is up so the server doesnt think youre ddossing, plus some randomness
        time.sleep(r.uniform(0.5, 1))

        votenumber += 1


    # sort by and drop dummy index column
    votearray.sort_values('votenumber', inplace=True)
    # return dataframe
    return votearray


def year2congress(year: int):
    congress = np.ceil((year - 1789) / 2 + 0.5)
    session = (year - 1789)%2 + 1
    return int(congress), int(session)
    

def congress2years(congress: int):
    y = congress*2 + 1787
    return y, y+1


if __name__ == '__main__':
    year = 2023
    congress, session = year2congress(year)
    votes = votesarray(congress, session)
    votes.to_csv(f'data/senate/{year}-{congress}-{session}.csv', index=False)
