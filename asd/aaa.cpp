#include <iostream>
#include <algorithm>
#include <string>
#include <cmath>
#include <iomanip>
#include <vector>
using namespace std;
int main(){
    string a;
    string s;
    string t;
    int n=0;
    vector<string> v;
    cin>>a;
    cin.ignore();
    getline(cin, s);
    for(int i = 0; i<s.size(); i++){
        if(s[i]!=' '){
            t+=s[i];
        }else{
            if(!t.empty()){
                v.push_back(t);
                t="";
            }
        }
    }
    if(!t.empty()){
            v.push_back(t);
        }
    for(int i = 0; i<v.size(); i++){
        if(a==v[i]){
            n++;
        }
    }
    cout<<n;
}