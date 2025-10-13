from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# ==========================================
# 📊 DATENBANK
# ==========================================
FEEDBACK_FILE = "feedback_data.json"

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_feedback(data):
    try:
        feedback_list = load_feedback()
        feedback_list.append(data)
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(feedback_list, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Could not save feedback: {e}")

# ==========================================
# 🚗 MEGA FAHRZEUG-DATENBANK (200+ Fahrzeuge)
# ==========================================

"""
Struktur:
"Marke Modell": {
    "category": Hauptkategorie für Basispreis
    "segment": Detailliertes Segment (Cabrio, Coupé, etc.)
    "body_type": Karosserieform
    "generations": {
        "Jahr-Bereich": {Neupreis, PS, Hubraum}
    }
}
"""

VEHICLE_DATABASE = {
    # ========================================
    # VOLKSWAGEN (VW)
    # ========================================
    "VW up!": {
        "category": "Kleinstwagen", "segment": "City-Car", "body_type": "Kleinwagen",
        "generations": {
            "2011-2016": {"new_price": 11000, "hp": 60, "engine": 1.0},
            "2017-2023": {"new_price": 13500, "hp": 75, "engine": 1.0}
        }
    },
    "VW Polo": {
        "category": "Kleinwagen", "segment": "Supermini", "body_type": "Kleinwagen",
        "generations": {
            "2009-2017": {"new_price": 14000, "hp": 90, "engine": 1.2},
            "2017-2023": {"new_price": 18000, "hp": 95, "engine": 1.0}
        }
    },
    "VW Golf": {
        "category": "Kompakt", "segment": "Kompaktklasse", "body_type": "Schrägheck",
        "generations": {
            "2008-2012": {"new_price": 22000, "hp": 105, "engine": 1.6},
            "2012-2019": {"new_price": 26000, "hp": 110, "engine": 1.4},
            "2019-2024": {"new_price": 30000, "hp": 130, "engine": 1.5}
        }
    },
    "VW Golf GTI": {
        "category": "Sport", "segment": "Hot Hatch", "body_type": "Schrägheck",
        "generations": {
            "2013-2020": {"new_price": 35000, "hp": 220, "engine": 2.0},
            "2020-2024": {"new_price": 42000, "hp": 245, "engine": 2.0}
        }
    },
    "VW Golf R": {
        "category": "Sport", "segment": "Performance Hatch", "body_type": "Schrägheck",
        "generations": {
            "2014-2020": {"new_price": 45000, "hp": 300, "engine": 2.0},
            "2020-2024": {"new_price": 52000, "hp": 320, "engine": 2.0}
        }
    },
    "VW Passat": {
        "category": "Mittelklasse", "segment": "Mittelklasse Limousine", "body_type": "Limousine",
        "generations": {
            "2010-2014": {"new_price": 32000, "hp": 140, "engine": 2.0},
            "2014-2019": {"new_price": 36000, "hp": 150, "engine": 2.0},
            "2019-2024": {"new_price": 42000, "hp": 190, "engine": 2.0}
        }
    },
    "VW Passat Variant": {
        "category": "Mittelklasse", "segment": "Mittelklasse Kombi", "body_type": "Kombi",
        "generations": {
            "2014-2019": {"new_price": 38000, "hp": 150, "engine": 2.0},
            "2019-2024": {"new_price": 44000, "hp": 190, "engine": 2.0}
        }
    },
    "VW Arteon": {
        "category": "Oberklasse", "segment": "Gran Turismo", "body_type": "Fastback",
        "generations": {
            "2017-2020": {"new_price": 45000, "hp": 190, "engine": 2.0},
            "2020-2024": {"new_price": 52000, "hp": 280, "engine": 2.0}
        }
    },
    "VW T-Roc": {
        "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2017-2022": {"new_price": 24000, "hp": 115, "engine": 1.0},
            "2022-2024": {"new_price": 28000, "hp": 150, "engine": 1.5}
        }
    },
    "VW T-Roc Cabrio": {
        "category": "SUV-Cabrio", "segment": "Cabrio-SUV", "body_type": "Cabriolet",
        "generations": {
            "2019-2024": {"new_price": 35000, "hp": 150, "engine": 1.5}
        }
    },
    "VW Tiguan": {
        "category": "SUV-Mittel", "segment": "Mittelklasse-SUV", "body_type": "SUV",
        "generations": {
            "2011-2016": {"new_price": 30000, "hp": 140, "engine": 2.0},
            "2016-2024": {"new_price": 38000, "hp": 190, "engine": 2.0}
        }
    },
    "VW Touareg": {
        "category": "SUV-Premium", "segment": "Oberklasse-SUV", "body_type": "SUV",
        "generations": {
            "2010-2018": {"new_price": 55000, "hp": 262, "engine": 3.0},
            "2018-2024": {"new_price": 68000, "hp": 286, "engine": 3.0}
        }
    },
    "VW Caddy": {
        "category": "Hochdachkombi", "segment": "Kastenwagen", "body_type": "Van",
        "generations": {
            "2015-2020": {"new_price": 22000, "hp": 102, "engine": 1.6},
            "2020-2024": {"new_price": 27000, "hp": 122, "engine": 2.0}
        }
    },
    "VW T6": {
        "category": "Transporter", "segment": "Großraum-Van", "body_type": "Van",
        "generations": {
            "2015-2019": {"new_price": 32000, "hp": 150, "engine": 2.0},
            "2019-2024": {"new_price": 38000, "hp": 150, "engine": 2.0}
        }
    },
    
    # ========================================
    # BMW
    # ========================================
    "BMW 1er": {
        "category": "Kompakt-Premium", "segment": "Premium-Kompaktklasse", "body_type": "Schrägheck",
        "generations": {
            "2011-2019": {"new_price": 28000, "hp": 136, "engine": 1.6},
            "2019-2024": {"new_price": 34000, "hp": 140, "engine": 1.5}
        }
    },
    "BMW 2er": {
        "category": "Kompakt-Premium", "segment": "Premium-Kompaktklasse", "body_type": "Coupé",
        "generations": {
            "2014-2021": {"new_price": 32000, "hp": 150, "engine": 1.5},
            "2021-2024": {"new_price": 38000, "hp": 170, "engine": 2.0}
        }
    },
    "BMW 2er Cabrio": {
        "category": "Cabrio-Premium", "segment": "Premium-Cabriolet", "body_type": "Cabriolet",
        "generations": {
            "2015-2024": {"new_price": 42000, "hp": 184, "engine": 2.0}
        }
    },
    "BMW 3er": {
        "category": "Mittelklasse-Premium", "segment": "Obere Mittelklasse", "body_type": "Limousine",
        "generations": {
            "2012-2019": {"new_price": 40000, "hp": 184, "engine": 2.0},
            "2019-2024": {"new_price": 48000, "hp": 184, "engine": 2.0}
        }
    },
    "BMW 3er Touring": {
        "category": "Mittelklasse-Premium", "segment": "Premium-Kombi", "body_type": "Kombi",
        "generations": {
            "2012-2019": {"new_price": 43000, "hp": 184, "engine": 2.0},
            "2019-2024": {"new_price": 51000, "hp": 184, "engine": 2.0}
        }
    },
    "BMW 4er": {
        "category": "Coupé-Premium", "segment": "Premium-Coupé", "body_type": "Coupé",
        "generations": {
            "2013-2020": {"new_price": 45000, "hp": 184, "engine": 2.0},
            "2020-2024": {"new_price": 52000, "hp": 258, "engine": 2.0}
        }
    },
    "BMW 4er Cabrio": {
        "category": "Cabrio-Premium", "segment": "Premium-Cabriolet", "body_type": "Cabriolet",
        "generations": {
            "2014-2020": {"new_price": 52000, "hp": 184, "engine": 2.0},
            "2020-2024": {"new_price": 60000, "hp": 258, "engine": 2.0}
        }
    },
    "BMW 5er": {
        "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_type": "Limousine",
        "generations": {
            "2010-2017": {"new_price": 52000, "hp": 218, "engine": 2.0},
            "2017-2023": {"new_price": 62000, "hp": 252, "engine": 2.0},
            "2023-2024": {"new_price": 72000, "hp": 292, "engine": 3.0}
        }
    },
    "BMW 5er Touring": {
        "category": "Oberklasse", "segment": "Premium-Kombi", "body_type": "Kombi",
        "generations": {
            "2017-2023": {"new_price": 65000, "hp": 252, "engine": 2.0},
            "2023-2024": {"new_price": 75000, "hp": 292, "engine": 3.0}
        }
    },
    "BMW 7er": {
        "category": "Luxus", "segment": "Oberklasse Limousine", "body_type": "Limousine",
        "generations": {
            "2015-2022": {"new_price": 95000, "hp": 326, "engine": 3.0},
            "2022-2024": {"new_price": 115000, "hp": 381, "engine": 3.0}
        }
    },
    "BMW 8er": {
        "category": "Luxus-Coupé", "segment": "Gran Turismo", "body_type": "Coupé",
        "generations": {
            "2018-2024": {"new_price": 105000, "hp": 340, "engine": 3.0}
        }
    },
    "BMW 8er Cabrio": {
        "category": "Luxus-Cabrio", "segment": "Luxus-Cabriolet", "body_type": "Cabriolet",
        "generations": {
            "2019-2024": {"new_price": 115000, "hp": 340, "engine": 3.0}
        }
    },
    "BMW X1": {
        "category": "SUV-Kompakt", "segment": "Premium-Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2015-2022": {"new_price": 35000, "hp": 140, "engine": 1.5},
            "2022-2024": {"new_price": 42000, "hp": 170, "engine": 2.0}
        }
    },
    "BMW X2": {
        "category": "SUV-Coupé", "segment": "SUV-Coupé", "body_type": "SUV",
        "generations": {
            "2018-2024": {"new_price": 40000, "hp": 178, "engine": 2.0}
        }
    },
    "BMW X3": {
        "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_type": "SUV",
        "generations": {
            "2017-2024": {"new_price": 52000, "hp": 252, "engine": 2.0}
        }
    },
    "BMW X4": {
        "category": "SUV-Coupé", "segment": "Premium-SUV-Coupé", "body_type": "SUV",
        "generations": {
            "2018-2024": {"new_price": 60000, "hp": 252, "engine": 2.0}
        }
    },
    "BMW X5": {
        "category": "SUV-Premium", "segment": "Oberklasse-SUV", "body_type": "SUV",
        "generations": {
            "2013-2018": {"new_price": 65000, "hp": 258, "engine": 3.0},
            "2018-2024": {"new_price": 78000, "hp": 340, "engine": 3.0}
        }
    },
    "BMW X6": {
        "category": "SUV-Coupé", "segment": "SAC (Sports Activity Coupé)", "body_type": "SUV",
        "generations": {
            "2014-2019": {"new_price": 72000, "hp": 313, "engine": 3.0},
            "2019-2024": {"new_price": 85000, "hp": 340, "engine": 3.0}
        }
    },
    "BMW X7": {
        "category": "SUV-Luxus", "segment": "Luxus-SUV", "body_type": "SUV",
        "generations": {
            "2018-2024": {"new_price": 98000, "hp": 340, "engine": 3.0}
        }
    },
    "BMW Z4": {
        "category": "Roadster", "segment": "Premium-Roadster", "body_type": "Roadster",
        "generations": {
            "2018-2024": {"new_price": 55000, "hp": 197, "engine": 2.0}
        }
    },
    "BMW M2": {
        "category": "Sportwagen", "segment": "Performance-Coupé", "body_type": "Coupé",
        "generations": {
            "2018-2023": {"new_price": 65000, "hp": 410, "engine": 3.0},
            "2023-2024": {"new_price": 75000, "hp": 460, "engine": 3.0}
        }
    },
    "BMW M3": {
        "category": "Sportwagen", "segment": "Performance-Limousine", "body_type": "Limousine",
        "generations": {
            "2014-2020": {"new_price": 75000, "hp": 431, "engine": 3.0},
            "2020-2024": {"new_price": 88000, "hp": 510, "engine": 3.0}
        }
    },
    "BMW M4": {
        "category": "Sportwagen", "segment": "Performance-Coupé", "body_type": "Coupé",
        "generations": {
            "2014-2020": {"new_price": 78000, "hp": 431, "engine": 3.0},
            "2020-2024": {"new_price": 92000, "hp": 510, "engine": 3.0}
        }
    },
    "BMW M5": {
        "category": "Supersportwagen", "segment": "Performance-Limousine", "body_type": "Limousine",
        "generations": {
            "2011-2017": {"new_price": 105000, "hp": 560, "engine": 4.4},
            "2017-2024": {"new_price": 125000, "hp": 625, "engine": 4.4}
        }
    },
    "BMW M8": {
        "category": "Supersportwagen", "segment": "Performance-Gran-Coupé", "body_type": "Coupé",
        "generations": {
            "2019-2024": {"new_price": 145000, "hp": 625, "engine": 4.4}
        }
    },
    "BMW i3": {
        "category": "Elektro-Kompakt", "segment": "Elektro-Kleinwagen", "body_type": "Schrägheck",
        "generations": {
            "2013-2022": {"new_price": 38000, "hp": 170, "engine": 0.0}
        }
    },
    "BMW i4": {
        "category": "Elektro-Premium", "segment": "Elektro-Gran-Coupé", "body_type": "Limousine",
        "generations": {
            "2021-2024": {"new_price": 60000, "hp": 340, "engine": 0.0}
        }
    },
    "BMW iX": {
        "category": "Elektro-SUV", "segment": "Elektro-Luxus-SUV", "body_type": "SUV",
        "generations": {
            "2021-2024": {"new_price": 85000, "hp": 326, "engine": 0.0}
        }
    },
    
    # ========================================
    # MERCEDES-BENZ
    # ========================================
    "Mercedes A-Klasse": {
        "category": "Kompakt-Premium", "segment": "Premium-Kompaktklasse", "body_type": "Schrägheck",
        "generations": {
            "2012-2018": {"new_price": 28000, "hp": 122, "engine": 1.6},
            "2018-2024": {"new_price": 35000, "hp": 163, "engine": 1.3}
        }
    },
    "Mercedes B-Klasse": {
        "category": "Kompakt-Van", "segment": "Premium-Kompakt-Van", "body_type": "Van",
        "generations": {
            "2011-2018": {"new_price": 30000, "hp": 122, "engine": 1.6},
            "2018-2024": {"new_price": 37000, "hp": 163, "engine": 1.3}
        }
    },
    "Mercedes C-Klasse": {
        "category": "Mittelklasse-Premium", "segment": "Obere Mittelklasse", "body_type": "Limousine",
        "generations": {
            "2014-2021": {"new_price": 42000, "hp": 184, "engine": 2.0},
            "2021-2024": {"new_price": 52000, "hp": 204, "engine": 2.0}
        }
    },
    "Mercedes C-Klasse T-Modell": {
        "category": "Mittelklasse-Premium", "segment": "Premium-Kombi", "body_type": "Kombi",
        "generations": {
            "2014-2021": {"new_price": 45000, "hp": 184, "engine": 2.0},
            "2021-2024": {"new_price": 55000, "hp": 204, "engine": 2.0}
        }
    },
    "Mercedes C-Klasse Coupé": {
        "category": "Coupé-Premium", "segment": "Premium-Coupé", "body_type": "Coupé",
        "generations": {
            "2015-2024": {"new_price": 50000, "hp": 204, "engine": 2.0}
        }
    },
    "Mercedes C-Klasse Cabrio": {
        "category": "Cabrio-Premium", "segment": "Premium-Cabriolet", "body_type": "Cabriolet",
        "generations": {
            "2016-2024": {"new_price": 56000, "hp": 204, "engine": 2.0}
        }
    },
    "Mercedes E-Klasse": {
        "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_type": "Limousine",
        "generations": {
            "2016-2023": {"new_price": 58000, "hp": 194, "engine": 2.0},
            "2023-2024": {"new_price": 70000, "hp": 272, "engine": 2.0}
        }
    },
    "Mercedes E-Klasse T-Modell": {
        "category": "Oberklasse", "segment": "Premium-Kombi", "body_type": "Kombi",
        "generations": {
            "2016-2023": {"new_price": 62000, "hp": 194, "engine": 2.0},
            "2023-2024": {"new_price": 74000, "hp": 272, "engine": 2.0}
        }
    },
    "Mercedes E-Klasse Coupé": {
        "category": "Luxus-Coupé", "segment": "Luxus-Coupé", "body_type": "Coupé",
        "generations": {
            "2017-2024": {"new_price": 68000, "hp": 299, "engine": 2.0}
        }
    },
    "Mercedes E-Klasse Cabrio": {
        "category": "Luxus-Cabrio", "segment": "Luxus-Cabriolet", "body_type": "Cabriolet",
        "generations": {
            "2017-2024": {"new_price": 74000, "hp": 299, "engine": 2.0}
        }
    },
    "Mercedes S-Klasse": {
        "category": "Luxus", "segment": "Luxus-Limousine", "body_type": "Limousine",
        "generations": {
            "2013-2020": {"new_price": 95000, "hp": 333, "engine": 3.0},
            "2020-2024": {"new_price": 120000, "hp": 435, "engine": 3.0}
        }
    },
    "Mercedes S-Klasse Coupé": {
        "category": "Luxus-Coupé", "segment": "Luxus-Gran-Coupé", "body_type": "Coupé",
        "generations": {
            "2014-2021": {"new_price": 130000, "hp": 462, "engine": 4.0}
        }
    },
    "Mercedes S-Klasse Cabrio": {
        "category": "Luxus-Cabrio", "segment": "Luxus-Cabriolet", "body_type": "Cabriolet",
        "generations": {
            "2015-2021": {"new_price": 145000, "hp": 462, "engine": 4.0}
        }
    },
    "Mercedes CLA": {
        "category": "Coupé-Premium", "segment": "Viertürer-Coupé", "body_type": "Coupé",
        "generations": {
            "2013-2019": {"new_price": 33000, "hp": 122, "engine": 1.6},
            "2019-2024": {"new_price": 38000, "hp": 163, "engine": 1.3}
        }
    },
    "Mercedes CLS": {
        "category": "Luxus-Coupé", "segment": "Viertürer-Coupé", "body_type": "Coupé",
        "generations": {
            "2018-2024": {"new_price": 75000, "hp": 299, "engine": 2.0}
        }
    },
    "Mercedes GLA": {
        "category": "SUV-Kompakt", "segment": "Premium-Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2013-2020": {"new_price": 32000, "hp": 122, "engine": 1.6},
            "2020-2024": {"new_price": 40000, "hp": 163, "engine": 1.3}
        }
    },
    "Mercedes GLB": {
        "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2019-2024": {"new_price": 42000, "hp": 163, "engine": 1.3}
        }
    },
    "Mercedes GLC": {
        "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_type": "SUV",
        "generations": {
            "2015-2022": {"new_price": 48000, "hp": 204, "engine": 2.0},
            "2022-2024": {"new_price": 58000, "hp": 258, "engine": 2.0}
        }
    },
    "Mercedes GLC Coupé": {
        "category": "SUV-Coupé", "segment": "SUV-Coupé", "body_type": "SUV",
        "generations": {
            "2016-2024": {"new_price": 60000, "hp": 258, "engine": 2.0}
        }
    },
    "Mercedes GLE": {
        "category": "SUV-Premium", "segment": "Oberklasse-SUV", "body_type": "SUV",
        "generations": {
            "2015-2019": {"new_price": 62000, "hp": 258, "engine": 2.0},
            "2019-2024": {"new_price": 75000, "hp": 367, "engine": 3.0}
        }
    },
    "Mercedes GLE Coupé": {
        "category": "SUV-Coupé", "segment": "Oberklasse-SUV-Coupé", "body_type": "SUV",
        "generations": {
            "2015-2024": {"new_price": 82000, "hp": 367, "engine": 3.0}
        }
    },
    "Mercedes GLS": {
        "category": "SUV-Luxus", "segment": "Luxus-SUV", "body_type": "SUV",
        "generations": {
            "2015-2019": {"new_price": 78000, "hp": 333, "engine": 3.0},
            "2019-2024": {"new_price": 95000, "hp": 367, "engine": 3.0}
        }
    },
    "Mercedes G-Klasse": {
        "category": "SUV-Offroad", "segment": "Geländewagen", "body_type": "SUV",
        "generations": {
            "2012-2018": {"new_price": 95000, "hp": 388, "engine": 5.5},
            "2018-2024": {"new_price": 130000, "hp": 422, "engine": 4.0}
        }
    },
    "Mercedes SL": {
        "category": "Luxus-Roadster", "segment": "Luxus-Roadster", "body_type": "Roadster",
        "generations": {
            "2012-2021": {"new_price": 105000, "hp": 435, "engine": 4.7},
            "2021-2024": {"new_price": 145000, "hp": 476, "engine": 4.0}
        }
    },
    "Mercedes SLC": {
        "category": "Roadster", "segment": "Kompakt-Roadster", "body_type": "Roadster",
        "generations": {
            "2016-2020": {"new_price": 48000, "hp": 184, "engine": 2.0}
        }
    },
    "Mercedes AMG GT": {
        "category": "
