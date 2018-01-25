EESchema Schematic File Version 2
LIBS:commonpart
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:1020-cache
EELAYER 25 0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 1
Title "Incandescent Plank (Gen 2)"
Date "25 jan 2018"
Rev "0"
Comp "Open Pinball Project"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L TST P4
U 1 1 55B18CB8
P 4500 7300
F 0 "P4" H 4500 7600 40  0000 C CNN
F 1 "TST" H 4500 7550 30  0000 C CNN
F 2 "commonlib:00_mtg_hole-2-56" H 4500 7300 60  0001 C CNN
F 3 "~" H 4500 7300 60  0000 C CNN
	1    4500 7300
	1    0    0    -1  
$EndComp
NoConn ~ 4500 7300
$Comp
L Conn_01x22 J1
U 1 1 5A678335
P 10200 3400
F 0 "J1" H 10200 4500 50  0000 C CNN
F 1 "Conn_01x22" H 10200 2200 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x22_Pitch2.54mm" H 10200 3400 50  0001 C CNN
F 3 "" H 10200 3400 50  0001 C CNN
	1    10200 3400
	1    0    0    1   
$EndComp
$Comp
L +5V #PWR01
U 1 1 5A679840
P 9600 2200
F 0 "#PWR01" H 9600 2290 20  0001 C CNN
F 1 "+5V" H 9600 2350 30  0000 C CNN
F 2 "" H 9600 2200 60  0001 C CNN
F 3 "" H 9600 2200 60  0001 C CNN
	1    9600 2200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 5A67AABA
P 9350 2250
F 0 "#PWR02" H 9350 2000 50  0001 C CNN
F 1 "GND" H 9350 2100 50  0000 C CNN
F 2 "" H 9350 2250 50  0001 C CNN
F 3 "" H 9350 2250 50  0001 C CNN
	1    9350 2250
	1    0    0    -1  
$EndComp
Text Label 9800 4000 0    60   ~ 0
P0.0
Text Label 9800 3900 0    60   ~ 0
P0.1
Text Label 9800 3800 0    60   ~ 0
P0.2
Text Label 9800 3700 0    60   ~ 0
P0.3
Text Label 9800 3200 0    60   ~ 0
P1.0
Text Label 9800 3100 0    60   ~ 0
P1.1
Text Label 9800 3000 0    60   ~ 0
P1.2
Text Label 9800 2900 0    60   ~ 0
P1.3
Text Label 9800 3600 0    60   ~ 0
P0.4
Text Label 9800 3500 0    60   ~ 0
P0.5
Text Label 9800 3400 0    60   ~ 0
P0.6
Text Label 9800 3300 0    60   ~ 0
P0.7
Text Label 9800 2800 0    60   ~ 0
P1.4
Text Label 9800 2700 0    60   ~ 0
P1.5
Text Label 9800 2600 0    60   ~ 0
P1.6
Text Label 9800 2500 0    60   ~ 0
P1.7
Text Label 9800 4400 0    60   ~ 0
P4.0
Text Label 9800 4300 0    60   ~ 0
P4.1
Text Label 9800 4200 0    60   ~ 0
P4.2
Text Label 9800 4100 0    60   ~ 0
P4.3
$Comp
L PWR_FLAG #FLG03
U 1 1 5A68DAAF
P 9800 2200
F 0 "#FLG03" H 9800 2295 30  0001 C CNN
F 1 "PWR_FLAG" H 9800 2380 30  0000 C CNN
F 2 "" H 9800 2200 60  0001 C CNN
F 3 "" H 9800 2200 60  0001 C CNN
	1    9800 2200
	1    0    0    -1  
$EndComp
$Comp
L TST P5
U 1 1 5A690B5C
P 4700 7300
F 0 "P5" H 4700 7600 40  0000 C CNN
F 1 "TST" H 4700 7550 30  0000 C CNN
F 2 "commonlib:00_mtg_hole-2-56" H 4700 7300 60  0001 C CNN
F 3 "~" H 4700 7300 60  0000 C CNN
	1    4700 7300
	1    0    0    -1  
