import os
from itertools import chain, combinations
from collections import defaultdict


def Subset(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def getitemwithleastsupport(itemset, transactionslist, Support, frequentset):
        _itemset = set()
        localSet = defaultdict(int)

        for item in itemset:
                for transaction in transactionslist:
                        if item.issubset(transaction):
                                frequentset[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = float(count)/len(transactionslist)

                if support >= Support:
                        _itemset.add(item)

        return _itemset


def mergeset(itemSet, length):
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def gettransactionlist(data):
    transactionList = list()
    itemSet = set()
    for record in data:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))             
    return itemSet, transactionList


def Apriori(data, Support, Confidence):
    itemSet, transactionlist = gettransactionlist(data)

    frequentset  = defaultdict(int)
    largeset  = dict()
    associationrules  = dict()
   
    CSet = getitemwithleastsupport(itemSet,
                                        transactionlist,
                                        Support,
                                        frequentset)

    currentLSet = CSet
    k = 2
    while(currentLSet != set([])):
        largeset[k-1] = currentLSet
        currentLSet = mergeset(currentLSet, k)
        currentcset = getitemwithleastsupport(currentLSet,
                                                transactionlist,
                                                Support,
                                                frequentset)
        currentLSet = currentcset
        k = k + 1

    def calculatesupport(item):
            return float(frequentset[item])/len(transactionlist)

    returneditems  = []
    for key, value in largeset.items():
        returneditems.extend([(tuple(item), calculatesupport(item))
                           for item in value])

    returnedrules  = []
    for key, value in largeset.items()[1:]:
        for item in value:
            _Subset = map(frozenset, [x for x in Subset(item)])
            for element in _Subset:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = calculatesupport(item)/calculatesupport(element)
                    if confidence >= Confidence:
                        returnedrules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return returneditems, returnedrules


def Results(items, rules):
    for item, support in sorted(items, key=lambda (item, support): support):
        print "item: %s , %.3f" % (str(item), support)
        print "\n-----------Rules-------------:"
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        print "Rule: %s --- %s , %.3f" % (str(pre), str(post), confidence)


def processFile(fname):
        file = open(fname, 'rU')
        for line in file:
                line = line.strip().rstrip(',')                         
                record = frozenset(line.split(','))
                yield record

def userinput():
    inputfile = raw_input('Enter the name of the file you wish to read \n')
    assert os.path.exists(inputfile), "There is no file in the current directory called"+str(inputfile)
    Support = float(input ('Enter the value for minimum support\n'))
    Confidence = float(input ('Enter the value for minumum Confidence\n'))

    inFile = processFile(inputfile)
    items, rules = Apriori(inFile, Support, Confidence)
    Results(items, rules)
    print('Input file name \t'+inputfile)
    print('Minimum support value \t'+str(Support))
    print('Minimum Confidence value \t'+str(Confidence))
    choice = raw_input('Do you want to process another file')
    if str(choice) == 'y':
        userinput()
    print('You have not selected any more files \n \t')

if __name__ == "__main__":
    userinput()

