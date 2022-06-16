# DRF_Practice
해당 Repository는 DRF 연습을 위한 Repository입니다.

***

## 1일차 과제
1. args, kwargs를 사용하는 예제 코드 짜보기.

2. mutable과 immutable은 어떤 특성이 있고, 어떤 자료형이 어디에 해당하는지 서술하기.

3. DB Field에서 사용되는 Key 종류와 특징 서술하기.

4. django에서 queryset과 object는 어떻게 다른지 서술하기.

***

### 1. args, kwargs 예제 코드
args : 복수의 인자를 함수로 받을 수 있다.  
kwargs : args와 비슷하나 함수를 (키워드 = 값)의 형태로 받을 수 있다.  

**[예제 코드]**  
```python
def argument(num, *args, **kwargs):
    print(f"num : {num}")
    print(f"args : {args}")
    print(f"kwargs : {kwargs}")

    return argument

argument(100, 1, 2, 3, 4, 5, num1=1, num2=2, num3=3)
```

**[실행 결과]**  
![ex1](/img/1.png)  

*args와 **kwargs에서 변수명 args와 kwargs를 다른 변수명으로 적어도 정상적으로 작동된다.  
키워드 인수를 표시하는 *과 **만 잘 적어준다면 변수명이 달라도 괜찮다.

**[변수명 변경 예제 코드]**
```python
def argument(num, *jinu, **racoon):
    print(f"num : {num}")
    print(f"jinu : {jinu}")
    print(f"racoon : {racoon}")

    return argument

argument(100, 1, 2, 3, 4, 5, num1=1, num2=2, num3=3)
```

**[실행 결과]**  
![ex2](/img/2.png)  

***

### 2. mutable, immutable 특성
**[특성]**  
mutable : 변할 수 있는 값  
immutable : 변할 수 없는 값

**[해당되는 자료형]**  
mutable : list, dictionary, set 등  
immutable : int, float, string, tuple 등  

***

### 3. DB Field의 Key 종류와 특징
**[Key]**  
**릴레이션(=테이블)**  
    - 데이터베이스의 데이터들을 표의 형태로 표현한 것  

**튜플 : Tuple**  
    - 릴레이션을 구성하는 행  
    - 튜플의 수를 기수(Cardinality)라고 부른다.  

**속성 : Attribute**  
    - 릴레이션을 구성하는 열  
    - 속성의 수를 차수(Degree)라고 부른다.  

**[키 종류와 특징]**  
**후보키 : Candidate Key**  
    - 릴레이션을 구성하는 속성들 중 튜플을 유일하게 식별할 수 있는 속성들의 부분 집합  
    - 모든 릴레이션은 하나 이상의 후보키를 가져야하며 유일성(Unique)과 최소성(Minimality)을 만족해야 한다.  

**기본키 : Primary Key**  
    - 후보키 중에서 선택한 주가 되는 키  
    - 릴레이션에서 특정 레코드를 유일하게 식별할 수 있는 속성, Null 값으로 둘 수 없다.  

**대체키 : Replacement Key**  
    - 후보키 중에서 기본키를 제외한 나머지 속성들  

**외래키 : Foreign Key**  
    - 관계를 맺는 릴레이션 간에 기본키를 참조하는 속성  
    - 하나의 릴레이션에는 다수의 외래키가 존재할 수 있다.  
    - 외래키로 지정된 필드는 중복 및 Null 값으로 둘 수 있다.  

**슈퍼키 : Super Key**  
    - 하나의 릴레이션 내에 있는 속성들의 집합  
    - 슈퍼키로 구성된 속성의 집합은 동일한 값으로 나타나지 않는다.  
    - 릴레이션을 구성하는 튜플들에 대해 유일성은 만족하나 최소성은 만족하지 못한다.  

***

### 4. django의 object, queryset
object : DB 모델에 대한 객체  
queryset : DB 모델에서 전달받은 객체(object)들의 목록  

**[ORM 활용 명령어 사용 방법]**  
[Model명].objects.~  

**[불러오기]**  
.all() : 전체 데이터 불러오기  
.get() : 하나의 데이터 불러오기  

**[조회]**  
.filter() : 조건에 해당되는 데이터 조회  
.exclude() : 조건에 해당되지 않는 데이터 조회  

**[생성]**  
.create() : 해당되는 모델 객체에서 원하는 데이터를 생성  

**[삭제]**  
.delete() : 해당되는 모델 객체에서 원하는 데이터를 삭제  

**[정렬]**  
.order_by() : 오름차순 '필드명' / 내림차순 '-필드명'  

***

## 2일차 과제
1. Django 프로젝트를 생성하고, user 라는 앱을 만들어서 settings.py 에 등록해보세요.

2. user/models.py에 `Custom user model`을 생성한 후 django에서 user table을 생성 한 모델로 사용할 수 있도록 설정해주세요.

3. user/models.py에 사용자의 상세 정보를 저장할 수 있는 `UserProfile` 이라는 모델을 생성해주세요.

4. blog라는 앱을 만든 후 settings.py에 등록해주세요.

5. blog/models.py에 <카테고리 이름, 설명>이 들어갈 수 있는 `Category`라는 모델을 만들어보세요.

6. blog/models.py에 <글 작성자, 글 제목, 카테고리, 글 내용>이 들어갈 수 있는 `Article` 이라는 모델을 만들어보세요. (카테고리는 2개 이상 선택할 수 있어야 해요)

7. Article 모델에서 외래 키를 활용해서 작성자와 카테고리의 관계를 맺어주세요.

8. admin.py에 만들었던 모델들을 추가해 사용자와 게시글을 자유롭게 생성, 수정 할 수 있도록 설정해주세요.

9. CBV 기반으로 로그인 / 로구아웃 기능을 구현해주세요.

10. CBV 기반으로 로그인 한 사용자의 게시글의 제목을 리턴해주는 기능을 구현해주세요.

***