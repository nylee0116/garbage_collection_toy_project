#include <stdio.h>
#include "gc.h"

int main() {
    VM* vm = new_vm();
    
    // 테스트 1- 가비지 많이 생성하기
    // Eden이 200KB고 객체가 약 32바이트니까, 6,400개 정도
    // 10,000개를 만들면 중간에 GC가 한 번 돌아야함.
    
    printf("--- Generating Garbage ---\n");
    for (int i = 0; i < 10000; i++) {
        new_object(vm, OBJ_INT); // 만들고 바로 스택에서 pop하지 않지만, pop하면 가비지가 됨
        pop(vm); // 바로 pop -> 가비지가 됨
    }
    
    // 테스트 2- 살아있는 객체 유지되는지 확인
    printf("\n--- Checking Live Objects ---\n");
    Object* a = new_object(vm, OBJ_INT);
    a->data.value = 100;
    
    Object* b = new_object(vm, OBJ_INT);
    b->data.value = 200;
    
    Object* pair = new_object(vm, OBJ_PAIR);
    pair->data.pair.head = a;
    pair->data.pair.tail = b;
    
    // 강제로 GC 유발 (더미 객체 왕창 생성)
    printf("Triggering GC by force allocation...\n");
    for (int i = 0; i < 50000; i++) {
        Object* dummy = new_object(vm, OBJ_INT);
        pop(vm);
    }
    
    // GC 후에도 pair가 가리키는 값이 100, 200인지 확인
    // (GC가 돌았다면 a, b, pair의 주소는 바뀌었겠지만 값은 유지되어야 함)
    printf("Value of pair->head: %d (Expected: 100)\n", pair->data.pair.head->data.value);
    printf("Value of pair->tail: %d (Expected: 200)\n", pair->data.pair.tail->data.value);

    return 0;
}