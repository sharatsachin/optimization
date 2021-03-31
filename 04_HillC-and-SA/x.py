def objective(X, func_no):
    if func_no == 1:
        return 10 * -cos(2 * (x ^ 2+y ^ 2) ^ 0.5) * exp(-0.5 * ((x+1) ^ 2+(y-1) ^ 2) ^ 0.5) + 5.1
    if func_no == 2:
        return -1*(0.2 + x^2 + y^2 - 0.1*cos(6*pi*x) - 0.1*cos(6*pi*y) )
    if func_no == 3:
        return -1 * (x^2 + y^2)