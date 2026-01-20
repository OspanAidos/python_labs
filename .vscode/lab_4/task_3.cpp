#include <iostream>
#include <string>
#include <cmath>
using namespace std;
int main(){
    int a;
    cin>>a;
    long long arr[a];
    for(int i = 0; i<a; i++){
        cin>>arr[i];
    }
     long long max = arr[0];
    for(int i = 0; i<a; i++){
        if (arr[i]>max){
            max = arr[i];
        }
    }
    cout<<max;
    return 0;
}