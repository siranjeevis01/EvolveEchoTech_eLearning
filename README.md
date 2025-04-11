# EvolveEchoTech eLearning Platform

**EvolveEchoTech** is a modern, scalable, and feature-rich eLearning platform built with Django and MySQL. It empowers users to explore, enroll, and manage courses seamlessly, while offering powerful administrative and interactive tools. Designed for flexibility and performance, this application is ideal for online learning environments.

---

## 🚀 Features

- 🎓 **Course Management**: Create, view, edit, and delete courses with detailed content.
- 👥 **User Roles**: Separate dashboards for Admins, Instructors, and Students.
- 🔒 **Authentication**: Secure user registration, login, logout, and password management.
- 📚 **Interactive Learning**: Course videos, notes, quizzes, and progress tracking.
- 📈 **Analytics Dashboard**: Admin dashboard for monitoring user and course stats.
- 🧾 **Certificates**: Auto-generated completion certificates.
- 📬 **Contact & Support**: User contact form and admin notifications.
- 📂 **File Uploads**: Video lectures, PDFs, and other materials.

---

## 🛠 Tech Stack

| Layer         | Technology                      |
|---------------|----------------------------------|
| Backend       | Django 5.2 (Python 3.11)         |
| Frontend      | HTML5, CSS3, Bootstrap           |
| Database      | MySQL                           |
| Environment   | Virtualenv (`env311`)            |
| Versioning    | Git + GitHub                     |

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   
   git clone https://github.com/siranjeevis01/EvolveEchoTech_eLearning.git
   cd EvolveEchoTech_eLearning

2. **Set up virtual environment**
   
  python -m venv env311
  env311\Scripts\activate

3. **Install dependencies**
   
   pip install -r requirements.txt

4. **Configure MySQL**
   
    Ensure MySQL server is running.
    Create a database named evolveecho_tech_elearning.
    Update DATABASES in myproject/settings.py with your credentials.

5. **Run migrations**
   
    python manage.py makemigrations
    python manage.py migrate

6. **Create superuser**
   
    python manage.py createsuperuser

7. **Start development server**
   
   python manage.py runserver

📸 Screenshots
You can add screenshots of:

Homepage
Course detail page
Admin dashboard
Student and instructor dashboard

✍️ Author
Siranjeevi
💼 Passionate Full-Stack Developer | Django Enthusiast | Innovator in EdTech
🔗 GitHub
