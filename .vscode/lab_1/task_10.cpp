#include <iostream>
using namespace std;

int main() {
    int a;
    cin>>a;
    int b;
    cin>>b;
    int c;
    cin>>c;
    if(a+b>c && b+c>a && a+c>b){
        cout<<"Yes";
    }else{
        cout<<"No";
    }
    return 0;
}
