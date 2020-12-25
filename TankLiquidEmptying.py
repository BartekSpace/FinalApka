from Hybrid import *
from nitrous import *
from Side_Functions import fuel_flow
from Cea import *

delta_time = 0.01


def Nitrous_tank_liquid(hybrid):
    hybrid.Omdot_tank_outflow = hybrid.mdot_tank_outflow
    Enth_of_vap = nox_enthV(hybrid.tank_fluid_temperature_K)
    Spec_heat_cap = nox_Cpl(hybrid.tank_fluid_temperature_K)
    deltaQ = hybrid.vaporised_mass_old * Enth_of_vap
    deltaTemp = -(deltaQ / (hybrid.tank_liquid_mass * Spec_heat_cap))
    hybrid.tank_fluid_temperature_K += deltaTemp
    if hybrid.tank_fluid_temperature_K < (-90.0 + 273.15):
        hybrid.tank_fluid_temperature_K = -90.0 + 273.15
        hybrid.hybrid_fault = 1

    elif hybrid.tank_fluid_temperature_K > (36.0 + 273.15):

        hybrid.tank_fluid_temperature_K = (36.0 + 273.15)
        hybrid.hybrid_fault = 2

    hybrid.tank_liquid_density = nox_Lrho(hybrid.tank_fluid_temperature_K)
    hybrid.tank_vapour_density = nox_Vrho(hybrid.tank_fluid_temperature_K)
    hybrid.tank_pressure_bar = nox_vp(hybrid.tank_fluid_temperature_K)
    Chamber_press_bar_abs = hybrid.chamber_pressure_bar

    hybrid.mdot_tank_outflow = hybrid.injector_model(
        hybrid.tank_pressure_bar, Chamber_press_bar_abs)
    delta_outflow_mass = 0.5 * delta_time * \
        (3.0 * hybrid.mdot_tank_outflow - hybrid.Omdot_tank_outflow)
    hybrid.tank_propellant_contents_mass -= delta_outflow_mass

    hybrid.old_liquid_nox_mass -= delta_outflow_mass
    bob = (1.0 / hybrid.tank_liquid_density) - \
        (1.0 / hybrid.tank_vapour_density)
    hybrid.tank_liquid_mass = (
        hybrid.tank_volume - (hybrid.tank_propellant_contents_mass / hybrid.tank_vapour_density)) / bob
    hybrid.tank_vapour_mass = hybrid.tank_propellant_contents_mass - hybrid.tank_liquid_mass

    bob = hybrid.old_liquid_nox_mass - hybrid.tank_liquid_mass
    tc = delta_time / 0.15
    hybrid.lagged_bob = tc * (bob - hybrid.lagged_bob) + hybrid.lagged_bob
    hybrid.vaporised_mass_old = hybrid.lagged_bob
    if hybrid.tank_liquid_mass > hybrid.old_liquid_nox_mass:
        hybrid.hybrid_fault = 9
    hybrid.old_liquid_nox_mass = hybrid.tank_liquid_mass
    return hybrid


