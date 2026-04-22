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