$EndComp
NoConn ~ 4700 7300
$Comp
L TST P6
U 1 1 5A690C29
P 4900 7300
F 0 "P6" H 4900 7600 40  0000 C CNN
F 1 "TST" H 4900 7550 30  0000 C CNN
F 2 "commonlib:00_mtg_hole-2-56" H 4900 7300 60  0001 C CNN
F 3 "~" H 4900 7300 60  0000 C CNN
	1    4900 7300
	1    0    0    -1  
$EndComp
NoConn ~ 4900 7300
$Comp
L TST P7
U 1 1 5A690C30
P 5100 7300
F 0 "P7" H 5100 7600 40  0000 C CNN
F 1 "TST" H 5100 7550 30  0000 C CNN
F 2 "commonlib:00_mtg_hole-2-56" H 5100 7300 60  0001 C CNN
F 3 "~" H 5100 7300 60  0000 C CNN
	1    5100 7300
	1    0    0    -1  
$EndComp
NoConn ~ 5100 7300
Text Label 650  6000 0    60   ~ 0
P4.0
Text Label 650  5900 0    60   ~ 0
P4.1
Text Label 650  5700 0    60   ~ 0
P4.2
$Comp
L CONN_4X2 P1
U 1 1 5A693F87
P 2750 5600
F 0 "P1" H 2750 5850 50  0000 C CNN
F 1 "CONN_4X2" V 2750 5600 40  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x04_Pitch2.54mm" H 2750 5600 60  0001 C CNN
F 3 "" H 2750 5600 60  0000 C CNN
	1    2750 5600
	0    1    1    0   
$EndComp
$Comp
L CONN_4X2 P2
U 1 1 5A693F88
P 2750 7100
F 0 "P2" H 2750 7350 50  0000 C CNN
F 1 "CONN_4X2" V 2750 7100 40  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x04_Pitch2.54mm" H 2750 7100 60  0001 C CNN
F 3 "" H 2750 7100 60  0000 C CNN
	1    2750 7100
	0    1    1    0   
$EndComp
Text Label 950  6000 0    60   ~ 0
RX
Text Label 950  5900 0    60   ~ 0
TX
NoConn ~ 2800 6000
NoConn ~ 2900 6000
NoConn ~ 2800 7500
NoConn ~ 2900 7500
$Comp
L +5V #PWR04
U 1 1 5A693F89
P 2600 4700
F 0 "#PWR04" H 2600 4790 20  0001 C CNN
F 1 "+5V" H 2600 4790 30  0000 C CNN
F 2 "" H 2600 4700 60  0001 C CNN
F 3 "" H 2600 4700 60  0001 C CNN
	1    2600 4700
	1    0    0    -1  
$EndComp
Text Label 950  5700 0    60   ~ 0
SYNCH
$Comp
L +12V1 #PWR05
U 1 1 5A693F8D
P 1500 6200
F 0 "#PWR05" H 1500 6150 20  0001 C CNN
F 1 "+12V1" H 1500 6300 30  0000 C CNN
F 2 "~" H 1500 6200 60  0000 C CNN
F 3 "~" H 1500 6200 60  0000 C CNN
	1    1500 6200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 5A693F8F
P 2300 7800
F 0 "#PWR06" H 2300 7550 50  0001 C CNN
F 1 "GND" H 2300 7650 50  0000 C CNN
F 2 "" H 2300 7800 50  0001 C CNN
F 3 "" H 2300 7800 50  0001 C CNN
	1    2300 7800
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 5A693F91
P 1400 5700
F 0 "R2" V 1300 5700 50  0000 C CNN
F 1 "480" V 1400 5700 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 1330 5700 50  0001 C CNN
F 3 "" H 1400 5700 50  0001 C CNN
	1    1400 5700
	0    1    1    0   
