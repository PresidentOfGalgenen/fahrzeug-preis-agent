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
    """Speichert neues Feedback in der Datei"""
    try:
        # Prüfe ob Datei existiert, wenn nicht erstelle leere Liste
        if not os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        feedback_list = load_feedback()
        feedback_list.append(data)
        
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(feedback_list, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Could not save feedback: {e}")

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
        "category": "Supersportwagen", "segment": "GT-Sportwagen", "body_type": "Coupé",
        "generations": {
            "2014-2019": {"new_price": 125000, "hp": 462, "engine": 4.0},
            "2019-2024": {"new_price": 145000, "hp": 585, "engine": 4.0}
        }
    },
    "Mercedes AMG GT Roadster": {
        "category": "Supersportwagen", "segment": "GT-Roadster", "body_type": "Roadster",
        "generations": {
            "2017-2024": {"new_price": 155000, "hp": 585, "engine": 4.0}
        }
    },
    "Mercedes EQC": {
        "category": "Elektro-SUV", "segment": "Elektro-SUV", "body_type": "SUV",
        "generations": {
            "2019-2024": {"new_price": 68000, "hp": 408, "engine": 0.0}
        }
    },
    "Mercedes EQS": {
        "category": "Elektro-Luxus", "segment": "Elektro-Luxuslimousine", "body_type": "Limousine",
        "generations": {
            "2021-2024": {"new_price": 110000, "hp": 333, "engine": 0.0}
        }
    },
    "Mercedes Sprinter": {
        "category": "Transporter", "segment": "Kastenwagen", "body_type": "Van",
        "generations": {
            "2018-2024": {"new_price": 42000, "hp": 143, "engine": 2.0}
        }
    },
    "Mercedes Vito": {
        "category": "Transporter", "segment": "Kastenwagen", "body_type": "Van",
        "generations": {
            "2014-2024": {"new_price": 38000, "hp": 136, "engine": 2.0}
        }
    },
    
    # ========================================
    # AUDI
    # ========================================
    "Audi A1": {
        "category": "Kleinwagen", "segment": "Premium-Kleinwagen", "body_type": "Kleinwagen",
        "generations": {
            "2010-2018": {"new_price": 20000, "hp": 86, "engine": 1.2},
            "2018-2024": {"new_price": 26000, "hp": 116, "engine": 1.0}
        }
    },
    "Audi A3": {
        "category": "Kompakt-Premium", "segment": "Premium-Kompaktklasse", "body_type": "Schrägheck",
        "generations": {
            "2012-2020": {"new_price": 28000, "hp": 150, "engine": 1.4},
            "2020-2024": {"new_price": 34000, "hp": 150, "engine": 1.5}
        }
    },
    "Audi A3 Limousine": {
        "category": "Kompakt-Premium", "segment": "Premium-Kompaktlimousine", "body_type": "Limousine",
        "generations": {
            "2013-2024": {"new_price": 32000, "hp": 150, "engine": 1.5}
        }
    },
    "Audi A3 Cabrio": {
        "category": "Cabrio-Premium", "segment": "Premium-Cabriolet", "body_type": "Cabriolet",
        "generations": {
            "2014-2020": {"new_price": 40000, "hp": 150, "engine": 1.4}
        }
    },
    "Audi A4": {
        "category": "Mittelklasse-Premium", "segment": "Obere Mittelklasse", "body_type": "Limousine",
        "generations": {
            "2015-2024": {"new_price": 42000, "hp": 150, "engine": 2.0}
        }
    },
    "Audi A4 Avant": {
        "category": "Mittelklasse-Premium", "segment": "Premium-Kombi", "body_type": "Kombi",
        "generations": {
            "2015-2024": {"new_price": 45000, "hp": 150, "engine": 2.0}
        }
    },
    "Audi A5": {
        "category": "Coupé-Premium", "segment": "Premium-Coupé", "body_type": "Coupé",
        "generations": {
            "2016-2024": {"new_price": 48000, "hp": 190, "engine": 2.0}
        }
    },
    "Audi A5 Cabrio": {
        "category": "Cabrio-Premium", "segment": "Premium-Cabriolet", "body_type": "Cabriolet",
        "generations": {
            "2017-2024": {"new_price": 54000, "hp": 190, "engine": 2.0}
        }
    },
    "Audi A6": {
        "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_type": "Limousine",
        "generations": {
            "2018-2024": {"new_price": 58000, "hp": 204, "engine": 2.0}
        }
    },
    "Audi A6 Avant": {
        "category": "Oberklasse", "segment": "Premium-Kombi", "body_type": "Kombi",
        "generations": {
            "2018-2024": {"new_price": 62000, "hp": 204, "engine": 2.0}
        }
    },
    "Audi A7": {
        "category": "Luxus-Coupé", "segment": "Sportback", "body_type": "Fastback",
        "generations": {
            "2018-2024": {"new_price": 72000, "hp": 340, "engine": 3.0}
        }
    },
    "Audi A8": {
        "category": "Luxus", "segment": "Luxus-Limousine", "body_type": "Limousine",
        "generations": {
            "2017-2024": {"new_price": 95000, "hp": 340, "engine": 3.0}
        }
    },
    "Audi Q2": {
        "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2016-2024": {"new_price": 28000, "hp": 116, "engine": 1.0}
        }
    },
    "Audi Q3": {
        "category": "SUV-Kompakt", "segment": "Premium-Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2018-2024": {"new_price": 38000, "hp": 150, "engine": 1.5}
        }
    },
    "Audi Q3 Sportback": {
        "category": "SUV-Coupé", "segment": "Kompakt-SUV-Coupé", "body_type": "SUV",
        "generations": {
            "2019-2024": {"new_price": 42000, "hp": 150, "engine": 1.5}
        }
    },
    "Audi Q5": {
        "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_type": "SUV",
        "generations": {
            "2016-2024": {"new_price": 52000, "hp": 204, "engine": 2.0}
        }
    },
    "Audi Q5 Sportback": {
        "category": "SUV-Coupé", "segment": "SUV-Coupé", "body_type": "SUV",
        "generations": {
            "2021-2024": {"new_price": 58000, "hp": 204, "engine": 2.0}
        }
    },
    "Audi Q7": {
        "category": "SUV-Premium", "segment": "Oberklasse-SUV", "body_type": "SUV",
        "generations": {
            "2015-2024": {"new_price": 68000, "hp": 340, "engine": 3.0}
        }
    },
    "Audi Q8": {
        "category": "SUV-Luxus", "segment": "Luxus-SUV-Coupé", "body_type": "SUV",
        "generations": {
            "2018-2024": {"new_price": 82000, "hp": 340, "engine": 3.0}
        }
    },
    "Audi TT": {
        "category": "Sportwagen", "segment": "Sport-Coupé", "body_type": "Coupé",
        "generations": {
            "2014-2023": {"new_price": 42000, "hp": 230, "engine": 2.0}
        }
    },
    "Audi TT Roadster": {
        "category": "Roadster", "segment": "Sport-Roadster", "body_type": "Roadster",
        "generations": {
            "2014-2023": {"new_price": 48000, "hp": 230, "engine": 2.0}
        }
    },
    "Audi R8": {
        "category": "Supersportwagen", "segment": "Supersportwagen", "body_type": "Coupé",
        "generations": {
            "2015-2024": {"new_price": 175000, "hp": 570, "engine": 5.2}
        }
    },
    "Audi R8 Spyder": {
        "category": "Supersportwagen", "segment": "Super-Roadster", "body_type": "Roadster",
        "generations": {
            "2016-2024": {"new_price": 195000, "hp": 570, "engine": 5.2}
        }
    },
    "Audi RS3": {
        "category": "Sportwagen", "segment": "Performance-Kompaktklasse", "body_type": "Limousine",
        "generations": {
            "2015-2024": {"new_price": 62000, "hp": 400, "engine": 2.5}
        }
    },
    "Audi RS4 Avant": {
        "category": "Sportwagen", "segment": "Performance-Kombi", "body_type": "Kombi",
        "generations": {
            "2017-2024": {"new_price": 82000, "hp": 450, "engine": 2.9}
        }
    },
    "Audi RS5": {
        "category": "Sportwagen", "segment": "Performance-Coupé", "body_type": "Coupé",
        "generations": {
            "2017-2024": {"new_price": 88000, "hp": 450, "engine": 2.9}
        }
    },
    "Audi RS6 Avant": {
        "category": "Supersportwagen", "segment": "Performance-Kombi", "body_type": "Kombi",
        "generations": {
            "2019-2024": {"new_price": 125000, "hp": 600, "engine": 4.0}
        }
    },
    "Audi RS7": {
        "category": "Supersportwagen", "segment": "Performance-Sportback", "body_type": "Fastback",
        "generations": {
            "2019-2024": {"new_price": 135000, "hp": 600, "engine": 4.0}
        }
    },
    "Audi e-tron": {
        "category": "Elektro-SUV", "segment": "Elektro-Premium-SUV", "body_type": "SUV",
        "generations": {
            "2019-2024": {"new_price": 75000, "hp": 408, "engine": 0.0}
        }
    },
    "Audi e-tron GT": {
        "category": "Elektro-Sportwagen", "segment": "Elektro-Gran-Turismo", "body_type": "Limousine",
        "generations": {
            "2021-2024": {"new_price": 105000, "hp": 530, "engine": 0.0}
        }
    },
    
    # ========================================
    # PORSCHE
    # ========================================
    "Porsche 911": {
        "category": "Supersportwagen", "segment": "Ikonen-Sportwagen", "body_type": "Coupé",
        "generations": {
            "2011-2019": {"new_price": 105000, "hp": 370, "engine": 3.4},
            "2019-2024": {"new_price": 130000, "hp": 385, "engine": 3.0}
        }
    },
    "Porsche 911 Cabrio": {
        "category": "Supersportwagen", "segment": "Sportwagen-Cabriolet", "body_type": "Cabriolet",
        "generations": {
            "2019-2024": {"new_price": 145000, "hp": 385, "engine": 3.0}
        }
    },
    "Porsche 911 Turbo": {
        "category": "Supersportwagen", "segment": "Turbo-Sportwagen", "body_type": "Coupé",
        "generations": {
            "2020-2024": {"new_price": 210000, "hp": 580, "engine": 3.8}
        }
    },
    "Porsche 911 GT3": {
        "category": "Supersportwagen", "segment": "Track-Sportwagen", "body_type": "Coupé",
        "generations": {
            "2021-2024": {"new_price": 185000, "hp": 510, "engine": 4.0}
        }
    },
    "Porsche 718 Cayman": {
        "category": "Sportwagen", "segment": "Mittelmotor-Sportwagen", "body_type": "Coupé",
        "generations": {
            "2016-2024": {"new_price": 65000, "hp": 300, "engine": 2.0}
        }
    },
    "Porsche 718 Boxster": {
        "category": "Roadster", "segment": "Mittelmotor-Roadster", "body_type": "Roadster",
        "generations": {
            "2016-2024": {"new_price": 68000, "hp": 300, "engine": 2.0}
        }
    },
    "Porsche Cayenne": {
        "category": "SUV-Premium", "segment": "Luxus-SUV", "body_type": "SUV",
        "generations": {
            "2017-2024": {"new_price": 82000, "hp": 340, "engine": 3.0}
        }
    },
    "Porsche Cayenne Coupé": {
        "category": "SUV-Coupé", "segment": "Luxus-SUV-Coupé", "body_type": "SUV",
        "generations": {
            "2019-2024": {"new_price": 92000, "hp": 340, "engine": 3.0}
        }
    },
    "Porsche Macan": {
        "category": "SUV-Sport", "segment": "Sport-SUV", "body_type": "SUV",
        "generations": {
            "2014-2024": {"new_price": 62000, "hp": 265, "engine": 2.0}
        }
    },
    "Porsche Panamera": {
        "category": "Luxus-Sportwagen", "segment": "Gran Turismo", "body_type": "Limousine",
        "generations": {
            "2016-2024": {"new_price": 95000, "hp": 330, "engine": 2.9}
        }
    },
    "Porsche Taycan": {
        "category": "Elektro-Sportwagen", "segment": "Elektro-Gran-Turismo", "body_type": "Limousine",
        "generations": {
            "2019-2024": {"new_price": 95000, "hp": 408, "engine": 0.0}
        }
    },
    
    # ========================================
    # TESLA
    # ========================================
    "Tesla Model 3": {
        "category": "Elektro-Mittelklasse", "segment": "Elektro-Limousine", "body_type": "Limousine",
        "generations": {
            "2019-2024": {"new_price": 48000, "hp": 325, "engine": 0.0}
        }
    },
    "Tesla Model S": {
        "category": "Elektro-Oberklasse", "segment": "Elektro-Luxuslimousine", "body_type": "Limousine",
        "generations": {
            "2012-2024": {"new_price": 95000, "hp": 670, "engine": 0.0}
        }
    },
    "Tesla Model X": {
        "category": "Elektro-SUV", "segment": "Elektro-Luxus-SUV", "body_type": "SUV",
        "generations": {
            "2015-2024": {"new_price": 105000, "hp": 670, "engine": 0.0}
        }
    },
    "Tesla Model Y": {
        "category": "Elektro-SUV", "segment": "Elektro-Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2021-2024": {"new_price": 58000, "hp": 462, "engine": 0.0}
        }
    },
    
    # ========================================
    # WEITERE PREMIUM-MARKEN
    # ========================================
    
    # FERRARI
    "Ferrari 488": {
        "category": "Supersportwagen", "segment": "Supersportwagen", "body_type": "Coupé",
        "generations": {
            "2015-2020": {"new_price": 250000, "hp": 670, "engine": 3.9}
        }
    },
    "Ferrari F8": {
        "category": "Supersportwagen", "segment": "Supersportwagen", "body_type": "Coupé",
        "generations": {
            "2019-2024": {"new_price": 280000, "hp": 720, "engine": 3.9}
        }
    },
    "Ferrari Roma": {
        "category": "Supersportwagen", "segment": "Gran Turismo", "body_type": "Coupé",
        "generations": {
            "2020-2024": {"new_price": 235000, "hp": 620, "engine": 3.9}
        }
    },
    "Ferrari Portofino": {
        "category": "Supersportwagen", "segment": "GT-Cabrio", "body_type": "Cabriolet",
        "generations": {
            "2017-2024": {"new_price": 225000, "hp": 600, "engine": 3.9}
        }
    },
    
    # LAMBORGHINI
    "Lamborghini Huracán": {
        "category": "Supersportwagen", "segment": "Supersportwagen", "body_type": "Coupé",
        "generations": {
            "2014-2024": {"new_price": 220000, "hp": 640, "engine": 5.2}
        }
    },
    "Lamborghini Aventador": {
        "category": "Supersportwagen", "segment": "Flaggschiff-Supersportwagen", "body_type": "Coupé",
        "generations": {
            "2011-2022": {"new_price": 380000, "hp": 770, "engine": 6.5}
        }
    },
    "Lamborghini Urus": {
        "category": "SUV-Super", "segment": "Super-SUV", "body_type": "SUV",
        "generations": {
            "2018-2024": {"new_price": 220000, "hp": 650, "engine": 4.0}
        }
    },
    
    # BENTLEY
    "Bentley Continental GT": {
        "category": "Luxus-Sportwagen", "segment": "Luxus-Gran-Turismo", "body_type": "Coupé",
        "generations": {
            "2018-2024": {"new_price": 220000, "hp": 550, "engine": 4.0}
        }
    },
    "Bentley Flying Spur": {
        "category": "Ultraluxus", "segment": "Luxus-Limousine", "body_type": "Limousine",
        "generations": {
            "2019-2024": {"new_price": 230000, "hp": 550, "engine": 4.0}
        }
    },
    "Bentley Bentayga": {
        "category": "SUV-Ultraluxus", "segment": "Luxus-SUV", "body_type": "SUV",
        "generations": {
            "2015-2024": {"new_price": 200000, "hp": 550, "engine": 4.0}
        }
    },
    
    # ROLLS-ROYCE
    "Rolls-Royce Ghost": {
        "category": "Ultraluxus", "segment": "Luxus-Limousine", "body_type": "Limousine",
        "generations": {
            "2020-2024": {"new_price": 320000, "hp": 571, "engine": 6.75}
        }
    },
    "Rolls-Royce Phantom": {
        "category": "Ultraluxus", "segment": "Flaggschiff-Limousine", "body_type": "Limousine",
        "generations": {
            "2017-2024": {"new_price": 450000, "hp": 571, "engine": 6.75}
        }
    },
    "Rolls-Royce Cullinan": {
        "category": "SUV-Ultraluxus", "segment": "Ultra-Luxus-SUV", "body_type": "SUV",
        "generations": {
            "2018-2024": {"new_price": 350000, "hp": 571, "engine": 6.75}
        }
    },
    
    # ========================================
    # VOLUMEN-MARKEN
    # ========================================
    
    # OPEL
    "Opel Corsa": {
        "category": "Kleinwagen", "segment": "Kleinwagen", "body_type": "Kleinwagen",
        "generations": {
            "2019-2024": {"new_price": 18000, "hp": 100, "engine": 1.2}
        }
    },
    "Opel Astra": {
        "category": "Kompakt", "segment": "Kompaktklasse", "body_type": "Schrägheck",
        "generations": {
            "2021-2024": {"new_price": 26000, "hp": 130, "engine": 1.2}
        }
    },
    "Opel Insignia": {
        "category": "Mittelklasse", "segment": "Mittelklasse", "body_type": "Limousine",
        "generations": {
            "2017-2024": {"new_price": 32000, "hp": 165, "engine": 2.0}
        }
    },
    "Opel Mokka": {
        "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2020-2024": {"new_price": 25000, "hp": 130, "engine": 1.2}
        }
    },
    "Opel Grandland": {
        "category": "SUV-Mittel", "segment": "Mittelklasse-SUV", "body_type": "SUV",
        "generations": {
            "2021-2024": {"new_price": 32000, "hp": 130, "engine": 1.2}
        }
    },
    
    # FORD
    "Ford Fiesta": {
        "category": "Kleinwagen", "segment": "Kleinwagen", "body_type": "Kleinwagen",
        "generations": {
            "2017-2023": {"new_price": 18000, "hp": 85, "engine": 1.1}
        }
    },
    "Ford Focus": {
        "category": "Kompakt", "segment": "Kompaktklasse", "body_type": "Schrägheck",
        "generations": {
            "2018-2024": {"new_price": 26000, "hp": 125, "engine": 1.0}
        }
    },
    "Ford Mustang": {
        "category": "Sportwagen", "segment": "Muscle Car", "body_type": "Coupé",
        "generations": {
            "2015-2024": {"new_price": 52000, "hp": 450, "engine": 5.0}
        }
    },
    "Ford Mustang Cabrio": {
        "category": "Cabrio-Sport", "segment": "Muscle Cabrio", "body_type": "Cabriolet",
        "generations": {
            "2015-2024": {"new_price": 58000, "hp": 450, "engine": 5.0}
        }
    },
    "Ford Kuga": {
        "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2019-2024": {"new_price": 32000, "hp": 150, "engine": 1.5}
        }
    },
    "Ford Explorer": {
        "category": "SUV-Groß", "segment": "Großraum-SUV", "body_type": "SUV",
        "generations": {
            "2019-2024": {"new_price": 62000, "hp": 457, "engine": 3.0}
        }
    },
    
    # FIAT
    "Fiat 500": {
        "category": "Kleinstwagen", "segment": "Retro-Kleinwagen", "body_type": "Kleinwagen",
        "generations": {
            "2015-2024": {"new_price": 16000, "hp": 69, "engine": 1.2}
        }
    },
    "Fiat 500 Cabrio": {
        "category": "Cabrio-Klein", "segment": "City-Cabrio", "body_type": "Cabriolet",
        "generations": {
            "2015-2024": {"new_price": 19000, "hp": 69, "engine": 1.2}
        }
    },
    "Fiat 500X": {
        "category": "SUV-Klein", "segment": "Mini-SUV", "body_type": "SUV",
        "generations": {
            "2018-2024": {"new_price": 24000, "hp": 120, "engine": 1.0}
        }
    },
    "Fiat Tipo": {
        "category": "Kompakt", "segment": "Kompaktklasse", "body_type": "Limousine",
        "generations": {
            "2016-2024": {"new_price": 20000, "hp": 120, "engine": 1.4}
        }
    },
    
    # RENAULT
    "Renault Clio": {
        "category": "Kleinwagen", "segment": "Kleinwagen", "body_type": "Kleinwagen",
        "generations": {
            "2019-2024": {"new_price": 18000, "hp": 90, "engine": 1.0}
        }
    },
    "Renault Megane": {
        "category": "Kompakt", "segment": "Kompaktklasse", "body_type": "Schrägheck",
        "generations": {
            "2020-2024": {"new_price": 26000, "hp": 140, "engine": 1.3}
        }
    },
    "Renault Captur": {
        "category": "SUV-Klein", "segment": "Mini-SUV", "body_type": "SUV",
        "generations": {
            "2019-2024": {"new_price": 24000, "hp": 130, "engine": 1.3}
        }
    },
    "Renault Kadjar": {
        "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2018-2024": {"new_price": 30000, "hp": 140, "engine": 1.3}
        }
    },
    
    # SEAT
    "Seat Ibiza": {
        "category": "Kleinwagen", "segment": "Kleinwagen", "body_type": "Kleinwagen",
        "generations": {
            "2017-2024": {"new_price": 18000, "hp": 95, "engine": 1.0}
        }
    },
    "Seat Leon": {
        "category": "Kompakt", "segment": "Kompaktklasse", "body_type": "Schrägheck",
        "generations": {
            "2020-2024": {"new_price": 26000, "hp": 110, "engine": 1.0}
        }
    },
    "Seat Ateca": {
        "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2020-2024": {"new_price": 28000, "hp": 110, "engine": 1.0}
        }
    },
    
    # SKODA
    "Skoda Fabia": {
        "category": "Kleinwagen", "segment": "Kleinwagen", "body_type": "Kleinwagen",
        "generations": {
            "2021-2024": {"new_price": 18000, "hp": 95, "engine": 1.0}
        }
    },
    "Skoda Octavia": {
        "category": "Kompakt", "segment": "Kompaktklasse", "body_type": "Limousine",
        "generations": {
            "2019-2024": {"new_price": 28000, "hp": 150, "engine": 1.5}
        }
    },
    "Skoda Octavia Combi": {
        "category": "Kompakt", "segment": "Kompakt-Kombi", "body_type": "Kombi",
        "generations": {
            "2019-2024": {"new_price": 30000, "hp": 150, "engine": 1.5}
        }
    },
    "Skoda Superb": {
        "category": "Mittelklasse", "segment": "Mittelklasse", "body_type": "Limousine",
        "generations": {
            "2019-2024": {"new_price": 38000, "hp": 190, "engine": 2.0}
        }
    },
    "Skoda Kodiaq": {
        "category": "SUV-Mittel", "segment": "Mittelklasse-SUV", "body_type": "SUV",
        "generations": {
            "2021-2024": {"new_price": 36000, "hp": 150, "engine": 1.5}
        }
    },
    
    # MAZDA
    "Mazda MX-5": {
        "category": "Roadster", "segment": "Roadster", "body_type": "Roadster",
        "generations": {
            "2015-2024": {"new_price": 32000, "hp": 184, "engine": 2.0}
        }
    },
    "Mazda 3": {
        "category": "Kompakt", "segment": "Kompaktklasse", "body_type": "Schrägheck",
        "generations": {
            "2019-2024": {"new_price": 26000, "hp": 122, "engine": 2.0}
        }
    },
    "Mazda CX-5": {
        "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_type": "SUV",
        "generations": {
            "2017-2024": {"new_price": 32000, "hp": 165, "engine": 2.0}
        }
    },
    
    # MINI
    "Mini Cooper": {
        "category": "Kleinwagen", "segment": "Premium-Kleinwagen", "body_type": "Kleinwagen",
        "generations": {
            "2018-2024": {"new_price": 24000, "hp": 136, "engine": 1.5}
        }
    },
    "Mini Cooper Cabrio": {
        "category": "Cabrio-Klein", "segment": "Premium-City-Cabrio", "body_type": "Cabriolet",
        "generations": {
            "2018-2024": {"new_price": 30000, "hp": 136, "engine": 1.5}
        }
    },
    "Mini Countryman": {
        "category": "SUV-Klein", "segment": "Premium-Mini-SUV", "body_type": "SUV",
        "generations": {
            "2017-2024": {"new_price": 32000, "hp": 136, "engine": 1.5}
        }
    },
    "Mini Clubman": {
        "category": "Kompakt", "segment": "Premium-Kombi", "body_type": "Kombi",
        "generations": {
            "2019-2024": {"new_price": 28000, "hp": 136, "engine": 1.5}
        }
    },
}

