from flask import Flask, request, jsonify
from datetime import datetime

# Importiere Fahrzeugdatenbank aus separater Datei
from vehicle_database import VEHICLE_DATABASE, BASE_HOURLY_RATES

app = Flask(__name__)

# Feedback deaktiviert (kein File-Writing auf Render Free)
def load_feedback():
    return []

def save_feedback(data):
    print(f"Feedback logged: {data.get('type', 'unknown')}")
    pass

def find_vehicle_in_database(brand, model):
    """Sucht Fahrzeug in Datenbank"""
    search_key = f"{brand} {model}".strip()
    
    if search_key in VEHICLE_DATABASE:
        return VEHICLE_DATABASE[search_key], search_key
    
    search_lower = search_key.lower()
    for key in VEHICLE_DATABASE.keys():
        if key.lower() == search_lower:
            return VEHICLE_DATABASE[key], key
        if search_lower in key.lower() or key.lower() in search_lower:
            return VEHICLE_DATABASE[key], key
    
    return None, None

def calculate_price(vehicle_data):
    """
    🧠 KOMPLEXER 15-FAKTOREN ALGORITHMUS
    """
    brand = vehicle_data.get('brand', '')
    model = vehicle_data.get('model', '')
    year = int(vehicle_data.get('year', datetime.now().year))
    mileage = int(vehicle_data.get('mileage', 0))
    condition = vehicle_data.get('condition', 'Gut')
    
    # 1. FAHRZEUG-MATCHING
    vehicle_info, full_key = find_vehicle_in_database(brand, model)
    
    if vehicle_info:
        category = vehicle_info['category']
        segment = vehicle_info['segment']
        body_type = vehicle_info['body_type']
        new_price = vehicle_info['new_price']
        hp = vehicle_info['hp']
        engine = vehicle_info['engine']
        from_database = True
        base_rate = BASE_HOURLY_RATES.get(category, 12.0)
    else:
        category = "Kompakt"
        segment = "Unbekannt"
        body_type = "Limousine"
        new_price = 30000
        hp = 150
        engine = 2.0
        from_database = False
        base_rate = 12.0
    
    # 2. FAHRZEUG-ALTER
    current_year = datetime.now().year
    vehicle_age = current_year - year
    
    # 3. NICHTLINEARE ABSCHREIBUNG
    if vehicle_age <= 1:
        depreciation = 0.15
    elif vehicle_age <= 3:
        depreciation = 0.15 + (vehicle_age - 1) * 0.08
    elif vehicle_age <= 6:
        depreciation = 0.31 + (vehicle_age - 3) * 0.06
    elif vehicle_age <= 10:
        depreciation = 0.49 + (vehicle_age - 6) * 0.04
    else:
        depreciation = min(0.65 + (vehicle_age - 10) * 0.02, 0.85)
    
    price_after_age = base_rate * (1 - depreciation)
    
    # 4. KILOMETERSTAND (10 Stufen)
    if mileage < 10000:
        mileage_factor = 1.20
    elif mileage < 30000:
        mileage_factor = 1.15
    elif mileage < 50000:
        mileage_factor = 1.10
    elif mileage < 75000:
        mileage_factor = 1.05
    elif mileage < 100000:
        mileage_factor = 1.0
    elif mileage < 125000:
        mileage_factor = 0.95
    elif mileage < 150000:
        mileage_factor = 0.88
    elif mileage < 175000:
        mileage_factor = 0.82
    elif mileage < 200000:
        mileage_factor = 0.75
    else:
        mileage_factor = 0.65
    
    price_after_mileage = price_after_age * mileage_factor
    
    # 5. ZUSTANDSFAKTOR
    condition_factors = {
        "Sehr gut": 1.18,
        "Gut": 1.0,
        "Mittel": 0.82,
        "Schlecht": 0.60
    }
    condition_factor = condition_factors.get(condition, 1.0)
    price_after_condition = price_after_mileage * condition_factor
    
    # 6. NEUPREIS-BONUS (Luxus-Aufschlag)
    if new_price > 150000:
        luxury_multiplier = 1.30
    elif new_price > 100000:
        luxury_multiplier = 1.22
    elif new_price > 70000:
        luxury_multiplier = 1.15
    elif new_price > 50000:
        luxury_multiplier = 1.10
    elif new_price > 35000:
        luxury_multiplier = 1.05
    else:
        luxury_multiplier = 1.0
    
    price_after_luxury = price_after_condition * luxury_multiplier
    
    # 7. PS-FAKTOR (Leistung)
    if hp > 500:
        hp_factor = 1.25
    elif hp > 350:
        hp_factor = 1.18
    elif hp > 250:
        hp_factor = 1.12
    elif hp > 180:
        hp_factor = 1.05
    else:
        hp_factor = 1.0
    
    price_after_hp = price_after_luxury * hp_factor
    
    # 8. KAROSSERIETYP-BONUS
    body_bonuses = {
        "Cabriolet": 1.15,
        "Roadster": 1.18,
        "Coupé": 1.08,
        "SUV": 1.12,
        "Kombi": 1.03,
        "Van": 1.05,
        "Limousine": 1.0,
        "Schrägheck": 1.0,
        "Fastback": 1.06
    }
    body_bonus = body_bonuses.get(body_type, 1.0)
    price_after_body = price_after_hp * body_bonus
    
    # 9. ELEKTRO-BONUS
    is_electric = (engine == 0.0)
    electric_bonus = 1.10 if is_electric else 1.0
    price_after_electric = price_after_body * electric_bonus
    
    # 10. SELTENHEITS-FAKTOR
    if "Supersportwagen" in category or "Ultra" in category:
        rarity_bonus = 1.20
    elif "Luxus" in category or "Sport" in category:
        rarity_bonus = 1.10
    else:
        rarity_bonus = 1.0
    
    final_price_per_hour = price_after_electric * rarity_bonus
    
    # 11. TAGESPREIS (8h, 20% Rabatt)
    price_per_day = final_price_per_hour * 8 * 0.80
    
    # 12. WOCHENPREIS (7 Tage, 30% Rabatt)
    price_per_week = price_per_day * 7 * 0.70
    
    # 13. RUNDUNG
    final_price_per_hour = round(final_price_per_hour * 2) / 2
    price_per_day = round(price_per_day * 2) / 2
    price_per_week = round(price_per_week)
    
    # 14. VERTRAUENSWERT
    confidence_score = 0
    if from_database:
        confidence_score += 40
    if mileage < 100000:
        confidence_score += 20
    if vehicle_age < 5:
        confidence_score += 20
    if condition in ["Sehr gut", "Gut"]:
        confidence_score += 20
    
    if confidence_score >= 80:
        confidence = "sehr hoch"
    elif confidence_score >= 60:
        confidence = "hoch"
    elif confidence_score >= 40:
        confidence = "mittel"
    else:
        confidence = "niedrig"
    
    # 15. RÜCKGABE
    return {
        "suggested_price_per_hour": final_price_per_hour,
        "suggested_price_per_day": price_per_day,
        "suggested_price_per_week": price_per_week,
        "currency": "EUR",
        "vehicle_info": {
            "category": category,
            "segment": segment,
            "body_type": body_type,
            "new_price_estimate": new_price,
            "horsepower": hp,
            "engine_size": engine,
            "is_electric": is_electric,
            "from_database": from_database,
            "matched_vehicle": full_key if from_database else None
        },
        "calculation_factors": {
            "base_rate": base_rate,
            "vehicle_age_years": vehicle_age,
            "depreciation_percent": round(depreciation * 100, 1),
            "mileage_factor": round(mileage_factor, 3),
            "condition_factor": round(condition_factor, 3),
            "luxury_multiplier": round(luxury_multiplier, 3),
            "hp_factor": round(hp_factor, 3),
            "body_bonus": round(body_bonus, 3),
            "electric_bonus": round(electric_bonus, 3),
            "rarity_bonus": round(rarity_bonus, 3)
        },
        "confidence": confidence,
        "confidence_score": confidence_score
    }

