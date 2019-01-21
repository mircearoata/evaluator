#include <fstream>

using namespace std;

ifstream in("test.in");
ofstream out("test.out");

int main()
{
	int n;
	in >> n;
    out << n+1;
    return 0;
}