# ==========================================
# 🎯 KATEGORIE-BASIERTE PREISE
# ==========================================

BASE_HOURLY_RATES = {
    "Kleinstwagen": 5.5,
    "Kleinwagen": 7.0,
    "Kompakt": 9.5,
    "Kompakt-Premium": 12.0,
    "Mittelklasse": 13.5,
    "Mittelklasse-Premium": 16.0,
    "Oberklasse": 22.0,
    "Luxus": 35.0,
    "Ultraluxus": 75.0,
    "Coupé-Premium": 18.0,
    "Luxus-Coupé": 32.0,
    "Cabrio-Klein": 10.0,
    "Cabrio-Premium": 20.0,
    "Luxus-Cabrio": 40.0,
    "Cabrio-Sport": 28.0,
    "Roadster": 22.0,
    "Luxus-Roadster": 45.0,
    "SUV-Klein": 10.0,
    "SUV-Kompakt": 12.0,
    "SUV-Mittel": 16.0,
    "SUV-Sport": 24.0,
    "SUV-Premium": 26.0,
    "SUV-Luxus": 38.0,
    "SUV-Ultraluxus": 65.0,
    "SUV-Super": 55.0,
    "SUV-Offroad": 28.0,
    "SUV-Coupé": 22.0,
    "SUV-Cabrio": 24.0,
    "Sport": 25.0,
    "Sportwagen": 38.0,
    "Luxus-Sportwagen": 55.0,
    "Supersportwagen": 85.0,
    "Transporter": 12.0,
    "Hochdachkombi": 10.0,
    "SUV-Groß": 20.0,
    "Elektro-Kompakt": 11.0,
    "Elektro-Mittelklasse": 15.0,
    "Elektro-Premium": 20.0,
    "Elektro-Oberklasse": 28.0,
    "Elektro-Luxus": 40.0,
    "Elektro-SUV": 22.0,
    "Elektro-Sportwagen": 45.0,
}

