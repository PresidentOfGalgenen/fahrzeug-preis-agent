# main_LEARNING.py
# Base44 Pricing Agent mit intelligentem Lern-System

from flask import Flask, request, jsonify
from flask_cors import CORS
from vehicle_database import VEHICLE_DATABASE, BASE_HOURLY_RATES
from datetime import datetime
import math
import json
import os

app = Flask(__name__)
CORS(app)

# ========================================
# FEEDBACK STORAGE
# ========================================

FEEDBACK_FILE = 'feedback_data.json'
LEARNING_ADJUSTMENTS_FILE = 'learning_adjustments.json'

def load_feedback():
    """Lade alle Feedback-Daten"""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_feedback(feedback_data):
    """Speichere neues Feedback"""
    feedbacks = load_feedback()
    feedbacks.append(feedback_data)
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedbacks, f, indent=2)
    return feedbacks

def load_adjustments():
    """Lade gelernte Anpassungen"""
    if os.path.exists(LEARNING_ADJUSTMENTS_FILE):
        with open(LEARNING_ADJUSTMENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_adjustments(adjustments):
    """Speichere gelernte Anpassungen"""
    with open(LEARNING_ADJUSTMENTS_FILE, 'w') as f:
        json.dump(adjustments, f, indent=2)

# ========================================
# STANDARD MULTIPLIERS
# ========================================

DEPRECIATION_RATES = {
    0: 1.0,
    1: 0.85,
    2: 0.75,
    3: 0.68,
    5: 0.55,
    7: 0.45,
    10: 0.35,
    15: 0.25,
    20: 0.20
}

CONDITION_MULTIPLIERS = {
    "Einwandfrei": 1.15,
    "Sehr gut": 1.0,
    "Gut": 0.85,
    "Akzeptabel": 0.70
}

BODY_STYLE_BONUSES = {
    "Cabrio": 1.15,
    "Roadster": 1.15,
    "Coupé": 1.08,
    "SUV-Coupé": 1.05,
    "SUV": 1.02,
    "Kombi": 0.98,
    "Van": 0.95,
    "Limousine": 1.0
}

# ========================================
# LERN-ALGORITHMUS
# ========================================

def analyze_feedback(feedback_data):
    """
    Analysiere Feedback und berechne Anpassungen
    
    Returns:
        Dict mit Anpassungsvorschlägen
    """
    feedback_type = feedback_data.get('feedback')
    calculated_price = feedback_data.get('calculated_price')
    correct_price = feedback_data.get('correct_price')
    
    vehicle_key = f"{feedback_data['brand']}_{feedback_data['model']}"
    
    adjustments = {}
    
    if feedback_type == 'perfect':
        # Preis war perfekt - keine Anpassung nötig
        adjustments['confidence_boost'] = 0.02  # Erhöhe Confidence
        adjustments['multiplier_adjustment'] = 1.0
        
    elif feedback_type == 'too_high' and correct_price:
        # Preis war zu hoch
        deviation = (calculated_price - correct_price) / calculated_price
        adjustment_factor = 1 - (deviation * 0.5)  # 50% der Abweichung korrigieren
        adjustments['multiplier_adjustment'] = max(0.8, adjustment_factor)
        adjustments['reason'] = f"Preis war {deviation*100:.1f}% zu hoch"
        
    elif feedback_type == 'too_low' and correct_price:
        # Preis war zu niedrig
        deviation = (correct_price - calculated_price) / calculated_price
        adjustment_factor = 1 + (deviation * 0.5)  # 50% der Abweichung korrigieren
        adjustments['multiplier_adjustment'] = min(1.2, adjustment_factor)
        adjustments['reason'] = f"Preis war {deviation*100:.1f}% zu niedrig"
        
    elif feedback_type == 'wrong' and correct_price:
        # Preis war komplett falsch
        deviation = abs(correct_price - calculated_price) / calculated_price
        if correct_price > calculated_price:
            adjustment_factor = 1 + (deviation * 0.3)  # Vorsichtige Korrektur
            adjustments['multiplier_adjustment'] = min(1.3, adjustment_factor)
        else:
            adjustment_factor = 1 - (deviation * 0.3)
            adjustments['multiplier_adjustment'] = max(0.7, adjustment_factor)
        adjustments['reason'] = "Komplette Neuberechnung basierend auf Feedback"
    
    adjustments['vehicle_key'] = vehicle_key
    adjustments['feedback_count'] = 1
    adjustments['last_updated'] = datetime.now().isoformat()
    
    return adjustments

def apply_learning_adjustments(vehicle, base_price):
    """
    Wende gelernte Anpassungen auf Preisberechnung an
    """
    adjustments = load_adjustments()
    vehicle_key = f"{vehicle['brand']}_{vehicle['model']}"
    
    if vehicle_key in adjustments:
        adj = adjustments[vehicle_key]
        multiplier = adj.get('multiplier_adjustment', 1.0)
        feedback_count = adj.get('feedback_count', 0)
        
        # Gewichte Anpassung basierend auf Anzahl Feedbacks
        # Je mehr Feedback, desto stärker die Anpassung
        weight = min(1.0, feedback_count / 10)  # Max bei 10 Feedbacks
        
        adjusted_multiplier = 1.0 + ((multiplier - 1.0) * weight)
        
        return base_price * adjusted_multiplier, {
            'learning_applied': True,
            'adjustment_factor': adjusted_multiplier,
            'feedback_count': feedback_count,
            'reason': adj.get('reason', 'Gelernt aus Feedback')
        }
    
    return base_price, {
        'learning_applied': False,
        'feedback_count': 0
    }

def update_learning_model(feedback_data):
    """
    Aktualisiere das Lernmodell mit neuem Feedback
    """
    # Analysiere Feedback
    new_adjustments = analyze_feedback(feedback_data)
    
    if not new_adjustments.get('multiplier_adjustment'):
        return None
    
    # Lade bestehende Anpassungen
    adjustments = load_adjustments()
    vehicle_key = new_adjustments['vehicle_key']
    
    if vehicle_key in adjustments:
        # Merge mit bestehenden Anpassungen
        existing = adjustments[vehicle_key]
        
        # Berechne gewichteten Durchschnitt
        existing_count = existing.get('feedback_count', 0)
        new_count = existing_count + 1
        
        existing_multiplier = existing.get('multiplier_adjustment', 1.0)
        new_multiplier = new_adjustments['multiplier_adjustment']
        
        # Gewichteter Durchschnitt
        combined_multiplier = (
            (existing_multiplier * existing_count + new_multiplier) / 
            (existing_count + 1)
        )
        
        adjustments[vehicle_key] = {
            'multiplier_adjustment': combined_multiplier,
            'feedback_count': new_count,
            'last_updated': datetime.now().isoformat(),
            'reason': new_adjustments.get('reason', 'Gelernt aus Feedback')
        }
    else:
        # Neue Anpassung
        adjustments[vehicle_key] = new_adjustments
    
    # Speichere
    save_adjustments(adjustments)
    
    return adjustments[vehicle_key]

# ========================================
# HELPER FUNCTIONS
# ========================================

def get_depreciation_factor(age):
    for year_threshold in sorted(DEPRECIATION_RATES.keys(), reverse=True):
        if age >= year_threshold:
            return DEPRECIATION_RATES[year_threshold]
    return 1.0

def find_vehicle(brand, model):
    for vehicle in VEHICLE_DATABASE:
        if vehicle["brand"].lower() == brand.lower() and vehicle["model"].lower() == model.lower():
            return vehicle
    return None

def calculate_confidence(vehicle, year, condition, learning_info):
    """Confidence mit Learning-Boost"""
    score = 100
    current_year = datetime.now().year
    age = current_year - year
    
    if age > 15:
        score -= 20
    elif age > 10:
        score -= 10
    
    if condition == "Akzeptabel":
        score -= 15
    elif condition == "Gut":
        score -= 5
    
    if vehicle["category"] in ["Supersportwagen", "Luxuslimousine"]:
        score += 10
    
    # Learning Boost
    if learning_info.get('learning_applied'):
        feedback_count = learning_info.get('feedback_count', 0)
        boost = min(15, feedback_count * 1.5)  # Max +15% für 10+ Feedbacks
        score += boost
    
    return max(0, min(100, score))

# ========================================
# PRICING CALCULATION (MIT LEARNING)
# ========================================

def calculate_price(brand, model, year, condition):
    """Preisberechnung MIT Lern-Algorithmus"""
    vehicle = find_vehicle(brand, model)
    
    if not vehicle:
        return None
    
    # Baujahr-Validierung
    if 'year_start' in vehicle and 'year_end' in vehicle:
        if year < vehicle['year_start'] or year > vehicle['year_end']:
            return None
    
    category = vehicle["category"]
    base_rate = BASE_HOURLY_RATES.get(category, 15.0)
    
    current_year = datetime.now().year
    age = max(0, current_year - year)
    
    # Standard Faktoren
    depreciation = get_depreciation_factor(age)
    condition_factor = CONDITION_MULTIPLIERS.get(condition, 0.85)
    
    new_price = vehicle["new_price"]
    price_multiplier = 1.0
    if new_price > 200000:
        price_multiplier = 1.5
    elif new_price > 100000:
        price_multiplier = 1.3
    elif new_price > 50000:
        price_multiplier = 1.1
    
    hp = vehicle.get("hp", 150)
    hp_factor = 1.0 + ((hp - 150) / 1000)
    
    body_style = vehicle.get("body_style", "Limousine")
    body_bonus = BODY_STYLE_BONUSES.get(body_style, 1.0)
    
    is_electric = vehicle.get("engine_displacement", 0) == 0
    electric_bonus = 1.1 if is_electric else 1.0
    
    rarity_bonus = 1.0
    if category in ["Supersportwagen", "Hypersportwagen"]:
        rarity_bonus = 1.2
    elif category == "Luxuslimousine":
        rarity_bonus = 1.1
    
    custom_rarity = vehicle.get("rarity_multiplier", 1.0)
    demand_factor = vehicle.get("demand_factor", 1.0)
    premium_package_bonus = 1.15 if vehicle.get("premium_package", False) else 1.0
    facelift_bonus = 1.05 if vehicle.get("facelift", False) else 1.0
    
    # BASISPREIS berechnen
    base_hourly_price = (
        base_rate * 
        depreciation * 
        condition_factor *
        price_multiplier * 
        hp_factor * 
        body_bonus * 
        electric_bonus * 
        rarity_bonus *
        custom_rarity *
        demand_factor *
        premium_package_bonus *
        facelift_bonus
    )
    
    # *** LERN-ALGORITHMUS ANWENDEN ***
    hourly_price, learning_info = apply_learning_adjustments(vehicle, base_hourly_price)
    
    hourly_price = round(hourly_price * 2) / 2
    
    daily_price = hourly_price * 8 * 0.8
    weekly_price = daily_price * 7 * 0.7
    
    confidence = calculate_confidence(vehicle, year, condition, learning_info)
    
    if confidence >= 90:
        confidence_label = "sehr hoch"
    elif confidence >= 75:
        confidence_label = "hoch"
    elif confidence >= 60:
        confidence_label = "mittel"
    else:
        confidence_label = "niedrig"
    
    return {
        "suggested_price_per_hour": hourly_price,
        "suggested_price_per_day": daily_price,
        "suggested_price_per_week": weekly_price,
        "vehicle_info": {
            "matched_vehicle": f"{vehicle['brand']} {vehicle['model']}",
            "category": category,
            "segment": vehicle.get("segment", "N/A"),
            "body_style": body_style,
            "new_price": new_price,
            "hp": hp,
            "engine_displacement": vehicle.get("engine_displacement", "N/A")
        },
        "calculation_details": {
            "base_rate": base_rate,
            "depreciation_factor": depreciation,
            "condition_factor": condition_factor,
            "age_years": age,
            "learning_info": learning_info,
            "note": "Preis wurde durch Lern-Algorithmus optimiert" if learning_info.get('learning_applied') else "Standard-Berechnung"
        },
        "confidence_score": confidence,
        "confidence": confidence_label
    }

# ========================================
# API ROUTES
# ========================================

@app.route('/')
def home():
    adjustments = load_adjustments()
    feedbacks = load_feedback()
    
    return jsonify({
        "message": "Base44 Fahrzeugpreis-Agent mit Lern-System",
        "version": "2.2-LEARNING",
        "learning_stats": {
            "total_feedback": len(feedbacks),
            "learned_vehicles": len(adjustments),
            "total_adjustments": sum(adj.get('feedback_count', 0) for adj in adjustments.values())
        },
        "endpoints": {
            "POST /calculate": "Berechne Mietpreis (mit Learning)",
            "POST /feedback": "Sende Feedback zum Lernen",
            "GET /learning-stats": "Zeige Lern-Statistiken",
            "GET /vehicles": "Liste aller Fahrzeuge",
            "GET /brands": "Liste aller Marken",
            "GET /models?brand=X": "Modelle einer Marke",
            "GET /health": "Health Check"
        }
    })

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    try:
        if request.method == 'GET':
            brand = request.args.get('brand')
            model = request.args.get('model')
            year = request.args.get('year', type=int)
            condition = request.args.get('condition', 'Gut')
        else:
            data = request.get_json()
            required_fields = ['brand', 'model', 'year', 'condition']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        "success": False,
                        "error": f"Fehlendes Feld: {field}"
                    }), 400
            
            brand = data['brand']
            model = data['model']
            year = data['year']
            condition = data['condition']
        
        result = calculate_price(brand, model, year, condition)
        
        if result is None:
            return jsonify({
                "success": False,
                "error": "Fahrzeug nicht gefunden oder Baujahr nicht verfügbar"
            }), 404
        
        return jsonify({
            "success": True,
            "hourly": result["suggested_price_per_hour"],
            "daily": result["suggested_price_per_day"],
            "weekly": result["suggested_price_per_week"],
            "confidence": result["confidence_score"],
            "confidence_label": result["confidence"],
            "vehicle_info": result["vehicle_info"],
            "calculation_details": result["calculation_details"]
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Empfange Feedback und aktualisiere Lernmodell
    
    Expected JSON:
    {
        "brand": "BMW",
        "model": "3er",
        "year": 2020,
        "condition": "Sehr gut",
        "feedback": "too_high" | "too_low" | "perfect" | "wrong",
        "calculated_price": 25.0,
        "correct_price": 22.0 (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Speichere Feedback
        feedback_data = {
            **data,
            'timestamp': datetime.now().isoformat(),
            'id': len(load_feedback()) + 1
        }
        save_feedback(feedback_data)
        
        # Aktualisiere Lernmodell
        adjustment_result = update_learning_model(feedback_data)
        
        return jsonify({
            "success": True,
            "message": "Feedback gespeichert und Modell aktualisiert",
            "learning_update": adjustment_result
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/learning-stats', methods=['GET'])
def learning_stats():
    """Zeige detaillierte Lern-Statistiken"""
    feedbacks = load_feedback()
    adjustments = load_adjustments()
    
    # Analysiere Feedback-Typen
    feedback_types = {}
    for fb in feedbacks:
        fb_type = fb.get('feedback', 'unknown')
        feedback_types[fb_type] = feedback_types.get(fb_type, 0) + 1
    
    # Top angepasste Fahrzeuge
    top_learned = sorted(
        adjustments.items(),
        key=lambda x: x[1].get('feedback_count', 0),
        reverse=True
    )[:10]
    
    return jsonify({
        "success": True,
        "stats": {
            "total_feedback": len(feedbacks),
            "learned_vehicles": len(adjustments),
            "feedback_by_type": feedback_types,
            "total_adjustments": sum(adj.get('feedback_count', 0) for adj in adjustments.values()),
            "top_learned_vehicles": [
                {
                    "vehicle": key.replace('_', ' '),
                    "feedback_count": adj.get('feedback_count', 0),
                    "adjustment_factor": adj.get('multiplier_adjustment', 1.0),
                    "last_updated": adj.get('last_updated')
                }
                for key, adj in top_learned
            ]
        }
    })

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify({
        "success": True,
        "count": len(VEHICLE_DATABASE),
        "vehicles": VEHICLE_DATABASE
    })

@app.route('/brands', methods=['GET'])
def get_brands():
    brands = sorted(set(v["brand"] for v in VEHICLE_DATABASE))
    return jsonify({
        "success": True,
        "count": len(brands),
        "brands": brands
    })

@app.route('/models', methods=['GET'])
def get_models():
    brand = request.args.get('brand')
    if not brand:
        return jsonify({
            "success": False,
            "error": "Parameter 'brand' fehlt"
        }), 400
    
    models = sorted(set(
        v["model"] for v in VEHICLE_DATABASE 
        if v["brand"].lower() == brand.lower()
    ))
    
    return jsonify({
        "success": True,
        "brand": brand,
        "count": len(models),
        "models": models
    })

@app.route('/models/<brand>', methods=['GET'])
def get_models_by_path(brand):
    models = sorted(set(
        v["model"] for v in VEHICLE_DATABASE 
        if v["brand"].lower() == brand.lower()
    ))
    
    return jsonify({
        "success": True,
        "brand": brand,
        "count": len(models),
        "models": models
    })

@app.route('/health', methods=['GET'])
def health():
    adjustments = load_adjustments()
    feedbacks = load_feedback()
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "vehicles_loaded": len(VEHICLE_DATABASE),
        "learning_enabled": True,
        "learned_vehicles": len(adjustments),
        "total_feedback": len(feedbacks)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
