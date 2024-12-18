import requests
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 환경변수에서 WEATHER_API_KEY를 가져옵니다.
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
KHOA_API_KEY = os.getenv('KHOA_API_KEY')
WEATHER_API_BASE_URL = 'http://api.weatherapi.com/v1/current.json'

def get_sea_weather_by_seapostid(obs_station_id):
    current_date = datetime.now().strftime('%Y%m%d')

    # 병렬로 처리할 함수
    def fetch_api_data(DATA_TYPE):
        api_url = f"http://www.khoa.go.kr/api/oceangrid/{DATA_TYPE}/search.do"
        params = {
            'ServiceKey': KHOA_API_KEY,
            'ObsCode': obs_station_id,
            'Date': current_date,
            'ResultType': 'json'
        }
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # 에러 발생 시 예외 처리
            try:
                api_data = response.json()  # JSON 파싱
            except ValueError:
                return (DATA_TYPE, {'error': 'Invalid JSON response'})

            # 예상하는 구조 확인
            if 'result' not in api_data or 'data' not in api_data['result']:
                if 'error' in api_data['result']:
                    # API 결과에 에러 메시지가 포함된 경우
                    return (DATA_TYPE, {'error': api_data['result']['error']})
                else:
                    # 알 수 없는 결과 처리
                    return (DATA_TYPE, {'error': 'Unexpected API response structure'})

            # 정상적인 데이터 반환
            filtered_api_data = api_data['result']['data']
            return (DATA_TYPE, filtered_api_data)
        except requests.exceptions.RequestException as e:
            return (DATA_TYPE, {'error': str(e)})

    # ThreadPoolExecutor를 사용해 병렬 요청 실행
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(fetch_api_data, "tideObsRecent"),
            executor.submit(fetch_api_data, "tideObsPreTab")
        ]

        results = {}
        for future in as_completed(futures):
            DATA_TYPE, result = future.result()
            results[DATA_TYPE] = result

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