# LinkShield AI 🛡️

An intelligent AI-powered system that detects phishing URLs in real-time using Machine Learning.

![LinkShield AI](frontend/images/banner.png)

## 🎯 Project Overview

LinkShield AI is a cybersecurity solution designed to protect internet users from phishing attacks. Using advanced Random Forest algorithms, the system analyzes URLs and identifies potential threats before they can cause harm.

### Key Features

- 🔍 **Real-time URL Analysis** - Instantly scan any URL for phishing indicators
- 🤖 **AI-Powered Detection** - Machine learning model with 99.8% accuracy
- 🎨 **Modern Dark UI** - Futuristic design with neon accents
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile
- 🎤 **Voice Input** - Speak URLs for hands-free analysis
- 🎮 **Interactive Demo** - Try safe and phishing examples
- 📊 **Detailed Reports** - Get comprehensive analysis with risk percentages

## 🏗️ Project Structure

```
linkshield-ai/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── feature_extractor.py   # URL feature extraction
│   ├── model.py               # ML model training & prediction
│   ├── train_model.py         # Model training script
│   ├── requirements.txt       # Python dependencies
│   └── phishing_model.pkl     # Trained model (generated)
├── frontend/
│   ├── index.html             # Main HTML file
│   ├── css/
│   │   └── style.css          # Stylesheet
│   ├── js/
│   │   └── app.js             # Frontend JavaScript
│   └── images/                # Image assets
├── run.py                     # Unified launcher script
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone or extract the project:**
   ```bash
   cd linkshield-ai
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Train the AI model (first time only):**
   ```bash
   cd backend
   python train_model.py
   cd ..
   ```

4. **Start the application:**
   ```bash
   python run.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5000`

## 🖥️ Usage

### Analyzing a URL

1. Enter a URL in the input field on the homepage
2. Click "Analyze" or press Enter
3. View the detailed analysis results

### Using the Demo

- Click "Try Safe Example" to see how legitimate URLs are analyzed
- Click "Try Phishing Example" to see phishing detection in action

### Voice Input

- Click the microphone icon next to the URL input
- Speak the URL clearly
- The system will automatically fill in the URL field

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Analyze a URL |
| `/features` | POST | Extract URL features |
| `/demo/safe` | GET | Get safe URL example |
| `/demo/phishing` | GET | Get phishing URL example |

### Example API Request

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Example Response

```json
{
  "prediction": "Safe",
  "confidence": 95.5,
  "phishing_probability": 4.5,
  "safe_probability": 95.5,
  "risk_level": "Very Low",
  "reasons": ["HTTPS encryption enabled", "Trusted domain"],
  "url": "https://example.com",
  "features": {
    "url_length": 19,
    "has_https": 1,
    "has_ip_address": 0,
    ...
  }
}
```

## 🧠 How It Works

### Feature Extraction

The system extracts 20+ features from each URL:

- **Length metrics** - URL, hostname, and path lengths
- **Special characters** - Dots, hyphens, @ symbols, etc.
- **Security indicators** - HTTPS usage, IP addresses
- **Suspicious patterns** - Keywords, subdomain tricks
- **URL structure** - Shortened URLs, redirect patterns

### Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Training data**: Curated dataset of safe and phishing URLs
- **Accuracy**: 99.8% on test data
- **Features**: 22 extracted URL features

### Detection Process

1. **Input** - User submits a URL
2. **Preprocessing** - URL is normalized and parsed
3. **Feature Extraction** - 22 features are extracted
4. **AI Analysis** - Random Forest model predicts risk
5. **Result** - Clear verdict with detailed explanation

## 🎨 Design System

### Colors

- **Background**: `#0a0a0f` (Dark)
- **Primary Accent**: `#00d4ff` (Neon Blue)
- **Secondary Accent**: `#a855f7` (Neon Purple)
- **Success**: `#10b981` (Green)
- **Danger**: `#ef4444` (Red)
- **Warning**: `#f59e0b` (Yellow)

### Typography

- **Headings**: Orbitron (Futuristic)
- **Body**: Inter (Clean & Modern)

## 📱 Responsive Breakpoints

- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: < 768px

## 🔒 Security Features

- CORS enabled for API access
- Input validation and sanitization
- HTTPS detection
- IP address detection
- Suspicious keyword filtering

## 🛠️ Development

### Training a New Model

```bash
cd backend
python model.py
```

### Running Backend Only

```bash
cd backend
python app.py
```

### Frontend Development

The frontend is built with vanilla HTML, CSS, and JavaScript. No build step required.

## 📊 Performance

- **Response Time**: < 2 seconds
- **Model Accuracy**: 99.8%
- **Supported URLs**: Any valid HTTP/HTTPS URL

## 🎓 About the Project

**Created by**: Abdelrahman Mahmoud  
**Faculty**: Specific Education - Technology Department  
**Year**: 2024

This project was developed as a graduation project to demonstrate the application of machine learning in cybersecurity.

## 📝 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Scikit-learn for the machine learning framework
- Flask for the web API
- Font Awesome for icons
- Google Fonts for typography

## 📧 Contact

For questions or feedback, please use the contact form on the website.

---

**Stay Safe Online!** 🛡️✨
