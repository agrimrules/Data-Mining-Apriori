import os
from itertools import chain, combinations
from collections import defaultdict


def Subset(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet


def joinSet(itemSet, length):
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))             
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    assocRules = dict()
   
    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []
    for key, value in largeSet.items()[1:]:
        for item in value:
            _Subset = map(frozenset, [x for x in Subset(item)])
            for element in _Subset:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules


def printResults(items, rules): 
    for item, support in sorted(items, key=lambda (item, support): support):
        print "item: %s , %.3f" % (str(item), support)
        print "\n-----------Rules-------------:"
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        print "Rule: %s --- %s , %.3f" % (str(pre), str(post), confidence)


def dataFromFile(fname):
        file_iter = open(fname, 'rU')
        for line in file_iter:
                line = line.strip().rstrip(',')                         
                record = frozenset(line.split(','))
                yield record

def userinput():
    inputfile = raw_input('Enter the name of the file you wish to read \n')
    assert os.path.exists(inputfile), "There is no file in the current directory called"+str(inputfile)
    minSupport = float(input ('Enter the value for minimum support\n'))
    minConfidence = float(input ('Enter the value for minumum Confidence\n'))

    inFile = dataFromFile(inputfile)
    items, rules = runApriori(inFile, minSupport, minConfidence)
    printResults(items, rules)
    print('Input file name \t'+inputfile)
    print('Minimum support value \t'+str(minSupport))
    print('Minimum Confidence value \t'+str(minConfidence))
    choice = raw_input('Do you want to process another file')
    if str(choice) == 'y':
        userinput()
    print('You have not selected any more files \n \t')

if __name__ == "__main__":
    userinput()

