# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyvisa
import serial
import numpy as np
import datetime
import cmath
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
import time
import os
import re

num_runs = 10

class DRM(object):

    def __init__(self):

        self.ChamberState = [  # possible subject positions
            ('Empty', 'e'),
            ('Replica', 'r'),
            ('Specimen', 's')
        ]

        #Empty chamber frequency 1
        self.YEFreq.set('0.00000')
        self.XEFreq.set('0.00000')
        self.YEQ1.set('0.00000')
        self.XEQ1.set('0.00000')
        self.ZEFreq.set('0.00000')
        self.ZEQ1.set('0.00000')

        # Loaded chamber SPECIMEN sample
        self.YSFreq.set('0.00000')
        self.XSFreq.set('0.00000')
        self.YSQ.set('0.00000')
        self.XSQ.set('0.00000')
        self.ZSFreq.set('0.00000')
        self.ZSQ.set('0.00000')

        self.e_star1.set('0.00000')
        self.e_star2.set('0.00000')
        self.vs1.set('0.00000')
        self.vs2.set('0.00000')

        # Empty chamber frequency 2
        self.YEFreq2.set('0.00000')
        self.XEFreq2.set('0.00000')
        self.YEQ2.set('0.00000')
        self.XEQ2.set('0.00000')
        self.ZEFreq2.set('0.00000')
        self.ZEQ2.set('0.00000')

        # Loaded chamber REPLICA sample
        self.YRFreq.set('0.00000')
        self.XRFreq.set('0.00000')
        self.YRQ.set('0.00000')
        self.ZRFreq.set('0.00000')
        self.ZRQ.set('0.00000')
        self.XRQ.set('0.00000')

        # Empty chamber frequency 3
        self.YEFreq3.set('0.00000')
        self.XEFreq3.set('0.00000')
        self.ZEFreq3.set('0.00000')
        self.YEQ3.set('0.00000')
        self.XEQ3.set('0.00000')
        self.ZEQ3.set('0.00000')

        self.deltaOmega_x1.set('0.00000')
        self.deltaOmega_y1.set('0.00000')
        self.deltaOmega_z1.set('0.00000')

        self.deltaOmega_x2.set('0.00000')
        self.deltaOmega_y2.set('0.00000')
        self.deltaOmega_z2.set('0.00000')

        self.sig_r_omega1.set('0.00000')
        self.sig_r_omega2.set('0.00000')

        self.alpha1_vol.set('0.00000')
        self.alpha2_vol.set('0.00000')

        self.alpha1.set('0.00000')
        self.tand.set('0.00000')

        self.temperature.set('0.00000')
        self.humidity.set('0.00000')

        self.vs1 = '0.00000'
        self.vs1.set('0.00000')
        self.vs2 = '0.00000'
        self.vs2.set('0.00000')

        self.e_star2.set('0.0000')


    def calc(self):
        for i in range(num_runs):
            # volume of cavity
            vc = 0.275 * 0.3 * 0.336
   
            #room temperature
            # self.Arduino_Serial.write(str.encode('3'))
            # time.sleep(2)
            # temp_data = self.Arduino_Serial.readline().decode('utf-8') # deg. C
            # temp_data = re.sub("[^0-9.]", "", temp_data)
            # self.temperature = temp_data[:5]
            # self.humidity = temp_data[-5:]
   
            # SAMPLE DETAILS
   
            # 1: SAMPLE
            # 2: REPLICA
   
            # sample volumes - from geometry or from mass/density or .stl reader
            self.vs1 = (self.vs1)*0.000001 # m^3 from geometry
            self.vs2 = (self.vs2)*0.000001 # m^3
   
   
            # DATA FROM ENA: EMPTY (AT START)
   
            # measured resonant frequency (MHz) and Q-factor, empty, x, 1, before
            f0_x1_before = DRM.XEFreq
            Q0_x1_before = DRM.XEQ1
   
            # measured resonant frequency (MHz) and Q-factor, empty, y, 1, before
            f0_y1_before = DRM.YEFreq
            Q0_y1_before = DRM.YEQ1
   
            # measured resonant frequency (MHz) and Q-factor, empty, z, 1, before
            f0_z1_before = DRM.ZEFreq
            Q0_z1_before = DRM.ZEQ1
   
            # SPECIMEN 1 (ORIGINAL)
   
            # measured resonant frequency (MHz) and Q-factor, sample 1, x
            f_x1 = DRM.XSFreq
            Q_x1 = DRM.XSQ
   
            # measured resonant frequency (MHz) and Q-factor, sample 1, y
            f_y1 = DRM.YSFreq
            Q_y1 = DRM.YSQ
   
            # measured resonant frequency (MHz) and Q-factor, sample 1, z
            f_z1 = DRM.ZSFreq
            Q_z1 = DRM.ZSQ
   
            # EMPTY (IN BETWEEN SAMPLES 1 AND 2)
   
            # measured resonant frequency (MHz) and Q-factor, empty, x, 1, after
            f0_x1_after = DRM.XEFreq1
            Q0_x1_after = DRM.XEQ2
   
            # measured resonant frequency (MHz) and Q-factor, empty, y, 1, after
            f0_y1_after = DRM.YEFreq1
            Q0_y1_after = DRM.YEQ2
   
            # measured resonant frequency (MHz) and Q-factor, empty, z, 1, after
            f0_z1_after = DRM.ZEFreq1
            Q0_z1_after = DRM.ZEQ2
   
   
            # 'after' for sample 1 is 'before' for sample 2
            # resonant frequency (MHz) and Q-factor, empty, x, 2, before
            f0_x2_before = f0_x1_after
            Q0_x2_before = Q0_x1_after
   
   
            # resonant frequency (MHz) and Q-factor, empty, y, 2, before
            f0_y2_before = f0_y1_after
            Q0_y2_before = Q0_y1_after
   
   
            # resonant frequency (MHz) and Q-factor, empty, z, 2, before
            f0_z2_before = f0_z1_after
            Q0_z2_before = Q0_z1_after
   
            # SAMPLE 2 (REPLICA)
   
            # measured resonant frequency (MHz) and Q-factor, sample 2, x
            f_x2 = DRM.XRFreq
            Q_x2 = DRM.XRQ
   
            # measured resonant frequency (MHz) and Q-factor, sample 2, y
            f_y2 = DRM.YRFreq
            Q_y2 = DRM.YRQ
   
            # measured resonant frequency (MHz) and Q-factor, sample 2, z
            f_z2 = DRM.ZRFreq
            Q_z2 = DRM.ZRQ
   
            # EMPTY (AT END)
   
            # measured resonant frequency (MHz) and Q-factor, empty, x, 2, after
            f0_x2_after = DRM.XEFreq2
            Q0_x2_after = DRM.XEQ3
   
            # measured resonant frequency (MHz) and Q-factor, empty, y, 2, after
            f0_y2_after = DRM.YEFreq2
            Q0_y2_after = DRM.YEQ3
   
            # measured resonant frequency (MHz) and Q-factor, empty, z, 2, after
            f0_z2_after = DRM.ZEFreq2
            Q0_z2_after = DRM.ZEQ3
   
            # TIMING
   
            # weights for f0 and Q0 measured before and after sample 1
            w_x1_before = (self.MeasurementTime[6] - self.MeasurementTime[3]) / (self.MeasurementTime[6] - self.MeasurementTime[0])
            w_x1_after = (self.MeasurementTime[3] - self.MeasurementTime[0]) / (self.MeasurementTime[6] - self.MeasurementTime[0])
   
   
            w_y1_before = (self.MeasurementTime[7] - self.MeasurementTime[4]) / (self.MeasurementTime[7] - self.MeasurementTime[1])
            w_y1_after = (self.MeasurementTime[4] - self.MeasurementTime[1]) / (self.MeasurementTime[7] - self.MeasurementTime[1])
   
            w_z1_before = (self.MeasurementTime[8] - self.MeasurementTime[5]) / (self.MeasurementTime[8] - self.MeasurementTime[2])
            w_z1_after = (self.MeasurementTime[5] - self.MeasurementTime[2]) / (self.MeasurementTime[8] - self.MeasurementTime[2])
   
            # weights for f0 and Q0 measured before and after sample 2
            w_x2_before = (self.MeasurementTime[12] - self.MeasurementTime[9]) / (self.MeasurementTime[12] - self.MeasurementTime[6])
            w_x2_after = (self.MeasurementTime[9] - self.MeasurementTime[6]) / (self.MeasurementTime[12] - self.MeasurementTime[6])
   
            w_y2_before = (self.MeasurementTime[13] - self.MeasurementTime[10]) / (self.MeasurementTime[13] - self.MeasurementTime[7])
            w_y2_after = (self.MeasurementTime[10] - self.MeasurementTime[7]) / (self.MeasurementTime[13] - self.MeasurementTime[7])
   
            w_z2_before = (self.MeasurementTime[14] - self.MeasurementTime[11]) / (self.MeasurementTime[14] - self.MeasurementTime[8])
            w_z2_after = (self.MeasurementTime[11] - self.MeasurementTime[8]) / (self.MeasurementTime[14] - self.MeasurementTime[8])
   
            # EMPTY 1 WEIGHTED AVERAGE
   
            # measured resonant frequency (MHz) and Q-factor, empty, x, 1
            # mean of 'before' and 'after'
            f0_x1 = w_x1_before * f0_x1_before + w_x1_after * f0_x1_after
            Q0_x1 = w_x1_before * Q0_x1_before + w_x1_after * Q0_x1_after
   
            # measured resonant frequency (MHz) and Q-factor, empty, y, 1
            # mean of 'before' and 'after'
            f0_y1 = w_y1_before * f0_y1_before + w_y1_after * f0_y1_after
            Q0_y1 = w_y1_before * Q0_y1_before + w_y1_after * Q0_y1_after
   
            # measured resonant frequency (MHz) and Q-factor, empty, z, 1
            # mean of 'before' and 'after'
            f0_z1 = w_z1_before * f0_z1_before + w_z1_after * f0_z1_after
            Q0_z1 = w_z1_before * Q0_z1_before + w_z1_after * Q0_z1_after
   
            # EMPTY 2 WEIGHTED AVERAGE
   
            # measured resonant frequency (MHz) and Q-factor, empty, x, 2
            # mean of 'before' and 'after'
            f0_x2 = w_x2_before * f0_x2_before + w_x2_after * f0_x2_after
            Q0_x2 = w_x2_before * Q0_x2_before + w_x2_after * Q0_x2_after
   
   
            # measured resonant frequency (MHz) and Q-factor, empty, y, 2
            # mean of 'before' and 'after'
            f0_y2 = w_y2_before * f0_y2_before + w_y2_after * f0_y2_after
            Q0_y2 = w_y2_before * Q0_y2_before + w_y2_after * Q0_y2_after
   
            # measured resonant frequency (MHz) and Q-factor, empty, z, 2
            # mean of 'before' and 'after'
            f0_z2 = w_z2_before * f0_z2_before + w_z2_after * f0_z2_after
            Q0_z2 = w_z2_before * Q0_z2_before + w_z2_after * Q0_z2_after
   
            # CALCULATE COMPLEX PERMITTIVITY
   
            # shifts in complex frequency
            self.deltaOmega_x1 = (f_x1 - f0_x1) / f0_x1 + 0.5 * 1j * (1. / Q_x1 - 1. / Q0_x1)
            self.deltaOmega_y1 = (f_y1 - f0_y1) / f0_y1 + 0.5 * 1j * (1. / Q_y1 - 1. / Q0_y1)
            self.deltaOmega_z1 = (f_z1 - f0_z1) / f0_z1 + 0.5 * 1j * (1. / Q_z1 - 1. / Q0_z1)
   
            self.sig_r_omega1 = 1. / self.deltaOmega_x1 + 1. / self.deltaOmega_y1 + 1. / self.deltaOmega_z1
   
            # or measured data (comment out if using previous data)
            self.deltaOmega_x2 = (f_x2 - f0_x2) / f0_x2 + 0.5 * 1j * (1. / Q_x2 - 1. / Q0_x2)
            self.deltaOmega_y2 = (f_y2 - f0_y2) / f0_y2 + 0.5 * 1j * (1. / Q_y2 - 1. / Q0_y2)
            self.deltaOmega_z2 = (f_z2 - f0_z2) / f0_z2 + 0.5 * 1j * (1. / Q_z2 - 1. / Q0_z2)
   
            self.sig_r_omega2 = 1. / self.deltaOmega_x2 + 1. / self.deltaOmega_y2 + 1. / self.deltaOmega_z2
   
   
            # Clausius-Mosotti factor for material 2 (replica)
            self.alpha2 = (self.e_star2 - 1) / (self.e_star2 + 2)
   
            # new analysis, quadratic fit
   
            p = [-0.056155651313900 + 0.000580840419927j,
                 -0.468920921941625 + 0.000960280535180j,
                 0.0000 + 0.0000j]
   
            # permittivity estimates from volume only
            self.alpha1_vol = np.polyval(p, vc / (self.vs1 * self.sig_r_omega1))
            self.e_star1_vol = (1 + 2 * self.alpha1_vol) / (1 - self.alpha1_vol)
            self.alpha2_vol = np.polyval(p, vc / (self.vs2 * self.sig_r_omega2))
            self.e_star2_vol = (1 + 2 * self.alpha2_vol) / (1 - self.alpha2_vol)
   
            # Clausius-Mosotti factor for material 1 (original)
   
            self.alpha1 = self.alpha2 * np.polyval(p, vc / (self.vs1 * self.sig_r_omega1)) / np.polyval(p, vc / (self.vs2 * self.sig_r_omega2))
   
            # permittivity of material 1 (SPECIMEN)
            self.e_star1 = (1 + (2 * self.alpha1)) / (1 - self.alpha1)
            print(self.e_star1)
   
            # loss tangent of material 1 (original)
            self.tand = -np.imag(self.e_star1) / np.real(self.e_star1)
           
            # Print or store the results if needed
            print("Run", i + 1, "completed.")

            # Add a delay to control the frequency of calculations
            time.sleep(10)  # Adjust the delay time as needed

