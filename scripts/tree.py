import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sci


def congress2years(congress: int):
    y = congress*2 + 1787
    return y, y+1


if __name__ == '__main__':

    congress = 117
    y1, y2 = congress2years(congress)
    
    votes1 = pd.read_csv(f'data/senate/{y1}-{congress}-1.csv')
    votes2 = pd.read_csv(f'data/senate/{y2}-{congress}-2.csv')
    
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
    
    dist = sci.spatial.distance.pdist(votesarray, 'matching')
    link = sci.cluster.hierarchy.linkage(dist)

    # plt.style.use('dark_background')
    fig, ax = plt.subplots(1, 1, figsize=(4, 10), layout='tight')
    sci.cluster.hierarchy.set_link_color_palette(['#16BAC5', '#FF0E0A', '#FEC620'])
    dend = sci.cluster.hierarchy.dendrogram(link, labels=voternames, orientation='left', above_threshold_color='#000000', color_threshold=0.25, ax=ax)
    ax.set_title(f'Similarity Dendrogram\nSenate {congress}, {y1}-{y2}')
    ax.set_xlabel('Difference Proportion')
    ax.set_xlim(0.35, 0.0)
    # ax.set_xscale('symlog')

    plt.savefig(f'figures/{congress}-{y1}-{y2}-tree.png', dpi=300)
    # plt.xscale('log')
    plt.show()
    
