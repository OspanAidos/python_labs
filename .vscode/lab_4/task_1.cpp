#include <iostream>
#include <string>
#include <cmath>
using namespace std;
int main(){
    int a;
    long long s = 0;
    cin>>a;
    int arr[a];
    for(int i = 0; i<a; i++){
        cin>>arr[i];
    }
    for(int i = 0; i<a; i++){
        s+=arr[i];
    }
    cout<<s;
    return 0;
}