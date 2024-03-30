#include<iostream>
using namespace std;
 class complex{
    int x;
    int y;
    public:

    complex(int a,int b)
    {
        x=a;
        y=b;
    }
    void print(void)
    {
        cout<<x<<" "<<y;
    }

    //
    complex operator +(complex);
 };
// return type  class name :: operator...
 complex complex :: operator +(complex c)
 {
    complex temp(0,0);
  temp.x = x + c.x;
    temp.y  = y + c.y;
    return temp;

 }

int main()
{
    complex c1(1,2);
    complex c2(3,4);
    
complex c3(0,0);
c3=c1+c2;
c3.print();
    
    return 0 ;
}