import requests
from bs4 import BeautifulSoup

def scrape_hotels(url):
    # TODO : url rabi date da vrze price nazaj
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        return {'error': f"Oops. {e}"}


    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the hotel elements in the HTML document
    hotels = soup.findAll('div', {'data-testid': 'property-card'})
    if not hotels:
        return {'error': 'No accomodations found :('}

    hotels_data = []
    # Loop over the hotel elements and extract the desired data
    for hotel in hotels:
        try:
            image = hotel.find('img', {'data-testid': 'image'})
        except AttributeError:
            image = 'No image'

        name = hotel.find('div', {'data-testid': 'title'})
        price = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
        
        try:
            review = hotel.find('div', {'data-testid': 'review-score'})
            review = review.text.split()[1:-1]
            review_str = f"{review[0]}/10 ({review[-1]} reviews)"
        except:
            review_str = 'No reviews yet'
        
        
        link = hotel.find('a', {'data-testid': 'title-link'})
        distance_from = hotel.find('span', {'data-testid': 'distance'})
        location = hotel.find('span', {'data-testid': 'address'})

        hotels_data.append(
            {
                'image': image.get('src'),
                'name': name.text,
                'price': price.text,
                # actual array to make it simpler on frontend -> "ocena", "ocena z besedo", "število reviewev"
                # TODO - right now there can be 3 indexes - instead of second being worded it can say Review score
                # TODO - right now it can also be "Very" "good"
                'review': review_str,
                'link': link.get('href'),
                'distance': ' '.join(distance_from.text.split()[0:2]),
                'location': location.text
            }
        )

    return hotels_data