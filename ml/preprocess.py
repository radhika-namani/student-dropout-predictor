import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split


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

# Split header into column names
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

# Remove quotes, spaces, tabs and other whitespace
df.columns = (
    df.columns
    .str.replace('"', '', regex=False)
    .str.replace("\t", "", regex=False)
    .str.strip()
)


# ============================================================
# 5. CONVERT FEATURE VALUES TO NUMBERS
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
# 6. CHECK DATASET
# ============================================================

print("Dataset Shape:", df.shape)

print("\nTarget Distribution:")
print(df["Target"].value_counts())

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())


# ============================================================
# 7. SEPARATE FEATURES AND TARGET
# ============================================================

X = df.drop("Target", axis=1)

y = df["Target"]


# ============================================================
# 8. CATEGORICAL FEATURES
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
# 9. VERIFY CATEGORICAL FEATURES
# ============================================================

missing_categorical = [
    column
    for column in categorical_features
    if column not in X.columns
]

if missing_categorical:
    print("\nERROR: These categorical columns were not found:")
    for column in missing_categorical:
        print(repr(column))

    print("\nActual columns:")
    for column in X.columns:
        print(repr(column))

    raise ValueError(
        "Some categorical feature names do not match the dataset."
    )


# ============================================================
# 10. NUMERICAL FEATURES
# ============================================================

numerical_features = [
    column
    for column in X.columns
    if column not in categorical_features
]


print(
    "\nNumber of categorical features:",
    len(categorical_features)
)

print(
    "Number of numerical features:",
    len(numerical_features)
)


# ============================================================
# 11. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# 12. CREATE PREPROCESSING PIPELINE
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
# 13. APPLY PREPROCESSING
# ============================================================

X_train_processed = preprocessor.fit_transform(
    X_train
)

X_test_processed = preprocessor.transform(
    X_test
)


# ============================================================
# 14. DISPLAY RESULTS
# ============================================================

print("\nOriginal Training Shape:")
print(X_train.shape)

print("\nProcessed Training Shape:")
print(X_train_processed.shape)

print("\nOriginal Testing Shape:")
print(X_test.shape)

print("\nProcessed Testing Shape:")
print(X_test_processed.shape)


# ============================================================
# 15. COMPLETION MESSAGE
# ============================================================

print("\n========================================")
print("PREPROCESSING COMPLETED SUCCESSFULLY")
print("========================================")