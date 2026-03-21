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
<img width="1899" height="892" alt="Login" src="https://github.com/user-attachments/assets/c310dc3c-86b7-4fad-9823-f4a8c1eda76b" />

### 🏠 Home Page
<img width="1905" height="888" alt="Home_1" src="https://github.com/user-attachments/assets/b08b9bef-4332-40da-b7b4-ac4b89c40a31" />
<img width="1908" height="893" alt="Home_2" src="https://github.com/user-attachments/assets/4d942a54-a102-4ab6-bf43-be63f0ceac83" />

### 📊 Admin Dashboard
<img width="1911" height="889" alt="Admin_Dashboard_1" src="https://github.com/user-attachments/assets/1bab543f-79d4-4596-a2da-88f02b81de66" />
<img width="1913" height="881" alt="Admin_dashboard_2" src="https://github.com/user-attachments/assets/287ed089-131a-4f34-a97f-94bd6b643f99" />
<img width="1912" height="888" alt="Admin_Dashboard_3" src="https://github.com/user-attachments/assets/24973d02-9f30-4cc2-be95-153a4e6701c5" />

### 📊 Sales Dashboard
<img width="1904" height="883" alt="Sales_Dashboard" src="https://github.com/user-attachments/assets/e5e334f6-7089-4a8b-8109-0dbcdc4c2352" />

### ➕ Add Lead
<img width="1908" height="889" alt="Add_Lead" src="https://github.com/user-attachments/assets/35c00306-ef34-4b9c-a012-8f9422b2efcc" />

### 📬 Contact Message
<img width="1905" height="895" alt="Contact_Message" src="https://github.com/user-attachments/assets/146acda7-909a-4869-aab3-eeb7098f037b" />

##Author
-Kavya Yalapalli
-GitHub: YalapalliKavya
