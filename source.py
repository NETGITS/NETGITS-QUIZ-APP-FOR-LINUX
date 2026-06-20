#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    NETGITS QUIZ v1.0.0-beta                               ║
║         Advanced Examination System with Full Accessibility              ║
║              Made by Adam Mahmoud - www.netgits.com                      ║
║        ⭐ GitHub: github.com/NETGITS | 📧 adam-mahmoud@netgits.com       ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import sys, os, json, sqlite3, datetime, hashlib, random, string, base64
import threading, time, socket, uuid, csv, io, shutil, tempfile, mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, unquote
from pathlib import Path
from typing import Optional, List, Dict, Any

from PyQt6.QtCore import (
    Qt, QUrl, QSize, QPoint, QTimer, QObject, pyqtSignal,
    QPropertyAnimation, QEasingCurve, QRect, QThread
)
from PyQt6.QtGui import (
    QIcon, QFont, QColor, QPalette, QAction, QKeySequence, QShortcut,
    QDesktopServices, QCursor, QPixmap, QPainter, QBrush, QPen,
    QLinearGradient, QRadialGradient, QFontDatabase, QFontMetrics
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTabWidget, QProgressBar,
    QFileDialog, QStatusBar, QListWidget, QListWidgetItem, QLabel,
    QFormLayout, QCheckBox, QMessageBox, QMenu, QFrame,
    QGridLayout, QTextEdit, QComboBox, QGroupBox, QSpinBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog,
    QScrollArea, QDialog, QSplitter, QStyleFactory,
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
    QSlider, QStyle, QDialogButtonBox, QStackedWidget, QToolButton
)

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

class Config:
    """Application configuration and constants"""
    
    APP_NAME = "NETGITS Quiz"
    APP_VERSION = "1.0.0-beta"
    APP_CODENAME = "Examiner Pro"
    APP_TAGLINE = "Advanced Local Network Examination System"
    APP_TAGLINE_AR = "نظام الامتحانات المتقدم عبر الشبكة المحلية"
    
    DEV_NAME = "Adam Mahmoud"
    EMAIL = "adam-mahmoud@netgits.com"
    WEBSITE = "https://www.netgits.com"
    GITHUB = "https://github.com/NETGITS"
    FACEBOOK = "https://www.facebook.com/profile.php?id=61591186311333"
    WHATSAPP = "https://wa.me/+201204403567"
    PHONE = "+201204403567"
    
    QUESTION_TYPES = [
        "Multiple Choice (A/B/C/D) - اختيار من متعدد",
        "True / False - صح وخطأ",
        "Short Answer - إجابة قصيرة",
        "Essay - مقالي",
        "Fill in the Blank - املأ الفراغ"
    ]
    
    LANGUAGES = {"en": "English", "ar": "العربية"}
    
    ACCESSIBILITY = {
        "font_sizes": [12, 14, 16, 18, 20, 24],
        "font_size_labels": ["Normal", "Medium", "Large", "XL", "XXL", "Huge"],
        "contrast_modes": ["Normal", "High Contrast", "Dark", "Light"],
        "extra_time_options": [0, 25, 50, 100, 150, 200],
        "zoom_levels": [100, 125, 150, 175, 200, 250, 300],
    }

# ═══════════════════════════════════════════════════════════════════════════
# DATABASE ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class Database:
    """Advanced database management system"""
    
    def __init__(self):
        self.base_path = os.path.join(os.path.expanduser("~"), ".netgits_quiz")
        os.makedirs(self.base_path, exist_ok=True)
        
        self.media_path = os.path.join(self.base_path, "media")
        os.makedirs(self.media_path, exist_ok=True)
        
        self.db_path = os.path.join(self.base_path, "quiz.db")
        self.connection = None
        self.lock = threading.Lock()
        self._initialize()
    
    def _initialize(self):
        """Initialize database connection and tables"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA journal_mode=WAL")
            self.connection.execute("PRAGMA foreign_keys=ON")
            self.connection.execute("PRAGMA cache_size=-8000")
            self._create_tables()
            self._insert_defaults()
        except Exception as error:
            print(f"Database initialization error: {error}")
    
    def _create_tables(self):
        """Create all database tables"""
        self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS exams(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                password TEXT DEFAULT '',
                duration_minutes INTEGER DEFAULT 30,
                shuffle_questions INTEGER DEFAULT 1,
                shuffle_choices INTEGER DEFAULT 1,
                show_results INTEGER DEFAULT 0,
                max_attempts INTEGER DEFAULT 1,
                passing_score INTEGER DEFAULT 50,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 0,
                accessibility_enabled INTEGER DEFAULT 1,
                extra_time_percent INTEGER DEFAULT 0,
                screen_reader_enabled INTEGER DEFAULT 1,
                large_font_enabled INTEGER DEFAULT 1,
                high_contrast_enabled INTEGER DEFAULT 1
            );
            
            CREATE TABLE IF NOT EXISTS questions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id INTEGER NOT NULL,
                question_type TEXT NOT NULL,
                question_text TEXT NOT NULL,
                option_a TEXT DEFAULT '',
                option_b TEXT DEFAULT '',
                option_c TEXT DEFAULT '',
                option_d TEXT DEFAULT '',
                correct_answer TEXT NOT NULL DEFAULT '',
                points INTEGER DEFAULT 1,
                order_num INTEGER DEFAULT 0,
                image_path TEXT DEFAULT '',
                audio_path TEXT DEFAULT '',
                alt_text TEXT DEFAULT '',
                audio_description TEXT DEFAULT '',
                FOREIGN KEY(exam_id) REFERENCES exams(id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                student_id TEXT DEFAULT '',
                email TEXT DEFAULT '',
                phone TEXT DEFAULT '',
                ip_address TEXT DEFAULT '',
                exam_id INTEGER NOT NULL,
                assigned_token TEXT DEFAULT '',
                accessibility_profile TEXT DEFAULT '{}',
                score REAL DEFAULT 0,
                total_points REAL DEFAULT 0,
                percentage REAL DEFAULT 0,
                status TEXT DEFAULT 'pending',
                needs_review INTEGER DEFAULT 0,
                start_time TEXT,
                end_time TEXT,
                answers TEXT DEFAULT '{}',
                extra_time_used INTEGER DEFAULT 0,
                FOREIGN KEY(exam_id) REFERENCES exams(id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS assigned_exams(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id INTEGER NOT NULL,
                student_name TEXT NOT NULL,
                assigned_token TEXT UNIQUE NOT NULL,
                is_used INTEGER DEFAULT 0,
                accessibility_profile TEXT DEFAULT '{}',
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(exam_id) REFERENCES exams(id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS settings(
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_date TEXT DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS activity_log(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                details TEXT DEFAULT '',
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.connection.commit()
    
    def _insert_defaults(self):
        """Insert default settings"""
        defaults = [
            ('theme', 'dark'),
            ('language', 'en'),
            ('server_port', '8080'),
            ('auto_start', '0'),
            ('notifications', '1'),
        ]
        for key, value in defaults:
            self.execute(
                "INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)",
                (key, value)
            )
        self.connection.commit()
    
    def execute(self, query: str, params: tuple = None):
        """Execute SQL query with thread safety"""
        with self.lock:
            try:
                if params:
                    return self.connection.execute(query, params)
                return self.connection.execute(query)
            except Exception as error:
                print(f"SQL Error: {error}")
                return None
    
    def fetch_all(self, query: str, params: tuple = None):
        """Fetch all rows"""
        with self.lock:
            try:
                if params:
                    return self.connection.execute(query, params).fetchall()
                return self.connection.execute(query).fetchall()
            except Exception as error:
                print(f"Fetch Error: {error}")
                return []
    
    def fetch_one(self, query: str, params: tuple = None):
        """Fetch single row"""
        with self.lock:
            try:
                if params:
                    return self.connection.execute(query, params).fetchone()
                return self.connection.execute(query).fetchone()
            except Exception as error:
                print(f"Fetch Error: {error}")
                return None
    
    def commit(self):
        """Commit changes with thread safety"""
        with self.lock:
            try:
                self.connection.commit()
            except Exception as error:
                print(f"Commit Error: {error}")
    
    def log_activity(self, action: str, details: str = ""):
        """Log activity"""
        self.execute(
            "INSERT INTO activity_log(action, details) VALUES(?, ?)",
            (action, details)
        )
        self.commit()
    
    def close(self):
        """Close database connection"""
        with self.lock:
            try:
                if self.connection:
                    self.connection.commit()
                    self.connection.close()
            except Exception as error:
                print(f"Close Error: {error}")

# ═══════════════════════════════════════════════════════════════════════════
# WEB SERVER
# ═══════════════════════════════════════════════════════════════════════════

class QuizServer(threading.Thread):
    """HTTP Server for student access"""
    
    def __init__(self, database: Database, port: int = 8080):
        super().__init__(daemon=True)
        self.database = database
        self.port = port
        self.http_server = None
        self.is_running = False
    
    def get_local_ip(self) -> str:
        """Get local network IP address"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip_address = sock.getsockname()[0]
            sock.close()
            return ip_address
        except Exception:
            return "127.0.0.1"
    
    def run(self):
        """Start server in thread"""
        self.is_running = True
        handler = lambda *args: StudentHandler(self.database, *args)
        self.http_server = HTTPServer(("0.0.0.0", self.port), handler)
        self.http_server.serve_forever()
    
    def stop(self):
        """Stop server"""
        self.is_running = False
        if self.http_server:
            try:
                self.http_server.shutdown()
            except Exception:
                pass

class StudentHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests from students"""
    
    def __init__(self, database: Database, *args):
        self.database = database
        super().__init__(*args)
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass
    
    def send_response_data(self, content, content_type="text/html", status_code=200):
        """Send HTTP response"""
        try:
            self.send_response(status_code)
            self.send_header("Content-type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            if isinstance(content, str):
                content = content.encode('utf-8')
            self.wfile.write(content)
        except Exception:
            pass
    
    def get_post_data(self) -> dict:
        """Parse POST data"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            return parse_qs(post_data)
        except Exception:
            return {}
    
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        routes = {
            "/": self.serve_login_page,
            "/login": self.serve_login_page,
            "/exam": self.serve_exam_page,
            "/style.css": self.serve_stylesheet,
            "/a11y.css": self.serve_accessibility_css,
            "/a11y.js": self.serve_accessibility_js,
        }
        
        handler = routes.get(path)
        if handler:
            handler()
        elif path.startswith("/media/"):
            self.serve_media(path)
        else:
            self.send_response_data("Not Found", status_code=404)
    
    def do_POST(self):
        """Handle POST requests"""
        path = urlparse(self.path).path
        
        if path == "/login":
            self.handle_login()
        elif path == "/submit":
            self.handle_submit()
        else:
            self.send_response_data("Not Found", status_code=404)
    
    def serve_media(self, path: str):
        """Serve media files"""
        media_full_path = os.path.join(
            os.path.expanduser("~"), ".netgits_quiz", path.lstrip("/")
        )
        if os.path.exists(media_full_path):
            mime_type, _ = mimetypes.guess_type(media_full_path)
            with open(media_full_path, 'rb') as file:
                self.send_response_data(
                    file.read(),
                    mime_type or "application/octet-stream"
                )
        else:
            self.send_response_data("Not Found", status_code=404)
    
    def serve_login_page(self):
        """Serve student login page"""
        exams = self.database.fetch_all(
            "SELECT id, title, description FROM exams WHERE is_active=1"
        )
        
        options_html = ""
        for exam in exams:
            options_html += f'<option value="{exam["id"]}">{exam["title"]}</option>'
        
        if not options_html:
            options_html = '<option value="">No active exams available</option>'
        
        html_content = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NETGITS Quiz - Student Login</title>
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="/a11y.css">
</head>
<body>
    <a href="#main-content" class="skip-link" role="navigation">Skip to main content</a>
    
    <div class="a11y-toolbar" role="toolbar" aria-label="Accessibility tools">
        <button onclick="increaseFontSize()" aria-label="Increase font size" title="Increase font">A+</button>
        <button onclick="decreaseFontSize()" aria-label="Decrease font size" title="Decrease font">A-</button>
        <button onclick="toggleHighContrast()" aria-label="Toggle high contrast" title="Contrast">◐</button>
        <button onclick="toggleDyslexiaFont()" aria-label="Toggle dyslexia-friendly font" title="Dyslexia font">𝐃</button>
        <button onclick="readPageAloud()" aria-label="Read page aloud" title="Screen reader">🔊</button>
    </div>
    
    <main id="main-content" class="container">
        <div class="card login-card">
            <div class="brand-logo" role="heading" aria-level="1">NETGITS</div>
            <div class="brand-subtitle">Online Examination System</div>
            
            <form method="POST" action="/login" id="loginForm" novalidate>
                <div class="form-group">
                    <label for="student_name">📝 Full Name *</label>
                    <input type="text" id="student_name" name="name" required 
                           placeholder="Enter your full name" autocomplete="name"
                           aria-required="true">
                </div>
                
                <div class="form-group">
                    <label for="student_id">🎓 Student ID</label>
                    <input type="text" id="student_id" name="student_id" 
                           placeholder="Enter your student ID (optional)" autocomplete="off">
                </div>
                
                <div class="form-group">
                    <label for="access_token">🔑 Access Token</label>
                    <input type="text" id="access_token" name="token" 
                           placeholder="Enter token if assigned" autocomplete="off">
                </div>
                
                <div class="form-group">
                    <label for="exam_select">📋 Select Exam *</label>
                    <select id="exam_select" name="exam_id" required aria-required="true">
                        <option value="">-- Choose Your Exam --</option>
                        {options_html}
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="exam_password">🔑 Exam Password</label>
                    <input type="password" id="exam_password" name="password" 
                           placeholder="Enter password if required" autocomplete="off">
                </div>
                
                <button type="submit" class="submit-button" aria-label="Start examination">
                    🚀 Start Exam
                </button>
            </form>
            
            <div class="brand-footer">
                Powered by <strong>NETGITS Quiz</strong><br>
                <small>www.netgits.com</small>
            </div>
        </div>
    </main>
    
    <script src="/a11y.js"></script>
    <script>
        // Load saved accessibility settings
        (function() {{
            try {{
                var settings = JSON.parse(localStorage.getItem('netgits_a11y_settings') || '{{}}');
                if (settings.fontSize) document.documentElement.style.fontSize = settings.fontSize + 'px';
                if (settings.highContrast) document.body.classList.add('high-contrast-mode');
                if (settings.dyslexiaFont) document.body.classList.add('dyslexia-friendly-font');
            }} catch(e) {{}}
        }})();
    </script>
