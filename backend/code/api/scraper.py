import requests
from bs4 import BeautifulSoup

def scrape_hotels(url):
    # TODO : url rabi date da vrze price nazaj
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the hotel elements in the HTML document
    hotels = soup.findAll('div', {'data-testid': 'property-card'})

    hotels_data = []
    # Loop over the hotel elements and extract the desired data
    for hotel in hotels:
        name = hotel.find('div', {'data-testid': 'title'})
        price = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
        review = hotel.find('div', {'data-testid': 'review-score'})
        link = hotel.find('a', {'data-testid': 'title-link'})
        distance_from = hotel.find('span', {'data-testid': 'distance'})
        location = hotel.find('span', {'data-testid': 'address'})

        # we need name - done, price - ok, rating - ok, link - ok, distance from festival location - done and location ???
        # we dont need (days, number of people) as it will be passed as params from frontend       
        
        hotels_data.append(
            {
                'name': name.text,
                'price': price.text,
                # actual array to make it simpler on frontend -> "ocena", "ocena z besedo", "število reviewev"
                # TODO - right now there can be 3 indexes - instead of second being worded it can say Review score
                # TODO - right now it can also be "Very" "good"
                'review': [review.text.split()[1:-1][0], review.text.split()[1:-1][-1]],
                'link': link.get('href'),
                'distance': distance_from.text,
                'location': location.text
            }
        )

    return hotels_data