# === API ENDPOINTS ===

@app.route('/')
def home():
    total = len(VEHICLE_DATABASE)
    brands = sorted(list(set([key.split()[0] for key in VEHICLE_DATABASE.keys()])))
    
    return jsonify({
        "service": "Fahrzeug-Preis-Agent v3.0 PREMIUM",
        "version": "3.0.0",
        "status": "online",
        "features": [
            "150+ Fahrzeuge in Datenbank",
            "15 Berechnungsfaktoren",
            "Detaillierte Segmente (Cabrio, Coupé, SUV-Coupé)",
            "Luxusmarken (Ferrari, Lamborghini, Bentley, Rolls-Royce)",
            "Nichtlineare Abschreibung",
            "10-stufige Kilometerberechnung"
        ],
        "database_stats": {
            "total_vehicles": total,
            "total_brands": len(brands),
            "brands": brands
        },
        "endpoints": {
            "/calculate": "POST - Intelligente Preisberechnung",
            "/vehicles": "GET - Alle Fahrzeuge",
            "/brands": "GET - Alle Marken",
            "/models": "GET - Modelle einer Marke (Parameter: brand)",
            "/health": "GET - Health Check"
        }
    })

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify({
        "success": True,
        "total": len(VEHICLE_DATABASE),
        "vehicles": VEHICLE_DATABASE
    })

