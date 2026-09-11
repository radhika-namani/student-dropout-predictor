// ============================================================
// API URL
// ============================================================

const API_URL = "http://127.0.0.1:8000/predict";


// ============================================================
// GET ELEMENTS
// ============================================================

const form = document.getElementById("predictionForm");

const predictButton =
    document.getElementById("predictButton");

const loading =
    document.getElementById("loading");

const error =
    document.getElementById("error");

const errorMessage =
    document.getElementById("errorMessage");

const result =
    document.getElementById("result");


// ============================================================
// FORM SUBMISSION
// ============================================================

form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // Hide previous messages

        error.classList.add("hidden");

        result.classList.add("hidden");


        // Show loading

        loading.classList.remove("hidden");

        predictButton.disabled = true;


        try {

            // ==================================================
            // CREATE STUDENT DATA
            // ==================================================

            const studentData = {

                marital_status:
                    Number(
                        document.getElementById(
                            "marital_status"
                        ).value
                    ),

                application_mode:
                    Number(
                        document.getElementById(
                            "application_mode"
                        ).value
                    ),

                application_order:
                    Number(
                        document.getElementById(
                            "application_order"
                        ).value
                    ),

                course:
                    Number(
                        document.getElementById(
                            "course"
                        ).value
                    ),

                daytime_evening_attendance:
                    Number(
                        document.getElementById(
                            "daytime_evening_attendance"
                        ).value
                    ),

                previous_qualification:
                    Number(
                        document.getElementById(
                            "previous_qualification"
                        ).value
                    ),

                previous_qualification_grade:
                    Number(
                        document.getElementById(
                            "previous_qualification_grade"
                        ).value
                    ),

                nationality:
                    Number(
                        document.getElementById(
                            "nationality"
                        ).value
                    ),

                mothers_qualification:
                    Number(
                        document.getElementById(
                            "mothers_qualification"
                        ).value
                    ),

                fathers_qualification:
                    Number(
                        document.getElementById(
                            "fathers_qualification"
                        ).value
                    ),

                mothers_occupation:
                    Number(
                        document.getElementById(
                            "mothers_occupation"
                        ).value
                    ),

                fathers_occupation:
                    Number(
                        document.getElementById(
                            "fathers_occupation"
                        ).value
                    ),

                admission_grade:
                    Number(
                        document.getElementById(
                            "admission_grade"
                        ).value
                    ),

                displaced:
                    Number(
                        document.getElementById(
                            "displaced"
                        ).value
                    ),

                educational_special_needs:
                    Number(
                        document.getElementById(
                            "educational_special_needs"
                        ).value
                    ),

                debtor:
                    Number(
                        document.getElementById(
                            "debtor"
                        ).value
                    ),

                tuition_fees_up_to_date:
                    Number(
                        document.getElementById(
                            "tuition_fees_up_to_date"
                        ).value
                    ),

                gender:
                    Number(
                        document.getElementById(
                            "gender"
                        ).value
                    ),

                scholarship_holder:
                    Number(
                        document.getElementById(
                            "scholarship_holder"
                        ).value
                    ),

                age_at_enrollment:
                    Number(
                        document.getElementById(
                            "age_at_enrollment"
                        ).value
                    ),

                international:
                    Number(
                        document.getElementById(
                            "international"
                        ).value
                    ),


                // ==================================================
                // FIRST SEMESTER
                // ==================================================

                curricular_units_1st_sem_credited:
                    Number(
                        document.getElementById(
                            "curricular_units_1st_sem_credited"
                        ).value
                    ),

                curricular_units_1st_sem_enrolled:
                    Number(
                        document.getElementById(
                            "curricular_units_1st_sem_enrolled"
                        ).value
                    ),

                curricular_units_1st_sem_evaluations:
                    Number(
                        document.getElementById(
                            "curricular_units_1st_sem_evaluations"
                        ).value
                    ),

                curricular_units_1st_sem_approved:
                    Number(
                        document.getElementById(
                            "curricular_units_1st_sem_approved"
                        ).value
                    ),

                curricular_units_1st_sem_grade:
                    Number(
                        document.getElementById(
                            "curricular_units_1st_sem_grade"
                        ).value
                    ),

                curricular_units_1st_sem_without_evaluations:
                    Number(
                        document.getElementById(
                            "curricular_units_1st_sem_without_evaluations"
                        ).value
                    ),


                // ==================================================
                // SECOND SEMESTER
                // ==================================================

                curricular_units_2nd_sem_credited:
                    Number(
                        document.getElementById(
                            "curricular_units_2nd_sem_credited"
                        ).value
                    ),

                curricular_units_2nd_sem_enrolled:
                    Number(
                        document.getElementById(
                            "curricular_units_2nd_sem_enrolled"
                        ).value
                    ),

                curricular_units_2nd_sem_evaluations:
                    Number(
                        document.getElementById(
                            "curricular_units_2nd_sem_evaluations"
                        ).value
                    ),

                curricular_units_2nd_sem_approved:
                    Number(
                        document.getElementById(
                            "curricular_units_2nd_sem_approved"
                        ).value
                    ),

                curricular_units_2nd_sem_grade:
                    Number(
                        document.getElementById(
                            "curricular_units_2nd_sem_grade"
                        ).value
                    ),

                curricular_units_2nd_sem_without_evaluations:
                    Number(
                        document.getElementById(
                            "curricular_units_2nd_sem_without_evaluations"
                        ).value
                    ),


                // ==================================================
                // ECONOMIC INFORMATION
                // ==================================================

                unemployment_rate:
                    Number(
                        document.getElementById(
                            "unemployment_rate"
                        ).value
                    ),

                inflation_rate:
                    Number(
                        document.getElementById(
                            "inflation_rate"
                        ).value
                    ),

                gdp:
                    Number(
                        document.getElementById(
                            "gdp"
                        ).value
                    )

            };


            // ==================================================
            // SEND REQUEST TO FASTAPI
            // ==================================================

            const response = await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            studentData
                        )
                }
            );


            // ==================================================
            // CHECK RESPONSE
            // ==================================================

            if (!response.ok) {

                const errorData =
                    await response.json();

                throw new Error(
                    errorData.detail ||
                    "Prediction request failed."
                );

            }


            // ==================================================
            // GET RESULT
            // ==================================================

            const data =
                await response.json();


            // ==================================================
            // DISPLAY RESULT
            // ==================================================

            displayResult(data);


        } catch (err) {

            console.error(err);

            errorMessage.textContent =
                err.message ||
                "Unable to connect to the prediction server.";

            error.classList.remove("hidden");

        } finally {

            loading.classList.add("hidden");

            predictButton.disabled = false;

        }

    }
);


