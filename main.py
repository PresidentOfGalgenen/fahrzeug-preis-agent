# main_LEARNING_POSTGRES.py
# Base44 Pricing Agent mit PostgreSQL für persistentes Lernen

from flask import Flask, request, jsonify
from flask_cors import CORS
from vehicle_database import VEHICLE_DATABASE, BASE_HOURLY_RATES
from datetime import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json

app = Flask(__name__)
CORS(app)

# ========================================
# POSTGRESQL CONNECTION
# ========================================

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Erstelle Datenbankverbindung"""
    # Render nutzt postgresql:// aber psycopg2 braucht postgres://
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    elif DATABASE_URL and DATABASE_URL.startswith('postgresql://'):
        conn = psycopg2.connect(DATABASE_URL.replace('postgresql://', 'postgres://'), cursor_factory=RealDictCursor)
    else:
        # Fallback auf lokale DB (für Entwicklung)
        conn = psycopg2.connect(
            host='localhost',
            database='base44_learning',
            user='postgres',
            password='postgres',
            cursor_factory=RealDictCursor
        )
    return conn

def init_database():
    """Erstelle Tabellen wenn sie nicht existieren"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Feedback-Tabelle
    cur.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            brand VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL,
            year INTEGER NOT NULL,
            condition VARCHAR(50) NOT NULL,
            feedback_type VARCHAR(50) NOT NULL,
            calculated_price DECIMAL(10,2),
            correct_price DECIMAL(10,2),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Learning-Adjustments Tabelle
    cur.execute('''
        CREATE TABLE IF NOT EXISTS learning_adjustments (
            id SERIAL PRIMARY KEY,
            vehicle_key VARCHAR(200) UNIQUE NOT NULL,
            multiplier_adjustment DECIMAL(10,4) NOT NULL,
            feedback_count INTEGER DEFAULT 1,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reason TEXT
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

# Initialisiere DB beim Start
try:
    init_database()
    print("✅ Datenbank initialisiert!")
except Exception as e:
    print(f"⚠️ DB-Init Fehler: {e}")

# ========================================
# DATABASE FUNCTIONS
# ========================================

def save_feedback_db(feedback_data):
    """Speichere Feedback in PostgreSQL"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO feedback 
        (brand, model, year, condition, feedback_type, calculated_price, correct_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (
        feedback_data['brand'],
        feedback_data['model'],
        feedback_data['year'],
        feedback_data['condition'],
        feedback_data['feedback'],
        feedback_data.get('calculated_price'),
        feedback_data.get('correct_price')
    ))
    
    conn.commit()
    cur.close()
    conn.close()

def load_adjustment_db(vehicle_key):
    """Lade Adjustment für ein Fahrzeug"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT * FROM learning_adjustments WHERE vehicle_key = %s
    ''', (vehicle_key,))
    
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    return dict(result) if result else None

def save_adjustment_db(vehicle_key, adjustment_data):
    """Speichere oder Update Adjustment"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO learning_adjustments 
        (vehicle_key, multiplier_adjustment, feedback_count, reason, last_updated)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (vehicle_key) 
        DO UPDATE SET 
            multiplier_adjustment = EXCLUDED.multiplier_adjustment,
            feedback_count = EXCLUDED.feedback_count,
            reason = EXCLUDED.reason,
            last_updated = CURRENT_TIMESTAMP
    ''', (
        vehicle_key,
        adjustment_data['multiplier_adjustment'],
        adjustment_data['feedback_count'],
        adjustment_data.get('reason', '')
    ))
    
    conn.commit()
    cur.close()
    conn.close()

def get_learning_stats_db():
    """Hole Statistiken aus DB"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Total Feedback
    cur.execute('SELECT COUNT(*) as count FROM feedback')
    total_feedback = cur.fetchone()['count']
    
    # Learned Vehicles
    cur.execute('SELECT COUNT(*) as count FROM learning_adjustments')
    learned_vehicles = cur.fetchone()['count']
    
    # Feedback by Type
    cur.execute('''
        SELECT feedback_type, COUNT(*) as count 
        FROM feedback 
        GROUP BY feedback_type
    ''')
    feedback_types = {row['feedback_type']: row['count'] for row in cur.fetchall()}
    
    # Top Learned Vehicles
    cur.execute('''
        SELECT * FROM learning_adjustments 
        ORDER BY feedback_count DESC 
        LIMIT 10
    ''')
    top_learned = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return {
        'total_feedback': total_feedback,
        'learned_vehicles': learned_vehicles,
        'feedback_by_type': feedback_types,
        'top_learned_vehicles': [dict(row) for row in top_learned]
    }

