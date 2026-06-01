# GetGig

GetGig is a modern, community-driven social freelancing platform designed to connect elite talent with visionary clients. By eliminating traditional bidding wars, GetGig focuses on high-quality matches powered by transparent project requirements, automated vetting logic, and real-time user notifications.

---

## Features

- **Dynamic Landing Page:** Fully customizable hero section, marketing copy, and assets managed through the Django admin via `SiteConfiguration`.
- **Dual-Dashboard Architecture:**
  - **Clients:** Post projects, define clear requirements, track incoming proposals, and vet applications.
  - **Freelancers:** Browse active gigs, match requirements, submit tailored proposals, and monitor application status.
- **Deadline-aware gigs:** Projects display active, due soon, happening today, or ended states.
- **Custom User Model:** Separate `client` and `freelancer` account types are supported from registration.
- **In-App Notifications:** Alerts are created automatically when freelancers apply or when application status changes.

---

## Tech Stack

- **Backend:** Django 6.x
- **Frontend:** Tailwind CSS (via CDN), HTML5, Django Template Language (DTL)
- **Database:** SQLite for development, PostgreSQL compatible for production
- **Image Handling:** Pillow
- **PWA support:** `django-pwa`
- **Storage foundations:** `django-storages`

---

## Getting Started

### Prerequisites
Make sure Python 3.10+ is installed on your machine.

### 1. Clone the repository
```bash
git clone https://github.com/your-username/GetGig.git
cd GetGig
```

### 2. Set up a virtual environment
```bash
python -m venv venv
```

### 3. Activate the environment
- On Windows:
```powershell
venv\Scripts\Activate.ps1
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run database migrations
```bash
python manage.py migrate
```

### 6. Create an admin account
```bash
python manage.py createsuperuser
```

### 7. Start the development server
```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Django Admin

The Django admin is useful for:
- editing `SiteConfiguration` hero title, subtitle, and hero image
- managing users and their freelancer/client profile details
- reviewing applications and vetting proposals

Access the admin at `/admin/` after creating a superuser.

---

## Production / Deployment Notes

- Replace the default `SECRET_KEY` with a secure value
- Set `DEBUG = False` in `core/settings.py`
- Use a production database such as PostgreSQL
- Collect static files before serving them:
```bash
python manage.py collectstatic
```
- Configure environment variables for your deployment platform

---

## Project Structure

## Project Structure 
```
GetGig/
│
├── core/                  # Project configuration directory (settings, urls)
│   ├── settings.py
│   └── urls.py
│
├── projects/              # Main application logic
│   ├── models.py          # Project, Application, SiteConfiguration models
│   ├── views.py           # Dashboard rendering, vetting logic, landing page controllers
│   ├── urls.py            # Project routing
│   └── forms.py           # ProjectForm, ApplicationForm
│
├── users/                 # Custom authentication app
│   ├── models.py          # CustomUser, Profile, Notification models
│   └── urls.py
│
└── templates/             # HTML templates (Base, Landing, Dashboards)

```
