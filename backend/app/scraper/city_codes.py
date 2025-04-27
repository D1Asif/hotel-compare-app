# Mapping of city names to Agoda city codes
# This is a sample mapping - you'll need to add more cities as needed
CITY_CODES = {
    "dhaka": "1390",
    "chittagong": "512855",
    "khulna": "513017",
    "rajshahi": "671813",
    "sylhet": "513022",
    "barisal": "700812",
    "cox's bazar": "671817",
}

def get_agoda_city_code(city_name: str) -> str:
    """
    Get the Agoda city code for a given city name.
    
    Args:
        city_name: Name of the city
        
    Returns:
        Agoda city code as string
        
    Raises:
        ValueError: If city is not found in the mapping
    """
    city_name = city_name.lower().strip()
    if city_name not in CITY_CODES:
        raise ValueError(f"City code not found for: {city_name}")
    return CITY_CODES[city_name] 