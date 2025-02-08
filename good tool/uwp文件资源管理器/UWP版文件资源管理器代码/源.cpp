#include<windows.h>
#pragma comment( linker, "/subsystem:\"windows\" /entry:\"mainCRTStartup\"" )
using namespace std;
int main()
{
	ShowWindow(FindWindow(L"ConsoleWindowClass", NULL), SW_HIDE);
	system("C:\\Windows\\explorer.exe shell:AppsFolder\\c5e2524a-ea46-4f67-841f-6a9465d9d515_cw5n1h2txyewy!App");
}