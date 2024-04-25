import pyvisa
import time

rm = pyvisa.ResourceManager()
ENA = rm.open_resource('GPIB0::1::INSTR')
print("works")
ENA.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %G' % (5.0)) ## 10 too high, as performance at this level is not specified. 7.0 is the max without this error
ENA.write('CONF "FILT:TRAN"; *WAI')
ENA.write('DISP:ANN:FREQ:MODE SSTOP')
ENA.write(':SENS:FREQ:STAR 1300 MHz;*WAI')
ENA.write(':SENS:FREQ:STOP 1500 MHz;*WAI')
ENA.write(':CALC:MARK:BWID -3')
ENA.write(':SENSe:SWEep:POINts 201' )
time.sleep(5)
ENA.write('DISP:WIND:TRAC:Y:AUTO ONCE;*WAI')
ENA.write(':CALCulate:MARKer:FUNCtion:TRACking 1')
results = ENA.query_ascii_values(':CALCulate:MARKer:FUNCtion:RESult?')
BWID = round(results[0], -3) * 1.05
ENA.write(':SENSe:FREQuency:SPAN %d' %(BWID))
ENA.write('SENS:FREQ:CENT %s' % (results[1]))
print(results)