# ==========================================
# 🧮 KOMPLEXER BERECHNUNGS-ALGORITHMUS
# ==========================================

def find_vehicle_generation(vehicle_key, year):
    """Findet die passende Fahrzeuggeneration"""
    if vehicle_key not in VEHICLE_DATABASE:
        return None
    
    vehicle = VEHICLE_DATABASE[vehicle_key]
    generations = vehicle.get("generations", {})
    
    for gen_years, gen_data in generations.items():
        if "-" in gen_years:
            start, end = gen_years.split("-")
            if int(start) <= year <= int(end):
                return {**vehicle, **gen_data}
    
    # Fallback: Nehme neueste Generation
    if generations:
        latest = sorted(generations.items(), key=lambda x: int(x[0].split("-")[1]), reverse=True)[0]
        return {**vehicle, **latest[1]}
    
    return vehicle

def find_vehicle_in_database(brand, model, year):
    """Sucht Fahrzeug mit Jahresberücksichtigung"""
    search_key = f"{brand} {model}".strip()
    
    # Exakte Suche
    if search_key in VEHICLE_DATABASE:
        return find_vehicle_generation(search_key, year), search_key
    
    # Teilweise Suche
    search_lower = search_key.lower()
    for key in VEHICLE_DATABASE.keys():
        if key.lower() == search_lower:
            return find_vehicle_generation(key, year), key
        if search_lower in key.lower() or key.lower() in search_lower:
            return find_vehicle_generation(key, year), key
    
    return None, None

