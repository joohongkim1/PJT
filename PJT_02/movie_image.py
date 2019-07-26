import requests
import csv

with open('movie_naver.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        movieCd = row['영화 대표코드']
        thumb_url = row['썸네일 URL']
        with open(f'images/{movieCd}.jpg', 'wb') as f: # 'wb' => write binary 
            response = requests.get(thumb_url)
            f.write(response.content)



