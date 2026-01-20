#include <iostream>
using namespace std;

int main() {
    int a;
    cin>>a;
    double b;
    cin>>b;
    if(b/a*100<80){
        cout<<"NO";
    }else{
        cout<<"YES";
    }
    return 0;
}
