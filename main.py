from flask import Flask, request, jsonify
from flask_cors import CORS
from vehicle_database import VEHICLE_DATABASE, BASE_HOURLY_RATES
from datetime import datetime
import math

app = Flask(__name__)
CORS(app)

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

# KILOMETERSTAND-FAKTOR ENTFERNT - wird nicht mehr verwendet!

CONDITION_MULTIPLIERS = {
    "Einwandfrei": 1.15,      # +15% für perfekten Zustand
    "Sehr gut": 1.0,          # Basis
    "Gut": 0.85,              # -15%
    "Akzeptabel": 0.70        # -30%
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

def calculate_confidence(vehicle, year, mileage, condition):
    score = 100
    current_year = datetime.now().year
    age = current_year - year
    
    # Alter-basierte Anpassung
    if age > 15:
        score -= 20
    elif age > 10:
        score -= 10
    
    # KILOMETERSTAND WIRD IGNORIERT - nicht mehr Teil der Confidence
    
    # Zustand-basierte Anpassung
    if condition == "Akzeptabel":
        score -= 15
    elif condition == "Gut":
        score -= 5
    # "Sehr gut" und "Einwandfrei" = keine Abzüge
    
    # Bonus für Premium-Fahrzeuge
    if vehicle["category"] in ["Supersportwagen", "Luxuslimousine"]:
        score += 10
    
    return max(0, min(100, score))

def calculate_price(brand, model, year, mileage, condition):
    vehicle = find_vehicle(brand, model)
    
    if not vehicle:
        return None
    
    # BAUJAHR-VALIDIERUNG
    if 'year_start' in vehicle and 'year_end' in vehicle:
        if year < vehicle['year_start'] or year > vehicle['year_end']:
            return None  # Fahrzeug gab es in diesem Baujahr nicht
    
    category = vehicle["category"]
    base_rate = BASE_HOURLY_RATES.get(category, 15.0)
    
    current_year = datetime.now().year
    age = max(0, current_year - year)
    
    depreciation = get_depreciation_factor(age)
    condition_factor = CONDITION_MULTIPLIERS.get(condition, 0.85)  # Default: "Gut"
    
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
    
    # CUSTOM MULTIPLIERS aus der Datenbank
    custom_rarity = vehicle.get("rarity_multiplier", 1.0)
    demand_factor = vehicle.get("demand_factor", 1.0)
    premium_package_bonus = 1.15 if vehicle.get("premium_package", False) else 1.0
    facelift_bonus = 1.05 if vehicle.get("facelift", False) else 1.0
    
    # KILOMETERSTAND-FAKTOR ENTFERNT!
    hourly_price = (
        base_rate * 
        depreciation * 
        condition_factor *  # Zustand hat jetzt größeren Einfluss (0.70 - 1.15)
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
    
    hourly_price = round(hourly_price * 2) / 2
    
    daily_price = hourly_price * 8 * 0.8
    weekly_price = daily_price * 7 * 0.7
    
    confidence = calculate_confidence(vehicle, year, mileage, condition)
    
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
            "note": "Kilometerstand wird ignoriert - nur Zustand beeinflusst Preis"
        },
        "confidence_score": confidence,
        "confidence": confidence_label
    }

@app.route('/')
def home():
    return jsonify({
        "message": "Base44 Fahrzeugpreis-Agent API",
        "version": "2.0",
        "endpoints": {
            "POST /calculate": "Berechne Mietpreis",
            "GET /vehicles": "Liste aller Fahrzeuge",
            "GET /brands": "Liste aller Marken",
            "GET /models?brand=X": "Modelle einer Marke",
            "POST /feedback": "Feedback senden",
            "GET /health": "Health Check"
        },
        "features": [
            "150+ Fahrzeuge",
            "15-Faktoren-Algorithmus",
            "CORS aktiviert"
        ]
    })

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    try:
        # GET-Request: Parameter aus URL
        if request.method == 'GET':
            brand = request.args.get('brand')
            model = request.args.get('model')
            year = request.args.get('year', type=int)
            mileage = request.args.get('mileage', type=int)
            condition = request.args.get('condition', 'Gut')
            
            if not all([brand, model, year, mileage]):
                return jsonify({
                    "success": False,
                    "error": "Fehlende Parameter: brand, model, year, mileage erforderlich"
                }), 400
        
        # POST-Request: JSON-Body
        else:
            data = request.get_json()
            
            required_fields = ['brand', 'model', 'year', 'mileage', 'condition']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        "success": False,
                        "error": f"Fehlendes Feld: {field}"
                    }), 400
            
            brand = data['brand']
            model = data['model']
            year = data['year']
            mileage = data['mileage']
            condition = data['condition']
        
        result = calculate_price(brand, model, year, mileage, condition)
        
        if result is None:
            return jsonify({
                "success": False,
                "error": "Fahrzeug nicht gefunden oder Baujahr nicht verfügbar"
            }), 404
        
        # Mappe die Feldnamen für Kompatibilität
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
    """Alternative Route mit Path Parameter statt Query Parameter"""
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

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        print(f"Feedback received: {data}")
        
        return jsonify({
            "success": True,
            "message": "Feedback gespeichert (aktuell nur geloggt)"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "vehicles_loaded": len(VEHICLE_DATABASE)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
