from typing import List, Dict, Any
from collections import defaultdict

def group_hotels_by_name(hotels: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group hotels by their names to compare prices across different sources.
    
    Args:
        hotels: List of hotel dictionaries containing hotel information
        
    Returns:
        Dictionary with hotel names as keys and lists of hotel data as values
    """
    grouped_hotels = defaultdict(list)
    
    for hotel in hotels:
        name = hotel.get('hotel_name', '').strip().lower()
        if name:  # Only add hotels with valid names
            grouped_hotels[name].append(hotel)
    
    return dict(grouped_hotels)

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
        
        # Create comparison entry
        comparison_entry = {
            'hotel_name': hotel_name,
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