$EndComp
$Comp
L R R3
U 1 1 5A693F92
P 1400 5900
F 0 "R3" V 1300 5900 50  0000 C CNN
F 1 "480" V 1400 5900 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 1330 5900 50  0001 C CNN
F 3 "" H 1400 5900 50  0001 C CNN
	1    1400 5900
	0    1    1    0   
$EndComp
$Comp
L CONN_4 P3
U 1 1 5A693F8A
P 4050 6050
F 0 "P3" V 4000 6050 50  0000 C CNN
F 1 "CONN_4" V 4100 6050 50  0000 C CNN
F 2 "commonlib:00_th1x4x100-lock" H 4050 6050 60  0001 C CNN
F 3 "" H 4050 6050 60  0001 C CNN
F 4 "FCI" H 4050 6050 60  0001 C CNN "Manufacturer"
F 5 "68001-436HLF" H 4050 6050 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4050 6050 60  0001 C CNN "Distributor"
F 7 "649-68001-436HLF" H 4050 6050 60  0001 C CNN "Distributor PN"
	1    4050 6050
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG07
U 1 1 5A698F7E
P 2150 6150
F 0 "#FLG07" H 2150 6245 30  0001 C CNN
F 1 "PWR_FLAG" H 2150 6330 30  0000 C CNN
F 2 "" H 2150 6150 60  0001 C CNN
F 3 "" H 2150 6150 60  0001 C CNN
	1    2150 6150
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 5A69D2DC
P 1400 5500
F 0 "R1" V 1300 5500 50  0000 C CNN
F 1 "0" V 1400 5500 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 1330 5500 50  0001 C CNN
F 3 "" H 1400 5500 50  0001 C CNN
	1    1400 5500
	0    1    1    0   
$EndComp
Text Label 650  5500 0    60   ~ 0
P4.3
Text Notes 750  5300 0    60   ~ 0
R1 only populated if on\nleft side of PSOC4200
$Comp
L MOSFET_N Q1
U 1 1 5A6A07DE
P 4100 2100
F 0 "Q1" H 4110 2270 60  0000 R CNN
F 1 "MOSFET_N" H 4110 1950 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 4100 2100 60  0001 C CNN
F 3 "" H 4100 2100 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 4100 2100 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 4100 2100 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4100 2100 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 4100 2100 60  0001 C CNN "Distributor PN"
	1    4100 2100
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q3
U 1 1 5A6A07E8
P 4800 2100
F 0 "Q3" H 4810 2270 60  0000 R CNN
F 1 "MOSFET_N" H 4810 1950 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 4800 2100 60  0001 C CNN
F 3 "" H 4800 2100 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 4800 2100 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 4800 2100 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4800 2100 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 4800 2100 60  0001 C CNN "Distributor PN"
	1    4800 2100
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q5
U 1 1 5A6A07E9
P 5500 2100
F 0 "Q5" H 5510 2270 60  0000 R CNN
F 1 "MOSFET_N" H 5510 1950 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 5500 2100 60  0001 C CNN
F 3 "" H 5500 2100 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 5500 2100 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 5500 2100 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5500 2100 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 5500 2100 60  0001 C CNN "Distributor PN"
	1    5500 2100
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q7
U 1 1 5A6A07EA
P 6200 2100
F 0 "Q7" H 6210 2270 60  0000 R CNN
F 1 "MOSFET_N" H 6210 1950 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 6200 2100 60  0001 C CNN
F 3 "" H 6200 2100 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 6200 2100 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 6200 2100 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6200 2100 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 6200 2100 60  0001 C CNN "Distributor PN"
	1    6200 2100
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q9
U 1 1 5A6A07EB
P 6900 2100
F 0 "Q9" H 6910 2270 60  0000 R CNN
F 1 "MOSFET_N" H 6910 1950 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 6900 2100 60  0001 C CNN
F 3 "" H 6900 2100 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 6900 2100 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 6900 2100 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6900 2100 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 6900 2100 60  0001 C CNN "Distributor PN"
	1    6900 2100
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q11
U 1 1 5A6A07EC
P 7600 2100
F 0 "Q11" H 7610 2270 60  0000 R CNN
F 1 "MOSFET_N" H 7610 1950 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 7600 2100 60  0001 C CNN
F 3 "" H 7600 2100 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 7600 2100 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 7600 2100 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7600 2100 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 7600 2100 60  0001 C CNN "Distributor PN"
	1    7600 2100
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q13
U 1 1 5A6A07ED
P 8300 2100
F 0 "Q13" H 8310 2270 60  0000 R CNN
F 1 "MOSFET_N" H 8310 1950 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 8300 2100 60  0001 C CNN
F 3 "" H 8300 2100 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 8300 2100 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 8300 2100 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 8300 2100 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 8300 2100 60  0001 C CNN "Distributor PN"
	1    8300 2100
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q15
U 1 1 5A6A07EE
P 9000 2100
F 0 "Q15" H 9010 2270 60  0000 R CNN
F 1 "MOSFET_N" H 9010 1950 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 9000 2100 60  0001 C CNN
F 3 "" H 9000 2100 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 9000 2100 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 9000 2100 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 9000 2100 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 9000 2100 60  0001 C CNN "Distributor PN"
	1    9000 2100
	1    0    0    -1  
