import numpy as np
import random
from collections import Counter


def load_symbols(filename):
    '''
    Open symbols file

    Returns:    list of symbols
    '''
    with open(filename,'r') as g:
        symbols = [line[0] for line in g]

    return symbols


def map_cypher(cypher,symbols):
    '''
    Generates dictionary of mapping
    cypher -> symbols

    Returns:    dict[cypher]=symbols
    '''

    return dict(zip(cypher,symbols))


def decode_message(message,map_cypher):
    '''
    Given an encrypted message and a
    cypher mapping, decode the message

    Returns:     String of decode message
    '''

    return "".join([map_cypher[m] for m in message])


def learn_stats_text(filename,symbols):
    '''
    Esitmates probability of symbols and couple
    of symbols from a text writte on filename.
    Transition matrix values are initalized to one
    to avoid zero probabilities.

    Returns:    matrix of transision
                symbols probability
                index map from symbols to int
    '''

    dist_unigram = Counter()
    dist_bigram = Counter()
    symb_to_int = {s:i for i,s in enumerate(symbols)}
    int_to_symb = {i:s for i,s in enumerate(symbols)}

    with open(filename,'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip().lower()
            line = [ch for ch in line if ch in symbols]

            if(len(line)>0):
                for i in range(len(line)-1):
                    dist_unigram[line[i]] +=1
                    dist_bigram[(line[i],line[i+1])] += 1
                dist_unigram[line[len(line)-1]] +=1

    prob_symbols = [dist_unigram[int_to_symb[i]] for i in range(len(symbols))]
    prob_symbols = prob_symbols/np.sum(prob_symbols)

    trans_matrix = np.ones([len(symbols),len(symbols)])

    for c in dist_bigram.keys():
        trans_matrix[symb_to_int[c[0]],symb_to_int[c[1]]] = dist_bigram[c]

    rsum = np.sum(trans_matrix,axis=1)
    trans_matrix = trans_matrix/np.expand_dims(rsum,1)

    return prob_symbols,trans_matrix,symb_to_int


def estimate_prob(message,trans_matrix,symb_to_int):
    '''
    Estimates log probability of a given message, based on
    the input transition matrix (it ignores the probability
    related to the first symbol).

    Returns:   probability (float)
    '''

    message = [symb_to_int[m] for m in message]

    # ignore probability for first symbol

    return np.sum([np.log(trans_matrix[message[i],message[i+1]]) for i in range(len(message)-1)])


def mcmc(encoded_message,symbols,trans_matrix,symb_to_int,iters=10000,repetitions=10):
    '''
    Implements Metropolis-Hastings sampler. It repeats the sampling procedure
    for repetitions (default 10) times. Each sampling is performed over iters
    (default 10000). Given the symbols list, a cypher is randomly proposed.
    The cypher has two symbols swapped at random, and the new cypher is accepted
    if has greater probability or with if U[0,1]<exp(proposed prob - prob).
    The best cypher over repetitions is returned.

    Returns: dictionary mapping of cypher
    '''


    best = {}

    for r in range(repetitions):

        cypher = symbols.copy()
        random.shuffle(cypher)

        decoded_message = decode_message(encoded_message,map_cypher(cypher,symbols))
        prob = estimate_prob(decoded_message,trans_matrix,symb_to_int)

        i = 0

        while(i < iters):
            swap = random.sample(list(range(len(symbols))),2)
            proposed_cypher = cypher.copy()

            t = proposed_cypher[swap[0]]
            proposed_cypher[swap[0]] = proposed_cypher[swap[1]]
            proposed_cypher[swap[1]] = t
            decoded_message_proposed = decode_message(encoded_message,map_cypher(proposed_cypher,symbols))

            proposed_prob = estimate_prob(decoded_message_proposed,trans_matrix,symb_to_int)

            if(proposed_prob>prob):
                cypher = proposed_cypher
                prob = proposed_prob
                decoded_message = decoded_message_proposed
            else:
                if(random.random()<np.exp(proposed_prob-prob)):
                    cypher = proposed_cypher
                    prob = proposed_prob
                    decoded_message = decoded_message_proposed
            if(i%100==0):
                print(decoded_message[:60])
            i +=1

        best[prob] = "".join(cypher)

    final_cypher = best[sorted(best)[-1]]

    return map_cypher(final_cypher,symbols)


if __name__=="__main__":
    alpha = load_symbols("symbols.txt")
    P,T,C = learn_stats_text("2600-0.txt",alpha)
    with open("message.txt","r") as f:
        message = f.read().strip()
    map = mcmc(message,alpha,T,C,iters=10000,repetitions=10)
    print("\n\nDECODED MESSAGE: ")
    print(decode_message(message,map))
