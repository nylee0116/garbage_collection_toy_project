"""
Project : Treadmill-based Incremental GC Simulator for AI Tensors
Author  : 이나연 (숙명여자대학교 인공지능공학부 2학년)
Date    : 2025. 12. 24
Context : CS Memory Management Study - Toy Project
"""

#객체와 리스트 관리(white, grey, black)
class GCObject:
    #메모리에 할당되는 하나의 객체
    def __init__(self,name):
        self.name = name
        self.color = "WHITE" #다익스트라 방식 초기 할당 white
        self.children = [] #(references) 이 객체가 가리키는 다른 객체들
        
    def __repr__(self):
        return self.name

class TreadmillHeap:
    #treadmill구조의 메모리 공간 관리하는 class
    #객체를 이동시키는 물리적 역할

    def __init__(self):
        #4개의 논리적 list (white / grey / black / free)
        #New, Free, From, To는 물리적 list

        self.white_list = [] #할당 직후, 방문 전
        self.grey_list = [] #방문 중
        self.black_list = [] #스캔 완료
        self.free_list = []

    def allocate(self,name):
        #(다익스트라) 새 객체를 White List로 할당
        new_obj = GCObject(name)
        new_obj.color = "WHITE"
        self.white_list.append(new_obj)
        print(f"[Allocation] {name} 생성됨 (White List)")
        return new_obj
    
    def move_to_grey(self, obj):
        #객체를 Grey List로 이동 (마킹 시작 또는 장벽 발동)
        if obj in self.white_list:
            self.white_list.remove(obj)
        elif obj in self.black_list:
            self.black_list.remove(obj)

        obj.color = "GREY"
        self.grey_list.append(obj)

    def move_to_black(self, obj):
        #객체를 Balck List로 이동 (스캔 완료)
        if obj in self.grey_list:
            self.grey_list.remove(obj)
        
        obj.color = "BLACK"
        self.black_list.append(obj)