from sklearn.metrics import (accuracy_score, precision_recall_fscore_support,
                             mean_absolute_error, mean_squared_error, cohen_kappa_score)

from scipy.stats import spearmanr
from sklearn.metrics import confusion_matrix

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def compute_class_metrics(y_true, y_pred):
    # Compute classification metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted")
    conf_matrix = confusion_matrix(y_true, y_pred)

    # Compute ordinal regression metrics
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    qwk = cohen_kappa_score(y_true, y_pred, weights="quadratic")

    # Compute Spearman's Rank Correlation
    spearman_corr, _ = spearmanr(y_true, y_pred)

    # Prepare results
    metrics_results = {
        "Accuracy": accuracy,
        "Precision (Weighted)": precision,
        "Recall (Weighted)": recall,
        "F1-Score (Weighted)": f1,
        "Mean Absolute Error (MAE)": mae,
        "Mean Squared Error (MSE)": mse,
        "Quadratic Weighted Kappa (QWK)": qwk,
        "Spearman’s Rank Correlation": spearman_corr,
    }

    print(metrics_results)


def generate_confusion_matrix(y_true, y_pred, model):
    # Compute the confusion matrix
    conf_matrix = confusion_matrix(y_true, y_pred)

    # Create a confusion matrix plot
    plt.figure(figsize=(8, 6), dpi=300)
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=range(7), yticklabels=range(7))
    plt.xlabel("Predicted Severity")
    plt.ylabel("True Severity")
    plt.title("Confusion Matrix for Severity Predictions")
    plt.savefig(f'graphs/{model}_cm.png')


# df = pd.read_csv("labeled_posts_all.csv")
models = ['claude','gpt','llama','mistral', 'gemini']

for model in models:
    print(model)
    df = pd.read_csv(f"labelled_data/csv/labeled_posts_{model}.csv")
    # Drop any rows where severity or predicted severity is NaN
    df_clean = df.dropna(subset=["severity", f"{model}_label"])

    # Extract ground truth and predictions
    y_true = df_clean["severity"].astype(int)
    y_pred = df_clean[f"{model}_label"].astype(int)

    compute_class_metrics(y_true, y_pred)
    generate_confusion_matrix(y_true, y_pred, model)
