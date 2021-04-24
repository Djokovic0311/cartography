import pandas as pd

filtered_path = "filtered/hard-to-learn/filted_"


def convert(data_path):
    data=[]
    with open(data_path, 'r',encoding='utf-8-sig') as f_input:
        for line in f_input:
            data.append(list(line.strip().split('\t')))
    df=pd.DataFrame(data[1:],columns=data[0])
    return df.loc[:,['question', 'sentence', 'label']]

def get_bad(rank):
    rank = '%.2f' % rank
    dp = filtered_path + "1/cartography_confidence_" + str(rank) + "/QNLI/train.tsv"
    df_ans = convert(dp)

    for i in range(2,11):
        dp2 = filtered_path + str(i) + "/cartography_confidence_" + str(rank) + "/QNLI/train.tsv"
        df2 = convert(dp2)
        df_ans = pd.merge(df_ans, df2, how='inner',on=['question','sentence','label'])
    print(df_ans)


def get_bad_fre():
    question_dict = {}
    for i in range(1, 11):
        dp_ = filtered_path + str(i) + "/cartography_confidence_0.01/QNLI/train.tsv"
        df_ = convert(dp_)
        for i in range(len(df_)):
            question = df_.loc[i, 'question']
            if question in question_dict:
                question_dict[question] += 1
            else:
                question_dict[question] = 1
    df_fre = pd.DataFrame(columns=['question','sentence','index','times'])
    for key, value in question_dict.items():
        for i in range(1, 11):
            dp_ = filtered_path + str(i) + "/cartography_confidence_0.01/QNLI/train.tsv"
            df_ = convert(dp_)
            for i in range(len(df_)):
                question = df_.loc[i, 'question']
                sentence = df_.loc[i, 'sentence']
                if question == key and question not in df_fre:
                    print(key,sentence,str(value))
                    df_fre.loc[len(df_fre)] = {'question': question, 'sentence': sentence, 'index': df_.loc[i, 'label'],'times':value}
                    print(df_fre)
                    break
    df_fre = df_fre.drop_duplicates().sort_values(by="times" , ascending=False).reset_index().drop(['level_0'],axis=1)
    df_fre.to_csv('bad_examples/confidence_fre.tsv',sep='\t',index=False)
    print(df_fre)
    question_dict = sorted(question_dict.items(), key=lambda item:item[1],reverse=True)
    return question_dict
def label_manually(df_ans):
    df_ans.insert(0,'index',range(len(df_ans)))
    # print(df_ans['label'].value_counts())
    f = open('label.txt')
    str = f.readline().strip()
    item = [int(i) for i in str]
    item_ = ['entailment' if i == 1 else 'not_entailment' for i in item]
    # print(item_)
    df_ans['manually'] = item_
    # print(df_ans)
    count = 0
    for i in range(len(df_ans)):
        if df_ans.loc[i,'label'] != df_ans.loc[i,'manually']:
            count += 1

get_bad(0.01)
get_bad(0.05)
get_bad(0.10)
get_bad(0.17)
get_bad(0.25)
get_bad(0.33)
get_bad(0.50)
get_bad(0.75)
