import pandas as pd
import re
from textblob import TextBlob

# load data..
data_path = "F:/Rani/Urbanbot intelligence/data/og_311_ServiceRequest_2021.csv"

df = pd.read_csv(data_path, low_memory = False)

print("Data loaded: ", df.shape)

print(df.columns)

# select required columns..
df_nlp = df[[
    "case_title",
    "subject",
    "closure_reason",
    "open_dt",
    "department",
    "latitude",
    "longitude",
    "case_status"
]]

# Create one text column..
df_nlp["complaint_text"] = (
    df_nlp["case_title"].astype(str) + " " +
    df_nlp["subject"].astype(str) + " " +
    df_nlp["closure_reason"].astype(str)
)

print("Selected columns: ", df_nlp.columns)
print("Row Before cleaning:", df_nlp.shape)            # (273951, 9)


# Remove empty complaints..
df_nlp = df_nlp.dropna(subset=["complaint_text"])
print("Rows after cleaning:", df_nlp.shape)            # (273945, 9)


# Text cleaning function..
def clean_text(text):
    text = str(text).lower()                       # lowercase
    text = re.sub(r"http\S+", "", text)       # remove urls
    text = re.sub(r"[^a-z\s]", " ", text)     # remove symbols
    text = re.sub(r"\s+", " ", text).strip()  # remove extra spaces
    text = re.sub(r"\d+", "", text)           # remove numbers
    return text

df_nlp["clean_text"] = df_nlp["complaint_text"].apply(clean_text)


# Sentiment analysis function..
def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"
    
df_nlp["sentiment"] = df_nlp["clean_text"].apply(get_sentiment)


# check priority scoring function..
def urgency_score(sentiment):
    if sentiment == "negative":
        return "high"
    elif sentiment == "neutral":
        return "medium"
    else:
        return "low"
    
df_nlp["priority"] = df_nlp["sentiment"].apply(urgency_score)

# verify result (Confidence check)..
print(df_nlp[["complaint_text", "clean_text", "sentiment", "priority"]].head(10))


# Save NLP output..
df_nlp.to_csv("complaint_nlp_output.csv", index = False)
print("Saved: complaint_nlp_output.csv")


# cleaned dataset with created & selected columns..
df_nlp[[
    "clean_text",
    "sentiment",
    "priority",
    "open_dt",
    "department",
    "latitude",
    "longitude"
]].to_csv("complaint_nlp_cleaned.csv", index=False)

print("Saved: ", "complaint_nlp_cleaned.csv")

print("Processing completed.")


