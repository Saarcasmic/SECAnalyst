
import os
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

load_dotenv()

def debug_url():
    url_str = os.getenv("DATABASE_URL")
    if not url_str:
        print("DATABASE_URL not found in environment.")
        return

    print(f"Original URL Start: {url_str[:15]}...")
    
    # Simulate the replacement logic in database.py
    if url_str.startswith("postgres://"):
        url_str = url_str.replace("postgres://", "postgresql://", 1)
        print("Applied postgres:// -> postgresql:// fix.")

    try:
        u = make_url(url_str)
        print("\n--- Parsed Components ---")
        print(f"Driver: {u.drivername}")
        print(f"Username: {u.username}")
        # Mask password
        if u.password:
            masked_pw = u.password[0] + "*" * (len(u.password)-2) + u.password[-1] if len(u.password) > 2 else "***"
            print(f"Password: {masked_pw}")
            
            # Check for special chars that might need encoding
            specials = ["@", ":", "/"]
            found_specials = [c for c in specials if c in u.password]
            if found_specials:
                print(f"WARNING: Password contains special characters that might need URL encoding: {found_specials}")
        else:
            print("Password: None")
            
        print(f"Host: {u.host}")
        print(f"Port: {u.port}")
        print(f"Database: {u.database}")
        
    except Exception as e:
        print(f"Error parsing URL: {e}")

if __name__ == "__main__":
    debug_url()
