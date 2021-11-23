### Commit 이력
	-20/2/24: 로그인/로그아웃 API 
    -20/3/2: 휴가신청		
### Build
```
$ 
```
### Execute
```
$ python app.py
```
### Client API 문서
- 로그인 API
   - /login
    - 요청url:
        - http://127.0.0.1:8000/login?name=사용자이름&passwd=비밀번호
    - 성공
        - {"사용자 고유키 값",200}
	- 실패
		- {"오류코드값" , 404}
			-오류코드:101 (암호가 일치하지 않음),102 (등록된사용자가 아님),103 (동명의 사용자 존재),500 (내부 시스템 오류)
- 로그아웃 API
    - /logout
    - 요청url:
        - http://127.0.0.1:8000/logout?key=고유키값        
    - 성공 
        - {"OK",200} 
- 휴가신청 API
    - / draftvacation
    - 요청url:
        -http://127.0.0.1:8000/draftvacation?draft_sdate=휴가첫날&draft_edate=마지막날&key=고유키값
    - 예시(2020/03/05~2020/03/15 휴가신청시):
        -http://127.0.0.1:8000/draftvacation?draft_sdate=20200305&draft_edate=20200315&key=고유키값  
    - 성공
        - {"휴가 기안 작성이 완료되었습니다.",200}
    