#include <iostream>
#include <cmath>

using namespace std;

const double FI = 1.6180339887;  // (sqrt(5) + 1) / 2

void input(double & a, double & b, double & eps, int & n,
           int & func, bool & maxima)
{
    cout << "Input a = "; cin >> a;
    cout << "Input b = "; cin >> b;
    cout << "Input eps = "; cin >> eps;
    cout << "Input n = "; cin >> n;
    cout << "Function (0: y=10x+2x^2, 1: y=10x-2x^2) = "; cin >> func;
    cout << "Extremum type (0: minima, 1: maxima) = "; cin >> maxima;
}

void print(const char *method, const double & xopt, const double & y,
           const double & eps, int i)
{
    cout << method
         << "xopt = " << xopt
         << ", f(xopt) = " << y
         << ", eps = " << eps
         << ", i = " << i
         << endl;
}

double f(const double & x, int func)
{
    switch (func) {
        case 0:
            return 10*x + 2*x*x;
        case 1:
            return 10*x - 2*x*x;
    }
}

void bitwise_approx(double a, double b, const double & eps,
                    int n, int c, int func)
{
    double h = (b - a) / n, x1 = a, x2, f1, f2;
    int i = 0;

    do {
        f1 = f(x1, func);
        x2 = x1 + h;
        f2 = f(x2, func);
        if (f1*c < f2*c) {
            x1 += h;
            if (x1 > b) {
                cout << "There is no extrema" << endl;
                return;
            }
        } else {
            a = x2 - 2*h;
            b = x2;
            h /= n;
            x1 = a;
        }
        ++i;
    } while (abs(f1 - f2) > eps);

    double xopt = (a + b) / 2;
    print("Bitwise approximation: ", xopt, f(xopt, func), eps, i);
}

void golden_section(double a, double b, const double & eps, int c, int func)
{
    double x1, x2, f1, f2;
    int i = 0;

    x1 = b - (b - a) / FI;
    x2 = a + (b - a) / FI;
    f1 = f(x1, func); f2 = f(x2, func);
    do {
        if (f1*c > f2*c) {
            b = x2;
            x2 = x1;
            x1 = b - (b - a) / FI;
            f2 = f1;
            f1 = f(x1, func);
        } else {
            a = x1;
            x1 = x2;
            x2 = a + (b - a) / FI;
            f1 = f2;
            f2 = f(x2, func);
        }
        ++i;
    } while (abs(b - a) > eps);

    double xopt = (a + b) / 2;
    print("Golden section method: ", xopt, f(xopt, func), eps, i);
}

int main()
{
    double a, b, eps; int n, func; bool maxima;
    input(a, b, eps, n, func, maxima);
    int c = maxima ? 1 : -1;
    bitwise_approx(a, b, eps, n, c, func);
    golden_section(a, b, eps, c, func);
    return 0;
}
