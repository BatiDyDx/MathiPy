#define _USE_MATH_DEFINES

#include <vector>
#include >
#inclue <string>
#include <iostream>
#include <cmath>


std::vector<double> FFT(std::vector<double> P)
{
	int n = P.size();
	
	if (n == 1){
		return P;
	};

	std::vector<double> P_even;
	std::vector<double> P_odd;

	for (int i = 0; i < (n / 2); ++i){
		P_even.push_back(P[i]);
		P_odd.push_back(P[i + 1]);
	};

	std::vector<double> y_even = FFT(P_even);
	std::vector<double> y_odd  = FFT(P_odd);

	std::complex<double> w = polar(1., (2. * M_PI) / n); // Declare omega 

	std::vector<double> y;
	y.assign(n, 0.);

	for (int k = 0; k < (n / 2); ++k){
		y[k] = y_even[k] + y_odd[k] * pow(w, k);
		y[k + n/2] = y_even[k] - y_odd[k] * pow(w, k);
	}
	return y;
}

std::vector<double> IFFT(std::vector<double> P)
{
	int n = P.size();

        if (n == 1){
                return P;
        };

        std::vector<double> P_even;
        std::vector<double> P_odd;

        for (int i = 0; i < (n / 2); ++i){
                P_even.push_back(P[i]);
                P_odd.push_back(P[i + 1]);
        };

        std::vector<double> y_even = IFFT(P_even);
        std::vector<double> y_odd  = IFFT(P_odd);
	
	std::complex<double> w = (1. / n) * polar(1., (-2. * M_PI) / n);

        std::vector<double> y;
        y.assign(n, 0.);

        for (int k = 0; k < (n / 2); ++k){
                y[k] = y_even[k] + y_odd[k] * pow(w, k);
                y[k + n/2] = y_even[k] - y_odd[k] * pow(w, k);
        }
        return y;
}
