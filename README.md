# garbage-collection-toy-project
숙명여자대학교 2025-2 학습공동체 Py-C Bridge팀의 Garbage Collection Toy Project repository입니다.
---
## 1. 프로젝트 개요
이 프로젝트는 숙명여자대학교 2025-2 학습공동체 최종 결과물인 Toy Project입니다.  
**Uniprocessor Garbage Collection Techniques** 논문을 참고하였습니다.

## 2. 개발 배경  
**CS 기초 탐구:** C언어 기반의 프로세스 메모리 구조(Stack, Heap 등) 연구를 통해 수동 관리의 한계를 체감하고, 자동 메모리 관리(GC)의 필요성을 학습했습니다.  
**이론의 시각화:** 논문으로 접한 추상적인 GC 알고리즘이 실제 메모리 참조 그래프 상에서 어떻게 작동하는지 확인하고자 했습니다.

## 3. 핵심 기술 및 알고리즘
* **Treadmill Abstraction:** Baker의 실시간 GC 알고리즘 추상화 
* **Dijkstra Write Barrier:** 증분형 마킹을 위한 동시성 제어 기법 
* **Serial Generational GC:** 세대별 가설을 적용한 메모리 관리 
* **Copying GC:** 메모리 단편화 해결을 위한 복사 알고리즘 
### Language : ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![C](https://img.shields.io/badge/C-00599C?style=flat&logo=c&logoColor=white)
### Visualization : ![NetworkX](https://img.shields.io/badge/NetworkX-2E8B57?style=flat&logo=networkx&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat&logo=matplotlib&logoColor=white)

## 4. 세부 내용 (Detail)
**4-1. GC_treadmill_Dijkstra**
프로젝트 구조
```bash
├── memory.py      # Treadmill Heap 구조 및 Tensor 객체 (White/Grey/Black)  
├── logic.py       # Dijkstra Write Barrier 및 GC 로직 구현  
├── visualizer.py  # NetworkX 기반의 시각화 모듈  
├── simulator.py   # 시뮬레이션 시나리오 및 스냅샷 관리  
└── main.py        # 프로그램 실행 
```
* **Step 1:** 초기 tensor 할당 및 Root 마킹 (Tri-color Markin)
* **Step 2:** GC 사이클 시작 (Incremental Marking)
* **Step 3:** **Mutator 개입, Write Barrier 발동**
    * Root(Black)가 아직 방문하지 않은 Tensor_A(White)를 참조할 때, Barrier가 작동하여 Tensor_A를 Grey로 바꾸는 과정 시각화
* **Step 4:** GC 완료 및 Garbage(White) 회수 
![이나연_toy_project_결과](https://github.com/user-attachments/assets/f09a1125-db1a-4897-9d92-5fe92efede59)

향후 과제 
* 실제 AI 모델의 텐서 할당 패턴을 적용하여 Efficient ML을 고려한 시뮬레이션 고도화
* Multi-thread 환경에서의 Write Barrier 동시성 제어 로직 추가 구현

---
**4-2. Serial_Gen_GC**
프로젝트 구조
```bash
├── gc.c       
├── gc.h      
├── main.c  
├── toy_gc.exe  
└── Serial Generational GC 토이 프로젝트 설명.md       
```  
프로젝트 목표 (Objectives)  
: 이론으로 배운 다음 3가지의 내용을 직접 구현한다

1. "대부분의 객체는 금방 죽는다"는 가설을 전제로, 힙을 두 영역(Young/Old)으로 나누는 것
2. GC가 실행될 때 객체의 메모리 주소가 바뀜(Copy/Compact). 이때 이 객체를 가리키고 있던 다른 객체들의 포인터를 깨지지 않고 갱신하는 것 구현
3. `malloc`을 쓰지 않고 포인터 덧셈만으로 메모리를 할당하는 Bump Pointer Allocation 구현

***Serial Generational GC 토이 프로젝트 설명.md에 자세한 내용 명시**

---
**4-3. WriteBarrier_Gen_GC**

## 5. 작성자 (Author)
* **Name:** 이나연
* **Major:** 숙명여자대학교 인공지능공학부 24학번 (2학년)
* **Role:** (GC_treadmill_Dijkstra) Treadmill Abstraction 구현, Dijkstra Write Barrier 시뮬레이션 설계 및 시각화
* **Contact:** nylee16@sookmyung.ac.kr
* **GitHub:** nylee0116
---
* **Name:** 문예선
* **Major:** 숙명여자대학교 소프트웨어학부 25학번 (1학년)
* **Role:** JVM의 기본 GC인 Serial Genrational GC 구현
* **Contact:** munyeseon@sookmyung.ac.kr
* **GitHub:** tjsl0607
---
* **Name:** 조현진
* **Major:** 숙명여자대학교 컴퓨터과학부 24학번 (2학년)
* **Role:** Generational GC write barrier 구현
* **Contact:** arthur_02@sookmyung.ac.kr
* **GitHub:** tjsl0607
