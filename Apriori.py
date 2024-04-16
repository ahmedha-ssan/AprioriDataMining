import pandas as pd
from itertools import combinations

def read_transactions(file_path, num_records):
    df = pd.read_csv(file_path, nrows=num_records)
    transactions = {}
    for row in df.iterrows():
        if row['TransactionNo'] in transactions:
            transactions[row['TransactionNo']].append(row['Items'])
        else:
            transactions[row['TransactionNo']] = [row['Items']]
    return transactions

def generate_candidates(itemsets, itemsetLen):
    candidates = []
    for i in range(len(itemsets)):
        for j in range(i+1, len(itemsets)):
            itemset1 = itemsets[i]
            itemset2 = itemsets[j]
            if itemset1[:itemsetLen-2] == itemset2[:itemsetLen-2]:
                candidates.append(sorted(list(set(itemset1) | set(itemset2))))
    return candidates

def prune_candidates(transactions, candidates, min_support):
    pruned_candidates = {}
    for candidate in candidates:
        support_count = 0
        for tid in transactions:
            if set(candidate).issubset(transactions[tid]):
                support_count += 1
        if support_count >= min_support:
            pruned_candidates[tuple(candidate)] = support_count
    return pruned_candidates

def apriori(transactions, min_support):
    itemsets = []
    frequent_itemsets = {}
    item_supports = {}

    for tid in transactions:
        for item in transactions[tid]:
            if [item] not in itemsets:
                itemsets.append([item])
            item_supports[item] = item_supports.get(item, 0) + 1

    frequent_itemsets = {tuple([item]): support for item, support in item_supports.items() if support >= min_support}

    itemsets.sort()
    k = 2
    while itemsets:
        candidates = generate_candidates(itemsets, k)
        frequent_candidates = prune_candidates(transactions, candidates, min_support)
        frequent_itemsets.update(frequent_candidates)
        itemsets = list(frequent_candidates.keys())
        k += 1

    return frequent_itemsets

def generate_association_rules(frequent_itemsets, min_confidence):
    association_rules = []
    last_itemset_length = len(list(frequent_itemsets.keys())[-1])
    
    for itemset, support in frequent_itemsets.items():
        if len(itemset) == last_itemset_length:
            itemset_size = len(itemset)
            itemset_support = support
            for subset_length in range(1, itemset_size):
                subsets = list(combinations(itemset, len(itemset)-subset_length))
                for subset in subsets:
                    antecedent = list(subset)
                    consequent = set(itemset).difference(antecedent)
                    antecedent_support = frequent_itemsets.get(tuple(antecedent), 0)
                    
                    if antecedent_support == 0:
                        continue
                    
                    confidence = itemset_support / antecedent_support
                    if confidence >= min_confidence:
                        association_rules.append((antecedent, consequent, confidence))

    return association_rules

def print_results(frequent_itemsets, association_rules):
    itemset_num = 1
    current_size = len(next(iter(frequent_itemsets.keys())))

    print(f"\nItemSet#{itemset_num}")    
    for itemset, support in frequent_itemsets.items():
        if len(itemset) > current_size:
            itemset_num += 1
            current_size = len(itemset)
            print(f"\nItemSet#{itemset_num}")
        print(f"{list(itemset)} : Support = {support}")

    print("\nAssociation Rules:")
    for rule in association_rules:
        antecedent = ' ^ '.join(map(str, rule[0]))
        consequent = ' ^ '.join(map(str, rule[1]))
        confidence = round(rule[2] * 100, 2)
        print(f"{antecedent} => {consequent} : Confidence = {confidence}%")