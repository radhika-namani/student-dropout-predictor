import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

file_path = "dataset/data.csv"

with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()


# ============================================================
# 2. FIX THE MALFORMED HEADER
# ============================================================

header = lines[0].strip()

# Remove outer quotes
if header.startswith('"') and header.endswith('"'):
    header = header[1:-1]

# Replace doubled quotes
header = header.replace('""', '"')

# Split header
columns = header.split(";")


# ============================================================
# 3. LOAD DATA ROWS
# ============================================================

data = []

for line in lines[1:]:
    row = line.strip().split(";")
    data.append(row)


# Create DataFrame
df = pd.DataFrame(data, columns=columns)


# ============================================================
# 4. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.replace('"', '', regex=False)
    .str.replace("\t", "", regex=False)
    .str.strip()
)


# ============================================================
# 5. CONVERT FEATURES TO NUMERIC
# ============================================================

feature_columns = [
    column for column in df.columns
    if column != "Target"
]

for column in feature_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# 6. DISPLAY DATASET INFORMATION
# ============================================================

print("========================================")
print("DATASET INFORMATION")
print("========================================")

print("\nDataset Shape:")
print(df.shape)

print("\nTarget Distribution:")
print(df["Target"].value_counts())


# ============================================================
# 7. SEPARATE FEATURES AND TARGET
# ============================================================

X = df.drop("Target", axis=1)

y = df["Target"]


# ============================================================
# 8. DEFINE CATEGORICAL FEATURES
# ============================================================

categorical_features = [
    "Marital status",
    "Application mode",
    "Course",
    "Daytime/evening attendance",
    "Previous qualification",
    "Nacionality",
    "Mother's qualification",
    "Father's qualification",
    "Mother's occupation",
    "Father's occupation",
    "Displaced",
    "Educational special needs",
    "Debtor",
    "Tuition fees up to date",
    "Gender",
    "Scholarship holder",
    "International"
]


# ============================================================
# 9. DEFINE NUMERICAL FEATURES
# ============================================================

numerical_features = [
    column
    for column in X.columns
    if column not in categorical_features
]


print("\nNumber of categorical features:")
print(len(categorical_features))

print("\nNumber of numerical features:")
print(len(numerical_features))


# ============================================================
# 10. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\n========================================")
print("TRAIN / TEST SPLIT")
print("========================================")

print("\nTraining samples:")
print(len(X_train))

print("\nTesting samples:")
print(len(X_test))


# ============================================================
# 11. CREATE PREPROCESSOR
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            numerical_features
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ]
)


# ============================================================
# 12. CREATE MACHINE LEARNING MODELS
# ============================================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42,
        max_depth=10
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
}


# ============================================================
# 13. TRAIN AND EVALUATE MODELS
# ============================================================

results = {}

best_model = None
best_model_name = None
best_f1_score = 0


for model_name, model in models.items():

    print("\n")
    print("========================================")
    print("TRAINING:", model_name)
    print("========================================")

    # Create complete pipeline
    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    # Train model
    pipeline.fit(
        X_train,
        y_train
    )

    # Make predictions
    y_pred = pipeline.predict(
        X_test
    )

    # Calculate metrics
    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    # Store results
    results[model_name] = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }


    # Display results
    print("\nAccuracy:")
    print(f"{accuracy:.4f}")

    print("\nPrecision:")
    print(f"{precision:.4f}")

    print("\nRecall:")
    print(f"{recall:.4f}")

    print("\nF1 Score:")
    print(f"{f1:.4f}")


    # Classification report
    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )


    # Confusion matrix
    print("Confusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )


    # Check if this is the best model
    if f1 > best_f1_score:

        best_f1_score = f1

        best_model = pipeline

        best_model_name = model_name


# ============================================================
# 14. DISPLAY MODEL COMPARISON
# ============================================================

print("\n\n")
print("========================================")
print("MODEL COMPARISON")
print("========================================")

print(
    f"{'Model':<25}"
    f"{'Accuracy':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1 Score':<12}"
)

print("-" * 73)


for model_name, metrics in results.items():

    print(
        f"{model_name:<25}"
        f"{metrics['accuracy']:<12.4f}"
        f"{metrics['precision']:<12.4f}"
        f"{metrics['recall']:<12.4f}"
        f"{metrics['f1_score']:<12.4f}"
    )


# ============================================================
# 15. DISPLAY BEST MODEL
# ============================================================

print("\n")
print("========================================")
print("BEST MODEL")
print("========================================")

print("\nBest Model:")
print(best_model_name)

print("\nBest F1 Score:")
print(f"{best_f1_score:.4f}")


# ============================================================
# 16. CREATE MODELS DIRECTORY
# ============================================================

import os

os.makedirs(
    "models",
    exist_ok=True
)


# ============================================================
# 17. SAVE COMPLETE MODEL PIPELINE
# ============================================================

model_path = "models/dropout_model.pkl"

joblib.dump(
    best_model,
    model_path
)


# ============================================================
# 18. FINAL MESSAGE
# ============================================================

print("\n")
print("========================================")
print("MODEL SAVED SUCCESSFULLY")
print("========================================")

print("\nSaved model:")
print(model_path)

print("\nThe saved file contains:")
print("- Data preprocessing")
print("- Feature scaling")
print("- One-Hot Encoding")
print("- Machine Learning model")

print("\n========================================")
print("STEP 6 COMPLETED SUCCESSFULLY")
print("========================================")