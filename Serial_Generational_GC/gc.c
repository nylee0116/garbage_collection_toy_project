#include <stdio.h>
#include <string.h>
#include "gc.h"

// 승격 기준 나이 (3번 살아남으면 Old로 이동)
#define AGE_THRESHOLD 3

// GC 수행 중에만 사용하는 전역 변수 (Young Gen 할당용)
static void* free_ptr; 

// 함수 프로토타입 수정 (vm 인자 추가)
static Object* copy_object(VM* vm, Object* obj);


// VM 생성 및 관리 
VM* new_vm() {
    VM* vm = (VM*)malloc(sizeof(VM));
    if (!vm) return NULL;

    vm->heap_start = calloc(1, HEAP_SIZE);
    char* heap_cursor = (char*)vm->heap_start;

    // 1. Young Generation (Eden: 200KB)
    vm->eden_start = heap_cursor;
    vm->eden_top = vm->eden_start;
    vm->eden_end = heap_cursor + (200 * 1024);
    heap_cursor += (200 * 1024);

    // Survivor 1 (100KB)
    vm->survivor_1_start = heap_cursor;
    vm->survivor_1_end = heap_cursor + (100 * 1024);
    heap_cursor += (100 * 1024);

    // Survivor 2 (100KB)
    vm->survivor_2_start = heap_cursor;
    vm->survivor_2_end = heap_cursor + (100 * 1024);
    heap_cursor += (100 * 1024);

    vm->survivor_from_start = vm->survivor_1_start;
    vm->survivor_to_start = vm->survivor_2_start;

    // 2. Old Generation (나머지 전부)
    vm->old_start = heap_cursor;
    vm->old_top = vm->old_start;
    vm->old_end = (char*)vm->heap_start + HEAP_SIZE;

    vm->stack_count = 0;
    
    printf("[Init] VM Heap initialized.\n");
    return vm;
}

void push(VM* vm, Object* obj) {
    if (vm->stack_count < STACK_MAX) {
        vm->stack[vm->stack_count++] = obj;
    }
}

Object* pop(VM* vm) {
    if (vm->stack_count > 0) {
        return vm->stack[--vm->stack_count];
    }
    return NULL;
}

Object* new_object(VM* vm, ObjectType type) {
    size_t size = sizeof(Object);

    // Eden 공간 부족 시 GC 트리거
    if ((char*)vm->eden_top + size > (char*)vm->eden_end) {
        minor_gc(vm);
        
        // GC 후에도 부족하면 OOM
        if ((char*)vm->eden_top + size > (char*)vm->eden_end) {
            printf("[OOM] Eden Full! Cannot allocate object.\n");
            exit(1);
        }
    }

    // Bump Pointer Allocation
    Object* obj = (Object*)vm->eden_top;
    vm->eden_top = (char*)vm->eden_top + size;

    obj->type = type;
    obj->age = 0;
    obj->marked = false;
    obj->forwarding_ptr = NULL;
    
    // 루트 셋 보호를 위해 자동 푸시 (실제 VM 동작 모방)
    push(vm, obj); 

    return obj;
}

// GC 핵심 로직

static Object* copy_object(VM* vm, Object* obj) {
    if (obj == NULL) return NULL;

    // Forwarding Pointer
    if (obj->forwarding_ptr != NULL) {
        return obj->forwarding_ptr;
    }

    // Promotion Check
    bool should_promote = (obj->age >= AGE_THRESHOLD);
    
    Object* new_obj;

    if (should_promote) {
        // Case A- Old Generation으로 승격
        // Old 영역 공간 확인
        if ((char*)vm->old_top + sizeof(Object) > (char*)vm->old_end) {
            printf("[Critical] Old Generation Full! (Major GC required but not impl)\n");
            exit(1); 
        }

        new_obj = (Object*)vm->old_top;
        vm->old_top = (char*)vm->old_top + sizeof(Object); // Bump Old Top
        
        printf("  >> [Promoted] Object moved to Old Gen (Addr: %p)\n", (void*)new_obj);

    } else {
        // Case B- Survivor로 이동
        new_obj = (Object*)free_ptr;
        free_ptr = (char*)free_ptr + sizeof(Object); // Bump Free Ptr
        
        new_obj->age = obj->age + 1; // 나이 증가
    }

    // 내용 복사
    memcpy(new_obj, obj, sizeof(Object));

    // Forwarding Pointer 설정
    obj->forwarding_ptr = new_obj;
    new_obj->forwarding_ptr = NULL; // 새 객체는 아직 이동 안 함

    // Promotion Edge Case Handling
    // 만약 객체가 승격되었다면, minor_gc의 while 루프(Scan)가 이 객체를 방문하지 못함.
    // (Scan 루프는 Survivor 영역만 돌기 때문)
    // 따라서 승격된 객체의 자식들은 여기서 즉시 처리해줘야 함 (DFS 방식 혼용)
    if (should_promote) {
        if (new_obj->type == OBJ_PAIR) {
            new_obj->data.pair.head = copy_object(vm, new_obj->data.pair.head);
            new_obj->data.pair.tail = copy_object(vm, new_obj->data.pair.tail);
        }
    }

    return new_obj;
}

void minor_gc(VM* vm) {
    printf("\n--- Minor GC Start ---\n");

    // To-Space 준비 - free_ptr 초기화
    free_ptr = vm->survivor_to_start;

    // Root Set (Stack) 스캔
    for (int i = 0; i < vm->stack_count; i++) {
        vm->stack[i] = copy_object(vm, vm->stack[i]);
    }

    // Cheney's Algorithm (BFS Scan)
    // Scan 포인터가 Free 포인터를 따라잡을 때까지 반복
    // 여기서는 Survivor To-Space에 있는 객체들만 스캔함
    char* scan_ptr = (char*)vm->survivor_to_start;
    
    while (scan_ptr < (char*)free_ptr) {
        Object* obj = (Object*)scan_ptr;

        if (obj->type == OBJ_PAIR) {
            // 자식들도 Survivor로 데려오거나, 승격시킴
            obj->data.pair.head = copy_object(vm, obj->data.pair.head);
            obj->data.pair.tail = copy_object(vm, obj->data.pair.tail);
        }

        scan_ptr += sizeof(Object);
    }

    // 4. Swap Survivor Spaces
    void* temp = vm->survivor_from_start;
    vm->survivor_from_start = vm->survivor_to_start;
    vm->survivor_to_start = temp;

    // 5. Eden 초기화 (싹 비움)
    vm->eden_top = vm->eden_start;

    printf("--- Minor GC Finished. Eden Reset. ---\n\n");
}