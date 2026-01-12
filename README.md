AI-Based Early Dementia Screening Web Application
Description

This project is a web-based AI screening system designed to identify early signs of dementia by analyzing cognitive task performance and speech patterns. Dementia often goes undiagnosed in its early stages due to subtle symptoms and lack of accessible screening tools. Our solution provides a low-cost, non-invasive, and accessible screening platform that helps users and caregivers detect cognitive decline early and seek timely medical consultation. The system is intended for elderly users, caregivers, and primary healthcare providers as an early risk-assessment tool (not a medical diagnosis).

Features

Web-based cognitive screening using memory, attention, and reaction-time tasks

Speech analysis using AI to extract cognitive markers from voice input

AI-generated dementia risk score with clear, explainable output

Privacy-focused design with no storage of personal or raw audio data

Tech Stack

Frontend: React, HTML, CSS, JavaScript

Backend: Python, FastAPI

AI / ML: scikit-learn, NumPy, Pandas

Speech Processing: librosa

Deployment & Cloud: Google Cloud Platform, Firebase Hosting

Google Technologies Used


Google Cloud Speech-to-Text – Used to convert user speech into text, enabling AI-based speech and language analysis for early dementia screening

Google Cloud Platform (Cloud Run) – Used to deploy and scale the backend AI inference service securely

Firebase Hosting – Used to host the web application with fast global delivery and high availability

Setup Instructions

Steps to run the project locally:

Clone the repository

Navigate to the backend folder and install dependencies using pip install -r requirements.txt

Train the AI model using the provided dummy dataset (python scripts/train_model.py)

Start the backend server using uvicorn main:app --reload

Navigate to the frontend folder, install dependencies, and start the web application

Access the application in your browser and run the cognitive and speech screening

Team Members

Name 1

Name 2

Name 3