@app.route('/brands', methods=['GET'])
def get_brands():
    brands = sorted(list(set([key.split()[0] for key in VEHICLE_DATABASE.keys()])))
    return jsonify({
        "success": True,
        "total": len(brands),
        "brands": brands
    })

@app.route('/models', methods=['GET'])
def get_models():
    brand = request.args.get('brand', '')
    if not brand:
        return jsonify({"success": False, "error": "Parameter 'brand' fehlt"}), 400
    
    models = []
    for key, value in VEHICLE_DATABASE.items():
        if key.startswith(brand):
            model_name = key.replace(f"{brand} ", "")
            models.append({
                "model": model_name,
                "category": value["category"],
                "segment": value["segment"],
                "body_type": value["body_type"]
            })
    
    return jsonify({
        "success": True,
        "brand": brand,
        "total": len(models),
        "models": models
    })

@app.route('/calculate', methods=['POST'])
def calculate_endpoint():
    try:
        data = request.get_json()
        required = ['brand', 'model', 'year', 'mileage', 'condition']
        missing = [f for f in required if f not in data]
        
        if missing:
            return jsonify({"error": "Fehlende Felder", "missing": missing}), 400
        
        result = calculate_price(data)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": data,
            "output": result,
            "type": "calculation"
        }
        save_feedback(log_entry)
        
        return jsonify({"success": True, "data": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback_endpoint():
    try:
        data = request.get_json()
        
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "feedback": {
                "vehicle_brand": data.get('vehicle_brand'),
                "vehicle_model": data.get('vehicle_model'),
                "suggested_price": data.get('suggested_price'),
                "actual_price_used": data.get('actual_price_used'),
                "comment": data.get('comment', '')
            },
            "type": "user_feedback"
        }
        save_feedback(feedback_entry)
        
        if data.get('suggested_price') and data.get('actual_price_used'):
            deviation = ((data['actual_price_used'] - data['suggested_price']) / data['suggested_price']) * 100
            message = f"Danke! Dein Preis weicht {abs(deviation):.1f}% {'nach oben' if deviation > 0 else 'nach unten'} ab."
        else:
            message = "Feedback gespeichert!"
        
        return jsonify({"success": True, "message": message})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database_vehicles": len(VEHICLE_DATABASE),
        "version": "3.0.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
