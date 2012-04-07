#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int N = 4;
const double xs[] = {10, 20, 30, 40};
const double ys[] = {10, 20, 10, 30};
int smooth = 10;

double lineral_interpolate(double y0, double y1, double mu)
{
    return y0 * (1 - mu) + y1 * mu;
}

double cos_interpolate(double y0, double y1, double mu)
{
    double mu2 = (1 - cos(mu * M_PI)) / 2;
    return y0 * (1 - mu2) + y1 * mu2;
}

double mu(double i)
{
    return i / smooth;
}

double x_dw(double x0, double x1, double smooth)
{
    return (x1 - x0) / smooth;
}

// returns interpolated dots between x[dot_i] and x[dot_i + 1]
// of double[smooth - 1]
double * interpolateX(const double xs[], int dot_i, int smooth)
{
    double *xi = (double *)malloc(sizeof(double) * (smooth - 1));
    memset(xi, 0, sizeof(double) * (smooth-1));

    int i;
    for (i = 1; i < smooth; ++i)
        xi[i - 1] = x_dw(xs[dot_i], xs[dot_i + 1], smooth) * i + xs[dot_i];

    return xi;
}

double * interpolateY(const double ys[], int dot_i, int smooth)
{
    double *yi = (double *)malloc(sizeof(double) * (smooth - 1));
    memset(yi, 0, sizeof(double) * (smooth-1));

    int i;
    for (i = 1; i < smooth; ++i)
        yi[i - 1] = cos_interpolate(ys[dot_i], ys[dot_i + 1], mu(i - 1));

    return yi;
}

int main()
{
    int dot_i;
    for (dot_i = 0; dot_i < N - 1; ++dot_i)
    {
        printf("%f %f\n", xs[dot_i], ys[dot_i]);
        double * dots_x = interpolateX(xs, dot_i, smooth);
        double * dots_y = interpolateY(ys, dot_i, smooth);
        int i;
        for (i = 0; i < smooth - 1; ++i)
            printf("%f %f\n", dots_x[i], dots_y[i]);
        free(dots_x);
        free(dots_y);
    }
    printf("%f %f\n", xs[N - 1], ys[N - 1]);
    return 0;
}
