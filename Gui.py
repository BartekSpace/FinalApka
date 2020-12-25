import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

def set_gui ():
    bl = {'size': (25,1)}
    br = {'size': (30,1), 'justification':('right')}

    tab1_layout =  [
        [sg.T('This is inside tab 1')],
       # [sg.Checkbox('Simulation time',default=True,key='check')],
        [ sg.Text("Time [s]"),sg.InputText( key='time_max',disabled=False,default_text='15')],
        [sg.Text('_'*120)],


        [sg.Text('Engine',size=(25,1),font=16,text_color='red'), sg.Text('Vessel', size=(40,1), font=16,justification='right',text_color='red')],
        [sg.Text('Combustion Pressure [bar]',**bl ), sg.InputText(key='Combustion_Pressure', default_text='30'),sg.Text('Pressure [bar]', **br), sg.InputText(key='Vessel_Pressure',default_text='60')],
        [sg.Text('Injector hole diameter [mm]', **bl), sg.InputText(key='hole_diam',default_text='1.5'),sg.Text('Volume [dm3]',**br), sg.InputText(key='Vessel_Volume', default_text='15')],
        [sg.Text('Holes number',**bl ), sg.InputText(key='holes_num',default_text='36'),sg.Text('Oxidizer Mass [kg]',**br),sg.InputText(key='oxid_mass',default_text='10.5')],
        [sg.Text('Throat Diameter [mm]',**bl), sg.InputText(key='throat_diam',default_text='32.8')],
        [sg.Text('Exit Nozzle Diameter [mm]', **bl), sg.InputText(key='nozzle_exit', default_text='70')],
        [sg.Text('K Loss', **bl),sg.InputText(key='K_loss',default_text='4.2')],
        [sg.Text('Real coeff',**bl),sg.InputText(key='chuj_coeff',default_text='0.9')],
        [sg.Text('_'*120)],
        [sg.Text('Fuel',size=(25,1),font=16,text_color='red')],
        [sg.Text('Length [mm]',**bl),sg.InputText(key='fuel_length',default_text='1000')],
        [sg.Text('Port Diameter [mm]',**bl),sg.InputText(key='port_diam',default_text='60')],
        [sg.Text('Density [kg/m3]',**bl),sg.InputText(key='fuel_dens',default_text='1130')],
        [sg.Text('a ballistic',**bl),sg.InputText(key='a_ballistic',default_text='0.00772597539149796')],
        [sg.Text('n ballistic',**bl),sg.InputText(key='n_ballistic',default_text='0.777265794840152')],
                    ]

    tab2_layout = [[sg.T('This is inside tab 2')],

                    [sg.Text('Oxidizer',size=(25,1),font=16,text_color='red'), sg.Text('Fuel', size=(40,1), font=16,justification='right',text_color='red')],
                   [sg.Text('Name', **bl), sg.InputText(key='oxid_name',default_text='Nitrous'), sg.Text('Name', **br),sg.InputText(key='fuel_name', default_text='Nylon')],
                   [sg.Text('Formula', **bl), sg.InputText(key='oxid_formula',default_text='N 2.0 O 1.0'), sg.Text('Formula', **br),sg.InputText(key='fuel_formula',default_text='C 6.0   H 11.0   O 1.0  N 1.0')],
                   [sg.Text('Temperature [K]', **bl), sg.InputText(key='oxid_temp',default_text='298.15'), sg.Text('Temperature [K]', **br),sg.InputText(key='fuel_temp',default_text='298.15')],
                   [sg.Text('Enthalpy [kJ/mol]', **bl), sg.InputText(key='oxid_enthalpy',default_text='75.24'), sg.Text('Enthalpy [kJ/mol]', **br),sg.InputText(key='fuel_enthalpy',default_text='67.69')],
                   ]

    tab3_layout = [[sg.T('This is inside tab 2')],

                   [sg.Text('Compare', size=(25, 1), font=16, text_color='red')],
                    #sg.Text('Fuel', size=(40, 1), font=16, justification='right', text_color='red')],


                #   [sg.Text('Name', **bl), sg.InputText(key='oxid_name', default_text='Nitrous'), sg.Text('Name', **br),
                 #   sg.InputText(key='fuel_name', default_text='Nylon')],
                   #[sg.Radio(key='m',text="d",group_id=1)],[sg.Radio(key='m',text="d",group_id=1)],
                   [sg.Checkbox(default=True,key="thrust_checkbox",text="Thrust",**bl), sg.Text('Path:', **br),sg.InputText(key='Thrust_input', default_text='Real/Thrust.txt') ],
                   [sg.Checkbox(default=True,key="vessel_checkbox",text="Pressure Vessel",**bl), sg.Text('Path:', **br),sg.InputText(key='Vessel_input', default_text='Real/Vessel.txt')],
                   [sg.Checkbox(default=True,key="chamber_checkbox",text="Pressure Chamber",**bl), sg.Text('Path:', **br), sg.InputText(key='Chamber_input', default_text='Real/Chamber.txt')],
                   [sg.Text("_"*120)],
                   [sg.Text('Burned Fuel Mass [kg]',**bl), sg.InputText(key="burned_fuel", default_text="0")]
                   ]

                   # [sg.In(key='in')]]

    layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout, tooltip='tip'), sg.Tab('Tab 2', tab2_layout),sg.Tab('Tab3',tab3_layout)]], tooltip='TIP2')],
              [sg.Button('Subbmit',key='button'),sg.Button('Generate Txt',key='txt'),sg.Button('Compare',key='compare'),sg.Button('Quit',key='quit')]]

    window = sg.Window('My window with tabs', default_element_size=(25,1)).Layout(layout).Finalize()

    #event,values = window.Read()
    #sg.Popup(event,values)





    while True:

       #
        # if window.Element('check'):
        #     window.Element('maslo').Update(disabled=False)
        #
        # if not window.Element('check'):
        #     window.Element('maslo').Update(disabled=True)
        # if event == 'check':
        #     if values[0] == True:
        #         window.Element('maslo').Update(disabled=False)
        #     if values[0] == False:
        #         window.Element('maslo').Update(disabled=True)

        # if values[0] == True:
        #       window.FindElement('maslo').Update(disabled=False)
        # if values[0] == False:
        #       window.FindElement('maslo').Update(disabled=True)
        #event, values = window.Read()
        event, values = window.read()
        txt_flag = False
        compare_flaq = False
       # print (values)

        if event is None:  # always,  always give a way out!
             quit()
             break
        if event is 'quit':
            quit()

        if event is 'button':
            return values, txt_flag, compare_flaq
            #print(event, values)
            quit()
            #print ('dupa')
        if event is 'txt':
            txt_flag = True
            return values, txt_flag,compare_flaq
            quit()
        if event is 'compare':
            compare_flaq = True
            return values,txt_flag,compare_flaq
            quit()


    # while True:
    #     event, values = window.read()
    #     print(event,values)
    #     if event is None:           # always,  always give a way out!
    #         break

