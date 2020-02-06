import json,os,re
#import jieba
from collections import Counter 

cwd = os.path.dirname(__file__)

def load_SS(fname):
    result = {}
    fpath = os.path.join(cwd,'spaces',fname)
    for line in open(fpath,'r',encoding='utf8'):
        obj = json.loads(line.strip())
        for key in obj:
            result[key.lower()] = obj[key]
    return result

def retrieve(space,string,topk=100,minweight = 0.1,lang = 'zh'):
    if lang != 'en':
        #keys = list(jieba.cut(string))
    #else:
        return 'language not supported'
    keys = re.split(' +',string)
    result = dict()
    for key in keys:
        if key in space:
            nns = space[key]
            filtered = list(filter(lambda x:x[1] >= minweight , nns[:topk]))
            for word,weight in filtered:
                result[word] = result.get(word,0)+weight
    result = Counter(result)
    return result.most_common(topk)