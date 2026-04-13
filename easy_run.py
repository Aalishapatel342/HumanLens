"""
AI Content Detector - Simplified Django Application
This is a single-file version for easy setup and running
"""

import os
import sys
import json
import re
from pathlib import Path
from collections import Counter
from django.conf import settings
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

# Configure Django settings
BASE_DIR = Path(__file__).resolve().parent

DJANGO_CONFIG = {
    'DEBUG': True,
    'SECRET_KEY': 'django-insecure-ai-detector-secret-key',
    'ALLOWED_HOSTS': ['*'],
    'INSTALLED_APPS': [
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
    'MIDDLEWARE': [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    },
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        },
    ],
}

if not settings.configured:
    settings.configure(**DJANGO_CONFIG)

# Import Django stuff after configuration
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
import nltk
from nltk import pos_tag, word_tokenize
from collections import Counter
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

from django.apps import AppConfig, apps
from django.core.asgi import get_asgi_application

# Register a minimal app





# ======================
# ANALYSIS LOGIC
# ======================

def analyze_text(text):
    """
    Analyze text to determine if it's human-written or AI-generated
    Returns: (result, confidence, explanation)
    """
    if not text or len(text.strip()) < 10:
        return 'mixed', 0.5, 'Text too short for reliable analysis'
    
    # Basic statistics
    words = text.lower().split()
    word_count = len(words)
    sentences = len(re.split(r'[.!?]+', text)) - 1
    
    # Extract features
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
    contractions = len(re.findall(r"\b(don't|can't|won't|it's|that's|i'm|we're)\b", text, re.IGNORECASE))
    questions = text.count('?')
    exclamations = text.count('!')
    personal_pronouns = len(re.findall(r'\b(i|we|you|me|us|our|my|your|he|she|they)\b', text, re.IGNORECASE))
    
    # AI writing markers
    ai_markers = len(re.findall(
        r'\b(furthermore|moreover|additionally|consequently|thus|therefore|regarding|'
        r'in conclusion|in summary|presented|provided|demonstrate|analyze|elucidate)\b',
        text, re.IGNORECASE
    ))
    
    # Word frequency analysis
    word_freq = Counter(words)
    most_common = word_freq.most_common(1)
    repetition_score = most_common[0][1] / len(words) if most_common else 0
    
    # Vocabulary diversity
    unique_words = len(set(words))
    vocabulary_diversity = unique_words / len(words) if words else 0
    
    # Calculate human score
    human_score = 50  # Start at 50
    
    # Contractions (strongly human)
    human_score += min(contractions / 10, 1.0) * 15
    
    # Natural conversation
    conversational = (questions + exclamations)
    human_score += min(conversational / 5, 1.0) * 15
    
    # Personal pronouns (human)
    human_score += min(personal_pronouns / (word_count * 0.05), 1.0) * 10
    
    # Formal markers (AI tendency)
    if ai_markers > 0:
        human_score -= min(ai_markers / 3, 1.0) * 20
    
    # Repetition (AI tendency)
    if repetition_score > 0.15:
        human_score -= 15
    
    # Vocabulary diversity (human tendency)
    if vocabulary_diversity > 0.75:
        human_score += 10
    
    # Normalize to 0-1
    confidence = max(0, min(100, human_score)) / 100
    
    # Determine result
    if confidence > 0.65:
        result = 'human'
    elif confidence < 0.35:
        result = 'ai'
    else:
        result = 'mixed'
    
    explanation = f"Analyzed {word_count} words across {sentences} sentences with ~{avg_word_length:.1f}avg word length"
    
    return result, confidence, explanation


# ======================
# VIEWS / API ENDPOINTS
# ======================

