#include "LinkedList.hpp"

struct myNode {
  SmartPointer<myNode> next;
};


int main(){

    LinkedList<int> list;

    SmartPointer<myNode> sp1(new myNode);
    SmartPointer<myNode> sp2(new myNode);
    SmartPointer<myNode> sp3(new myNode);

    sp1->next = sp2;
    sp2->next = sp3;
    sp3->next = sp1;
     
    ~sp1;
    ~sp2;
    ~sp3;
}

// To free a node you have to delete all SmartPointers to that node, which means the reference counter has to be 0.
// Since each SmartPointer points has a node and each node has a next SmartPointer pointing the next node, 
// each SmartPointer's reference counter is 2. 

// After executing line 20, the reference counter for sp1 is 1, since sp3 has a SmartPointer 
// to sp1 and the node of sp1 doesn't get freed. 
// After line 21, the reference counter for sp2 is 1, since there exists SmartPointer of 
// sp3 pointing to sp2's node. Therefore, node sp2 won't be freed as well. 
// After line 22, the reference counter of sp3 will also be 1, since the SmartPointer next of 
// sp1 node points to sp3. So sp3's node doesn't get freed. 
// Therefore, all of the SmartPointer's reference counters are 1 and none of the nodes get free.

