# Smart Agriculture Portal

An Agriculture Information Portal built with Django, designed to help farmers with crop information, community Q&A, and agricultural best practices.

## Features

- **Farmer Dashboard**: Customized dashboard for farmers to access agricultural information.
- **Admin Dashboard**: Dashboard for administrators to manage crops, users, and content.
- **Crop Information system**: Add, view, and read details about various crops, their growing seasons, and soil requirements.
- **Community Q&A**: A dynamic question and answer forum for farmers to discuss agricultural queries.
- **Image Support**: Upload and display images of crops and agricultural practices.
- **Secure Backend**: Built with Django's robust authentication and MySQL database support.

## Technologies Used

- **Backend Framework**: Django ~4.2
- **Database**: MySQL (`mysqlclient`)
- **API**: Django REST Framework
- **Frontend/Forms**: Django Crispy Forms, crispy-bootstrap5
- **Image Processing**: Pillow

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ChetanChavan45/smart-agriculture-portal.git
   cd smart-agriculture-portal
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration:**
   Configure your MySQL database connection details in `agri_portal/settings.py` or through your `.env` file.

5. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (Optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load Initial Data (Optional):**
   ```bash
   python load_data.py
   ```

8. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Access the portal at `http://127.0.0.1:8000/`.

## License

This project is open-source and available for the farming community.
