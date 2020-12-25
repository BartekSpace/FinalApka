from Hybrid import *
from TankLiquidEmptying import *
from Cea import *
from Side_Functions import *
from Gui import set_gui
from plot import *
#from rocketcea.cea_obj_w_units import CEA_Obj
#from rocketcea.cea_obj import  add_new_fuel, add_new_oxidizer, add_new_propellant

OF = []
Pressure_Chamber= []
Pressure_Vessel= []
Thrust= []
Isp= []
Fuel_Flow= []
Oxid_Flow= []
Time= [0]
Radius= []


cea, txt_flag, compare_flag = set_gui()


hybrid = Hybrid(float(cea["oxid_temp"])+273.15,float(cea["Vessel_Volume"])/1000,float( cea['oxid_mass']), float(cea['hole_diam'])/1000, float(cea['K_loss']),
                float(cea['holes_num']), float(cea['Vessel_Pressure']), float(cea['Combustion_Pressure']))

hybrid.initialise_hybrid_engine()
#add_oxid("Nitrous", "N 2.0 O 1.0", "298.15", "75.24")
#add_fuel("Nylon", "C 6.0   H 11.0   O 1.0  N 1.0", "298.15", "67.69")
hybrid = init_engine_properties(hybrid,cea)
time = 0
# erlier=0
oxid_flow =[]
while hybrid.hybrid_fault != 9 and time <= cea['time_max']:
    #print(x, " ", hybrid.mdot_tank_outflow)



    hybrid = Nitrous_tank_liquid(hybrid)
    hybrid = simmulate_regression(hybrid)
    hybrid = simmulate_engine_efficience(hybrid)
    #mf,Gox,radius,reg = fuel_flow(hybrid.mdot_tank_outflow,30,0.00772597539149796,0.777265794840152,1000,1130,0.01)
    #OF = hybrid.mdot_tank_outflow/mf
    #Isp =get_Isp("Nitrous", "Nylon", hybrid.chamber_pressure_bar,
     #        OF, pow(exit_nozzle_diam/throat_diam, 2))
    #x += 0.01
    #oxid_flow.append(hybrid.mdot_tank_outflow)
    prepare_data_lists(OF, Pressure_Chamber, Pressure_Vessel, Thrust, Isp, Fuel_Flow, Oxid_Flow, Time, Radius,hybrid)
    time+=0.01

T_vap = nox_on_press(hybrid.tank_pressure_bar)
m_vap_flow = injector_model(hybrid.tank_pressure_bar, hybrid.chamber_pressure_bar,
                            hybrid.tank_vapour_density, hybrid.injector_loss_coefficient)

hybrid_vap = HybridVapour(T_vap, hybrid.tank_vapour_mass, hybrid.tank_vapour_density, hybrid.tank_pressure_bar,
                          hybrid.chamber_pressure_bar, hybrid.injector_loss_coefficient, m_vap_flow, 0, hybrid.tank_propellant_contents_mass, hybrid.hybrid_fault)
hybrid_vap ==hybrid

hybrid_vap.vapour_init()

# while hybrid_vap.erlier >= hybrid_vap.mdot_tank_outflow:
# while x <= 9.32:
while hybrid_vap.vapour_mass > 0.1 and time <= cea['time_max']:

    hybrid_vap = subcritical_tank_no_liquid(hybrid_vap)
    hybrid_vap = simmulate_regression(hybrid_vap)
    hybrid_vap = simmulate_engine_efficience(hybrid_vap)
    #print(x, " ", hybrid_vap.mdot_tank_outflow)
    #oxid_flow.append(hybrid_vap.mdot_tank_outflow)
    prepare_data_lists(OF, Pressure_Chamber, Pressure_Vessel, Thrust, Isp, Fuel_Flow, Oxid_Flow, Time, Radius,hybrid_vap)
    #x += 0.01
    time += 0.01


plot_config = [[cea["thrust_checkbox"],cea["Thrust_input"]], [cea["vessel_checkbox"],cea["Vessel_input"]],[cea["chamber_checkbox"], cea["Chamber_input"]],[cea["burned_fuel"],cea["oxid_mass"]]]

if compare_flag == False:
   plot_config[0][0] = False
   plot_config[1][0] = False
   plot_config[2][0] = False
   #plot_config[3][3] = False

plot(OF, Pressure_Chamber, Pressure_Vessel, Thrust, Isp, Fuel_Flow, Oxid_Flow, Time, Radius,plot_config)
# if compare_flag == True:
#    if cea["thrust_checkbox"]:
#       pass
#    if cea["vessel_checkbox"]:
#       pass
#    if cea["chamber_checkbox"]:
#       pass

if txt_flag == True:
   make_txt(Pressure_Chamber,Pressure_Vessel,Thrust,Time,Fuel_Flow,Oxid_Flow)






#print(oxid_flow)
#y=0


# with open("test.txt","w") as file:
#     for i in oxid_flow:
#         file.write(str(y).replace(".", ","))
#         file.write(" ")
#         file.write(str(i).replace(".",","))
#         y+=0.01
#         file.write("\n")
