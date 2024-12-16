import pandas as pd
import json
from urllib.request import urlopen


'''Get list of indicators from SDP API'''

urls: dict[str, str] = {
    'indicators': 'https://api-sdp.stat.gov.pl/api/1.0.0/indicators/indicator-indicator?lang=pl',
    'way-of-presentation': 'https://api-sdp.stat.gov.pl/api/1.0.0/dictionaries/way-of-presentation?page=1&page-size=5000&lang=pl',
    'periods': 'https://api-sdp.stat.gov.pl/api/1.0.0/dictionaries/periods-dictionary?page=1&page-size=5000&lang=pl'
}

def get_indicators(api_url):
    with urlopen(api_url) as response:
        data = json.load(response)

    return data

def get_indicator_by_id(query_result):
    list_of_indicators = json.dumps(query_result, indent=4, ensure_ascii=False)

    indicators_dict = json.loads(list_of_indicators)
    indicators_df = pd.DataFrame(indicators_dict) # Convert list_of_indicators JSON string to DataFrame

    print(indicators_df)  # Display the first few rows of the DataFrame

for url in urls.values():
    try:
        data = get_indicators(url)
        if isinstance(data, dict):
            get_indicator_by_id(data['data'])
        elif isinstance(data, list):
            get_indicator_by_id(data)
    except Exception as e:
        print(f"Error: {e}")
