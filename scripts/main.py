import pandas as pd
import numpy as np
import networkx as nx
from typing import Callable
import gravis as gv
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

VOTECODES = {
    'Yea': 1,
    'Aye': 1,
    'Nay': 0,
    'No': 0,
    "Present": 2,
    'Not Voting': 3,
    'Missing Data': 4,}
VALIDVOTES = [0, 1, 2, 3, 4]


def generatecontingency(a: pd.Series, b: pd.Series):
    # yes this is written horribly
    # NOTE: rewrite this to be more efficient and generalized
    return np.array([
        [
            sum((a==0) & (b==0)),
            sum((a==1) & (b==0)),
            sum((a==2) & (b==0))],
        [
            sum((a==0) & (b==1)),
            sum((a==1) & (b==1)),
            sum((a==2) & (b==1))],
        [
            sum((a==0) & (b==2)),
            sum((a==1) & (b==2)),
            sum((a==2) & (b==2))]
    ])


def chisquare(a: pd.Series, b: pd.Series) -> float:
    '''finds the probability that the members vote independantly, the p value of a chi2 test.'''
    # then take chi2 and return p value
    return chi2_contingency(generatecontingency(a, b)).pvalue


def overlap(a: pd.Series, b: pd.Series) -> float:
    '''compares by percentage of identical votes'''
    comparison = a == b
    comparison = comparison.dropna()
    return np.nansum(comparison)/len(comparison)


def generateedges(votes: pd.DataFrame, metric: Callable[[pd.Series, pd.Series], float] = overlap) -> pd.DataFrame:
    '''generates edges list, comparing all members based on a similarity metric'''
    # define counting parameters
    length = len(votes.columns)
    n = int(((length-1) * length)/2)
    k = 0

    m1 = ['a000000'] * n
    m2 = ['a000000'] * n
    weight = [0.0] * n
    for i in range(length):
        for j in range(i + 1, length):
            # god has forgiven me, for not using append like an idiot (T-T)
            m1[k] = votes.columns[i]
            m2[k] = votes.columns[j]
            weight[k] = metric(votes.iloc[:, i], votes.iloc[:, j])
            k += 1
    # construct dataframe
    df = pd.DataFrame()
    df['source'] = m1
    df['target'] = m2
    df['weight'] = weight
    return df

def generategraph(edges: pd.DataFrame) -> nx.Graph:
    '''creates graph of members voting patterns with identification data'''
    # generate list of legislators from dataframe
    legislators = pd.read_csv('data/legislators.csv').set_index('bioguide_id')
    # read graph from edgelist
    G = nx.from_pandas_edgelist(edges, edge_attr=True)
    # return G
    '''
    # pull out list relevant congresspeople
    voters = legislators.loc[list(G.nodes)]

    # crossreference with legislator list
    # label each node with biodata id, surname, state, and district
    surnames = voters['last_name']
    state = voters['state']
    district = voters['district']
    labels = [f'{surnames.iloc[i]}\n{state.iloc[i]} {district.iloc[i]}' for i in range(len(surnames))]
    # give names to all nodes
    # first create a list of dicts of {'name': label}
    names = [{'label': label} for label in labels]
    # names is a dictionary of node names (bioguide id strings), within each of which is {'name': label}
    names = dict(zip(G.nodes, names))
    nx.set_node_attributes(G, names)
    '''
    # return graph
    return G
    

def visualize(graph: nx.Graph, name: str):
    fig = gv.d3(graph, use_edge_size_normalization=True, edge_size_data_source='weight')
    fig.export_html(f'{name}.html')


if __name__ == '__main__':
    # load votes and make edge data
    alignments = generateedges(pd.read_csv('senate2022.csv'))
    #print(len(alignments.index))
    #testgraph = generategraph(alignments)
    #print(testgraph.number_of_nodes())
    alignments = alignments[alignments['weight'] >= 0.5]
    #print(len(alignments.index))
    realgraph = generategraph(alignments)
    # cull weak edges
    #print(realgraph.number_of_nodes())
    visualize(realgraph, '2022-senate')


    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 5), layout='tight')
    # ax.hist(alignments.weight, bins=100, density=True, color='magenta')
    # ax.set_xlabel('Vote Similarity (%)')
    # ax.set_ylabel('Frequency (%)')
    # ax.set_title('Frequency of Inter-Member Vote Alignments\nUS House 2022')
    # fig.savefig('similarities.png')

    pass