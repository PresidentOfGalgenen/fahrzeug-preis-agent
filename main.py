from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# ==========================================
# 📊 DATENBANK (Einfache JSON-Datei)
# ==========================================
# Hier speichern wir Feedback, um zu lernen
FEEDBACK_FILE = "feedback_data.json"

def load_feedback():
    """Lädt gespeichertes Feedback aus der Datei"""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_feedback(data):
    """Speichert neues Feedback in der Datei"""
    feedback_list = load_feedback()
    feedback_list.append(data)
    with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
        json.dump(feedback_list, f, indent=2, ensure_ascii=False)

# ==========================================
# 🧠 KI-LOGIK: Preisberechnung
# ==========================================

# Basis-Preise pro Stunde nach Fahrzeugklasse (in EUR)
BASE_PRICES = {
    "Klein": 8.0,      # z.B. VW Polo, Fiat 500
    "Mittel": 12.0,    # z.B. VW Golf, Ford Focus
    "Groß": 18.0,      # z.B. VW Passat, BMW 3er
    "SUV": 22.0,       # z.B. Audi Q5, BMW X3
    "Luxus": 35.0,     # z.B. Mercedes S-Klasse, BMW 7er
    "Transporter": 15.0, # z.B. VW T6, Mercedes Sprinter
    "Sportwagen": 50.0  # z.B. Porsche, Ferrari
}

# Marken-Kategorien (für automatische Klassifizierung)
BRAND_CATEGORIES = {
    "Klein": ["Fiat", "Smart", "Renault Twingo", "Toyota Aygo", "Citroen C1"],
    "Mittel": ["VW Golf", "Ford Focus", "Opel Astra", "Seat Leon", "Skoda Octavia"],
    "Groß": ["VW Passat", "BMW 3er", "Audi A4", "Mercedes C-Klasse"],
    "SUV": ["Audi Q5", "BMW X3", "VW Tiguan", "Volvo XC60"],
    "Luxus": ["Mercedes S-Klasse", "BMW 7er", "Audi A8", "Porsche Panamera"],
    "Transporter": ["VW T6", "Mercedes Sprinter", "Ford Transit"],
    "Sportwagen": ["Porsche 911", "BMW M", "Audi R8", "Ferrari", "Lamborghini"]
}

def detect_category(brand, model):
    """
    Erkennt die Fahrzeugkategorie basierend auf Marke und Modell
    """
    search_term = f"{brand} {model}".lower()
    
    for category, keywords in BRAND_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in search_term:
                return category
    
    # Standard-Kategorie wenn nichts passt
    return "Mittel"

