// https://github.com/stevengj/nlopt/blob/master/src/util/sobolseq.c

using namespace std;
typedef unsigned int unit;

static unsigned int a = 0x05f66a47;
byte decode[] = { 0, 1, 2, 26, 23, 3, 15, 27, 24, 21, 19, 4, 12, 16, 28, 6, 31, 25, 22, 14, 20, 18, 11, 5, 30, 13, 17, 10, 29, 9, 8, 7 };
static unit handle = 0xffffffff;
uint one(uint n)
{
    unsigned int tmp = a * (unsigned int)((int)n & (-(int)n));
    cout << hex << ((unsigned int)((int)n & (-(int)n))) <<endl;
    auto result = decode[tmp >> 27];
    
    return result;
}

void test()
{
  // 每次转换handle的一位为0，直至32位全部为0，代表cache用完
  int i = 32;
  while(i-- > 0)
  {
    auto result = one(handle);
    cout << result << endl;
    handle &= (unit)~(1 << result);
  }
}
