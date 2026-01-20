#include <iostream>
using namespace std;

int main() {
    int n;
    cin>>n;
    if(n!=0){
        if(n%2==0){
            cout<<"Even";
        }
        else{
            cout<<"Odd";
        }
    }else{
        cout<<"None";
    }
    return 0;
}
