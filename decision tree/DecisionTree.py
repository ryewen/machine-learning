import math
import copy
from Node import Node

class DecisionTree:

    sample_dicts = []

    feat_len = 0

    root = Node()

    def __init__(self, txtpath, begin, end):
        self.sample_dicts = []
        self.feat_len = 0
        self.root = Node()
        self.root.name = 'null'
        
        txt = open(txtpath, 'r', encoding='UTF-8')
        feat_names = []
        i = 0
        for line in txt:
            strs = line.split('\n')[0].split(',')
            if i == 0:
                feat_names = strs[begin: end]
                self.feat_len = len(feat_names)
                i += 1
            else:
                sample_dict = {}
                for j in range(0, len(feat_names)):
                    sample_dict[feat_names[j]] = strs[begin + j]
                if strs[len(strs) - 1] == '是':
                    sample_dict['class'] = '好瓜'
                else:
                    sample_dict['class'] = '坏瓜'
                self.sample_dicts.append(sample_dict)


    def prediction(self, sample_dict):
        if len(sample_dict.keys()) != self.feat_len + 1:
            print('length match error')
            return 1
        node = self.root
        while True:
            if node.name == 'result':
                return node.result
            else:
                if not '<=' in node.name:
                    node = node.child_dict[sample_dict[node.name]]
                else:
                    kind = node.name.split('<=')[0]
                    index = float(node.name.split('<=')[1])
                    if float(sample_dict[kind]) <= index:
                        node = node.child_dict['less']
                    else:
                        node = node.child_dict['more']


    def decision(self):
        self.decision_once(self.root, self.sample_dicts)


    def decision_once(self, node, sample_dicts):
        same = self.if_same(sample_dicts)
        if same != 0:
            node.name = 'result'
            if same == 1:
                node.result = '好瓜'
            if same == -1:
                node.result = '坏瓜'
            print(node.result)
            return
        no_feat = self.if_no_feat(sample_dicts)
        if no_feat != 0:
            node.name = 'result'
            if no_feat == 1:
                node.result = '好瓜'
            if no_feat == -1:
                node.result = '坏瓜'
            print(node.result)
            return
        best_feat = self.find_best_feat(sample_dicts)
        node.name = best_feat
        value_samples_dict = {}
        if not '<=' in best_feat:
            for sample_dict in sample_dicts:
                sample_dict = copy.copy(sample_dict)
                if not sample_dict[best_feat] in value_samples_dict.keys():
                    value_samples_dict[sample_dict[best_feat]] = [sample_dict]
                else:
                    value_samples_dict[sample_dict[best_feat]].append(sample_dict)
                sample_dict.pop(best_feat)
        else:
            value_samples_dict['less'] = []
            value_samples_dict['more'] = []
            kind = best_feat.split('<=')[0]            
            index = float(best_feat.split('<=')[1])
            for sample_dict in sample_dicts:
                sample_dict = copy.copy(sample_dict)
                if float(sample_dict[kind]) <= index:
                    value_samples_dict['less'].append(sample_dict)
                else:
                    value_samples_dict['more'].append(sample_dict)
        for key in value_samples_dict.keys():
            child = Node()
            node.child_dict[key] = child
            print(key)
            self.decision_once(child, value_samples_dict[key])
            

    def find_best_feat(self, sample_dicts):
        kinds = [sample_dict['class'] for sample_dict in sample_dicts]
        total_ent = self.entropy(kinds)
        ent_dict = {}
        for key in sample_dicts[0].keys():
            if key == 'class':
                continue
            if not key in ['密度', '含糖率']:
                value_kinds_dict = {}
                for sample_dict in sample_dicts:
                    value = sample_dict[key]
                    if not value in value_kinds_dict.keys():
                        value_kinds_dict[value] = [sample_dict['class']]
                    else:
                        value_kinds_dict[value].append(sample_dict['class'])
                ent = total_ent
                for value in value_kinds_dict.keys():
                    ent -= len(value_kinds_dict[value]) / len(sample_dicts) * self.entropy(value_kinds_dict[value])
                ent_dict[key] = ent
            else:
                values = [float(sample_dict[key]) for sample_dict in sample_dicts]
                values.sort()
                index_ent_dict = {}
                for i in range(0, len(values) - 1):
                    index = (values[i] + values[i + 1]) / 2
                    less_kinds = []
                    more_kinds = []
                    for sample_dict in sample_dicts:
                        if float(sample_dict[key]) <= index:
                            less_kinds.append(sample_dict['class'])
                        else:
                            more_kinds.append(sample_dict['class'])
                    ent = total_ent - len(less_kinds) / len(sample_dicts) * self.entropy(less_kinds) - len(more_kinds) / len(sample_dicts) * self.entropy(more_kinds)
                    index_ent_dict[index] = ent
                for index in index_ent_dict.keys():
                    ifMax = True
                    for k in index_ent_dict.keys():
                        if index_ent_dict[index] < index_ent_dict[k]:
                            ifMax = False
                            break
                    if ifMax == True:
                        ent_dict[key + '<=' + str(index)] = index_ent_dict[index]
        best_feat = ''
        for key in ent_dict.keys():
            ifMax = True
            for k in ent_dict.keys():
                if ent_dict[key] < ent_dict[k]:
                    ifMax = False
            if ifMax == True:
                best_feat = key
                break
        print(best_feat)
        return best_feat


    def entropy(self, kinds):
        s = 0
        for kind in kinds:
            if kind == '好瓜':
                s += 1
        ss = []
        ss.append(s)
        ss.append(len(kinds) - s)
        ent = 0
        for s in ss:
            if s != 0:
                p = s / len(kinds)
                ent -= p * math.log(p, 2)
        return ent
        

    def if_same(self, sample_dicts):
        s = 0
        for sample_dict in sample_dicts:
            if sample_dict['class'] == '好瓜':
                s += 1
        length = len(sample_dicts)
        if s == length:
            return 1 #全为好瓜
        if s == 0:
            return -1 #全为坏瓜
        return 0 #类别不一致


    def if_no_feat(self, sample_dicts):
        if len(list(sample_dicts[0].keys())) == 1:
            s = 0
            for sample_dict in sample_dicts:
                if sample_dict['class'] == '好瓜':
                    s += 1
            if s >= len(sample_dicts) / 2:
                return 1
            else:
                return -1
        else:
            return 0
