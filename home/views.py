import csv
import os
import random
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from home.models import UserGeolocation


VALID_IPS_FILE = "valid_proxies.csv"
INVALID_IPS_FILE = "invalid_proxies.csv"
PROXY_API_KEY = "DQdmxp4NzhnGRHFSuT9tAsZaCJg3Vfej"
PROXY_ENDPOINT = "http://falcon.proxyrotator.com:51337/"


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def generate_user_agents(num_agents):
    user_agents = []
    for _ in range(num_agents):
        user_agent = (
            f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500, 599)}.0 '
            f'(KHTML, like Gecko) Chrome/{random.randint(70, 90)}.0.{random.randint(1000, 9999)}.0 Safari/{random.randint(500, 599)}.36'
        )
        user_agents.append(user_agent)
    return user_agents


def get_location(loc):
    words = loc.split(" ")
    last_word = words[-1]
    try:
        uule = UserGeolocation.objects.filter(name=last_word).values('uule').first()
        return uule['uule'] if uule else "w+CAIQICIdTG9uZG9uLEVuZ2xhbmQsVW5pdGVkIEtpbmdkb20"
    except UserGeolocation.DoesNotExist:
        return "w+CAIQICIdTG9uZG9uLEVuZ2xhbmQsVW5pdGVkIEtpbmdkb20"


def get_keyword_placement(keyword, target_url, domain, advanced=False, sleep_interval=1):
    base_url = f'https://www.google.{domain}/search'
    location = ''
    language = ''
    results = []

    uule = get_location(location)

    for page in range(0, 10, 10):
        pagination_params = {
            'q': keyword,
            'gl': location,
            'hl': language,
            'uule': uule,
            'start': str(page),
            'sa': 'N',
            'num': 100
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,'
                      'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': f'https://www.google.{domain}/',
            'user-agent': random.choice(generate_user_agents(50)),
        }
        params = pagination_params
        response = requests.get(base_url, params=params, headers=headers)
        content = BeautifulSoup(response.text, "html.parser")
        result_block = content.find_all("div", attrs={"class": "g"})
        for result in result_block:
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find(
                "div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.text
                if link and title and description:
                    if advanced:
                        yield SearchResult(link["href"], title.text, description)
                    else:
                        yield link["href"]


def fetch_google_results(query, page, domain):
    base_url = f'https://www.google.{domain}/search'
    pagination_params = {
        'q': query,
        'sxsrf': 'ACYBGNRmhZ3C1fo8pX_gW_d8i4gVeu41Bw:1575654668368',
        'ei': 'z1y1ZN7YPKO4hbIP5bOgmAE',
        'start': '',
        'sa': 'N',
        'ved': '0ahUKEwie_NL7hZaAAxUjXEEAHeUZCBMQ4dUDCAw',
    }

    initial_params = {
        'sxsrf': 'ACYBGNQ16aJKOqQVdyEW9OtCv8zRsBcRig:1575650951873',
        'ei': 'z1y1ZN7YPKO4hbIP5bOgmAE',
        'q': '',
        'oq': '',
        'gs_lp': 'Egxnd3Mtd2l6LXNlcnAiG2xvY2F0aW9ucyBpbiB1bml0ZWQgaW5nZG9tIEjzClD4AVjuCnAAeAGQAQCYAdwFoAHcBaoBAzYtMbgBA8gBAPgBAeIDBBgAIEGIBgE'
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'AEC=Ad49MVHN8Q-TL6_Ou15PP12ZjMBYrPSAd9L2wekonPviDVlihGl1rO4Gyg; OTZ=7121284_36_36__36_; '
                  'CONSENT=PENDING+418; SOCS=CAISHAgCEhJnd3NfMjAyMzA3MTAtMF9SQzIaAmVuIAEaBgiAidKlBg; '
                  'NID=511'
                  '=ITHrRlQIZRnhCNOO9fnccJ7B5Sr9rqQD2Sai9axiE9swh1m8qtO2KdrZX5x9EF4Kvk88x09AovKn6v1UFM5BDHckFLm8QdnW_sltHF7sLar1X43t61St3jx-_-LqpdyRnxZy42tCwIEtTx0CyPX-Tkfw091JanEzRkqf2B9XVbhTkXDQzdk4JdFFpSg4Qlg; 1P_JAR=2023-07-17-14',
        'pragma': 'no-cache',
        'referer': f'https://www.google.{domain}/',
        'upgrade-insecure-requests': '1',
        'user-agent': random.choice(generate_user_agents(50)),
        'gl': 'uk',
        'uule': 'w+CAIQICIOVW5pdGVkIEtpbmdkb20'
    }

    results = []

    def parse(html):
        content = BeautifulSoup(html, 'lxml')
        link = [link.next_element['href'] for link in content.findAll('div', {'class': 'yuRUbf'})]
        for index in range(0, len(link)):
            results.append({'link': link[index]})

    def fetch_page(query, page):
        if not page:
            params = initial_params
        else:
            params = pagination_params
            params['start'] = str(page * 10)

        params['q'] = query
        response = requests.get(base_url, params=params, headers=headers)
        print('HTTP GET request to URL: %s | Status code: %s' % (response.url, response.status_code))
        return response

    for page in range(0, 15):
        response = fetch_page(query, page)
        parse(response.text)
        time.sleep(2)

    return results


def write_csv(results, keyword):
    if len(results):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{keyword}_{timestamp}.csv"

        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"File '{file_name}' deleted successfully.")
        else:
            print(f"File '{file_name}' does not exist.")

        print(f"Writing results to '{file_name}' ... ', end=''")
        with open(file_name, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())

            if not os.path.exists(file_name):
                writer.writeheader()

            for row in results:
                writer.writerow(row)

        print('Done')


