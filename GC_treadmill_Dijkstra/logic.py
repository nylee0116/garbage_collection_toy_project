"""
Project : Treadmill-based Incremental GC Simulator for AI Tensors
Author  : 이나연 (숙명여자대학교 인공지능공학부 2학년)
Date    : 2025. 12. 24
Context : CS Memory Management Study - Toy Project
"""

#dijkstra 기반 쓰기 장벽(barrier), collection logic
from memory import TreadmillHeap

class WriteBarrierGC:
    def __init__(self, heap: TreadmillHeap):
        self.heap = heap

    def write_barrier(self, source, target):
        #dijkstra incremental update barrier 부분
        #참조가 변경될 때 호출됨
        #규칙 : black 객체가 white 객체를 가리키면 black을 grey로 바꾼다 (다시 참조하기 위해서)

        #Mutator : 자식 객체 추가 / 필요 시 write_barrier와 분리 가능
        source.children.append(target)

        #장벽 로직, black 객체가 white 객체를 가리키게 되었을 때
        if source.color == "BLACK" and target.color == "WHITE":
            print(f"[Barrier Triggered] {source.name}(BLACK)이 {target.name}(WHITE)를 가리킵니다.")
            print(f"=>{source.name}을 GREY로 되돌립니다.")
            self.heap.move_to_grey(source)

    def step(self):
        #GC가 Incremental하게 수행. Grey List에서 하나 꺼내서 자식 스캔
        if not self.heap.grey_list:
            print("[GC] Grey List is empty")
            return False
        
        #Grey List에서 객체를 하나 꺼내기
        current_obj = self.heap.grey_list[0]
        print(f"[GC] {current_obj.name} 스캔")

        #자식 객체 확인하기 (추적, trace)
        for child in current_obj.children:
            if child.color == "WHITE":
                print(f"=> 자식 {child.name}(WHITE) 발견, Grey로 이동")
                self.heap.move_to_grey(child)

        self.heap.move_to_black(current_obj)
        return True