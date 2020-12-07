#!/usr/bin/python3
#coding:utf-8
# test in Win
__version__ = 20191208



import os,sys
import PySimpleGUI as sg      
from multiprocessing import Process,freeze_support


from config import logfile,dldir
from xm_json import chromef12


layout = [           
    [sg.Text('Year',size=(5, 1)),sg.InputText(size=(20, 1),key='year',default_text='2019')],    
    # [sg.Text('_'*36,justification='center')],          
    # [sg.Text('_'*36,justification='center')],
    [sg.Button('Go',tooltip='Click to start',key='go'),sg.Button('Stop',key='stop',disabled=True)]      
]  


window = sg.Window('xiami',layout, grab_anywhere=False,size=(150,70))      


def xmgui(dldir):
    while True:
        event, values = window.Read()  
        if event is None:
            break        
        elif event == 'go':  
            year = values['year']
            chromef12(year)
    window.Close()




if __name__ == "__main__":
    freeze_support()
    try:
        # if os.path.exists(logfile):
        #     os.remove(logfile)
        xmgui(dldir)
    except KeyboardInterrupt:
        print('ctrl + c')
    