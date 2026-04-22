"""
LinkShield AI - Flask Backend API
Provides endpoints for URL phishing detection and serves frontend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging

from feature_extractor import URLFeatureExtractor, extract_features
from model import load_model, predict_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get paths
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

# For deployment: if frontend folder doesn't exist in parent, use current directory
if not os.path.exists(FRONTEND_DIR):
    FRONTEND_DIR = BACKEND_DIR

# Load the AI model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'phishing_model.pkl')
model = None


def get_model():
    """Lazy load the model"""
    global model
    if model is None:
        logger.info("Loading AI model...")
        model = load_model(MODEL_PATH)
    return model


@app.route('/')
def index():
    """Serve the frontend HTML"""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files"""
    return send_from_directory(os.path.join(FRONTEND_DIR, 'css'), filename)


@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files"""
    return send_from_directory(os.path.join(FRONTEND_DIR, 'js'), filename)


@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve image files"""
    return send_from_directory(os.path.join(FRONTEND_DIR, 'images'), filename)


@app.route('/api')
def api_info():
    """API info endpoint"""
    return jsonify({
        'name': 'LinkShield AI API',
        'version': '1.0.0',
        'description': 'AI-powered phishing URL detection',
        'endpoints': {
            '/predict': 'POST - Analyze a URL for phishing (url parameter)',
            '/health': 'GET - Check API health status',
            '/features': 'POST - Extract features from URL (url parameter)'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        get_model()
        return jsonify({
            'status': 'healthy',
            'model_loaded': True
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint
    
    Request body: {"url": "https://example.com"}
    Response: {"prediction": "Safe|Dangerous", "confidence": 95.5, "reasons": [...]}
    """
    try:
        # Get URL from request
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'Missing URL parameter',
                'message': 'Please provide a URL in the request body: {"url": "https://example.com"}'
            }), 400
        
        url = data['url'].strip()
        
        if not url:
            return jsonify({
                'error': 'Empty URL',
                'message': 'Please provide a valid URL'
            }), 400
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        logger.info(f"Analyzing URL: {url}")
        
        # Get explanation
        extractor = URLFeatureExtractor(url)
        reasons = extractor.get_explanation()
        
        # Make prediction
        model = get_model()
        result = predict_url(model, url)
        
        # Determine status based on prediction and confidence
        prediction = result['prediction']
        confidence = result['confidence']
        phishing_prob = result['phishing_probability']
        
        # Add risk level
        if prediction == 'Dangerous':
            if phishing_prob >= 80:
                risk_level = 'High'
            elif phishing_prob >= 50:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
        else:
            if phishing_prob <= 20:
                risk_level = 'Very Low'
            elif phishing_prob <= 40:
                risk_level = 'Low'
            else:
                risk_level = 'Medium'
        
        response = {
            'prediction': prediction,
            'confidence': confidence,
            'phishing_probability': phishing_prob,
            'safe_probability': result['safe_probability'],
            'risk_level': risk_level,
            'reasons': reasons,
            'url': url,
            'features': extract_features(url)
        }
        
        logger.info(f"Prediction for {url}: {prediction} ({confidence}% confidence)")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/features', methods=['POST'])
def features():
    """
    Extract features from a URL without making a prediction
    
    Request body: {"url": "https://example.com"}
    Response: Feature dictionary
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'Missing URL parameter'
            }), 400
        
        url = data['url'].strip()
        
        if not url:
            return jsonify({
                'error': 'Empty URL'
            }), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        features = extract_features(url)
        
        return jsonify({
            'url': url,
            'features': features
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/demo/safe', methods=['GET'])
def demo_safe():
    """Return a safe URL example for demo"""
    return jsonify({
        'url': 'https://www.google.com',
        'description': 'A legitimate, well-known website'
    })


@app.route('/demo/phishing', methods=['GET'])
def demo_phishing():
    """Return a phishing URL example for demo"""
    return jsonify({
        'url': 'http://192.168.1.1/login@secure-bank.com',
        'description': 'A suspicious URL with IP address and @ symbol'
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Method not allowed',
        'message': 'Please check the HTTP method for this endpoint'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end'
    }), 500


if __name__ == '__main__':
    # Ensure model is trained and saved
    if not os.path.exists(MODEL_PATH):
        logger.info("Model not found. Training new model...")
        from model import train_model, save_model
        model = train_model()
        save_model(model, MODEL_PATH)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
