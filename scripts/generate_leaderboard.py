import pandas as pd
import glob
import os
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

truth = pd.read_csv("data/test_labels.csv")

rows=[]

files=glob.glob("submissions/*.csv")

for file in files:

    team=os.path.basename(file).replace('.csv','')

    sub=pd.read_csv(file)

    merged=truth.merge(sub,on='id')

    y_true=merged['label_x']
    y_pred=merged['label_y']

    acc=accuracy_score(y_true,y_pred)
    prec=precision_score(
        y_true,
        y_pred,
        pos_label='spam'
    )
    rec=recall_score(
        y_true,
        y_pred,
        pos_label='spam'
    )
    f1=f1_score(
        y_true,
        y_pred,
        pos_label='spam'
    )

    rows.append({
        'team':team,
        'accuracy':round(acc,4),
        'precision':round(prec,4),
        'recall':round(rec,4),
        'f1':round(f1,4)
    })


lb=pd.DataFrame(rows)

if len(lb)>0:
    lb=lb.sort_values(
        by='f1',
        ascending=False
    ).reset_index(drop=True)

    lb.insert(
        0,
        'rank',
        range(1,len(lb)+1)
    )

lb.to_csv(
    'docs/leaderboard.csv',
    index=False
)

print('Leaderboard updated.')