def calculate_price(vehicle_data):
    """
    🧠 Hauptfunktion: Berechnet den Mietpreis
    
    Parameter:
    - brand: Marke (z.B. "BMW")
    - model: Modell (z.B. "3er")
    - year: Baujahr (z.B. 2020)
    - mileage: Kilometerstand (z.B. 45000)
    - condition: Zustand ("Sehr gut", "Gut", "Mittel", "Schlecht")
    - postal_code: PLZ (für regionale Anpassung - später)
    - category: Fahrzeugklasse (optional, wird sonst automatisch erkannt)
    """
    
    # 1. Kategorie bestimmen
    category = vehicle_data.get('category')
    if not category:
        category = detect_category(
            vehicle_data.get('brand', ''),
            vehicle_data.get('model', '')
        )
    
    # 2. Basis-Preis holen
    base_price = BASE_PRICES.get(category, 12.0)
    
    # 3. Alter des Fahrzeugs berechnen
    current_year = datetime.now().year
    vehicle_age = current_year - int(vehicle_data.get('year', current_year))
    
    # 4. Abschreibung pro Jahr (5% bis max. 40%)
    depreciation = min(vehicle_age * 0.05, 0.40)
    price_after_age = base_price * (1 - depreciation)
    
    # 5. Kilometerstand-Faktor
    mileage = int(vehicle_data.get('mileage', 0))
    if mileage < 50000:
        mileage_factor = 1.1  # Bonus für wenig Kilometer
    elif mileage < 100000:
        mileage_factor = 1.0
    elif mileage < 150000:
        mileage_factor = 0.9
    else:
        mileage_factor = 0.8
    
    price_after_mileage = price_after_age * mileage_factor
    
    # 6. Zustandsfaktor
    condition_factors = {
        "Sehr gut": 1.15,
        "Gut": 1.0,
        "Mittel": 0.85,
        "Schlecht": 0.70
    }
    condition = vehicle_data.get('condition', 'Gut')
    condition_factor = condition_factors.get(condition, 1.0)
    
    final_price_per_hour = price_after_mileage * condition_factor
    
    # 7. Tagespreis (6 Stunden = 1 Tag, mit Rabatt)
    price_per_day = final_price_per_hour * 6 * 0.85  # 15% Rabatt für Tagesmiete
    
    # 8. Runde auf 0.50 EUR
    final_price_per_hour = round(final_price_per_hour * 2) / 2
    price_per_day = round(price_per_day * 2) / 2
    
    # 9. Rückgabe mit Details
    return {
        "suggested_price_per_hour": final_price_per_hour,
        "suggested_price_per_day": price_per_day,
        "currency": "EUR",
        "category": category,
        "calculation_details": {
            "base_price": base_price,
            "vehicle_age": vehicle_age,
            "depreciation_percent": round(depreciation * 100, 1),
            "mileage_factor": mileage_factor,
            "condition_factor": condition_factor
        },
        "confidence": "high" if mileage < 100000 and vehicle_age < 5 else "medium"
    }

# ==========================================
# 🌐 API ENDPOINTS
# ==========================================

@app.route('/')
def home():
    """Startseite - zeigt API-Info"""
    return jsonify({
        "service": "Fahrzeug-Preis-Agent",
        "version": "1.0",
        "status": "online",
        "endpoints": {
            "/calculate": "POST - Berechnet Mietpreis",
            "/feedback": "POST - Speichert Feedback",
            "/health": "GET - Health Check"
        },
        "example_request": {
            "url": "/calculate",
            "method": "POST",
            "body": {
                "brand": "BMW",
                "model": "3er",
                "year": 2020,
                "mileage": 45000,
                "condition": "Gut",
                "postal_code": "10115"
            }
        }
    })

@app.route('/calculate', methods=['POST'])
def calculate_endpoint():
    """
    🎯 Hauptendpoint: Berechnet den Preis
    
    Beispiel-Request (JSON):
    {
        "brand": "VW",
        "model": "Golf",
        "year": 2019,
        "mileage": 65000,
        "condition": "Gut",
        "postal_code": "10115"
    }
    """
    try:
        # Daten aus Request holen
        data = request.get_json()
        
        # Validierung
        required_fields = ['brand', 'model', 'year', 'mileage', 'condition']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "error": "Fehlende Pflichtfelder",
                "missing": missing_fields
            }), 400
        
        # Preis berechnen
        result = calculate_price(data)
        
        # Anfrage loggen (für späteres Lernen)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": data,
            "output": result,
            "type": "calculation"
        }
        save_feedback(log_entry)
        
        return jsonify({
            "success": True,
            "data": result,
            "message": "Preis erfolgreich berechnet"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/feedback', methods=['POST'])
def feedback_endpoint():
    """
    📝 Feedback-Endpoint: Nutzer können sagen, ob der Preis gut war
    
    Beispiel-Request:
    {
        "calculation_id": "2024-01-15T10:30:00",
        "actual_price_used": 14.50,
        "user_satisfaction": "good",
        "comment": "Preis war etwas zu hoch"
    }
    """
    try:
        data = request.get_json()
        
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "feedback": data,
            "type": "user_feedback"
        }
        save_feedback(feedback_entry)
        
        return jsonify({
            "success": True,
            "message": "Feedback gespeichert. Danke!"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health Check - prüft ob API läuft"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

# ==========================================
# 🚀 SERVER STARTEN
# ==========================================
if __name__ == '__main__':
    # In Replit automatisch auf Port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
