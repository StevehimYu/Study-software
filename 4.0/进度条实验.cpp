#include <bits/stdc++.h>
#include <windows.h>
using namespace std;
int target = 10;

string _list[10] = {"fsfsfs", "fsdfsfs", "DFgdgf", "hrthr", "hfghssg", "dtesgsdf", "SDfgegs", "gfgdgf", "gsdergb", "bcvbnsrb"};
void _print(int num) {
	for (int i = 0; i < num; i++) {
		printf("¡ö");
	}
	for (int i = 0; i < 10 - num + 1; i++) {
		printf("  ");
	}
}

int main() {
	for (int i = 0; i < 10; i++) {
//		char ch;
		_print(i + 1);
		printf("ÕýÔÚ¼ì²é");
		cout << _list[i];
		Sleep(200);
		system("cls");
//		cout << endl;
	}
	return 0;
}
