# AI Content Detector - Setup & Run Guide

A Django-based application to detect whether text is human-written or AI-generated.

## 🚀 Quick Start

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Setup Django Project Structure

Create the following directory structure:
```
your_project/
├── manage.py
├── settings.py
├── wsgi.py
├── urls.py (rename to core_urls.py in actual project)
├── requirements.txt
├── detector/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│       └── __init__.py
└── templates/
    └── index.html
```

### Step 3: Create Django App

```bash
python manage.py startapp detector
```

### Step 4: Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

## 📝 How It Works

### Text Analysis Algorithm

The detector analyzes text using linguistic features:

1. **Contractions** - More common in human writing (don't, can't, I'm)
2. **Personal Pronouns** - Natural human conversation uses "I", "we", "you"
3. **Question Marks & Exclamations** - Natural speech patterns
4. **Formal Transitions** - AI often uses "furthermore", "moreover", "consequently"
5. **Word Variety** - Diversity of vocabulary
6. **Repetition Patterns** - AI tends to repeat words
7. **Sentence Structure** - Variety in sentence length and structure

### Result Categories

- **✓ Human Written** (Confidence > 65%)
- **⚠ AI Generated** (Confidence < 35%)
- **? Mixed/Unclear** (Between 35-65%)

## 🎨 Features

- Clean, modern UI with gradient design
- Real-time character counter
- Detailed analysis breakdown
- Confidence score visualization
- Mobile-responsive design
- No external API required (local analysis)
- Fast processing

## 📱 API Endpoint

```
POST /api/detect/
Content-Type: application/json

Request:
{
    "text": "Your text to analyze..."
}

Response:
{
    "success": true,
    "result": "human|ai|mixed",
    "confidence": 0.85,
    "word_count": 150,
    "explanation": "Analysis details...",
    "message": "Human-readable result message"
}
```

## 🔧 Customization

### Modify Detection Sensitivity

Edit the threshold values in `views.py` (analyze_text function):
- Change confidence thresholds for more/less strict detection
- Adjust feature weights for different analysis priorities

### Change UI Colors

Edit the CSS variables in `index.html`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 📊 Database Models

### TextAnalysis Model
- `text`: The analyzed text
- `result`: Detection result (human/ai/mixed)
- `confidence`: Confidence score (0-1)
- `word_count`: Number of words
- `created_at`: Timestamp
- `updated_at`: Updated timestamp

## 🌐 Production Deployment

For production use:

1. Set `DEBUG = False` in settings.py
2. Change `SECRET_KEY` to a strong random value
3. Update `ALLOWED_HOSTS` with your domain
4. Use PostgreSQL instead of SQLite
5. Configure static files properly
6. Use a production WSGI server (Gunicorn, uWSGI)

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Errors
```bash
python manage.py flush  # Clear all data
python manage.py migrate
```

### CSRF Errors
The application handles CSRF automatically. Make sure cookies are enabled.

## 📚 Technology Stack

- **Backend**: Django 4.2, Python 3.8+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Analysis**: Scikit-learn, Custom NLP features

## 📄 License

Open source - feel free to modify and distribute

## ❓ FAQ

**Q: Is my data stored?**
A: By default, analysis results are saved to the database but can be disabled.

**Q: How accurate is the detector?**
A: The detector is ~75-85% accurate for obvious cases. Mixed/borderline cases may need human review.

**Q: Can I use this offline?**
A: Yes! It works completely offline with no external API calls.

**Q: How long is the text limit?**
A: No hard limit, but best results are with 50+ words.

---

**Need Help?** Check the included code comments and Django documentation at https://docs.djangoproject.com/
