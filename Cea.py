from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import  add_new_fuel, add_new_oxidizer, add_new_propellant


# print(rr)


def add_oxid(name, formula, temperature, enthalpy):
    string = """
    oxid """ + name + """ """ + formula + """  wt%=100.00
    h,kJ/mol="""+enthalpy+"""   t(k)=""" + temperature
    add_new_oxidizer(name,string)


#add_oxid('N2O1','N 2.0 O 1.0','298.15','75.24')


def add_fuel(name,formula,temperature,enthalpy):
    string = """
    fuel """ + name + """ """ + formula + """  wt%=100.00
    h,kJ/mol="""+enthalpy+"""     t(k)=""" + temperature
    add_new_fuel(name,string)


#add_fuel('Nylon','C 6.0   H 11.0   O 1.0  N 1.0','298.15','67.69')


def get_Isp(oxid_name, fuel_name, chamber_pressure, OF, eps_nozzle):
    C = CEA_Obj(oxName=oxid_name, fuelName=fuel_name, pressure_units='Bar', cstar_units='m/s')
    x=C.estimate_Ambient_Isp(Pc=chamber_pressure,MR=OF,eps=eps_nozzle,Pamb=1)
    return x[0]

def get_c_star(oxid_name, fuel_name, chamber_pressure, OF):
    C = CEA_Obj(oxName=oxid_name, fuelName=fuel_name, pressure_units='Bar', cstar_units='m/s')
    x=C.get_Cstar(Pc=chamber_pressure, MR=OF)
    return x
