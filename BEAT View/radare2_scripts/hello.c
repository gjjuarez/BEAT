#include <stdio.h>

int myGlobal = 11;
int addition(int addVar) {
	addVar++;
	return addVar;
}
int otherGlobal = 6;
char myCharGlobal = 'Y';

char* stringFunction() {
	return "this is a string";
}

void nothingFunction() {
}

int main(){
	int myVar = 5;
	printf("hello world");
	addition(myVar);
	myCharGlobal = 'N';

	myVar = addition(myVar);
	char* myString = stringFunction();
	return 8;
}
