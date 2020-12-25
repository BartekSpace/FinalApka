from nitrous import *


def LinearInterpolate(x, x1, y1, x2, y2):
    if ((x1 < x2) and ((x <= x1) or (x >= x2))):
        if (x <= x1):
            return y1
        else:
            return y2
    elif ((x1 > x2) and ((x >= x1) or (x <= x2))):
        if (x >= x1):
            return y1
        else:
            return y2
    else:
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        y = m * x + c
        return y


def compressibility_factor(P_Bar_abs, pCrit, ZCrit):
    return LinearInterpolate(P_Bar_abs, 0.0, 1.0, pCrit, ZCrit)


def LinearExtrapolate(x, x1, y1, x2, y2):
    a = (y1 - y2) / (x1 - x2)
    b = y1 - x1 * a
    return x * a + b


def liquid_phase(vessel_volume, pressure, total_mass):
    T = nox_on_press(pressure)
    return (vessel_volume - total_mass / nox_Vrho(T)) / (1 / nox_Lrho(T) - 1 / nox_Vrho(T))


def D_loss(K, num_holes, diam_holes):
    return (K / pow(3.14 * diam_holes * diam_holes * num_holes / 4 / 1000000, 2))


def Temperature_Iteration(T1, liquid_mass, mv):

    Hv = nox_enthV(T1)
    deltaT = -mv * Hv / liquid_mass / nox_Cpl(T1)
    return T1 + deltaT


def fuel_flow(liquid_flow, radius, a_coeff, n_coeff, length, dens, delta_t):

    radius = radius/1000
    Gox = liquid_flow/(radius*radius*3.14)
    reg = a_coeff*pow(Gox, n_coeff)/1000
    radius = radius + reg * delta_t

    return (2*3.14*radius*length/1000*dens*reg, Gox, radius*1000, reg)


def injector_model(tank_pressure_bar, chamber_pressure_bar, vapour_dens, injector_loss_coef):
    pressure_drop = tank_pressure_bar - chamber_pressure_bar
    if pressure_drop < 0.00001:
        pressure_drop = 0.00001
    mass_flowrate = (2.0 * vapour_dens * pressure_drop /
                     injector_loss_coef)**0.5
    return mass_flowrate
