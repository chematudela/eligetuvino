import argparse

import utils.constants as c
from utils.requester import Requester


def get_arguments():
    """Gets arguments from the command line.

    Returns:
        A parser with the input arguments.

    """

    parser = argparse.ArgumentParser(usage='Scraps all wine URLs from Vivino.')

    parser.add_argument('output_file', help='Output .txt file', type=str)

    parser.add_argument('-start_page', help='Starting page identifier', type=int, default=1)

    return parser.parse_args()


if __name__ == '__main__':
    # Gathers the input arguments and its variables
    args = get_arguments()
    output_file = args.output_file
    start_page = args.start_page

    # Instantiates a wrapper over the `requests` package
    r = Requester(c.BASE_URL)

    # Defines the payload, i.e., filters to be used on the search
    payload = {
        #"country_codes[]": "de",
        #"country_codes[]": "ar",
        #"country_codes[]": "au",
        #"country_codes[]": "at",
        #"country_codes[]": "cl",
        #"country_codes[]": "es",
        #"country_codes[]": "us",
        #"country_codes[]": "it",
        "country_codes[]": "pt",
        #"currency_code": "EUR",
        # "food_ids[]": 20,
        # "grape_ids[]": 3,
        # "grape_filter": "varietal",
        "min_rating":1,
        "order_by": "price",
        "order": "desc",
        "price_range_min": 499,
        "price_range_max": 500,
        "vc_only" : "",
        "wsa_year": "null",
        "discount_prices":"false",
        # "region_ids[]": 383,
        # "wine_style_ids[]": 98,
        "wine_type_ids[]": 1,
        #wine_type_ids[]" : 2,
        # "wine_type_ids[]": 3,
        # "wine_type_ids[]": 4,
        # "wine_type_ids[]": 7,
        # "wine_type_ids[]": 24,
    }
#https://www.vivino.com/explore?currency_code=EUR&min_rating=1&order_by=price&order=desc&page=2&price_range_max=500&price_range_min=500&vc_only=&wsa_year=null&discount_prices=false&country_codes[]=de&country_codes[]=ar&country_codes[]=au&country_codes[]=at&country_codes[]=cl&country_codes[]=es&country_codes[]=us&country_codes[]=it&country_codes[]=pt&wine_type_ids[]=1
    # Performs an initial request to get the number of records (wines)
    res = r.get('explore/explore?', params=payload)
    n_matches = res.json()['explore_vintage']['records_matched']

    print(f'Number of matches: {n_matches}')

    # Iterates through the amount of possible pages
    for i in range(start_page, max(1, int(n_matches / c.RECORDS_PER_PAGE)) + 1):
        # Adds the page to the payload
        payload['page'] = i

        print(f'Scraping data from page: {payload["page"]}')

        # Performs the request and scraps the URLs
        res = r.get('explore/explore', params=payload)
        matches = res.json()['explore_vintage']['matches']

        # Opens the output file with append
        with open(output_file, 'a') as f:
            # Iterates over every match
            for match in matches:
                # Dumps the URL to file
                f.write(f'{c.BASE_URL}w/{match["vintage"]["wine"]["id"]}\n')