def subcritical_tank_no_liquid(hybrid):
    # calculate injector pressure drop and mass flowrate
    hybrid.erlier = hybrid.mdot_tank_outflow
    if hybrid.first_flag == False:
        hybrid.old_mdot_tank_outflow = hybrid.erlier

    hybrid.mdot_tank_outflow = hybrid.injector_model()
    hybrid.first_flag = False

    # /* integrate mass flowrate using Addams second order integration formula */
    # /* Xn=X(n-1) + DT/2 * ((3 * Xdot(n-1) - Xdot(n-2))
    # */
    delta_outflow_mass = 0.5 * delta_time * \
        (3.0 * hybrid.mdot_tank_outflow - hybrid.old_mdot_tank_outflow)
    # drain the tank based on flowrates only
    hybrid.tank_contents_mass -= delta_outflow_mass
    hybrid.vapour_mass -= delta_outflow_mass
    current_Z_guess = compressibility_factor(
        hybrid.tank_pressure_bar, pCrit, ZCrit)
    step = 1.0/0.9
    OldAim = 2
    Aim = 0
    do_while_flag = True
    current_Z = 1000
    while (((current_Z_guess / current_Z) > 1.000001) or ((current_Z_guess / current_Z) < (1.0 / 1.000001))) or do_while_flag:
        do_while_flag = False
        bob = Gamma - 1
        hybrid.vapour_temperature_K = hybrid.initial_vapour_temp_K * \
            pow(((hybrid.vapour_mass * current_Z_guess) /
                 (hybrid.initial_vapour_mass * hybrid.initial_Z)), bob)
        bob = Gamma/(Gamma - 1.0)
        hybrid.tank_pressure_bar = hybrid.initial_vapour_pressure_bar * \
            pow((hybrid.vapour_temperature_K / hybrid.initial_vapour_temp_K), bob)
        current_Z = compressibility_factor(
            hybrid.tank_pressure_bar, pCrit, ZCrit)
        OldAim = Aim
        if current_Z_guess < current_Z:
            current_Z_guess *= step
            Aim = 1
        else:
            current_Z_guess /= step
            Aim = -1

        if Aim == -OldAim:
            step = step**0.5
    bob = 1/(Gamma-1)
    hybrid.vapour_density = hybrid.initial_vapour_density * \
        pow(hybrid.vapour_temperature_K/hybrid.initial_vapour_temp_K, bob)
    return hybrid

def simmulate_regression(hybrid):
    mf, Gox, radius, reg =fuel_flow(hybrid.mdot_tank_outflow,hybrid.Radius,hybrid.a_coeff,hybrid.n_coeff,hybrid.Length_fuel,hybrid.Dens_fuel,0.01)
    hybrid.Fuel_outflow = mf
    hybrid.Gox = Gox
    hybrid.Radius = radius
    hybrid.Reg = reg
    hybrid.OF = hybrid.mdot_tank_outflow/mf
    return hybrid

def simmulate_engine_efficience(hybrid):
    hybrid.Isp = get_Isp(hybrid.Oxid_name,hybrid.Fuel_name,hybrid.chamber_pressure_bar,hybrid.OF,(hybrid.Exit_nozzle_diam/hybrid.Throat_nozzle_diam)**2)


    #hybrid.Old_c_star = hybrid.c_star

    # hybrid.c_star = (hybrid.chamber_pressure_bar * 100000 * pow(hybrid.Throat_nozzle_diam / 1000, 2) * 3.14 / 4 / (
    #             hybrid.mdot_tank_outflow + hybrid.Fuel_outflow))
    #hybrid.old_cstar = hybrid.c_star
    hybrid.c_star = get_c_star(hybrid.Oxid_name,hybrid.Fuel_name,hybrid.chamber_pressure_bar,hybrid.OF)
    At = pow(hybrid.Throat_nozzle_diam / 1000, 2) * 3.14 / 4
    hybrid.chamber_pressure_bar = (hybrid.c_star * (hybrid.Fuel_outflow + hybrid.mdot_tank_outflow) / At / 100000)

    hybrid.chamber_pressure_bar = hybrid.chamber_pressure_bar*hybrid.Real_coeff ## sprawdzic
    # if hybrid.first_pressure_flag==0:
    #     hybrid.old_pressure_chamber = hybrid.chamber_pressure_bar
    #     hybrid.chamber_pressure_bar = (hybrid.c_star * (hybrid.Fuel_outflow + hybrid.mdot_tank_outflow) / At / 100000)
    #     hybrid.chamber_pressure_bar = hybrid.chamber_pressure_bar*hybrid.Real_coeff ## sprawdzic
    #     hybrid.first_pressure_flag=1
    # elif hybrid.first_pressure_flag == 1:
    #     hybrid.very_old_pressure_chamber = hybrid.old_pressure_chamber
    #     hybrid.old_pressure_chamber = hybrid.chamber_pressure_bar
    #     hybrid.chamber_pressure_bar = 2*hybrid.old_pressure_chamber-hybrid.very_old_pressure_chamber
    #     hybrid.first_pressure_flag =2
    # elif hybrid.first_pressure_flag >=2:
    #     hybrid.very_old_pressure_chamber = hybrid.old_pressure_chamber
    #     hybrid.old_pressure_chamber = hybrid.chamber_pressure_bar
    #     hybrid.chamber_pressure_bar=2.5*hybrid.chamber_pressure_bar-2*hybrid.old_pressure_chamber+0.5*hybrid.very_old_pressure_chamber
    #     hybrid.first_pressure_flag +=1

    #delta_pc = 0.5*delta_time*(3*hybrid.chamber_pressure_bar - hybrid.old_pressure_chamber)
    #hybrid.chamber_pressure_bar-=delta_pc

    #hybrid.chamber_pressure_bar = hybrid.chamber_pressure_bar*hybrid.Real_coeff ## sprawdzic

    # /* integrate mass flowrate using Addams second order integration formula */
    # /* Xn=X(n-1) + DT/2 * ((3 * Xdot(n-1) - Xdot(n-2))
    # */
    #delta_outflow_mass = 0.5 * delta_time * \
    #                     (3.0 * hybrid.mdot_tank_outflow - hybrid.old_mdot_tank_outflow)


    # if hybrid.first_iteration_flag == True:
    #     hybrid.Old_c_star=hybrid.c_star
    #
    # if hybrid.first_iteration_flag == False:
    #     At = pow(hybrid.Throat_nozzle_diam / 1000, 2) * 3.14 / 4
    #     hybrid.chamber_pressure_bar = (hybrid.Old_c_star * (hybrid.Fuel_outflow + hybrid.mdot_tank_outflow) / At / 100000)
    #hybrid.chamber_pressure_bar = hybrid.tank_pressure_bar/(1+0.2*(hybrid.Throat_nozzle_diam/1000/2/hybrid.Radius/1000)**4)



    hybrid.first_iteration_flag=False
    hybrid.Thrust =(hybrid.Isp * (hybrid.mdot_tank_outflow+hybrid.Fuel_outflow)*9.81*hybrid.Real_coeff)


    return hybrid

