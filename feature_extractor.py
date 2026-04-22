"""
LinkShield AI - URL Feature Extractor
Extracts features from URLs for phishing detection
"""

import re
from urllib.parse import urlparse


class URLFeatureExtractor:
    """Extract features from URLs for machine learning analysis"""
    
    def __init__(self, url):
        self.url = url.lower()
        self.parsed = urlparse(self.url)
        
    def extract_all_features(self):
        """Extract all features and return as dictionary"""
        features = {
            'url_length': self.get_url_length(),
            'hostname_length': self.get_hostname_length(),
            'path_length': self.get_path_length(),
            'num_dots': self.count_dots(),
            'num_hyphens': self.count_hyphens(),
            'num_at': self.count_at_symbol(),
            'num_question_marks': self.count_question_marks(),
            'num_and': self.count_and_symbol(),
            'num_or': self.count_or_symbol(),
            'num_equal': self.count_equal_symbol(),
            'num_underscores': self.count_underscores(),
            'num_tildes': self.count_tildes(),
            'num_percent': self.count_percent(),
            'num_slashes': self.count_slashes(),
            'num_colons': self.count_colons(),
            'num_digits': self.count_digits(),
            'num_letters': self.count_letters(),
            'has_https': self.has_https(),
            'has_ip_address': self.has_ip_address(),
            'has_suspicious_words': self.has_suspicious_words(),
            'domain_in_subdomain': self.domain_in_subdomain(),
            'domain_in_path': self.domain_in_path(),
            'is_shortened': self.is_shortened_url(),
            'path_suspicious': self.path_has_suspicious_patterns(),
        }
        return features
    
    def get_url_length(self):
        """Get total URL length"""
        return len(self.url)
    
    def get_hostname_length(self):
        """Get hostname length"""
        return len(self.parsed.netloc)
    
    def get_path_length(self):
        """Get path length"""
        return len(self.parsed.path)
    
    def count_dots(self):
        """Count number of dots in URL"""
        return self.url.count('.')
    
    def count_hyphens(self):
        """Count number of hyphens"""
        return self.url.count('-')
    
    def count_at_symbol(self):
        """Count @ symbols (common in phishing)"""
        return self.url.count('@')
    
    def count_question_marks(self):
        """Count ? symbols"""
        return self.url.count('?')
    
    def count_and_symbol(self):
        """Count & symbols"""
        return self.url.count('&')
    
    def count_or_symbol(self):
        """Count | symbols"""
        return self.url.count('|')
    
    def count_equal_symbol(self):
        """Count = symbols"""
        return self.url.count('=')
    
    def count_underscores(self):
        """Count _ symbols"""
        return self.url.count('_')
    
    def count_tildes(self):
        """Count ~ symbols"""
        return self.url.count('~')
    
    def count_percent(self):
        """Count % symbols"""
        return self.url.count('%')
    
    def count_slashes(self):
        """Count / symbols"""
        return self.url.count('/')
    
    def count_colons(self):
        """Count : symbols"""
        return self.url.count(':')
    
    def count_digits(self):
        """Count digits in URL"""
        return sum(c.isdigit() for c in self.url)
    
    def count_letters(self):
        """Count letters in URL"""
        return sum(c.isalpha() for c in self.url)
    
    def has_https(self):
        """Check if URL uses HTTPS"""
        return 1 if self.parsed.scheme == 'https' else 0
    
    def has_ip_address(self):
        """Check if URL contains IP address"""
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        return 1 if re.search(ip_pattern, self.parsed.netloc) else 0
    
    def has_suspicious_words(self):
        """Check for suspicious keywords"""
        suspicious = ['secure', 'account', 'webscr', 'login', 'ebayisapi', 
                      'signin', 'banking', 'confirm', 'paypal', 'verif',
                      'wallet', 'alert', 'protection', 'limited', 'suspend',
                      'verify', 'update', 'security', 'authenticate']
        return 1 if any(word in self.url for word in suspicious) else 0
    
    def domain_in_subdomain(self):
        """Check if brand domains appear in subdomain (phishing technique)"""
        brands = ['paypal', 'google', 'facebook', 'amazon', 'apple', 
                  'microsoft', 'netflix', 'bank', 'wells', 'chase',
                  'citibank', 'amex', 'visa', 'mastercard']
        subdomain = self.parsed.netloc.split('.')[0] if '.' in self.parsed.netloc else ''
        return 1 if any(brand in subdomain and brand != subdomain for brand in brands) else 0
    
    def domain_in_path(self):
        """Check if brand domains appear in path (phishing technique)"""
        brands = ['paypal', 'google', 'facebook', 'amazon', 'apple',
                  'microsoft', 'netflix', 'bank', 'login', 'signin']
        return 1 if any(brand in self.parsed.path for brand in brands) else 0
    
    def is_shortened_url(self):
        """Check if URL uses a shortening service"""
        shorteners = ['bit.ly', 'tinyurl', 't.co', 'goo.gl', 'ow.ly',
                      'buff.ly', 'is.gd', 'short.link', 'rebrand.ly',
                      'cutt.ly', 'shorturl', 'tr.im', 'cli.gs']
        return 1 if any(s in self.parsed.netloc for s in shorteners) else 0
    
    def path_has_suspicious_patterns(self):
        """Check for suspicious path patterns"""
        patterns = [r'\/\d{5,}', r'[?&]redirect=', r'[?&]url=', 
                   r'[?&]return=', r'[?&]next=', r'javascript:',
                   r'data:text\/html', r'\.exe$', r'\.zip$',
                   r'\.pdf$', r'\.docx?$']
        return 1 if any(re.search(p, self.parsed.path, re.I) for p in patterns) else 0
    
    def get_explanation(self):
        """Get human-readable explanation of detected features"""
        reasons = []
        
        if self.get_url_length() > 75:
            reasons.append("URL is unusually long (common in phishing)")
        
        if self.count_at_symbol() > 0:
            reasons.append("Contains @ symbol (can redirect to different site)")
        
        if self.has_ip_address():
            reasons.append("Uses IP address instead of domain name")
        
        if not self.has_https():
            reasons.append("Does not use secure HTTPS connection")
        
        if self.count_dots() > 3:
            reasons.append("Multiple subdomains (suspicious structure)")
        
        if self.has_suspicious_words():
            reasons.append("Contains suspicious keywords (secure, login, bank, etc.)")
        
        if self.domain_in_subdomain():
            reasons.append("Brand name in subdomain (possible impersonation)")
        
        if self.domain_in_path():
            reasons.append("Brand name in path (possible impersonation)")
        
        if self.is_shortened_url():
            reasons.append("URL shortening service (hides real destination)")
        
        if self.path_has_suspicious_patterns():
            reasons.append("Suspicious file extensions or redirect patterns")
        
        if self.count_hyphens() > 2:
            reasons.append("Multiple hyphens in domain name")
        
        return reasons if reasons else ["No major red flags detected"]


def extract_features(url):
    """Convenience function to extract features from a URL"""
    extractor = URLFeatureExtractor(url)
    return extractor.extract_all_features()


def get_url_explanation(url):
    """Get explanation for why a URL might be suspicious"""
    extractor = URLFeatureExtractor(url)
    return extractor.get_explanation()
