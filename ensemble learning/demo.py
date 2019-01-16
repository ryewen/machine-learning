import sys
sys.path.append('../decision tree')

from DecisionTree import DecisionTree

if __name__ == '__main__':
    tree = DecisionTree('xigua.txt', 7, 9)
    print(tree.sample_dicts)
    tree.decision()

    s = 0
    for sample_dict in tree.sample_dicts:
        if tree.prediction(sample_dict) == sample_dict['class']:
            s += 1

    print('result:', s / len(tree.sample_dicts))
