"""
Project : Treadmill-based Incremental GC Simulator for AI Tensors
Author  : 이나연 (숙명여자대학교 인공지능공학부 2학년)
Date    : 2025. 12. 24
Context : CS Memory Management Study - Toy Project
"""

def print_memory_state(heap, step_name):
    print("\n")
    print(f"State: {step_name}")
    print(f"WHITE(미방문, 신규): {heap.white_list}")
    print(f"GREY(방문중, 대기): {heap.grey_list}")
    print(f"BLACK(방문완료, 보존): {heap.black_list}")

#시각화 관련 함수
import networkx as nx
import matplotlib.pyplot as plt

#TreadmillHeap 상태를 그래프로 그리기
def draw_memory_graph(heap, title="Memory State", filename=None, fixed_pos=None, show_mutator_label=False):
    Graph = nx.DiGraph() #방향 그래프

    #노드 추가 및 색상 설정
    color_map = []
    all_objects=heap.white_list + heap.grey_list + heap.black_list 

    for obj in all_objects:
        Graph.add_node(obj.name) #networkx 내장 함수

        if obj.color == "WHITE":
            color_map.append("white") #시각적인걸 고려하여 light blue도 사용 가능
        elif obj.color=="GREY":
            color_map.append("lightgrey")
        elif obj.color=="BLACK":
            color_map.append("#3A3A3A") #글씨 때문에 검정 대신 진한 회색 사용하려면 dimgrey 사용하기
        else:
            color_map.append("red") #에러처리용

    #edge 추가
    for obj in all_objects:
        for child in obj.children:
            Graph.add_edge(obj.name, child.name) #networkx 내장 함수

    plt.figure(figsize=(10,8)) #크기

    if fixed_pos is None:
        pos = nx.spring_layout(Graph, seed=42, k=1.5) #노드 배치 스타일
    else:
        pos = fixed_pos

    #노드, 엣지, 라벨 그리기
    nx.draw_networkx_nodes(Graph, pos, node_color=color_map, node_size=2000, edgecolors="black")
    nx.draw_networkx_edges(Graph, pos, edge_color = "black", arrows=True)
    
    label_pos = {k: (v[0], v[1] + 0.09) for k, v in pos.items()} #Y축 방향으로 이동
    
    nx.draw_networkx_labels(Graph, label_pos, font_weight="bold", font_size=12, font_color="black")

    #mutator 강조 라벨
    if show_mutator_label:
        # 그래프 상단 중앙(x=0, y=1.2 정도 위치)에 빨간색 텍스트 추가
        plt.text(0, 1.3, "Mutator Intervened! (Write Barrier Triggered)", 
        fontsize=14, color='red', ha='center', fontweight='bold',
        bbox=dict(facecolor='yellow', alpha=0.3, edgecolor='red')) # 노란색 배경 박스 추가

    plt.margins(0.2)
    plt.title(title)

    if filename:
        plt.savefig(filename)
        print(f"saved {filename}")
        plt.close()
    else:
        plt.show()
    
    return pos