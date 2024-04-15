import pyvisa
import time

rm = pyvisa.ResourceManager()
ENA = rm.open_resource('GPIB0::1::INSTR')
print("works")
ENA.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %G' % (5.0)) ## 10 too high, as performance at this level is not specified. 7.0 is the max without this error
ENA.write('CONF "FILT:TRAN"; *WAI')
ENA.write('DISP:ANN:FREQ:MODE SSTOP')
ENA.write(':SENS:FREQ:STAR 1300 MHz;*WAI')
ENA.write(':SENS:FREQ:STOP 1400 MHz;*WAI')
ENA.write(':CALCulate:MARKer:STATe %d' % (1))
ENA.write(':SENSe:FREQuency:SPAN 200 MHz' )
ENA.write(':SENSe:SWEep:POINts 201' )
time.sleep(15)
ENA.write('DISP:WIND:TRAC:Y:AUTO ONCE;*WAI')
time.sleep(15)
ENA.write(':CALCulate:MARKer:FUNCtion:TRACking 1')
time.sleep(3)
centre = ENA.query('CALC:MARK:X:ABS?')
ENA.write('SENS:FREQ:CENT %s;*WAI' % (centre))
time.sleep(1)
Freq_x = ENA.query_ascii_values(':SENS:FREQuency:CENT?')
print(Freq_x)

BWID_x = ENA.query_ascii_values(':CALCulate:MARKer:BWIDth?')
print(BWID_x)

cent_freq_rnd_x = round(Freq_x[0])
bw_x = BWID_x[0] * 1.05
bw_xf = round(bw_x,-2)
ENA.write(':SENSe:FREQuency:SPAN 50 MHz')
