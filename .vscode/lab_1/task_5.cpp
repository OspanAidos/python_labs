#include <iostream>
using namespace std;

int main() {
    int n;
    cin>>n;
    switch(n%2){
        case 1: cout<<"TAILS";break;
        case 0: cout<<"EAGLE";break;
    }
    return 0;
}
