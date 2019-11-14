#include <stdio.h>

int myGlobal = 11;
void addition(int addVar) {
	addVar++;
}
int otherGlobal = 6;

int main(){
	int myVar = 5;
	printf("hello world");
	addition(myVar);
	return 0;
}
