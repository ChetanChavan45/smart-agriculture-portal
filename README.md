<div align="center">
  <img src="https://img.icons8.com/color/96/000000/tractor.png" alt="Tractor Icon"/>
  <h1>AgriPortal - AI Smart Agriculture Platform</h1>
  <p><strong>A production-grade, AI-powered agricultural hub connecting farmers, verified experts, and intelligent data systems.</strong></p>
  
  [![Django](https://img.shields.io/badge/Django-v4.2-green.svg?style=for-the-badge&logo=django)](https://djangoproject.com)
  [![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML_Engine-orange.svg?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
  [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-blue.svg?style=for-the-badge&logo=bootstrap)](https://getbootstrap.com)
  [![Javascript](https://img.shields.io/badge/JavaScript-ES6-yellow.svg?style=for-the-badge&logo=javascript)](https://developer.mozilla.org/)
</div>

<hr/>

## 🌟 Overview
AgriPortal is a next-generation real-world platform designed to optimize farming ecosystems. Powered by **Python, Django, and Machine Learning (Scikit-Learn)**, the platform serves as an interactive bridge between farmers and agricultural experts. It replaces static farming lists with dynamic, real-time filtering, live weather feeds, and AI-driven recommendations.

## 🔥 Key Startup-Level Features

* 🤖 **Smart AI Crop Recommendation Engine:** Integrated Scikit-Learn **DecisionTreeClassifier** analyzing Soil Type, Season, and Water Availability to intelligently recommend the perfect crop via a blazing-fast AJAX payload interface.
* 🌦️ **OpenWeatherMap Integration:** Live dashboard weather widget rendering Temperature, Humidity, and conditions seamlessly using asynchronous ES6 Javascript fetching.
* ⚡ **Javascript Dynamic Frontend Architecture:** Zero-reload SPA-like experiences. Browse, search, and filter the crop database dynamically utilizing DRF endpoints and the raw Javascript Fetch API.
* 💬 **Interactive Community Q&A Ecosystem:** A robust thread system where farmers ask questions and *Verified Experts* respond. Features "Helpful" toggle states, instant Toast notification feedback, and conditional UI badging.
* 📊 **Enterprise Data Visualization:** Admin and Farmer dashboards fueled by **Chart.js** displaying questions-asked-over-time graphs and multi-color crop category distribution doughnuts.
* 🎨 **Premium UI/UX System:** Completely responsive Bootstrap 5 interface built with glass-morphism navbars, shadow-sm hovering cards, FontAwesome/Bootstrap icons, and centralized system-wide Toast notifications.

## 🛠️ Tech Stack & Architecture

| Layer | Technologies Used |
| :--- | :--- |
| **Backend & APIs** | Python 3, Django ~4.2, Django REST Framework |
| **Machine Learning** | Scikit-Learn (Decision Tree), Numpy |
| **Frontend UI** | HTML5, Bootstrap 5.3, CSS3, `crispy-bootstrap5` |
| **Frontend Logic** | Vanilla JavaScript (ES6), Fetch API, Chart.js, AJAX |
| **Database** | SQLite3 (configured for easy MySQL drop-in via `mysqlclient`) |
| **File Handling** | Pillow (Image Processing) |

<br/>

## 🚀 Installation & Local Environment Setup

AgriPortal was designed to be running locally in less than 2 minutes. 

```bash
# 1. Clone the repository
git clone https://github.com/ChetanChavan45/smart-agriculture-portal.git

# 2. Enter directory and spin up a virtual environment
cd smart-agriculture-portal
python -m venv venv

# 3. Activate the environment (Windows)
.\venv\Scripts\activate
# For Mac/Linux: source venv/bin/activate

# 4. Install all exact dependencies (including scikit-learn)
pip install -r requirements.txt

# 5. Execute migrations to build database tables
python manage.py makemigrations
python manage.py migrate

# 6. Ignite the server! 🔥
python manage.py runserver
```

### 🎮 Demo Instructions
Once running, navigate to `http://127.0.0.1:8000/`. You can log in as a Farmer to query the AI Recommendation engine and ask questions, or as an Expert to gain analytical insights and answer community threads!

---
*Built with ❤️ to revolutionize agriculture worldwide.*