def init_engine_properties(hybrid,cea):

    for key in cea:
        if key == 'oxid_name':
            break
        cea[key]=float(cea[key])
    #cea['oxid_temp']= float( cea['oxid_temp'])
    #cea['fuel_temp'] = float(cea['fuel_temp'])
    #cea['fuel_enthalpy'] = float(cea['fuel_enthalpy'])
    #cea['oxid_enthalpy'] = float(cea['oxid_enthalpy'])

    add_fuel(cea['fuel_name'],cea['fuel_formula'],cea['fuel_temp'],cea['fuel_enthalpy'])
    add_oxid(cea['oxid_name'],cea['oxid_formula'],cea['oxid_temp'],cea['oxid_enthalpy'])
    #
    #
    hybrid.a_coeff = cea['a_ballistic']
    hybrid.n_coeff = cea['n_ballistic']
    hybrid.Length_fuel = cea['fuel_length']
    hybrid.Dens_fuel = cea['fuel_dens']
    hybrid.Oxid_name = cea['oxid_name']
    hybrid.Fuel_name = cea['fuel_name']
    hybrid.Exit_nozzle_diam = cea['nozzle_exit']
    hybrid.Throat_nozzle_diam = cea['throat_diam']
    hybrid.Real_coeff = cea['chuj_coeff']
    hybrid.Radius = cea['port_diam']/2
    return hybrid

def prepare_data_lists (OF, Pressure_Chamber, Pressure_Vessel, Thrust, Isp, Fuel_Flow, Oxid_Flow, Time, Radius,hybrid):
    OF.append(hybrid.OF)
    Pressure_Chamber.append(hybrid.chamber_pressure_bar)
    Pressure_Vessel.append(hybrid.tank_pressure_bar)
    Thrust.append(hybrid.Thrust)
    Isp.append(hybrid.Isp)
    Fuel_Flow.append(hybrid.Fuel_outflow)
    Oxid_Flow.append(hybrid.mdot_tank_outflow)
    Time.append(Time[-1]+0.01)
    Radius.append(hybrid.Radius)