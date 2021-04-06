# piku_backend_api

- 해당 레포지토리는 [PIKU(이미지 월드컵)](https://www.piku.co.kr/) 웹사이트를 분석하여 Django로 백엔드 API를 클론하기 위해 제작되었습니다.

## Dev Apps

- accountapp
  - 유저 정보 관리
  - models = CustomUser, Profile
- tokenapp
  - 유저의 token 발급, 재발급을 관리
- worldcupapp
  - worldcup을 관리
  - models = Worldcup, Media, Comment
- reportapp
  - 신고 정보를 관리
  - models = UserReport, WorldcupReport, MediaReport, CommentReport

## 개발 환경

- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)

## pip 종속성

- 모든 라이브러리 종속성은 requirements 디렉토리 내의 아래의 파일들로 관리됩니다.
  - common.txt - 공통 라이브러리
  - dev.txt - 개발 환경 전용 라이브러리
  - prod.txt - 배포 환경 전용 라이브러리

## 예제 사이트

- [API 문서 (redoc)](http://www.piku.kro.kr/api/schema/redoc/)

## RESTful API 구조

- [예제 사이트](http://www.piku.kro.kr/api/schema/redoc/)에서 확인할 수 있습니다.

## 컨테이너 구조

- 개발 환경(docker-compose.dev.yml)
  - postgres : django에서 사용될 데이터베이스
  - django : django로 구현된 web application
- 배포 환경(docker-compose.prod.yml)
  - postgres : django에서 사용될 데이터베이스
  - django_with_gunicorn : gunicorn을 통해 실행되는 application server
  - nginx_with_certbot : let's encript를 통해 ssl 인증서 발급이 자동으로 수행되는 nginx

## 개발 환경에서의 실행

- 먼저 프로젝트의 backend/settings 디렉토리에 dev.env 파일을 작성합니다.
  
  ```yaml
  DJANGO_SECRET_KEY=your_secret_key
  DJANGO_ALLOWED_HOSTS=*
  DJANGO_DATABASE_URL="psql://postgres:password@database:5432/postgres"
  ```

- docker-compose를 통해 docker/docker-compose.dev.yml 파일을 실행합니다.

## 배포 환경에서의 실행

- docker 디렉토리 내의 Dockerfile.prod를 활용하여 docker image를 생성합니다.
- 생성된 이미지를 자신의 docker hub에 push합니다.
- docker-compose.prod.yml 파일의 service인 'django_with_gunicorn'의 image를 자신의 image로 변경합니다.
- [staticfloat/nginx-certbot](https://hub.docker.com/r/staticfloat/nginx-certbot/)의 사용방법을 숙지하고, docker-compose가 수행될 서버 또는 인스턴스에 적절한 nginx 설정 디렉토리를 구축합니다.
- docker-compose.prod.yml 파일의 service인 'nginx_with_certbot'의 volumes 중 nginx의 conf.d 볼륨을 적절히 설정합니다.
- docker를 swarm으로 변경합니다.
- docker secret에 prod.env 이름으로 아래의 내용을 저장합니다. DJANGO_DATABASE_URL 설정은 다음 단계를 참조하여 작성합니다.

  ```yaml
  DJANGO_SECRET_KEY=your_secret_key
  DJANGO_ALLOWED_HOSTS=your_frontent_hosts
  DJANGO_DATABASE_URL="psql://{db_username}:{db_password}@{db_service_name}:5432/{db_name}"
  ```

- docker-compose를 통해 docker/docker-compose.prod.yml 파일을 실행합니다.
  - 이 때, 환경변수 POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD 또한 함께 전달해야 합니다.
  - 이는 backend/settings/prod.env 내의 DJANGO_DATABASE_URL 설정과 일치해야 합니다.

## 더미 데이터 추가

- python manage.py setup_dummy_data
- 자세한 설정은 dummydata/factorys, dummydata/setup_dummy_data.py를 살펴본다.

## 나머지 작업들 (수행 여부 불확실)

- selery와 rabbitmq를 활용하여 accountapp의 email 전송 로직을 비동기로 수행한다.
- 캐싱용 redis 컨테이너를 추가하고, View 로직의 효율적인 처리를 위해 캐싱을 적용한다.
- database를 호스팅 서비스로 분리한다.
- static file을 storage 서비스로 분리한다.
- 캐싱용 서버를 대여하고 redis를 분리한다.
- log를 효율적으로 관리할 수 있도록 sentry를 활용한다.
- 부하 테스트를 진행한다.
- Front-end를 구현하고, ALLOWED_HOSTS 설정을 변경한다.
