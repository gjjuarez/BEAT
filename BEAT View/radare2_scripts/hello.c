#include <stdio.h>

int myGlobal = 11;
void addition(int addVar) {
	addVar++;
}
int otherGlobal = 6;

struct S1 {
    int x;
    int z;
};

int main(){
	int myVar = 5;
	printf("hello world");
	addition(myVar);
	struct S1 myStruct = {12, 3};
	return 0;
}
