# Housing Market Analysis Dashboard

Interactive visualization dashboard for housing market analysis, featuring price trends, growth rates, and market comparisons across different regions.

## Features

- City Trends Chart showing historical price data
- Growth Rates Chart displaying year-over-year changes
- Market Heatmap showing current market performance
- Interactive time series visualizations
- Regional market comparisons
- Statistical insights

## Project Structure

```
housing-project/
├── backups/              # Database backups
├── data/                 # Data storage
│   ├── bls/             # Bureau of Labor Statistics data
│   ├── census/          # Census Bureau data
│   └── kaggle/          # Kaggle datasets
├── housing-dashboard/    # Main application
│   ├── src/             # React frontend
│   │   └── services/    # API services
│   ├── api/             # FastAPI backend
│   │   └── main.py      # API endpoints
│   └── public/          # Static assets
└── scripts/             # ETL and utility scripts
    ├── scrapers/        # Data extraction scripts
    ├── data_cleaning.py # Data cleaning utilities
    ├── process_datasets.py # Data processing pipeline
    ├── drop_create_db.py  # Database management
    ├── backup_db.py     # Database backup utility
    └── load_to_db.py    # Database loading
```

## ETL Pipeline

1. **Extract**: Data collection from multiple sources
   - BLS housing data (CPI, costs)
   - Census housing statistics
   - Kaggle datasets (prices, rates)

2. **Transform**: Data cleaning and processing
   - Standardize date formats
   - Handle missing values
   - Calculate growth rates
   - Validate numeric data

3. **Load**: Database operations
   - PostgreSQL database storage
   - Automated data loading
   - Data integrity checks

## Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- PostgreSQL database

## Setup

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/housing-project.git
cd housing-project
```

2. Install frontend dependencies:
```bash
cd housing-dashboard
npm install
```

3. Install backend dependencies:
```bash
cd api
pip install -r requirements.txt
```

4. Configure environment variables:

housing-dashboard/.env:
```
REACT_APP_API_URL=http://localhost:8002
```

scripts/scrapers/.env:
```
DB_NAME=housing_db
DB_USER=[username]
DB_PASSWORD=[password]
DB_HOST=localhost
DB_PORT=5432
```

5. Initialize the database:
```bash
python scripts/drop_create_db.py
```

6. Run the ETL pipeline:
```bash
# Extract and process data
python scripts/process_datasets.py

# Load data into database
python scripts/scrapers/load_to_db.py
```

7. Start the development servers:

Backend:
```bash
cd housing-dashboard/api
uvicorn main:app --reload --port 8002
```

Frontend:
```bash
cd housing-dashboard
npm start
```

The application will be available at http://localhost:3000

## Key Scripts

- `scripts/scrapers/*.py`: Data extraction from various sources
- `scripts/data_cleaning.py`: Core data cleaning utilities
- `scripts/process_datasets.py`: Data processing pipeline
- `scripts/drop_create_db.py`: Database initialization
- `scripts/backup_db.py`: Database backup creation
- `scripts/load_to_db.py`: Data loading into database

## Development Stack

- Frontend: React with TypeScript
- Data Visualization: Plotly.js
- Backend: Python with FastAPI
- Database: PostgreSQL
- ETL: Custom Python pipeline

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
