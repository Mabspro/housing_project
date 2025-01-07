import os
from pathlib import Path
import shutil
import argparse

def toggle_db_config(env_type=None):
    """
    Toggle between local and Supabase database configurations.
    Args:
        env_type: Optional str, either 'local' or 'supabase'. If not provided, will toggle to the opposite of current.
    """
    # Define paths
    env_path = Path(__file__).parent / '.env'
    local_env_path = Path(__file__).parent / '.env.local'
    supabase_env_path = Path(__file__).parent / '.env.supabase'
    
    # Create .env.supabase if it doesn't exist
    if not supabase_env_path.exists():
        supabase_content = """DB_USER=postgres.uhfrcjhackormolekcxk
DB_PASSWORD=Idexx@15234
DB_HOST=aws-0-us-west-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
# Bureau of Labor Statistics (BLS) API key
# Get your key at: https://www.bls.gov/developers/
BLS_API_KEY=your_bls_api_key_here

# Census Bureau API key
# Get your key at: https://api.census.gov/data/key_signup.html
CENSUS_API_KEY=your_census_api_key_here"""
        with open(supabase_env_path, 'w') as f:
            f.write(supabase_content)
    
    # Determine current configuration
    with open(env_path, 'r') as f:
        current_config = f.read()
    
    is_currently_local = 'DB_HOST=localhost' in current_config
    
    # Determine which configuration to use
    if env_type is None:
        # Toggle to opposite of current
        use_local = not is_currently_local
    else:
        # Use specified configuration
        use_local = env_type.lower() == 'local'
    
    # Backup current .env
    backup_path = env_path.with_suffix('.env.backup')
    shutil.copy2(env_path, backup_path)
    
    # Copy appropriate config to .env
    source_path = local_env_path if use_local else supabase_env_path
    shutil.copy2(source_path, env_path)
    
    print(f"Switched to {'local' if use_local else 'Supabase'} database configuration")
    print(f"Previous configuration backed up to {backup_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Toggle between local and Supabase database configurations')
    parser.add_argument('--env', choices=['local', 'supabase'], 
                      help='Specify environment to switch to. If not provided, will toggle to opposite of current.')
    args = parser.parse_args()
    
    toggle_db_config(args.env if args.env else None)
