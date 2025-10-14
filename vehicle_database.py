# vehicle_database.py
# PROFI-FAHRZEUGDATENBANK mit maximaler Flexibilität
# Enthält: Generationen, Facelifts, Baujahre, Sondermodelle, Custom-Multipliers

VEHICLE_DATABASE = [
    # ========================================
    # VW - VOLKSWAGEN
    # ========================================
    
    # VW up! (2011-heute)
    {"brand": "VW", "model": "up!", "generation": "AA", "facelift": False, "year_start": 2011, "year_end": 2025, 
     "category": "Kleinstwagen", "segment": "City-Car", "body_style": "Kleinwagen", 
     "new_price": 13500, "hp": 75, "engine_displacement": 1.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # VW Polo (VI Generation)
    {"brand": "VW", "model": "Polo", "generation": "VI", "facelift": False, "year_start": 2017, "year_end": 2021, 
     "category": "Kleinwagen", "segment": "Supermini", "body_style": "Kleinwagen", 
     "new_price": 18000, "hp": 95, "engine_displacement": 1.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "VW", "model": "Polo", "generation": "VI FL", "facelift": True, "year_start": 2021, "year_end": 2025, 
     "category": "Kleinwagen", "segment": "Supermini", "body_style": "Kleinwagen", 
     "new_price": 20500, "hp": 95, "engine_displacement": 1.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0, "demand_factor": 1.05},
    
    # VW Golf 7
    {"brand": "VW", "model": "Golf", "generation": "VII", "facelift": False, "year_start": 2012, "year_end": 2017, 
     "category": "Kompakt", "segment": "Kompaktklasse", "body_style": "Schrägheck", 
     "new_price": 25000, "hp": 110, "engine_displacement": 1.4, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "VW", "model": "Golf", "generation": "VII FL", "facelift": True, "year_start": 2017, "year_end": 2019, 
     "category": "Kompakt", "segment": "Kompaktklasse", "body_style": "Schrägheck", 
     "new_price": 27000, "hp": 130, "engine_displacement": 1.5, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # VW Golf 8
    {"brand": "VW", "model": "Golf", "generation": "VIII", "facelift": False, "year_start": 2019, "year_end": 2025, 
     "category": "Kompakt", "segment": "Kompaktklasse", "body_style": "Schrägheck", 
     "new_price": 30000, "hp": 130, "engine_displacement": 1.5, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0, "demand_factor": 1.1},
    
    # VW Golf GTI (Performance-Modelle)
    {"brand": "VW", "model": "Golf GTI", "generation": "VII", "facelift": False, "year_start": 2013, "year_end": 2017, 
     "category": "Sport", "segment": "Hot Hatch", "body_style": "Schrägheck", 
     "new_price": 35000, "hp": 220, "engine_displacement": 2.0, 
     "special_edition": True, "premium_package": False, "rarity_multiplier": 1.15},
    
    {"brand": "VW", "model": "Golf GTI", "generation": "VIII", "facelift": False, "year_start": 2020, "year_end": 2025, 
     "category": "Sport", "segment": "Hot Hatch", "body_style": "Schrägheck", 
     "new_price": 42000, "hp": 245, "engine_displacement": 2.0, 
     "special_edition": True, "premium_package": False, "rarity_multiplier": 1.2, "demand_factor": 1.15},
    
    # VW Golf R (Top-Modell)
    {"brand": "VW", "model": "Golf R", "generation": "VII", "facelift": False, "year_start": 2014, "year_end": 2019, 
     "category": "Sport", "segment": "Performance Hatch", "body_style": "Schrägheck", 
     "new_price": 45000, "hp": 300, "engine_displacement": 2.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.25},
    
    {"brand": "VW", "model": "Golf R", "generation": "VIII", "facelift": False, "year_start": 2020, "year_end": 2025, 
     "category": "Sport", "segment": "Performance Hatch", "body_style": "Schrägheck", 
     "new_price": 52000, "hp": 320, "engine_displacement": 2.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.3, "demand_factor": 1.2},
    
    # VW Passat B8
    {"brand": "VW", "model": "Passat", "generation": "B8", "facelift": False, "year_start": 2014, "year_end": 2019, 
     "category": "Mittelklasse", "segment": "Mittelklasse Limousine", "body_style": "Limousine", 
     "new_price": 38000, "hp": 150, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "VW", "model": "Passat", "generation": "B8 FL", "facelift": True, "year_start": 2019, "year_end": 2022, 
     "category": "Mittelklasse", "segment": "Mittelklasse Limousine", "body_style": "Limousine", 
     "new_price": 42000, "hp": 190, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # VW T-Roc (2017-heute)
    {"brand": "VW", "model": "T-Roc", "generation": "A1", "facelift": False, "year_start": 2017, "year_end": 2022, 
     "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_style": "SUV", 
     "new_price": 26000, "hp": 110, "engine_displacement": 1.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "VW", "model": "T-Roc", "generation": "A1 FL", "facelift": True, "year_start": 2022, "year_end": 2025, 
     "category": "SUV-Kompakt", "segment": "Kompakt-SUV", "body_style": "SUV", 
     "new_price": 28000, "hp": 150, "engine_displacement": 1.5, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0, "demand_factor": 1.08},
    
    # VW Tiguan
    {"brand": "VW", "model": "Tiguan", "generation": "II", "facelift": False, "year_start": 2016, "year_end": 2020, 
     "category": "SUV-Mittel", "segment": "Mittelklasse-SUV", "body_style": "SUV", 
     "new_price": 35000, "hp": 150, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "VW", "model": "Tiguan", "generation": "II FL", "facelift": True, "year_start": 2020, "year_end": 2025, 
     "category": "SUV-Mittel", "segment": "Mittelklasse-SUV", "body_style": "SUV", 
     "new_price": 38000, "hp": 190, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # ========================================
    # BMW
    # ========================================
    
    # BMW 1er (F40 - aktuelle Generation)
    {"brand": "BMW", "model": "1er", "generation": "F40", "facelift": False, "year_start": 2019, "year_end": 2025, 
     "category": "Kompakt-Premium", "segment": "Premium-Kompaktklasse", "body_style": "Schrägheck", 
     "new_price": 34000, "hp": 140, "engine_displacement": 1.5, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # BMW 3er (G20 - aktuelle Generation)
    {"brand": "BMW", "model": "3er", "generation": "G20", "facelift": False, "year_start": 2019, "year_end": 2022, 
     "category": "Mittelklasse-Premium", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 45000, "hp": 184, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "BMW", "model": "3er", "generation": "G20 FL", "facelift": True, "year_start": 2022, "year_end": 2025, 
     "category": "Mittelklasse-Premium", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 48000, "hp": 184, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0, "demand_factor": 1.05},
    
    # BMW 3er M-Paket (Sportpaket)
    {"brand": "BMW", "model": "3er M Sport", "generation": "G20", "facelift": False, "year_start": 2019, "year_end": 2025, 
     "category": "Mittelklasse-Premium", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 53000, "hp": 184, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": True, "rarity_multiplier": 1.15, "demand_factor": 1.1},
    
    # BMW 5er (G30)
    {"brand": "BMW", "model": "5er", "generation": "G30", "facelift": False, "year_start": 2017, "year_end": 2020, 
     "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 65000, "hp": 252, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "BMW", "model": "5er", "generation": "G30 FL", "facelift": True, "year_start": 2020, "year_end": 2023, 
     "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 72000, "hp": 292, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # BMW 5er (G60 - neue Generation)
    {"brand": "BMW", "model": "5er", "generation": "G60", "facelift": False, "year_start": 2023, "year_end": 2025, 
     "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 78000, "hp": 292, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.05, "demand_factor": 1.15},
    
    # BMW X3 (G01)
    {"brand": "BMW", "model": "X3", "generation": "G01", "facelift": False, "year_start": 2017, "year_end": 2021, 
     "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_style": "SUV", 
     "new_price": 48000, "hp": 184, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "BMW", "model": "X3", "generation": "G01 FL", "facelift": True, "year_start": 2021, "year_end": 2025, 
     "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_style": "SUV", 
     "new_price": 52000, "hp": 252, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # BMW X5 (G05)
    {"brand": "BMW", "model": "X5", "generation": "G05", "facelift": False, "year_start": 2018, "year_end": 2023, 
     "category": "SUV-Premium", "segment": "Oberklasse-SUV", "body_style": "SUV", 
     "new_price": 75000, "hp": 340, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "BMW", "model": "X5", "generation": "G05 FL", "facelift": True, "year_start": 2023, "year_end": 2025, 
     "category": "SUV-Premium", "segment": "Oberklasse-SUV", "body_style": "SUV", 
     "new_price": 78000, "hp": 340, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0, "demand_factor": 1.08},
    
    # BMW M-Modelle (Performance)
    {"brand": "BMW", "model": "M2", "generation": "G87", "facelift": False, "year_start": 2022, "year_end": 2025, 
     "category": "Sportwagen", "segment": "Performance-Coupé", "body_style": "Coupé", 
     "new_price": 75000, "hp": 460, "engine_displacement": 3.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.35, "demand_factor": 1.25},
    
    {"brand": "BMW", "model": "M3", "generation": "G80", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Sportwagen", "segment": "Performance-Limousine", "body_style": "Limousine", 
     "new_price": 88000, "hp": 510, "engine_displacement": 3.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.4, "demand_factor": 1.3},
    
    {"brand": "BMW", "model": "M3 Competition", "generation": "G80", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Sportwagen", "segment": "Performance-Limousine", "body_style": "Limousine", 
     "new_price": 95000, "hp": 510, "engine_displacement": 3.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.5, "demand_factor": 1.4},
    
    {"brand": "BMW", "model": "M4", "generation": "G82", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Sportwagen", "segment": "Performance-Coupé", "body_style": "Coupé", 
     "new_price": 92000, "hp": 510, "engine_displacement": 3.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.4, "demand_factor": 1.35},
    
    {"brand": "BMW", "model": "M5", "generation": "F90", "facelift": False, "year_start": 2018, "year_end": 2023, 
     "category": "Supersportwagen", "segment": "Performance-Limousine", "body_style": "Limousine", 
     "new_price": 125000, "hp": 625, "engine_displacement": 4.4, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.5, "demand_factor": 1.4},
    
    # BMW i-Modelle (Elektro)
    {"brand": "BMW", "model": "i4", "generation": "G26", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Elektro-Premium", "segment": "Elektro-Gran-Coupé", "body_style": "Limousine", 
     "new_price": 60000, "hp": 340, "engine_displacement": 0.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.1, "demand_factor": 1.15},
    
    {"brand": "BMW", "model": "iX", "generation": "I20", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Elektro-SUV", "segment": "Elektro-Luxus-SUV", "body_style": "SUV", 
     "new_price": 85000, "hp": 326, "engine_displacement": 0.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.15, "demand_factor": 1.2},
    
    # ========================================
    # MERCEDES-BENZ
    # ========================================
    
    # Mercedes A-Klasse (W177)
    {"brand": "Mercedes", "model": "A-Klasse", "generation": "W177", "facelift": False, "year_start": 2018, "year_end": 2022, 
     "category": "Kompakt-Premium", "segment": "Premium-Kompaktklasse", "body_style": "Schrägheck", 
     "new_price": 33000, "hp": 163, "engine_displacement": 1.3, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "Mercedes", "model": "A-Klasse", "generation": "W177 FL", "facelift": True, "year_start": 2022, "year_end": 2025, 
     "category": "Kompakt-Premium", "segment": "Premium-Kompaktklasse", "body_style": "Schrägheck", 
     "new_price": 35000, "hp": 163, "engine_displacement": 1.3, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # Mercedes C-Klasse (W206 - neue Generation)
    {"brand": "Mercedes", "model": "C-Klasse", "generation": "W206", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Mittelklasse-Premium", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 52000, "hp": 204, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.05, "demand_factor": 1.1},
    
    # Mercedes E-Klasse (W213)
    {"brand": "Mercedes", "model": "E-Klasse", "generation": "W213", "facelift": False, "year_start": 2016, "year_end": 2020, 
     "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 62000, "hp": 194, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "Mercedes", "model": "E-Klasse", "generation": "W213 FL", "facelift": True, "year_start": 2020, "year_end": 2023, 
     "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 70000, "hp": 272, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # Mercedes S-Klasse (W223 - neue Generation)
    {"brand": "Mercedes", "model": "S-Klasse", "generation": "W223", "facelift": False, "year_start": 2020, "year_end": 2025, 
     "category": "Luxuslimousine", "segment": "Luxus-Limousine", "body_style": "Limousine", 
     "new_price": 120000, "hp": 435, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.1, "demand_factor": 1.15},
    
    # Mercedes GLA (H247)
    {"brand": "Mercedes", "model": "GLA", "generation": "H247", "facelift": False, "year_start": 2020, "year_end": 2025, 
     "category": "SUV-Kompakt", "segment": "Premium-Kompakt-SUV", "body_style": "SUV", 
     "new_price": 40000, "hp": 163, "engine_displacement": 1.3, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # Mercedes GLC (X253/X254)
    {"brand": "Mercedes", "model": "GLC", "generation": "X253", "facelift": False, "year_start": 2015, "year_end": 2019, 
     "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_style": "SUV", 
     "new_price": 52000, "hp": 211, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "Mercedes", "model": "GLC", "generation": "X253 FL", "facelift": True, "year_start": 2019, "year_end": 2022, 
     "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_style": "SUV", 
     "new_price": 56000, "hp": 258, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "Mercedes", "model": "GLC", "generation": "X254", "facelift": False, "year_start": 2022, "year_end": 2025, 
     "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_style": "SUV", 
     "new_price": 58000, "hp": 258, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.05, "demand_factor": 1.1},
    
    # Mercedes GLE (W167)
    {"brand": "Mercedes", "model": "GLE", "generation": "W167", "facelift": False, "year_start": 2019, "year_end": 2023, 
     "category": "SUV-Premium", "segment": "Oberklasse-SUV", "body_style": "SUV", 
     "new_price": 72000, "hp": 367, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "Mercedes", "model": "GLE", "generation": "W167 FL", "facelift": True, "year_start": 2023, "year_end": 2025, 
     "category": "SUV-Premium", "segment": "Oberklasse-SUV", "body_style": "SUV", 
     "new_price": 75000, "hp": 367, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # Mercedes G-Klasse (W463)
    {"brand": "Mercedes", "model": "G-Klasse", "generation": "W463", "facelift": False, "year_start": 2018, "year_end": 2025, 
     "category": "SUV-Offroad", "segment": "Geländewagen", "body_style": "SUV", 
     "new_price": 130000, "hp": 422, "engine_displacement": 4.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.45, "demand_factor": 1.5},
    
    # Mercedes AMG-Modelle
    {"brand": "Mercedes", "model": "AMG A 45 S", "generation": "W177", "facelift": False, "year_start": 2019, "year_end": 2025, 
     "category": "Sportwagen", "segment": "Performance-Kompaktklasse", "body_style": "Schrägheck", 
     "new_price": 58000, "hp": 421, "engine_displacement": 2.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.35, "demand_factor": 1.3},
    
    {"brand": "Mercedes", "model": "AMG C 63", "generation": "W206", "facelift": False, "year_start": 2022, "year_end": 2025, 
     "category": "Sportwagen", "segment": "Performance-Limousine", "body_style": "Limousine", 
     "new_price": 95000, "hp": 510, "engine_displacement": 4.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.4, "demand_factor": 1.35},
    
    {"brand": "Mercedes", "model": "AMG GT", "generation": "C190", "facelift": False, "year_start": 2014, "year_end": 2022, 
     "category": "Supersportwagen", "segment": "GT-Sportwagen", "body_style": "Coupé", 
     "new_price": 145000, "hp": 585, "engine_displacement": 4.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.5, "demand_factor": 1.45},
    
    # Mercedes EQ-Modelle (Elektro)
    {"brand": "Mercedes", "model": "EQA", "generation": "H243", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Elektro-SUV", "segment": "Elektro-Kompakt-SUV", "body_style": "SUV", 
     "new_price": 48000, "hp": 190, "engine_displacement": 0.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.05, "demand_factor": 1.1},
    
    {"brand": "Mercedes", "model": "EQS", "generation": "V297", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Elektro-Luxus", "segment": "Elektro-Luxuslimousine", "body_style": "Limousine", 
     "new_price": 110000, "hp": 333, "engine_displacement": 0.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.2, "demand_factor": 1.25},
    
    # ========================================
    # AUDI
    # ========================================
    
    # Audi A3 (8Y)
    {"brand": "Audi", "model": "A3", "generation": "8Y", "facelift": False, "year_start": 2020, "year_end": 2025, 
     "category": "Kompakt-Premium", "segment": "Premium-Kompaktklasse", "body_style": "Schrägheck", 
     "new_price": 34000, "hp": 150, "engine_displacement": 1.5, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # Audi A4 (B9)
    {"brand": "Audi", "model": "A4", "generation": "B9", "facelift": False, "year_start": 2016, "year_end": 2019, 
     "category": "Mittelklasse-Premium", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 40000, "hp": 150, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "Audi", "model": "A4", "generation": "B9 FL", "facelift": True, "year_start": 2019, "year_end": 2023, 
     "category": "Mittelklasse-Premium", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 42000, "hp": 150, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # Audi A6 (C8)
    {"brand": "Audi", "model": "A6", "generation": "C8", "facelift": False, "year_start": 2018, "year_end": 2024, 
     "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 58000, "hp": 204, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "Audi", "model": "A6", "generation": "C8 FL", "facelift": True, "year_start": 2024, "year_end": 2025, 
     "category": "Oberklasse", "segment": "Obere Mittelklasse", "body_style": "Limousine", 
     "new_price": 62000, "hp": 204, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0, "demand_factor": 1.05},
    
    # Audi A8 (D5)
    {"brand": "Audi", "model": "A8", "generation": "D5", "facelift": False, "year_start": 2017, "year_end": 2022, 
     "category": "Luxuslimousine", "segment": "Luxus-Limousine", "body_style": "Limousine", 
     "new_price": 92000, "hp": 340, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.05},
    
    {"brand": "Audi", "model": "A8", "generation": "D5 FL", "facelift": True, "year_start": 2022, "year_end": 2025, 
     "category": "Luxuslimousine", "segment": "Luxus-Limousine", "body_style": "Limousine", 
     "new_price": 95000, "hp": 340, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.05},
    
    # Audi Q3 (F3)
    {"brand": "Audi", "model": "Q3", "generation": "F3", "facelift": False, "year_start": 2018, "year_end": 2023, 
     "category": "SUV-Kompakt", "segment": "Premium-Kompakt-SUV", "body_style": "SUV", 
     "new_price": 36000, "hp": 150, "engine_displacement": 1.5, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "Audi", "model": "Q3", "generation": "F3 FL", "facelift": True, "year_start": 2023, "year_end": 2025, 
     "category": "SUV-Kompakt", "segment": "Premium-Kompakt-SUV", "body_style": "SUV", 
     "new_price": 38000, "hp": 150, "engine_displacement": 1.5, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # Audi Q5 (FY)
    {"brand": "Audi", "model": "Q5", "generation": "FY", "facelift": False, "year_start": 2017, "year_end": 2020, 
     "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_style": "SUV", 
     "new_price": 48000, "hp": 190, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    {"brand": "Audi", "model": "Q5", "generation": "FY FL", "facelift": True, "year_start": 2020, "year_end": 2025, 
     "category": "SUV-Mittel", "segment": "Premium-Mittelklasse-SUV", "body_style": "SUV", 
     "new_price": 52000, "hp": 204, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # Audi RS-Modelle (Performance)
    {"brand": "Audi", "model": "RS3", "generation": "8Y", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Sportwagen", "segment": "Performance-Kompaktklasse", "body_style": "Limousine", 
     "new_price": 62000, "hp": 400, "engine_displacement": 2.5, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.35, "demand_factor": 1.3},
    
    {"brand": "Audi", "model": "RS6 Avant", "generation": "C8", "facelift": False, "year_start": 2019, "year_end": 2025, 
     "category": "Supersportwagen", "segment": "Performance-Kombi", "body_style": "Kombi", 
     "new_price": 125000, "hp": 600, "engine_displacement": 4.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.5, "demand_factor": 1.45},
    
    # Audi e-tron (Elektro)
    {"brand": "Audi", "model": "Q4 e-tron", "generation": "E2", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Elektro-SUV", "segment": "Elektro-Kompakt-SUV", "body_style": "SUV", 
     "new_price": 48000, "hp": 204, "engine_displacement": 0.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.05, "demand_factor": 1.1},
    
    {"brand": "Audi", "model": "e-tron GT", "generation": "F8", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Elektro-Sportwagen", "segment": "Elektro-Gran-Turismo", "body_style": "Limousine", 
     "new_price": 105000, "hp": 530, "engine_displacement": 0.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.3, "demand_factor": 1.35},
    
    # ========================================
    # PORSCHE
    # ========================================
    
    # Porsche 911 (992)
    {"brand": "Porsche", "model": "911 Carrera", "generation": "992", "facelift": False, "year_start": 2019, "year_end": 2024, 
     "category": "Supersportwagen", "segment": "Ikonen-Sportwagen", "body_style": "Coupé", 
     "new_price": 130000, "hp": 385, "engine_displacement": 3.0, 
     "special_edition": True, "premium_package": False, "rarity_multiplier": 1.4, "demand_factor": 1.4},
    
    {"brand": "Porsche", "model": "911 Carrera", "generation": "992 FL", "facelift": True, "year_start": 2024, "year_end": 2025, 
     "category": "Supersportwagen", "segment": "Ikonen-Sportwagen", "body_style": "Coupé", 
     "new_price": 138000, "hp": 394, "engine_displacement": 3.0, 
     "special_edition": True, "premium_package": False, "rarity_multiplier": 1.45, "demand_factor": 1.5},
    
    {"brand": "Porsche", "model": "911 Turbo S", "generation": "992", "facelift": False, "year_start": 2020, "year_end": 2025, 
     "category": "Supersportwagen", "segment": "Turbo-Sportwagen", "body_style": "Coupé", 
     "new_price": 240000, "hp": 650, "engine_displacement": 3.8, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.6, "demand_factor": 1.6},
    
    # Porsche 718 Cayman/Boxster
    {"brand": "Porsche", "model": "718 Cayman", "generation": "982", "facelift": False, "year_start": 2016, "year_end": 2023, 
     "category": "Sportwagen", "segment": "Mittelmotor-Sportwagen", "body_style": "Coupé", 
     "new_price": 62000, "hp": 300, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.2, "demand_factor": 1.15},
    
    {"brand": "Porsche", "model": "718 Cayman GTS", "generation": "982", "facelift": False, "year_start": 2017, "year_end": 2023, 
     "category": "Sportwagen", "segment": "Mittelmotor-Sportwagen", "body_style": "Coupé", 
     "new_price": 82000, "hp": 400, "engine_displacement": 4.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.35, "demand_factor": 1.3},
    
    # Porsche Cayenne (E3)
    {"brand": "Porsche", "model": "Cayenne", "generation": "E3", "facelift": False, "year_start": 2017, "year_end": 2023, 
     "category": "SUV-Premium", "segment": "Luxus-SUV", "body_style": "SUV", 
     "new_price": 78000, "hp": 340, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.15, "demand_factor": 1.1},
    
    {"brand": "Porsche", "model": "Cayenne", "generation": "E3 FL", "facelift": True, "year_start": 2023, "year_end": 2025, 
     "category": "SUV-Premium", "segment": "Luxus-SUV", "body_style": "SUV", 
     "new_price": 82000, "hp": 340, "engine_displacement": 3.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.15, "demand_factor": 1.15},
    
    # Porsche Macan
    {"brand": "Porsche", "model": "Macan", "generation": "95B", "facelift": False, "year_start": 2014, "year_end": 2018, 
     "category": "SUV-Sport", "segment": "Sport-SUV", "body_style": "SUV", 
     "new_price": 58000, "hp": 252, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.1},
    
    {"brand": "Porsche", "model": "Macan", "generation": "95B FL", "facelift": True, "year_start": 2018, "year_end": 2024, 
     "category": "SUV-Sport", "segment": "Sport-SUV", "body_style": "SUV", 
     "new_price": 62000, "hp": 265, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.1},
    
    # Porsche Taycan (Elektro)
    {"brand": "Porsche", "model": "Taycan", "generation": "Y1A", "facelift": False, "year_start": 2019, "year_end": 2023, 
     "category": "Elektro-Sportwagen", "segment": "Elektro-Gran-Turismo", "body_style": "Limousine", 
     "new_price": 92000, "hp": 408, "engine_displacement": 0.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.25, "demand_factor": 1.25},
    
    {"brand": "Porsche", "model": "Taycan", "generation": "Y1A FL", "facelift": True, "year_start": 2023, "year_end": 2025, 
     "category": "Elektro-Sportwagen", "segment": "Elektro-Gran-Turismo", "body_style": "Limousine", 
     "new_price": 95000, "hp": 408, "engine_displacement": 0.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.3, "demand_factor": 1.3},
    
    {"brand": "Porsche", "model": "Taycan Turbo S", "generation": "Y1A", "facelift": False, "year_start": 2019, "year_end": 2025, 
     "category": "Elektro-Sportwagen", "segment": "Elektro-Gran-Turismo", "body_style": "Limousine", 
     "new_price": 190000, "hp": 761, "engine_displacement": 0.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.5, "demand_factor": 1.5},
    
    # ========================================
    # TESLA
    # ========================================
    
    {"brand": "Tesla", "model": "Model 3", "generation": "Highland", "facelift": True, "year_start": 2023, "year_end": 2025, 
     "category": "Elektro-Mittelklasse", "segment": "Elektro-Limousine", "body_style": "Limousine", 
     "new_price": 42000, "hp": 283, "engine_displacement": 0.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.1, "demand_factor": 1.15},
    
    {"brand": "Tesla", "model": "Model 3 Performance", "generation": "Highland", "facelift": True, "year_start": 2023, "year_end": 2025, 
     "category": "Elektro-Sportwagen", "segment": "Elektro-Performance", "body_style": "Limousine", 
     "new_price": 54000, "hp": 460, "engine_displacement": 0.0, 
     "special_edition": True, "premium_package": False, "rarity_multiplier": 1.25, "demand_factor": 1.25},
    
    {"brand": "Tesla", "model": "Model S", "generation": "Plaid", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Elektro-Oberklasse", "segment": "Elektro-Luxuslimousine", "body_style": "Limousine", 
     "new_price": 110000, "hp": 1020, "engine_displacement": 0.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.4, "demand_factor": 1.4},
    
    {"brand": "Tesla", "model": "Model X", "generation": "Plaid", "facelift": False, "year_start": 2021, "year_end": 2025, 
     "category": "Elektro-SUV", "segment": "Elektro-Luxus-SUV", "body_style": "SUV", 
     "new_price": 120000, "hp": 1020, "engine_displacement": 0.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.4, "demand_factor": 1.45},
    
    {"brand": "Tesla", "model": "Model Y", "generation": "Juniper", "facelift": True, "year_start": 2024, "year_end": 2025, 
     "category": "Elektro-SUV", "segment": "Elektro-Kompakt-SUV", "body_style": "SUV", 
     "new_price": 48000, "hp": 378, "engine_displacement": 0.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.15, "demand_factor": 1.2},
    
    # ========================================
    # FERRARI
    # ========================================
    
    {"brand": "Ferrari", "model": "F8 Tributo", "generation": "F142", "facelift": False, "year_start": 2019, "year_end": 2023, 
     "category": "Supersportwagen", "segment": "Supersportwagen", "body_style": "Coupé", 
     "new_price": 280000, "hp": 720, "engine_displacement": 3.9, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.7, "demand_factor": 1.7},
    
    {"brand": "Ferrari", "model": "Roma", "generation": "F169", "facelift": False, "year_start": 2020, "year_end": 2025, 
     "category": "Supersportwagen", "segment": "Gran Turismo", "body_style": "Coupé", 
     "new_price": 235000, "hp": 620, "engine_displacement": 3.9, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.6, "demand_factor": 1.6},
    
    {"brand": "Ferrari", "model": "SF90 Stradale", "generation": "F173", "facelift": False, "year_start": 2019, "year_end": 2025, 
     "category": "Hypersportwagen", "segment": "Hybrid-Supersportwagen", "body_style": "Coupé", 
     "new_price": 500000, "hp": 1000, "engine_displacement": 4.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 2.0, "demand_factor": 2.0},
    
    # ========================================
    # LAMBORGHINI
    # ========================================
    
    {"brand": "Lamborghini", "model": "Huracán", "generation": "LB724", "facelift": False, "year_start": 2014, "year_end": 2019, 
     "category": "Supersportwagen", "segment": "Supersportwagen", "body_style": "Coupé", 
     "new_price": 210000, "hp": 610, "engine_displacement": 5.2, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.65, "demand_factor": 1.6},
    
    {"brand": "Lamborghini", "model": "Huracán EVO", "generation": "LB724 FL", "facelift": True, "year_start": 2019, "year_end": 2024, 
     "category": "Supersportwagen", "segment": "Supersportwagen", "body_style": "Coupé", 
     "new_price": 220000, "hp": 640, "engine_displacement": 5.2, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.7, "demand_factor": 1.65},
    
    {"brand": "Lamborghini", "model": "Urus", "generation": "LB736", "facelift": False, "year_start": 2018, "year_end": 2022, 
     "category": "SUV-Super", "segment": "Super-SUV", "body_style": "SUV", 
     "new_price": 210000, "hp": 650, "engine_displacement": 4.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.65, "demand_factor": 1.65},
    
    {"brand": "Lamborghini", "model": "Urus S", "generation": "LB736 FL", "facelift": True, "year_start": 2022, "year_end": 2025, 
     "category": "SUV-Super", "segment": "Super-SUV", "body_style": "SUV", 
     "new_price": 220000, "hp": 666, "engine_displacement": 4.0, 
     "special_edition": True, "premium_package": True, "rarity_multiplier": 1.7, "demand_factor": 1.7},
    
    # ========================================
    # WEITERE MARKEN (Auswahl)
    # ========================================
    
    # Opel Corsa
    {"brand": "Opel", "model": "Corsa", "generation": "F", "facelift": False, "year_start": 2019, "year_end": 2025, 
     "category": "Kleinwagen", "segment": "Kleinwagen", "body_style": "Kleinwagen", 
     "new_price": 18000, "hp": 100, "engine_displacement": 1.2, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.0},
    
    # Ford Mustang
    {"brand": "Ford", "model": "Mustang GT", "generation": "S650", "facelift": False, "year_start": 2023, "year_end": 2025, 
     "category": "Sportwagen", "segment": "Muscle Car", "body_style": "Coupé", 
     "new_price": 55000, "hp": 486, "engine_displacement": 5.0, 
     "special_edition": True, "premium_package": False, "rarity_multiplier": 1.3, "demand_factor": 1.25},
    
    # Mazda MX-5
    {"brand": "Mazda", "model": "MX-5", "generation": "ND2", "facelift": True, "year_start": 2018, "year_end": 2025, 
     "category": "Roadster", "segment": "Roadster", "body_style": "Roadster", 
     "new_price": 32000, "hp": 184, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.15, "demand_factor": 1.15},
    
    # Mini Cooper
    {"brand": "Mini", "model": "Cooper S", "generation": "F56 FL", "facelift": True, "year_start": 2021, "year_end": 2025, 
     "category": "Kleinwagen", "segment": "Premium-Kleinwagen", "body_style": "Kleinwagen", 
     "new_price": 28000, "hp": 178, "engine_displacement": 2.0, 
     "special_edition": False, "premium_package": False, "rarity_multiplier": 1.1, "demand_factor": 1.1},
]

# ANGEPASSTE BASE HOURLY RATES (realistischer für Carsharing)
BASE_HOURLY_RATES = {
    "Kleinstwagen": 8.0,
    "Kleinwagen": 10.0,
    "Kompakt": 14.0,
    "Kompakt-Premium": 18.0,
    "Mittelklasse": 20.0,
    "Mittelklasse-Premium": 25.0,
    "Oberklasse": 35.0,
    "Luxuslimousine": 60.0,
    "Ultraluxus": 120.0,
    "Hypersportwagen": 250.0,
    "Coupé-Premium": 28.0,
    "Luxus-Coupé": 50.0,
    "Cabrio-Klein": 15.0,
    "Cabrio-Premium": 32.0,
    "Luxus-Cabrio": 65.0,
    "Cabrio-Sport": 45.0,
    "Roadster": 35.0,
    "Luxus-Roadster": 75.0,
    "SUV-Klein": 15.0,
    "SUV-Kompakt": 18.0,
    "SUV-Mittel": 25.0,
    "SUV-Sport": 38.0,
    "SUV-Premium": 42.0,
    "SUV-Luxus": 65.0,
    "SUV-Ultraluxus": 110.0,
    "SUV-Super": 90.0,
    "SUV-Offroad": 45.0,
    "SUV-Coupé": 35.0,
    "SUV-Cabrio": 38.0,
    "Sport": 40.0,
    "Sportwagen": 65.0,
    "Luxus-Sportwagen": 95.0,
    "Supersportwagen": 150.0,
    "Transporter": 18.0,
    "Hochdachkombi": 15.0,
    "Kompakt-Van": 16.0,
    "Elektro-Kompakt": 16.0,
    "Elektro-Mittelklasse": 22.0,
    "Elektro-Premium": 30.0,
    "Elektro-Oberklasse": 45.0,
    "Elektro-Luxus": 65.0,
    "Elektro-SUV": 35.0,
    "Elektro-Sportwagen": 75.0,
}
