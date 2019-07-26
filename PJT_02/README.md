# PJT_02



###  1. 네이버 영화 검색 API 

- 요청 
  - 영화명을 통해 요청

- 응답
  - 영화별로 다음과 같은 내용 저장 - 영진위 영화 대표코드, 하이퍼텍스트 link, 영화 썸네일 이미지 URL, 유저 평점
  - 영화 썸네일 이미지의 URL 이 없는 경우 저장하지 않는다.
  - 해당 결과를 movie_naver.csv 에 저장



1-1 ) 

- 네이버 오픈 API 를 통해 기본 url 정보와 CLIENT_ID, CLIENT_SECRET 값을 받아온다. 

- ID 와 SECRET 값은 환경 변수에 저장

```
import requests 
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
```



1-2 )

- movie.csv 에서 값을 읽어와서 movie_data 에 저장

- 읽어온 값들을 대표할 수 있는 movieCd 변수를 키 값으로 지정하여 movie_data 딕셔너리 생성

- 중복된 값을 없애기 위해 같은 제목을 갖는 영화들의 첫 번째 인덱스에 있는 값을 가져온다. 

  (첫 번째 인덱스에 있는 데이터가 가장 최근의 데이터) 

```
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
```



1-3 ) 

- 위에서 읽어온 데이터를 이용하여 csv 파일을 작성한다.

```
with open('movie_naver.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ('영화 대표코드', '하이퍼텍스트 link', '썸네일 URL', '유저 평점')
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for item in movie_data.values():
        writer.writerow(item)


```





### 2. 영화 포스터 이미지 저장

- 요청
  - 영화 썸네일 이미지 URL

- 응답
  - 응답 받은 결과를 파일로 저장, wb 옵션 적용
  - images 폴더 내에 [영진위 영화 대표코드].jpg 로 저장



2-1 ) 

- 앞서 작성한 movie_naver.csv 에서 '영화 대표코드' 를 읽어와 파일명에 변수로 사용
- 앞서 작성한 movie_naver.csv 에서 '썸네일 URL' 를 읽어와 image 파일 생성에 이용

```
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

```

