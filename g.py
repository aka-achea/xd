import os
import PySimpleGUI as sg      
from multiprocessing import Process,freeze_support


layout = [           
    [sg.Text('Year', size=(5, 1)), sg.InputText(size=(10, 1),key='year')],    
    # [sg.Text('_'*36,justification='center')],          
    # [sg.Text('_'*36,justification='center')],
    [sg.Button('Go',tooltip='Click to start',key='go'),sg.Button('Stop',key='stop',disabled=True)]      
]  


window = sg.Window(f'Xiami download', layout, default_element_size=(40, 1),
             grab_anywhere=False,size=(100,70))      


def xdgui():

    while True:
        event, values = window.Read()  
        if event is None:
            break
        
        elif event == 'go':
            print(value['year'])

        
    window.Close()


if __name__ == "__main__":
    freeze_support()
    try:
        xdgui()
    except KeyboardInterrupt:
        print('ctrl + c')
    