$EndComp
$Comp
L spade_187 P11
U 1 1 5A6A5CCA
P 10000 5000
F 0 "P11" H 10000 5100 40  0000 C CNN
F 1 "SPADE_187" H 10000 5000 40  0000 C CNN
F 2 "commonlib:00_th1x2x200" H 10000 5000 60  0001 C CNN
F 3 "" H 10000 5000 60  0001 C CNN
F 4 "Keystone" H 10000 5000 60  0001 C CNN "Manufacturer"
F 5 "1285" H 10000 5000 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 10000 5000 60  0001 C CNN "Distributor"
F 7 "534-1285" H 10000 5000 60  0001 C CNN "Distributor PN"
	1    10000 5000
	1    0    0    -1  
$EndComp
$Comp
L CONN_2 P10
U 1 1 5A6A5CD3
P 9650 6000
F 0 "P10" V 9600 6000 40  0000 C CNN
F 1 "CONN_2" V 9700 6000 40  0000 C CNN
F 2 "commonlib:00_th1x2x4.2mm_cheap" H 9650 6000 60  0001 C CNN
F 3 "" H 9650 6000 60  0000 C CNN
	1    9650 6000
	1    0    0    -1  
$EndComp
$Comp
L CONN_8 P8
U 1 1 5A6A5F0E
P 9550 1350
F 0 "P8" V 9500 1350 60  0000 C CNN
F 1 "CONN_8" V 9600 1350 60  0000 C CNN
F 2 "commonlib:00_th1x8x100-lock" H 9550 1350 60  0001 C CNN
F 3 "" H 9550 1350 60  0000 C CNN
	1    9550 1350
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q2
U 1 1 5A6A87F5
P 4100 5400
F 0 "Q2" H 4110 5570 60  0000 R CNN
F 1 "MOSFET_N" H 4110 5250 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 4100 5400 60  0001 C CNN
F 3 "" H 4100 5400 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 4100 5400 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 4100 5400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4100 5400 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 4100 5400 60  0001 C CNN "Distributor PN"
	1    4100 5400
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q4
U 1 1 5A6A87FF
P 4800 5400
F 0 "Q4" H 4810 5570 60  0000 R CNN
F 1 "MOSFET_N" H 4810 5250 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 4800 5400 60  0001 C CNN
F 3 "" H 4800 5400 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 4800 5400 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 4800 5400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4800 5400 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 4800 5400 60  0001 C CNN "Distributor PN"
	1    4800 5400
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q6
U 1 1 5A6A8809
P 5500 5400
F 0 "Q6" H 5510 5570 60  0000 R CNN
F 1 "MOSFET_N" H 5510 5250 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 5500 5400 60  0001 C CNN
F 3 "" H 5500 5400 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 5500 5400 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 5500 5400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5500 5400 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 5500 5400 60  0001 C CNN "Distributor PN"
	1    5500 5400
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q8
U 1 1 5A6A8813
P 6200 5400
F 0 "Q8" H 6210 5570 60  0000 R CNN
F 1 "MOSFET_N" H 6210 5250 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 6200 5400 60  0001 C CNN
F 3 "" H 6200 5400 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 6200 5400 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 6200 5400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6200 5400 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 6200 5400 60  0001 C CNN "Distributor PN"
	1    6200 5400
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q10
U 1 1 5A6A881D
P 6900 5400
F 0 "Q10" H 6910 5570 60  0000 R CNN
F 1 "MOSFET_N" H 6910 5250 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 6900 5400 60  0001 C CNN
F 3 "" H 6900 5400 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 6900 5400 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 6900 5400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6900 5400 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 6900 5400 60  0001 C CNN "Distributor PN"
	1    6900 5400
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q12
U 1 1 5A6A8827
P 7600 5400
F 0 "Q12" H 7610 5570 60  0000 R CNN
F 1 "MOSFET_N" H 7610 5250 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 7600 5400 60  0001 C CNN
F 3 "" H 7600 5400 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 7600 5400 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 7600 5400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7600 5400 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 7600 5400 60  0001 C CNN "Distributor PN"
	1    7600 5400
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q14
U 1 1 5A6A8831
P 8300 5400
F 0 "Q14" H 8310 5570 60  0000 R CNN
F 1 "MOSFET_N" H 8310 5250 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 8300 5400 60  0001 C CNN
F 3 "" H 8300 5400 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 8300 5400 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 8300 5400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 8300 5400 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 8300 5400 60  0001 C CNN "Distributor PN"
	1    8300 5400
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q16
U 1 1 5A6A883B
P 9000 5400
F 0 "Q16" H 9010 5570 60  0000 R CNN
F 1 "MOSFET_N" H 9010 5250 60  0000 R CNN
F 2 "commonlib:00_to92_dgs" H 9000 5400 60  0001 C CNN
F 3 "" H 9000 5400 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 9000 5400 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 9000 5400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 9000 5400 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 9000 5400 60  0001 C CNN "Distributor PN"
	1    9000 5400
	1    0    0    -1  
