"""
Project : Treadmill-based Incremental GC Simulator for AI Tensors
Author  : 이나연 (숙명여자대학교 인공지능공학부 2학년)
Date    : 2025. 12. 24
Context : CS Memory Management Study - Toy Project
"""

from memory import TreadmillHeap
from logic import WriteBarrierGC
from visualizer import print_memory_state, draw_memory_graph

"""
mutator에 의해 참조하는 객체가 변할 때 
write barrier 발동
"""

class GCSimulator:
    def __init__(self):
        #시각화 관련 전역 변수
        self.step_counter = 0
        self.visualization_mode = "SHOW"

        self.graph_pos = None

        #heap, GC 관련 전역 변수
        self.heap = TreadmillHeap()
        self.gc = WriteBarrierGC(self.heap)

    def configure_visualization(self):
        print("-----------------"*5)
        print("Dijkstra 기반 GC Simulator (AI Tensor Memory)")
        print("-----------------"*5)
        print("\n** <화면에 띄우기>는 창이 하나씩 실행됩니다.")
        user_input = input("시각화 방식을 선택하세요 (1: 화면에 띄우기, 2: 이미지 저장, 그 외 숫자 : text log만 출력) : ")

        if user_input == "1":
            self.visualization_mode = "SHOW"
            print("화면 출력 모드입니다.")
        elif user_input == "2":
            self.visualization_mode = "SAVE"
            print("파일 저장 모드입니다.")
        
        else:
            self.visualization_mode = "OFF"
            print("시각화 없이 text log만 출력합니다.")

    def save_snapshot(self, description, mutator_active=False):
        #인자로 description 하나 받음
        self.step_counter += 1

        print_memory_state(self.heap, description)

        if self.visualization_mode == "SAVE":
            filename=f"step_{self.step_counter:02d}_{description}.png"
            self.graph_pos=draw_memory_graph(self.heap, title=description, filename=filename, fixed_pos=self.graph_pos, show_mutator_label=mutator_active)

        elif self.visualization_mode == "SHOW":
            self.graph_pos=draw_memory_graph(self.heap, title=description, filename=None, fixed_pos=self.graph_pos, show_mutator_label=mutator_active)
        else:
            print("시각화를 건너뜁니다.")
            pass

    def run(self):
        """실제 simulation 시나리오"""

        #설정 받기
        self.configure_visualization()

        #객체 생성
        root = self.heap.allocate("Root_Model")
        tensor_a = self.heap.allocate("Tensor_A")
        tensor_b = self.heap.allocate("Tensor_B")

        self.save_snapshot("01_Initial_State") #시각화 1

        #GC 시작
        print(">>> GC 사이클 시작, Root를 Grey로 이동")
        self.heap.move_to_grey(root)
        self.save_snapshot("02_Root_Marked_Grey") #시각화 2
        
        self.gc.step() #root 스캔 => 자식 없음 => root는 black됨
        self.save_snapshot("03_GC_First_Scan") #시각화 3

        #메인 시나리오 : mutator 개입 (Dijkstra barrier)
        #=> 이미 black이 된 root가 아직 white인 객체 tensor_a를 가리키게 하기
        print(">>> mutator 개입 : root(black)이 tensor_a(white) 연결 시도")
        #barrier 발동
        self.gc.write_barrier(root, tensor_a) 

        #Barrier 발동 후 / root가 grey로 복귀했는지 확인 필요
        self.save_snapshot("04_Barrier_Triggered", mutator_active=True) #시각화 4

        #Barrier 발동 후 / root가 grey로 복귀했는지 확인 필요

        #GC 재개
        loop_count = 0
        while self.gc.step():
            loop_count += 1
            self.save_snapshot(f"05_GC_Progress_{loop_count}") #시각화 5
        
        print(">>> GC 완료, 살아남은 객체는 Balck, 나머지는 White(Garbage)")
        self.save_snapshot("06_GC_Completed") #시각화 6, 최종 결과
