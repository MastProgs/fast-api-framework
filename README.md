# fast-api-framework
xlsx code generator, async db, logger 등등 회사에서 쓸려고 만든 프레임워크 틀


## 개발 언어
+ Python -V 3.11.0
+ SQLAlchemy 1.4 


## 필요한 모듈
``` python
pip install fastapi
pip install "uvicorn[standard]"
pip install PyMySQL
pip install sqlalchemy
pip install sqlalchemy[asyncio]
pip install asyncmy
pip install pandas
pip install openpyxl
pip install mysqlclient
pip install databases[mysql]
pip install databases[aiomysql]
pip install pymongo
pip install redis
pip install redis_om
pip install "python-jose[cryptography]" "passlib[bcrypt]" python-multipart
```

## 설치도구
+ 몽고DB ( https://www.mongodb.com/download-center/enterprise/releases )

## 유용한 기능
+ Ctrl + , => 검색창에서 file:exclude 항목에 불필요한 파일들 필터링 가능 ( ex: **/__pycache__ 추가 시, 파이썬 캐싱 파일이 탐색기에서 삭제됨 )

## Socket 서버
+ fast-api 를 활용한 다중 접속 socket 서버
+ 정상통신 되는 부분 확인 & process packet 에 정의된 함수를, 사전 start up 시점에 각 프로토콜에 맞는 함수들을 등록해주고 활용해줌
