# JAVIC

[![capston_javic](https://res.cloudinary.com/marcomontalbano/image/upload/v1637514897/video_to_markdown/images/youtube--m3kJfnsywrk-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=m3kJfnsywrk "javic youtube")

## Description

##### JAVIC(Just A Very Intelligent Chatbot, 자빅)

<img src="/javic_server/javic_capture/summary.PNG" width="px" height="px"></img>

##### Naive Bayes model

<img src="/javic_server/javic_capture/NB.PNG" width="px" height="px"></img>

---

## Project Architecture

<img src="/javic_server/javic_capture/architecture.PNG" width="px" height="px"></img>

---

## Project Function

<img src="/javic_server/javic_capture/docwrite.PNG" width="px" height="px"></img>

<img src="/javic_server/javic_capture/mailcheck.PNG" width="px" height="px"></img>

<img src="/javic_server/javic_capture/textsummary.PNG" width="px" height="px"></img>

---

## Project Scrum

<img src="/javic_server/javic_capture/scrum.PNG" width="px" height="px"></img>
<img src="/javic_server/javic_capture/part.PNG" width="px" height="px"></img>

---

## run project

- Dependency install

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

- my_logic_adapter
- naive_bayes_model
- chatterbot

### Docker 배포 완료

- oauth 동작 확인
- handy 와 연동 여부 확인 필요 (VPN 사용이 불가능하여 현재 미뤄두었습니다)
- requirements.txt 와 pip3_requirements.txt 는 개발서버 배포용이므로, 기존에 Chatterbot이 잘 깔려있고 동작이 원활하다면 requirements.txt install 을 절대 권장하지 않습니다.
- 개별 PC에서 oauth 동작을 확인하고 싶으시면 run.sh의 환경변수 주석 여부를 확인하시고 실행해주세요(localhost로 되어있어야 개별 동작 확인 가능합니다)
