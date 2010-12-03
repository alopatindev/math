#include <iostream>
#include <cmath>

using namespace std;

void input(double & a, double & b, double & eps, int & n)
{
    cout << "Input a = "; cin >> a;
    cout << "Input b = "; cin >> b;
    cout << "Input eps = "; cin >> eps;
    cout << "Input n = "; cin >> n;
}

void print(const char *method, const double & s, int n, const double & eps)
{
    cout << method
         << "s = " << s
         << ", n = " << n
         << ", eps = " << eps
         << endl;
}

double f(const double & x)
{
    return 10*x - 2*x*x;
}

void trapeze(const double & a, const double & b, int n, const double & eps)
{
    double h, x, s = 0, s_old;
    bool done;

    do {
        done = true;
        h = (b - a) / n;
        s_old = s;

        s = 0;
        for (x = a; x < b; x += h)
            s += (f(x+h) + f(x)) / 2*h;

        if (abs(s_old - s) > eps) {
            done = false;
            n *= 2;
        }
    } while (!done);

    print("Trapeze method: ", s, n, eps);
}

double ff(int i, const double & a, const double & h)
{
    return f(a + h*i/2);
}

void simpson(const double & a, const double & b, int n, const double & eps)
{
    double h, s = 0, s_old, s1, s2;
    int i; bool done;

    do {
        h = (b - a) / n;
        done = true;
        s_old = s;

        s1 = 0;
        for (i = 2; i < 2*n-1; i += 2)
            s1 += ff(i, a, h);

        s2 = 0;
        for (i = 1; i < 2*n; i += 2)
            s2 += ff(i, a, h);

        s = h/6 * (ff(0, a, h) + 2*s1 + 4*s2 + ff(2*n, a, h));

        if (abs(s_old - s) > eps*h*n / (b - a)) {
            done = false;
            n *= 2;
        }
    } while (!done);

    print("Simpson's method: ", s, n, eps);
}

int main()
{
    double a, b, eps; int n;
    input(a, b, eps, n);
    trapeze(a, b, n, eps);
    simpson(a, b, n, eps);
    return 0;
}
