# AI Sales Lead Scoring Platform

An AI-powered CRM-style web application that helps organizations identify, score, and prioritize high-potential leads using machine learning.

## Project Overview

The AI Sales Lead Scoring Platform is designed to help sales teams improve efficiency by predicting which leads are most likely to convert into paying customers. Instead of manually reviewing large numbers of leads from websites, campaigns, referrals, and other sources, this platform uses machine learning models to analyze lead attributes and generate conversion insights.

The system provides a centralized Lead Management System with role-based dashboards for admins and sales users. It enables teams to manage leads, track CRM status, view performance analytics, and focus on the most promising opportunities.

Machine learning models such as **Logistic Regression** and **XGBoost** are used to generate lead scores and classify leads into categories such as **Hot**, **Warm**, and **Cold**.

---

## Features

- AI-based lead scoring
- Conversion probability prediction
- Lead classification into Hot, Warm, and Cold
- CRM-style lead management
- Admin dashboard with analytics
- Sales user dashboard with assigned leads
- Multi-user support with role-based access
- Bulk lead import through CSV/Excel-compatible format
- Contact page with message submission
- Sales pipeline tracking
- Source-wise lead analytics
- Top lead and conversion source tracking

---

## User Roles

### Admin
- View all leads
- Monitor overall analytics
- Track sales user performance
- Create sales users
- View contact messages
- Manage complete system data

### Sales User
- Add new leads
- Import leads in bulk
- View only assigned leads
- Update CRM status
- Edit or delete own leads
- Track personal dashboard metrics

---

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework

### Frontend
- HTML
- CSS
- JavaScript
- Chart.js

### Database
- MySQL

### Machine Learning
- Scikit-learn
- XGBoost

---

## Machine Learning Functionality

The platform uses machine learning models to predict lead conversion probability based on lead attributes such as:

- Company size
- Budget
- Interaction score
- Source
- Industry
- Interaction history

### Output
- Lead Score
- Conversion Probability
- AI Status:
  - Hot
  - Warm
  - Cold

---

## Main Modules

- Authentication and role-based login
- Lead registration and management
- AI prediction engine
- Admin dashboard analytics
- Sales dashboard
- Bulk import
- Contact message handling
- REST API for leads

---

## Project Structure

```bash
AI-Sales-Lead-Scoring-Platform/
│
├── backend/
│   ├── backend/
│   ├── crm/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── serializers.py
│   │   └── ...
│   ├── ml_engine/
│   │   └── predict.py
│   ├── manage.py
│   └── ...
│
└── README.md

---
## Screenshots

### 🔐 Login Page
<img width="1899" height="892" alt="Screenshot 2026-03-21 093624" src="https://github.com/user-attachments/assets/2e942abb-eee8-41ff-bc7c-a5f24818552d" />

### 🏠 Home Page
<img width="1905" height="888" alt="Screenshot 2026-03-21 093656" src="https://github.com/user-attachments/assets/d64f1620-676e-4081-8672-e4d40eb29cb6" />
<img width="1908" height="893" alt="Screenshot 2026-03-21 094100" src="https://github.com/user-attachments/assets/c3d4d22c-137f-4a37-9b86-7afc829e7332" />

### 📊 Admin Dashboard
<img width="1911" height="889" alt="Screenshot 2026-03-21 093806" src="https://github.com/user-attachments/assets/77879a5d-61af-4c2d-8032-6873a5079aa8" />
<img width="1913" height="881" alt="Screenshot 2026-03-21 093827" src="https://github.com/user-attachments/assets/decef9e0-fac8-40e0-972e-b593bc1b9034" />
<img width="1912" height="888" alt="Screenshot 2026-03-21 093846" src="https://github.com/user-attachments/assets/3df734c5-2262-48e8-bef2-02a5ff8614e2" />

### 📊 Sales Dashboard
<img width="1904" height="883" alt="Screenshot 2026-03-21 093736" src="https://github.com/user-attachments/assets/6b491dbf-8687-499a-a5c8-52c74f94a654" />

### ➕ Add Lead
<img width="1908" height="889" alt="Screenshot 2026-03-21 093958" src="https://github.com/user-attachments/assets/9a52e29d-c40c-42d0-a968-98544661265d" />

### 📬 Contact Message
<img width="1905" height="895" alt="Screenshot 2026-03-21 093914" src="https://github.com/user-attachments/assets/46405f66-97c9-421f-a0f4-058081b02cc1" />
