const API_BASE_URL = '/api';

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

export const api = {
  fetchCityTrends,
  fetchGrowthRates,
  fetchMarketHeatmap,
};

export default api;
