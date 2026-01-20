#include <iostream>
using namespace std;

int main() {
    int a;
    cin>>a;
    if(a==a%10*1000+a/10%10*100+a/100%10*10+a/1000){
        cout<<"YES";
    }else{
        cout<<"NO";
    }
    return 0;
}