$EndComp
$Comp
L CONN_8 P9
U 1 1 5A6AB397
P 9550 4650
F 0 "P9" V 9500 4650 60  0000 C CNN
F 1 "CONN_8" V 9600 4650 60  0000 C CNN
F 2 "commonlib:00_th1x8x100-lock" H 9550 4650 60  0001 C CNN
F 3 "" H 9550 4650 60  0000 C CNN
	1    9550 4650
	1    0    0    1   
$EndComp
$Comp
L GNDPWR #PWR08
U 1 1 5A6B21EE
P 10100 5800
F 0 "#PWR08" H 10100 5600 50  0001 C CNN
F 1 "GNDPWR" H 10100 5670 50  0000 C CNN
F 2 "" H 10100 5750 50  0001 C CNN
F 3 "" H 10100 5750 50  0001 C CNN
	1    10100 5800
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG09
U 1 1 5A6B312B
P 9700 5500
F 0 "#FLG09" H 9700 5595 30  0001 C CNN
F 1 "PWR_FLAG" H 9700 5680 30  0000 C CNN
F 2 "" H 9700 5500 60  0001 C CNN
F 3 "" H 9700 5500 60  0001 C CNN
	1    9700 5500
	1    0    0    -1  
$EndComp
$Comp
L GNDPWR #PWR010
U 1 1 5A6B46C9
P 3900 2500
F 0 "#PWR010" H 3900 2300 50  0001 C CNN
F 1 "GNDPWR" H 3900 2370 50  0000 C CNN
F 2 "" H 3900 2450 50  0001 C CNN
F 3 "" H 3900 2450 50  0001 C CNN
	1    3900 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	9600 2200 9600 2300
