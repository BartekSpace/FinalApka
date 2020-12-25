from nitrous import *
from Side_Functions import*
import sys

class Hybrid:
    def __init__(self, initial_oxid_temp, tank_volume, oxid_mass, orfice_diam, inj_k_loss, orfice_nums, tank_pressure, initial_chamber_pressure):
        self.hybrid_fault = 0
        self.tank_vapour_mass = 0
        self.tank_fluid_temperature_K = 0
        self.initial_tank_pressure = tank_pressure
        self.initial_fluid_propellant_temp = initial_oxid_temp
        self.tank_liquid_density = 0
        self.tank_liquid_volume = 0
        self.tank_vapour_density = 0
        self.tank_vapour_volume = 0
        self.tank_liquid_mass = 0
        self.tank_volume = tank_volume
        self.tank_propellant_contents_mass = oxid_mass
        self.orifice_diameter = orfice_diam
        self.initial_liquid_propellant_mass = 0
        self.initial_vapour_propellant_mass = 0
        #self.injector_loss_coefficient = inj_k_loss
        self.orifice_k2_coefficient = inj_k_loss
        self.orifice_number = orfice_nums
        self.tank_pressure_bar = tank_pressure
        self.chamber_pressure_bar = initial_chamber_pressure

        self.mdot_tank_outflow = 0
        self.old_liquid_nox_mass = 0
        self.old_vapour_nox_mass = 0
        self.vaporised_mass_old = 0
        self.lagged_bob = 0
        self.Omdot_tank_outflow = 0
        self.first_iteration_flag=True
        self.first_pressure_flag = 0
        self.Gox = 0
        self.Reg = 0
        self.Fuel_outflow =0
        self.Radius = 0
        self.a_coeff =0
        self.n_coeff =0
        self.Length_fuel=0
        self.Dens_fuel=0
        self.Isp = 0
        self.c_star =0

        #self.Old_c_star=0
        self.OF = 0
        self.Oxid_name =""
        self.Fuel_name = ""
        self.Exit_nozzle_diam=0
        self.Throat_nozzle_diam =0
        self.Thrust = 0
        self.Real_coeff=0
        self.old_pressure_chamber = 0
        self.very_old_pressure_chamber =0

    def initialise_hybrid_engine(self):
        self.hybrid_fault = 0
        self.tank_vapour_mass = 0.0
        self.mdot_tank_outflow = 0.0


        #self.tank_fluid_temperature_K = self.initial_fluid_propellant_temp + 273.15
        self.tank_fluid_temperature_K = nox_on_press(
            self.initial_tank_pressure)
        if self.tank_fluid_temperature_K > 36 + 273.15:
            self.tank_fluid_temperature_K = 36 + 273.15
            self.hybrid_fault = 2

        self.tank_liquid_density = nox_Lrho(self.tank_fluid_temperature_K)

        self.tank_vapour_density = nox_Vrho(self.tank_fluid_temperature_K)

        # self.tank_liquid_mass = liquid_phase(
        # self.tank_volume, self.tank_pressure_bar, self.tank_propellant_contents_mass)

        self.tank_liquid_mass = ((self.tank_volume-self.tank_propellant_contents_mass /
                                  self.tank_vapour_density)/(1/self.tank_liquid_density-1/self.tank_vapour_density))

        self.tank_liquid_volume = self.tank_liquid_mass/self.tank_liquid_density
        self.tank_vapour_mass = self.tank_propellant_contents_mass - self.tank_liquid_mass
        self.tank_vapour_volume = self.tank_vapour_mass/self.tank_vapour_density

        self.old_liquid_nox_mass = self.tank_liquid_mass
        self.old_vapour_nox_mass = self.tank_vapour_mass
        self.initial_liquid_propellant_mass = self.tank_liquid_mass
        self.initial_vapour_propellant_mass = self.tank_vapour_mass
        self.vaporised_mass_old = 0.001
        bob = 3.14*((self.orifice_diameter / 2.0)**2)
        self.injector_loss_coefficient = (
            self.orifice_k2_coefficient / (((self.orifice_number * bob)**2))) * 1e-5

        self.old_liquid_nox_mass = self.tank_liquid_mass
        self.old_vapour_nox_mass = self.tank_vapour_mass
        self.initial_liquid_propellant_mass = self.tank_liquid_mass
        self.initial_vapour_propellant_mass = self.tank_vapour_mass

    def injector_model(self, upstream_pressure, downstream_pressure):
        pressure_drop = upstream_pressure-downstream_pressure
        if pressure_drop < 0.00001:
            pressure_drop = 0.00001
        if pressure_drop/self.chamber_pressure_bar < 0.2:
            self.hybrid_fault = 3
            #print("Too low pressure drop")
            sys.stderr.write("To low pressure drop\n")
        mass_flowrate = ((2.0 * self.tank_liquid_density *
                          pressure_drop / self.injector_loss_coefficient))**0.5
        return mass_flowrate


