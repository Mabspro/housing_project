-- Housing Market Data Schema

-- BLS Housing CPI Data
CREATE TABLE IF NOT EXISTS bls_housing_cpi (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    housing_cpi DECIMAL(10, 2),
    shelter_cpi DECIMAL(10, 2),
    fuels_utilities_cpi DECIMAL(10, 2),
    household_furnishings_cpi DECIMAL(10, 2),
    -- Month-over-Month changes
    housing_cpi_mom DECIMAL(6, 3),
    shelter_cpi_mom DECIMAL(6, 3),
    fuels_utilities_mom DECIMAL(6, 3),
    furnishings_mom DECIMAL(6, 3),
    -- Year-over-Year changes
    housing_cpi_yoy DECIMAL(6, 3),
    shelter_cpi_yoy DECIMAL(6, 3),
    fuels_utilities_yoy DECIMAL(6, 3),
    furnishings_yoy DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

-- Census Housing Data
CREATE TABLE IF NOT EXISTS census_housing (
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
CREATE TABLE IF NOT EXISTS kaggle_housing_prices (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    us_national DECIMAL(10, 2),
    city_composite_20 DECIMAL(10, 2),
    city_composite_10 DECIMAL(10, 2),
    -- Month-over-Month changes
    us_national_mom DECIMAL(6, 3),
    city_20_mom DECIMAL(6, 3),
    city_10_mom DECIMAL(6, 3),
    -- Year-over-Year changes
    us_national_yoy DECIMAL(6, 3),
    city_20_yoy DECIMAL(6, 3),
    city_10_yoy DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

-- Wages by Education
CREATE TABLE IF NOT EXISTS wages_education (
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
CREATE TABLE IF NOT EXISTS interest_rates (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    fed_funds_target DECIMAL(5, 2),
    fed_funds_upper DECIMAL(5, 2),
    fed_funds_lower DECIMAL(5, 2),
    effective_rate DECIMAL(5, 2),
    real_gdp_change DECIMAL(5, 2),
    unemployment_rate DECIMAL(5, 2),
    inflation_rate DECIMAL(5, 2),
    -- Month-over-Month changes
    target_rate_mom DECIMAL(6, 3),
    effective_rate_mom DECIMAL(6, 3),
    -- Year-over-Year changes
    target_rate_yoy DECIMAL(6, 3),
    effective_rate_yoy DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

-- Zillow Housing Data
CREATE TABLE IF NOT EXISTS zillow_housing (
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
CREATE TABLE IF NOT EXISTS zillow_home_value_index (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    state VARCHAR(50) NOT NULL,
    home_value_index DECIMAL(12, 2),
    hvi_mom DECIMAL(6, 3),
    hvi_yoy DECIMAL(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, state)
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_bls_date ON bls_housing_cpi(date);
CREATE INDEX IF NOT EXISTS idx_census_state_year ON census_housing(state, year);
CREATE INDEX IF NOT EXISTS idx_housing_prices_date ON kaggle_housing_prices(date);
CREATE INDEX IF NOT EXISTS idx_wages_year ON wages_education(year);
CREATE INDEX IF NOT EXISTS idx_interest_rates_date ON interest_rates(date);
CREATE INDEX IF NOT EXISTS idx_zillow_date_region ON zillow_housing(date, region_name);
CREATE INDEX IF NOT EXISTS idx_zillow_hvi_date_state ON zillow_home_value_index(date, state);

-- Add comments for documentation
COMMENT ON TABLE bls_housing_cpi IS 'Monthly housing-related Consumer Price Index data from BLS';
COMMENT ON TABLE census_housing IS 'Annual housing statistics by state from Census Bureau';
COMMENT ON TABLE kaggle_housing_prices IS 'Historical housing prices from Kaggle dataset';
COMMENT ON TABLE wages_education IS 'Wages by education level and demographic groups';
COMMENT ON TABLE interest_rates IS 'Federal Reserve interest rates and related economic indicators';
COMMENT ON TABLE zillow_housing IS 'Zillow housing prices by region';
COMMENT ON TABLE zillow_home_value_index IS 'Zillow Home Value Index by state';
