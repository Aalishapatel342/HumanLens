# 🔍 AI Content Detector

A Django-based web application that uses advanced linguistic analysis to detect whether text is human-written or AI-generated.

## ✨ Features

- ✅ **Instant Analysis** - Real-time detection of AI vs human text
- ✅ **No API Keys Needed** - Completely local processing
- ✅ **Beautiful UI** - Modern, responsive design
- ✅ **Detailed Results** - Confidence scores and analysis breakdown
- ✅ **Fast Performance** - No external dependencies
- ✅ **Easy to Run** - Simple setup process

## 🚀 Quick Start (30 seconds)

### Method 1: Super Easy (Single File)

```bash
# 1. Install dependencies
pip install Django==4.2.0

# 2. Run the application
python easy_run.py
```

That's it! Visit **http://localhost:8000**

---

### Method 2: Full Django Project Setup

#### Step 3: Run Migrations

```bash
python manage.py migrate
```

#### Step 4: Start Development Server

```bash
python manage.py runserver
```

Visit **http://localhost:8000** in your browser.

---

## 📁 Project Structure

```
ai_detector_project/
├── manage.py                 # Django management script
├── settings.py              # Django configuration
├── wsgi.py                  # WSGI application
├── requirements.txt         # Python dependencies
├── db.sqlite3              # Database (auto-created)
│
├── detector/               # Django app
│   ├── __init__.py
│   ├── models.py           # Database models
│   ├── views.py            # API endpoints & logic
│   ├── urls.py             # URL routing
│   ├── migrations/
│   │   └── __init__.py
│
├── core/                   # Project configuration
│   ├── __init__.py
│   ├── urls.py             # Main URL config
│   └── wsgi.py
│
├── templates/
│   └── index.html          # Main page
│
└── static/                 # CSS, JS, images (if needed)
```

---

## 📊 How the Detector Works

The application analyzes text using multiple linguistic features:

### Human Writing Indicators ✓
- Contractions (don't, can't, I'm)
- Personal pronouns (I, we, you)
- Natural conversation patterns
- Questions and exclamations
- Varied vocabulary
- Diverse sentence structures

### AI Writing Indicators ⚠
- Formal transitions (furthermore, moreover)
- Repetitive word patterns
- Overly structured content
- Lack of contractions
- Formal language

### Confidence Scoring

```
Confidence > 65%  → HUMAN (✓)
Confidence < 35%  → AI (⚠)
35% - 65%         → MIXED (?)
```

---

## 🎯 API Documentation

### Endpoint: POST `/api/detect/`

**Request:**
```json
{
    "text": "Your text to analyze..."
}
```

**Response:**
```json
{
    "success": true,
    "result": "human",
    "confidence": 0.85,
    "word_count": 250,
    "explanation": "Analysis details...",
    "message": "✓ Appears to be human-written"
}
```

**Result Values:**
- `human` - Detected as human-written
- `ai` - Detected as AI-generated
- `mixed` - Unclear or mixed characteristics

---

## 🛠️ Configuration

### Change Detection Sensitivity

Edit `views.py` in the `analyze_text()` function:

```python
# Adjust these thresholds (0-1 scale)
if confidence > 0.65:          # Increase for stricter detection
    result = 'human'
elif confidence < 0.35:        # Decrease for stricter detection
    result = 'ai'
else:
    result = 'mixed'
```

### Change UI Colors

Edit the `<style>` section in `index.html`:

```css
/* Change gradient colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Or use single color */
background: #667eea;
```

### Change Server Port

```bash
# Default is 8000
python manage.py runserver 8001
python manage.py runserver 0.0.0.0:3000
```

---

## 🔐 Production Deployment

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run production server
gunicorn settings.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```bash
docker build -t ai-detector .
docker run -p 8000:8000 ai-detector
```

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
# or find and kill the process
lsof -i :8000
kill -9 <PID>
```

### "Database locked" error
```bash
# Delete the database and start fresh
rm db.sqlite3
python manage.py migrate
```

### CSRF token missing
- Make sure cookies are enabled
- Check browser console for errors
- Try clearing browser cache

### Module not found errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Changes not reflected
```bash
# Clear Django cache
python manage.py clear_cache
# or restart the server
```

---
Good luck! 🚀