Wire Wire Line
	9600 2300 10000 2300
Wire Wire Line
	10000 2400 9500 2400
Wire Wire Line
	9500 2400 9500 2100
Wire Wire Line
	9500 2100 9350 2100
Wire Wire Line
	9800 2200 9800 2300
Connection ~ 9800 2300
Wire Wire Line
	2800 5200 2800 4900
Wire Wire Line
	2000 4900 3500 4900
Wire Wire Line
	2000 6000 2000 4900
Wire Wire Line
	2900 6700 2900 6600
Wire Wire Line
	2900 6600 3100 6600
Wire Wire Line
	3100 6600 3100 5100
Wire Wire Line
	3100 5100 2900 5100
Wire Wire Line
	2900 5100 2900 5200
Wire Wire Line
	2400 5900 2400 6400
Wire Wire Line
	2800 6400 2800 6700
Wire Wire Line
	2700 5200 2700 5000
Wire Wire Line
	2700 5000 2300 5000
Wire Wire Line
	2300 5000 2300 7800
Wire Wire Line
	2700 6700 2700 6500
Wire Wire Line
	2700 6500 2300 6500
Connection ~ 2300 6500
Wire Wire Line
	2600 4700 2600 5200
Wire Wire Line
	2600 5100 2500 5100
Wire Wire Line
	2500 5100 2500 6600
Wire Wire Line
	2500 6600 2600 6600
Wire Wire Line
	2600 6600 2600 6700
Connection ~ 2600 5100
Wire Wire Line
	2700 6000 2700 6300
Wire Wire Line
	2700 6300 1800 6300
Wire Wire Line
	1800 5700 1800 7700
Wire Wire Line
	2600 6200 2600 6000
Wire Wire Line
	1500 6200 2600 6200
Wire Wire Line
	1900 7600 2600 7600
Wire Wire Line
	2600 7600 2600 7500
Connection ~ 1900 6200
Wire Wire Line
	1800 7700 2700 7700
Wire Wire Line
	2700 7700 2700 7500
Connection ~ 1800 6300
Wire Wire Line
	1550 5900 2400 5900
Wire Wire Line
	1550 5700 1800 5700
Wire Wire Line
	3500 6000 3700 6000
Connection ~ 2800 4900
Wire Wire Line
	3500 4900 3500 6000
Wire Wire Line
	3100 5900 3700 5900
Wire Wire Line
	1900 6200 1900 7600
Connection ~ 2300 6100
Wire Wire Line
	2300 6100 3700 6100
Connection ~ 2600 4800
Wire Wire Line
	2600 4800 3400 4800
Wire Wire Line
	3400 4800 3400 6200
Wire Wire Line
	3400 6200 3700 6200
Connection ~ 3100 5900
Wire Wire Line
	2400 6400 2800 6400
Wire Wire Line
	650  5700 1250 5700
Wire Wire Line
	650  5900 1250 5900
Wire Wire Line
	650  6000 2000 6000
Wire Wire Line
	10000 4100 9800 4100
Wire Wire Line
	10000 4200 9800 4200
Wire Wire Line
	10000 4300 9800 4300
Wire Wire Line
	10000 4400 9800 4400
Wire Wire Line
	2150 6150 2150 6200
Connection ~ 2150 6200
Wire Wire Line
	2300 5500 1550 5500
Connection ~ 2300 5500
Wire Wire Line
	650  5500 1250 5500
