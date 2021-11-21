### javic 나이브베이즈 분류기

<p aligin=center>
<iframe width="560" height="315" src="https://www.youtube.com/embed/m3kJfnsywrk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</p>
```
pip3 install -r requirements.txt
```

#### run project

*PulseSecure실행
*핸디소프트(123.212.190.200)연결

\*handy_gw 디렉토리

```
$> redis-server
```

\*handy_api 서버 실행

```
$> python3 app.py
```

\*javic final 디렉토리

```
$> python3 app.py
```

\*로그인 페이지

- ID : 현승재
- PW : 1234

### 변경점

- my_logic_adapter
- naive_bayes_model

### Docker 배포 완료

- oauth 동작 확인
- handy 와 연동 여부 확인 필요 (VPN 사용이 불가능하여 현재 미뤄두었습니다)
- requirements.txt 와 pip3_requirements.txt 는 개발서버 배포용이므로, 기존에 Chatterbot이 잘 깔려있고 동작이 원활하다면 requirements.txt install 을 절대 권장하지 않습니다.
- 개별 PC에서 oauth 동작을 확인하고 싶으시면 run.sh의 환경변수 주석 여부를 확인하시고 실행해주세요(localhost로 되어있어야 개별 동작 확인 가능합니다)
