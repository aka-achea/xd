#!/usr/bin/python3
#coding:utf-8
# test in Win
# version:20190827



import os,sys,pathlib
import PySimpleGUI as sg      
from multiprocessing import Process,freeze_support
import pyautogui as auto

from mytool import clickbutton,mywait,capture
from xm_json import xm_json
from config import logfile,dldir


layout = [           
    [sg.Text('Year',size=(5, 1)),sg.InputText(size=(20, 1),key='year')],    
    # [sg.Text('_'*36,justification='center')],          
    # [sg.Text('_'*36,justification='center')],
    [sg.Button('Go',tooltip='Click to start',key='go'),sg.Button('Stop',key='stop',disabled=True)]      
]  


window = sg.Window('xiami',layout, grab_anywhere=False,size=(150,70))      


def xmgui(workfolder):

    while True:
        event, values = window.Read()  
        if event is None:
            break        
        elif event == 'go':  
            imgpath = os.path.join(pathlib.PurePath(__file__).parent,'img')
            clickbutton( os.path.join(imgpath,'xm.png'))
            auto.press('f12')
            mywait(1)
            auto.press('f5')
            clickbutton( os.path.join(imgpath,'getalbumdetail.png'))
            auto.click(button='right')
            clickbutton( os.path.join(imgpath,'copy.png'))
            clickbutton( os.path.join(imgpath,'copyresponse.png'))
            year = values['year']
            xm_json(workfolder,year=year)
            auto.hotkey('ctrl','w')
    window.Close()


if __name__ == "__main__":
    freeze_support()
    try:
        if os.path.exists(logfile):
            os.remove(logfile)
        xmgui(dldir)
    except KeyboardInterrupt:
        print('ctrl + c')
    