/**
 * LinkShield AI - Frontend Application
 * Handles URL analysis, demo functionality, and UI interactions
 */

// API Configuration
// For local development: 'http://localhost:5000'
// For static deployment: '' (uses client-side analysis)
const API_BASE_URL = '';

// DOM Elements
const urlInput = document.getElementById('urlInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const voiceInputBtn = document.getElementById('voiceInputBtn');
const loadingState = document.getElementById('loadingState');
const resultCard = document.getElementById('resultCard');
const trySafeBtn = document.getElementById('trySafeBtn');
const tryPhishingBtn = document.getElementById('tryPhishingBtn');
const demoResult = document.getElementById('demoResult');
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');
const contactForm = document.getElementById('contactForm');
const toastContainer = document.getElementById('toastContainer');

// Scan History
let scanHistory = JSON.parse(localStorage.getItem('linkshield_history')) || [];

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    setupNavigation();
    setupAnalyzer();
    setupDemo();
    setupContactForm();
    setupVoiceInput();
    setupScrollAnimations();
    setupNavbarScroll();
}

// ========== Navigation ==========
function setupNavigation() {
    // Mobile menu toggle
    navToggle?.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        navToggle.innerHTML = navMenu.classList.contains('active') 
            ? '<i class="fas fa-times"></i>' 
            : '<i class="fas fa-bars"></i>';
    });

    // Smooth scroll for nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
                
                // Update active state
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                
                // Close mobile menu
                navMenu.classList.remove('active');
                navToggle.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });
    });

    // Update active nav on scroll
    window.addEventListener('scroll', () => {
        const sections = document.querySelectorAll('section[id]');
        const scrollPos = window.scrollY + 100;

        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');

            if (scrollPos >= top && scrollPos < top + height) {
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });
}

function setupNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ========== URL Analyzer ==========
function setupAnalyzer() {
    analyzeBtn?.addEventListener('click', () => analyzeURL());
    
    urlInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeURL();
        }
    });
}

async function analyzeURL(url = null, isDemo = false) {
    const targetUrl = url || urlInput.value.trim();
    
    if (!targetUrl) {
        showToast('Please enter a URL to analyze', 'error');
        return;
    }

    // Update UI for loading state
    if (!isDemo) {
        analyzeBtn.classList.add('loading');
        resultCard.classList.remove('active');
        loadingState.classList.add('active');
    }

    // Animate loading steps
    animateLoadingSteps();

    try {
        // Simulate processing delay for better UX
        await delay(2000);

        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: targetUrl })
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        const data = await response.json();
        
        if (!isDemo) {
            displayResult(data);
            addToHistory(data);
        }
        
        return data;

    } catch (error) {
        console.error('Analysis error:', error);
        
        // Fallback: Use client-side analysis if server is unavailable
        const fallbackResult = performClientSideAnalysis(targetUrl);
        
        if (!isDemo) {
            displayResult(fallbackResult);
            showToast('Using offline analysis mode', 'info');
        }
        
        return fallbackResult;
    } finally {
        if (!isDemo) {
            analyzeBtn.classList.remove('loading');
            loadingState.classList.remove('active');
        }
    }
}

function animateLoadingSteps() {
    const steps = document.querySelectorAll('.loading-steps .step');
    steps.forEach((step, index) => {
        setTimeout(() => {
            steps.forEach(s => s.classList.remove('active'));
            step.classList.add('active');
            if (index > 0) {
                steps[index - 1].classList.add('completed');
            }
        }, (index + 1) * 600);
    });
}

