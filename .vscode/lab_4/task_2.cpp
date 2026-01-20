#include <iostream>
#include <string>
#include <cmath>
using namespace std;
int main(){
    int a;
    cin>>a;
    int arr[a];
    for(int i = 0; i<a; i++){
        cin>>arr[i];
    }
    for(int i = 0; i<a; i++){
        if (arr[i]%2==1){
            cout<<arr[i]<<" ";
        }
    }
    return 0;
}