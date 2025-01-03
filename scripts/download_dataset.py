import kagglehub
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Download dataset
print("Downloading dataset...")
path = kagglehub.dataset_download("praveenchandran2006/u-s-housing-prices-regional-trends-2000-2023")

# Move dataset to data directory
print(f"Moving dataset to data/ directory...")
os.rename(path, os.path.join('data', os.path.basename(path)))

print(f"Dataset successfully downloaded to: data/{os.path.basename(path)}")
