#include <iostream>
#include <algorithm>
#include <cctype>
#include <string>
#include <vector>
using namespace std;
struct student{
        string name;
        float point;
    };
int main(){
    int n;
    cin>>n;
    vector<student> v(n);
    for(int i  = 0; i<n; i++){
        cin>>v[i].name>>v[i].point;
    }
    for(int i = 0; i<n; i++){
        cout<<v[i].name<<" "<<v[i].point<<endl;
    }
    return 0;
}