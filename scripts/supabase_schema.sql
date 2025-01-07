-- Enable RLS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Housing Market Data Schema
DROP TABLE IF EXISTS public.bls_housing_cpi CASCADE;
DROP TABLE IF EXISTS public.census_housing CASCADE;
DROP TABLE IF EXISTS public.kaggle_housing_prices CASCADE;
DROP TABLE IF EXISTS public.wages_education CASCADE;
DROP TABLE IF EXISTS public.interest_rates CASCADE;
DROP TABLE IF EXISTS public.zillow_housing CASCADE;
DROP TABLE IF EXISTS public.zillow_home_value_index CASCADE;

-- BLS Housing CPI Data
CREATE TABLE public.bls_housing_cpi (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    housing_cpi DECIMAL(10, 2),
    shelter_cpi DECIMAL(10, 2),
    fuels_utilities_cpi DECIMAL(10, 2),
    household_furnishings_cpi DECIMAL(10, 2),
    housing_cpi_mom DECIMAL(6, 3),
    shelter_cpi_mom DECIMAL(6, 3),
    fuels_utilities_mom DECIMAL(6, 3),
    furnishings_mom DECIMAL(6, 3),
    housing_cpi_yoy DECIMAL(6, 3),
    shelter_cpi_yoy DECIMAL(6, 3),
    fuels_utilities_yoy DECIMAL(6, 3),
    furnishings_yoy DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

-- Census Housing Data
CREATE TABLE public.census_housing (
    id SERIAL PRIMARY KEY,
    state VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    total_housing_units INTEGER,
    occupied_units INTEGER,
    vacant_units INTEGER,
    owner_occupied INTEGER,
    renter_occupied INTEGER,
    median_home_value DECIMAL(12, 2),
    median_monthly_cost DECIMAL(8, 2),
    vacancy_rate DECIMAL(5, 2),
    homeownership_rate DECIMAL(5, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(state, year)
);

-- Kaggle Housing Prices
CREATE TABLE public.kaggle_housing_prices (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    us_national DECIMAL(10, 2),
    city_composite_20 DECIMAL(10, 2),
    city_composite_10 DECIMAL(10, 2),
    us_national_mom DECIMAL(6, 3),
    city_20_mom DECIMAL(6, 3),
    city_10_mom DECIMAL(6, 3),
    us_national_yoy DECIMAL(6, 3),
    city_20_yoy DECIMAL(6, 3),
    city_10_yoy DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

-- Wages by Education
CREATE TABLE public.wages_education (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    education_level VARCHAR(50) NOT NULL,
    demographic_group VARCHAR(50) NOT NULL,
    wage_value DECIMAL(10, 2),
    wage_yoy_change DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(year, education_level, demographic_group)
);

-- Interest Rates
CREATE TABLE public.interest_rates (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    fed_funds_target DECIMAL(5, 2),
    fed_funds_upper DECIMAL(5, 2),
    fed_funds_lower DECIMAL(5, 2),
    effective_rate DECIMAL(5, 2),
    real_gdp_change DECIMAL(5, 2),
    unemployment_rate DECIMAL(5, 2),
    inflation_rate DECIMAL(5, 2),
    target_rate_mom DECIMAL(6, 3),
    effective_rate_mom DECIMAL(6, 3),
    target_rate_yoy DECIMAL(6, 3),
    effective_rate_yoy DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

-- Zillow Housing Data
CREATE TABLE public.zillow_housing (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    region_name VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    metro_area VARCHAR(100),
    county_name VARCHAR(100),
    price DECIMAL(12, 2),
    price_mom DECIMAL(6, 3),
    price_yoy DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, region_name)
);

-- Zillow Home Value Index
CREATE TABLE public.zillow_home_value_index (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    state VARCHAR(50) NOT NULL,
    home_value_index DECIMAL(12, 2),
    hvi_mom DECIMAL(6, 3),
    hvi_yoy DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, state)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_bls_date ON public.bls_housing_cpi(date);
CREATE INDEX IF NOT EXISTS idx_census_state_year ON public.census_housing(state, year);
CREATE INDEX IF NOT EXISTS idx_housing_prices_date ON public.kaggle_housing_prices(date);
CREATE INDEX IF NOT EXISTS idx_wages_year ON public.wages_education(year);
CREATE INDEX IF NOT EXISTS idx_interest_rates_date ON public.interest_rates(date);
CREATE INDEX IF NOT EXISTS idx_zillow_date_region ON public.zillow_housing(date, region_name);
CREATE INDEX IF NOT EXISTS idx_zillow_hvi_date_state ON public.zillow_home_value_index(date, state);

-- Enable row level security but allow all operations
ALTER TABLE public.bls_housing_cpi ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.census_housing ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.kaggle_housing_prices ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.wages_education ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.interest_rates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.zillow_housing ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.zillow_home_value_index ENABLE ROW LEVEL SECURITY;

-- Create policies to allow all operations
CREATE POLICY "Allow all" ON public.bls_housing_cpi FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.census_housing FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.kaggle_housing_prices FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.wages_education FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.interest_rates FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.zillow_housing FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.zillow_home_value_index FOR ALL USING (true);
