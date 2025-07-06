---

# 🚀 30 Days Dev Challenge – Project Showcase Platform

This is an open-source platform built using Django that showcases all projects contributed by participants of the **30 Days Dev Challenge**. It includes a contributor scoring system based on pull requests, issues, and labels, along with badge assignment and a dynamic leaderboard.

---

## 🔧 Features

- Automatically fetches issues and pull requests from GitHub
- Calculates contributor scores based on defined label weights
- Assigns ranks and badges
- Displays a project showcase
- Open-source and editable by participants

---

## ⚙️ Tech Stack

- **Backend**: Django (Python)
- **Database**: PostgreSQL (Recommended), SQLite (for local testing)
- **Frontend**: HTML/CSS, Bootstrap (optional)
- **Other**: GitHub API, TQDM (for CLI progress display)

---

## 🛢️ Database Environment

The platform uses **PostgreSQL** for robust production support. You can also use **SQLite** for lightweight local development and testing.

### 1. PostgreSQL Setup

If using PostgreSQL:

- Install PostgreSQL and ensure it is running
- Create a database (e.g., `dev_challenge`)
- Update `settings.py` or `.env` with:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=dev_challenge
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

And in settings.py:

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST", "localhost"),
        'PORT': os.getenv("DB_PORT", "5432"),
    }
}
```
2. SQLite (For Quick Local Testing)

Django uses SQLite by default. If no database environment is configured, SQLite will work out of the box.


---

## 📦 Setup Instructions

1. Clone the Repository


```
git clone https://github.com/<your-org>/<repo-name>.git
cd <repo-name>
```
2. Create and Activate a Virtual Environment


```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install the Dependencies


```
pip install -r requirements.txt
```
4. Create a .env File



Create a .env in the root directory:
```
GITHUB_TOKEN=your_github_token
REPO_OWNER=your_github_username_or_org
REPO_NAME=your_repo_name
# Optional: Database env variables if using PostgreSQL
```
5. Apply Migrations


```
python manage.py makemigrations
python manage.py migrate
```
6. Run the GitHub Data Fetcher


```
python manage.py fetch_github_data
```
7. Run the Development Server


```
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser.


---

🧪 Testing

Run tests with:
```
python manage.py test
```

---

🤝 Contributing

This is an open-source initiative. Participants are encouraged to open PRs and collaborate on both backend and frontend.

---

📄 License

MIT License

---

Let me know if you want me to add:

- Docker setup
- Deployment instructions (Render, Heroku, etc.)
- `.env.example` file
- Screenshots or badges for your repo

