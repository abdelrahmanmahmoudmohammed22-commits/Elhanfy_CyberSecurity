"""
LinkShield AI - Machine Learning Model
Trains and saves a Random Forest classifier for phishing detection
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os

from feature_extractor import URLFeatureExtractor


def generate_training_data():
    """
    Generate training data for the phishing detection model.
    In a real scenario, this would use a dataset of known phishing and legitimate URLs.
    For this demo, we'll create synthetic data based on known patterns.
    """
    
    # Safe URLs - legitimate websites
    safe_urls = [
        "https://www.google.com",
        "https://www.youtube.com",
        "https://www.facebook.com",
        "https://www.amazon.com",
        "https://www.wikipedia.org",
        "https://www.twitter.com",
        "https://www.instagram.com",
        "https://www.linkedin.com",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.reddit.com",
        "https://www.netflix.com",
        "https://www.apple.com",
        "https://www.microsoft.com",
        "https://www.adobe.com",
        "https://www.spotify.com",
        "https://www.whatsapp.com",
        "https://www.telegram.org",
        "https://www.zoom.us",
        "https://www.slack.com",
        "https://www.dropbox.com",
        "https://www.medium.com",
        "https://www.quora.com",
        "https://www.twitch.tv",
        "https://www.discord.com",
        "https://www.pinterest.com",
        "https://www.tumblr.com",
        "https://www.flickr.com",
        "https://www.vimeo.com",
        "https://www.soundcloud.com",
        "https://www.behance.net",
        "https://www.dribbble.com",
        "https://www.figma.com",
        "https://www.notion.so",
        "https://www.trello.com",
        "https://www.asana.com",
        "https://www.monday.com",
        "https://www.salesforce.com",
        "https://www.hubspot.com",
        "https://www.mailchimp.com",
        "https://www.shopify.com",
        "https://www.etsy.com",
        "https://www.ebay.com",
        "https://www.aliexpress.com",
        "https://www.walmart.com",
        "https://www.target.com",
        "https://www.bestbuy.com",
        "https://www.costco.com",
        "https://www.homedepot.com",
        "https://www.lowes.com",
        "https://www.ikea.com",
        "https://www.nike.com",
        "https://www.adidas.com",
        "https://www.zara.com",
        "https://www.hm.com",
        "https://www.gap.com",
        "https://www.macys.com",
        "https://www.nordstrom.com",
        "https://www.sephora.com",
        "https://www.ulta.com",
        "https://www.cvs.com",
        "https://www.walgreens.com",
        "https://www.riteaid.com",
        "https://www.kroger.com",
        "https://www.safeway.com",
        "https://www.wholefoodsmarket.com",
        "https://www.traderjoes.com",
        "https://www.sprouts.com",
        "https://www.publix.com",
        "https://www.wegmans.com",
        "https://www.heb.com",
        "https://www.hy-vee.com",
        "https://www.meijer.com",
        "https://www.gianteagle.com",
        "https://www.stopandshop.com",
        "https://www.hannaford.com",
        "https://www.shaws.com",
        "https://www.marketbasket.com",
        "https://www.bigy.com",
        "https://www.pricechopper.com",
        "https://www.topsmarkets.com",
        "https://www.weismarkets.com",
        "https://www.foodlion.com",
        "https://www.harristeeter.com",
        "https://www.lowesfoods.com",
        "https://www.bi-lo.com",
        "https://www.winn-dixie.com",
        "https://www.frescoymas.com",
        "https://www.elsupermarkets.com",
        "https://www.northgatemarket.com",
        "https://www.vallartasupermarkets.com",
        "https://www.cardenasmarkets.com",
        "https://www.superior-grocers.com",
        "https://www.food4less.com",
        "https://www.foods-co.com",
        "https://www.ralphs.com",
        "https://www.frysfood.com",
        "https://www.kingsoopers.com",
        "https://www.citymarket.com",
        "https://www.dillons.com",
        "https://www.bakersplus.com",
        "https://www.gerbes.com",
        "https://www.pay-less.com",
        "https://www.owensmarket.com",
        "https://www.scottsfoods.com",
        "https://www.jaycfoods.com",
        "https://www.kwikshop.com",
        "https://www.turkeyhillstores.com",
        "https://www.loafnjug.com",
        "https://www.quikstop.com",
        "https://www.tomthumb.com",
        "https://www.randalls.com",
        "https://www.pavilions.com",
        "https://www.vons.com",
        "https://www.albertsons.com",
        "https://www.safeway.com",
        "https://www.carrsqc.com",
        "https://www.acmemarkets.com",
        "https://www.jewelosco.com",
        "https://www.shaws.com",
        "https://www.starmarket.com",
        "https://www.haggen.com",
    ]
    
    # Phishing URLs - suspicious patterns
    phishing_urls = [
        "http://192.168.1.1/login@secure-paypal.com",
        "http://paypal.com.secure-login.xyz/verify",
        "http://secure-bank-login.tk/auth",
        "http://google.com.phishing-site.ru/search",
        "http://facebook-security-alert.ml/login",
        "http://amazon-account-verify.cf/signin",
        "http://apple-id-confirm.ga/verify",
        "http://microsoft-security-update.gq/auth",
        "http://netflix-billing-issue.ga/login",
        "http://chase-online-banking.tk/secure",
        "http://wellsfargo-account-verify.ml/signin",
        "http://citibank-secure-login.ga/auth",
        "http://bankofamerica-security.cf/verify",
        "http://usbank-account-update.tk/login",
        "http://pnc-online-banking.ga/secure",
        "http://capitalone-verify.ml/signin",
        "http://discover-card-secure.ga/auth",
        "http://amex-account-verify.cf/login",
        "http://visa-secure-confirmation.tk/verify",
        "http://mastercard-security-update.ga/auth",
        "http://paypal-secure-center.ml/signin",
        "http://ebay-account-suspend.ga/verify",
        "http://apple-icloud-locked.cf/unlock",
        "http://google-drive-share.tk/download",
        "http://dropbox-document-shared.ga/view",
        "http://onedrive-file-share.ml/download",
        "http://icloud-find-my-iphone.ga/track",
        "http://yahoo-mail-security.tk/verify",
        "http://outlook-account-update.ga/login",
        "http://gmail-security-alert.ml/auth",
        "http://hotmail-verify-account.cf/signin",
        "http://aol-mail-security.tk/confirm",
        "http://zoom-meeting-invite.ga/join",
        "http://teams-microsoft-update.ml/login",
        "http://slack-workspace-invite.cf/join",
        "http://discord-nitro-free.ga/claim",
        "http://steam-gift-card-free.ml/redeem",
        "http://epic-games-free-vbucks.ga/claim",
        "http://robux-generator-free.cf/generate",
        "http://bitcoin-wallet-verify.tk/login",
        "http://coinbase-account-secure.ga/auth",
        "http://binance-security-update.ml/verify",
        "http://kraken-login-secure.cf/signin",
        "http://blockchain-wallet-recover.ga/restore",
        "http://crypto-exchange-bonus.tk/claim",
        "http://nft-mint-free.ml/mint",
        "http://opensea-secure-login.ga/auth",
        "http://metamask-wallet-verify.cf/confirm",
        "http://trust-wallet-backup.ga/restore",
        "http://ledger-live-update.ml/download",
        "http://trezor-wallet-setup.ga/install",
        "http://amazon-prime-renew.tk/update",
        "http://hulu-subscription-verify.ga/confirm",
        "http://disney-plus-billing.ml/update",
        "http://hbo-max-payment-issue.cf/fix",
        "http://spotify-premium-free.ga/claim",
        "http://youtube-premium-offer.tk/activate",
        "http://twitch-prime-loot.ml/claim",
        "http://playstation-plus-free.ga/redeem",
        "http://xbox-game-pass-free.cf/claim",
        "http://nintendo-switch-online.tk/free",
        "http://steam-free-games.ga/download",
        "http://origin-ea-free-games.ml/claim",
        "http://ubisoft-free-games.cf/download",
        "http://gog-free-games.ga/claim",
        "http://itch-io-free-bundle.tk/download",
        "http://humble-bundle-free.ml/redeem",
        "http://fanatical-free-games.ga/claim",
        "http://green-man-gaming.cf/free",
        "http://cdkeys-discount.tk/buy",
        "http://g2a-cheap-keys.ml/purchase",
        "http://kinguin-discount.ga/shop",
        "http://gamivo-cheap.cf/buy",
        "http://eneba-discount.tk/shop",
        "http://instant-gaming-free.ga/claim",
        "http://dlgamer-sale.ml/buy",
        "http://gamesplanet-discount.cf/shop",
        "http://direct2drive-sale.ga/buy",
        "http://gamebillet-discount.tk/shop",
        "http://voidu-cheap-keys.ml/purchase",
        "http://mmoga-discount.ga/shop",
        "http://hrk-game-cheap.cf/buy",
        "http://gamersgate-sale.tk/shop",
        "http://indiegala-free.ga/claim",
        "http://wingamestore-discount.ml/buy",
        "http://macgamestore-sale.cf/shop",
        "http://amazon-free-prime.ga/claim",
        "http://walmart-gift-card-free.tk/redeem",
        "http://target-redcard-update.ml/verify",
        "http://costco-membership-renew.ga/confirm",
        "http://bestbuy-reward-zone.cf/activate",
        "http://home-depot-credit.tk/apply",
        "http://lowes-credit-card.ml/apply",
        "http://ikea-family-update.ga/verify",
        "http://nike-membership-free.cf/join",
        "http://adidas-confirmed-app.ga/download",
        "http://zara-sale-exclusive.tk/shop",
        "http://hm-member-discount.ml/activate",
        "http://gap-credit-card.ga/apply",
        "http://macys-credit-card.cf/apply",
        "http://nordstrom-card-apply.tk/apply",
        "http://sephora-beauty-insider.ml/update",
        "http://ulta-rewards-activate.ga/activate",
        "http://cvs-extra-care.cf/update",
        "http://walgreens-balance-rewards.tk/verify",
        "http://rite-aid-wellness.ml/update",
        "http://kroger-plus-card.ga/activate",
        "http://safeway-club-card.cf/update",
        "http://whole-foods-prime.tk/activate",
        "http://trader-joes-newsletter.ml/signup",
        "http://sprouts-app-download.ga/download",
    ]
    
    # Generate features for all URLs
    data = []
    
    # Safe URLs (label = 0)
    for url in safe_urls:
        try:
            extractor = URLFeatureExtractor(url)
            features = extractor.extract_all_features()
            features['label'] = 0  # Safe
            data.append(features)
        except:
            continue
    
    # Phishing URLs (label = 1)
    for url in phishing_urls:
        try:
            extractor = URLFeatureExtractor(url)
            features = extractor.extract_all_features()
            features['label'] = 1  # Phishing
            data.append(features)
        except:
            continue
    
    return pd.DataFrame(data)


def train_model():
    """Train the Random Forest model"""
    print("Generating training data...")
    df = generate_training_data()
    
    # Prepare features and labels
    X = df.drop('label', axis=1)
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Phishing']))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nTop 10 Important Features:")
    print(feature_importance.head(10))
    
    return model


def save_model(model, filepath='phishing_model.pkl'):
    """Save the trained model to a pickle file"""
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {filepath}")


def load_model(filepath='phishing_model.pkl'):
    """Load the trained model from a pickle file"""
    if not os.path.exists(filepath):
        print("Model file not found. Training new model...")
        model = train_model()
        save_model(model, filepath)
        return model
    
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    print(f"Model loaded from {filepath}")
    return model


def predict_url(model, url):
    """Predict if a URL is phishing or safe"""
    extractor = URLFeatureExtractor(url)
    features = extractor.extract_all_features()
    
    # Convert to DataFrame with same column order as training
    feature_df = pd.DataFrame([features])
    
    # Get prediction and probability
    prediction = model.predict(feature_df)[0]
    probabilities = model.predict_proba(feature_df)[0]
    
    # Get confidence score
    confidence = max(probabilities) * 100
    
    return {
        'prediction': 'Dangerous' if prediction == 1 else 'Safe',
        'confidence': round(confidence, 2),
        'phishing_probability': round(probabilities[1] * 100, 2),
        'safe_probability': round(probabilities[0] * 100, 2)
    }


if __name__ == '__main__':
    # Train and save the model
    model = train_model()
    save_model(model)
    
    # Test predictions
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/login@secure-paypal.com",
        "https://github.com",
        "http://paypal.com.secure-login.xyz/verify"
    ]
    
    print("\n" + "="*50)
    print("Testing predictions:")
    print("="*50)
    
    for url in test_urls:
        result = predict_url(model, url)
        print(f"\nURL: {url}")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']}%")