def find_target_url(results, target_url=None):
    for index, result in enumerate(results):
        if target_url in result['link']:
            return index + 1

    return 'Target URL is not found'


def home(request):
    if request.method == 'POST':
        data = request.POST
        keyword = data.get('keyword')
        target_url = data.get('target_url')
        domain = data.get('gDomain')

        # Scrape Google results for the keyword
        results = fetch_google_results(keyword, page=0, domain=domain)

        # Find target URL in the results
        target_placement = find_target_url(results, target_url=target_url)

        return render(request, "results.html", {'all_responses': target_placement})

    return render(request, "index.html")


def form_submit(request):
    if request.method == 'POST':
        data = request.POST
        keywords = data.get('q')
        lines = keywords.splitlines()
        target_url = data.get('target_url')
        location = data.get('gl')
        language = data.get('hl')
        device = data.get('deviceSelect')
        adTest = data.get('adTest')
        domain = data.get('gDomain')
        base_url = f'https://www.google.{domain}/search'
        all_responses = []

        uule_map = {line: get_location(line) for line in lines}

        for line in lines:
            keyword_data = {
                'keyword': line,
                'pagination_urls': [],
                'placement': None,
            }
            for page in range(0, 5):
                pagination_params = {
                    'q': line,
                    'gl': location,
                    'adtest': adTest,
                    'hl': language,
                    'uule': uule_map[line],
                    'start': str(page * 10),
                    'sa': 'N',
                    'num': 100
                }
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,'
                              'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'referer': f'https://www.google.{domain}/',
                    'user-agent': random.choice(generate_user_agents(50)),
                }
                params = pagination_params
                response = requests.get(base_url, params=params, headers=headers)
                if response is not None:
                    keyword_data['pagination_urls'].append(response.url)

            # Get the placement for the keyword with the target URL
            keyword_data['placement'] = get_keyword_placement(line, target_url, domain)

            all_responses.append(keyword_data)

        return render(request, "results.html", {'all_responses': all_responses})

    return render(request, "index.html")
