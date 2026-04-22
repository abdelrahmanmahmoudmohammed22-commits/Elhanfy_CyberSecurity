#!/usr/bin/env python3
"""
LinkShield AI - Model Training Script
Run this script to train and save the phishing detection model
"""

from model import train_model, save_model

def main():
    print("="*60)
    print("LinkShield AI - Model Training")
    print("="*60)
    
    # Train the model
    model = train_model()
    
    # Save the model
    save_model(model, 'phishing_model.pkl')
    
    print("\n" + "="*60)
    print("Training complete! Model saved to phishing_model.pkl")
    print("="*60)

if __name__ == '__main__':
    main()
