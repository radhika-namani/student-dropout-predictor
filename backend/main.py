from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os


# ============================================================
# 1. CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Student Dropout Predictor API",
    description="AI-Based Student Dropout Prediction System",
    version="1.0.0"
)


# ============================================================
# 2. ENABLE CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# 3. LOAD TRAINED MODEL
# ============================================================

MODEL_PATH = "models/dropout_model.pkl"


if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        "Model file not found. "
        "Please run: python ml/train_model.py"
    )


model = joblib.load(MODEL_PATH)


# ============================================================
# 4. STUDENT INPUT MODEL
# ============================================================

class StudentData(BaseModel):

    marital_status: int
    application_mode: int
    application_order: int
    course: int
    daytime_evening_attendance: int
    previous_qualification: int
    previous_qualification_grade: float
    nationality: int
    mothers_qualification: int
    fathers_qualification: int
    mothers_occupation: int
    fathers_occupation: int
    admission_grade: float
    displaced: int
    educational_special_needs: int
    debtor: int
    tuition_fees_up_to_date: int
    gender: int
    scholarship_holder: int
    age_at_enrollment: int
    international: int

    curricular_units_1st_sem_credited: int
    curricular_units_1st_sem_enrolled: int
    curricular_units_1st_sem_evaluations: int
    curricular_units_1st_sem_approved: int
    curricular_units_1st_sem_grade: float
    curricular_units_1st_sem_without_evaluations: int

    curricular_units_2nd_sem_credited: int
    curricular_units_2nd_sem_enrolled: int
    curricular_units_2nd_sem_evaluations: int
    curricular_units_2nd_sem_approved: int
    curricular_units_2nd_sem_grade: float
    curricular_units_2nd_sem_without_evaluations: int

    unemployment_rate: float
    inflation_rate: float
    gdp: float


# ============================================================
# 5. ROOT ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Student Dropout Predictor API is running",
        "status": "success"
    }


# ============================================================
# 6. HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True
    }


# ============================================================
# 7. PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict_student(student: StudentData):

    try:

        # ----------------------------------------------------
        # Convert input to dictionary
        # ----------------------------------------------------

        data = student.model_dump()


        # ----------------------------------------------------
        # Convert frontend field names to dataset names
        # ----------------------------------------------------

        student_data = {

            "Marital status":
                data["marital_status"],

            "Application mode":
                data["application_mode"],

            "Application order":
                data["application_order"],

            "Course":
                data["course"],

            "Daytime/evening attendance":
                data["daytime_evening_attendance"],

            "Previous qualification":
                data["previous_qualification"],

            "Previous qualification (grade)":
                data["previous_qualification_grade"],

            "Nacionality":
                data["nationality"],

            "Mother's qualification":
                data["mothers_qualification"],

            "Father's qualification":
                data["fathers_qualification"],

            "Mother's occupation":
                data["mothers_occupation"],

            "Father's occupation":
                data["fathers_occupation"],

            "Admission grade":
                data["admission_grade"],

            "Displaced":
                data["displaced"],

            "Educational special needs":
                data["educational_special_needs"],

            "Debtor":
                data["debtor"],

            "Tuition fees up to date":
                data["tuition_fees_up_to_date"],

            "Gender":
                data["gender"],

            "Scholarship holder":
                data["scholarship_holder"],

            "Age at enrollment":
                data["age_at_enrollment"],

            "International":
                data["international"],


            "Curricular units 1st sem (credited)":
                data["curricular_units_1st_sem_credited"],

            "Curricular units 1st sem (enrolled)":
                data["curricular_units_1st_sem_enrolled"],

            "Curricular units 1st sem (evaluations)":
                data["curricular_units_1st_sem_evaluations"],

            "Curricular units 1st sem (approved)":
                data["curricular_units_1st_sem_approved"],

            "Curricular units 1st sem (grade)":
                data["curricular_units_1st_sem_grade"],

            "Curricular units 1st sem (without evaluations)":
                data["curricular_units_1st_sem_without_evaluations"],


            "Curricular units 2nd sem (credited)":
                data["curricular_units_2nd_sem_credited"],

            "Curricular units 2nd sem (enrolled)":
                data["curricular_units_2nd_sem_enrolled"],

            "Curricular units 2nd sem (evaluations)":
                data["curricular_units_2nd_sem_evaluations"],

            "Curricular units 2nd sem (approved)":
                data["curricular_units_2nd_sem_approved"],

            "Curricular units 2nd sem (grade)":
                data["curricular_units_2nd_sem_grade"],

            "Curricular units 2nd sem (without evaluations)":
                data["curricular_units_2nd_sem_without_evaluations"],


            "Unemployment rate":
                data["unemployment_rate"],

            "Inflation rate":
                data["inflation_rate"],

            "GDP":
                data["gdp"]
        }


        # ----------------------------------------------------
        # Create DataFrame
        # ----------------------------------------------------

        input_df = pd.DataFrame(
            [student_data]
        )


        # ----------------------------------------------------
        # Make prediction
        # ----------------------------------------------------

        prediction = model.predict(
            input_df
        )[0]


        # ----------------------------------------------------
        # Get probabilities
        # ----------------------------------------------------

        probabilities = model.predict_proba(
            input_df
        )[0]


        # ----------------------------------------------------
        # Get class names
        # ----------------------------------------------------

        class_names = model.classes_


        # ----------------------------------------------------
        # Create probability dictionary
        # ----------------------------------------------------

        probability_result = {}

        for class_name, probability in zip(
            class_names,
            probabilities
        ):

            probability_result[str(class_name)] = round(
                float(probability) * 100,
                2
            )


        # ----------------------------------------------------
        # Get dropout probability
        # ----------------------------------------------------

        dropout_probability = probability_result.get(
            "Dropout",
            0
        )


        # ----------------------------------------------------
        # Determine risk
        # ----------------------------------------------------

        if dropout_probability >= 70:

            risk_level = "HIGH"

        elif dropout_probability >= 40:

            risk_level = "MEDIUM"

        else:

            risk_level = "LOW"


        # ----------------------------------------------------
        # Return prediction
        # ----------------------------------------------------

        return {

            "prediction":
                str(prediction),

            "dropout_probability":
                dropout_probability,

            "risk_level":
                risk_level,

            "probabilities":
                probability_result
        }


    except Exception as error:

        print(
            "Prediction Error:",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# END OF FILE
# ============================================================