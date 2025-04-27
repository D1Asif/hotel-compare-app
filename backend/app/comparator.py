from collections import defaultdict

def group_hotels_by_name(hotels):
    hotel_map = defaultdict(list)
    
    for hotel in hotels:
        name = hotel['hotel_name'].strip().lower()  # normalize name
        hotel_map[name].append(hotel)
    
    return hotel_map

def fix_image_url(url):
    if url.startswith("//"):
        return "https:" + url
    return url

def organize_hotel_comparison(hotel_map):
    comparison_list = []

    for hotel_name, sources in hotel_map.items():
        hotel_entry = {
            "hotel_name": hotel_name.title()
        }
        for entry in sources:
            source = entry['source']
            hotel_entry[source] = {
                "price": entry['price'],
                "image": fix_image_url(entry['image']),
                "link": entry['booking_url']
            }
        comparison_list.append(hotel_entry)

    return comparison_list