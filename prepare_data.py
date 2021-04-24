import pandas as pd
import csv
import os

pd.set_option('display.max_rows', None)


def convert(data_path):
    data=[]
    with open(data_path, 'r',encoding='utf-8-sig') as f_input:
        for line in f_input:
            data.append(list(line.strip().split('\t')))
    df=pd.DataFrame(data[1:],columns=data[0])
    return df



def assign(df1_origin,df2_origin,fold):
    df1 = df1_origin
    df2 = df2_origin
    dev_len = len(df2)
    print(dev_len)

    df_tmp = df1.loc[fold * dev_len: (fold+1) * dev_len -1,['question','sentence','label']]

    df_tmp_2 = df2.loc[:,['question','sentence','label']]
    map_set = {}
    for i in range(dev_len):
        map_set.update({i:i+(fold)*dev_len})

    df_tmp_2 = df_tmp_2.rename(map_set)

    df1.loc[fold * dev_len: (fold+1) * dev_len-1, ['question','sentence','label']] = df_tmp_2

    df2.loc[:,['question','sentence','label']] = df_tmp.reset_index()

    print(df1)
    return df1, df2


if __name__ == '__main__':


    for i in range(10):
        dev = convert('data/QNLI/dev.tsv')
        train = convert('data/QNLI/train.tsv')

        folder = os.path.join('data/','QNLI'+'_'+str(i+1))
        new_dev_path = os.path.join(folder,'dev.tsv')
        new_train_path = os.path.join(folder,'train.tsv')
        if not os.path.exists(folder):
            os.makedirs(folder)
        # else:
        #     pass
        df1, df2 = assign(train,dev,i)

        df1.to_csv(new_train_path,sep='\t',index=False)
        df2.to_csv(new_dev_path,sep='\t',index=False)