function displayResult(data) {
    const resultHeader = resultCard.querySelector('.result-header');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultSubtitle = document.getElementById('resultSubtitle');
    const riskPercentage = document.getElementById('riskPercentage');
    const riskBar = document.getElementById('riskBar');
    const reasonsList = document.getElementById('reasonsList');
    const featuresGrid = document.getElementById('featuresGrid');

    // Reset classes
    resultHeader.className = 'result-header';
    riskBar.className = 'meter-fill';

    // Set result based on prediction
    const prediction = data.prediction;
    const confidence = data.confidence;
    const phishingProb = data.phishing_probability;

    if (prediction === 'Safe') {
        resultHeader.classList.add('safe');
        resultIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
        resultTitle.textContent = 'Safe';
        resultSubtitle.textContent = 'No threats detected - This URL appears to be legitimate';
        riskBar.classList.add('safe');
    } else if (phishingProb >= 70) {
        resultHeader.classList.add('dangerous');
        resultIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        resultTitle.textContent = 'Dangerous';
        resultSubtitle.textContent = 'High risk - This URL shows phishing characteristics';
        riskBar.classList.add('dangerous');
    } else {
        resultHeader.classList.add('suspicious');
        resultIcon.innerHTML = '<i class="fas fa-question-circle"></i>';
        resultTitle.textContent = 'Suspicious';
        resultSubtitle.textContent = 'Medium risk - Exercise caution with this URL';
        riskBar.classList.add('suspicious');
    }

    // Update risk meter
    riskPercentage.textContent = `${phishingProb}%`;
    setTimeout(() => {
        riskBar.style.width = `${phishingProb}%`;
    }, 100);

    // Update reasons
    reasonsList.innerHTML = '';
    if (data.reasons && data.reasons.length > 0) {
        data.reasons.forEach(reason => {
            const li = document.createElement('li');
            li.textContent = reason;
            reasonsList.appendChild(li);
        });
    }

    // Update features
    featuresGrid.innerHTML = '';
    if (data.features) {
        const keyFeatures = [
            { key: 'url_length', label: 'URL Length' },
            { key: 'has_https', label: 'HTTPS' },
            { key: 'has_ip_address', label: 'IP Address' },
            { key: 'num_dots', label: 'Dots' },
            { key: 'num_at', label: '@ Symbols' },
            { key: 'is_shortened', label: 'Shortened' }
        ];

        keyFeatures.forEach(({ key, label }) => {
            const value = data.features[key];
            const div = document.createElement('div');
            div.className = 'feature-item';
            div.innerHTML = `
                <span class="feature-name">${label}</span>
                <span class="feature-value">${typeof value === 'boolean' || value === 0 || value === 1 ? (value ? 'Yes' : 'No') : value}</span>
            `;
            featuresGrid.appendChild(div);
        });
    }

    // Show result card
    resultCard.classList.add('active');
    
    // Scroll to result
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Client-side fallback analysis
function performClientSideAnalysis(url) {
    const features = extractClientFeatures(url);
    let score = 0;
    let reasons = [];

    // Calculate risk score
    if (features.url_length > 75) {
        score += 15;
        reasons.push('URL is unusually long');
    }

    if (features.has_ip_address) {
        score += 25;
        reasons.push('Uses IP address instead of domain');
    }

    if (features.num_at > 0) {
        score += 20;
        reasons.push('Contains @ symbol (redirect trick)');
    }

    if (!features.has_https) {
        score += 15;
        reasons.push('No HTTPS encryption');
    }

    if (features.num_dots > 3) {
        score += 10;
        reasons.push('Multiple subdomains (suspicious)');
    }

    if (features.is_shortened) {
        score += 10;
        reasons.push('URL shortening service');
    }

    if (features.has_suspicious_words) {
        score += 15;
        reasons.push('Contains suspicious keywords');
    }

    // Normalize score
    score = Math.min(score, 100);

    let prediction, confidence;
    if (score < 30) {
        prediction = 'Safe';
        confidence = 95 - score;
    } else if (score < 60) {
        prediction = 'Suspicious';
        confidence = 70;
    } else {
        prediction = 'Dangerous';
        confidence = score;
    }

    if (reasons.length === 0) {
        reasons.push('No major red flags detected');
    }

    return {
        prediction,
        confidence,
        phishing_probability: score,
        safe_probability: 100 - score,
        reasons,
        url,
        features
    };
}

function extractClientFeatures(url) {
    const parsed = new URL(url.startsWith('http') ? url : `https://${url}`);
    const fullUrl = url.toLowerCase();

    return {
        url_length: url.length,
        hostname_length: parsed.hostname.length,
        path_length: parsed.pathname.length,
        num_dots: (fullUrl.match(/\./g) || []).length,
        num_hyphens: (fullUrl.match(/-/g) || []).length,
        num_at: (fullUrl.match(/@/g) || []).length,
        num_question_marks: (fullUrl.match(/\?/g) || []).length,
        num_and: (fullUrl.match(/&/g) || []).length,
        num_equal: (fullUrl.match(/=/g) || []).length,
        num_underscores: (fullUrl.match(/_/g) || []).length,
        num_slashes: (fullUrl.match(/\//g) || []).length,
        has_https: parsed.protocol === 'https:',
        has_ip_address: /\b(?:\d{1,3}\.){3}\d{1,3}\b/.test(parsed.hostname),
        has_suspicious_words: /secure|account|login|bank|paypal|verify|update|confirm/i.test(fullUrl),
        is_shortened: /bit\.ly|tinyurl|t\.co|goo\.gl|ow\.ly/i.test(parsed.hostname),
        domain_in_subdomain: false,
        domain_in_path: false,
        path_suspicious: /\.exe$|\.zip$|\.pdf$|redirect/i.test(parsed.pathname)
    };
}

// ========== Demo Section ==========
function setupDemo() {
    trySafeBtn?.addEventListener('click', () => runDemo('safe'));
    tryPhishingBtn?.addEventListener('click', () => runDemo('phishing'));
}

async function runDemo(type) {
    const safeUrl = 'https://www.google.com';
    const phishingUrl = 'http://192.168.1.1/login@secure-bank.com';
    
    const url = type === 'safe' ? safeUrl : phishingUrl;
    
    // Fill input
    urlInput.value = url;
    
    // Scroll to analyzer
    document.getElementById('analyzer').scrollIntoView({ behavior: 'smooth' });
    
    // Show demo animation
    demoResult.classList.add('active');
    
    // Wait a moment then analyze
    await delay(500);
    
    // Perform analysis
    const result = await analyzeURL(url, true);
    
    // Hide demo animation
    demoResult.classList.remove('active');
    
    // Display result
    displayResult(result);
    
    // Show toast
    showToast(
        type === 'safe' 
            ? 'Safe URL detected! No threats found.' 
            : 'Dangerous URL detected! Multiple red flags found.',
        type === 'safe' ? 'success' : 'error'
    );
}

// ========== Voice Input ==========
function setupVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        voiceInputBtn.style.display = 'none';
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    voiceInputBtn?.addEventListener('click', () => {
        if (voiceInputBtn.classList.contains('recording')) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });

    recognition.onstart = () => {
        voiceInputBtn.classList.add('recording');
        showToast('Listening... Speak the URL', 'info');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        // Clean up the transcript
        let cleanedUrl = transcript
            .replace(/\s+/g, '')
            .replace(/dot/g, '.')
            .replace(/slash/g, '/')
            .replace(/colon/g, ':')
            .replace(/at/g, '@');
        
        urlInput.value = cleanedUrl;
        voiceInputBtn.classList.remove('recording');
        showToast('URL captured from voice!', 'success');
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        voiceInputBtn.classList.remove('recording');
        showToast('Voice recognition failed. Please try again.', 'error');
    };

    recognition.onend = () => {
        voiceInputBtn.classList.remove('recording');
    };
}

// ========== Contact Form ==========
function setupContactForm() {
    contactForm?.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(contactForm);
        const name = formData.get('name');
        const email = formData.get('email');
        const message = formData.get('message');
        
        // Simulate form submission
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<div class="spinner"></div> Sending...';
        
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
            contactForm.reset();
            showToast('Message sent successfully! We\'ll get back to you soon.', 'success');
        }, 1500);
    });
}

// ========== Scan History ==========
function addToHistory(data) {
    const entry = {
        url: data.url,
        prediction: data.prediction,
        confidence: data.confidence,
        timestamp: new Date().toISOString()
    };
    
    scanHistory.unshift(entry);
    if (scanHistory.length > 10) {
        scanHistory = scanHistory.slice(0, 10);
    }
    
    localStorage.setItem('linkshield_history', JSON.stringify(scanHistory));
}

// ========== Toast Notifications ==========
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? 'check-circle' : 
                 type === 'error' ? 'exclamation-circle' : 'info-circle';
    const title = type === 'success' ? 'Success' : 
                  type === 'error' ? 'Error' : 'Info';
    
    toast.innerHTML = `
        <i class="fas fa-${icon} toast-icon"></i>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.classList.add('hiding');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// ========== Scroll Animations ==========
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Add fade-in class to elements
    document.querySelectorAll('.section-header, .step-card, .demo-card, .about-stat').forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
}

// ========== Utility Functions ==========
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Make functions globally accessible
window.analyzeURL = analyzeURL;
window.showToast = showToast;
