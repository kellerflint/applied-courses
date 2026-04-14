---
title: "Find Your Dataset"
order: 1
---

You've already trained logistic regression and random forest models. This unit puts both of them to work on real data, adds a third model (a neural network), and then pits all three against each other to see how they actually compare. Speed, accuracy, size, and where each one fails.

You'll do this in a shared Google Colab notebook. One partner sets it up, shares it with edit access, and you both work in it together. At the end of the unit you'll each submit the link.

## Find a Dataset on Kaggle

Go to [Kaggle Datasets](https://www.kaggle.com/datasets). You're looking for a dataset where you can predict a category, since you'll be building classification models.

A good dataset for this project:

- Has at least a few hundred rows (more is better)
- Has a mix of numeric features
- Has a column you can predict as a category (the target)
- Is about something you actually find interesting

Search for things like "classification dataset", "predict", or a topic you care about (health data, sports stats, housing, etc.).

> **With your partner:** Browse Kaggle together and pick a dataset you both find interesting. Don't spend more than 10 minutes on this.

### Continuous targets work too

If you find a dataset with a **continuous numeric target** (like a price, score, or rating), you can convert it into categories and use it as a classification problem.

> **With your partner:** How would you go about doing that? Think through what you'd actually need to do to turn a column of numbers into a column of categories.

<details>
<summary>Reveal answer</summary>

Pick a threshold and classify everything above it as one category and everything below as another.

```python
# Example: binarize a continuous column into 0/1
threshold = df["score"].median()  # or pick any value that makes sense
df["target"] = (df["score"] > threshold).astype(int)
```

You can also split into more than two categories using `pd.cut` or `pd.qcut`, though binary is simpler to start with.

</details>

## Set Up Your Colab Notebook

Go to [colab.research.google.com](https://colab.research.google.com), create a new notebook, and share it with your partner.

Download your dataset from Kaggle as a CSV, then upload it to Colab:

```python
from google.colab import files
uploaded = files.upload()  # opens a file picker
```

Then load it into a DataFrame:

```python
import pandas as pd

# Replace 'your_file.csv' with the actual filename
df = pd.read_csv("your_file.csv")
print(df.shape)
df.head()
```

## Choose Your Columns

Before cleaning anything, decide which columns you're actually going to use. Run this to see what you're working with:

```python
print(df.dtypes)
```

You want numeric columns only. String or categorical columns will break the models later. Pick the ones that make sense as features and set them here:

```python
# List the feature columns you want to use
feature_cols = ["col_a", "col_b", "col_c"]  # replace with your actual column names

# The column you're trying to predict
target_col = "target"  # replace with your actual target column name
```

This is also a good moment to think about which features are actually meaningful. If a column is an ID, a name, or something that wouldn't logically help predict your target, leave it out.

## Clean Your Data

Before training anything, you need to deal with missing values and outliers. Models break in unexpected ways when fed messy data.

### Check for missing values

```python
print(df.isnull().sum())
```

This prints how many nulls are in each column. You have two main options:

**Drop rows with missing values** (simpler, fine if you're not losing too much data):

```python
df = df.dropna()
```

**Fill missing values with the column median** (better if you have many nulls and can't afford to lose rows):

```python
df = df.fillna(df.median(numeric_only=True))
```

Use the median rather than the mean because the median isn't pulled by outliers the way the mean is.

### Check for outliers

Outliers are data points so far from the rest that they're likely errors or genuinely unusual cases. They can distort your model, especially logistic regression and neural networks.

The IQR method flags anything that falls more than 3× the interquartile range beyond the first or third quartile. That's a loose filter that catches obvious outliers without aggressively trimming your data.

```python
def remove_outliers_iqr(dataframe, columns, factor=3.0):
    mask = pd.Series([True] * len(dataframe), index=dataframe.index)
    for col in columns:
        Q1 = dataframe[col].quantile(0.25)
        Q3 = dataframe[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR
        mask = mask & dataframe[col].between(lower, upper)
    return dataframe[mask]

df_clean = remove_outliers_iqr(df, feature_cols)
print(f"Rows before: {len(df)}, after: {len(df_clean)}")
```

If this drops more than 20-30% of your data, consider using a larger factor (like 4.0 or 5.0) or skipping it and just relying on the null handling above.

## Prepare Features and Target

```python
X = df_clean[feature_cols]
y = df_clean[target_col]
```

If your target column has string labels like `"yes"` / `"no"`, you may need to encode them:

```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(y)
```

## Split and Scale

Split into training and test sets, then scale the features. Scaling is important because neural networks (and logistic regression to a lesser degree) train much better when all features are on the same scale. Without it, features with large numeric ranges dominate the training and smaller-scale features get ignored.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Important:** fit the scaler only on the training data, then use that same fitted scaler to transform the test data. Fitting on the test data would leak information about the test set into your preprocessing, which gives you a falsely optimistic accuracy.

Once this is done, you're ready to train your first model.
