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
pip install asyncmy
pip install pandas
pip install databases[aiomysql]
```


## 유용한 기능
+ Ctrl + , => 검색창에서 file:exclude 항목에 불필요한 파일들 필터링 가능 ( ex: **/__pycache__ 추가 시, 파이썬 캐싱 파일이 탐색기에서 삭제됨 )
