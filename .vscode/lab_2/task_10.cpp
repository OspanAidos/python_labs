#include <iostream>
#include <cmath>
#include <string>
using namespace std;
int main(){
    string n = "";
    cin>>n;
    int t = 0;
    int z = 0;
    for(int i = 0; i<n.size();i++){
        int d = n[i] - '0';
        if(i%2==0){
            z+=d;
        }else{
            t+=d;
        }
    }
    if(t==z){
        cout<<"YES";
    }else{
        cout<<"NO";
    }
    return 0;
}