# Refleksi-J Project

A comprehensive web-based reflection and module management system built with Django, htmx, and Tailwind CSS. This platform enables teachers to manage educational modules, create reflection journals, conduct surveys (angket), and utilize AI-powered feedback systems.

## Features

- **Module Management**: Upload, organize, and share educational modules with AI-powered analysis
- **Reflection Journals**: Daily reflection system with customizable templates
- **Survey System (Angket)**: Create and manage surveys for students and teachers
- **AI Integration**: ChatPDF integration for module component analysis and feedback
- **File Storage**: Vercel Blob storage integration for scalable file management
- **User Authentication**: Secure login system with email verification
- **Responsive Design**: Built with Tailwind CSS for mobile-friendly interface

## Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: htmx, Tailwind CSS
- **Database**: PostgreSQL
- **File Storage**: Vercel Blob Storage
- **AI Integration**: ChatPDF API
- **Email**: Gmail SMTP
- **Deployment**: Vercel

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL
- Node.js (for Tailwind CSS)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd "Refleksi-J Project"
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv refleksi-j-venv
   refleksi-j-venv\Scripts\activate  # Windows
   # source refleksi-j-venv/bin/activate  # Linux/Mac
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=postgresql://username:password@localhost:5432/refleksij
   
   # Email Configuration
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   
   # Vercel Blob Storage
   IS_VERCEL=False
   BLOB_READ_WRITE_TOKEN=your-vercel-blob-token
   
   # Other settings
   ALLOWED_HOSTS=localhost,127.0.0.1
   PARENT_HOST=localhost:8000
   ```

5. **Set up PostgreSQL database:**
   ```sql
   CREATE DATABASE refleksij;
   CREATE USER faris WITH PASSWORD 'your-password';
   GRANT ALL PRIVILEGES ON DATABASE refleksij TO faris;
   GRANT CREATE ON SCHEMA public TO faris;
   ```

6. **Install and configure Tailwind CSS:**
   ```bash
   npm install -g tailwindcss
   ```

7. **Build CSS (in separate terminal):**
   ```bash
   tailwindcss -i ./static/src/main.css -o ./static/src/output.css --watch
   ```

8. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

9. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

10. **Start development server:**
    ```bash
    python manage.py runserver
    ```

11. **Access the application:**
    - Main app: [http://localhost:8000/](http://localhost:8000/)
    - Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Project Structure

```
Refleksi-J Project/
├── config/              # Django settings and configuration
│   ├── settings.py      # Main settings
│   ├── urls.py          # URL configuration
│   ├── wsgi.py          # WSGI configuration
│   └── vercel_storage.py # Vercel Blob storage backend
├── core/                # Main application
│   ├── models.py        # Database models
│   ├── views/           # View modules
│   │   ├── main.py      # Main views
│   │   ├── module.py    # Module management
│   │   ├── journal.py   # Reflection journals
│   │   └── angket.py    # Survey system
│   ├── templates/       # HTML templates
│   └── urls.py          # App URLs
├── static/              # Static files
│   ├── src/             # Source files
│   │   ├── main.css     # Tailwind input
│   │   └── output.css   # Generated CSS
│   └── js/              # JavaScript files
├── templates/           # Global templates
├── utils/               # Utility functions
│   └── mail.py          # Email utilities
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel deployment config
└── .env                 # Environment variables
```

## Key Features Guide

### Module Management
- Upload educational modules (PDF, DOC, PPT)
- AI-powered component analysis via ChatPDF
- Organize modules by subjects
- Generate feedback and suggestions

### Reflection System
- Daily agenda and reflection entries
- Customizable reflection questions
- Historical reflection tracking
- Subject-based scheduling

### Survey System (Angket)
- Create surveys for students or teachers
- Multiple question types support
- Real-time response collection
- Result analysis and visualization

## Deployment

### Vercel Deployment

1. **Set environment variables in Vercel:**
   - All variables from `.env` file
   - Set `IS_VERCEL=True`
   - Configure `BLOB_READ_WRITE_TOKEN`

2. **Deploy:**
   ```bash
   vercel --prod
   ```

### Production CSS Build
```bash
tailwindcss -i ./static/src/main.css -o ./static/src/output.css --minify
```

## API Integration

### ChatPDF Setup
1. Get API key from ChatPDF
2. Add to environment variables
3. Configure in `utils/chatpdf.py`

### Vercel Blob Storage
1. Create Vercel Blob storage
2. Get read/write token
3. Add `BLOB_READ_WRITE_TOKEN` to environment

## Development

### Running Tests
```bash
# Test storage configuration
python test_blob.py

# Test module uploads
python test_module_upload.py

# Debug storage settings
python debug_storage.py
```

### Database Operations
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please create an issue in the repository.