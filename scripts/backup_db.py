import os
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

def create_backup():
    # Load environment variables from the scrapers/.env file
    env_path = Path('scripts/scrapers/.env')
    load_dotenv(env_path)

    # Get database connection parameters
    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    # Create backups directory if it doesn't exist
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f"housing_db_backup_{timestamp}.sql"

    try:
        # Set PGPASSWORD environment variable for pg_dump
        os.environ['PGPASSWORD'] = db_params['password']

        # Construct pg_dump command
        command = [
            'pg_dump',
            '-h', db_params['host'],
            '-p', db_params['port'],
            '-U', db_params['user'],
            '-d', db_params['dbname'],
            '-F', 'p',  # plain text format
            '-f', str(backup_file)
        ]

        # Execute pg_dump
        print(f"Creating backup: {backup_file}")
        subprocess.run(command, check=True)
        print("Backup completed successfully!")

        # Get file size
        size_bytes = os.path.getsize(backup_file)
        size_mb = size_bytes / (1024 * 1024)
        print(f"Backup size: {size_mb:.2f} MB")

    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        # Clean up environment variable
        if 'PGPASSWORD' in os.environ:
            del os.environ['PGPASSWORD']

if __name__ == "__main__":
    create_backup()