@csrf_exempt
@require_http_methods(["POST"])
def detect_api(request):
    """API endpoint for text detection"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({'error': 'No text provided', 'success': False}, status=400)
        
        result, confidence, explanation = analyze_text(text)
        word_count = len(text.split())
        
        response = {
            'success': True,
            'result': result,
            'confidence': round(confidence, 3),
            'word_count': word_count,
            'explanation': explanation,
            'message': {
                'human': '✓ Appears to be human-written',
                'ai': '⚠ Appears to be AI-generated',
                'mixed': '? Mixed or unclear characteristics'
            }[result]
        }
        return JsonResponse(response)
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def home(request):
    """Serve the main HTML page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Content Detector</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; display: flex; justify-content: center; align-items: center; }
            .container { background: white; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); max-width: 800px; width: 100%; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; }
            .header h1 { font-size: 28px; margin-bottom: 10px; }
            .header p { font-size: 14px; opacity: 0.9; }
            .content { padding: 40px 30px; }
            label { display: block; margin-bottom: 10px; font-weight: 500; }
            textarea { width: 100%; padding: 15px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 14px; min-height: 200px; resize: vertical; }
            textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
            button { padding: 12px 24px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.3s; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102,126,234,0.3); }
            button:disabled { opacity: 0.7; cursor: not-allowed; }
            .button-group { display: flex; gap: 10px; margin: 20px 0; }
            .btn-clear { background: #f0f0f0; color: #333; }
            .loading { display: none; text-align: center; padding: 20px; }
            .spinner { border: 4px solid #f0f0f0; border-top: 4px solid #667eea; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .result { display: none; border-radius: 8px; padding: 25px; margin-top: 25px; animation: slideIn 0.3s ease; }
            @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            .result.human { background: #e8f5e9; border-left: 5px solid #4caf50; }
            .result.ai { background: #fff3e0; border-left: 5px solid #ff9800; }
            .result.mixed { background: #f3e5f5; border-left: 5px solid #9c27b0; }
            .result-title { font-size: 18px; font-weight: 600; margin-bottom: 15px; }
            .progress-bar { width: 100%; height: 8px; background: #ddd; border-radius: 4px; overflow: hidden; margin: 10px 0; }
            .progress-fill { height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 4px; }
            .stat-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; font-size: 13px; }
            .error { background: #ffebee; color: #c62828; border-left: 5px solid #c62828; padding: 15px; border-radius: 8px; margin-top: 20px; display: none; }
            .char-count { text-align: right; color: #999; font-size: 12px; margin-top: 8px; }
            .info-box { background: #e3f2fd; border-left: 5px solid #2196f3; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 13px; color: #1565c0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 AI Content Detector</h1>
                <p>Identify human-written vs AI-generated text</p>
            </div>
            <div class="content">
                <div class="info-box">💡 Paste your text and let our AI analyze whether it was written by a human or generated by an AI.</div>
                <form id="form">
                    <label>Paste your text:</label>
                    <textarea id="text" placeholder="Enter text to analyze..." required></textarea>
                    <div class="char-count"><span id="chars">0</span> characters</div>
                    <div class="button-group">
                        <button type="submit">Analyze Text</button>
                        <button type="button" class="btn-clear" onclick="clear_()">Clear</button>
                    </div>
                </form>
                <div class="loading" id="loading"><div class="spinner"></div><p>Analyzing...</p></div>
                <div class="error" id="error"></div>
                <div class="result" id="result">
                    <div class="result-title" id="title"></div>
                    <div class="progress-bar"><div class="progress-fill" id="bar"></div></div>
                    <div style="text-align: center; font-weight: 600; margin: 10px 0;" id="conf"></div>
                    <div class="stat-row">
                        <div><strong>Result:</strong> <span id="res"></span></div>
                        <div><strong>Words:</strong> <span id="wc"></span></div>
                    </div>
                    <div style="margin-top: 10px; font-size: 12px; color: #666;" id="exp"></div>
                </div>
            </div>
        </div>
        <script>
            document.getElementById('text').addEventListener('input', function() {
                document.getElementById('chars').textContent = this.value.length;
            });
            document.getElementById('form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const text = document.getElementById('text').value.trim();
                if (!text) return;
                document.getElementById('loading').style.display = 'block';
                document.getElementById('result').style.display = 'none';
                document.getElementById('error').style.display = 'none';
                try {
                    const res = await fetch('/api/detect/', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({text})
                    });
                    const data = await res.json();
                    if (data.success) {
                        const r = data.result;
                        document.getElementById('result').className = 'result ' + r;
                        document.getElementById('title').textContent = data.message;
                        document.getElementById('bar').style.width = (data.confidence * 100) + '%';
                        document.getElementById('conf').textContent = (data.confidence * 100).toFixed(1) + '%';
                        document.getElementById('res').textContent = r.toUpperCase();
                        document.getElementById('wc').textContent = data.word_count;
                        document.getElementById('exp').textContent = data.explanation;
                        document.getElementById('result').style.display = 'block';
                    } else {
                        document.getElementById('error').textContent = data.error;
                        document.getElementById('error').style.display = 'block';
                    }
                } catch(e) {
                    document.getElementById('error').textContent = 'Error: ' + e.message;
                    document.getElementById('error').style.display = 'block';
                }
                document.getElementById('loading').style.display = 'none';
            });
            function clear_() {
                document.getElementById('text').value = '';
                document.getElementById('chars').textContent = '0';
                document.getElementById('result').style.display = 'none';
                document.getElementById('error').style.display = 'none';
            }
        </script>
    </body>
    </html>
    """
    from django.http import HttpResponse
    return HttpResponse(html_content)


# ======================
# URL ROUTING
# ======================

urlpatterns = [
    path('', home, name='home'),
    path('api/detect/', detect_api, name='detect'),
]


# ======================
# WSGI APPLICATION
# ======================

class DjangoApplication:
    def __init__(self):
        from django.core.wsgi import get_wsgi_application
        self.app = get_wsgi_application()
    
    def __call__(self, environ, start_response):
        return self.app(environ, start_response)


# ======================
# MAIN ENTRY POINT
# ======================

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
    

    
    # Configure URL patterns
    settings.ROOT_URLCONF = sys.modules[__name__]
    
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