Wire Wire Line
	3600 2100 3900 2100
Wire Wire Line
	4300 2100 4600 2100
Wire Wire Line
	5000 2100 5300 2100
Wire Wire Line
	5700 2100 6000 2100
Wire Wire Line
	6400 2100 6700 2100
Wire Wire Line
	7100 2100 7400 2100
Wire Wire Line
	7800 2100 8100 2100
Wire Wire Line
	8500 2100 8800 2100
Wire Wire Line
	4200 1000 4200 1900
Wire Wire Line
	4900 1100 4900 1900
Wire Wire Line
	5600 1200 5600 1900
Wire Wire Line
	6300 1300 6300 1900
Wire Wire Line
	7000 1400 7000 1900
Wire Wire Line
	7700 1500 7700 1900
Wire Wire Line
	8400 1600 8400 1900
Wire Wire Line
	9100 1700 9100 1900
Wire Wire Line
	4200 1000 9200 1000
Wire Wire Line
	4900 1100 9200 1100
Wire Wire Line
	5600 1200 9200 1200
Wire Wire Line
	6300 1300 9200 1300
Wire Wire Line
	7000 1400 9200 1400
Wire Wire Line
	7700 1500 9200 1500
Wire Wire Line
	8400 1600 9200 1600
Wire Wire Line
	9100 1700 9200 1700
Wire Wire Line
	9100 2400 9100 2300
Wire Wire Line
	8400 2400 8400 2300
Connection ~ 8400 2400
Wire Wire Line
	7700 2400 7700 2300
Connection ~ 7700 2400
Wire Wire Line
	7000 2400 7000 2300
Connection ~ 7000 2400
Wire Wire Line
	6300 2400 6300 2300
Connection ~ 6300 2400
Wire Wire Line
	5600 2400 5600 2300
Connection ~ 5600 2400
Wire Wire Line
	4900 2400 4900 2300
Connection ~ 4900 2400
Wire Wire Line
	4200 2300 4200 2400
Connection ~ 4200 2400
Wire Wire Line
	4300 5400 4600 5400
Wire Wire Line
	5000 5400 5300 5400
Wire Wire Line
	5700 5400 6000 5400
Wire Wire Line
	6400 5400 6700 5400
Wire Wire Line
	7100 5400 7400 5400
Wire Wire Line
	7800 5400 8100 5400
Wire Wire Line
	8500 5400 8800 5400
Wire Wire Line
	9100 5700 9100 5600
Wire Wire Line
	8400 5700 8400 5600
Connection ~ 8400 5700
Wire Wire Line
	7700 5700 7700 5600
Connection ~ 7700 5700
Wire Wire Line
	7000 5700 7000 5600
Connection ~ 7000 5700
Wire Wire Line
	6300 5600 6300 5800
Connection ~ 6300 5700
Wire Wire Line
	5600 5700 5600 5600
Connection ~ 5600 5700
Wire Wire Line
	4900 5700 4900 5600
Connection ~ 4900 5700
Wire Wire Line
	4200 5600 4200 5700
Wire Wire Line
	4200 4300 4200 5200
Wire Wire Line
	4900 4400 4900 5200
Wire Wire Line
	5600 4500 5600 5200
Wire Wire Line
	6300 4600 6300 5200
Wire Wire Line
	7000 4700 7000 5200
Wire Wire Line
	7700 4800 7700 5200
Wire Wire Line
	8400 4900 8400 5200
Wire Wire Line
	9100 5000 9100 5200
Wire Wire Line
	4200 4300 9200 4300
Wire Wire Line
	4900 4400 9200 4400
Wire Wire Line
	5600 4500 9200 4500
Wire Wire Line
	6300 4600 9200 4600
Wire Wire Line
	7000 4700 9200 4700
Wire Wire Line
	7700 4800 9200 4800
Wire Wire Line
	8400 4900 9200 4900