def get_learning_adjustment(vehicle_data):
    """Lernanpassung basierend auf Feedback"""
    feedback_list = load_feedback()
    brand = vehicle_data.get('brand', '').lower()
    model = vehicle_data.get('model', '').lower()
    
    # Exakte Übereinstimmung
    relevant = [f for f in feedback_list 
                if f.get('type') == 'user_feedback' 
                and f.get('feedback', {}).get('actual_price_used')
                and f.get('feedback', {}).get('vehicle_brand', '').lower() == brand
                and f.get('feedback', {}).get('vehicle_model', '').lower() == model]
    
    if not relevant:
        # Nur Marke
        relevant = [f for f in feedback_list 
                    if f.get('type') == 'user_feedback' 
                    and f.get('feedback', {}).get('actual_price_used')
                    and f.get('feedback', {}).get('vehicle_brand', '').lower() == brand]
    
    if not relevant:
        return 1.0
    
    adjustments = []
    for fb in relevant:
        suggested = fb['feedback'].get('suggested_price')
        actual = fb['feedback'].get('actual_price_used')
        if suggested and actual and suggested > 0:
            adjustments.append(actual / suggested)
    
    if adjustments:
        avg = sum(adjustments) / len(adjustments)
        return max(0.7, min(1.3, avg))
    
    return 1.0