# ========================================
# STANDARD MULTIPLIERS (wie vorher)
# ========================================

DEPRECIATION_RATES = {
    0: 1.0, 1: 0.85, 2: 0.75, 3: 0.68, 5: 0.55,
    7: 0.45, 10: 0.35, 15: 0.25, 20: 0.20
}

CONDITION_MULTIPLIERS = {
    "Einwandfrei": 1.15, "Sehr gut": 1.0,
    "Gut": 0.85, "Akzeptabel": 0.70
}

BODY_STYLE_BONUSES = {
    "Cabrio": 1.15, "Roadster": 1.15, "Coupé": 1.08,
    "SUV-Coupé": 1.05, "SUV": 1.02, "Kombi": 0.98,
    "Van": 0.95, "Limousine": 1.0
}

# ========================================
# LEARNING FUNCTIONS (angepasst für DB)
# ========================================

def analyze_feedback(feedback_data):
    """Analysiere Feedback (wie vorher)"""
    feedback_type = feedback_data.get('feedback')
    calculated_price = feedback_data.get('calculated_price')
    correct_price = feedback_data.get('correct_price')
    
    vehicle_key = f"{feedback_data['brand']}_{feedback_data['model']}"
    adjustments = {}
    
    if feedback_type == 'perfect':
        adjustments['confidence_boost'] = 0.02
        adjustments['multiplier_adjustment'] = 1.0
        
    elif feedback_type == 'too_high' and correct_price:
        deviation = (calculated_price - correct_price) / calculated_price
        adjustment_factor = 1 - (deviation * 0.5)
        adjustments['multiplier_adjustment'] = max(0.8, adjustment_factor)
        adjustments['reason'] = f"Preis war {deviation*100:.1f}% zu hoch"
        
    elif feedback_type == 'too_low' and correct_price:
        deviation = (correct_price - calculated_price) / calculated_price
        adjustment_factor = 1 + (deviation * 0.5)
        adjustments['multiplier_adjustment'] = min(1.2, adjustment_factor)
        adjustments['reason'] = f"Preis war {deviation*100:.1f}% zu niedrig"
        
    elif feedback_type == 'wrong' and correct_price:
        deviation = abs(correct_price - calculated_price) / calculated_price
        if correct_price > calculated_price:
            adjustment_factor = 1 + (deviation * 0.3)
            adjustments['multiplier_adjustment'] = min(1.3, adjustment_factor)
        else:
            adjustment_factor = 1 - (deviation * 0.3)
            adjustments['multiplier_adjustment'] = max(0.7, adjustment_factor)
        adjustments['reason'] = "Komplette Neuberechnung"
    
    adjustments['vehicle_key'] = vehicle_key
    adjustments['feedback_count'] = 1
    
    return adjustments

def apply_learning_adjustments(vehicle, base_price):
    """Wende Adjustments aus DB an"""
    vehicle_key = f"{vehicle['brand']}_{vehicle['model']}"
    
    adjustment = load_adjustment_db(vehicle_key)
    
    if adjustment:
        multiplier = adjustment['multiplier_adjustment']
        feedback_count = adjustment['feedback_count']
        
        weight = min(1.0, feedback_count / 10)
        adjusted_multiplier = 1.0 + ((multiplier - 1.0) * weight)
        
        return base_price * adjusted_multiplier, {
            'learning_applied': True,
            'adjustment_factor': adjusted_multiplier,
            'feedback_count': feedback_count,
            'reason': adjustment.get('reason', 'Gelernt aus DB')
        }
    
    return base_price, {'learning_applied': False, 'feedback_count': 0}

def update_learning_model(feedback_data):
    """Update Learning Model mit DB"""
    new_adjustments = analyze_feedback(feedback_data)
    
    if not new_adjustments.get('multiplier_adjustment'):
        return None
    
    vehicle_key = new_adjustments['vehicle_key']
    existing = load_adjustment_db(vehicle_key)
    
    if existing:
        existing_count = existing['feedback_count']
        new_count = existing_count + 1
        
        existing_multiplier = existing['multiplier_adjustment']
        new_multiplier = new_adjustments['multiplier_adjustment']
        
        combined_multiplier = (
            (float(existing_multiplier) * existing_count + new_multiplier) / 
            new_count
        )
        
        adjustment_data = {
            'multiplier_adjustment': combined_multiplier,
            'feedback_count': new_count,
            'reason': new_adjustments.get('reason', '')
        }
    else:
        adjustment_data = new_adjustments
    
    save_adjustment_db(vehicle_key, adjustment_data)
    
    return adjustment_data

