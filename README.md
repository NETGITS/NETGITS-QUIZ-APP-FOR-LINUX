# 📝 NETGITS QUIZ (Examiner Pro)

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0--beta-blue?style=for-the-badge&logo=github" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-brightgreen?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-PyQt6-orange?style=for-the-badge&logo=qt" alt="Framework">
  <img src="https://img.shields.io/badge/Accessibility-WCAG%20Compliant-purple?style=for-the-badge" alt="Accessibility">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

## 🌟 Overview

**NETGITS QUIZ** (Codename: *Examiner Pro*) is an advanced, high-performance local network examination system built using **Python 3** and **PyQt6**. It features an integrated HTTP server tailored for schools, universities, and training centers to manage and conduct secure exams seamlessly across local area networks (LAN). 

Designed with a high emphasis on **Full Accessibility (A11y)**, it ensures absolute compliance with modern inclusion standards, making digital assessment accessible to everyone, including users with visual, reading, or learning difficulties.

[🌐 Visit Official Website](https://www.netgits.com) | [📧 Support Email](mailto:adam-mahmoud@netgits.com)

---

## ✨ Key Features

### 🖥️ Admin Dashboard (PyQt6-powered Desktop App)
* **Complete Exam Creator:** Supports multiple question types (MCQ, True/False, Short Answer, Essay, Fill in the Blanks).
* **Media-Rich Assessments:** Easily attach images and audio elements to questions, complete with alternative text (`alt_text`) for screen readers.
* **Secure SQLite Engine:** Powered by SQLite with Write-Ahead Logging (WAL) enabled for high concurrency and bulletproof thread safety.
* **Access Token Management:** Generate unique, secure student tokens to lock down exam entry.

### 🌐 Student Examination Portal (Web-based Interface)
* **No Client Installation Required:** Students join instantly via any standard modern web browser over the local network.
* **Built-in Anti-Cheating Suite:** Detects tab-switching, disables right-click, and prevents text copying, cutting, or pasting.
* **Robust Session Auto-Save:** Automatically tracks and safely auto-submits student responses if the exam timer expires.

### ♿ World-Class Accessibility Tools (A11y)
* **Font Scaling & Zooming:** Instant on-the-fly text scaling to fit visual preferences.
* **Contrast Modes:** Toggle high contrast, professional dark theme, or native light styles.
* **Dyslexia-Friendly Typography:** Native mode implementing accessible font spacing.
* **Audio Description Compatibility:** Extra options for extended timers and detailed audio cues.

---

## 🚀 Tech Stack

* **GUI Frontend (Admin):** PyQt6 (Python Bindings for Qt6)
* **Web Portal Backend:** Python Native `http.server` (Zero external heavy dependencies)
* **Database:** SQLite3 with Multi-threading Thread-Locks
* **Web Frontend:** Accessible HTML5, Responsive CSS3, Vanilla JS

---

## 🛠️ Quick Start & Installation

You can download, install dependencies, and run the system using our automated setup scripts.

### 🐧 For Linux & macOS (Bash)
Open your terminal and run this one-liner to automate the entire process:
```bash
curl -sSL [https://raw.githubusercontent.com/NETGITS/netgits-quiz/main/setup.sh](https://raw.githubusercontent.com/NETGITS/netgits-quiz/main/setup.sh) | bash
