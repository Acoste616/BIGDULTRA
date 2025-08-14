-- =====================================================
-- ULTRA BIGDECODER 3.0 - EXPERT KNOWLEDGE TABLES
-- Tabele z wiedzą ekspercką o polskim rynku EV
-- =====================================================

-- 1. DOPŁATY I PROGRAMY WSPARCIA
CREATE TABLE IF NOT EXISTS ev_subsidies_poland (
    id SERIAL PRIMARY KEY,
    program_name VARCHAR(255) NOT NULL,
    program_type VARCHAR(100), -- national/local/nfos
    max_amount_pln DECIMAL(10,2),
    eligibility_criteria JSONB, -- {"max_price": 225000, "customer_type": ["individual", "business"]}
    requirements TEXT,
    valid_from DATE,
    valid_until DATE,
    region VARCHAR(100), -- null for national, city name for local
    additional_benefits JSONB,
    application_process TEXT,
    documentation_required JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. PRZEPISY PODATKOWE DLA FIRM
CREATE TABLE IF NOT EXISTS tax_regulations_business (
    id SERIAL PRIMARY KEY,
    regulation_type VARCHAR(100), -- vat/depreciation/bik/excise
    description TEXT,
    benefit_amount VARCHAR(255), -- "0% VAT", "100% depreciation", etc.
    applies_to VARCHAR(100), -- BEV/PHEV/all_ev
    calculation_formula TEXT,
    example_calculation JSONB,
    legal_basis VARCHAR(255), -- ustawa/rozporządzenie
    valid_from DATE,
    valid_until DATE,
    special_conditions JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. INTEGRACJA Z PANELAMI FOTOWOLTAICZNYMI
CREATE TABLE IF NOT EXISTS solar_panels_compatibility (
    id SERIAL PRIMARY KEY,
    system_type VARCHAR(100), -- home_charging/powerwall/v2g
    pv_system_size_kwp DECIMAL(5,2),
    daily_production_kwh DECIMAL(6,2),
    ev_range_per_day_km INTEGER,
    investment_cost_pln DECIMAL(10,2),
    roi_years DECIMAL(3,1),
    compatibility_tesla_models JSONB, -- ["Model 3", "Model Y"]
    technical_requirements TEXT,
    installation_partners JSONB,
    government_support JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 4. INFRASTRUKTURA ŁADOWANIA W POLSCE
CREATE TABLE IF NOT EXISTS charging_infrastructure_pl (
    id SERIAL PRIMARY KEY,
    network_name VARCHAR(100),
    station_type VARCHAR(50), -- supercharger/ccs/chademo/type2
    location_city VARCHAR(100),
    location_address TEXT,
    coordinates JSONB, -- {"lat": 52.23, "lng": 21.01}
    max_power_kw INTEGER,
    connectors_count INTEGER,
    price_per_kwh DECIMAL(5,2),
    price_time_based JSONB, -- {"peak": 2.10, "off_peak": 1.45}
    availability_24h BOOLEAN,
    payment_methods JSONB,
    amenities JSONB, -- ["restaurant", "shopping", "restrooms"]
    tesla_compatible BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 5. KORZYŚCI DLA FLOT FIRMOWYCH
CREATE TABLE IF NOT EXISTS company_fleet_benefits (
    id SERIAL PRIMARY KEY,
    benefit_type VARCHAR(100),
    description TEXT,
    savings_calculation JSONB,
    minimum_fleet_size INTEGER,
    applicable_models JSONB,
    tax_advantages TEXT,
    operational_benefits TEXT,
    case_study_example JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 6. PARAMETRY KALKULACJI LEASINGU
CREATE TABLE IF NOT EXISTS leasing_calculator_params (
    id SERIAL PRIMARY KEY,
    provider_name VARCHAR(100),
    vehicle_category VARCHAR(50), -- passenger/commercial
    down_payment_percent DECIMAL(5,2),
    interest_rate_percent DECIMAL(5,2),
    lease_term_months INTEGER,
    residual_value_percent DECIMAL(5,2),
    insurance_included BOOLEAN,
    service_package_available BOOLEAN,
    early_termination_fee DECIMAL(10,2),
    special_ev_conditions JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 7. UBEZPIECZENIA DLA EV
CREATE TABLE IF NOT EXISTS insurance_providers_ev (
    id SERIAL PRIMARY KEY,
    provider_name VARCHAR(100),
    oc_annual_cost_from DECIMAL(10,2),
    oc_annual_cost_to DECIMAL(10,2),
    ac_annual_cost_from DECIMAL(10,2),
    ac_annual_cost_to DECIMAL(10,2),
    ev_specific_coverage JSONB, -- ["battery", "charging_cable", "autopilot_damage"]
    discount_for_tesla DECIMAL(5,2),
    online_purchase_discount DECIMAL(5,2),
    assistance_package TEXT,
    claims_process_time_days INTEGER,
    customer_rating DECIMAL(2,1),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 8. SIEĆ SERWISOWA TESLA W POLSCE
CREATE TABLE IF NOT EXISTS service_network_tesla (
    id SERIAL PRIMARY KEY,
    location_type VARCHAR(50), -- service_center/mobile_service/body_shop
    city VARCHAR(100),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    services_offered JSONB,
    working_hours JSONB,
    mobile_service_radius_km INTEGER,
    average_wait_time_days INTEGER,
    customer_satisfaction DECIMAL(2,1),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 9. DANE O WYDAJNOŚCI ZIMOWEJ
CREATE TABLE IF NOT EXISTS winter_performance_data (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100),
    temperature_celsius INTEGER,
    range_loss_percent DECIMAL(5,2),
    heating_consumption_kw DECIMAL(4,2),
    charging_speed_reduction_percent DECIMAL(5,2),
    heat_pump_equipped BOOLEAN,
    preconditioning_time_minutes INTEGER,
    real_world_tips JSONB,
    test_conditions TEXT,
    source VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 10. SZABLONY KALKULACJI TCO
CREATE TABLE IF NOT EXISTS tco_calculation_templates (
    id SERIAL PRIMARY KEY,
    customer_segment VARCHAR(100), -- private/business/fleet
    annual_mileage_km INTEGER,
    ownership_period_years INTEGER,
    fuel_cost_per_100km DECIMAL(6,2),
    electricity_cost_per_100km DECIMAL(6,2),
    service_cost_annual_ice DECIMAL(10,2),
    service_cost_annual_ev DECIMAL(10,2),
    depreciation_ice_percent DECIMAL(5,2),
    depreciation_ev_percent DECIMAL(5,2),
    insurance_difference DECIMAL(10,2),
    tax_benefits_annual DECIMAL(10,2),
    total_savings_period DECIMAL(12,2),
    break_even_months INTEGER,
    assumptions JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- INSERTOWANIE PRZYKŁADOWYCH DANYCH
-- =====================================================

-- Dopłaty
INSERT INTO ev_subsidies_poland (program_name, program_type, max_amount_pln, eligibility_criteria, requirements, valid_from, valid_until, region) VALUES
('Mój Elektryk', 'national', 27000, '{"max_price": 225000, "customer_type": ["individual"]}', 'Nowy samochód BEV, pierwsza rejestracja w Polsce', '2024-01-01', '2025-12-31', NULL),
('Zielony Samochód', 'nfos', 70000, '{"customer_type": ["business"], "min_fleet": 1}', 'Firma z siedzibą w Polsce, samochód na działalność', '2024-01-01', '2025-12-31', NULL),
('Karta Warszawiaka EV', 'local', 10000, '{"residence": "Warsaw", "card_holder": true}', 'Zameldowanie w Warszawie, posiadanie Karty Warszawiaka', '2024-01-01', '2024-12-31', 'Warszawa'),
('KAWKA Kraków', 'local', 12000, '{"residence": "Krakow", "old_car_disposal": true}', 'Złomowanie starego auta, zameldowanie w Krakowie', '2024-01-01', '2024-12-31', 'Kraków');

-- Przepisy podatkowe
INSERT INTO tax_regulations_business (regulation_type, description, benefit_amount, applies_to, valid_from, valid_until) VALUES
('VAT', 'Zerowa stawka VAT na samochody elektryczne', '0%', 'BEV', '2024-01-01', '2026-12-31'),
('Depreciation', 'Jednorazowa amortyzacja do 225,000 PLN', '100%', 'BEV', '2023-01-01', NULL),
('BIK', 'Obniżona stawka dla samochodów elektrycznych', '1% monthly', 'BEV', '2022-01-01', NULL),
('Excise', 'Brak akcyzy dla samochodów elektrycznych', '0%', 'BEV', '2020-01-01', NULL);

-- Infrastruktura ładowania
INSERT INTO charging_infrastructure_pl (network_name, station_type, location_city, max_power_kw, connectors_count, price_per_kwh, tesla_compatible) VALUES
('Tesla Supercharger', 'supercharger', 'Warszawa', 250, 8, 1.75, true),
('Tesla Supercharger', 'supercharger', 'Kraków', 250, 6, 1.75, true),
('Tesla Supercharger', 'supercharger', 'Poznań', 250, 8, 1.75, true),
('Orlen Charge', 'ccs', 'Warszawa', 150, 4, 2.39, true),
('GreenWay', 'ccs', 'Katowice', 120, 2, 2.19, true),
('Ionity', 'ccs', 'Wrocław', 350, 6, 2.85, true);

-- Wydajność zimowa
INSERT INTO winter_performance_data (model_name, temperature_celsius, range_loss_percent, heat_pump_equipped) VALUES
('Model 3 LR', -10, 25, false),
('Model Y LR', -10, 20, true),
('Model 3 SR', -10, 30, false),
('Model Y SR', -10, 22, true),
('Model 3 LR', -20, 35, false),
('Model Y LR', -20, 28, true);

-- Kalkulacje TCO
INSERT INTO tco_calculation_templates (customer_segment, annual_mileage_km, ownership_period_years, fuel_cost_per_100km, electricity_cost_per_100km, total_savings_period) VALUES
('private', 15000, 5, 45.00, 12.00, 49500),
('business', 30000, 3, 45.00, 12.00, 59400),
('fleet', 50000, 4, 45.00, 12.00, 132000);

-- =====================================================
-- INDEKSY DLA WYDAJNOŚCI
-- =====================================================

CREATE INDEX idx_subsidies_valid ON ev_subsidies_poland(valid_from, valid_until);
CREATE INDEX idx_charging_city ON charging_infrastructure_pl(location_city);
CREATE INDEX idx_charging_tesla ON charging_infrastructure_pl(tesla_compatible);
CREATE INDEX idx_winter_model ON winter_performance_data(model_name);
CREATE INDEX idx_tco_segment ON tco_calculation_templates(customer_segment);
