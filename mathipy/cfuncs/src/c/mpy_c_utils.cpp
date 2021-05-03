#include <math.h>

extern "C" {

  int factorial(int n)
  {
    if(n == 0 || n == 1)
    {
      return 1;
    }
    else
    {
      return factorial(n - 1) * n;
    }
  };

  int gcd(int a, int b)
  {
    int r = a % b; // r is equal to the remainder of a and b

    if(r == 0){
      return b;
    }else{
      return gcd(b, r);
    }
  };

  int lcm(int a, int b)
  {
    int mul = gcd(a, b);
    return (a * b) / mul;
  };

  int variation(int n, int k, bool repetitions)
  {
    if (repetitions == true)
    {
      return pow(n, k);
    }else{
      return factorial(n) / factorial(n - k);
    }
  };

  int permutation(int n, int k, bool circular)
  {
    if (k == 0)
    {
      if (circular == true)
      {
        return factorial(n - 1);
      }
      else
      {
        return factorial(n);
      }
    }
    else
    {
      int denominator = 1;
      for(int i = 0; i < k; i++)
      {
        denominator *= factorial(i);
      }
      return factorial(n) / denominator;
    }
  };

  int combinatorial(int n, int k, bool repetitions)
  {
    if (repetitions == false)
    {
      int num = factorial(n);
      int den = factorial(k) * factorial(n - k);
      return num / den;
    }
    else
    {
      return combinatorial(n + k - 1, k, false);
    }
  };
}