class HybridVapour:
    def __init__(self, vap_temp, vap_mass, vap_dens, tank_press, chamber_press, inj_loss_coef, mdot_tank_outflow, old_mdot_tank_outflow, tank_contents_mass, fault):
        self.vapour_temperature_K = vap_temp
        self.vapour_mass = vap_mass
        self.vapour_density = vap_dens
        self.tank_pressure_bar = tank_press
        self.chamber_pressure_bar = chamber_press
        self.injector_loss_coefficient = inj_loss_coef
        self.mdot_tank_outflow = mdot_tank_outflow
        self.old_mdot_tank_outflow = old_mdot_tank_outflow
        self.tank_contents_mass = tank_contents_mass
        self.fault = fault
        self.first_flag = True

        self.initial_vapour_density = 0
        self.initial_vapour_mass = 0
        self.initial_vapour_pressure_bar = 0
        self.initial_vapour_temp_K = 0
        self.initial_Z = 0
        self.erlier = 100000
        self.old_pressure_chamber=0
        self.very_old_pressure_chamber = 0

    def __eq__(self, hybrid):
        self.Gox = hybrid.Gox
        self.Reg = hybrid.Reg
        self.Fuel_outflow = hybrid.Fuel_outflow
        self.Radius = hybrid.Radius
        self.a_coeff = hybrid.a_coeff
        self.n_coeff = hybrid.n_coeff
        self.Length_fuel = hybrid.Length_fuel
        self.Dens_fuel = hybrid.Dens_fuel
        self.Isp = hybrid.Isp
        self.c_star = hybrid.c_star
        #self.Old_c_star = 0
        self.OF = hybrid.OF
        self.Oxid_name = hybrid.Oxid_name
        self.Fuel_name = hybrid.Fuel_name
        self.Exit_nozzle_diam = hybrid.Exit_nozzle_diam
        self.Throat_nozzle_diam = hybrid.Throat_nozzle_diam
        self.Thrust = hybrid.Thrust
        self.Real_coeff = hybrid.Real_coeff


    def vapour_init(self):
        self.initial_vapour_temp_K = self.vapour_temperature_K
        self.initial_vapour_mass = self.vapour_mass
        self.initial_vapour_pressure_bar = self.tank_pressure_bar
        self.initial_vapour_density = self.vapour_density
        self.initial_Z = compressibility_factor(
            self.initial_vapour_pressure_bar, pCrit, ZCrit)
        self.old_mdot_tank_outflow = 0

    def injector_model(self):
        pressure_drop = self.tank_pressure_bar - self.chamber_pressure_bar
        if pressure_drop < 0.00001:
            pressure_drop = 0.00001
            sys.stderr.write("To low pressure drop\n")
        mass_flowrate = (2.0 * self.vapour_density *
                         pressure_drop / self.injector_loss_coefficient)**0.5
        return mass_flowrate


def liquid_phase(vessel_volume, pressure, total_mass):
    T = nox_on_press(pressure)
    return (vessel_volume - total_mass / nox_Vrho(T)) / (1 / nox_Lrho(T) - 1 / nox_Vrho(T))


def fuel_flow(liquid_flow, radius, a_coeff=0.00772597539149796, n_coeff=0.777265794840152, length=1, dens=1130, delta_t=0.01):

    radius = radius/1000
    Gox = liquid_flow/(radius*radius*3.14)
    reg = a_coeff*pow(Gox, n_coeff)/1000
    radius = radius + reg * delta_t

    return (2*3.14*radius*length/1000*dens*reg, Gox, radius*1000, reg)


# def initialise_hybrid_engine(hybrid):
#     hybrid.hybrid_fault = 0
#     hybrid.tank_vapour_mass = 0.0
#     hybrid.mdot_tank_outflow = 0.0

#     #hybrid.tank_fluid_temperature_K = hybrid.initial_fluid_propellant_temp + 273.15
#     hybrid.tank_fluid_temperature_K = nox_on_press(
#         hybrid.initial_tank_pressure)
#     if hybrid.tank_fluid_temperature_K > 36 + 273.15:
#         hybrid.tank_fluid_temperature_K = 36 + 273.15
#         hybrid.hybrid_fault = 2
#     hybrid.tank_liquid_density = nox_Lrho(hybrid.tank_fluid_temperature_K)
#     hybrid.tank_vapour_density = nox_Vrho(hybrid.tank_fluid_temperature_K)
#     hybrid.tank_liquid_mass = liquid_phase(
#         hybrid.tank_volume, hybrid.tank_pressure_bar, hybrid.tank_propellant_contents_mass)
#     hybrid.tank_liquid_volume = hybrid.tank_liquid_mass/hybrid.tank_liquid_density
#     hybrid.tank_vapour_mass = hybrid.tank_propellant_contents_mass = hybrid.tank_liquid_mass
#     hybrid.tank_vapour_volume = hybrid.tank_vapour_mass/hybrid.tank_vapour_density

#     hybrid.old_liquid_nox_mass = hybrid.tank_liquid_mass
#     hybrid.old_vapour_nox_mass = hybrid.tank_vapour_mass
#     hybrid.initial_liquid_propellant_mass = hybrid.tank_liquid_mass
#     hybrid.initial_vapour_propellant_mass = hybrid.tank_vapour_mass
#     hybrid.vaporised_mass_old = 0.001
#     bob = 3.14*(((hybrid.orifice_diameter / 2.0))**0.5)
#     hybrid.injector_loss_coefficient = (
#         hybrid.orifice_k2_coefficient / (0.5**((hybrid.orifice_number * bob)))) * 1e-5

#     hybrid.old_liquid_nox_mass = hybrid.tank_liquid_mass
#     hybrid.old_vapour_nox_mass = hybrid.tank_vapour_mass
#     hybrid.initial_liquid_propellant_mass = hybrid.tank_liquid_mass
#     hybrid.initial_vapour_propellant_mass = hybrid.tank_vapour_mass