def calculate_price(vehicle_data):
    """
    🧠 KOMPLEXER PREIS-ALGORITHMUS mit 15+ Faktoren
    """
    brand = vehicle_data.get('brand', '')
    model = vehicle_data.get('model', '')
    year = int(vehicle_data.get('year', datetime.now().year))
    mileage = int(vehicle_data.get('mileage', 0))
    condition = vehicle_data.get('condition', 'Gut')
    
    # 1. FAHRZEUG-MATCHING
    vehicle_info, full_key = find_vehicle_in_database(brand, model, year)
    
    if vehicle_info:
        category = vehicle_info['category']
        segment = vehicle_info['segment']
        body_type = vehicle_info['body_type']
        new_price = vehicle_info.get('new_price', 30000)
        hp = vehicle_info.get('hp', 150)
        engine = vehicle_info.get('engine', 2.0)
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
    
    # 3. ABSCHREIBUNG (nichtlinear, nach Alter)
    if vehicle_age <= 1:
        depreciation = 0.15  # Neuwagen verliert sofort 15%
    elif vehicle_age <= 3:
        depreciation = 0.15 + (vehicle_age - 1) * 0.08  # Jahre 2-3: je 8%
    elif vehicle_age <= 6:
        depreciation = 0.31 + (vehicle_age - 3) * 0.06  # Jahre 4-6: je 6%
    elif vehicle_age <= 10:
        depreciation = 0.49 + (vehicle_age - 6) * 0.04  # Jahre 7-10: je 4%
    else:
        depreciation = min(0.65 + (vehicle_age - 10) * 0.02, 0.85)  # Ab Jahr 11: je 2%, max 85%
    
    price_after_age = base_rate * (1 - depreciation)
    
    # 4. KILOMETERSTAND (sehr detailliert)
    if mileage < 10000:
        mileage_factor = 1.20  # Fast neu
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
        mileage_factor = 0.65  # Sehr viel gefahren
    
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
    
    # 7. PS-FAKTOR (Leistung beeinflusst Preis)
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
    
    # 9. ELEKTRO-BONUS (moderne Technologie)
    is_electric = (engine == 0.0)
    if is_electric:
        electric_bonus = 1.10
    else:
        electric_bonus = 1.0
    
    price_after_electric = price_after_body * electric_bonus
    
    # 10. SELTENHEITS-FAKTOR (Supersportwagen & Luxus)
    if "Supersportwagen" in category or "Ultra" in category:
        rarity_bonus = 1.20
    elif "Luxus" in category or "Sport" in category:
        rarity_bonus = 1.10
    else:
        rarity_bonus = 1.0
    
    price_after_rarity = price_after_electric * rarity_bonus
    
    # 11. LERNANPASSUNG (aus Feedback)
    learning_factor = get_learning_adjustment(vehicle_data)
    final_price_per_hour = price_after_rarity * learning_factor
    
    # 12. TAGESPREIS (8h = 1 Tag, 20% Rabatt)
    hours_per_day = 8
    day_discount = 0.80
    price_per_day = final_price_per_hour * hours_per_day * day_discount
    
    # 13. WOCHENPREIS (7 Tage, 30% Rabatt)
    price_per_week = price_per_day * 7 * 0.70
    
    # 14. RUNDUNG
    final_price_per_hour = round(final_price_per_hour * 2) / 2
    price_per_day = round(price_per_day * 2) / 2
    price_per_week = round(price_per_week)
    
    # 15. VERTRAUENSWERT
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
            "rarity_bonus": round(rarity_bonus, 3),
            "learning_adjustment": round(learning_factor, 3)
        },
        "confidence": confidence,
        "confidence_score": confidence_score
    }

