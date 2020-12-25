from numpy import sign
import math
pCrit = 72.51
rhoCrit = 452.0
tCrit = 309.57
ZCrit = 0.28
Gamma = 1.3


def nox_vp(T_Kelvin):
    # return -255.024059969015 + 3.65374953721262 * T - 0.0181854641613239 * T * T + 3.16518936143792e-05 * T * T * T
    p = (1.0, 1.5, 2.5, 5.0)
    b = (-6.71893, 1.35966, -1.3779, -4.051)
    Tr = T_Kelvin / tCrit
    rab = 1.0 - Tr
    shona = 0.0
    for dd in range(0, 4):
        shona += b[dd] * pow(rab, p[dd])
    bob = pCrit * 2.7182818**((shona / Tr))
    return bob


def nox_Vrho(T_Kelvin):
    b = (-1.009, -6.28792, 7.50332, -7.90463, 0.629427)
    Tr = T_Kelvin / tCrit
    rab = (1.0 / Tr) - 1.0
    shona = 0.0
    for dd in range(0, 5):
        shona += b[dd] * pow(rab, ((dd + 1) / 3.0))
    bob = rhoCrit * 2.7182818**shona
    return bob


def nox_Lrho(T_Kelvin):
    b = (1.72328, -0.8395, 0.5106, -0.10412)
    Tr = T_Kelvin / tCrit
    rab = 1.0 - Tr
    shona = 0.0
    for dd in range(0, 4):
        shona += b[dd] * pow(rab, ((dd + 1) / 3.0))
    bob = rhoCrit * 2.7182818**shona
    return bob


def nox_enthV(T_Kelvin):
    bL = (-200.0, 116.043, -917.225, 794.779, -589.587)
    bV = (-200.0, 440.055, -459.701, 434.081, -485.338)
    Tr = T_Kelvin / tCrit
    rab = 1.0 - Tr
    shonaL = bL[0]
    shonaV = bV[0]
    for dd in range(1, 5):
        shonaL += bL[dd] * pow(rab, (dd / 3.0))
        shonaV += bV[dd] * pow(rab, (dd / 3.0))
    bob = (shonaV - shonaL) * 1000.0
    return(bob)


def nox_Cpl(T_Kelvin):
    b = (2.49973, 0.023454, -3.80136, 13.0945, -14.518)
    Tr = T_Kelvin / tCrit
    rab = 1.0 - Tr
    shona = 1.0 + b[1] / rab
    for dd in range(1, 4):
        shona += b[(dd + 1)] * pow(rab, dd)
    bob = b[0] * shona * 1000.0
    return(bob)


def nox_on_press(P_Bar_abs):
    p = (1.0, 1.5, 2.5, 5.0)
    b = (-6.71893, 1.35966, -1.3779, -4.051)
    pp_guess = 0
    flag1 = True
    flag2 = True
    step = -1.0
    tempK = (tCrit - 0.1) - step
    while (abs((pp_guess - P_Bar_abs)) > 0.01 or flag1 == True):
        flag1 = False
        while(((pp_guess - P_Bar_abs) * sign(step)) < 0.0 or flag2 == True):
            flag2 = False
            tempK += step
            Tr = tempK / tCrit
            rab = 1.0 - Tr
            shona = 0.0
            for dd in range(0, 4):
                shona += b[dd] * pow(rab, p[dd])
            pp_guess = pCrit * 2.7182818**((shona / Tr))
        step = step / (-2.0)
    bob = tempK
    return bob
