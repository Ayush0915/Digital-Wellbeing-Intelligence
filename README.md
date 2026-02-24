# 🧠 Digital Wellbeing Intelligence System (DWIS)

A production-ready Machine Learning web application that analyzes digital behavior patterns and generates actionable productivity insights using clustering and behavioral analytics.

---

## 🚀 What This Project Does

This system transforms daily screen activity metrics into meaningful digital wellbeing intelligence.

It:

- Segments users using **K-Means clustering**
- Calculates a **Productivity Score (0–100)**
- Calculates a **Digital Risk Score**
- Generates intelligent behavioral insights
- Displays interactive analytics using Plotly
- Runs on a FastAPI production backend

---

## 🧠 Machine Learning Approach

### ✔ Feature Engineering
Derived behavioral metrics such as:
- Interaction rate  
- Productivity ratio  
- Notification density  
- Unlock intensity  

### ✔ Standardization
Used `StandardScaler` to normalize features before clustering.

### ✔ K-Means Clustering
Unsupervised model used to segment users into:

- 🟢 Productive  
- 🟡 Balanced  
- 🔴 Distracted  

Models are persisted using `joblib` and loaded in production.

---

## 📊 Dashboard Features

Built using **FastAPI + Jinja2 + Plotly**:

- Behavior Status Badge  
- Productivity Gauge Visualization  
- Behavioral Radar Chart  
- AI-style Insight Generator  
- Clean minimal Apple-style UI  

---

## 🤖 Insight Engine

Designed a rule-based behavioral intelligence system that:

- Detects distraction patterns  
- Identifies attention fragmentation  
- Analyzes social usage dominance  
- Suggests measurable optimization strategies  

Example Insight:

> Reducing social usage by 30 minutes daily could significantly improve productivity score.

---

## 🛠 Tech Stack

**Backend**
- FastAPI  
- Uvicorn  

**Machine Learning**
- Scikit-learn  
- NumPy  
- Pandas  
- Joblib  

**Visualization**
- Plotly  

**Deployment**
- Render (Production-ready)

---

## 📂 Project Structure

```bash
DW-Digital-Wellbeing/
│
├── api/
├── app/
├── model/
├── requirements.txt
└── README.md
```

---

## 🎯 Key Highlights

✔ End-to-end ML pipeline  
✔ Unsupervised behavioral segmentation  
✔ Custom productivity scoring model  
✔ AI-style rule-based recommendation engine  
✔ Interactive deployed dashboard  

---