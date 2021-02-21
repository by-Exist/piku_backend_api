# 설명서

- 본 레포지토리는 [PIKU(이미지 월드컵)](https://www.piku.co.kr/)을 클론할 목적으로 사용할 백엔드 API를 설계하기 위해 작성되었습니다.
- 개발 환경을 구축하고, Restful API를 구현하여 실제 배포를 수행합니다.

## Plan

- Django의 개인적인 초기 설정을 기록한다.
  - [django-environ(로컬용)](https://django-environ.readthedocs.io/en/latest/)
  - [django-environ(도커용)](https://pypi.org/project/django-environ-docker/)
- 도메인 파악 후 ERD 툴을 활용하여 테이블을 설계한다.
  - [.vuerd](https://marketplace.visualstudio.com/items?itemName=dineug.vuerd-vscode)
- git의 브랜치 구조를 설명하고 그에 대한 근거를 제시한다.
  - [하루에 1000번 배포하는 조직 되기](https://blog.banksalad.com/tech/become-an-organization-that-deploys-1000-times-a-day/)
- rest 형식에 맞추어 api를 설계한다.
  - [ms api-design](https://docs.microsoft.com/ko-kr/azure/architecture/best-practices/api-design)
  - [RESTful URL 설계](https://blog.appkr.dev/files/again2011_workshop_keynote_2.pdf)
  - [REST API 설계 해보기](https://digitalbourgeois.tistory.com/54)
- Docker를 활용하여 로컬 개발환경을 구축한다.
  - [도커 컴포즈를 활용하여 완벽한 개발 환경 구성하기](https://www.44bits.io/ko/post/almost-perfect-development-environment-with-docker-and-docker-compose#build)
- CI(지속적 통합) - github action을 활용하여 push/pull_request시 수행
  - [black](https://github.com/marketplace?type=actions&query=black)
  - [test, build image...](https://medium.com/intelligentmachines/github-actions-end-to-end-ci-cd-pipeline-for-django-5d48d6f00abf)
- 호스팅에 활용할 서버 자원을 대여한다.
  - 웹 서버, 웹 어플리케이션 서버, DB, Storage, ...
- CD(지속적 배포) - github action을 활용하여 원할 때 서비스 배포를 수행하도록 구현한다.
  - Docker Compose 활용
- Django Debug Toolbar를 활용하여 DB 히트를 확인하고 쿼리를 최적화한다.
  - [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
  - [select_related, prepetch_related](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#select-related)
- API에 버저닝을 도입한다.
  - ...
- swagger를 활용하여 api를 문서화한다.
  - [친절하게 django rest framework api 문서 자동화하기](https://medium.com/towncompany-engineering/%EC%B9%9C%EC%A0%88%ED%95%98%EA%B2%8C-django-rest-framework-api-%EB%AC%B8%EC%84%9C-%EC%9E%90%EB%8F%99%ED%99%94%ED%95%98%EA%B8%B0-drf-yasg-c835269714fc)
- 조회수 기능에 캐싱을 활용하여 주기적/효율적인 insert 작업을 구현한다.
  - [캐싱하기](https://jupiny.com/2018/02/27/caching-using-redis-on-django/)
- celery와 MQ를 활용하여 비동기적인 작업을 구현한다.
  - ...

## 상세정보

### 1. Django의 개인적인 초기 환경을 설정한다

- secrets
  - [django-environ-docker](https://pypi.org/project/django-environ-docker/)
    - 도커의 secret을 통해 전달된 여러 환경변수를 사용할 수 있도록 돕는 라이브러리

### 2. 도메인 파악 후 ERD 툴을 활용하여 테이블을 설계한다

- 사이트를 제작함에 있어 필요한 테이블 구조를 설계한다.
- Tool
  - [ERD Editor](https://marketplace.visualstudio.com/items?itemName=dineug.vuerd-vscode)
- Image
  - ![ERD](./_erd/erd.jpg)

### 3. git의 브랜치 구조를 설명하고 그에 대한 근거를 제시한다

- [하루에 1000번 배포하는 조직 되기](https://blog.banksalad.com/tech/become-an-organization-that-deploys-1000-times-a-day/)
  - 기존에 활용되는 5가지로 분류되는 브랜치(Git-Flow 방식)를 기반으로 하여 하나의 기능을 추가/배포하는 과정에 있어 5번의 merge/branch switching과 6번의 pull request/code review가 필요했다.
  - 이를 복잡히 여겨 master branch를 제외한 모든 branch를 삭제
    - 추가할 기능은 모두 master branch를 base로 한 브랜치이며 squash merge 방식을 활용한다.
    - 추후 기능 장애 발생 시 revert pull request 기능을 활용하여 쉽게 롤백할 수 있다고 한다.
  - 배포 타이밍은 main에 merge 시가 아닌 action을 수행할 때이다.

### 4. restful http api를 설계한다

- url 정의

  - account

    | account url             | http method | mixin method   |
    | ----------------------- | ----------- | -------------- |
    | \<domain>/account       | get         | list           |
    | \<domain>/account       | post        | create         |
    | \<domain>/account/\<id> | get         | retrieve       |
    | \<domain>/account/\<id> | put         | update         |
    | \<domain>/account/\<id> | patch       | partial update |
    | \<domain>/account/\<id> | delete      | destroy        |

  - profile

    | profile url             | http method | mixin method   |
    | ----------------------- | ----------- | -------------- |
    | \<domain>/profile       | get         | list           |
    | \<domain>/profile       | post        | create         |
    | \<domain>/profile/\<id> | get         | retrieve       |
    | \<domain>/profile/\<id> | put         | update         |
    | \<domain>/profile/\<id> | patch       | partial update |
    | \<domain>/profile/\<id> | delete      | destroy        |

  - jwt token

    | token url               | http method | mixin method |
    | ----------------------- | ----------- | ------------ |
    | \<domain>/token/        | post        | obtain       |
    | \<domain>/token/refresh | post        | refresh      |

  - worldcup

    | worldcup url             | http method | mixin method   |
    | ------------------------ | ----------- | -------------- |
    | \<domain>/worldcup       | get         | list           |
    | \<domain>/worldcup       | post        | create         |
    | \<domain>/worldcup/\<id> | get         | retrieve       |
    | \<domain>/worldcup/\<id> | put         | update         |
    | \<domain>/worldcup/\<id> | patch       | partial update |
    | \<domain>/worldcup/\<id> | delete      | destroy        |

  - worldcup -> media

    | media url                                     | http method | mixin method   |
    | --------------------------------------------- | ----------- | -------------- |
    | \<domain>/worldcup/\<worldcup_id>/media       | get         | list           |
    | \<domain>/worldcup/\<worldcup_id>/media       | post        | create         |
    | \<domain>/worldcup/\<worldcup_id>/media/\<id> | get         | retrieve       |
    | \<domain>/worldcup/\<worldcup_id>/media/\<id> | put         | update         |
    | \<domain>/worldcup/\<worldcup_id>/media/\<id> | patch       | partial update |
    | \<domain>/worldcup/\<worldcup_id>/media/\<id> | delete      | destroy        |

  - worldcup -> comment

    | comment url                                     | http method | mixin method   |
    | ----------------------------------------------- | ----------- | -------------- |
    | \<domain>/worldcup/\<worldcup_id>/comment       | get         | list           |
    | \<domain>/worldcup/\<worldcup_id>/comment       | post        | create         |
    | \<domain>/worldcup/\<worldcup_id>/comment/\<id> | get         | retrieve       |
    | \<domain>/worldcup/\<worldcup_id>/comment/\<id> | put         | update         |
    | \<domain>/worldcup/\<worldcup_id>/comment/\<id> | patch       | partial update |
    | \<domain>/worldcup/\<worldcup_id>/comment/\<id> | delete      | destroy        |

  - report

    - target = user | media | comment

    | report url             | http method | mixin method   |
    | ---------------------- | ----------- | -------------- |
    | \<domain>/report       | get         | list           |
    | \<domain>/report       | post        | create         |
    | \<domain>/report/\<id> | get         | retrieve       |
    | \<domain>/report/\<id> | put         | update         |
    | \<domain>/report/\<id> | patch       | partial update |
    | \<domain>/report/\<id> | delete      | destroy        |

### 5. Docker를 활용하여 로컬 개발환경을 구축한다

- Dockerfile과 docker-compose를 활용하여 개발환경과 배포환경을 일치시킨다.
  - [Dockerfile.dev](./docker/Dockerfile.dev)
  - [docker-compose.dev.yml](./docker/docker-compose.dev.yml)

### 6. Github action을 활용하여 CI 환경을 구축한다

- [코드 스타일 체크](./.github/workflows/formatting.yml)
- [테스트 코드 수행](./.github/workflows/testing.yml)
- 배포에 활용될 이미지 생성

### 7. API 구현 및 문서화

- [친절하게 django rest framework api 문서 자동화하기](https://medium.com/towncompany-engineering/%EC%B9%9C%EC%A0%88%ED%95%98%EA%B2%8C-django-rest-framework-api-%EB%AC%B8%EC%84%9C-%EC%9E%90%EB%8F%99%ED%99%94%ED%95%98%EA%B8%B0-drf-yasg-c835269714fc)