#include <stdio.h>

int myGlobal = 11;
int addition(int addVar) {
	addVar++;
	return addVar;
}
int otherGlobal = 6;
char myCharGlobal = 'Y';

struct S1 {
    int x;
    int z;
};

int main(){
	int myVar = 5;
	printf("hello world");
	addition(myVar);
	myCharGlobal = 'N';

	myVar = addition(myVar);
	return 8;
}
