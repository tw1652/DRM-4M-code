import pyvisa

rm = pyvisa.ResourceManager()
ENA = rm.open_resource('GPIB0::1::INSTR')
print("works")
ENA.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %G' % (7.0)) ## 10 too high, as performance at this level is not specified. 7.0 is the max without this error
ENA.write('CONF "AMPL:TRAN"; *WAI')
ENA.write(':SENS:FREQ:STAR 1300 MHz')
ENA.write(':SENS:FREQ:STOP 1400 MHz')
ENA.write(':CALCulate:MARKer:STATe %d' % (1))
ENA.write(':SENSe:FREQuency:SPAN 200 MHz' )
ENA.write(':SENSe:SWEep:POINts %d' % (1601))
ENA.write(':CALCulate:MARKer:FUNCtion:TRACking %d' % (1))
ENA.write(':TRIGger:SEQuence:SOURce %s' % ('EXTernal'))
ENA.write(':CALCulate1:MARKer:FUNCtion %s;*WAI' % ('MAXimum'))
centre = ENA.query('CALC1:MARK:X:ABS?')
ENA.write('SENS:FREQ:CENT %s;*WAI' % (centre))
ENA.write('SENSe:SWEep:TRIGger:SOURce IMMediate')

operation_status = ENA.query_ascii_values(':STATus:OPERation:CONDition?')
status = int(operation_status[0])
print(operation_status)

Freq_x = ENA.query_ascii_values(':SENS:FREQuency:CENT?')
print(Freq_x)

BWID_x = ENA.query_ascii_values(':CALCulate:MARKer:BWIDth?')
print(BWID_x)



cent_freq_rnd_x = round(Freq_x[0], -3)
bw_x = BWID_x[0] * 1.05
bw_xf = round(bw_x, -3)
# ENA.write(':SENSe:FREQuency:CENTer %G' % (cent_freq_rnd_x))
# ENA.write(':SENSe:BWID:RESolution %G' % (100.0))
# ENA.write(':SENSe:FREQuency:SPAN %G' % (bw_xf))
#ENA.write('SENSe:SWEep:TRIGger:SOURce IMMediate')
