import numpy as np
import math

class NaiveBayes:

    dis_dict = {}

    con_dict = {}

    class_pr_dict = {}

    class_len_dict = {}

    dis_pr_dict = {}

    con_pr_dict = {}


    def __init__(self, xiguatxt):
        self.read(xiguatxt)
        
        self.class_pr()

        self.dic_pr()

        self.con_pr()


    def prediction(self, dis_feats, con_feats):
        prs = []
        for key in self.dis_pr_dict.keys():
            pr = self.class_pr_dict[key]
            feat_len = len(self.dis_pr_dict[key])
            if feat_len != len(dis_feats):
                print('discrete feat length match error')
                return 0
            for i in range(0, feat_len):
                time = 0
                for k in self.dis_pr_dict[key][i].keys():
                    if dis_feats[i] == k:
                        time = self.dis_pr_dict[key][i][k]
                pr *= (time + 1) / (self.class_len_dict[key] + len(self.dis_pr_dict[key][i].keys()))
            feat_len = len(self.con_pr_dict[key])
            if feat_len != len(con_feats):
                print('continous feat length match eror')
                return 0
            for i in range(0, feat_len):
                pr *= 1 / (np.sqrt(2 * math.pi) * self.con_pr_dict[key][i][1]) * math.exp(0 - np.square(con_feats[i] - self.con_pr_dict[key][i][0]) / (2 * np.square(self.con_pr_dict[key][i][1])))
            prs.append(pr)
        print(prs)
        label = []
        for i in range(0, len(prs)):
            ifMax = True
            for j in range(0, len(prs)):
                if prs[i] < prs[j]:
                    ifMax = False
                    break
            if ifMax:
                label.append(list(self.class_len_dict.keys())[i])
        return label


    def read(self, xiguatxt):
        self.dis_dict = {}
        self.con_dict = {}
        
        txt = open(xiguatxt, 'r', encoding='UTF-8')
        for line in txt:
            strs = line.split('\n')[0].split(',')
            insert(self.dis_dict, strs[9], strs[1: 7])
            insert(self.con_dict, strs[9], strs[7: 9])
        txt.close()


    def class_pr(self):
        self.class_pr_dict = {}
        self.class_len_dict = {}
        
        size = 0
        for key in self.dis_dict.keys():
            size += len(self.dis_dict[key])
            self.class_len_dict[key] = len(self.dis_dict[key])
        for key in self.dis_dict.keys():
            self.class_pr_dict[key] = (len(self.dis_dict[key]) + 1) / (size + len(self.dis_dict.keys()))


    def dic_pr(self):
        self.dis_pr_dict = {}
        
        for key in self.dis_dict.keys():
            feat_time_dicts = []
            feat_size = len(self.dis_dict[key][0])
            for i in range(0, feat_size):
                feat_time_dict = {}
                for feats in self.dis_dict[key]:
                    if not feats[i] in feat_time_dict.keys():
                        feat_time_dict[feats[i]] = 1
                    else:
                        feat_time_dict[feats[i]] += 1
                feat_time_dicts.append(feat_time_dict)
            self.dis_pr_dict[key] = feat_time_dicts


    def con_pr(self):
        self.con_pr_dict = {}
        for key in self.con_dict.keys():
            uvs = []
            for i in range(0, len(self.con_dict[key][0])):
                s = 0
                for array in self.con_dict[key]:
                    s += float(array[i])
                u = s / self.class_len_dict[key]
                s = 0
                for array in self.con_dict[key]:
                    s += np.square(float(array[i]) - u)
                v = np.sqrt(s / (self.class_len_dict[key] - 1))
                uvs.append([u, v])
            self.con_pr_dict[key] = uvs


def insert(dict_, key, item):
    if key in dict_.keys():
        dict_[key].append(item)
    else:
        dict_[key] = [item]
