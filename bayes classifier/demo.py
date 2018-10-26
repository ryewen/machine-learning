from NavieBayes import NaiveBayes

if __name__ == '__main__':
    nb = NaiveBayes('xigua.txt')
    print(nb.dis_dict)
    print(nb.con_dict)
    print(nb.class_pr_dict)
    print(nb.class_len_dict)
    print(nb.dis_pr_dict)
    print(nb.con_pr_dict)

    print(nb.prediction(['青绿', '蜷缩', '浊响', '清晰', '凹陷', '硬滑'], [0.697,0.46]))
