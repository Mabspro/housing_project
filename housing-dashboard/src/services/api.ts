const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8002/api';

// Interfaces for price trends data
export interface CityTrendsData {
  date: string[];
  values: { [city: string]: number[] };
}

export interface GrowthRatesData {
  date: string[];
  values: { [market: string]: number[] };
}

export interface MarketHeatmapData {
  markets: string[];
  growthRates: number[];
}

// Interfaces for rental data
export interface RentalTrendsData {
  date: string[];
  values: { [city: string]: number[] };
}

export interface RentalGrowthData {
  date: string[];
  values: { [market: string]: number[] };
}

export interface RentalHeatmapData {
  markets: string[];
  growthRates: number[];
}

export interface HousingAffordabilityData {
  dates: string[];
  regions: string[];
  metrics: {
    homePrices: { [region: string]: number[] };
    medianWages: { [region: string]: number[] };
    interestRates: { [region: string]: number[] };
    priceToIncomeRatios: { [region: string]: number[] };
  };
  metadata: {
    totalRecords: number;
    timestamp: string;
  };
}

// Price trends API calls
export const fetchCityTrends = async (): Promise<CityTrendsData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/city-trends`);
    if (!response.ok) {
      throw new Error('Failed to fetch city trends data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching city trends:', error);
    throw error;
  }
};

export const fetchGrowthRates = async (): Promise<GrowthRatesData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/growth-rates`);
    if (!response.ok) {
      throw new Error('Failed to fetch growth rates data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching growth rates:', error);
    throw error;
  }
};

export const fetchMarketHeatmap = async (): Promise<MarketHeatmapData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/market-heatmap`);
    if (!response.ok) {
      throw new Error('Failed to fetch market heatmap data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching market heatmap:', error);
    throw error;
  }
};

// Rental data API calls
export const fetchRentalTrends = async (): Promise<RentalTrendsData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/rental-trends`);
    if (!response.ok) {
      throw new Error('Failed to fetch rental trends data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching rental trends:', error);
    throw error;
  }
};

export const fetchRentalGrowth = async (): Promise<RentalGrowthData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/rental-growth`);
    if (!response.ok) {
      throw new Error('Failed to fetch rental growth data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching rental growth:', error);
    throw error;
  }
};

export const fetchRentalHeatmap = async (): Promise<RentalHeatmapData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/rental-heatmap`);
    if (!response.ok) {
      throw new Error('Failed to fetch rental heatmap data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching rental heatmap:', error);
    throw error;
  }
};

export const fetchHousingAffordability = async (): Promise<HousingAffordabilityData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/housing-affordability`);
    if (!response.ok) {
      throw new Error('Failed to fetch housing affordability data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching housing affordability:', error);
    throw error;
  }
};

export const api = {
  // Price trends endpoints
  fetchCityTrends,
  fetchGrowthRates,
  fetchMarketHeatmap,
  // Rental data endpoints
  fetchRentalTrends,
  fetchRentalGrowth,
  fetchRentalHeatmap,
  // Other endpoints
  fetchHousingAffordability,
};

export default api;
