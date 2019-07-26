import requests
from pprint import pprint
from decouple import config
import csv
import time

BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
ID = config('CLIENT_ID')
SECRET = config('CLIENT_SECRET')
HEADERS = {
    'X-Naver-Client-id': ID,
    'X-Naver-Client-secret': SECRET,
}

movie_data = {}

with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        time.sleep(0.1)
        movieNm = row['영화명(국문)']
        movieCd = row['영화 대표코드']
        movieEnNm = row['영화명(영문)']
        API_URL = f'{BASE_URL}?query={movieNm}'
        response = requests.get(API_URL, headers=HEADERS).json()

        movie = response.get('items')[0]
        if movie.get('image') != '':
            for data in range(len(movie)):
                movie_data[movieCd] = {
                    '영화 대표코드': movieCd,
                    '하이퍼텍스트 link': movie.get('link'),
                    '썸네일 URL': movie.get('image'),
                    '유저 평점': movie.get('userRating'),
                    }
                    
with open('movie_naver.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ('영화 대표코드', '하이퍼텍스트 link', '썸네일 URL', '유저 평점')
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for item in movie_data.values():
        writer.writerow(item)

