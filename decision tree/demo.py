from DecisionTree import DecisionTree

if __name__ == '__main__':
    tree = DecisionTree('xigua.txt')
    print(tree.sample_dicts)
    tree.decision()

    sample_dict = {'色泽': '青绿', '根蒂': '蜷缩', '敲声': '沉闷', '纹理': '稍糊', '脐部': '稍凹', '触感': '硬滑', '密度': '0.719', '含糖率': '0.103', 'class': '坏瓜'}
    print('result:', tree.prediction(sample_dict))

