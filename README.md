# JAVIC

<img alt="PyPI - License" src="https://img.shields.io/pypi/l/chatterbot">

### Description

##### JAVIC(Just A Very Intelligent Chatbot, 자빅)

<img src="/javic_server/javic_capture/summary.PNG" width="px" height="px"></img>

사내 그룹웨어와 연동하여 간단한 사내 문서 작성과 이메일의 확인 및 요약이 가능한 챗봇 웹앱입니다.

##### 나이브 베이즈 분류 모델

<img src="/javic_server/javic_capture/NB.PNG" width="px" height="px"></img>

---

### Project Architecture

<img src="/javic_server/javic_capture/architecture.PNG" width="px" height="px"></img>

### Tech Stack

- Chatbot :
  - Chatterbot (Chatbot Engine)
  - KoNLPy (한국어 자연어 처리 Open Source)
  - Scikit-Learn (TextRank 기반 문장 요약 기능 구현을 위한 ML Library)
- Business Logic :
  - OAuth (구글 계정 연동)
  - Handy Groupware Open API (휴가신청서 작성)
  - Redis( 각 별 계정 정보 저장을 위한 메모리기반 Container NoSQL Cache Server)
- REST API Server & Client :
  - Flask (Web App Framework)
  - Ajax
  - BootStrap
  - JQuery
- Release :
  - Docker
  - docker-compose(Docker Container Orchestration)

---

### Project Schedule

<img src="/javic_server/javic_capture/scrum.PNG" width="px" height="px"></img>
<img src="/javic_server/javic_capture/part.PNG" width="px" height="px"></img>

---

### Main Function

[![capston_javic](https://res.cloudinary.com/marcomontalbano/image/upload/v1637514897/video_to_markdown/images/youtube--m3kJfnsywrk-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=m3kJfnsywrk "javic youtube")

<img src="/javic_server/javic_capture/docwrite.PNG" width="px" height="px"></img>

<img src="/javic_server/javic_capture/mailcheck.PNG" width="px" height="px"></img>

<img src="/javic_server/javic_capture/textsummary.PNG" width="px" height="px"></img>

---

### Run Project

Dependency install

```{shell}
pip3 install -r requirements.txt
```

PulseSecure 실행
핸디소프트(123.212.190.200)연결

handy_gw 디렉토리

```{shell}
 redis-server
```

handy_api 서버 실행

```{shell}
 python3 app.py
```

javic_server 디렉토리

```{shell}
 python3 app.py
```

Login

- ID : 현승재
- PW : 1234

---

### 변경점

- 회사에서 발급된 vpn ID의 기간 만료로 인해 서비스 실행불가

### Docker 배포 완료

- requirements.txt 와 pip3_requirements.txt 는 개발서버 배포용이므로, 기존에 Chatterbot이 잘 깔려있고 동작이 원활하다면 requirements.txt install 을 절대 권장하지 않습니다.
- 개별 PC에서 oauth 동작을 확인하고 싶으시면 run.sh의 환경변수 주석 여부를 확인하시고 실행해주세요(localhost로 되어있어야 개별 동작 확인 가능합니다)