// ============================================================
// DISPLAY RESULT
// ============================================================

function displayResult(data) {


    // Show result section

    result.classList.remove("hidden");


    // Prediction

    document.getElementById(
        "prediction"
    ).textContent =
        data.prediction;


    // Dropout probability

    document.getElementById(
        "dropoutProbability"
    ).textContent =
        data.dropout_probability + "%";


    // Risk level

    const riskLevel =
        document.getElementById(
            "riskLevel"
        );

    riskLevel.textContent =
        data.risk_level;


    // ========================================================
    // RISK CARD
    // ========================================================

    const riskCard =
        document.getElementById(
            "riskCard"
        );


    // Remove previous classes

    riskCard.classList.remove(
        "risk-low",
        "risk-medium",
        "risk-high"
    );


    // Add appropriate class

    if (
        data.risk_level === "LOW"
    ) {

        riskCard.classList.add(
            "risk-low"
        );

    }

    else if (
        data.risk_level === "MEDIUM"
    ) {

        riskCard.classList.add(
            "risk-medium"
        );

    }

    else if (
        data.risk_level === "HIGH"
    ) {

        riskCard.classList.add(
            "risk-high"
        );

    }


    // ========================================================
    // PROBABILITIES
    // ========================================================

    const probabilityList =
        document.getElementById(
            "probabilityList"
        );


    probabilityList.innerHTML = "";


    const probabilities =
        data.probabilities;


    for (
        const [className, probability]
        of Object.entries(probabilities)
    ) {


        // Create item

        const item =
            document.createElement(
                "div"
            );

        item.className =
            "probability-item";


        // Header

        const header =
            document.createElement(
                "div"
            );

        header.className =
            "probability-header";


        const name =
            document.createElement(
                "span"
            );

        name.textContent =
            className;


        const percentage =
            document.createElement(
                "span"
            );

        percentage.textContent =
            probability + "%";


        header.appendChild(name);

        header.appendChild(
            percentage
        );


        // Progress bar container

        const progress =
            document.createElement(
                "div"
            );

        progress.className =
            "progress";


        // Progress bar

        const bar =
            document.createElement(
                "div"
            );

        bar.className =
            "progress-bar";


        bar.style.width =
            probability + "%";


        progress.appendChild(bar);


        // Add everything

        item.appendChild(header);

        item.appendChild(progress);

        probabilityList.appendChild(item);

    }


    // ========================================================
    // SCROLL TO RESULT
    // ========================================================

    result.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}