</body>
</html>"""
        self.send_response_data(html_content)
    
    def handle_login(self):
        """Handle student login form submission"""
        data = self.get_post_data()
        
        student_name = data.get('name', [''])[0].strip()
        student_id = data.get('student_id', [''])[0].strip()
        access_token = data.get('token', [''])[0].strip()
        exam_id = data.get('exam_id', [''])[0]
        exam_password = data.get('password', [''])[0].strip()
        
        # Validation
        if not student_name:
            self.send_response_data(
                self._error_page("Please enter your full name."), status_code=400
            )
            return
        
        if not exam_id:
            self.send_response_data(
                self._error_page("Please select an exam."), status_code=400
            )
            return
        
        # Verify exam exists and is active
        exam = self.database.fetch_one(
            "SELECT * FROM exams WHERE id = ? AND is_active = 1",
            (exam_id,)
        )
        
        if not exam:
            self.send_response_data(
                self._error_page("Exam not found or is no longer active."), status_code=400
            )
            return
        
        # Check exam password if set
        if exam["password"] and exam["password"] != exam_password:
            self.send_response_data(
                self._error_page("Incorrect exam password!"), status_code=400
            )
            return
        
        # Handle assigned token
        accessibility_profile = {}
        if access_token:
            assigned = self.database.fetch_one(
                "SELECT * FROM assigned_exams WHERE exam_id = ? AND assigned_token = ? AND is_used = 0",
                (exam_id, access_token)
            )
            
            if not assigned:
                self.send_response_data(
                    self._error_page("Invalid or already used access token!"), status_code=400
                )
                return
            
            # Mark token as used
            self.database.execute(
                "UPDATE assigned_exams SET is_used = 1 WHERE assigned_token = ?",
                (access_token,)
            )
            self.database.commit()
            
            student_name = assigned["student_name"]
            accessibility_profile = json.loads(assigned["accessibility_profile"] or '{}')
        
        # Register student
        client_ip = self.client_address[0]
        current_time = datetime.datetime.now().isoformat()
        
        self.database.execute("""
            INSERT INTO students (name, student_id, ip_address, exam_id, 
                                 assigned_token, accessibility_profile, start_time, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'started')
        """, (student_name, student_id, client_ip, exam_id, 
              access_token, json.dumps(accessibility_profile), current_time))
        self.database.commit()
        
        student_db_id = self.database.fetch_one("SELECT last_insert_rowid()")[0]
        
        # Redirect to exam page
        self.send_response(302)
        self.send_header("Location", f"/exam?sid={student_db_id}&eid={exam_id}")
        self.end_headers()
    
    def serve_exam_page(self):
        """Serve exam page with questions"""
        query_params = parse_qs(urlparse(self.path).query)
        student_id = query_params.get('sid', [''])[0]
        exam_id = query_params.get('eid', [''])[0]
        
        if not student_id or not exam_id:
            self.send_response_data(self._error_page("Invalid access."), status_code=400)
            return
        
        student = self.database.fetch_one("SELECT * FROM students WHERE id = ?", (student_id,))
        exam = self.database.fetch_one("SELECT * FROM exams WHERE id = ?", (exam_id,))
        
        if not student or not exam:
            self.send_response_data(self._error_page("Session expired."), status_code=400)
            return
        
        if student["status"] == "completed":
            self.send_response_data(
                self._error_page("You have already submitted this exam."), status_code=400
            )
            return
        
        # Get accessibility settings
        accessibility = json.loads(student["accessibility_profile"] or '{}')
        extra_time_percent = 0
        if exam["accessibility_enabled"]:
            extra_time_percent = exam["extra_time_percent"]
        if accessibility.get("extra_time"):
            extra_time_percent = max(extra_time_percent, accessibility["extra_time"])
        
        # Calculate duration with extra time
        duration_minutes = int(exam["duration_minutes"] * (1 + extra_time_percent / 100))
        duration_seconds = duration_minutes * 60
        
        # Get questions
        questions = list(self.database.fetch_all(
            "SELECT * FROM questions WHERE exam_id = ? ORDER BY order_num",
            (exam_id,)
        ))
        
        if exam["shuffle_questions"]:
            random.shuffle(questions)
        
        # Build questions HTML
        questions_html = ""
        for index, question in enumerate(questions):
            question_number = index + 1
            questions_html += self._build_question_html(question, question_number, exam)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NETGITS Quiz - Examination</title>
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="/a11y.css">
</head>
<body>
    <a href="#exam-form" class="skip-link">Skip to exam questions</a>
    
    <div class="a11y-toolbar" role="toolbar" aria-label="Accessibility tools">
        <button onclick="increaseFontSize()" title="Increase font">A+</button>
        <button onclick="decreaseFontSize()" title="Decrease font">A-</button>
        <button onclick="toggleHighContrast()" title="Contrast">◐</button>
        <button onclick="readCurrentQuestion()" title="Read aloud">🔊</button>
    </div>
    
    <main id="main-content" class="container">
        <div class="card exam-card" role="main" aria-label="Examination paper">
            <div class="brand-logo">NETGITS</div>
            <h2>📝 {exam["title"]}</h2>
            <p class="exam-description">{exam["description"] or ''}</p>
            
            <div class="timer-display" id="exam-timer" role="timer" aria-live="polite">
                ⏱️ <span id="timer-text">{duration_minutes}:00</span>
            </div>
            
            <div class="student-info">
                Student: <strong>{student["name"]}</strong> | 
                Extra Time: {extra_time_percent}%
            </div>
            
            <form id="exam-form" method="POST" action="/submit" 
                  onsubmit="return confirm('Are you sure you want to submit your exam? This cannot be undone.')">
                <input type="hidden" name="student_id" value="{student_id}">
                <input type="hidden" name="exam_id" value="{exam_id}">
                
                {questions_html}
                
                <button type="submit" class="submit-button" aria-label="Submit examination">
                    📤 Submit Exam
                </button>
            </form>
        </div>
    </main>
    
    <script src="/a11y.js"></script>
    <script>
        // Timer functionality
        var timeLeft = {duration_seconds};
        var timerDisplay = document.getElementById('timer-text');
        var timerBox = document.getElementById('exam-timer');
        
        setInterval(function() {{
            timeLeft--;
            var minutes = Math.floor(timeLeft / 60);
            var seconds = timeLeft % 60;
            timerDisplay.textContent = minutes + ':' + String(seconds).padStart(2, '0');
            
            // Warning when 5 minutes remaining
            if (timeLeft <= 300) {{
                timerBox.style.background = '#7f1d1d';
                timerBox.style.color = '#fca5a5';
                timerBox.style.borderColor = '#dc2626';
            }}
            
            // Auto-submit when time is up
            if (timeLeft <= 0) {{
                alert('⏰ Time is up! Your exam will be submitted automatically.');
                document.getElementById('exam-form').submit();
            }}
        }}, 1000);
        
        // Anti-cheating measures
        document.addEventListener('visibilitychange', function() {{
            if (document.hidden) {{
                alert('⚠️ Warning: Switching tabs is not allowed during the exam!');
            }}
        }});
        
        document.addEventListener('contextmenu', function(e) {{ e.preventDefault(); }});
        document.addEventListener('copy', function(e) {{ e.preventDefault(); }});
        document.addEventListener('paste', function(e) {{ e.preventDefault(); }});
        document.addEventListener('cut', function(e) {{ e.preventDefault(); }});
        
        // Load saved settings
        (function() {{
            try {{
                var settings = JSON.parse(localStorage.getItem('netgits_a11y_settings') || '{{}}');
                if (settings.fontSize) document.documentElement.style.fontSize = settings.fontSize + 'px';
                if (settings.highContrast) document.body.classList.add('high-contrast-mode');
                if (settings.dyslexiaFont) document.body.classList.add('dyslexia-friendly-font');
            }} catch(e) {{}}
        }})();
    </script>
</body>
</html>"""
        self.send_response_data(html_content)
    
    def _build_question_html(self, question, question_number, exam) -> str:
        """Build HTML for a single question"""
        html = f'<div class="question-block" role="region" aria-label="Question {question_number}">'
        html += f'<div class="question-header">'
        html += f'<span class="question-number">Question {question_number}</span>'
        html += f'<span class="question-type-badge">({question["question_type"]})</span>'
        html += f'<span class="question-points">{question["points"]} pts</span>'
        html += f'</div>'
        
        # Question text
        html += f'<div class="question-text">{question["question_text"]}</div>'
        
        # Alt text for accessibility
        if question["alt_text"]:
            html += f'<div class="sr-only">{question["alt_text"]}</div>'
        
        # Image attachment
        if question["image_path"]:
            image_url = f"/media/{os.path.relpath(question['image_path'], os.path.join(os.path.expanduser('~'), '.netgits_quiz'))}"
            alt_text = question["alt_text"] or "Question image"
            html += f'<div class="media-container">'
            html += f'<img src="{image_url}" alt="{alt_text}" class="question-image">'
            html += f'</div>'
        
        # Audio attachment
        if question["audio_path"]:
            audio_url = f"/media/{os.path.relpath(question['audio_path'], os.path.join(os.path.expanduser('~'), '.netgits_quiz'))}"
            html += f'<div class="media-container">'
            html += f'<audio controls class="question-audio" aria-label="Audio question">'
            html += f'<source src="{audio_url}" type="audio/mpeg"></audio>'
            html += f'</div>'
            if question["audio_description"]:
                html += f'<div class="sr-only">{question["audio_description"]}</div>'
        
        # Answer options based on question type
        question_type = question["question_type"]
        
        if question_type.startswith("Multiple Choice"):
            options = []
            for letter, key in [('A', 'option_a'), ('B', 'option_b'), 
                               ('C', 'option_c'), ('D', 'option_d')]:
                if question[key]:
                    options.append((letter, question[key]))
            
            if exam["shuffle_choices"]:
                random.shuffle(options)
            
            for letter, text in options:
                html += f'''<label class="option-label" tabindex="0">
                    <input type="radio" name="q_{question["id"]}" value="{letter}" required>
                    <span class="option-text"><strong>{letter})</strong> {text}</span>
                </label>'''
        
        elif question_type.startswith("True / False"):
            for value in ['True', 'False']:
                html += f'''<label class="option-label" tabindex="0">
                    <input type="radio" name="q_{question["id"]}" value="{value}" required>
                    <span class="option-text">{value}</span>
                </label>'''
        
        elif question_type.startswith("Short Answer") or question_type.startswith("Fill in the Blank"):
            html += f'<input type="text" name="q_{question["id"]}" class="text-input" '
            html += f'placeholder="Type your answer here..." required '
            html += f'aria-label="Answer for question {question_number}">'
        
        elif question_type.startswith("Essay"):
            html += f'<textarea name="q_{question["id"]}" class="text-input essay-input" '
            html += f'rows="5" placeholder="Write your detailed answer here..." required '
            html += f'aria-label="Essay answer for question {question_number}"></textarea>'
        
        html += '</div>'
        return html
    
    def handle_submit(self):
        """Handle exam submission"""
        data = self.get_post_data()
        
        student_id = data.get('student_id', [''])[0]
        exam_id = data.get('exam_id', [''])[0]
        
        if not student_id or not exam_id:
            self.send_response_data(self._error_page("Invalid submission."), status_code=400)
            return
        
        # Verify student hasn't already submitted
        student = self.database.fetch_one(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        )
        
        if not student or student["status"] == "completed":
            self.send_response_data(
                self._error_page("Exam already submitted or session expired."), status_code=400
            )
            return
        
        # Get all questions for grading
        questions = self.database.fetch_all(
            "SELECT * FROM questions WHERE exam_id = ?", (exam_id,)
        )
        
        total_points = 0
        earned_points = 0
        answers_dict = {}
        needs_review = False
        
        for question in questions:
            question_id = question["id"]
            question_type = question["question_type"]
            correct_answer = question["correct_answer"].strip().lower() if question["correct_answer"] else ""
            points = question["points"]
            total_points += points
            
            answer_key = f"q_{question_id}"
            student_answer = data.get(answer_key, [''])[0].strip()
            
            # Store answer
            answers_dict[str(question_id)] = {
                'question': question["question_text"][:150],
                'type': question_type,
                'answer': student_answer,
                'correct': correct_answer,
                'points': points,
                'max_points': points
            }
            
            # Auto-grade based on type
            if question_type.startswith("Multiple Choice") or question_type.startswith("True / False"):
                if student_answer.lower() == correct_answer:
                    earned_points += points
                    answers_dict[str(question_id)]['result'] = '✅ Correct'
                else:
                    answers_dict[str(question_id)]['result'] = '❌ Incorrect'
            
            elif question_type.startswith("Short Answer") or question_type.startswith("Fill in the Blank"):
                if student_answer and correct_answer in student_answer.lower():
                    earned_points += points
                    answers_dict[str(question_id)]['result'] = '✅ Correct'
                else:
                    # Partial credit - needs teacher review
                    earned_points += points * 0.3
                    answers_dict[str(question_id)]['result'] = '⚠️ Needs Review'
                    needs_review = True
            
            elif question_type.startswith("Essay"):
                # Essay always needs teacher review
                earned_points += points * 0.5
                answers_dict[str(question_id)]['result'] = '📝 Needs Review'
                needs_review = True
        
        # Calculate percentage
        percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        current_time = datetime.datetime.now().isoformat()
        
        # Update student record
        self.database.execute("""
            UPDATE students 
            SET score = ?, total_points = ?, percentage = ?, 
                status = 'completed', needs_review = ?, 
                end_time = ?, answers = ?
            WHERE id = ?
        """, (
            round(earned_points, 1), total_points, round(percentage, 1),
            int(needs_review), current_time, json.dumps(answers_dict, ensure_ascii=False),
            student_id
        ))
        self.database.commit()
        
        # Check if passed
        passing_score = exam["passing_score"] if 'exam' in dir() else 50
        exam = self.database.fetch_one("SELECT passing_score FROM exams WHERE id = ?", (exam_id,))
        if exam:
            passing_score = exam["passing_score"]
        
        passed = percentage >= passing_score
        
        # Show result page
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NETGITS Quiz - Result</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <main class="container">
        <div class="card result-card" role="alert" aria-live="assertive">
            <div class="brand-logo">NETGITS</div>
            <div class="result-icon">{'🎉' if passed else '😞'}</div>
            <h2>{'Congratulations! You Passed!' if passed else 'Better Luck Next Time!'}</h2>
            <div class="score-display" style="color: {'#3fb950' if passed else '#f85149'}">
                {round(percentage, 1)}%
            </div>
            <div class="score-details">
                <p><strong>Score:</strong> {earned_points:.1f} / {total_points} points</p>
                <p><strong>Status:</strong> {'✅ PASSED' if passed else '❌ FAILED'}</p>
                <p><strong>Passing Score:</strong> {passing_score}%</p>
            </div>
            <p class="result-note">Your answers have been submitted successfully. The teacher will review your results.</p>
            <div class="brand-footer">
                Powered by <strong>NETGITS Quiz</strong><br>
                <small>www.netgits.com</small>
            </div>
        </div>
    </main>