Wire Wire Line
	9100 5000 9200 5000
Wire Wire Line
	8500 2100 8500 2500
Wire Wire Line
	8500 2500 10000 2500
Wire Wire Line
	7800 2100 7800 2600
Wire Wire Line
	7800 2600 10000 2600
Wire Wire Line
	7100 2100 7100 2700
Wire Wire Line
	7100 2700 10000 2700
Wire Wire Line
	6400 2100 6400 2800
Wire Wire Line
	6400 2800 10000 2800
Wire Wire Line
	5700 2100 5700 2900
Wire Wire Line
	5700 2900 10000 2900
Wire Wire Line
	5000 2100 5000 3000
Wire Wire Line
	5000 3000 10000 3000
Wire Wire Line
	4300 2100 4300 3100
Wire Wire Line
	4300 3100 10000 3100
Wire Wire Line
	3600 2100 3600 3200
Wire Wire Line
	3600 3200 10000 3200
Wire Wire Line
	8500 5400 8500 4000
Wire Wire Line
	8500 4000 10000 4000
Wire Wire Line
	7800 5400 7800 3900
Wire Wire Line
	7800 3900 10000 3900
Wire Wire Line
	7100 5400 7100 3800
Wire Wire Line
	7100 3800 10000 3800
Wire Wire Line
	6400 5400 6400 3700
Wire Wire Line
	6400 3700 10000 3700
Wire Wire Line
	5700 5400 5700 3600
Wire Wire Line
	5700 3600 10000 3600
Wire Wire Line
	5000 5400 5000 3500
Wire Wire Line
	5000 3500 10000 3500
Wire Wire Line
	4300 5400 4300 3400
Wire Wire Line
	4300 3400 10000 3400
Wire Wire Line
	3600 3300 3600 5400
Wire Wire Line
	3600 5400 3900 5400
Wire Wire Line
	9350 2000 9350 2250
Connection ~ 9100 5700
Wire Wire Line
	10100 5200 10100 5800
Connection ~ 10100 5700
Wire Wire Line
	9900 5200 9900 5300
Wire Wire Line
	9900 5300 10100 5300
Connection ~ 10100 5300
Wire Wire Line
	9700 5700 9700 5500
Connection ~ 9700 5700
Wire Wire Line
	3900 2500 3900 2400
Wire Wire Line
	3900 2400 9100 2400
Wire Wire Line
	9200 5700 9200 6100
Wire Wire Line
	9200 5900 9300 5900
Connection ~ 9200 5700
Wire Wire Line
	9200 6100 9300 6100
Connection ~ 9200 5900
Wire Wire Line
	4200 5700 10100 5700
$Comp
L PWR_FLAG #FLG011
U 1 1 5A6B8256
P 9350 2000
F 0 "#FLG011" H 9350 2095 30  0001 C CNN
F 1 "PWR_FLAG" H 9350 2180 30  0000 C CNN
F 2 "" H 9350 2000 60  0001 C CNN
F 3 "" H 9350 2000 60  0001 C CNN
	1    9350 2000
	1    0    0    -1  
$EndComp
Connection ~ 9350 2100
Wire Wire Line
	3600 3300 10000 3300
$Comp
L R R4
U 1 1 5A6B968A
P 6300 5950
F 0 "R4" V 6200 5950 50  0000 C CNN
F 1 "0" V 6300 5950 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 6230 5950 50  0001 C CNN
F 3 "" H 6300 5950 50  0001 C CNN
	1    6300 5950
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR012
U 1 1 5A6B9957
P 6300 6200
F 0 "#PWR012" H 6300 5950 50  0001 C CNN
F 1 "GND" H 6300 6050 50  0000 C CNN
F 2 "" H 6300 6200 50  0001 C CNN
F 3 "" H 6300 6200 50  0001 C CNN
	1    6300 6200
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 6100 6300 6200
$EndSCHEMATC
