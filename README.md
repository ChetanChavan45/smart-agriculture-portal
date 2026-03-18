<div align="center">
  <img src="https://img.icons8.com/color/96/000000/tractor.png" alt="AgriPortal Logo"/>
  <h1>AgriPortal</h1>
  <p><strong>A Modern, Smart Agriculture Platform with AI-Powered Recommendations</strong></p>

  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python)](https://python.org)
  [![Django](https://img.shields.io/badge/Django-v4.2-green.svg?style=for-the-badge&logo=django)](https://djangoproject.com)
  [![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg?style=for-the-badge&logo=mysql)](https://mysql.com)
  [![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow.svg?style=for-the-badge&logo=javascript)](https://developer.mozilla.org/)
</div>

<hr/>

## 📖 Description
**AgriPortal** is a cutting-edge technological platform bridging the gap between farmers, agricultural data, and verified experts. Built as a full-stack Django Single Page Application (SPA), the system delivers dynamic community threads, interactive weather visualizations, and a state-of-the-art **Machine Learning Engine** tailored to maximize agricultural yields globally.

## ✨ Core Features

* 🌾 **Crop Information System**: A dynamic, categorized database of vast agricultural data. Includes detailed metrics on ideal seasons, soil structures, and water requirements.
* 💬 **Advanced Community Q&A**: A secure ecosystem enabling real-time interactions between local farmers and verified agricultural experts. Features status tracking (Pending/Answered), feedback polling (Helpful tags), and chronological sorting.
* 🤖 **Machine Learning Crop Recommendation**: Includes a deeply integrated *Scikit-Learn Decision Tree Classifier*. The engine ingests localized variables (Soil Type, Season, Water Availability) and intelligently curates a top-3 recommendation list coupled with AI-driven reasoning and confidence scoring.
* 🔍 **Zero-Reload Search & Filtering**: Built entirely on standard JavaScript Native Fetch APIs integrating against DRF headless endpoints. Users can cross-filter crops on factors like seasons and categories in milliseconds without page refreshes.

## 🛠️ Technology Stack
* **Backend Firmware**: Python, Django ~4.2, Django REST Framework
* **Artificial Intelligence**: Scikit-Learn (DecisionTreeClassifier), Numpy
* **Database Pipeline**: MySQL (production via `mysqlclient`), SQLite3 (local development)
* **Frontend Architecture**: HTML5, Vanilla JavaScript (ES6), Bootstrap 5 UI/UX, CSS3, Chart.js

---

## 📸 Platform Previews *(Screenshots)*

| **Home / Analytics Dashboard** | **Dynamic Explore Crops Page** |
| :---: | :---: |
| <img src="https://via.placeholder.com/600x350?text=Analytics+Dashboard+with+Charts" alt="Home Dashboard" /> | <img src="https://via.placeholder.com/600x350?text=Dynamic+Javascript+Crop+Search" alt="Crop Page" /> |

<br/>

| **🤖 AI Machine Learning Recommendation Engine** |
| :---: |
| <img src="https://via.placeholder.com/1200x500?text=Scikit-Learn+Decision+Tree+Recommendation+UI" alt="ML Interface" /> |

<br/>

## 🚀 Installation Architecture

To host or contribute to this infrastructure, follow the terminal instructions below.

**1. Clone the repository**
```bash
git clone https://github.com/ChetanChavan45/smart-agriculture-portal.git
cd smart-agriculture-portal
```

**2. Isolate your environment**
It's considered best practice to isolate Python dependencies per application.
```bash
python -m venv venv

# For Windows:
.\venv\Scripts\activate
# For Mac / Linux:
source venv/bin/activate
```

**3. Install dependencies**
Install the framework, database clients, and mathematical plotting software seamlessly:
```bash
pip install -r requirements.txt
```

**4. Build Database Schema**
Ensure the project routes the ORM instructions to your local database correctly:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🖥️ How to Run the Project
Once the installation phase succeeds, spinning up the localized development server takes seconds.
```bash
python manage.py runserver
```
Navigate to your web browser and open `http://127.0.0.1:8000/`.

---
*Developed with Passion for the Agricultural Community.*
