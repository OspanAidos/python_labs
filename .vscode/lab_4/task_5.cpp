#include <string>
#include <cmath>
#include <algorithm>
#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;

int main() {
    int x;
    int z;
    cin>>x>>z;
    int s = 0;
    long long v[x][z];
    long long m[z];
    for(int i = 0; i<x; i++){
        for(int j = 0; j<z; j++){
            cin>>v[i][j];
    }
}
int minv = v[0][0];
    for(int i=0; i<x; i++){
        for(int j = 0; j<z; j++){
            if(j==0 && minv>v[j][i]){
                minv=v[j][i];
            }
        }
        m[i]=minv;
        minv=v[i][0];
    }
    for(int i = 0; i<z; i++){
        s+=m[i];
    }
    cout<<s;
    for(int i = 0; i<z; i++){
        cout<<m[i];
    }
    return 0;
}