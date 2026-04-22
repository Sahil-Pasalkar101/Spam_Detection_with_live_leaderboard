# Spam Detection Challenge (GitHub PR + Live Leaderboard)

A complete beginner-friendly GitHub project where contributors submit predictions via Pull Requests and a live leaderboard updates automatically.

---

# Project Structure

```bash
spam-detection-challenge/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── test_labels.csv
│   └── sample_submission.csv
│
├── submissions/
│   └── (participant CSV files go here)
│
├── scripts/
│   ├── evaluate_submission.py
│   └── generate_leaderboard.py
│
├── docs/
│   ├── leaderboard.csv
│   └── index.html
│
└── .github/
    └── workflows/
        └── leaderboard.yml
```

---

# 1 README.md

````md
# Spam Detection Challenge

Submit a Pull Request with your predictions file in:

```bash
submissions/team_name.csv
```

Format:

```csv
id,label
1,spam
2,ham
```

Leaderboard updates automatically after PR merge.

## Metric
- Accuracy
- Precision
- Recall
- F1 Score

## Run locally

```bash
pip install -r requirements.txt
python scripts/evaluate_submission.py submissions/sample.csv
```
````

---

# 2 requirements.txt

```txt
pandas
scikit-learn
```

---

# 3 .gitignore

```gitignore
__pycache__/
*.pyc
.env
```

---

# 4 data/test_labels.csv

(ground truth hidden in real competitions, visible for demo)

```csv
id,label
1,spam
2,ham
3,spam
4,ham
5,spam
6,ham
7,spam
8,ham
9,spam
10,ham
```

---

# 5 data/sample_submission.csv

```csv
id,label
1,spam
2,ham
3,spam
4,ham
5,spam
6,ham
7,spam
8,ham
9,spam
10,ham
```

---

# 6 Example participant submission

Create:

submissions/team_alpha.csv

```csv
id,label
1,spam
2,ham
3,spam
4,ham
5,spam
6,ham
7,spam
8,spam
9,spam
10,ham
```

---

# 7 scripts/evaluate_submission.py

```python
import pandas as pd
import sys
import json
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


def evaluate(submission_path):

    truth = pd.read_csv("data/test_labels.csv")
    sub = pd.read_csv(submission_path)

    merged = truth.merge(sub,on="id")

    y_true = merged["label_x"]
    y_pred = merged["label_y"]

    metrics = {
        "accuracy": round(accuracy_score(y_true,y_pred),4),
        "precision": round(
            precision_score(
                y_true,
                y_pred,
                pos_label="spam"
            ),4),
        "recall": round(
            recall_score(
                y_true,
                y_pred,
                pos_label="spam"
            ),4),
        "f1": round(
            f1_score(
                y_true,
                y_pred,
                pos_label="spam"
            ),4)
    }

    return metrics


if __name__ == "__main__":

    path=sys.argv[1]
    results=evaluate(path)

    print(json.dumps(results))
```

---

# 8 scripts/generate_leaderboard.py

```python
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
```

---

# 9 docs/leaderboard.csv

(initial seed)

```csv
rank,team,accuracy,precision,recall,f1
```

---

# 10 docs/index.html

Live leaderboard website (GitHub Pages)

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Spam Detection Leaderboard</title>
<style>
body{
font-family:Arial;
padding:40px;
background:#f5f5f5;
}

h1{
text-align:center;
}

table{
width:90%;
margin:auto;
border-collapse:collapse;
background:white;
box-shadow:0 2px 10px rgba(0,0,0,.1);
}

th,td{
padding:15px;
border:1px solid #ddd;
text-align:center;
}

th{
background:#222;
color:white;
}

tr:hover{
background:#f2f2f2;
}
</style>
</head>
<body>

<h1>📊 Spam Detection Challenge Leaderboard</h1>

<table id="leaderboard">
<thead>
<tr>
<th>Rank</th>
<th>Team</th>
<th>Accuracy</th>
<th>Precision</th>
<th>Recall</th>
<th>F1</th>
</tr>
</thead>
<tbody></tbody>
</table>

<script>
fetch('leaderboard.csv')
.then(response=>response.text())
.then(data=>{

let rows=data.trim().split('\n').slice(1)
let tbody=document.querySelector('tbody')

rows.forEach(r=>{
let cols=r.split(',')
let tr=document.createElement('tr')

cols.forEach(c=>{
let td=document.createElement('td')
td.textContent=c
tr.appendChild(td)
})

tbody.appendChild(tr)

})
})
</script>

</body>
</html>
```

---

# 11 .github/workflows/leaderboard.yml

This updates leaderboard whenever PR merges to main.

```yaml
name: Update Leaderboard

on:
  push:
    branches:
      - main

jobs:
 update:

   if: github.actor != 'github-actions[bot]'

   runs-on: ubuntu-latest

   permissions:
      contents: write

   steps:

    - name: Checkout
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Generate leaderboard
      run: |
        python scripts/generate_leaderboard.py

    - name: Commit updates
      run: |
        git config --global user.name github-actions
        git config --global user.email actions@github.com
        git add docs/leaderboard.csv
        git commit -m "Update leaderboard" || echo "No changes"
        git push
```

---

# 12 Enable GitHub Pages

Repository:

Settings → Pages

Set:

```text
Branch: main
Folder: /docs
```

Site becomes:

```text
https://username.github.io/spam-detection-challenge/
```

Live leaderboard auto-refreshes after each merged PR.

---

# 13 Contributor Workflow

Participants:

Fork repo

Add:

```bash
submissions/my_team.csv
```

Open Pull Request.

Merge PR.

Leaderboard updates automatically.

---

# 14 Optional PR Validation (Reject Bad Submissions)

Add extra file:

scripts/validate_submission.py

```python
import pandas as pd
import sys

sub=pd.read_csv(sys.argv[1])

assert list(sub.columns)==['id','label']
assert set(sub['label']).issubset({'spam','ham'})

print('Submission valid')
```

Then in workflow before scoring:

```yaml
- name: Validate submissions
  run: |
      for file in submissions/*.csv
      do
        python scripts/validate_submission.py $file
      done
```

---

# 15 Bonus Features (easy upgrades)

## Add medals

Modify HTML:

```javascript
if(cols[0]=='1') cols[0]='🥇'
if(cols[0]=='2') cols[0]='🥈'
if(cols[0]=='3') cols[0]='🥉'
```

---

## Add PR badges

Show:

* Number of submissions
* Latest challenger
* Top score

---

## Hidden leaderboard split

* public.csv
* private.csv

Like Kaggle.

---

# 16 First Commit Commands

```bash
git init
git add .
git commit -m "Initial challenge setup"
git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main
```

---

# 17 Sample Challenge README badge section

```md
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)
![Leaderboard Live](https://img.shields.io/badge/Leaderboard-Live-blue)
```

---

# 18 Future upgrade (Kaggle-style)

Can add:

* hidden evaluation server
* public/private leaderboard split
* robustness attacks on spam models
* Streamlit submission dashboard
* auto comments on PR with scores

PR bot comment example:

```yaml
Accuracy: 0.92
F1: 0.90
Current Rank: #3
```

Very cool.

---

# Example Pull Request Submission Example

Contributor adds:

```csv
id,label
1,spam
2,ham
...
```

Opens PR:

```text
Team Name: Data Wizards
Model: Naive Bayes
F1 Local: 0.91
```

Merged → leaderboard updates.

---

This is basically a mini Kaggle clone built entirely on GitHub.
