import plotly_express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    votes1 = pd.read_csv('data/senate/2021-117-1.csv')
    votes2 = pd.read_csv('data/senate/2022-117-2.csv')
    
    votes = votes1.merge(votes2, how='outer')
    names = pd.read_csv('data/legislators.csv', dtype=object)
    # pull out and create labels
    labels = names[['last_name', 'party', 'lis_id', 'state']]
    # convert to string, because python is wierd and the data gets indexed
    labels.loc[:, 'party'] = [str(i) for i in labels.party]
    labels['label'] = [f'{row.last_name} ({row.party[0]}-{row.state})' for i, row in labels.iterrows()]
    mapping = dict(zip(labels.lis_id, labels.label))
    # clean votes array for clustering calculation
    votesarray = votes.drop(columns=['voteid', 'votenumber', 'votedate', 'majorityreq', 'result', 'votedesc']).transpose()
    # rename index to proper labels
    voternames = [mapping[i] for i in votesarray.index]

    fig, ax = plt.subplots()
    ax.imshow(votesarray)
    ax.set_yticks(range(len(voternames)), voternames)
    
    
    plt.imshow(votesarray)
    plt.show()