# ========================================
# HELPER FUNCTIONS (wie vorher)
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
    
    if learning_info.get('learning_applied'):
        feedback_count = learning_info.get('feedback_count', 0)
        boost = min(15, feedback_count * 1.5)
        score += boost
    
    return max(0, min(100, score))

def calculate_price(brand, model, year, condition):
    """Preisberechnung mit DB-Learning"""
    vehicle = find_vehicle(brand, model)
    
    if not vehicle:
        return None
    
    if 'year_start' in vehicle and 'year_end' in vehicle:
        if year < vehicle['year_start'] or year > vehicle['year_end']:
            return None
    
    category = vehicle["category"]
    base_rate = BASE_HOURLY_RATES.get(category, 15.0)
    
    current_year = datetime.now().year
    age = max(0, current_year - year)
    
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
    
    base_hourly_price = (
        base_rate * depreciation * condition_factor * price_multiplier * 
        hp_factor * body_bonus * electric_bonus * rarity_bonus *
        custom_rarity * demand_factor * premium_package_bonus * facelift_bonus
    )
    
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
            "note": "PostgreSQL-persistentes Lernen" if learning_info.get('learning_applied') else "Standard"
        },
        "confidence_score": confidence,
        "confidence": confidence_label
    }

# ========================================
# API ROUTES
# ========================================

@app.route('/')
def home():
    try:
        stats = get_learning_stats_db()
        return jsonify({
            "message": "Base44 Pricing Agent mit PostgreSQL",
            "version": "2.3-POSTGRES",
            "learning_stats": stats,
            "database": "PostgreSQL (Persistent!)"
        })
    except:
        return jsonify({
            "message": "Base44 Pricing Agent",
            "version": "2.3-POSTGRES",
            "database": "DB noch nicht initialisiert"
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
            brand = data['brand']
            model = data['model']
            year = data['year']
            condition = data['condition']
        
        result = calculate_price(brand, model, year, condition)
        
        if result is None:
            return jsonify({"success": False, "error": "Fahrzeug nicht gefunden"}), 404
        
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
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        
        feedback_data = {
            **data,
            'timestamp': datetime.now().isoformat()
        }
        
        save_feedback_db(feedback_data)
        adjustment_result = update_learning_model(feedback_data)
        
        return jsonify({
            "success": True,
            "message": "Feedback in PostgreSQL gespeichert!",
            "learning_update": adjustment_result
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/learning-stats', methods=['GET'])
def learning_stats():
    try:
        stats = get_learning_stats_db()
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify({"success": True, "count": len(VEHICLE_DATABASE), "vehicles": VEHICLE_DATABASE})

@app.route('/brands', methods=['GET'])
def get_brands():
    brands = sorted(set(v["brand"] for v in VEHICLE_DATABASE))
    return jsonify({"success": True, "count": len(brands), "brands": brands})

@app.route('/models', methods=['GET'])
def get_models():
    brand = request.args.get('brand')
    if not brand:
        return jsonify({"success": False, "error": "Parameter 'brand' fehlt"}), 400
    
    models = sorted(set(v["model"] for v in VEHICLE_DATABASE if v["brand"].lower() == brand.lower()))
    return jsonify({"success": True, "brand": brand, "count": len(models), "models": models})

@app.route('/models/<brand>', methods=['GET'])
def get_models_by_path(brand):
    models = sorted(set(v["model"] for v in VEHICLE_DATABASE if v["brand"].lower() == brand.lower()))
    return jsonify({"success": True, "brand": brand, "count": len(models), "models": models})

@app.route('/health', methods=['GET'])
def health():
    try:
        stats = get_learning_stats_db()
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "vehicles_loaded": len(VEHICLE_DATABASE),
            "learning_enabled": True,
            "database": "PostgreSQL",
            "learned_vehicles": stats['learned_vehicles'],
            "total_feedback": stats['total_feedback']
        })
    except Exception as e:
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "vehicles_loaded": len(VEHICLE_DATABASE),
            "learning_enabled": True,
            "database": "PostgreSQL (not connected)",
            "error": str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