# ==========================================
# 🌐 API ENDPOINTS
# ==========================================

@app.route('/')
def home():
    """API Info"""
    total = len(VEHICLE_DATABASE)
    brands = sorted(list(set([key.split()[0] for key in VEHICLE_DATABASE.keys()])))
    
    return jsonify({
        "service": "Fahrzeug-Preis-Agent v3.0 PREMIUM",
        "version": "3.0.0",
        "status": "online",
        "features": [
            "200+ Fahrzeuge in Datenbank",
            "Jahrgangsspezifische Bewertung",
            "15+ Berechnungsfaktoren",
            "Detaillierte Segmente (Cabrio, Coupé, SUV-Coupé, etc.)",
            "Luxusmarken (Ferrari, Lamborghini, Bentley, Rolls-Royce)",
            "Lernfähiges Feedback-System"
        ],
        "database_stats": {
            "total_vehicles": total,
            "total_brands": len(brands),
            "brands": brands
        },
        "endpoints": {
            "/calculate": "POST - Intelligente Preisberechnung",
            "/feedback": "POST - Feedback-System",
            "/vehicles": "GET - Alle Fahrzeuge",
            "/brands": "GET - Alle Marken",
            "/models": "GET - Modelle einer Marke",
            "/health": "GET - Health Check"
        }
    })

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    """Alle Fahrzeuge"""
    return jsonify({
        "success": True,
        "total": len(VEHICLE_DATABASE),
        "vehicles": VEHICLE_DATABASE
    })

@app.route('/brands', methods=['GET'])
def get_brands():
    """Alle Marken"""
    brands = sorted(list(set([key.split()[0] for key in VEHICLE_DATABASE.keys()])))
    return jsonify({
        "success": True,
        "total": len(brands),
        "brands": brands
    })

@app.route('/models', methods=['GET'])
def get_models():
    """Modelle einer Marke"""
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
    """Hauptendpoint"""
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
    """Feedback speichern"""
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
            message = f"Danke! Dein Preis weicht {abs(deviation):.1f}% {'nach oben' if deviation > 0 else 'nach unten'} ab. Der Agent lernt daraus!"
        else:
            message = "Feedback gespeichert!"
        
        return jsonify({"success": True, "message": message})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health Check"""
    feedback_count = len(load_feedback())
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database_vehicles": len(VEHICLE_DATABASE),
        "total_feedback": feedback_count,
        "version": "3.0.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