</body>
</html>"""
        self.send_response_data(html_content)
    
    def serve_stylesheet(self):
        """Serve main CSS stylesheet"""
        css = """
        /* ═══════════════════════════════════════════════ */
        /* NETGITS Quiz - Main Stylesheet                  */
        /* ═══════════════════════════════════════════════ */
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #484f58;
            --accent: #58a6ff;
            --accent-hover: #1f6feb;
            --border: #30363d;
            --success: #3fb950;
            --warning: #d29922;
            --error: #f85149;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
        }
        
        body {
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-primary) 100%);
            color: var(--text-primary);
            font-family: 'Segoe UI', 'Cairo', 'Noto Sans', system-ui, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            width: 100%;
            max-width: 520px;
        }
        
        .exam-card {
            max-width: 850px;
        }
        
        .card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: 40px 35px;
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
            animation: fadeInUp 0.5s ease-out;
        }
        
        .result-card {
            text-align: center;
            max-width: 480px;
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .brand-logo {
            font-size: 40px;
            font-weight: 900;
            text-align: center;
            background: linear-gradient(135deg, var(--accent), var(--success));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 6px;
            letter-spacing: 3px;
        }
        
        .brand-subtitle {
            text-align: center;
            color: var(--text-secondary);
            font-size: 13px;
            margin-bottom: 35px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .brand-footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 11px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }
        
        h2 {
            color: var(--accent);
            text-align: center;
            margin-bottom: 20px;
            font-size: 22px;
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 6px;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 13px;
        }
        
        input[type="text"],
        input[type="email"],
        input[type="password"],
        select,
        .text-input {
            width: 100%;
            padding: 13px 18px;
            background: var(--bg-primary);
            border: 2px solid var(--border);
            border-radius: var(--radius-md);
            color: var(--text-primary);
            font-size: 14px;
            font-family: inherit;
            transition: all 0.3s ease;
        }
        
        input:focus,
        select:focus,
        .text-input:focus {
            border-color: var(--accent);
            outline: none;
            box-shadow: 0 0 0 4px rgba(88, 166, 255, 0.15);
        }
        
        textarea.text-input {
            resize: vertical;
            min-height: 100px;
        }
        
        .submit-button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, var(--accent), var(--accent-hover));
            color: #ffffff;
            border: none;
            border-radius: var(--radius-md);
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            margin-top: 25px;
            transition: all 0.3s ease;
            letter-spacing: 0.5px;
        }
        
        .submit-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(88, 166, 255, 0.4);
        }
        
        .submit-button:active {
            transform: translateY(0);
        }
        
        .question-block {
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 22px;
            margin-bottom: 18px;
            transition: border-color 0.3s ease;
        }
        
        .question-block:hover {
            border-color: var(--accent);
        }
        
        .question-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }
        
        .question-number {
            color: var(--accent);
            font-weight: 700;
            font-size: 14px;
        }
        
        .question-type-badge {
            font-size: 10px;
            background: var(--bg-tertiary);
            padding: 4px 12px;
            border-radius: 20px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .question-points {
            color: var(--success);
            font-size: 12px;
            font-weight: 700;
        }
        
        .question-text {
            font-size: 15px;
            margin-bottom: 16px;
            line-height: 1.7;
            color: var(--text-primary);
        }
        
        .option-label {
            display: flex;
            align-items: center;
            padding: 14px 18px;
            margin-bottom: 8px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: all 0.2s ease;
            min-height: 48px;
        }
        
        .option-label:hover {
            background: var(--bg-tertiary);
            border-color: var(--accent);
            transform: translateX(5px);
        }
        
        .option-label input[type="radio"] {
            margin-right: 12px;
            accent-color: var(--accent);
            transform: scale(1.3);
            min-width: 18px;
            min-height: 18px;
        }
        
        .option-text {
            font-size: 14px;
            color: var(--text-primary);
        }
        
        .timer-display {
            text-align: center;
            font-size: 26px;
            font-weight: 700;
            padding: 14px;
            margin: 18px 0;
            background: var(--bg-primary);
            border: 2px solid var(--warning);
            border-radius: var(--radius-md);
            color: var(--warning);
            transition: all 0.3s ease;
        }
        
        .student-info {
            text-align: center;
            color: var(--text-secondary);
            font-size: 12px;
            padding: 10px;
            background: var(--bg-primary);
            border-radius: var(--radius-sm);
            margin-bottom: 20px;
        }
        
        .media-container {
            margin: 12px 0;
            text-align: center;
        }
        
        .question-image {
            max-width: 100%;
            max-height: 350px;
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
        }
        
        .question-audio {
            width: 100%;
            margin: 8px 0;
        }
        
        .result-icon {
            font-size: 80px;
            margin: 20px 0;
        }
        
        .score-display {
            font-size: 70px;
            font-weight: 900;
            margin: 15px 0;
        }
        
        .score-details {
            text-align: left;
            margin: 20px 0;
            padding: 18px;
            background: var(--bg-primary);
            border-radius: var(--radius-md);
            font-size: 14px;
        }
        
        .score-details p {
            padding: 6px 0;
            border-bottom: 1px solid var(--border);
        }
        
        .score-details p:last-child {
            border-bottom: none;
        }
        
        .result-note {
            color: var(--text-secondary);
            font-size: 13px;
            margin-top: 15px;
        }
        
        .exam-description {
            text-align: center;
            color: var(--text-secondary);
            font-size: 13px;
            margin-bottom: 10px;
        }
        
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            border: 0;
        }
        
        .skip-link {
            position: absolute;
            top: -100px;
            left: 10px;
            background: var(--accent);
            color: #ffffff;
            padding: 12px 20px;
            z-index: 9999;
            border-radius: var(--radius-sm);
            font-weight: 700;
            text-decoration: none;
        }
        
        .skip-link:focus {
            top: 10px;
        }
        
        @media (max-width: 768px) {
            .card {
                padding: 25px 20px;
            }
            .brand-logo {
                font-size: 30px;
            }
            .score-display {
                font-size: 50px;
            }
            .question-block {
                padding: 16px;
            }
        }
        
        @media (prefers-reduced-motion: reduce) {
            * {
                animation: none !important;
                transition: none !important;
            }
        }
        """
        self.send_response_data(css, "text/css")
    
    def serve_accessibility_css(self):
        """Serve accessibility CSS"""
        css = """
        /* ═══════════════════════════════════════════════ */
        /* NETGITS Quiz - Accessibility Styles             */
        /* ═══════════════════════════════════════════════ */
        
        .a11y-toolbar {
            position: fixed;
            top: 12px;
            right: 12px;
            z-index: 9998;
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }
        
        .a11y-toolbar button {
            padding: 8px 14px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            color: var(--accent);
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s ease;
            min-height: 40px;
            min-width: 40px;
        }
        
        .a11y-toolbar button:hover,
        .a11y-toolbar button:focus {
            background: var(--accent);
            color: #ffffff;
            outline: 3px solid var(--accent);
            outline-offset: 2px;
        }
        
        /* High Contrast Mode */
        body.high-contrast-mode {
            background: #000000 !important;
            color: #ffffff !important;
        }
        
        body.high-contrast-mode .card {
            background: #000000 !important;
            border-color: #ffffff !important;
            border-width: 3px !important;
        }
        
        body.high-contrast-mode input,
        body.high-contrast-mode select,
        body.high-contrast-mode textarea {
            background: #000000 !important;
            border-color: #ffffff !important;
            color: #ffffff !important;
            border-width: 2px !important;
        }
        
        body.high-contrast-mode .submit-button {
            background: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #ffffff !important;
        }
        
        body.high-contrast-mode .question-block {
            background: #000000 !important;
            border-color: #ffffff !important;
            border-width: 2px !important;
        }
        
        body.high-contrast-mode .option-label {
            background: #000000 !important;
            border-color: #ffffff !important;
        }
        
        body.high-contrast-mode .brand-logo {
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* Dyslexia-Friendly Font */
        body.dyslexia-friendly-font {
            font-family: 'OpenDyslexic', 'Comic Sans MS', 'Arial', sans-serif !important;
        }
        
        body.dyslexia-friendly-font * {
            letter-spacing: 0.5px !important;
            word-spacing: 2px !important;
            line-height: 1.9 !important;
        }
        
        /* Focus indicators */
        *:focus-visible {
            outline: 3px solid var(--accent) !important;
            outline-offset: 3px !important;
        }
        
        /* Larger touch targets for mobile */
        @media (max-width: 768px) {
            .option-label {
                min-height: 52px;
                padding: 16px;
            }
            .a11y-toolbar button {
                padding: 10px 16px;
                font-size: 14px;
            }
        }
        """
        self.send_response_data(css, "text/css")
    
    def serve_accessibility_js(self):
        """Serve accessibility JavaScript"""
        js = """
        // ═══════════════════════════════════════════════
        // NETGITS Quiz - Accessibility Functions
        // ═══════════════════════════════════════════════
        
        function increaseFontSize() {
            var currentSize = parseInt(getComputedStyle(document.documentElement).fontSize);
            var newSize = Math.min(currentSize + 2, 28);
            document.documentElement.style.fontSize = newSize + 'px';
            saveAccessibilitySetting('fontSize', newSize);
        }
        
        function decreaseFontSize() {
            var currentSize = parseInt(getComputedStyle(document.documentElement).fontSize);
            var newSize = Math.max(currentSize - 2, 10);
            document.documentElement.style.fontSize = newSize + 'px';
            saveAccessibilitySetting('fontSize', newSize);
        }
        
        function toggleHighContrast() {
            document.body.classList.toggle('high-contrast-mode');
            var isHighContrast = document.body.classList.contains('high-contrast-mode');
            saveAccessibilitySetting('highContrast', isHighContrast);
        }
        
        function toggleDyslexiaFont() {
            document.body.classList.toggle('dyslexia-friendly-font');
            var isDyslexiaFont = document.body.classList.contains('dyslexia-friendly-font');
            saveAccessibilitySetting('dyslexiaFont', isDyslexiaFont);
        }
        
        function readPageAloud() {
            if ('speechSynthesis' in window) {
                var textToRead = document.querySelector('.card')?.textContent || document.body.textContent;
                var utterance = new SpeechSynthesisUtterance(textToRead.substring(0, 1000));
                utterance.rate = 0.9;
                utterance.pitch = 1;
                utterance.volume = 1;
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(utterance);
            }
        }
        
        function readCurrentQuestion() {
            if ('speechSynthesis' in window) {
                var questionText = document.querySelector('.question-text');
                if (questionText) {
                    var utterance = new SpeechSynthesisUtterance(questionText.textContent);
                    utterance.rate = 0.85;
                    utterance.pitch = 1;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(utterance);
                }
            }
        }
        
        function saveAccessibilitySetting(key, value) {
            try {
                var settings = JSON.parse(localStorage.getItem('netgits_a11y_settings') || '{}');
                settings[key] = value;
                localStorage.setItem('netgits_a11y_settings', JSON.stringify(settings));
            } catch(e) {}
        }
        
        // Keyboard shortcut for accessibility menu
        document.addEventListener('keydown', function(e) {
            if (e.altKey && e.key === 'a') {
                e.preventDefault();
                var toolbar = document.querySelector('.a11y-toolbar');
                if (toolbar) {
                    toolbar.style.display = toolbar.style.display === 'none' ? 'flex' : 'none';
                }
            }
            
            if (e.key === 'Escape') {
                var toolbar = document.querySelector('.a11y-toolbar');
                if (toolbar && toolbar.style.display === 'none') {
                    toolbar.style.display = 'flex';
                }
            }
        });
        
        // Announce page changes to screen readers
        function announceToScreenReader(message) {
            var announcement = document.createElement('div');
            announcement.setAttribute('role', 'status');
            announcement.setAttribute('aria-live', 'polite');
            announcement.className = 'sr-only';
            announcement.textContent = message;
            document.body.appendChild(announcement);
            setTimeout(function() { document.body.removeChild(announcement); }, 3000);
        }
        """
        self.send_response_data(js, "application/javascript")
    
    def _error_page(self, message: str) -> str:
        """Generate error page HTML"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - NETGITS Quiz</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <main class="container">
        <div class="card" style="text-align: center;">
            <div class="brand-logo">NETGITS</div>
            <div style="font-size: 50px; margin: 20px 0;">⚠️</div>
            <h2 style="color: var(--error);">{message}</h2>
            <p style="color: var(--text-secondary); margin: 15px 0;">
                Please go back and try again.
            </p>
            <a href="/" style="display: inline-block; margin-top: 15px; color: var(--accent); 
               text-decoration: none; font-weight: 700; padding: 10px 20px; 
               border: 1px solid var(--accent); border-radius: var(--radius-sm);">
                ← Back to Login
            </a>
        </div>
    </main>
</body>
</html>"""

# ═══════════════════════════════════════════════════════════════════════════
# THEME ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class ThemeEngine:
    """Professional theme management system"""
    
    THEMES = {
        "dark": {
            "name": "Dark Professional",
            "bg_primary": "#0d1117",
            "bg_secondary": "#161b22",
            "bg_tertiary": "#21262d",
            "text_primary": "#e6edf3",
            "text_secondary": "#8b949e",
            "accent": "#58a6ff",
            "accent_hover": "#1f6feb",
            "border": "#30363d",
            "success": "#3fb950",
            "warning": "#d29922",
            "error": "#f85149",
            "input_bg": "#0d1117",
            "card_bg": "#161b22",
            "tab_bg": "#161b22"
        },
        "light": {
            "name": "Light Professional",
            "bg_primary": "#ffffff",
            "bg_secondary": "#f6f8fa",
            "bg_tertiary": "#eaeef2",
            "text_primary": "#1f2328",
            "text_secondary": "#656d76",
            "accent": "#0969da",
            "accent_hover": "#0550ae",
            "border": "#d0d7de",
            "success": "#1a7f37",
            "warning": "#9a6700",
            "error": "#cf222e",
            "input_bg": "#ffffff",
            "card_bg": "#f6f8fa",
            "tab_bg": "#f6f8fa"
        }
    }
    
    def __init__(self):
        self.current_theme = "dark"
        self.colors = self.THEMES["dark"]
    
    def set_theme(self, theme_name: str):
        """Set active theme"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            self.colors = self.THEMES[theme_name]
    
    def toggle_theme(self):
        """Toggle between dark and light"""
        self.set_theme("light" if self.current_theme == "dark" else "dark")
    
    def get_stylesheet(self) -> str:
        """Generate complete Qt stylesheet"""
        c = self.colors
        return f"""
        QMainWindow {{
            background-color: {c['bg_primary']};
        }}
        
        QWidget {{
            color: {c['text_primary']};
            font-family: 'Segoe UI', 'Cairo', 'Noto Sans', sans-serif;
            font-size: 12px;
            background-color: transparent;
        }}
        
        QLabel {{
            color: {c['text_primary']};
            background: transparent;
            padding: 2px;
        }}
        
        QLabel#app_title {{
            font-size: 24px;
            font-weight: 900;
            color: {c['accent']};
            letter-spacing: 1px;
        }}
        
        QLabel#app_subtitle {{
            font-size: 10px;
            color: {c['text_secondary']};
            letter-spacing: 2px;
            text-transform: uppercase;
        }}
        
        QLabel#app_developer {{
            font-size: 10px;
            color: {c['text_secondary']};
            font-style: italic;
        }}
        
        QLabel#server_url {{
            font-size: 15px;
            font-weight: bold;
            color: {c['success']};
            padding: 10px 14px;
            background: {c['input_bg']};
            border-radius: 8px;
            border: 1px solid {c['border']};
        }}
        
        QPushButton {{
            background-color: {c['bg_secondary']};
            border: 1px solid {c['border']};
            border-radius: 7px;
            padding: 9px 18px;
            color: {c['accent']};
            font-weight: bold;
            font-size: 12px;
            min-height: 26px;
        }}
        
        QPushButton:hover {{
            background-color: {c['accent']};
            color: #ffffff;
            border-color: {c['accent_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {c['accent_hover']};
        }}
        
        QPushButton#primary_button {{
            background-color: {c['accent']};
            color: #ffffff;
            font-size: 14px;
            padding: 12px 28px;
            border-radius: 10px;
            font-weight: 700;
        }}
        
        QPushButton#primary_button:hover {{
            background-color: {c['accent_hover']};
            box-shadow: 0 4px 15px rgba(88, 166, 255, 0.3);
        }}
        
        QPushButton#danger_button {{
            background-color: #7f1d1d;
            color: #fca5a5;
            border-color: #dc2626;
        }}
        
        QPushButton#danger_button:hover {{
            background-color: #dc2626;
            color: #ffffff;
        }}
        
        QPushButton#success_button {{
            background-color: #14532d;
            color: #86efac;
            border-color: #22c55e;
        }}
        
        QPushButton#success_button:hover {{
            background-color: #16a34a;
            color: #ffffff;
        }}
        
        QPushButton#icon_button {{
            background: transparent;
            border: none;
            color: {c['accent']};
            font-size: 18px;
            padding: 4px 8px;
            min-width: 32px;
            min-height: 32px;
        }}
        
        QPushButton#icon_button:hover {{
            color: {c['accent_hover']};
            background: rgba(88, 166, 255, 0.1);
            border-radius: 50%;
        }}
        
        QLineEdit, QTextEdit, QSpinBox {{
            background-color: {c['input_bg']};
            border: 1px solid {c['border']};
            border-radius: 7px;
            padding: 9px 14px;
            color: {c['text_primary']};
            font-size: 12px;
            selection-background-color: {c['accent']};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {c['accent']};
        }}
        
        QComboBox {{
            background-color: {c['input_bg']};
            border: 1px solid {c['border']};
            border-radius: 7px;
            padding: 9px 14px;
            color: {c['accent']};
            font-weight: bold;
            font-size: 12px;
            min-height: 26px;
        }}
        
        QComboBox:hover {{
            border-color: {c['accent']};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {c['bg_secondary']};
            border: 1px solid {c['border']};
            border-radius: 7px;
            selection-background-color: {c['accent']};
            selection-color: #ffffff;
            color: {c['text_primary']};
            padding: 4px;
            outline: none;
        }}
        
        QCheckBox {{
            color: {c['text_primary']};
            spacing: 10px;
            font-size: 12px;
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {c['border']};
            border-radius: 4px;
            background-color: {c['input_bg']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {c['accent']};
            border-color: {c['accent']};
        }}
        
        QGroupBox {{
            border: 1px solid {c['border']};
            border-radius: 10px;
            margin-top: 12px;
            padding: 18px 14px 12px;
            font-weight: bold;
            color: {c['accent']};
            font-size: 12px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 14px;
            padding: 0 10px;
            color: {c['accent']};
            background-color: {c['bg_primary']};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {c['border']};
            background-color: {c['bg_primary']};
            border-radius: 0 0 10px 10px;
            top: -1px;
        }}
        
        QTabBar::tab {{
            background-color: {c['tab_bg']};
            color: {c['text_secondary']};
            padding: 10px 22px;
            margin-right: 2px;
            border: 1px solid {c['border']};
            border-bottom: none;
            border-radius: 10px 10px 0 0;
            font-size: 11px;
            font-weight: 600;
        }}
        
        QTabBar::tab:selected {{
            background-color: {c['bg_primary']};
            color: {c['accent']};
            border-bottom: 3px solid {c['accent']};
        }}
        
        QTabBar::tab:hover:!selected {{
            color: {c['accent']};
            background-color: {c['bg_tertiary']};
        }}
        
        QTableWidget {{
            background-color: {c['input_bg']};
            border: 1px solid {c['border']};
            border-radius: 7px;
            gridline-color: {c['border']};
        }}
        
        QTableWidget::item {{
            padding: 7px;
        }}
        
        QTableWidget::item:selected {{
            background-color: {c['accent']};
            color: #ffffff;
        }}
        
        QHeaderView::section {{
            background-color: {c['bg_secondary']};
            color: {c['accent']};
            padding: 10px;
            border: 1px solid {c['border']};
            font-weight: bold;
            font-size: 11px;
        }}
        
        QListWidget {{
            background-color: {c['input_bg']};
            border: 1px solid {c['border']};
            border-radius: 7px;
            padding: 3px;
            color: {c['text_primary']};
            font-size: 12px;
        }}
        
        QListWidget::item {{
            padding: 9px 12px;
            border-bottom: 1px solid {c['border']};
            border-radius: 4px;
        }}
        
        QListWidget::item:hover {{
            background-color: {c['bg_secondary']};
        }}
        
        QListWidget::item:selected {{
            background-color: {c['accent']};
            color: #ffffff;
        }}
        
        QProgressBar {{
            border: none;
            background-color: {c['bg_secondary']};
            height: 6px;
            border-radius: 3px;
        }}
        
        QProgressBar::chunk {{
            background-color: {c['accent']};
            border-radius: 3px;
        }}
        
        QStatusBar {{
            background-color: {c['bg_secondary']};
            color: {c['text_secondary']};
            border-top: 1px solid {c['border']};
            font-size: 11px;
            padding: 3px 8px;
        }}
        
        QScrollBar:vertical {{
            background: {c['bg_primary']};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {c['accent']};
            border-radius: 5px;
            min-height: 25px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {c['accent_hover']};
        }}
        
        QScrollBar::add-line, QScrollBar::sub-line {{
            height: 0;
            width: 0;
        }}
        
        QMenu {{
            background-color: {c['bg_secondary']};
            border: 1px solid {c['border']};
            border-radius: 10px;
            padding: 6px;
        }}
        
        QMenu::item {{
            padding: 10px 30px;
            border-radius: 6px;
        }}
        
        QMenu::item:selected {{
            background-color: {c['accent']};
            color: #ffffff;
        }}
        
        QToolTip {{
            background-color: {c['bg_secondary']};
            color: {c['text_primary']};
            border: 1px solid {c['accent']};
            border-radius: 5px;
            padding: 7px 12px;
            font-size: 11px;
        }}
        
        QDialog {{
            background-color: {c['bg_primary']};
        }}
        
        QFrame#about_frame {{
            background-color: {c['card_bg']};
            border: 2px solid {c['accent']};
            border-radius: 20px;
        }}
        
        QScrollArea {{
            border: none;
            background: transparent;
        }}
        
        QSlider::groove:horizontal {{
            height: 6px;
            background: {c['bg_secondary']};
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background: {c['accent']};
            width: 20px;
            height: 20px;
            margin: -7px 0;
            border-radius: 10px;
        }}
        """

# ═══════════════════════════════════════════════════════════════════════════
# ABOUT DIALOG
# ═══════════════════════════════════════════════════════════════════════════

class AboutDialog(QDialog):
    """Professional about dialog with contact information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About NETGITS Quiz")
        self.setFixedSize(440, 520)
        self.setModal(True)
        
        self._setup_ui()
        self._animate_entrance()
    
    def _setup_ui(self):
        """Setup the about dialog UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Main card
        card = QFrame()
        card.setObjectName("about_frame")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(5)
        card_layout.setContentsMargins(25, 20, 25, 20)
        
        # Title bar with close button
        title_bar = QHBoxLayout()
        title_bar.addStretch()
        close_button = QPushButton("✕")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet(
            "background: transparent; border: none; color: #8b949e; "
            "font-size: 16px; font-weight: bold;"
        )
        close_button.clicked.connect(self.close)
        close_button.setToolTip("Close")
        title_bar.addWidget(close_button)
        card_layout.addLayout(title_bar)
        
        # Logo
        logo_label = QLabel("NETGITS QUIZ")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet(
            "font-size: 28px; font-weight: 900; color: #58a6ff; letter-spacing: 2px;"
        )
        card_layout.addWidget(logo_label)
        
        # Version
        version_label = QLabel(f"Version {Config.APP_VERSION}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(
            "color: #f85149; font-size: 13px; font-weight: bold;"
        )
        card_layout.addWidget(version_label)
        
        # Codename
        codename_label = QLabel(f'"{Config.APP_CODENAME}"')
        codename_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        codename_label.setStyleSheet(
            "color: #3fb950; font-size: 11px; font-style: italic;"
        )
        card_layout.addWidget(codename_label)
        
        # Accessibility badge
        a11y_badge = QLabel("♿ Full Accessibility Support")
        a11y_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        a11y_badge.setStyleSheet(
            "color: #d29922; font-size: 11px; font-weight: bold; "
            "background: #21262d; padding: 4px 12px; border-radius: 12px;"
        )
        card_layout.addWidget(a11y_badge)
        
        # Tagline
        tagline_label = QLabel(Config.APP_TAGLINE)
        tagline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline_label.setStyleSheet("color: #8b949e; font-size: 11px;")
        card_layout.addWidget(tagline_label)
        
        # Separator
        separator = QLabel()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #30363d; margin: 8px 0;")
        card_layout.addWidget(separator)
        
        # Developer info
        dev_label = QLabel(f"👨‍💻 Developed by {Config.DEV_NAME}")
        dev_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dev_label.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #e6edf3;"
        )
        card_layout.addWidget(dev_label)
        
        # Contact links
        contacts = [
            ("📧", "Email", Config.EMAIL, f"mailto:{Config.EMAIL}"),
            ("🌐", "Website", Config.WEBSITE, Config.WEBSITE),
            ("💬", "WhatsApp", Config.PHONE, Config.WHATSAPP),
            ("📘", "Facebook", "Adam Mahmoud", Config.FACEBOOK),
            ("⭐", "GitHub", "NETGITS", Config.GITHUB),
        ]
        
        for icon, label, text, url in contacts:
            row = QHBoxLayout()
            row.setSpacing(8)
            
            link_button = QPushButton(icon)
            link_button.setObjectName("icon_button")
            link_button.setFixedSize(36, 36)
            link_button.setToolTip(f"Open {label}")
            link_button.clicked.connect(
                lambda checked, u=url: QDesktopServices.openUrl(QUrl(u))
            )
            row.addWidget(link_button)
            
            info_column = QVBoxLayout()
            info_column.setSpacing(0)
            
            name_label = QLabel(f"<b>{label}</b>")
            name_label.setStyleSheet("font-size: 11px;")
            info_column.addWidget(name_label)
            
            value_label = QLabel(text)
            value_label.setStyleSheet("color: #58a6ff; font-size: 10px;")
            value_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            value_label.mousePressEvent = lambda e, u=url: QDesktopServices.openUrl(QUrl(u))
            info_column.addWidget(value_label)
            
            row.addLayout(info_column, 1)
            card_layout.addLayout(row)
        
        # Separator
        separator2 = QLabel()
        separator2.setFixedHeight(1)
        separator2.setStyleSheet("background-color: #30363d; margin: 8px 0;")
        card_layout.addWidget(separator2)
        
        # Copyright
        copyright_label = QLabel("© 2024 NETGITS Technologies")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setStyleSheet("color: #484f58; font-size: 10px;")
        card_layout.addWidget(copyright_label)
        
        # Star request
        star_label = QLabel("⭐ If you like this app, please star us on GitHub!")
        star_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        star_label.setStyleSheet(
            "color: #d29922; font-size: 11px; font-weight: bold;"
        )
        card_layout.addWidget(star_label)
        
        # Bottom close button
        bottom_close = QPushButton("✕ Close")
        bottom_close.clicked.connect(self.close)
        bottom_close.setStyleSheet(
            "background-color: #30363d; border: 1px solid #484f58; "
            "border-radius: 6px; padding: 8px; color: #e6edf3; "
            "font-weight: bold; font-size: 12px; margin-top: 6px;"
        )
        card_layout.addWidget(bottom_close)
        
        main_layout.addWidget(card)
    
    def _animate_entrance(self):
        """Fade in animation"""
        self.setWindowOpacity(0.0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(400)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

# ═══════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION WINDOW
# ═══════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    """NETGITS Quiz - Teacher Panel Main Window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize core components
        self.database = Database()
        self.server: Optional[QuizServer] = None
        self.theme_engine = ThemeEngine()
        self.current_language = "en"
        
        # Teacher accessibility settings
        self.accessibility_settings = {
            "font_size": 12,
            "high_contrast": False,
            "dyslexia_font": False,
            "screen_reader": False,
            "zoom_level": 100
        }
        
        # Window setup
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        self.setGeometry(100, 100, 1120, 760)
        self.setMinimumSize(920, 640)
        
        # Apply theme
        self._apply_theme()
        
        # Setup UI
        self._setup_ui()
        self._setup_keyboard_shortcuts()
        
        # Load data
        QTimer.singleShot(500, self._refresh_all_data)
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._refresh_all_data)
        self.refresh_timer.start(30000)
        
        # Log activity
        self.database.log_activity("Application started")
    
    def _apply_theme(self):
        """Apply current theme"""
        self.setStyleSheet(self.theme_engine.get_stylesheet())
    
    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        shortcuts = {
            "Ctrl+R": self._refresh_all_data,
            "Ctrl+1": lambda: self.main_tabs.setCurrentIndex(0),
            "Ctrl+2": lambda: self.main_tabs.setCurrentIndex(1),
            "Ctrl+3": lambda: self.main_tabs.setCurrentIndex(2),
            "Ctrl+4": lambda: self.main_tabs.setCurrentIndex(3),
            "Ctrl+5": lambda: self.main_tabs.setCurrentIndex(4),
            "Ctrl+T": self._toggle_theme,
            "Ctrl+Shift+A": self._show_accessibility_panel,
            "F1": self._show_help,
            "F5": self._refresh_all_data,
            "F11": self._toggle_fullscreen,
        }
        
        for key_sequence, callback in shortcuts.items():
            QShortcut(QKeySequence(key_sequence), self, callback)
    
    def _setup_ui(self):
        """Setup the complete user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(14, 10, 14, 8)
        
        # ═══════════════════ Header ═══════════════════
        header_layout = QHBoxLayout()
        
        # Title section
        title_column = QVBoxLayout()
        title_column.setSpacing(1)
        
        app_title = QLabel(Config.APP_NAME)
        app_title.setObjectName("app_title")
        title_column.addWidget(app_title)
        
        app_subtitle = QLabel("Teacher Panel | ♿ Full Accessibility")
        app_subtitle.setObjectName("app_subtitle")
        title_column.addWidget(app_subtitle)
        
        developer_label = QLabel(f"by {Config.DEV_NAME} | {Config.WEBSITE}")
        developer_label.setObjectName("app_developer")
        title_column.addWidget(developer_label)
        
        header_layout.addLayout(title_column)
        header_layout.addStretch()
        
        # Accessibility button
        a11y_button = QPushButton("♿")
        a11y_button.setObjectName("icon_button")
        a11y_button.setToolTip("Accessibility Settings (Ctrl+Shift+A)")
        a11y_button.clicked.connect(self._show_accessibility_panel)
        header_layout.addWidget(a11y_button)
        
        # Language selector
        language_combo = QComboBox()
        language_combo.addItems(["English", "العربية"])
        language_combo.setCurrentIndex(0)
        language_combo.setFixedWidth(100)
        language_combo.setToolTip("Select Language")
        header_layout.addWidget(language_combo)
        
        # Theme toggle
        theme_button = QPushButton("🌓")
        theme_button.setObjectName("icon_button")
        theme_button.setToolTip("Toggle Theme (Ctrl+T)")
        theme_button.clicked.connect(self._toggle_theme)
        header_layout.addWidget(theme_button)
        
        # About button
        about_button = QPushButton("ℹ️")
        about_button.setObjectName("icon_button")
        about_button.setToolTip("About NETGITS Quiz")
        about_button.clicked.connect(self._show_about_dialog)
        header_layout.addWidget(about_button)
        
        main_layout.addLayout(header_layout)
        
        # ═══════════════════ Tab Widget ═══════════════════
        self.main_tabs = QTabWidget()
        
        # Tab 1: Exams Management
        self.main_tabs.addTab(self._create_exams_tab(), "📋 Exams")
        
        # Tab 2: Create Exam
        self.main_tabs.addTab(self._create_exam_builder_tab(), "➕ Create")
        
        # Tab 3: Results
        self.main_tabs.addTab(self._create_results_tab(), "📊 Results")
        
        # Tab 4: Assign Students
        self.main_tabs.addTab(self._create_assign_tab(), "👥 Assign")
        
        # Tab 5: Server
        self.main_tabs.addTab(self._create_server_tab(), "🌐 Server")
        
        main_layout.addWidget(self.main_tabs)
        
        # ═══════════════════ Status Bar ═══════════════════
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🟢 Ready | Create an exam and start the server")
    
    def _create_exams_tab(self) -> QWidget:
        """Create exams management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(6, 8, 6, 6)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        refresh_button = QPushButton("🔄 Refresh List")
        refresh_button.clicked.connect(self._refresh_exams_list)
        refresh_button.setToolTip("Refresh exam list (F5)")
        actions_layout.addWidget(refresh_button)
        
        delete_button = QPushButton("🗑️ Delete Selected")
        delete_button.setObjectName("danger_button")
        delete_button.clicked.connect(self._delete_selected_exam)
        delete_button.setToolTip("Delete the selected exam")
        actions_layout.addWidget(delete_button)
        
        actions_layout.addStretch()
        
        total_label = QLabel("Total: 0 exams")
        total_label.setObjectName("total_label")
        actions_layout.addWidget(total_label)
        
        layout.addLayout(actions_layout)
        
        # Exams table
        self.exams_table = QTableWidget()
        self.exams_table.setColumnCount(8)
        self.exams_table.setHorizontalHeaderLabels([
            "ID", "Title", "Questions", "Duration", "Password", 
            "Accessibility", "Status", "Action"
        ])
        
        # Set column widths
        self.exams_table.setColumnWidth(0, 40)
        self.exams_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.exams_table.setColumnWidth(2, 70)
        self.exams_table.setColumnWidth(3, 70)
        self.exams_table.setColumnWidth(4, 80)
        self.exams_table.setColumnWidth(5, 90)
        self.exams_table.setColumnWidth(6, 80)
        self.exams_table.setColumnWidth(7, 110)
        
        self.exams_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.exams_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.exams_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.exams_table.verticalHeader().setVisible(False)
        self.exams_table.setAlternatingRowColors(True)
        self.exams_table.setShowGrid(True)
        
        layout.addWidget(self.exams_table)
        
        return widget
    
    def _create_exam_builder_tab(self) -> QWidget:
        """Create exam builder tab"""
        widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(6, 8, 6, 6)
        
        # ═══ Exam Details ═══
        details_group = QGroupBox("📝 Exam Details")
        details_layout = QFormLayout(details_group)
        details_layout.setSpacing(10)
        details_layout.setContentsMargins(14, 22, 14, 14)
        
        self.exam_title_input = QLineEdit()
        self.exam_title_input.setPlaceholderText("e.g., Midterm Examination - Computer Science 101")
        self.exam_title_input.setMinimumHeight(38)
        self.exam_title_input.setToolTip("Enter a descriptive title for the exam")
        details_layout.addRow("Title *:", self.exam_title_input)
        
        self.exam_description_input = QTextEdit()
        self.exam_description_input.setMaximumHeight(55)
        self.exam_description_input.setMinimumHeight(45)
        self.exam_description_input.setPlaceholderText("Optional description or instructions for students...")
        details_layout.addRow("Description:", self.exam_description_input)
        
        # Password and Duration row
        settings_row = QHBoxLayout()
        settings_row.setSpacing(14)
        
        password_column = QVBoxLayout()
        password_column.setSpacing(4)
        password_column.addWidget(QLabel("Password:"))
        self.exam_password_input = QLineEdit()
        self.exam_password_input.setPlaceholderText("Optional password")
        self.exam_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.exam_password_input.setMinimumHeight(38)
        password_column.addWidget(self.exam_password_input)
        settings_row.addLayout(password_column)
        
        duration_column = QVBoxLayout()
        duration_column.setSpacing(4)
        duration_column.addWidget(QLabel("Duration:"))
        self.exam_duration_spin = QSpinBox()
        self.exam_duration_spin.setRange(1, 180)
        self.exam_duration_spin.setValue(30)
        self.exam_duration_spin.setSuffix(" minutes")
        self.exam_duration_spin.setMinimumHeight(38)
        self.exam_duration_spin.setToolTip("Exam duration in minutes (1-180)")
        duration_column.addWidget(self.exam_duration_spin)
        settings_row.addLayout(duration_column)
        
        details_layout.addRow(settings_row)
        layout.addWidget(details_group)
        
        # ═══ Accessibility Settings ═══
        accessibility_group = QGroupBox("♿ Accessibility Options")
        accessibility_layout = QGridLayout(accessibility_group)
        accessibility_layout.setContentsMargins(14, 22, 14, 14)
        accessibility_layout.setSpacing(8)
        
        self.accessibility_enabled_check = QCheckBox("Enable Accessibility Features")
        self.accessibility_enabled_check.setChecked(True)
        self.accessibility_enabled_check.setToolTip(
            "Enable screen reader, large font, and high contrast options for students"
        )
        accessibility_layout.addWidget(self.accessibility_enabled_check, 0, 0, 1, 2)
        
        accessibility_layout.addWidget(QLabel("Extra Time:"), 1, 0)
        self.extra_time_combo = QComboBox()
        self.extra_time_combo.addItems(["0%", "25%", "50%", "100%", "150%", "200%"])
        self.extra_time_combo.setToolTip("Additional time percentage for students with accessibility needs")
        accessibility_layout.addWidget(self.extra_time_combo, 1, 1)
        
        self.screen_reader_check = QCheckBox("Screen Reader Support")
        self.screen_reader_check.setChecked(True)
        accessibility_layout.addWidget(self.screen_reader_check, 2, 0)
        
        self.large_font_check = QCheckBox("Large Font Option")
        self.large_font_check.setChecked(True)
        accessibility_layout.addWidget(self.large_font_check, 3, 0)
        
        self.high_contrast_check = QCheckBox("High Contrast Option")
        self.high_contrast_check.setChecked(True)
        accessibility_layout.addWidget(self.high_contrast_check, 4, 0)
        
        layout.addWidget(accessibility_group)
        
        # ═══ Exam Settings ═══
        settings_group = QGroupBox("⚙️ Exam Configuration")
        settings_inner_layout = QVBoxLayout(settings_group)
        settings_inner_layout.setContentsMargins(14, 22, 14, 14)
        
        self.shuffle_questions_check = QCheckBox("Randomize Question Order")
        self.shuffle_questions_check.setChecked(True)
        self.shuffle_questions_check.setToolTip("Questions will appear in random order for each student")
        settings_inner_layout.addWidget(self.shuffle_questions_check)
        
        self.shuffle_choices_check = QCheckBox("Randomize Answer Choices")
        self.shuffle_choices_check.setChecked(True)
        self.shuffle_choices_check.setToolTip(
            "Answer options (A/B/C/D) will be shuffled for multiple choice questions"
        )
        settings_inner_layout.addWidget(self.shuffle_choices_check)
        
        layout.addWidget(settings_group)
        
        # ═══ Questions List ═══
        questions_group = QGroupBox("📌 Questions")
        questions_layout = QVBoxLayout(questions_group)
        questions_layout.setContentsMargins(14, 22, 14, 14)
        
        self.questions_list_widget = QListWidget()
        self.questions_list_widget.setMinimumHeight(180)
        self.questions_list_widget.setAlternatingRowColors(True)
        self.questions_list_widget.setToolTip("List of questions for this exam")
        questions_layout.addWidget(self.questions_list_widget)
        
        # Question action buttons
        question_buttons_layout = QHBoxLayout()
        question_buttons_layout.setSpacing(8)
        
        add_question_button = QPushButton("➕ Add New Question")
        add_question_button.setMinimumHeight(34)
        add_question_button.setToolTip("Add a new question to the exam")
        add_question_button.clicked.connect(self._show_add_question_dialog)
        question_buttons_layout.addWidget(add_question_button)
        
        remove_question_button = QPushButton("🗑️ Remove Selected")
        remove_question_button.setObjectName("danger_button")
        remove_question_button.setMinimumHeight(34)
        remove_question_button.setToolTip("Remove the selected question")
        remove_question_button.clicked.connect(
            lambda: self.questions_list_widget.takeItem(
                self.questions_list_widget.currentRow()
            ) if self.questions_list_widget.currentRow() >= 0 else None
        )
        question_buttons_layout.addWidget(remove_question_button)
        
        questions_layout.addLayout(question_buttons_layout)
        layout.addWidget(questions_group)
        
        # ═══ Create Button ═══
        self.create_exam_button = QPushButton("🚀 Create Examination")
        self.create_exam_button.setObjectName("primary_button")
        self.create_exam_button.setMinimumHeight(48)
        self.create_exam_button.setToolTip("Create the exam with all questions")
        self.create_exam_button.clicked.connect(self._create_exam)
        layout.addWidget(self.create_exam_button)
        
        layout.addStretch()
        return scroll_area
    
    def _create_results_tab(self) -> QWidget:
        """Create results tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(6, 8, 6, 6)
        
        # Exam selector
        selector_row = QHBoxLayout()
        selector_row.setSpacing(8)
        selector_row.addWidget(QLabel("Select Exam:"))
        
        self.results_exam_combo = QComboBox()
        self.results_exam_combo.setMinimumHeight(34)
        self.results_exam_combo.currentIndexChanged.connect(self._load_results)
        selector_row.addWidget(self.results_exam_combo, 1)
        
        layout.addLayout(selector_row)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(8)
        self.results_table.setHorizontalHeaderLabels([
            "Student Name", "Student ID", "Score", "Total", "Percentage", 
            "Status", "Grading", "View"
        ])
        
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for i, width in enumerate([0, 0, 60, 60, 70, 80, 80, 70]):
            if i > 1:
                self.results_table.setColumnWidth(i, width)
        
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.results_table)
        
        # Export button
        export_button = QPushButton("📥 Export Results to CSV")
        export_button.setMinimumHeight(34)
        export_button.clicked.connect(self._export_results)
        export_button.setToolTip("Export student results to CSV file")
        layout.addWidget(export_button)
        
        return widget
    
    def _create_assign_tab(self) -> QWidget:
        """Create student assignment tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(6, 8, 6, 6)
        
        # Assignment section
        assign_group = QGroupBox("👥 Assign Exam to Students")
        assign_layout = QFormLayout(assign_group)
        assign_layout.setSpacing(10)
        assign_layout.setContentsMargins(14, 22, 14, 14)
        
        self.assign_exam_combo = QComboBox()
        self.assign_exam_combo.setMinimumHeight(34)
        assign_layout.addRow("Select Exam:", self.assign_exam_combo)
        
        self.assign_names_text = QTextEdit()
        self.assign_names_text.setMaximumHeight(90)
        self.assign_names_text.setPlaceholderText(
            "Enter student names (one per line)...\n\nExample:\nAhmed Mohamed\nSara Ali\nOmar Hassan"
        )
        assign_layout.addRow("Student Names:", self.assign_names_text)
        
        # Accessibility profile
        assign_layout.addRow(QLabel("<b>Accessibility Profile:</b>"))
        self.assign_extra_time_combo = QComboBox()
        self.assign_extra_time_combo.addItems(["0%", "25%", "50%", "100%", "150%", "200%"])
        assign_layout.addRow("Extra Time:", self.assign_extra_time_combo)
        
        self.assign_large_font_check = QCheckBox("Large Font Enabled")
        assign_layout.addRow("", self.assign_large_font_check)
        
        self.assign_screen_reader_check = QCheckBox("Screen Reader Enabled")
        assign_layout.addRow("", self.assign_screen_reader_check)
        
        assign_button = QPushButton("🎫 Generate Access Tokens")
        assign_button.setObjectName("primary_button")
        assign_button.setMinimumHeight(40)
        assign_button.clicked.connect(self._assign_exam_to_students)
        assign_layout.addRow("", assign_button)
        
        layout.addWidget(assign_group)
        
        # Tokens section
        tokens_group = QGroupBox("📋 Generated Tokens")
        tokens_layout = QVBoxLayout(tokens_group)
        tokens_layout.setContentsMargins(14, 22, 14, 14)
        
        self.tokens_table = QTableWidget()
        self.tokens_table.setColumnCount(4)
        self.tokens_table.setHorizontalHeaderLabels([
            "Student Name", "Access Token", "Status", "Accessibility"
        ])
        self.tokens_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tokens_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tokens_table.verticalHeader().setVisible(False)
        tokens_layout.addWidget(self.tokens_table)
        
        refresh_tokens_button = QPushButton("🔄 Refresh Tokens")
        refresh_tokens_button.clicked.connect(self._refresh_tokens)
        tokens_layout.addWidget(refresh_tokens_button)
        
        layout.addWidget(tokens_group)
        
        return widget
    
    def _create_server_tab(self) -> QWidget:
        """Create server management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(6, 8, 6, 6)
        
        # Server Information
        server_info_group = QGroupBox("🌐 Server Information")
        server_info_layout = QFormLayout(server_info_group)
        server_info_layout.setSpacing(10)
        server_info_layout.setContentsMargins(14, 22, 14, 14)
        
        self.server_ip_label = QLabel("Detecting IP address...")
        self.server_ip_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #58a6ff;")
        server_info_layout.addRow("Local IP Address:", self.server_ip_label)
        
        self.server_url_label = QLabel("http://localhost:8080")
        self.server_url_label.setObjectName("server_url")
        server_info_layout.addRow("Student Access URL:", self.server_url_label)
        
        copy_url_button = QPushButton("📋 Copy URL to Clipboard")
        copy_url_button.setMinimumHeight(34)
        copy_url_button.clicked.connect(
            lambda: QApplication.clipboard().setText(self.server_url_label.text())
        )
        server_info_layout.addRow("", copy_url_button)
        
        layout.addWidget(server_info_group)
        
        # Server Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        self.start_server_button = QPushButton("🚀 Start Server")
        self.start_server_button.setObjectName("primary_button")
        self.start_server_button.setMinimumHeight(48)
        self.start_server_button.clicked.connect(self._start_server)
        controls_layout.addWidget(self.start_server_button)
        
        self.stop_server_button = QPushButton("⏹️ Stop Server")
        self.stop_server_button.setObjectName("danger_button")
        self.stop_server_button.setMinimumHeight(48)
        self.stop_server_button.setEnabled(False)
        self.stop_server_button.clicked.connect(self._stop_server)
        controls_layout.addWidget(self.stop_server_button)
        
        layout.addLayout(controls_layout)
        
        # Active Exams
        active_exams_group = QGroupBox("📋 Active Exams on Network")
        active_exams_layout = QVBoxLayout(active_exams_group)
        active_exams_layout.setContentsMargins(14, 22, 14, 14)
        
        self.active_exams_list = QListWidget()
        self.active_exams_list.setMinimumHeight(120)
        active_exams_layout.addWidget(self.active_exams_list)
        
        layout.addWidget(active_exams_group)
        
        # Update IP on load
        QTimer.singleShot(600, self._update_server_ip)
        
        return widget
    
    # ═══════════════════ Core Functions ═══════════════════
    
    def _show_add_question_dialog(self):
        """Show dialog to add a new question"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Question")
        dialog.setFixedSize(560, 480)
        dialog.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(8)
        layout.setContentsMargins(22, 18, 22, 18)
        
        # Question Type
        layout.addWidget(QLabel("<b>Question Type:</b>"))
        question_type_combo = QComboBox()
        question_type_combo.addItems(Config.QUESTION_TYPES)
        question_type_combo.setMinimumHeight(34)
        layout.addWidget(question_type_combo)
        
        # Question Text
        layout.addWidget(QLabel("<b>Question Text:</b>"))
        question_text_edit = QTextEdit()
        question_text_edit.setMaximumHeight(75)
        question_text_edit.setMinimumHeight(55)
        question_text_edit.setPlaceholderText("Enter the question here...")
        layout.addWidget(question_text_edit)
        
        # Alt text for accessibility
        layout.addWidget(QLabel("<b>Alt Text (for visually impaired students):</b>"))
        alt_text_input = QLineEdit()
        alt_text_input.setPlaceholderText("Describe the question for screen readers...")
        layout.addWidget(alt_text_input)
        
        # Media attachments
        self.temp_image_path = ""
        self.temp_audio_path = ""
        
        media_row = QHBoxLayout()
        image_button = QPushButton("📷 Attach Image")
        image_button.clicked.connect(lambda: self._attach_media_file("image"))
        media_row.addWidget(image_button)
        
        audio_button = QPushButton("🎵 Attach Audio")
        audio_button.clicked.connect(lambda: self._attach_media_file("audio"))
        media_row.addWidget(audio_button)
        
        self.media_status_label = QLabel("")
        media_row.addWidget(self.media_status_label)
        media_row.addStretch()
        layout.addLayout(media_row)
        
        # Options
        options_frame = QFrame()
        options_layout = QGridLayout(options_frame)
        options_layout.setSpacing(6)
        
        option_a = QLineEdit()
        option_a.setPlaceholderText("Option A")
        option_a.setMinimumHeight(34)
        options_layout.addWidget(QLabel("A:"), 0, 0)
        options_layout.addWidget(option_a, 0, 1)
        
        option_b = QLineEdit()
        option_b.setPlaceholderText("Option B")
        option_b.setMinimumHeight(34)
        options_layout.addWidget(QLabel("B:"), 1, 0)
        options_layout.addWidget(option_b, 1, 1)
        
        option_c = QLineEdit()
        option_c.setPlaceholderText("Option C (optional)")
        option_c.setMinimumHeight(34)
        options_layout.addWidget(QLabel("C:"), 2, 0)
        options_layout.addWidget(option_c, 2, 1)
        
        option_d = QLineEdit()
        option_d.setPlaceholderText("Option D (optional)")
        option_d.setMinimumHeight(34)
        options_layout.addWidget(QLabel("D:"), 3, 0)
        options_layout.addWidget(option_d, 3, 1)
        
        layout.addWidget(options_frame)
        
        # Answer and Points
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(14)
        
        answer_column = QVBoxLayout()
        answer_column.setSpacing(4)
        answer_column.addWidget(QLabel("<b>Correct Answer:</b>"))
        correct_answer_input = QLineEdit()
        correct_answer_input.setPlaceholderText("A / B / C / D / True / False / text")
        correct_answer_input.setMinimumHeight(34)
        answer_column.addWidget(correct_answer_input)
        bottom_row.addLayout(answer_column, 2)
        
        points_column = QVBoxLayout()
        points_column.setSpacing(4)
        points_column.addWidget(QLabel("<b>Points:</b>"))
        points_spin = QSpinBox()
        points_spin.setRange(1, 20)
        points_spin.setValue(1)
        points_spin.setMinimumHeight(34)
        points_column.addWidget(points_spin)
        bottom_row.addLayout(points_column, 1)
        
        layout.addLayout(bottom_row)
        
        # Save button
        save_button = QPushButton("✅ Add Question to Exam")
        save_button.setObjectName("primary_button")
        save_button.setMinimumHeight(42)
        
        def save_question():
            if not question_text_edit.toPlainText().strip():
                QMessageBox.warning(dialog, "Error", "Please enter the question text!")
                return
            
            question_data = {
                'type': question_type_combo.currentText(),
                'text': question_text_edit.toPlainText().strip(),
                'a': option_a.text().strip(),
                'b': option_b.text().strip(),
                'c': option_c.text().strip(),
                'd': option_d.text().strip(),
                'correct': correct_answer_input.text().strip(),
                'points': points_spin.value(),
                'image': self.temp_image_path,
                'audio': self.temp_audio_path,
                'alt_text': alt_text_input.text().strip()
            }
            
            # Build display text
            display_text = f"[{question_data['type'][:20]}] {question_data['text'][:55]}... ({question_data['points']}pts)"
            if question_data['image']:
                display_text += " 📷"
            if question_data['audio']:
                display_text += " 🎵"
            if question_data['alt_text']:
                display_text += " ♿"
            
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.ItemDataRole.UserRole, question_data)
            self.questions_list_widget.addItem(list_item)
            
            self.temp_image_path = ""
            self.temp_audio_path = ""
            self.media_status_label.setText("")
            dialog.accept()
        
        save_button.clicked.connect(save_question)
        layout.addWidget(save_button)
        
        dialog.exec()
    
    def _attach_media_file(self, media_type: str):
        """Attach image or audio file to question"""
        if media_type == "image":
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Image", os.path.expanduser("~"),
                "Images (*.png *.jpg *.jpeg *.gif *.bmp)"
            )
            if file_path:
                dest_path = os.path.join(
                    self.database.media_path,
                    f"img_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(file_path)}"
                )
                shutil.copy2(file_path, dest_path)
                self.temp_image_path = dest_path
                self.media_status_label.setText("📷 Image attached")
        
        elif media_type == "audio":
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Audio", os.path.expanduser("~"),
                "Audio (*.mp3 *.wav *.ogg *.m4a)"
            )
            if file_path:
                dest_path = os.path.join(
                    self.database.media_path,
                    f"aud_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(file_path)}"
                )
                shutil.copy2(file_path, dest_path)
                self.temp_audio_path = dest_path
                self.media_status_label.setText("🎵 Audio attached")
    
    def _create_exam(self):
        """Create new exam"""
        title = self.exam_title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "⚠️ Error", "Please enter an exam title!")
            return
        
        if self.questions_list_widget.count() == 0:
            QMessageBox.warning(self, "⚠️ Error", "Please add at least one question!")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Creation",
            f"Create exam '{title}' with {self.questions_list_widget.count()} questions?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        try:
            password = self.exam_password_input.text().strip() or None
            duration = self.exam_duration_spin.value()
            extra_time = int(self.extra_time_combo.currentText().replace("%", ""))
            
            self.database.execute("""
                INSERT INTO exams (
                    title, description, password, duration_minutes,
                    shuffle_questions, shuffle_choices,
                    accessibility_enabled, extra_time_percent,
                    screen_reader_enabled, large_font_enabled, high_contrast_enabled
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                title,
                self.exam_description_input.toPlainText().strip(),
                password,
                duration,
                int(self.shuffle_questions_check.isChecked()),
                int(self.shuffle_choices_check.isChecked()),
                int(self.accessibility_enabled_check.isChecked()),
                extra_time,
                int(self.screen_reader_check.isChecked()),
                int(self.large_font_check.isChecked()),
                int(self.high_contrast_check.isChecked())
            ))
            self.database.commit()
            
            exam_id = self.database.fetch_one("SELECT last_insert_rowid()")[0]
            
            # Insert questions
            for i in range(self.questions_list_widget.count()):
                item = self.questions_list_widget.item(i)
                question_data = item.data(Qt.ItemDataRole.UserRole)
                
                self.database.execute("""
                    INSERT INTO questions (
                        exam_id, question_type, question_text,
                        option_a, option_b, option_c, option_d,
                        correct_answer, points, order_num,
                        image_path, audio_path, alt_text
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    exam_id,
                    question_data['type'],
                    question_data['text'],
                    question_data['a'],
                    question_data['b'],
                    question_data['c'],
                    question_data['d'],
                    question_data['correct'],
                    question_data['points'],
                    i + 1,
                    question_data.get('image', ''),
                    question_data.get('audio', ''),
                    question_data.get('alt_text', '')
                ))
            
            self.database.commit()
            self.database.log_activity("Exam created", f"Title: {title}, Questions: {self.questions_list_widget.count()}")
            
            QMessageBox.information(
                self, "✅ Success",
                f"Exam '{title}' created successfully!\n\n"
                f"📝 Questions: {self.questions_list_widget.count()}\n"
                f"⏱️ Duration: {duration} minutes\n"
                f"♿ Accessibility: {'Enabled' if self.accessibility_enabled_check.isChecked() else 'Disabled'}\n\n"
                f"Go to the 'Exams' tab to activate it, then start the server."
            )
            
            # Clear form
            self.exam_title_input.clear()
            self.exam_description_input.clear()
            self.exam_password_input.clear()
            self.questions_list_widget.clear()
            self._refresh_all_data()
            
        except Exception as error:
            QMessageBox.critical(self, "❌ Error", f"Failed to create exam:\n\n{str(error)}")
    
    def _refresh_exams_list(self):
        """Refresh exams table"""
        try:
            exams = self.database.fetch_all(
                "SELECT * FROM exams ORDER BY created_date DESC"
            )
            
            self.exams_table.setRowCount(len(exams))
            
            for i, exam in enumerate(exams):
                # Count questions
                question_count = self.database.fetch_one(
                    "SELECT COUNT(*) as cnt FROM questions WHERE exam_id = ?",
                    (exam["id"],)
                )
                q_count = question_count["cnt"] if question_count else 0
                
                self.exams_table.setItem(i, 0, QTableWidgetItem(str(exam["id"])))
                self.exams_table.setItem(i, 1, QTableWidgetItem(exam["title"]))
                self.exams_table.setItem(i, 2, QTableWidgetItem(str(q_count)))
                self.exams_table.setItem(i, 3, QTableWidgetItem(f"{exam['duration_minutes']} min"))
                self.exams_table.setItem(i, 4, QTableWidgetItem(exam["password"] or "None"))
                
                # Accessibility indicator
                a11y_indicator = "♿" if exam["accessibility_enabled"] else "-"
                self.exams_table.setItem(i, 5, QTableWidgetItem(a11y_indicator))
                
                # Status
                status_text = "🟢 Active" if exam["is_active"] else "🔴 Inactive"
                self.exams_table.setItem(i, 6, QTableWidgetItem(status_text))
                
                # Toggle button
                toggle_text = "Deactivate" if exam["is_active"] else "Activate"
                toggle_button = QPushButton(toggle_text)
                toggle_button.setObjectName(
                    "danger_button" if exam["is_active"] else "success_button"
                )
                toggle_button.setMinimumHeight(30)
                
                exam_id = exam["id"]
                is_active = exam["is_active"]
                toggle_button.clicked.connect(
                    lambda checked, eid=exam_id, active=is_active: self._toggle_exam_status(eid, not active)
                )
                self.exams_table.setCellWidget(i, 7, toggle_button)
                
        except Exception as error:
            QMessageBox.critical(self, "❌ Error", f"Failed to refresh exams:\n\n{str(error)}")
    
    def _toggle_exam_status(self, exam_id: int, activate: bool):
        """Toggle exam active status"""
        try:
            self.database.execute(
                "UPDATE exams SET is_active = ? WHERE id = ?",
                (1 if activate else 0, exam_id)
            )
            self.database.commit()
            self.database.log_activity(
                f"Exam {'activated' if activate else 'deactivated'}", f"ID: {exam_id}"
            )
            self._refresh_all_data()
        except Exception as error:
            QMessageBox.critical(self, "❌ Error", f"Failed to toggle exam:\n\n{str(error)}")
    
    def _delete_selected_exam(self):
        """Delete selected exam"""
        current_row = self.exams_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "⚠️ Error", "Please select an exam first!")
            return
        
        try:
            exam_id = int(self.exams_table.item(current_row, 0).text())
            exam_title = self.exams_table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self, "⚠️ Confirm Deletion",
                f"Are you sure you want to delete '{exam_title}'?\n\n"
                f"This will permanently delete ALL questions, student results, and assigned tokens.\n\n"
                f"This action CANNOT be undone!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Delete in correct order (respect foreign keys)
                self.database.execute("DELETE FROM assigned_exams WHERE exam_id = ?", (exam_id,))
                self.database.execute("DELETE FROM students WHERE exam_id = ?", (exam_id,))
                self.database.execute("DELETE FROM questions WHERE exam_id = ?", (exam_id,))
                self.database.execute("DELETE FROM exams WHERE id = ?", (exam_id,))
                self.database.commit()
                
                self.database.log_activity("Exam deleted", f"ID: {exam_id}, Title: {exam_title}")
                self._refresh_all_data()
                
                QMessageBox.information(self, "✅ Deleted", f"Exam '{exam_title}' has been deleted.")
                
        except Exception as error:
            QMessageBox.critical(self, "❌ Error", f"Failed to delete exam:\n\n{str(error)}")
    
    def _load_results(self):
        """Load student results for selected exam"""
        exam_id = self.results_exam_combo.currentData()
        if not exam_id:
            self.results_table.setRowCount(0)
            return
        
        try:
            students = self.database.fetch_all(
                "SELECT * FROM students WHERE exam_id = ? ORDER BY percentage DESC",
                (exam_id,)
            )
            
            self.results_table.setRowCount(len(students))
            
            for i, student in enumerate(students):
                self.results_table.setItem(i, 0, QTableWidgetItem(student["name"]))
                self.results_table.setItem(i, 1, QTableWidgetItem(student["student_id"] or "-"))
                self.results_table.setItem(i, 2, QTableWidgetItem(str(student["score"])))
                self.results_table.setItem(i, 3, QTableWidgetItem(str(student["total_points"])))
                
                # Percentage with color coding
                percentage_item = QTableWidgetItem(f"{student['percentage']}%")
                if student["percentage"] >= 80:
                    percentage_item.setForeground(QColor("#3fb950"))
                elif student["percentage"] >= 50:
                    percentage_item.setForeground(QColor("#d29922"))
                else:
                    percentage_item.setForeground(QColor("#f85149"))
                self.results_table.setItem(i, 4, percentage_item)
                
                # Status
                status_text = "✅ Completed" if student["status"] == "completed" else "⏳ Pending"
                if student["needs_review"]:
                    status_text += " 🔍"
                self.results_table.setItem(i, 5, QTableWidgetItem(status_text))
                
                # Manual grading button
                if student["needs_review"]:
                    grade_button = QPushButton("✏️ Grade")
                    grade_button.setMinimumHeight(28)
                    grade_button.setObjectName("success_button")
                    student_id = student["id"]
                    grade_button.clicked.connect(
                        lambda checked, sid=student_id: self._show_manual_grading(sid)
                    )
                    self.results_table.setCellWidget(i, 6, grade_button)
                
                # View answers button
                view_button = QPushButton("👁️ View")
                view_button.setMinimumHeight(28)
                student_id = student["id"]
                student_name = student["name"]
                view_button.clicked.connect(
                    lambda checked, sid=student_id, name=student_name: self._view_student_answers(sid, name)
                )
                self.results_table.setCellWidget(i, 7, view_button)
                
        except Exception as error:
            QMessageBox.critical(self, "❌ Error", f"Failed to load results:\n\n{str(error)}")
    
    def _show_manual_grading(self, student_id: int):
        """Show manual grading dialog for essay/short answer questions"""
        student = self.database.fetch_one("SELECT * FROM students WHERE id = ?", (student_id,))
        if not student:
            return
        
        answers = json.loads(student["answers"]) if student["answers"] else {}
        total_points = student["total_points"]
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Manual Grading - {student['name']}")
        dialog.setFixedSize(580, 480)
        dialog.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        
        # Header
        header_label = QLabel(
            f"<b>Student:</b> {student['name']} | "
            f"<b>Current Score:</b> {student['score']}/{total_points}"
        )
        header_label.setStyleSheet("font-size: 13px; padding: 8px;")
        layout.addWidget(header_label)
        
        # Scrollable question list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(8)
        
        grade_widgets = {}
        for qid, data in answers.items():
            frame = QFrame()
            frame.setFrameStyle(QFrame.Shape.Box)
            frame_layout = QVBoxLayout(frame)
            frame_layout.setSpacing(4)
            
            frame_layout.addWidget(QLabel(f"<b>Question:</b> {data.get('question', 'N/A')}"))
            frame_layout.addWidget(QLabel(f"<b>Student Answer:</b> {data.get('answer', 'No answer')}"))
            frame_layout.addWidget(QLabel(f"<b>Correct Answer:</b> {data.get('correct', 'N/A')}"))
            
            points_spin = QSpinBox()
            points_spin.setRange(0, data.get('max_points', data.get('points', 1)))
            points_spin.setValue(data.get('points', 0))
            points_spin.setPrefix("Points: ")
            frame_layout.addWidget(points_spin)
            
            grade_widgets[qid] = points_spin
            scroll_layout.addWidget(frame)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Save button
        save_button = QPushButton("💾 Save Grades")
        save_button.setObjectName("primary_button")
        save_button.setMinimumHeight(40)
        
        def save_grades():
            new_score = 0
            for qid, data in answers.items():
                if qid in grade_widgets:
                    data['points'] = grade_widgets[qid].value()
                    data['result'] = '✏️ Manually Graded'
                if data.get('result', '') in ['✅ Correct', '✏️ Manually Graded']:
                    new_score += data.get('points', 0)
            
            percentage = (new_score / total_points * 100) if total_points > 0 else 0
            
            self.database.execute(
                "UPDATE students SET score = ?, percentage = ?, answers = ?, needs_review = 0 WHERE id = ?",
                (new_score, round(percentage, 1), json.dumps(answers, ensure_ascii=False), student_id)
            )
            self.database.commit()
            self.database.log_activity("Manual grading completed", f"Student ID: {student_id}")
            
            dialog.accept()
            self._load_results()
            
            QMessageBox.information(
                self, "✅ Graded",
                f"New score: {new_score}/{total_points} ({round(percentage, 1)}%)"
            )
        
        save_button.clicked.connect(save_grades)
        layout.addWidget(save_button)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        
        dialog.exec()
    
    def _view_student_answers(self, student_id: int, student_name: str):
        """View student's detailed answers"""
        student = self.database.fetch_one(
            "SELECT answers FROM students WHERE id = ?", (student_id,)
        )
        
        if not student or not student["answers"]:
            QMessageBox.information(self, "No Data", "No answers available for this student.")
            return
        
        answers = json.loads(student["answers"])
        
        # Build display text
        display_text = f"📝 Student: {student_name}\n{'='*60}\n\n"
        
        for qid, data in answers.items():
            display_text += f"📌 Question: {data.get('question', 'N/A')}\n"
            display_text += f"📋 Type: {data.get('type', 'N/A')}\n"
            display_text += f"✏️ Student Answer: {data.get('answer', 'No answer')}\n"
            display_text += f"✅ Correct Answer: {data.get('correct', 'N/A')}\n"
            display_text += f"📊 Result: {data.get('result', 'N/A')}\n"
            display_text += f"💯 Points: {data.get('points', 0)}/{data.get('max_points', data.get('points', 0))}\n"
            display_text += "-" * 60 + "\n"
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Answers - {student_name}")
        dialog.setFixedSize(620, 480)
        dialog.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(display_text)
        text_edit.setFont(QFont("Consolas", 11))
        layout.addWidget(text_edit)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        
        dialog.exec()
    
    def _assign_exam_to_students(self):
        """Assign exam to students with generated tokens"""
        exam_id = self.assign_exam_combo.currentData()
        if not exam_id:
            QMessageBox.warning(self, "⚠️ Error", "Please select an exam first!")
            return
        
        names_text = self.assign_names_text.toPlainText().strip()
        if not names_text:
            QMessageBox.warning(self, "⚠️ Error", "Please enter student names!")
            return
        
        student_names = [name.strip() for name in names_text.split('\n') if name.strip()]
        if not student_names:
            QMessageBox.warning(self, "⚠️ Error", "No valid student names found!")
            return
        
        # Build accessibility profile
        accessibility_profile = {
            "extra_time": int(self.assign_extra_time_combo.currentText().replace("%", "")),
            "large_font": self.assign_large_font_check.isChecked(),
            "screen_reader": self.assign_screen_reader_check.isChecked()
        }
        
        # Generate tokens
        tokens_generated = 0
        for name in student_names:
            token = f"{name[:3].upper()}{random.randint(1000, 9999)}"
            self.database.execute(
                "INSERT INTO assigned_exams (exam_id, student_name, assigned_token, accessibility_profile) VALUES (?, ?, ?, ?)",
                (exam_id, name, token, json.dumps(accessibility_profile))
            )
            tokens_generated += 1
        
        self.database.commit()
        self.database.log_activity("Tokens generated", f"Exam ID: {exam_id}, Students: {tokens_generated}")
        
        self._refresh_tokens()
        QMessageBox.information(
            self, "✅ Assigned",
            f"Successfully generated {tokens_generated} access tokens for {tokens_generated} students!\n\n"
            f"Students can use their token to access the exam."
        )
    
    def _refresh_tokens(self):
        """Refresh tokens table"""
        exam_id = self.assign_exam_combo.currentData()
        if not exam_id:
            self.tokens_table.setRowCount(0)
            return
        
        tokens = self.database.fetch_all(
            "SELECT * FROM assigned_exams WHERE exam_id = ? ORDER BY created_date DESC",
            (exam_id,)
        )
        
        self.tokens_table.setRowCount(len(tokens))
        
        for i, token in enumerate(tokens):
            self.tokens_table.setItem(i, 0, QTableWidgetItem(token["student_name"]))
            self.tokens_table.setItem(i, 1, QTableWidgetItem(token["assigned_token"]))
            self.tokens_table.setItem(i, 2, QTableWidgetItem("✅ Used" if token["is_used"] else "❌ Not Used"))
            
            # Accessibility info
            a11y = json.loads(token["accessibility_profile"] or '{}')
            a11y_text = ""
            if a11y.get("extra_time"):
                a11y_text += f"⏱️ +{a11y['extra_time']}% "
            if a11y.get("large_font"):
                a11y_text += "🔍 "
            if a11y.get("screen_reader"):
                a11y_text += "🔊 "
            self.tokens_table.setItem(i, 3, QTableWidgetItem(a11y_text or "-"))
    
    def _export_results(self):
        """Export results to CSV file"""
        exam_id = self.results_exam_combo.currentData()
        if not exam_id:
            QMessageBox.warning(self, "⚠️ Error", "Please select an exam first!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results",
            f"exam_results_{exam_id}.csv",
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        try:
            students = self.database.fetch_all(
                "SELECT name, student_id, score, total_points, percentage, status FROM students WHERE exam_id = ? ORDER BY percentage DESC",
                (exam_id,)
            )
            
            with open(file_path, 'w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Student Name", "Student ID", "Score", "Total Points", "Percentage", "Status"])
                
                for student in students:
                    writer.writerow([
                        student["name"],
                        student["student_id"] or "",
                        student["score"],
                        student["total_points"],
                        f"{student['percentage']}%",
                        student["status"]
                    ])
            
            QMessageBox.information(
                self, "✅ Exported",
                f"Results exported successfully to:\n{file_path}"
            )
            
        except Exception as error:
            QMessageBox.critical(self, "❌ Error", f"Failed to export:\n\n{str(error)}")
    
    def _update_server_ip(self):
        """Update server IP display"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip_address = sock.getsockname()[0]
            sock.close()
        except Exception:
            ip_address = "127.0.0.1"
        
        self.server_ip_label.setText(ip_address)
        self.server_url_label.setText(f"http://{ip_address}:8080")
    
    def _start_server(self):
        """Start the quiz web server"""
        if self.server and self.server.is_running:
            return
        
        try:
            self.server = QuizServer(self.database, 8080)
            self.server.start()
            
            self.start_server_button.setEnabled(False)
            self.stop_server_button.setEnabled(True)
            self._update_server_ip()
            
            self.status_bar.showMessage(f"🌐 Server running at {self.server_url_label.text()}")
            self.database.log_activity("Server started")
            
        except Exception as error:
            QMessageBox.critical(self, "❌ Error", f"Failed to start server:\n\n{str(error)}")
    
    def _stop_server(self):
        """Stop the quiz web server"""
        if self.server:
            try:
                self.server.stop()
            except Exception:
                pass
            self.server = None
        
        self.start_server_button.setEnabled(True)
        self.stop_server_button.setEnabled(False)
        self.status_bar.showMessage("⏹️ Server stopped")
        self.database.log_activity("Server stopped")
    
    def _refresh_all_data(self):
        """Refresh all UI data"""
        self._refresh_exams_list()
        self._update_active_exams_list()
        self._update_combo_boxes()
        self._refresh_tokens()
    
    def _update_active_exams_list(self):
        """Update active exams list"""
        self.active_exams_list.clear()
        
        exams = self.database.fetch_all("SELECT * FROM exams WHERE is_active = 1")
        
        for exam in exams:
            student_count = self.database.fetch_one(
                "SELECT COUNT(*) as cnt FROM students WHERE exam_id = ?",
                (exam["id"],)
            )
            count = student_count["cnt"] if student_count else 0
            
            a11y_icon = "♿" if exam["accessibility_enabled"] else ""
            
            self.active_exams_list.addItem(
                f"📋 {exam['title']} {a11y_icon} | 🔑 {exam['password'] or 'None'} | 👨‍🎓 {count} students"
            )
        
        if not exams:
            self.active_exams_list.addItem("No active exams. Activate an exam from the Exams tab.")
    
    def _update_combo_boxes(self):
        """Update combo box selections"""
        for combo_box in [self.results_exam_combo, self.assign_exam_combo]:
            current_data = combo_box.currentData()
            combo_box.blockSignals(True)
            combo_box.clear()
            combo_box.addItem("-- Select Exam --", None)
            
            exams = self.database.fetch_all("SELECT id, title FROM exams ORDER BY created_date DESC")
            for exam in exams:
                combo_box.addItem(exam["title"], exam["id"])
            
            # Restore selection
            for i in range(combo_box.count()):
                if combo_box.itemData(i) == current_data:
                    combo_box.setCurrentIndex(i)
                    break
            
            combo_box.blockSignals(False)
    
    def _show_accessibility_panel(self):
        """Show accessibility settings panel"""
        dialog = QDialog(self)
        dialog.setWindowTitle("♿ Accessibility Settings")
        dialog.setFixedSize(420, 300)
        dialog.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 18, 20, 18)
        
        layout.addWidget(QLabel("<b>Teacher Panel Accessibility</b>"))
        
        # Font size
        font_row = QHBoxLayout()
        font_row.addWidget(QLabel("Font Size:"))
        font_spin = QSpinBox()
        font_spin.setRange(10, 28)
        font_spin.setValue(self.accessibility_settings["font_size"])
        font_spin.setSuffix(" px")
        font_row.addWidget(font_spin)
        layout.addLayout(font_row)
        
        # High contrast
        high_contrast_check = QCheckBox("High Contrast Mode")
        high_contrast_check.setChecked(self.accessibility_settings["high_contrast"])
        layout.addWidget(high_contrast_check)
        
        # Dyslexia font
        dyslexia_check = QCheckBox("Dyslexia-Friendly Font")
        dyslexia_check.setChecked(self.accessibility_settings["dyslexia_font"])
        layout.addWidget(dyslexia_check)
        
        # Apply button
        apply_button = QPushButton("✅ Apply Settings")
        apply_button.setObjectName("primary_button")
        
        def apply_settings():
            self.accessibility_settings["font_size"] = font_spin.value()
            self.accessibility_settings["high_contrast"] = high_contrast_check.isChecked()
            self.accessibility_settings["dyslexia_font"] = dyslexia_check.isChecked()
            
            # Apply font
            if self.accessibility_settings["dyslexia_font"]:
                QApplication.setFont(QFont("Comic Sans MS", self.accessibility_settings["font_size"]))
            else:
                QApplication.setFont(QFont("Segoe UI", self.accessibility_settings["font_size"]))
            
            # Apply theme
            if self.accessibility_settings["high_contrast"]:
                self.theme_engine.set_theme("light")
            else:
                self.theme_engine.set_theme("dark")
            self._apply_theme()
            
            dialog.accept()
            self.status_bar.showMessage("♿ Accessibility settings applied")
        
        apply_button.clicked.connect(apply_settings)
        layout.addWidget(apply_button)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        
        dialog.exec()
    
    def _toggle_theme(self):
        """Toggle between dark and light theme"""
        self.theme_engine.toggle_theme()
        self._apply_theme()
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def _show_help(self):
        """Show help dialog"""
        QMessageBox.information(
            self, "⌨️ Keyboard Shortcuts",
            "<h2>Keyboard Shortcuts</h2>"
            "<ul>"
            "<li><b>Ctrl+1-5</b> - Switch tabs</li>"
            "<li><b>Ctrl+R / F5</b> - Refresh data</li>"
            "<li><b>Ctrl+T</b> - Toggle theme</li>"
            "<li><b>Ctrl+Shift+A</b> - Accessibility panel</li>"
            "<li><b>F11</b> - Fullscreen</li>"
            "<li><b>F1</b> - This help</li>"
            "<li><b>Tab</b> - Navigate between elements</li>"
            "</ul>"
        )
    
    def _show_about_dialog(self):
        """Show about dialog"""
        dialog = AboutDialog(self)
        dialog.exec()
    
    def closeEvent(self, event):
        """Handle application close"""
        # Stop server if running
        if self.server:
            try:
                self.server.stop()
            except Exception:
                pass
        
        # Close database
        try:
            self.database.log_activity("Application closed")
            self.database.close()
        except Exception:
            pass
        
        event.accept()

# ═══════════════════════════════════════════════════════════════════════════
# APPLICATION ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main application entry point"""
    application = QApplication(sys.argv)
    application.setApplicationName(Config.APP_NAME)
    application.setOrganizationName("NETGITS Technologies")
    application.setOrganizationDomain("netgits.com")
    
    # Set application style
    application.setStyle('Fusion')
    
    # Set default font
    application.setFont(QFont("Segoe UI", 12))
    
    try:
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        print(f"🚀 {Config.APP_NAME} v{Config.APP_VERSION}")
        print(f"📋 {Config.APP_TAGLINE}")
        print(f"♿ Full Accessibility Support Enabled")
        print(f"👨‍💻 Developed by {Config.DEV_NAME}")
        print(f"🌐 {Config.WEBSITE}")
        print(f"📧 {Config.EMAIL}")
        print(f"✅ Application started successfully!")
        print(f"💡 Create an exam → Activate it → Start Server → Share URL with students")
        
        sys.exit(application.exec())
        
    except Exception as error:
        QMessageBox.critical(
            None,
            "NETGITS Quiz - Fatal Error",
            f"Failed to start application:\n\n{str(error)}\n\n"
            f"Please check your Python and PyQt6 installation."
        )
        sys.exit(1)

if __name__ == "__main__":
    main()