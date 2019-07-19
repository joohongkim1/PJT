import requests
import csv
from pprint import pprint
from decouple import config
# csv 파일을 읽어들이면서 대표코드에 새로운 요청을 보낸다.

key = config('API_KEY')
base_url = ' http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

movie_data = {}
with open('boxoffice.csv', 'r', newline='', encoding='utf-8') as f: 
    reader = csv.DictReader(f) 
    for row in reader:
        movieCd = row['movieCd']
        api_url =  f'{base_url}?key={key}&movieCd={movieCd}'
        response = requests.get(api_url)
        data = response.json()
        for movie in data['movieInfoResult']['movieInfo']:
            print(movie)
            # movie_data = {    
            #     'movieCd': movie.get('movieCd'),
            #     'movieNm': movie.get('movieNm'),
            #     'movieNmOg': movie.get('movieNmOg'),
            #     'openDt': movie.get('openDt'),
            #     'showTm': movie.get('showTm'),
            # }   





# with open('movie.csv', 'w', newline='', encoding='utf-8') as f:
#     fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm' )
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     writer.writeheader()

#     for item in movie_data.values():
#         writer.writerow(item)



# data = data['movieInfoResult']['movieInfo']

# movieCd = data['movieCd']
# movieNm = data['movieNm']
# movieNmEn = data['movieNmEn']
# movieOg = data['movieNmOg']
# openDt = data['openDt']
# showTm = data['showTm']


# watchGradeNm = data['audits']['watchGradeNm']
# genreNm = data['genres']['genreNm']
# peopleNm = data['director']['peopleNm']