class GUI(object):


    def __init__(self):  # Initialise the GUI

        self.root = Tk()
        self.status = '0'
        self.rm = pyvisa.ResourceManager()
        self.ENA = self.rm.open_resource('GPIB0::1::INSTR')  # ENA-E5061A
        self.ENA.Arduino_Serial = serial.Serial('com3', 9600)
        self.ENA.Arduino_Serial.close()
        self.ENA.MeasurementNum = 0
        self.ENA.ChamberState = 'e'
        self.ENA.MeasurementTime = [None] * 15
        self.filename = ""
        self.master = self.root
        self.headingFont = 'Helvetica'

        ## Title"
        self.TitleFrame = Frame(self.master, borderwidth=10)  # create a frame for the title
        self.TitleFrame.pack(side=TOP, fill="x")

        #TAB setup
        self.nb = Notebook(self.master)
        self.tab1 = Frame(self.nb)
        self.nb.add(self.tab1, text='Parameters')
        self.tab2 = Frame(self.nb)
        self.nb.add(self.tab2, text='Measure')
        self.nb.pack(expand=1, fill='both')

        #Measurement TAB2
        self.MSFrame = Frame(self.tab2, borderwidth=1)  # Full Frame
        self.MSFrame.pack(side=LEFT, anchor=W)
        self.MFrame = Frame(self.MSFrame, borderwidth=10)  # Measurement Frame
        self.MFrame.pack(side=LEFT, anchor=W)
        self.OFrame = Frame(self.MSFrame, borderwidth=10)  # Output Frame
        self.OFrame.pack(side=BOTTOM, anchor=N, fill="x")

        #Parameter TAB1
        self.MSFrame1 = Frame(self.tab1, borderwidth=1)  # Full Frame
        self.MSFrame1.pack(side=TOP, anchor=W)
        self.MFrame1 = Frame(self.MSFrame1, borderwidth=10)  # Measurement Frame
        self.MFrame1.pack(side=LEFT, anchor=W)
        self.OFrame1 = Frame(self.MSFrame1, borderwidth=10)  # Output Frame
        self.OFrame1.pack(side=BOTTOM, anchor=N, fill="x")

        # Measurement
        self.MeasFrame = Frame(self.MFrame, borderwidth=10)  # create a frame for measurement setup
        self.MeasFrame.pack(side=TOP, anchor=W, fill="x")  #

        # Frequency Displays:
        ##################################
        # GUI FOR EMPTY RESULTS 1
        self.VERFrame = Frame(self.MFrame, borderwidth=10)  # create a frame for measurement setup
        self.VERFrame.pack(side=TOP, anchor=W, fill="x")  #
        self.VERLabel = Label(self.VERFrame, text="X. empty /MHz:")
        self.VERLabel.pack(side=LEFT, anchor=W)
        self.VERLabelTxt = StringVar()
        self.VERLabelEntry = Entry(self.VERFrame, textvariable=self.VERLabelTxt, width=25)
        self.VERLabelEntry.pack(side=RIGHT, anchor=W)

        self.VERFrameQ = Frame(self.OFrame, borderwidth=10)
        self.VERFrameQ.pack(side=TOP, anchor=W, fill="x")
        self.VERLabelQ = Label(self.VERFrameQ, text="X. empty /Q:")
        self.VERLabelQ.pack(side=LEFT, anchor=W)
        self.VERLabelQTxt = StringVar()
        self.VERLabelQEntry = Entry(self.VERFrameQ, textvariable=self.VERLabelQTxt, width=25)
        self.VERLabelQEntry.pack(side=RIGHT, anchor=W)

        self.HERFrame = Frame(self.MFrame, borderwidth=10)
        self.HERFrame.pack(side=TOP, anchor=W, fill="x")
        self.HERLabel = Label(self.HERFrame, text= 'Y. empty /MHz:')
        self.HERLabel.pack(side=LEFT, anchor=W)
        self.HERLabelTxt = StringVar()
        self.HERLabelEntry = Entry(self.HERFrame, textvariable=self.HERLabelTxt, width=25)
        self.HERLabelEntry.pack(side=RIGHT, anchor=W)

        self.HERFrameQ = Frame(self.OFrame, borderwidth=10)
        self.HERFrameQ.pack(side=TOP, anchor=W, fill="x")
        self.HERLabelQ = Label(self.HERFrameQ, text="Y. empty /Q:")
        self.HERLabelQ.pack(side=LEFT, anchor=W)
        self.HERLabelQTxt = StringVar()
        self.HERLabelQEntry = Entry(self.HERFrameQ, textvariable=self.HERLabelQTxt, width=25)
        self.HERLabelQEntry.pack(side=RIGHT, anchor=W)

        self.ZERFrame = Frame(self.MFrame, borderwidth=10)
        self.ZERFrame.pack(side=TOP, anchor=W, fill="x")
        self.ZERLabel = Label(self.ZERFrame, text="Z. empty /MHz:")
        self.ZERLabel.pack(side=LEFT, anchor=W)
        self.ZERLabelTxt = StringVar()
        self.ZERLabelEntry = Entry(self.ZERFrame, textvariable=self.ZERLabelTxt, width=25)
        self.ZERLabelEntry.pack(side=RIGHT, anchor=W)

        self.ZERFrameQ = Frame(self.OFrame, borderwidth=10)
        self.ZERFrameQ.pack(side=TOP, anchor=W, fill="x")
        self.ZERLabelQ = Label(self.ZERFrameQ, text="Z. empty /Q:")
        self.ZERLabelQ.pack(side=LEFT, anchor=W)
        self.ZERLabelQTxt = StringVar()
        self.ZERLabelQEntry = Entry(self.ZERFrameQ, textvariable=self.ZERLabelQTxt, width=25)
        self.ZERLabelQEntry.pack(side=RIGHT, anchor=W)

        ##################################
        # GUI FOR SAMPLE RESULTS
        self.VSRFrame = Frame(self.MFrame, borderwidth=10)  # create a frame for measurement setup
        self.VSRFrame.pack(side=TOP, anchor=W, fill="x")  #
        self.VSRLabel = Label(self.VSRFrame, text="X. Original /MHz:")
        self.VSRLabel.pack(side=LEFT, anchor=W)
        self.VSRLabelTxt = StringVar()
        self.VSRLabelEntry = Entry(self.VSRFrame, textvariable=self.VSRLabelTxt, width=25)
        self.VSRLabelEntry.pack(side=RIGHT, anchor=W)

        self.VSRFrameQ = Frame(self.OFrame, borderwidth=10)
        self.VSRFrameQ.pack(side=TOP, anchor=W, fill="x")
        self.VSRLabelQ = Label(self.VSRFrameQ, text="X. Original /Q:")
        self.VSRLabelQ.pack(side=LEFT, anchor=W)
        self.VSRLabelQTxt = StringVar()
        self.VSRLabelQEntry = Entry(self.VSRFrameQ, textvariable=self.VSRLabelQTxt, width=25)
        self.VSRLabelQEntry.pack(side=RIGHT, anchor=W)

        self.HSRFrame = Frame(self.MFrame, borderwidth=10)
        self.HSRFrame.pack(side=TOP, anchor=W, fill="x")
        self.HSRLabel = Label(self.HSRFrame, text="Y. Original /MHz:")
        self.HSRLabel.pack(side=LEFT, anchor=W)
        self.HSRLabelTxt = StringVar()
        self.HSRLabelEntry = Entry(self.HSRFrame, textvariable=self.HSRLabelTxt, width=25)
        self.HSRLabelEntry.pack(side=RIGHT, anchor=W)

        self.HSRFrameQ = Frame(self.OFrame, borderwidth=10)
        self.HSRFrameQ.pack(side=TOP, anchor=W, fill="x")
        self.HSRLabelQ = Label(self.HSRFrameQ, text="Y. Original /Q:")
        self.HSRLabelQ.pack(side=LEFT, anchor=W)
        self.HSRLabelQTxt = StringVar()
        self.HSRLabelQEntry = Entry(self.HSRFrameQ, textvariable=self.HSRLabelQTxt, width=25)
        self.HSRLabelQEntry.pack(side=RIGHT, anchor=W)

        self.ZSRFrame = Frame(self.MFrame, borderwidth=10)
        self.ZSRFrame.pack(side=TOP, anchor=W, fill="x")
        self.ZSRLabel = Label(self.ZSRFrame, text="Z. Original /MHz:")
        self.ZSRLabel.pack(side=LEFT, anchor=W)
        self.ZSRLabelTxt = StringVar()
        self.ZSRLabelEntry = Entry(self.ZSRFrame, textvariable=self.ZSRLabelTxt, width=25)
        self.ZSRLabelEntry.pack(side=RIGHT, anchor=W)

        self.ZSRFrameQ = Frame(self.OFrame, borderwidth=10)
        self.ZSRFrameQ.pack(side=TOP, anchor=W, fill="x")
        self.ZSRLabelQ = Label(self.ZSRFrameQ, text="Z. Original /Q:")
        self.ZSRLabelQ.pack(side=LEFT, anchor=W)
        self.ZSRLabelQTxt = StringVar()
        self.ZSRLabelQEntry = Entry(self.ZSRFrameQ, textvariable=self.ZSRLabelQTxt, width=25)
        self.ZSRLabelQEntry.pack(side=RIGHT, anchor=W)

        ##################################
        # GUI FOR EMPTY RESULTS 2
        self.VERFrame1 = Frame(self.MFrame, borderwidth=10)  # create a frame for measurement setup
        self.VERFrame1.pack(side=TOP, anchor=W, fill="x")  #
        self.VERLabel1 = Label(self.VERFrame1, text="X1. empty /MHz:")
        self.VERLabel1.pack(side=LEFT, anchor=W)
        self.VERLabel1Txt = StringVar()
        self.VERLabel1Entry = Entry(self.VERFrame1, textvariable=self.VERLabel1Txt, width=25)
        self.VERLabel1Entry.pack(side=RIGHT, anchor=W)

        self.VERFrameQ1 = Frame(self.OFrame, borderwidth=10)
        self.VERFrameQ1.pack(side=TOP, anchor=W, fill="x")
        self.VERLabelQ = Label(self.VERFrameQ1, text="X1. empty /Q:")
        self.VERLabelQ.pack(side=LEFT, anchor=W)
        self.VERFrameQ1Txt = StringVar()
        self.VERLabel1QEntry = Entry(self.VERFrameQ1, textvariable=self.VERFrameQ1Txt, width=25)
        self.VERLabel1QEntry.pack(side=RIGHT, anchor=W)

        self.HERFrame1 = Frame(self.MFrame, borderwidth=10)
        self.HERFrame1.pack(side=TOP, anchor=W, fill="x")
        self.HERLabel1 = Label(self.HERFrame1, text="Y1. empty /MHz:")
        self.HERLabel1.pack(side=LEFT, anchor=W)
        self.HERLabel1Txt = StringVar()
        self.HERLabel1Entry = Entry(self.HERFrame1, textvariable=self.HERLabel1Txt, width=25)
        self.HERLabel1Entry.pack(side=RIGHT, anchor=W)

        self.HERFrameQ1 = Frame(self.OFrame, borderwidth=10)
        self.HERFrameQ1.pack(side=TOP, anchor=W, fill="x")
        self.HERLabelQ = Label(self.HERFrameQ1, text="Y1. empty /Q:")
        self.HERLabelQ.pack(side=LEFT, anchor=W)
        self.HERFrame1Q1Txt = StringVar()
        self.HERLabelQ1Entry = Entry(self.HERFrameQ1, textvariable=self.HERFrame1Q1Txt, width=25)
        self.HERLabelQ1Entry.pack(side=RIGHT, anchor=W)

        self.ZERFrame1 = Frame(self.MFrame, borderwidth=10)
        self.ZERFrame1.pack(side=TOP, anchor=W, fill="x")
        self.ZERLabel1 = Label(self.ZERFrame1, text="Z1. empty /MHz:")
        self.ZERLabel1.pack(side=LEFT, anchor=W)
        self.ZERLabel1Txt = StringVar()
        self.ZERLabel1Entry = Entry(self.ZERFrame1, textvariable=self.ZERLabel1Txt, width=25)
        self.ZERLabel1Entry.pack(side=RIGHT, anchor=W)

        self.ZERFrameQ1 = Frame(self.OFrame, borderwidth=10)
        self.ZERFrameQ1.pack(side=TOP, anchor=W, fill="x")
        self.ZERLabelQ1 = Label(self.ZERFrameQ1, text="Z1. empty /Q:")
        self.ZERLabelQ1.pack(side=LEFT, anchor=W)
        self.ZERFrame1Q1Txt = StringVar()
        self.ZERLabelQ1Entry = Entry(self.ZERFrameQ1, textvariable=self.ZERFrame1Q1Txt, width=25)
        self.ZERLabelQ1Entry.pack(side=RIGHT, anchor=W)

        ##################################
        # GUI FOR REPLICA RESULTS
        self.VRRFrame = Frame(self.MFrame, borderwidth=10)  # create a frame for measurement setup
        self.VRRFrame.pack(side=TOP, anchor=W, fill="x")  #
        self.VRRLabel = Label(self.VRRFrame, text="X. Replica /MHz:")
        self.VRRLabel.pack(side=LEFT, anchor=W)
        self.VRRLabelTxt = StringVar()
        self.VRRLabelEntry = Entry(self.VRRFrame, textvariable=self.VRRLabelTxt, width=25)
        self.VRRLabelEntry.pack(side=RIGHT, anchor=W)

        self.VRRFrameQ1 = Frame(self.OFrame, borderwidth=10)
        self.VRRFrameQ1.pack(side=TOP, anchor=W, fill="x")
        self.VRRLabelQ = Label(self.VRRFrameQ1, text="X. Replica /Q:")
        self.VRRLabelQ.pack(side=LEFT, anchor=W)
        self.VRRFrameQ1Txt = StringVar()
        self.VRRLabelQEntry = Entry(self.VRRFrameQ1, textvariable=self.VRRFrameQ1Txt, width=25)
        self.VRRLabelQEntry.pack(side=RIGHT, anchor=W)

        self.HRRFrame = Frame(self.MFrame, borderwidth=10)
        self.HRRFrame.pack(side=TOP, anchor=W, fill="x")
        self.HRRLabel = Label(self.HRRFrame, text="Y. Replica /MHz:")
        self.HRRLabel.pack(side=LEFT, anchor=W)
        self.HRRLabelTxt = StringVar()
        self.HRRLabelEntry = Entry(self.HRRFrame, textvariable=self.HRRLabelTxt, width=25)
        self.HRRLabelEntry.pack(side=RIGHT, anchor=W)

        self.HRRFrameQ1 = Frame(self.OFrame, borderwidth=10)
        self.HRRFrameQ1.pack(side=TOP, anchor=W, fill="x")
        self.HRRLabelQ = Label(self.HRRFrameQ1, text="Y. Replica /Q:")
        self.HRRLabelQ.pack(side=LEFT, anchor=W)
        self.HRRFrameQ1Txt = StringVar()
        self.HRRLabelQEntry = Entry(self.HRRFrameQ1, textvariable=self.HRRFrameQ1Txt, width=25)
        self.HRRLabelQEntry.pack(side=RIGHT, anchor=W)

        self.ZRRFrame = Frame(self.MFrame, borderwidth=10)
        self.ZRRFrame.pack(side=TOP, anchor=W, fill="x")
        self.ZRRLabel = Label(self.ZRRFrame, text="Z. Replica /MHz:")
        self.ZRRLabel.pack(side=LEFT, anchor=W)
        self.ZRRLabelTxt = StringVar()
        self.ZRRLabelEntry = Entry(self.ZRRFrame, textvariable=self.ZRRLabelTxt, width=25)
        self.ZRRLabelEntry.pack(side=RIGHT, anchor=W)

        self.ZRRFrameQ1 = Frame(self.OFrame, borderwidth=10)
        self.ZRRFrameQ1.pack(side=TOP, anchor=W, fill="x")
        self.ZRRLabelQ = Label(self.ZRRFrameQ1, text="Z. Replica /Q:")
        self.ZRRLabelQ.pack(side=LEFT, anchor=W)
        self.ZRRFrameQ1Txt = StringVar()
        self.ZRRLabelQEntry = Entry(self.ZRRFrameQ1, textvariable=self.ZRRFrameQ1Txt, width=25)
        self.ZRRLabelQEntry.pack(side=RIGHT, anchor=W)

        ##################################
        #GUI FOR EMPTY RESULTS 3
        self.VERFrame2 = Frame(self.MFrame, borderwidth=10)  # create a frame for measurement setup
        self.VERFrame2.pack(side=TOP, anchor=W, fill="x")  #
        self.VERLabel2 = Label(self.VERFrame2, text="X2. empty /MHz:")
        self.VERLabel2.pack(side=LEFT, anchor=W)
        self.VERLabel2Txt = StringVar()
        self.VERLabel2Entry = Entry(self.VERFrame2, textvariable=self.VERLabel2Txt, width=25)
        self.VERLabel2Entry.pack(side=RIGHT, anchor=W)

        self.VERFrameQ2 = Frame(self.OFrame, borderwidth=10)
        self.VERFrameQ2.pack(side=TOP, anchor=W, fill="x")
        self.VERLabelQ2 = Label(self.VERFrameQ2, text="X2. empty /Q:")
        self.VERLabelQ2.pack(side=LEFT, anchor=W)
        self.VERFrameQ2Txt = StringVar()
        self.VERLabelQEntry2 = Entry(self.VERFrameQ2, textvariable=self.VERFrameQ2Txt, width=25)
        self.VERLabelQEntry2.pack(side=RIGHT, anchor=W)

        self.HERFrame2 = Frame(self.MFrame, borderwidth=10)
        self.HERFrame2.pack(side=TOP, anchor=W, fill="x")
        self.HERLabel2 = Label(self.HERFrame2, text="Y2. empty /MHz:")
        self.HERLabel2.pack(side=LEFT, anchor=W)
        self.HERLabel2Txt = StringVar()
        self.HERLabel2Entry = Entry(self.HERFrame2, textvariable=self.HERLabel2Txt, width=25)
        self.HERLabel2Entry.pack(side=RIGHT, anchor=W)

        self.HERFrameQ2 = Frame(self.OFrame, borderwidth=10)
        self.HERFrameQ2.pack(side=TOP, anchor=W, fill="x")
        self.HERLabelQ2 = Label(self.HERFrameQ2, text="Y2. empty /Q:")
        self.HERLabelQ2.pack(side=LEFT, anchor=W)
        self.HERFrameQ2Txt = StringVar()
        self.HERLabelQEntry2 = Entry(self.HERFrameQ2, textvariable=self.HERFrameQ2Txt, width=25)
        self.HERLabelQEntry2.pack(side=RIGHT, anchor=W)

        self.ZERFrame2 = Frame(self.MFrame, borderwidth=10)
        self.ZERFrame2.pack(side=TOP, anchor=W, fill="x")
        self.ZERLabel2 = Label(self.ZERFrame2, text="Z2. empty /MHz:")
        self.ZERLabel2.pack(side=LEFT, anchor=W)
        self.ZERLabel2Txt = StringVar()
        self.ZERLabel2Entry = Entry(self.ZERFrame2, textvariable=self.ZERLabel2Txt, width=25)
        self.ZERLabel2Entry.pack(side=RIGHT, anchor=W)

        self.ZERFrameQ2 = Frame(self.OFrame, borderwidth=10)
        self.ZERFrameQ2.pack(side=TOP, anchor=W, fill="x")
        self.ZERLabelQ2 = Label(self.ZERFrameQ2, text="Z2. empty /Q:")
        self.ZERLabelQ2.pack(side=LEFT, anchor=W)
        self.ZERFrameQ2Txt = StringVar()
        self.ZERLabelQEntry2 = Entry(self.ZERFrameQ2, textvariable=self.ZERFrameQ2Txt, width=25)
        self.ZERLabelQEntry2.pack(side=RIGHT, anchor=W)
        ##########################

        # Temperature display
        self.TempFrame = Frame(self.tab2, borderwidth=10)  # create a frame
        self.TempFrame.pack(side=TOP, anchor=W, fill="x")  #
        self.TempLabel = Label(self.TempFrame, text="Temperature (C): ")
        self.TempLabel.pack(side=TOP, anchor=W)
        self.TempLabelTxt = StringVar()
        self.TempLabelEntry = Entry(self.TempFrame, textvariable=self.TempLabelTxt, width=25)
        self.TempLabelEntry.pack(side=TOP, anchor=W)

        #dielectic output
        self.DielectricResultFrame = Frame(self.tab2, borderwidth=10)  # create a frame comments
        self.DielectricResultFrame.pack(side=TOP, anchor=W, fill="x")  #
        self.DielectricResultLabel = Label(self.DielectricResultFrame, text="Dielectric permittivity of Material:")
        self.DielectricResultLabel.pack(side=TOP, anchor=W)
        self.DielectricResultLabelTxt = StringVar()
        self.DielectricResultEntry = Entry(self.DielectricResultFrame, textvariable=self.DielectricResultLabelTxt, width=50)
        self.DielectricResultEntry.pack(side=TOP, anchor=W)

        # Comment
        self.CommentFrame = Frame(self.tab2, borderwidth=10)  # create a frame comments
        self.CommentFrame.pack(side=TOP, anchor=W, fill="x")  #
        self.CommentLabel = Label(self.CommentFrame, text="Comments:")
        self.CommentLabel.pack(side=TOP, anchor=W)
        self.CommentBox = Text(self.CommentFrame, height=4, width=50)
        self.CommentBox.pack(side=TOP, anchor=W)

        # VS1 - SAMPLE
        self.VS1Frame = Frame(self.tab1, borderwidth=10)  # create a frame comments
        self.VS1Frame.pack(side=TOP, anchor=W, fill="x")  #
        self.VS1Label = Label(self.VS1Frame, text="Volume of sample (cm³):")
        self.VS1Label.pack(side=TOP, anchor=W)
        self.VS1LabelTxt = StringVar()
        self.VS1LabelEntry = Entry(self.VS1Frame, textvariable=self.VS1LabelTxt, width=25)
        self.VS1LabelEntry.pack(side=TOP, anchor=W)

        # VS2 - Replica
        self.VS2Frame = Frame(self.tab1, borderwidth=10)  # create a frame comments
        self.VS2Frame.pack(side=TOP, anchor=W, fill="x")  #
        self.VS2Label = Label(self.VS2Frame, text="Volume of replica (cm³):")
        self.VS2Label.pack(side=TOP, anchor=W)
        self.VS2LabelTxt = StringVar()
        self.VS2LabelEntry = Entry(self.VS2Frame, textvariable=self.VS2LabelTxt, width=25)
        self.VS2LabelEntry.pack(side=TOP, anchor=W)

        # VS2 - Replica Permittivity
        self.VS2PFrame = Frame(self.tab1, borderwidth=10)  # create a frame comments
        self.VS2PFrame.pack(side=TOP, anchor=W, fill="x")  #
        self.VS2PLabel = Label(self.VS2PFrame, text="Permittivity of replica (x-yj):")
        self.VS2PLabel.pack(side=TOP, anchor=W)
        self.VS2PLabelTxt = StringVar()
        self.VS2PLabelEntry = Entry(self.VS2PFrame, textvariable=self.VS2PLabelTxt, width=25)
        self.VS2PLabelEntry.pack(side=TOP, anchor=W)
        # Buttons
        self.ButtonFrame = Frame(self.tab2, borderwidth=10)  # create the frame for the control buttons
        self.ButtonFrame.pack(side=TOP, anchor=W, fill="x")

        self.ButtonFrame1 = Frame(self.tab1, borderwidth=10)  # create the frame for the control buttons
        self.ButtonFrame1.pack(side=TOP, anchor=W, fill="x")

        self.QuitButton1 = Button(self.ButtonFrame1, text="QUIT", command=self.terminate)
        self.QuitButton1.pack(side=LEFT)

        self.QuitButton = Button(self.ButtonFrame, text="QUIT", command=self.terminate)
        self.QuitButton.pack(side=LEFT)

        self.ComfirmButton = Button(self.ButtonFrame1, text="Confirm Parameters", command=self.comfirm)
        self.ComfirmButton.pack(side=LEFT)

        self.runButton = Button(self.ButtonFrame, text="RUN", command=self.run)
        self.runButton.pack(side=LEFT)

        self.reportButton = Button(self.ButtonFrame, text="CREATE REPORT", command=self.create_report)
        self.reportButton.pack(side=LEFT)

        self.newButton = Button(self.ButtonFrame, text="NEW MEASUREMENT", command=self.new_measurement)
        self.newButton.pack(side=LEFT)
        #progress bar
        self.progress = Progressbar(self.ButtonFrame, orient=HORIZONTAL, length=100)
        self.progress.pack(side=RIGHT)
        self.progress.config(mode='determinate', maximum=100, value=5)
        self.progress['value'] = 0
        self.retrieve_parameters()

        self.root.wm_title("DRM Measurement Facility")
        self.root.mainloop()

    def terminate(self):
        self.root.destroy()
        sys.exit()

    def new_measurement(self):

        # Frequency Displays:
        ##################################
        # GUI FOR EMPTY RESULTS 1
        self.VERLabelEntry.delete(0, 'end')
        self.VERLabelQEntry.delete(0, 'end')
        self.HERLabelEntry.delete(0, 'end')
        self.HERLabelQEntry.delete(0, 'end')
        self.ZERLabelEntry.delete(0, 'end')
        self.ZERLabelQEntry.delete(0, 'end')
        ##################################
        # GUI FOR SAMPLE RESULTS
        self.VSRLabelEntry.delete(0, 'end')
        self.VSRLabelQEntry.delete(0, 'end')
        self.HSRLabelEntry.delete(0, 'end')
        self.HSRLabelQEntry.delete(0, 'end')
        self.ZSRLabelEntry.delete(0, 'end')
        self.ZSRLabelQEntry.delete(0, 'end')
        ##################################
        # GUI FOR EMPTY RESULTS 2
        self.VERLabel1Entry.delete(0, 'end')
        self.VERLabel1QEntry.delete(0, 'end')
        self.HERLabel1Entry.delete(0, 'end')
        self.HERLabelQ1Entry.delete(0, 'end')
        self.ZERLabel1Entry.delete(0, 'end')
        self.ZERLabelQ1Entry.delete(0, 'end')
        ##################################
        # GUI FOR REPLICA RESULTS
        self.VRRLabelEntry.delete(0, 'end')
        self.VRRLabelQEntry.delete(0, 'end')
        self.HRRLabelEntry.delete(0, 'end')
        self.HRRLabelQEntry.delete(0, 'end')
        self.ZRRLabelEntry.delete(0, 'end')
        self.ZRRLabelQEntry.delete(0, 'end')
        ##################################
        # GUI FOR EMPTY RESULTS 3
        self.VERLabel2Entry.delete(0, 'end')
        self.VERLabelQEntry2.delete(0, 'end')
        self.HERLabel2Entry.delete(0, 'end')
        self.HERLabelQEntry2.delete(0, 'end')
        self.ZERLabel2Entry.delete(0, 'end')
        self.ZERLabelQEntry2.delete(0, 'end')
        ##########################
        # Temperature display
        self.TempLabelEntry.delete(0, 'end')
        # dielectric output
        self.DielectricResultEntry.delete(0, 'end')
        #DRM RESET RESULTS
        self.VS1LabelEntry.delete(0, 'end')
        # VS2 - Replica
        self.VS2LabelEntry.delete(0, 'end')
        # VS2 - Replica Permittivity
        self.VS2PLabelEntry.delete(0, 'end')
        self.retrieve_parameters()

        self.nb.select(self.tab1)

    def comfirm(self):
        self.nb.select(self.tab2)
        self.ENA.vs1 = float(self.VS1LabelEntry.get())
        self.ENA.vs2 = float(self.VS2LabelEntry.get())
        self.ENA.e_star2 = complex(self.VS2PLabelEntry.get())

    def x_axis(self):
        self.ENA.Arduino_Serial.open()
        time.sleep(2)
        self.mode = 0
        self.ENA.Arduino_Serial.write(bytes(str(self.mode), 'utf-8'))
        time.sleep(5)
        self.ENA.Arduino_Serial.close()
        if self.ENA.MeasurementNum == 0:
            self.ENA.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %G' % (5.0))  ## 10 too high, as performance at this level is not specified. 7.0 is the max without this error
            self.ENA.write('CONF "FILT:TRAN"; *WAI')
            self.ENA.write('DISP:ANN:FREQ:MODE SSTOP')
            self.ENA.write(':SENS:FREQ:STAR 1300 MHz;*WAI')
            self.ENA.write(':SENS:FREQ:STOP 1500 MHz;*WAI')
            self.ENA.write(':CALC:MARK:BWID -3')
            self.ENA.write(':SENSe:SWEep:POINts 201')
            time.sleep(10)
            self.ENA.write('DISP:WIND:TRAC:Y:AUTO ONCE;*WAI')
            self.ENA.write(':CALCulate:MARKer:FUNCtion:TRACking 1')
            self.results = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
            self.BWID = round(self.results[0], -3) * 1.05
            self.ENA.write(':SENSe:FREQuency:SPAN %d' % (self.BWID))
            self.ENA.write('SENS:FREQ:CENT %s' % (self.results[1]))
        self.ENA.write('DISP:ANN:FREQ:MODE SSTOP')
        self.ENA.write(':SENS:FREQ:STAR 1300 MHz;*WAI')
        self.ENA.write(':SENS:FREQ:STOP 1500 MHz;*WAI')
        time.sleep(10)
        self.ENA.write('DISP:WIND:TRAC:Y:AUTO ONCE;*WAI')
        self.ENA.write(':CALCulate:MARKer:FUNCtion:TRACking 1')
        self.results = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
        self.BWID = round(self.results[0], -3) * 1.05
        self.ENA.write(':SENSe:FREQuency:SPAN %d' % (self.BWID))
        self.ENA.write('SENS:FREQ:CENT %s' % (self.results[1]))
        print("x")
        print(self.results)
        time.sleep(5)
        if self.ENA.ChamberState == 'e':

            #Empty 1
            if self.ENA.MeasurementNum == 0:
                peak_dataX = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
                DRM.XEFreq = peak_dataX[1]/1000000
                DRM.XEQ1 = peak_dataX[2]
                self.ENA.MeasurementTime[0] = time.time()
            #Empty 2
            elif self.ENA.MeasurementNum == 1:
                peak_dataX1 = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
                DRM.XEFreq1 = peak_dataX1[1]/1000000
                DRM.XEQ2 = peak_dataX1[2]
                self.ENA.MeasurementTime[6] = time.time()
            #Empty 3
            elif self.ENA.MeasurementNum == 2:
                peak_dataX2 = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
                DRM.XEFreq2 = peak_dataX2[1]/1000000
                DRM.XEQ3 = peak_dataX2[2]
                self.ENA.MeasurementTime[12] = time.time()

        #REPLICA
        elif self.ENA.ChamberState == 'r':
            peak_dataXR = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
            DRM.XRFreq = peak_dataXR[1]/1000000
            DRM.XRQ = peak_dataXR[2]
            self.ENA.MeasurementTime[9] = time.time()

        #SPECIMEN
        elif self.ENA.ChamberState == 's':
            peak_dataXS = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
            DRM.XSFreq = peak_dataXS[1]/1000000
            DRM.XSQ = peak_dataXS[2]
            self.ENA.MeasurementTime[3] = time.time()


    def y_axis(self):
        self.ENA.Arduino_Serial.open()
        time.sleep(3)
        self.mode = 1
        self.ENA.Arduino_Serial.write(bytes(str(self.mode), 'utf-8'))
        time.sleep(5)
        self.ENA.Arduino_Serial.close()
        self.ENA.write('DISP:ANN:FREQ:MODE SSTOP')
        self.ENA.write(':SENS:FREQ:STAR 1300 MHz;*WAI')
        self.ENA.write(':SENS:FREQ:STOP 1500 MHz;*WAI')
        time.sleep(10)
        self.ENA.write('DISP:WIND:TRAC:Y:AUTO ONCE;*WAI')
        self.ENA.write(':CALCulate:MARKer:FUNCtion:TRACking 1')
        self.results = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
        self.BWID = round(self.results[0], -3) * 1.05
        self.ENA.write(':SENSe:FREQuency:SPAN %d' % (self.BWID))
        self.ENA.write('SENS:FREQ:CENT %s' % (self.results[1]))
        print("y")
        print(self.results)
        time.sleep(5)
        if self.ENA.ChamberState == 'e':

            #Empty 1
            if self.ENA.MeasurementNum == 0:
                peak_dataY = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
                DRM.YEFreq = peak_dataY[1]/1000000
                DRM.YEQ1 = peak_dataY[2]
                self.ENA.MeasurementTime[1] = time.time()

            #Empty 2
            if self.ENA.MeasurementNum == 1:
                peak_dataY1 = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
                DRM.YEFreq1 = peak_dataY1[1]/1000000
                DRM.YEQ2 = peak_dataY1[2]
                self.ENA.MeasurementTime[7] = time.time()

            #Empty 3
            elif self.ENA.MeasurementNum == 2:
                peak_dataY2 = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
                DRM.YEFreq2 = peak_dataY2[1]/1000000
                DRM.YEQ3 = peak_dataY2[2]
                self.ENA.MeasurementTime[13] = time.time()

        #REPLICA
        if self.ENA.ChamberState == 'r':
            peak_dataYR = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
            DRM.YRFreq = peak_dataYR[1]/1000000
            DRM.YRQ = peak_dataYR[2]
            self.ENA.MeasurementTime[10] = time.time()

        #SPECIMEN
        elif self.ENA.ChamberState == 's':
            peak_dataYS = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
            DRM.YSFreq = peak_dataYS[1]/1000000
            DRM.YSQ = peak_dataYS[2]
            self.ENA.MeasurementTime[4] = time.time()

    def z_axis(self):
        self.ENA.Arduino_Serial.open()
        time.sleep(3)
        self.mode = 2
        self.ENA.Arduino_Serial.write(bytes(str(self.mode), 'utf-8'))
        time.sleep(5)
        self.ENA.Arduino_Serial.close()
        self.ENA.write('DISP:ANN:FREQ:MODE SSTOP')
        self.ENA.write(':SENS:FREQ:STAR 1300 MHz;*WAI')
        self.ENA.write(':SENS:FREQ:STOP 1500 MHz;*WAI')
        time.sleep(10)
        self.ENA.write('DISP:WIND:TRAC:Y:AUTO ONCE;*WAI')
        self.ENA.write(':CALCulate:MARKer:FUNCtion:TRACking 1')
        self.results = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
        self.BWID = round(self.results[0], -3) * 1.05
        self.ENA.write(':SENSe:FREQuency:SPAN %d' % (self.BWID))
        self.ENA.write('SENS:FREQ:CENT %s' % (self.results[1]))
        print("z")
        print(self.results)
        time.sleep(5)


        if self.ENA.ChamberState == 'e':

            # Empty 1
            if self.ENA.MeasurementNum == 0:
                peak_dataZ = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
                DRM.ZEFreq = peak_dataZ[1]/1000000
                DRM.ZEQ1 = peak_dataZ[2]
                self.ENA.MeasurementNum += 1
                self.ENA.MeasurementTime[2] = time.time()

            # Empty 2
            elif self.ENA.MeasurementNum == 1:
                peak_dataZ1 = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
                DRM.ZEFreq1 = peak_dataZ1[1]/1000000
                DRM.ZEQ2 = peak_dataZ1[2]
                self.ENA.MeasurementNum += 1
                self.ENA.MeasurementTime[8] = time.time()

            # Empty 3
            elif self.ENA.MeasurementNum == 2:
                peak_dataZ2 = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
                DRM.ZEFreq2 = peak_dataZ2[1]/1000000
                DRM.ZEQ3 = peak_dataZ2[2]
                self.ENA.MeasurementNum += 1
                self.ENA.MeasurementTime[14] = time.time()

        # REPLICA
        elif self.ENA.ChamberState == 'r':
            peak_dataZR = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
            DRM.ZRFreq = peak_dataZR[1]/1000000
            DRM.ZRQ = peak_dataZR[2]
            self.ENA.MeasurementTime[11] = time.time()

        # SPECIMEN
        elif self.ENA.ChamberState == 's':
            peak_dataZS = self.ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
            DRM.ZSFreq = peak_dataZS[1]/1000000
            DRM.ZSQ = peak_dataZS[2]
            self.ENA.MeasurementTime[5] = time.time()

    def TempRead(self):
        while True:
            try:  # Attempt to read the temperature
                self.ENA.Arduino_Serial.open()
                time.sleep(2)
                self.mode = 3
                self.ENA.Arduino_Serial.write(bytes(str(self.mode), 'utf-8'))
                time.sleep(5)
                temp_data = self.ENA.Arduino_Serial.readline().decode('utf-8')  # deg. C
                temp_data = re.sub("[^0-9.]", "", temp_data)
                time.sleep(2)
                self.ENA.Arduino_Serial.close()
                DRM.temperature = temp_data[:5]
                DRM.humidity = temp_data[-5:]
            except:  # If failed, set reading to Not Read
                msgbox = messagebox.askyesno('Temperature read failed', 'Do you want to try and read again?')
                if msgbox == False:
                    self.manual = simpledialog.askstring("Manual input", "Please enter temperature manually")
                    if self.manual == None or self.manual == "":
                        DRM.temperature = ("Not Read")
                    else:
                        DRM.temperature(self.manual)
                    break


    def run(self):
        self.root.update_idletasks()
        msgbox = messagebox.showwarning('WARNING', 'EMPTY CAVITY')
        if msgbox == 'ok':
            self.ENA.ChamberState = 'e'
            self.x_axis()
            self.progress['value'] = 6.66
            self.VERLabelEntry.insert(0, str(DRM.XEFreq))
            self.VERLabelQEntry.insert(0, str(DRM.XEQ1))
            self.y_axis()
            self.progress['value'] = 6.66*2
            self.HERLabelEntry.insert(0, str(DRM.YEFreq))
            self.HERLabelQEntry.insert(0, str(DRM.YEQ1))
            self.z_axis()
            self.progress['value'] = 6.66*3
            self.ZERLabelEntry.insert(0, str(DRM.ZEFreq))
            self.ZERLabelQEntry.insert(0, str(DRM.ZEQ1))
        msgbox = messagebox.showwarning('WARNING',  'PLACE ORIGINAL IN CAVITY')
        if msgbox == 'ok':
            self.ENA.ChamberState = 's'
            self.x_axis()
            self.progress['value'] = 6.66*4
            self.VSRLabelQEntry.insert(0, str(DRM.XSQ))
            self.VSRLabelEntry.insert(0, str(DRM.XSFreq))
            self.y_axis()
            self.progress['value'] = 6.66 * 5
            self.HSRLabelEntry.insert(0, str(DRM.YSFreq))
            self.HSRLabelQEntry.insert(0, str(DRM.YSQ))
            self.z_axis()
            self.progress['value'] = 6.66 * 6
            self.ZSRLabelEntry.insert(0, str(DRM.ZSFreq))
            self.ZSRLabelQEntry.insert(0, str(DRM.ZSQ))
        msgbox = messagebox.showwarning('WARNING',  'EMPTY CAVITY')
        if msgbox == 'ok':
            self.ENA.ChamberState = 'e'
            self.x_axis()
            self.progress['value'] = 6.66 * 7
            self.VERLabel1Entry.insert(0, str(DRM.XEFreq1))
            self.VERLabel1QEntry.insert(0, str(DRM.XEQ2))
            self.y_axis()
            self.progress['value'] = 6.66 * 8
            self.HERLabel1Entry.insert(0, str(DRM.YEFreq1))
            self.HERLabelQ1Entry.insert(0, str(DRM.YEQ2))
            self.z_axis()
            self.progress['value'] = 6.66 * 9
            self.ZERLabelQ1Entry.insert(0, str(DRM.ZEQ2))
            self.ZERLabel1Entry.insert(0, str(DRM.ZEFreq1))
        msgbox = messagebox.showwarning('WARNING',  'PLACE REPLICA IN CAVITY')
        if msgbox == 'ok':
            self.ENA.ChamberState = 'r'
            self.x_axis()
            self.progress['value'] = 6.66 * 10
            self.VRRLabelEntry.insert(0, str(DRM.XRFreq))
            self.VRRLabelQEntry.insert(0, str(DRM.XRQ))
            self.y_axis()
            self.progress['value'] = 6.66 * 11
            self.HRRLabelEntry.insert(0, str(DRM.YRFreq))
            self.HRRLabelQEntry.insert(0, str(DRM.YRQ))
            self.z_axis()
            self.progress['value'] = 6.66 * 12
            self.ZRRLabelEntry.insert(0, str(DRM.ZRFreq))
            self.ZRRLabelQEntry.insert(0, str(DRM.ZRQ))
        msgbox = messagebox.showwarning('WARNING',  'EMPTY CAVITY')
        if msgbox == 'ok':
            self.ENA.ChamberState = 'e'
            self.x_axis()
            self.progress['value'] = 6.66 * 13
            self.VERLabel2Entry.insert(0, str(DRM.XEFreq2))
            self.VERLabelQEntry2.insert(0, str(DRM.XEQ3))
            self.y_axis()
            self.progress['value'] = 6.66 * 14
            self.HERLabel2Entry.insert(0, str(DRM.YEFreq2))
            self.HERLabelQEntry2.insert(0, str(DRM.YEQ3))
            self.z_axis()
            self.progress['value'] = 6.66 * 14.5
            self.ZERLabel2Entry.insert(0, str(DRM.ZEFreq2))
            self.ZERLabelQEntry2.insert(0, str(DRM.ZEQ3))
            self.root.update_idletasks()
        try:
            self.TempRead()
        except:
            time.sleep(0.01)
        DRM.calc(self.ENA)
        self.progress['value'] = 100
        self.DielectricResultEntry.insert(0, str(self.ENA.e_star1))
        self.TempLabelEntry.insert(0, str(self.ENA.temperature))
        self.root.mainloop()

    def show_info(self):
        messagebox.showinfo('Warning', 'unable to retrieve parameters')

    def retrieve_parameters(self):
        dn = open("directory.txt", "r")
        dn_str = dn.readline()
        dirName = dn_str
        if dirName == '':
            i = 0
            while os.path.exists("drm_GUI_analysis%s.txt" % i):
                i += 1
            j = i - 1
            if j == -1:
                print('')
            else:
                fh = open("drm_GUI_analysis%s.txt" % j, "r")
                lines = fh.readlines()
                vs1_str = str(lines[4][15:19])
                vs1_str = re.sub("[^0-9.]", "", vs1_str)
                self.VS1LabelEntry.insert(0, vs1_str)
                vs2_str = str(lines[5][16:20])
                vs2_str = re.sub("[^0-9.]", "", vs2_str)
                self.VS2LabelEntry.insert(0, vs2_str)
                vs2p_str = str(lines[6][23:36])
                vs2p_str = re.sub("[^0-9.-j-]", "", vs2p_str)
                self.VS2PLabelEntry.insert(0, vs2p_str)

        else:
            try:
                # Create target Directory
                os.mkdir(dirName)
            except FileExistsError:
                print('')
            if not os.path.exists(dirName):
                os.mkdir(dirName)
            i = 0
            while os.path.exists(dn_str+"/drm_GUI_analysis%s.txt" % i):
                i += 1
            j = i - 1
            fh = open(dn_str+"/drm_GUI_analysis%s.txt" % j, "r")
            lines = fh.readlines()
            vs1_str = str(lines[4][15:19])
            vs1_str = re.sub("[^0-9.]", "", vs1_str)
            self.VS1LabelEntry.insert(0, vs1_str)
            vs2_str = str(lines[5][16:20])
            vs2_str = re.sub("[^0-9.]", "", vs2_str)
            self.VS2LabelEntry.insert(0, vs2_str)
            vs2p_str = str(lines[6][23:36])
            vs2p_str = re.sub("[^0-9.-j-]", "", vs2p_str)
            self.VS2PLabelEntry.insert(0, vs2p_str)

    def create_report(self):
        j = 0
        self.filename = filedialog.askdirectory()
        fn = open("directory.txt", "w")
        fn.write("%s" % self.filename)
        while os.path.exists(self.filename+"/drm_GUI_analysis%s.txt" % j):
            j+=1
        fh = open(self.filename+"/drm_GUI_analysis%s.txt" % j, "w")
        fh.write("Operating Conditions\n")
        fh.write("%s\n" % datetime.datetime.now())
        try:
            fh.write("Temperature: %s °C\n" % self.ENA.temperature)
            fh.write("Humidity: %s" % self.ENA.humidity)
        except:
            time.sleep(0.1)
        fh.write("%\n")
        fh.write("SAMPLE VOLUME: %s\n" % self.ENA.vs1)
        fh.write("REPLICA VOLUME: %s\n" % self.ENA.vs2)
        fh.write("REPLICA PERMITTIVITY: %s\n" % self.ENA.e_star2)
        fh.write("FREQ EMPTY X1: %s\n" % DRM.XEFreq)
        fh.write("Q EMPTY X1: %s\n" % DRM.XEQ1)
        fh.write("FREQ EMPTY Y1: %s\n" % DRM.YEFreq)
        fh.write("Q EMPTY Y1: %s\n" % DRM.YEQ1)
        fh.write("FREQ EMPTY Z1: %s\n" % DRM.ZEFreq)
        fh.write("Q EMPTY Z1: %s\n" % DRM.ZEQ1)
        fh.write("FREQ SAMPLE X: %s\n" % DRM.XSFreq)
        fh.write("Q SAMPLE X: %s\n" % DRM.XSQ)
        fh.write("FREQ SAMPLE Y: %s\n" % DRM.YSFreq)
        fh.write("Q SAMPLE Y: %s\n" % DRM.YSQ)
        fh.write("FREQ SAMPLE Z: %s\n" % DRM.ZSFreq)
        fh.write("Q SAMPLE Z: %s\n" % DRM.ZSQ)
        fh.write("FREQ EMPTY X2: %s\n" % DRM.XEFreq1)
        fh.write("Q EMPTY X2: %s\n" % DRM.XEQ2)
        fh.write("FREQ EMPTY Y2: %s\n" % DRM.YEFreq1)
        fh.write("Q EMPTY Y2: %s\n" % DRM.YEQ2)
        fh.write("FREQ EMPTY Z2: %s\n" % DRM.ZEFreq1)
        fh.write("Q EMPTY Z2: %s\n" % DRM.ZEQ2)
        fh.write("FREQ REPLICA X: %s\n" % DRM.XRFreq)
        fh.write("Q REPLICA X: %s\n" % DRM.XRQ)
        fh.write("FREQ REPLICA Y: %s\n" % DRM.YRFreq)
        fh.write("Q REPLICA Y: %s\n" % DRM.YRQ)
        fh.write("FREQ REPLICA Z: %s\n" % DRM.ZRFreq)
        fh.write("Q REPLICA Z: %s\n" % DRM.ZRQ)
        fh.write("FREQ EMPTY X3: %s\n" % DRM.XEFreq2)
        fh.write("Q EMPTY X3: %s\n" % DRM.XEQ3)
        fh.write("FREQ EMPTY Y3: %s\n" % DRM.YEFreq2)
        fh.write("Q EMPTY Y3: %s\n" % DRM.YEQ3)
        fh.write("FREQ EMPTY Z3: %s\n" % DRM.ZEFreq2)
        fh.write("Q EMPTY Z3: %s\n" % DRM.ZEQ3)
        fh.write("deltaOmega_x1: %s\n" % self.ENA.deltaOmega_x1)
        fh.write("deltaOmega_y1: %s\n" % self.ENA.deltaOmega_y1)
        fh.write("deltaOmega_z1: %s\n" % self.ENA.deltaOmega_z1)
        fh.write("sig_r_omega1: %s\n" % self.ENA.sig_r_omega1)
        fh.write("deltaOmega_x2: %s\n" % self.ENA.deltaOmega_x2)
        fh.write("deltaOmega_y2: %s\n" % self.ENA.deltaOmega_y2)
        fh.write("deltaOmega_z2: %s\n" % self.ENA.deltaOmega_z2)
        fh.write("sig_r_omega2: %s\n" % self.ENA.sig_r_omega2)
        fh.write("ALPHA1 VOL: %s\n" % self.ENA.alpha1_vol)
        fh.write("ALPHA2 VOL: %s\n" % self.ENA.alpha2_vol)
        fh.write("ALPHA1: %s\n" % self.ENA.alpha1)
        fh.write("PERMITTIVITY OF SAMPLE: %s\n" % self.ENA.e_star1)
        fh.write("LOSS TANGENT OF MATERIAL: %s\n" % self.ENA.tand)
        fh.write("COMMENTS: %s\n" % self.CommentBox.get("1.0", END))
        msgbox = messagebox.showwarning('File Saved', 'drm_GUI_analysis%s.txt' % j)

if __name__ == '__main__':
    gui = GUI()
    # # end of Untitled
