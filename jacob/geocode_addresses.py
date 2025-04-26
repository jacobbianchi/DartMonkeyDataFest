import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# --- Load CSV ---
df = pd.read_csv('aditya/employee_growth/employees.csv')

# --- Setup geolocator ---
geolocator = Nominatim(user_agent="industry_mapper", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

# --- Geocode with Dallas context ---
def get_lat_lon(address):
    try:
        location = geocode(f"{address}, Dallas, TX")
        if location:
            return pd.Series([location.latitude, location.longitude])
        else:
            return pd.Series([None, None])
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return pd.Series([None, None])

# --- Apply ---
df[['latitude', 'longitude']] = df['address'].apply(get_lat_lon)

# --- Drop bad ---
df = df.dropna(subset=['latitude', 'longitude'])

# --- Save ---
df.to_csv('jacob/geocoded_addresses.csv', index=False)

print("✅ Geocoding complete. Saved as 'geocoded_addresses.csv'.")