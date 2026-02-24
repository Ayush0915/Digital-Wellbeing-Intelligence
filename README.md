# 🧠 DW – Digital Wellbeing Behavioral Intelligence System

A multi-user behavioral analytics system that segments smartphone users into digital wellbeing archetypes using unsupervised learning.

---

## 🚀 Project Overview

This project analyzes multi-user smartp hone activity logs and applies behavioral feature engineering with KMeans clustering to identify digital engagement patterns.

Users are segmented into:

- 🎯 Balanced Productive Users
- 🚨 Distracted Users
- 📱 High Engagement Users

Cluster validation is performed using:
- Elbow Method
- Silhouette Score

---

## 🛠 Tech Stack

- Python
- Pandas
- Scikit-learn
- Matplotlib
- Seaborn

---

## 🧠 ML Pipeline

1. Data aggregation per user
2. Behavioral feature engineering
3. Standardization (StandardScaler)
4. KMeans clustering
5. Cluster validation
6. Behavioral interpretation

---

## 📊 Results

- 3 distinct behavioral segments identified
- Silhouette Score ≈ 0.28
- Balanced cluster distribution

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python main.py