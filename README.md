# CalorieTracker Django MVP

> **Note:** This project is under progress and will be completed soon. Managed by Aditya Singh.

A production-ready, full-stack Calorie and Macronutrient Tracking application built on Django. This project implements a robust monolithic architecture, leveraging serverless deployment paradigms for zero-cost operational overhead via Vercel and Neon (PostgreSQL).

The user interface implements a premium, responsive dark/light mode design system (inspired by modern fitness applications) without relying on heavy frontend frameworks, prioritizing minimal payload size and rapid server-side rendering (SSR) via Django Templates.

---

## 🏗 System Architecture & Design Patterns

This application is designed with scalability and developer ergonomy in mind:

- **MVT (Model-View-Template) Architecture:** Adheres strictly to Django's core patterns, ensuring separation of concerns between database models, business logic (views), and presentation components.
- **Serverless Adaptability:** The `api/index.py` handles the WSGI instantiation for Vercel's serverless environment, allowing the traditional monolithic Django app to scale horizontally as stateless functions.
- **Environment Parity:** Utilizes `python-decouple` and `dj-database-url`. Development relies on an effortless SQLite3 configuration, while production seamlessly transitions to PostgreSQL with connection pooling.
- **Componentized Static Asset Delivery:** Static assets are aggressively hashed, compressed, and cached using `WhiteNoiseMiddleware`, eliminating the need for complex external CDN configurations (like AWS S3) for the MVP stage.
- **Fat Models, Skinny Views:** Core calculation logic (e.g., TDEE and Mifflin-St Jeor equations, dynamic calorie aggregates) are abstracted to Model properties and methods, keeping View controllers clean and testable.

---

## ✨ Core Features & Technical Implementation

| Feature | Implementation Detail |
|---|---|
| 📊 **Real-time Dashboard** | Daily calorie aggregates with Chart.js canvas visualizations rendering context data injected directly from Django views. |
| 🍽 **Journaling System** | Full CRUD capabilities for logging meals, grouped contextually by meal type (Breakfast, Lunch, Dinner, Snack). |
| 🔍 **AJAX Food Search** | Real-time queried JSON API (`food_search_api`) utilizing Django `Q` objects for efficient, secure substring searching of food indices. |
| 🧮 **Bulk Meal Calculation** | Accepts serialized JSON payloads for logging multi-item meals in a single atomic database transaction. |
| 🌒 **Theme Persistence** | Client-side `localStorage` state management combined with CSS Variables for instantaneous, flash-less light/dark mode transitions. |
| 🔐 **Authentication** | Built on `django.contrib.auth`, utilizing secure HTTP-only session cookies and robust password validation algorithms. |

---

## 🛠 Technology Stack

- **Backend:** Python 3.11, Django 5.x
- **Database:** PostgreSQL (Production via Neon.tech), SQLite3 (Local Development)
- **Deployment & Hosting:** Vercel (Serverless Edge Network)
- **Static Asset Pipeline:** WhiteNoise (Gzip/Brotli Compression)
- **Frontend / UI:** Vanilla HTML5, CSS3 Variables, ES6 JavaScript (No Build Step Required)
- **Data Visualization:** Chart.js 4.x

---

## 🚀 Local Development Environment Setup

To orchestrate the environment locally, execute the following shell commands:

```bash
# 1. Clone the repository
git clone https://github.com/imsinghaditya07/Calorie-teacker-using-Django.git
cd Calorie-teacker-using-Django

# 2. Bootstrap virtual environment
python -m venv venv
source venv/bin/activate  # UNIX/macOS
# .\venv\Scripts\activate # Windows

# 3. Resolve dependencies
pip install -r requirements.txt

# 4. Environment Configuration
cp .env.example .env
# Ensure DEBUG=True is set. DATABASE_URL can be omitted for fallback to SQLite3.

# 5. Database Initialization & Seeding
python manage.py migrate
python manage.py seed_foods  # Executes custom management command to populate 300+ food items

# 6. Admin Creation & Execution
python manage.py createsuperuser
python manage.py runserver
# Server operational at http://127.0.0.1:8000
```

---

## ☁️ Zero-Cost Production Deployment (Vercel)

The repository is configured for immediate CI/CD deployment via Vercel using `vercel.json` and `build_files.sh`.

### Prerequisites
1. Provision a free PostgreSQL database instance at [Neon](https://neon.tech).
2. Retrieve the Postgres connection string (ensure pooling is disabled if required by Vercel Edge).

### Vercel Configuration
1. Import the repository into the Vercel dashboard.
2. Inject the following Environment Variables into the project settings:

```plaintext
SECRET_KEY       = <Cryptographically secure random 50-character string>
DEBUG            = False
DATABASE_URL     = <Neon PostgreSQL Connection String>
ALLOWED_HOSTS    = <Your Vercel Production Domain>
```

3. Vercel will automatically execute `build_files.sh` (installing dependencies, collecting static files via WhiteNoise, and applying production migrations).

---

## 📂 Repository Structure

```text
├── api/                    # Vercel Serverless Function entry point
├── calorie_counter/        # Core Django Configuration (Settings, WSGI, Base Routing)
├── calories/               # Primary Application Module
│   ├── management/         # Custom CLI extensions (e.g., seed_foods)
│   ├── templatetags/       # Custom rendering filters for Django Templates
│   ├── views/              # Segmented controller logic (Auth, API, Logging)
│   ├── models.py           # Relational schema definitions
│   └── forms.py            # Data validation and sanitary payload handling
├── static/                 # Raw frontend assets (CSS, JS, Fonts)
├── templates/              # Server-side rendered HTML components
├── requirements.txt        # Exacting package dependencies
└── vercel.json             # Vercel execution and routing rules
```

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
