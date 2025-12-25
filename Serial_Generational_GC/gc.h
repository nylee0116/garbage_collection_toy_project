#ifndef GC_H
#define GC_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#define HEAP_SIZE (1024 * 1024)   // 전체 힙 1MB
#define STACK_MAX 256             // 스택 최대 깊이
#define REMEMBERED_SET_MAX 1024   // Old -> Young 참조 기록 최대 개수


typedef enum {
    OBJ_INT,   // 정수 값 (Leaf 노드)
    OBJ_PAIR   // 두 개의 다른 객체를 가리킴 (참조 노드)
} ObjectType;

// 전방 선언
struct Object;

typedef struct Object {
    ObjectType type;    
    unsigned char age;             // Promotion 기준
    bool marked;                   // 방문 여부 확인
    struct Object* forwarding_ptr; // Copying GC 중 이동된 주소 저장

    // 편의를 위해 구조체 사용
    union {
        int value; // OBJ_INT일 때 사용
        struct {
            struct Object* head;
            struct Object* tail;
        } pair;    // OBJ_PAIR일 때 사용
    } data;
    
} Object;

typedef struct { // 메모리 관리자
    // 전체 힙 메모리 덩어리
    void* heap_start;

    // Young Gen
    void* eden_start;
    void* eden_end;
    void* eden_top; // Bump Pointer

    // Survivor (S0, S1)
    void* survivor_1_start;
    void* survivor_1_end;
    void* survivor_2_start;
    void* survivor_2_end;
    
    // To-Space 포인터
    void* survivor_to_start;   // 목적지
    void* survivor_from_start; // 출발지 (현재 live)

    // Old Gen
    void* old_start;
    void* old_end;
    void* old_top; 

    // Root Set
    Object* stack[STACK_MAX];
    int stack_count;

    // Remembered Set (나중에 구현)
    Object* remembered_set[REMEMBERED_SET_MAX];
    int remembered_set_count;

} VM;


VM* new_vm();
Object* new_object(VM* vm, ObjectType type);
void push(VM* vm, Object* obj);
Object* pop(VM* vm);
void minor_gc(VM* vm);

#endif // GC_H