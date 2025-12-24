"""
================================================================================
Project : Treadmill-based Incremental GC Simulator for AI Tensors
        (트레드밀 기반 증분형 가비지 컬렉션 시뮬레이터)
Author  : 이나연 (숙명여자대학교 인공지능공학부 2학년)
Date    : 2025. 12. 24
Context : CS Memory Management Study - Toy Project
--------------------------------------------------------------------------------
Description :
    이 프로그램은 Baker's Treadmill 알고리즘과 Dijkstra's Write Barrier를
    기반으로 한 AI 텐서(Tensor) 메모리 관리 시뮬레이터입니다.
    
    주요 기능:
    1. Treadmill 추상화: White/Grey/Black 리스트를 통한 객체 수명 관리
    2. Write Barrier: Mutator 개입 시 발생하는 참조 변경 감지 및 색상 보정
    3. Visualization: NetworkX & Matplotlib을 활용한 단계별 메모리 상태 시각화
    
    * Mutator가 실행 도중 참조를 변경할 때(Write Barrier 발동), 
    회색(Grey)으로 마킹이 복구되는 과정을 시각적으로 검증합니다.
================================================================================
"""

from simulator import GCSimulator

def main():
    #시뮬레이션 객체 생성 및 실행
    sim = GCSimulator()
    sim.run()

if __name__ == "__main__":
    main()