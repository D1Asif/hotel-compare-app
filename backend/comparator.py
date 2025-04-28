from typing import List, Dict, Any
from collections import defaultdict
from fuzzywuzzy import fuzz
import re

def normalize_hotel_name(name: str) -> str:
    """
    Normalize hotel name by removing common words and formatting.
    """
    name = name.lower()
    name = re.sub(r'[^a-z\s]', '', name)  # Remove non-letter characters
    words = name.split()
    stopwords = {'hotel', 'dhaka', 'resort', 'inn', 'the'}
    filtered_words = [word for word in words if word not in stopwords]
    normalized_name = ' '.join(filtered_words)
    return normalized_name.strip()

def group_hotels_by_name(hotels: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group hotels by their fuzzy-matched names.
    """
    grouped_hotels = []
    
    for hotel in hotels:
        raw_name = hotel.get('hotel_name', '')
        normalized_name = normalize_hotel_name(raw_name)
        
        if not normalized_name:
            continue

        matched_group = None
        
        for group in grouped_hotels:
            representative_name = group['name']
            similarity = fuzz.ratio(normalized_name, representative_name)
            if similarity >= 75:  # threshold for considering names as similar
                matched_group = group
                break
        
        if matched_group:
            matched_group['hotels'].append(hotel)
        else:
            grouped_hotels.append({'name': normalized_name, 'hotels': [hotel]})
    
    # Convert to the final dictionary format
    result = {}
    for group in grouped_hotels:
        result[group['name']] = group['hotels']
    
    return result

def organize_hotel_comparison(grouped_hotels: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Organize hotel data for comparison, finding the best deals across sources.
    
    Args:
        grouped_hotels: Dictionary of hotels grouped by name
        
    Returns:
        List of organized hotel data with best deals highlighted
    """
    comparison_list = []
    
    for hotel_name, hotels in grouped_hotels.items():
        if not hotels:
            continue
            
        # Find the best price among all sources
        best_price = min(hotel['price'] for hotel in hotels)
        
        # Use the most complete name as the display name
        display_name = max(hotels, key=lambda x: len(x['hotel_name']))['hotel_name']
        
        # Create comparison entry
        comparison_entry = {
            'hotel_name': display_name,
            'best_price': best_price,
            'sources': []
        }
        
        # Add data from each source
        for hotel in hotels:
            source_data = {
                'source': hotel.get('source', 'unknown'),
                'price': hotel.get('price', 0),
                'rating': hotel.get('rating', 0),
                'image': hotel.get('image', ''),
                'booking_url': hotel.get('booking_url', ''),
                'is_best_deal': hotel.get('price', 0) == best_price
            }
            comparison_entry['sources'].append(source_data)
        
        comparison_list.append(comparison_entry)
    
    # Sort by best price
    comparison_list.sort(key=lambda x: x['best_price'])
    
    return comparison_list 