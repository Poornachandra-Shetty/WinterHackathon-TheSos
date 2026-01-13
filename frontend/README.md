.

🧠 AI-Based Early Dementia Screening Web Application
📌 Overview

Early-stage dementia often goes undetected due to subtle symptoms, delayed clinical visits, and lack of accessible screening tools. This project presents an AI-powered web application that performs early dementia risk screening by analyzing cognitive task performance and speech patterns.

The system provides a low-cost, non-invasive, and accessible screening solution designed for elderly individuals, caregivers, and primary healthcare providers. It is intended strictly as a screening and risk-assessment tool, not a medical diagnosis.

🎯 Key Objectives

Enable early identification of cognitive decline

Reduce dependency on expensive or invasive diagnostic procedures

Provide explainable AI-driven insights

Ensure privacy and data safety

Facilitate easy access to results for caregivers and clinicians

🚀 Features
🧩 Cognitive Assessment

Memory-based tasks

Attention and reaction-time tests

Automatic scoring and normalization

🎤 Speech Analysis

Voice input analysis for cognitive markers

Feature extraction from speech patterns

AI-based risk inference

🤖 AI Risk Prediction

Machine learning–based dementia risk score (0–100)

Risk categorization: Low / Moderate / High

Confidence score indicating prediction reliability

Clinically interpretable recommendations

📄 Automated Google Docs Report Generation

Assessment results are automatically saved to Google Docs

Each submission generates a structured, readable report

Enables easy sharing with caregivers or healthcare professionals

No manual export required

🔒 Privacy-Focused Design

No storage of personal identifiers

No permanent storage of raw audio data

Only processed results are recorded

🛠️ Tech Stack
Frontend

React

HTML, CSS, JavaScript

Backend

Python

FastAPI

AI / Machine Learning

scikit-learn

NumPy

Pandas

Speech Processing

librosa

☁️ Google Technologies Used

Google Drive API

Google Cloud Platform 

Google Docs API
Automatically stores generated assessment reports in Google Docs for easy access and sharing.

📊 Output & Reporting

Upon completion of an assessment:

AI generates a dementia risk score and recommendations

A detailed assessment report is automatically written to Google Docs

Reports include:

Patient ID (anonymized)

Cognitive and speech risk scores

Confidence level

AI-generated insights and recommendations

This ensures persistent, shareable, and clinician-friendly output

⚙️ Setup Instructions
Run Locally

Clone the repository

Navigate to the backend directory

pip install -r requirements.txt


Train the AI model using the dummy dataset

python scripts/train_model.py


Start the backend server

uvicorn main:app --reload


Navigate to the frontend directory

npm install
npm run dev


Open the application in your browser and complete the cognitive and speech screening

⚠️ Medical Disclaimer

This application is intended only for early screening and awareness.
It does not provide a medical diagnosis.
Users are strongly advised to consult qualified healthcare professionals for clinical evaluation and diagnosis.

👥 Team Members

Shetty Poornachandra Jnanachandra

Sunil Jayappa Lamani

Shravan S Kotian

S Rohith