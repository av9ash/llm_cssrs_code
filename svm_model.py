import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

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


# Load the Excel file
file_path = "labeled_posts_full_set_manual.csv"
df = pd.read_csv(file_path)

# Drop rows with missing content or severity
df_clean = df.dropna(subset=['content', 'severity'])

# Features and labels
X = df_clean['content']
y = df_clean['severity']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create pipeline: TF-IDF vectorizer + SVM classifier
svm_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.95)),
    ('svm', SVC(kernel='linear'))
])

# Train the model
svm_pipeline.fit(X_train, y_train)

# Predict on test set
y_pred = svm_pipeline.predict(X_test)

# Display classification report
print(classification_report(y_test, y_pred))


generate_confusion_matrix(y_true=y_test, y_pred=y_pred,model='SVM')
