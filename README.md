# 🔥 CalorieTrack

A **free, full-stack calorie & nutrition tracker** built with Django.  
Beautiful TitanFit-inspired dark UI with light/dark mode toggle, animated charts, and a full food database.

---

## ✨ Features

| Feature | Details |
|---|---|
| 📊 **Dashboard** | Daily calorie ring, 4 macro stat cards, Energy Balance chart |
| 🍽 **Daily Fuel** | Log meals by Breakfast / Lunch / Dinner / Snack |
| 🔍 **Food Search** | Live search across 100+ built-in foods |
| ➕ **Custom Foods** | Add your own foods with full macro breakdown |
| ⚖️ **Weight Tracker** | Log weight with 90-day trend chart |
| 📅 **History** | 30-day calorie & macro bar charts |
| 🧮 **Calculator** | Multi-food meal builder with bulk log |
| 👤 **Profile** | Set calorie goal, height, weight, DOB, gender |
| 🌙 **Light / Dark Mode** | Persisted via localStorage, no flash |
| 🔐 **Auth** | Register, login, logout with secure session |

---

## � Project Structure

```
calorie-tracker/
│
├── api/
│   └── index.py              # Vercel WSGI entry point
│
├── calorie_counter/          # Django project config
│   ├── settings.py           # Settings (supports local + Vercel)
│   ├── urls.py               # Root URL config
│   └── wsgi.py
│
├── calories/                 # Main Django app
│   ├── views/                # Views split by concern
│   │   ├── __init__.py       # Re-exports all views
│   │   ├── auth.py           # Register / Login / Logout
│   │   ├── dashboard.py      # Dashboard with macro totals
│   │   ├── food_log.py       # Add / Edit / Delete food logs
│   │   ├── food_api.py       # JSON API: food search & detail
│   │   ├── food_custom.py    # Create custom food items
│   │   ├── calculator.py     # Food calculator + bulk log
│   │   ├── weight.py         # Weight tracker
│   │   ├── history.py        # 30-day history charts
│   │   └── profile.py        # User profile
│   │
│   ├── models.py             # UserProfile, FoodItem, FoodLog, WeightLog
│   ├── forms.py              # All Django forms
│   ├── admin.py              # Django admin registrations
│   ├── urls.py               # App URL patterns
│   │
│   ├── templatetags/
│   │   └── calorie_tags.py   # Custom template filter: get_item
│   │
│   └── management/commands/  # Custom management commands
│
├── templates/
│   ├── base.html             # Main layout (sidebar, topbar, alerts)
│   ├── dashboard.html        # TitanFit-style dashboard
│   ├── history.html          # 30-day history charts
│   ├── profile.html          # User profile form
│   ├── weight_tracker.html   # Weight logging + chart
│   ├── food_log_form.html    # Add / Edit food log form
│   ├── food_calculator.html  # Multi-food calculator
│   ├── custom_food.html      # Create custom food form
│   └── auth/
│       ├── login.html        # Premium split-layout sign-in
│       └── register.html     # Premium split-layout register
│
├── static/
│   ├── css/
│   │   └── style.css         # Complete design system (dark+light themes)
│   └── js/
│       ├── theme.js          # Light/dark mode toggle
│       ├── sidebar.js        # Mobile sidebar open/close
│       └── main.js           # Alerts, ring animations, date inputs
│
├── .env.example              # Environment variable template
├── vercel.json               # Vercel deployment config
├── build_files.sh            # Vercel build script (install + collectstatic + migrate)
├── requirements.txt          # Python dependencies
├── runtime.txt               # Python version for Vercel
└── manage.py
```

---

## 🚀 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/calorie-tracker.git
cd calorie-tracker

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env
# Edit .env — set DEBUG=True, leave DATABASE_URL empty for SQLite

# 5. Run migrations
python manage.py migrate

# 6. (Optional) Load sample food data
python manage.py load_foods   # if available

# 7. Create superuser (for /admin)
python manage.py createsuperuser

# 8. Run the server
python manage.py runserver

# Open http://127.0.0.1:8000
```

---

## ☁️ Vercel Deployment (Free)

### Step 1 — Free PostgreSQL Database
1. Go to [neon.tech](https://neon.tech) → "Get started free"
2. Create a project & copy the connection string

### Step 2 — Deploy to Vercel
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) → Import Project → select your repo
3. Set **Environment Variables** in the Vercel dashboard:

| Variable | Value |
|---|---|
| `SECRET_KEY` | Run: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `DATABASE_URL` | Your Neon PostgreSQL connection string |
| `ALLOWED_HOSTS` | `your-app.vercel.app` |

4. Click **Deploy** ✅

> **Total cost: $0/month** — Vercel hobby tier + Neon free tier are both completely free.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x (Python 3.11) |
| Database | PostgreSQL (Neon) / SQLite (local) |
| Static files | WhiteNoise (compressed + cached) |
| Hosting | Vercel (serverless Python) |
| Frontend | Vanilla HTML + CSS + JS |
| Charts | Chart.js 4 |
| Icons | Font Awesome 6 |
| Fonts | Google Fonts (Inter) |

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ | Django secret key — generate a random one |
| `DEBUG` | ✅ | `True` locally, `False` in production |
| `DATABASE_URL` | Production only | PostgreSQL connection string |
| `ALLOWED_HOSTS` | Production only | Comma-separated hostnames |

---

## 📄 License

MIT — free to use, modify, and deploy.
