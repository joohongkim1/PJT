import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config # 환경변수 작업
import csv

movie_data = {}

for week in range(51):
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=week)
    targetDt = targetDt.strftime('%Y%m%d')

    key = config('API_KEY')  # 깃허브에 올릴 떄 .env 안 올라가도록 관리
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
    api_url = f'{base_url}?key={key}&targetDt={targetDt}&weekGb=0'

    response = requests.get(api_url)
    data = response.json()  # requests에서 지원하는 json메소드

    for movie in data['boxOfficeResult']['weeklyBoxOfficeList']:
        if movie.get('movieCd') not in movie_data:
            movie_data[movie.get('movieCd')] = {    
                'movieCd': movie.get('movieCd'),
                'movieNm': movie.get('movieNm'),
                'audiAcc': movie.get('audiAcc'),
            }   

with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 지정하는 작업
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)

        # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()
       
            # Dictionary를 순회하며 key 값에 맞는 value 를 한 줄씩 작성한다.
    for item in movie_data.values():
        writer.writerow(item)  
                    
    
