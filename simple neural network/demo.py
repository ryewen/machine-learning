from Network import Network

def read(path):
    datas = []
    labels = []
    txt = open(path, 'r', encoding='UTF-8')
    for line in txt:
        line = line.split('\n')[0]
        if line == '':
            continue
        strs = line.split(',')
        datas.append([float(strs[7]), float(strs[8])])
        if strs[9] == '是':
            labels.append([1, 0])
        else:
            labels.append([0, 1])
    return datas, labels

if __name__ == '__main__':
    network = Network([2, 5, 2], 0.1, 1, 1)
    datas, labels = read('xigua.txt')
    for time in range(0, 5000):
        for i in range(0, len(datas)):
            network.train(datas[i], labels[i])
    
    prediction = network.prediction([0.697,0.46])

    print(prediction[0])
    

    

