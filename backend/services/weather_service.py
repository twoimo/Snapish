import requests
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 환경변수에서 WEATHER_API_KEY를 가져옵니다.
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
KHOA_API_KEY = os.getenv('KHOA_API_KEY')
WEATHER_API_BASE_URL = 'http://api.weatherapi.com/v1/current.json'

def get_sea_weather_by_seapostid(obs_data):
    current_date = datetime.now().strftime('%Y%m%d')

    # 병렬로 처리할 함수
    def fetch_api_data(DATA_TYPE, obs_post_id):
        api_url = f"http://www.khoa.go.kr/api/oceangrid/{DATA_TYPE}/search.do"
        params = {
            'ServiceKey': KHOA_API_KEY,
            'ObsCode': obs_post_id,
            'Date': current_date,
            'ResultType': 'json'
        }
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            try:
                api_data = response.json()
            except ValueError:
                return (DATA_TYPE, {'error': 'Invalid JSON response'})

            if 'result' not in api_data or 'data' not in api_data['result']:
                if 'error' in api_data['result']:
                    return (DATA_TYPE, {'error': api_data['result']['error']})
                else:
                    return (DATA_TYPE, {'error': 'Unexpected API response structure'})

            filtered_api_data = api_data['result']['data']
            return (DATA_TYPE, filtered_api_data)
        except requests.exceptions.RequestException as e:
            return (DATA_TYPE, {'error': str(e)})

    # ThreadPoolExecutor를 사용해 병렬 요청 실행
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(fetch_api_data, "tideObsRecent", obs_data['obsrecent']),
            executor.submit(fetch_api_data, "tideObsPreTab", obs_data['obspretab'])
        ]

        results = {
            'obsrecent': {},
            'obspretab': {}
        }
        
        for future in as_completed(futures):
            DATA_TYPE, result = future.result()
            if DATA_TYPE == "tideObsRecent":
                results['obsrecent'] = result
            else:
                results['obspretab'] = result

    return results
    

def get_weather_by_coordinates(lat, lon):
    """
    Get Current Weather info by using latitude & longitude
    """
    try:
        # 날씨 API 호출
        weather_url = f"{WEATHER_API_BASE_URL}"
        params = {
            "key": WEATHER_API_KEY,
            "q": f"{lat},{lon}",
            "lang": "ko"
        }
        response = requests.get(weather_url, params=params)
        data = response.json()

        if 'error' in data:
            raise ValueError(data['error']['message'])
        
        # 날씨 데이터 가공
        weather_data = data
        return weather_data

    except Exception as e:
        raise Exception(f"Error fetching weather data: {str(e)}")