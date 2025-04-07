import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# import nltk
# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# # Download stopwords if not already downloaded
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('punkt_tab')


def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    stop_words.update(['want','feel','going','life','know'])
    words = word_tokenize(text)  # Tokenize the text
    filtered_words = [word for word in words if word.lower() not in stop_words]  # Remove stopwords
    return ' '.join(filtered_words)


# Function to clean text by normalizing apostrophes and removing contractions
def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r"[\u2018\u2019\u201C\u201D]", "'", text)  # Normalize special symbols to standard apostrophes
        contractions = {
            "can't": "cannot", "don't": "do not","don t": "do not",  "I'm": "I am", "I've": "I have", "you're": "you are",
            "he's": "he is", "she's": "she is", "it's": "it is", "we're": "we are", "they're": "they are",
            "we've": "we have", "they've": "they have", "that's": "that is", "wouldn't": "would not",
            "couldn't": "could not", "shouldn't": "should not", "weren't": "were not", "wasn't": "was not",
            "hasn't": "has not", "haven't": "have not", "hadn't": "had not", "doesn't": "does not",
            "isn't": "is not", "aren't": "are not", "y'all": "you all", "let's": "let us",
            "won't": "will not", "didn't": "did not", "gonna": "going to", "wanna": "want to",
            "gotta": "got to", "im":"I am", "ll":"will"
        }
        for contraction, expanded in contractions.items():
            text = re.sub(r"\b" + re.escape(contraction) + r"\b", expanded, text, flags=re.IGNORECASE)
        return text
    return text


def severity_distribution_graph(df):
    # Distribution of severity scores
    plt.figure(figsize=(8, 5))
    sns.countplot(x=df["severity"], palette="viridis")
    # plt.title("Distribution of Severity Scores")
    plt.xlabel("Severity Score (CSSR-S)")
    plt.ylabel("Count of Posts")
    # plt.show()
    plt.savefig("images/severity_distribution_graph.png")


def plot_posting_frequency(df):
    # Convert Unix timestamp to datetime
    df['created_datetime'] = pd.to_datetime(df['created'], unit='s')

    # Plot post frequency over time
    plt.figure(figsize=(12, 9))
    df.set_index('created_datetime').resample('D').size().plot()
    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    plt.title("Daily Posting Frequency on Reddit (SuicideWatch)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.show()
    plt.savefig("images/daily_posting_frequency.png")

def word_count_serverity(df):
    df['word_count'] = df['content'].apply(lambda x: len(str(x).split()))

    # Plot word count distribution across severity levels
    plt.figure(figsize=(8, 5))
    df.groupby('severity')['word_count'].mean().plot(kind='bar', edgecolor='black')
    plt.xlabel("Severity Level (CSSR-S)")
    plt.ylabel("Average Word Count")
    plt.title("Average Word Count by Severity Level")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def serverity_word_clouds(df):
    # Generate word clouds for each severity level
    for severity in sorted(df["severity"].unique()):
        text = " ".join(df[df["severity"] == severity]["cleaned_content"].dropna())  # Combine all text
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

        # Display the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.title(f"Word Cloud for Severity {severity}", fontsize=14)
        plt.axis("off")

        # Show the image
        # plt.show()
        plt.savefig(f"images/wordcloud_{severity}.png")

def get_bigrams(text):
    tokens = re.findall(r'\b\w+\b', text.lower())  # Tokenize words without NLTK dependency
    bigrams = list(zip(tokens, tokens[1:]))  # Extract bigrams
    return bigrams

def severity_top20_bigrams_graph(df):
    # Generate bigram frequency plots per severity level
    for severity in sorted(df["severity"].unique()):
        # Combine all cleaned text for the given severity level
        text = " ".join(df[df["severity"] == severity]["cleaned_content"].dropna())

        # Extract bigrams
        bigram_list = get_bigrams(text)

        # Count bigram frequencies
        bigram_counts = Counter(bigram_list)
        most_common_bigrams = bigram_counts.most_common(20)  # Get top 20 bigrams

        # Convert to DataFrame for visualization
        bigram_df = pd.DataFrame(most_common_bigrams, columns=["Bigram", "Count"])

        # Plot bigram frequencies
        plt.figure(figsize=(12, 6))
        sns.barplot(y=[" ".join(bigram) for bigram in bigram_df["Bigram"]], x=bigram_df["Count"], palette="magma")
        plt.title(f"Top 20 Bigrams for Severity {severity}")
        plt.xlabel("Frequency")
        plt.ylabel("Bigrams")
        # plt.show()
        plt.savefig(f"top20_bigrams_{severity}.png")


def violin_plot_word_freq(df):
    # Replot violin plot for word count vs severity
    df['word_count'] = df['content'].apply(lambda x: len(str(x).split()))
    plt.figure(figsize=(12, 6))
    sns.violinplot(x=df['severity'], y=df['word_count'], inner="quartile")
    plt.xlabel("Severity Level (CSSR-S)")
    plt.ylabel("Word Count")
    plt.title("Violin Plot of Word Count Distribution by Severity Level")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def box_plot_word_freq(df):
    # Replot box plot for word count vs severity
    df['word_count'] = df['content'].apply(lambda x: len(str(x).split()))
    # plt.figure(figsize=(12, 6))
    plt.figure(dpi=300)
    # sns.boxplot(x=df['severity'], y=df['word_count'])
    sns.boxplot(x=df['severity'], y=df['word_count'],
                boxprops=dict(facecolor='orange', edgecolor='black'))

    plt.xlabel("Severity Level (CSSR-S)")
    plt.ylabel("Word Count")
    plt.title("Box Plot of Word Count Distribution by Severity Level")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.show()
    plt.savefig(f"images/box_plot_word_counts.png")


# Load the CSV file
file_path = "labeled_posts_all.csv"  # Update the filename accordingly
df = pd.read_csv(file_path)
df["cleaned_content"] = df["content"].apply(clean_text).apply(remove_stopwords)
# Display basic information about the dataset
# df.info()
# print(df.head())

# # Summary statistics for numerical columns
# summary_stats = df.describe()
# print(summary_stats)

# # Checking for missing values
# missing_values = df.isnull().sum()
# print("Missing Values:\n", missing_values)

severity_distribution_graph(df)
plot_posting_frequency(df)
# word_count_serverity(df)
# violin_plot_word_freq(df)
box_plot_word_freq(df)
serverity_word_clouds(df)
# severity_top20_bigrams_graph(df)
