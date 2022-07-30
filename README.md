# kleenex-backend

## 팀원

 - BACKEND
 
 김도연, 안상현
 
 - FRONTEND
 
 김영수, 오창훈, 최원익

## 개발 기간
- 개발 기간 : 2022-07-18 ~ 2022-07-29 (12일)
- 협업 툴 : Slack, Trello, Github, Notion

## 프로젝트 목표

테라로사(https://terarosa.com/) 사이트 클론코딩

---

### 구현 사항

공통: ERD모델링

**김도연**
- 회원가입
   - 비밀번호 암호화(Bcrypt)
   - 이메일, 비밀번호 정규식 사용
- 로그인
   - 로그인시 토큰 발행(JWT)
- 장바구니
   - 발행한 토큰으로 유저인증기능 구현
   - 관련 장바구니 정보 전달 
   - 장바구니 페이지 내 주문상품 수정 및 삭제 기능 구현

**안상현**

- 메인화면
   - 고가 상품, 로스팅최신순 상품 정보 전달
- 상품리스트 및 상품 상세정보 
   - 상품정보 전체 리스트 전달
   - 카테고리별 상품 정보 전달
   - Pagination구현(limit & offset)
- 상품 필터링기능
   - 상품 맛별 다중 선택 필터링 기능 구현
   - 가격, 로스팅 데이트 기준 정렬기능 구현
- 검색 기능 구현
   - 상품명 검색 기능 구현

---

## 사이트 시현 영상

https://user-images.githubusercontent.com/99232122/181917935-402877fe-ae48-42bd-871c-3246b5ac6bf7.mov

## DB모델링
![DB](https://user-images.githubusercontent.com/99232122/181917443-5e959b79-4af4-4775-9c71-8be9a1e22194.png)


## 기술 스택
|                                                Language                                                |                                                Framwork                                                |                                               Database                                               |                                                     ENV                                                      |                                                   HTTP                                                   |                                                  Deploy                                                 |
| :----------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------: |:------------------------------------------------------------------------------------------------------: |
| <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> | <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> | <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=black"> | <img src="https://img.shields.io/badge/miniconda3-44A833?style=for-the-badge&logo=anaconda&logoColor=white"> | <img src="https://img.shields.io/badge/postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white"> | <img src="https://img.shields.io/badge/aws-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white">|



