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
LIBS:special
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
LIBS:1017-cache
EELAYER 27 0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 1
Title "Surface Mount Incandescent Driver (Gen 2)"
Date "18 dec 2015"
Rev "-"
Comp "Open Pinball Project"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L PWR_FLAG #FLG2
U 1 1 4F79A982
P 1500 1600
F 0 "#FLG2" H 1500 1695 30  0001 C CNN
F 1 "PWR_FLAG" H 1500 1780 30  0000 C CNN
F 2 "" H 1500 1600 60  0001 C CNN
F 3 "" H 1500 1600 60  0001 C CNN
	1    1500 1600
	1    0    0    -1  
$EndComp
$Comp
L SPADE_187 P4
U 1 1 4F789F3A
P 3100 3300
F 0 "P4" H 3100 3400 40  0000 C CNN
F 1 "SPADE_187" H 3100 3300 40  0000 C CNN
F 2 "" H 3100 3300 60  0001 C CNN
F 3 "" H 3100 3300 60  0001 C CNN
F 4 "Keystone" H 3100 3300 60  0001 C CNN "Manufacturer"
F 5 "1285" H 3100 3300 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 3100 3300 60  0001 C CNN "Distributor"
F 7 "534-1285" H 3100 3300 60  0001 C CNN "Distributor PN"
	1    3100 3300
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q1
U 1 1 55B16200
P 4000 4000
F 0 "Q1" H 4010 4170 60  0000 R CNN
F 1 "MOSFET_N" H 4010 3850 60  0000 R CNN
F 2 "" H 4000 4000 60  0001 C CNN
F 3 "" H 4000 4000 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 4000 4000 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 4000 4000 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4000 4000 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 4000 4000 60  0001 C CNN "Distributor PN"
	1    4000 4000
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P1
U 1 1 55B16234
P 2050 1350
F 0 "P1" V 2000 1350 50  0000 C CNN
F 1 "CONN_4" V 2100 1350 50  0000 C CNN
F 2 "" H 2050 1350 60  0001 C CNN
F 3 "" H 2050 1350 60  0001 C CNN
F 4 "FCI" H 2050 1350 60  0001 C CNN "Manufacturer"
F 5 "68001-436HLF" H 2050 1350 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 2050 1350 60  0001 C CNN "Distributor"
F 7 "649-68001-436HLF" H 2050 1350 60  0001 C CNN "Distributor PN"
	1    2050 1350
	0    -1   -1   0   
$EndComp
$Comp
L CONN_4 P3
U 1 1 55B1623E
P 2050 2150
F 0 "P3" V 2000 2150 50  0000 C CNN
F 1 "CONN_4" V 2100 2150 50  0000 C CNN
F 2 "" H 2050 2150 60  0001 C CNN
F 3 "" H 2050 2150 60  0001 C CNN
F 4 "FCI" H 2050 2150 60  0001 C CNN "Manufacturer"
F 5 "68001-436HLF" H 2050 2150 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 2050 2150 60  0001 C CNN "Distributor"
F 7 "649-68001-436HLF" H 2050 2150 60  0001 C CNN "Distributor PN"
	1    2050 2150
	0    -1   -1   0   
$EndComp
$Comp
L +5V #PWR3
U 1 1 55B16244
P 2400 1600
F 0 "#PWR3" H 2400 1690 20  0001 C CNN
F 1 "+5V" H 2400 1690 30  0000 C CNN
F 2 "" H 2400 1600 60  0001 C CNN
F 3 "" H 2400 1600 60  0001 C CNN
	1    2400 1600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR5
U 1 1 55B16408
P 2500 3200
F 0 "#PWR5" H 2500 3200 30  0001 C CNN
F 1 "GND" H 2500 3130 30  0001 C CNN
F 2 "" H 2500 3200 60  0001 C CNN
F 3 "" H 2500 3200 60  0001 C CNN
	1    2500 3200
	1    0    0    -1  
$EndComp
$Comp
L +12V1 #PWR2
U 1 1 55B165D8
P 1700 1600
F 0 "#PWR2" H 1700 1550 20  0001 C CNN
F 1 "+12V1" H 1700 1700 30  0000 C CNN
F 2 "~" H 1700 1600 60  0000 C CNN
F 3 "~" H 1700 1600 60  0000 C CNN
	1    1700 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2200 1700 2200 1800
Wire Wire Line
	2200 1800 2500 1800
Wire Wire Line
	2500 1800 2500 3200
Wire Wire Line
	2200 2500 2200 2600
Wire Wire Line
	2200 2600 2500 2600
Connection ~ 2500 2600
Wire Wire Line
	2100 1700 2100 1900
Wire Wire Line
	2100 1900 2400 1900
Wire Wire Line
	2400 1600 2400 2700
Wire Wire Line
	2100 2500 2100 2700
Wire Wire Line
	2100 2700 2400 2700
Connection ~ 2400 1900
Wire Wire Line
	1700 1600 1700 2700
Wire Wire Line
	1700 1900 2000 1900
Wire Wire Line
	2000 1900 2000 1700
Wire Wire Line
	1700 2700 2000 2700
Wire Wire Line
	2000 2700 2000 2500
Connection ~ 1700 1900
Wire Wire Line
	1900 1800 1900 1700
Wire Wire Line
	1000 1800 1900 1800
Wire Wire Line
	1900 2500 1900 2600
Wire Wire Line
	1900 2600 1600 2600
$Comp
L R R1
U 1 1 55B1776F
P 3700 3250
F 0 "R1" V 3780 3250 40  0000 C CNN
F 1 "10K" V 3707 3251 40  0000 C CNN
F 2 "~" V 3630 3250 30  0000 C CNN
F 3 "~" H 3700 3250 30  0000 C CNN
	1    3700 3250
	-1   0    0    1   
$EndComp
Wire Wire Line
	6200 2200 6000 2200
Wire Wire Line
	6200 2100 5900 2100
Wire Wire Line
	3500 1500 6200 1500
Wire Wire Line
	4200 1600 6200 1600
Wire Wire Line
	4900 1700 6200 1700
Wire Wire Line
	5600 1800 6200 1800
Connection ~ 2500 3000
$Comp
L TST P6
U 1 1 55B18CB8
P 2000 4100
F 0 "P6" H 2000 4400 40  0000 C CNN
F 1 "TST" H 2000 4350 30  0000 C CNN
F 2 "~" H 2000 4100 60  0000 C CNN
F 3 "~" H 2000 4100 60  0000 C CNN
	1    2000 4100
	1    0    0    -1  
$EndComp
NoConn ~ 2000 4100
$Comp
L PWR_FLAG #FLG3
U 1 1 55B18D79
P 2600 1600
F 0 "#FLG3" H 2600 1695 30  0001 C CNN
F 1 "PWR_FLAG" H 2600 1780 30  0000 C CNN
F 2 "" H 2600 1600 60  0001 C CNN
F 3 "" H 2600 1600 60  0001 C CNN
	1    2600 1600
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG1
U 1 1 55B18D7F
P 1000 1600
F 0 "#FLG1" H 1000 1695 30  0001 C CNN
F 1 "PWR_FLAG" H 1000 1780 30  0000 C CNN
F 2 "" H 1000 1600 60  0001 C CNN
F 3 "" H 1000 1600 60  0001 C CNN
	1    1000 1600
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG4
U 1 1 55B18D85
P 2700 2900
F 0 "#FLG4" H 2700 2995 30  0001 C CNN
F 1 "PWR_FLAG" H 2700 3080 30  0000 C CNN
F 2 "" H 2700 2900 60  0001 C CNN
F 3 "" H 2700 2900 60  0001 C CNN
	1    2700 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	2700 3000 2700 2900
Wire Wire Line
	1500 1600 1500 1700
Wire Wire Line
	1500 1700 1700 1700
Connection ~ 1700 1700
Wire Wire Line
	2600 1600 2600 1700
Wire Wire Line
	2600 1700 2400 1700
Connection ~ 2400 1700
$Comp
L CONN_8 P2
U 1 1 55B15C94
P 6550 1850
F 0 "P2" V 6500 1850 60  0000 C CNN
F 1 "CONN_8" V 6600 1850 60  0000 C CNN
F 2 "" H 6550 1850 60  0000 C CNN
F 3 "" H 6550 1850 60  0000 C CNN
	1    6550 1850
	1    0    0    -1  
$EndComp
Text Label 6050 1500 0    60   ~ 0
P0
Text Label 6050 1600 0    60   ~ 0
P1
Text Label 6050 1700 0    60   ~ 0
P2
Text Label 6050 1800 0    60   ~ 0
P3
Text Label 6050 1900 0    60   ~ 0
P4
Text Label 6050 2000 0    60   ~ 0
P5
Text Label 6050 2100 0    60   ~ 0
P6
Text Label 6050 2200 0    60   ~ 0
P7
$Comp
L MOSFET_N Q2
U 1 1 55B4EEB4
P 4700 4000
F 0 "Q2" H 4710 4170 60  0000 R CNN
F 1 "MOSFET_N" H 4710 3850 60  0000 R CNN
F 2 "" H 4700 4000 60  0001 C CNN
F 3 "" H 4700 4000 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 4700 4000 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 4700 4000 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4700 4000 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 4700 4000 60  0001 C CNN "Distributor PN"
	1    4700 4000
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 55B4EEBA
P 4400 3250
F 0 "R2" V 4480 3250 40  0000 C CNN
F 1 "10K" V 4407 3251 40  0000 C CNN
F 2 "~" V 4330 3250 30  0000 C CNN
F 3 "~" H 4400 3250 30  0000 C CNN
	1    4400 3250
	-1   0    0    1   
$EndComp
$Comp
L MOSFET_N Q3
U 1 1 55B4EEC4
P 5400 4000
F 0 "Q3" H 5410 4170 60  0000 R CNN
F 1 "MOSFET_N" H 5410 3850 60  0000 R CNN
F 2 "" H 5400 4000 60  0001 C CNN
F 3 "" H 5400 4000 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 5400 4000 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 5400 4000 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5400 4000 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 5400 4000 60  0001 C CNN "Distributor PN"
	1    5400 4000
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 55B4EECA
P 5100 3250
F 0 "R3" V 5180 3250 40  0000 C CNN
F 1 "10K" V 5107 3251 40  0000 C CNN
F 2 "~" V 5030 3250 30  0000 C CNN
F 3 "~" H 5100 3250 30  0000 C CNN
	1    5100 3250
	-1   0    0    1   
$EndComp
$Comp
L MOSFET_N Q4
U 1 1 55B4EED4
P 6100 4000
F 0 "Q4" H 6110 4170 60  0000 R CNN
F 1 "MOSFET_N" H 6110 3850 60  0000 R CNN
F 2 "" H 6100 4000 60  0001 C CNN
F 3 "" H 6100 4000 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 6100 4000 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 6100 4000 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6100 4000 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 6100 4000 60  0001 C CNN "Distributor PN"
	1    6100 4000
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 55B4EEDA
P 5800 3250
F 0 "R4" V 5880 3250 40  0000 C CNN
F 1 "10K" V 5807 3251 40  0000 C CNN
F 2 "~" V 5730 3250 30  0000 C CNN
F 3 "~" H 5800 3250 30  0000 C CNN
	1    5800 3250
	-1   0    0    1   
$EndComp
$Comp
L MOSFET_N Q5
U 1 1 55B4EEE4
P 6800 4000
F 0 "Q5" H 6810 4170 60  0000 R CNN
F 1 "MOSFET_N" H 6810 3850 60  0000 R CNN
F 2 "" H 6800 4000 60  0001 C CNN
F 3 "" H 6800 4000 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 6800 4000 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 6800 4000 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6800 4000 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 6800 4000 60  0001 C CNN "Distributor PN"
	1    6800 4000
	1    0    0    -1  
$EndComp
$Comp
L R R5
U 1 1 55B4EEEA
P 6500 3250
F 0 "R5" V 6580 3250 40  0000 C CNN
F 1 "10K" V 6507 3251 40  0000 C CNN
F 2 "~" V 6430 3250 30  0000 C CNN
F 3 "~" H 6500 3250 30  0000 C CNN
	1    6500 3250
	-1   0    0    1   
$EndComp
$Comp
L MOSFET_N Q6
U 1 1 55B4EEF4
P 7500 4000
F 0 "Q6" H 7510 4170 60  0000 R CNN
F 1 "MOSFET_N" H 7510 3850 60  0000 R CNN
F 2 "" H 7500 4000 60  0001 C CNN
F 3 "" H 7500 4000 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 7500 4000 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 7500 4000 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7500 4000 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 7500 4000 60  0001 C CNN "Distributor PN"
	1    7500 4000
	1    0    0    -1  
$EndComp
$Comp
L R R6
U 1 1 55B4EEFA
P 7200 3250
F 0 "R6" V 7280 3250 40  0000 C CNN
F 1 "10K" V 7207 3251 40  0000 C CNN
F 2 "~" V 7130 3250 30  0000 C CNN
F 3 "~" H 7200 3250 30  0000 C CNN
	1    7200 3250
	-1   0    0    1   
$EndComp
$Comp
L MOSFET_N Q7
U 1 1 55B4EF04
P 8200 4000
F 0 "Q7" H 8210 4170 60  0000 R CNN
F 1 "MOSFET_N" H 8210 3850 60  0000 R CNN
F 2 "" H 8200 4000 60  0001 C CNN
F 3 "" H 8200 4000 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 8200 4000 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 8200 4000 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 8200 4000 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 8200 4000 60  0001 C CNN "Distributor PN"
	1    8200 4000
	1    0    0    -1  
$EndComp
$Comp
L R R7
U 1 1 55B4EF0A
P 7900 3250
F 0 "R7" V 7980 3250 40  0000 C CNN
F 1 "10K" V 7907 3251 40  0000 C CNN
F 2 "~" V 7830 3250 30  0000 C CNN
F 3 "~" H 7900 3250 30  0000 C CNN
	1    7900 3250
	-1   0    0    1   
$EndComp
$Comp
L MOSFET_N Q8
U 1 1 55B4EF14
P 8900 4000
F 0 "Q8" H 8910 4170 60  0000 R CNN
F 1 "MOSFET_N" H 8910 3850 60  0000 R CNN
F 2 "" H 8900 4000 60  0001 C CNN
F 3 "" H 8900 4000 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 8900 4000 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 8900 4000 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 8900 4000 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 8900 4000 60  0001 C CNN "Distributor PN"
	1    8900 4000
	1    0    0    -1  
$EndComp
$Comp
L R R8
U 1 1 55B4EF1A
P 8600 3250
F 0 "R8" V 8680 3250 40  0000 C CNN
F 1 "10K" V 8607 3251 40  0000 C CNN
F 2 "~" V 8530 3250 30  0000 C CNN
F 3 "~" H 8600 3250 30  0000 C CNN
	1    8600 3250
	-1   0    0    1   
$EndComp
Wire Wire Line
	3500 1500 3500 6200
Wire Wire Line
	3700 3500 3700 4000
Wire Wire Line
	4200 1600 4200 6200
Wire Wire Line
	4400 4000 4500 4000
Wire Wire Line
	4400 3500 4400 4000
Wire Wire Line
	4900 1700 4900 6200
Wire Wire Line
	5100 4000 5200 4000
Wire Wire Line
	5100 3500 5100 4000
Wire Wire Line
	5600 1800 5600 6200
Wire Wire Line
	5800 4000 5900 4000
Wire Wire Line
	5800 3500 5800 4000
Wire Wire Line
	5700 1900 6200 1900
Wire Wire Line
	5700 1900 5700 2700
Wire Wire Line
	5700 2700 6300 2700
Wire Wire Line
	6300 2700 6300 6200
Wire Wire Line
	6500 4000 6600 4000
Wire Wire Line
	5800 2000 6200 2000
Wire Wire Line
	5800 2000 5800 2600
Wire Wire Line
	5800 2600 7000 2600
Wire Wire Line
	7000 2600 7000 6200
Wire Wire Line
	7200 4000 7300 4000
Wire Wire Line
	7200 3500 7200 4000
Wire Wire Line
	5900 2100 5900 2500
Wire Wire Line
	5900 2500 7700 2500
Wire Wire Line
	7700 2500 7700 6200
Wire Wire Line
	7900 4000 8000 4000
Wire Wire Line
	7900 3500 7900 4000
Wire Wire Line
	6000 2200 6000 2400
Wire Wire Line
	6000 2400 8400 2400
Wire Wire Line
	8400 2400 8400 6200
Wire Wire Line
	8600 4000 8700 4000
Wire Wire Line
	8600 3500 8600 4000
$Comp
L +12V1 #PWR4
U 1 1 55B4FA5C
P 3700 2800
F 0 "#PWR4" H 3700 2750 20  0001 C CNN
F 1 "+12V1" H 3700 2900 30  0000 C CNN
F 2 "~" H 3700 2800 60  0000 C CNN
F 3 "~" H 3700 2800 60  0000 C CNN
	1    3700 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 2800 3700 3000
Wire Wire Line
	3700 2900 8600 2900
Wire Wire Line
	4400 2900 4400 3000
Connection ~ 3700 2900
Wire Wire Line
	5100 2900 5100 3000
Connection ~ 4400 2900
Wire Wire Line
	5800 2900 5800 3000
Connection ~ 5100 2900
Wire Wire Line
	6500 2900 6500 3000
Connection ~ 5800 2900
Wire Wire Line
	7200 2900 7200 3000
Connection ~ 6500 2900
Wire Wire Line
	7900 2900 7900 3000
Connection ~ 7200 2900
Wire Wire Line
	8600 2900 8600 3000
Connection ~ 7900 2900
Wire Wire Line
	4100 4200 4100 6000
Wire Wire Line
	9200 3600 3000 3600
Wire Wire Line
	9000 4200 9000 6000
Wire Wire Line
	4800 4200 4800 6000
Wire Wire Line
	5500 4200 5500 6000
Wire Wire Line
	6900 4200 6900 6000
Wire Wire Line
	7600 4200 7600 6000
Wire Wire Line
	8300 4200 8300 6000
Wire Wire Line
	6500 3500 6500 4000
$Comp
L CONN_8 P7
U 1 1 55B503D5
P 9850 5250
F 0 "P7" V 9800 5250 60  0000 C CNN
F 1 "CONN_8" V 9900 5250 60  0000 C CNN
F 2 "" H 9850 5250 60  0000 C CNN
F 3 "" H 9850 5250 60  0000 C CNN
	1    9850 5250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 4900 9500 4900
Wire Wire Line
	4800 5000 9500 5000
Wire Wire Line
	5500 5100 9500 5100
Wire Wire Line
	6200 5200 9500 5200
Wire Wire Line
	6900 5300 9500 5300
Wire Wire Line
	7600 5400 9500 5400
Wire Wire Line
	8300 5500 9500 5500
Wire Wire Line
	9000 5600 9500 5600
Wire Wire Line
	3200 3500 3200 3600
Wire Wire Line
	3000 3600 3000 3500
Connection ~ 3200 3600
$Comp
L CONN_2 P5
U 1 1 55B50F36
P 9750 3400
F 0 "P5" V 9700 3400 40  0000 C CNN
F 1 "CONN_2" V 9800 3400 40  0000 C CNN
F 2 "" H 9750 3400 60  0000 C CNN
F 3 "" H 9750 3400 60  0000 C CNN
	1    9750 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	9400 3300 9200 3300
Wire Wire Line
	9200 3300 9200 3600
Wire Wire Line
	9400 3500 9200 3500
Connection ~ 9200 3500
Wire Wire Line
	6200 4200 6200 6000
Wire Wire Line
	4100 3600 4100 3800
Connection ~ 4100 3600
Wire Wire Line
	4800 3600 4800 3800
Connection ~ 4800 3600
Wire Wire Line
	5500 3600 5500 3800
Connection ~ 5500 3600
Wire Wire Line
	6200 3600 6200 3800
Connection ~ 6200 3600
Wire Wire Line
	6900 3600 6900 3800
Connection ~ 6900 3600
Wire Wire Line
	7600 3600 7600 3800
Connection ~ 7600 3600
Wire Wire Line
	8300 3600 8300 3800
Connection ~ 8300 3600
Wire Wire Line
	9000 3600 9000 3800
Connection ~ 9000 3600
Connection ~ 3350 3600
Wire Wire Line
	2500 3000 2700 3000
$Comp
L +VLED #PWR1
U 1 1 55BA97CE
P 1200 1600
F 0 "#PWR1" H 1200 1690 20  0001 C CNN
F 1 "+VLED" H 1200 1690 30  0000 C CNN
F 2 "~" H 1200 1600 60  0000 C CNN
F 3 "~" H 1200 1600 60  0000 C CNN
	1    1200 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	1600 2600 1600 1800
Wire Wire Line
	1200 1800 1200 1600
Connection ~ 1600 1800
Connection ~ 1200 1800
Wire Wire Line
	1000 1800 1000 1600
$Comp
L +VLED #PWR6
U 1 1 55BA9C4E
P 3350 3500
F 0 "#PWR6" H 3350 3590 20  0001 C CNN
F 1 "+VLED" H 3350 3590 30  0000 C CNN
F 2 "~" H 3350 3500 60  0000 C CNN
F 3 "~" H 3350 3500 60  0000 C CNN
	1    3350 3500
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q17
U 1 1 5673EC14
P 4000 6200
F 0 "Q17" H 4010 6370 60  0000 R CNN
F 1 "MOSFET_N" H 4010 6050 60  0000 R CNN
F 2 "" H 4000 6200 60  0001 C CNN
F 3 "" H 4000 6200 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 4000 6200 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 4000 6200 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4000 6200 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 4000 6200 60  0001 C CNN "Distributor PN"
	1    4000 6200
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q18
U 1 1 5673EC1E
P 4700 6200
F 0 "Q18" H 4710 6370 60  0000 R CNN
F 1 "MOSFET_N" H 4710 6050 60  0000 R CNN
F 2 "" H 4700 6200 60  0001 C CNN
F 3 "" H 4700 6200 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 4700 6200 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 4700 6200 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4700 6200 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 4700 6200 60  0001 C CNN "Distributor PN"
	1    4700 6200
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q19
U 1 1 5673EC28
P 5400 6200
F 0 "Q19" H 5410 6370 60  0000 R CNN
F 1 "MOSFET_N" H 5410 6050 60  0000 R CNN
F 2 "" H 5400 6200 60  0001 C CNN
F 3 "" H 5400 6200 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 5400 6200 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 5400 6200 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5400 6200 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 5400 6200 60  0001 C CNN "Distributor PN"
	1    5400 6200
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q20
U 1 1 5673EC32
P 6100 6200
F 0 "Q20" H 6110 6370 60  0000 R CNN
F 1 "MOSFET_N" H 6110 6050 60  0000 R CNN
F 2 "" H 6100 6200 60  0001 C CNN
F 3 "" H 6100 6200 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 6100 6200 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 6100 6200 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6100 6200 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 6100 6200 60  0001 C CNN "Distributor PN"
	1    6100 6200
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q21
U 1 1 5673EC3C
P 6800 6200
F 0 "Q21" H 6810 6370 60  0000 R CNN
F 1 "MOSFET_N" H 6810 6050 60  0000 R CNN
F 2 "" H 6800 6200 60  0001 C CNN
F 3 "" H 6800 6200 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 6800 6200 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 6800 6200 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6800 6200 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 6800 6200 60  0001 C CNN "Distributor PN"
	1    6800 6200
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q22
U 1 1 5673EC46
P 7500 6200
F 0 "Q22" H 7510 6370 60  0000 R CNN
F 1 "MOSFET_N" H 7510 6050 60  0000 R CNN
F 2 "" H 7500 6200 60  0001 C CNN
F 3 "" H 7500 6200 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 7500 6200 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 7500 6200 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7500 6200 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 7500 6200 60  0001 C CNN "Distributor PN"
	1    7500 6200
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q23
U 1 1 5673EC50
P 8200 6200
F 0 "Q23" H 8210 6370 60  0000 R CNN
F 1 "MOSFET_N" H 8210 6050 60  0000 R CNN
F 2 "" H 8200 6200 60  0001 C CNN
F 3 "" H 8200 6200 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 8200 6200 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 8200 6200 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 8200 6200 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 8200 6200 60  0001 C CNN "Distributor PN"
	1    8200 6200
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q24
U 1 1 5673EC5A
P 8900 6200
F 0 "Q24" H 8910 6370 60  0000 R CNN
F 1 "MOSFET_N" H 8910 6050 60  0000 R CNN
F 2 "" H 8900 6200 60  0001 C CNN
F 3 "" H 8900 6200 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 8900 6200 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 8900 6200 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 8900 6200 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 8900 6200 60  0001 C CNN "Distributor PN"
	1    8900 6200
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q9
U 1 1 5673EC94
P 3700 4500
F 0 "Q9" H 3710 4670 60  0000 R CNN
F 1 "MOSFET_N" H 3710 4350 60  0000 R CNN
F 2 "" H 3700 4500 60  0001 C CNN
F 3 "" H 3700 4500 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 3700 4500 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 3700 4500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 3700 4500 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 3700 4500 60  0001 C CNN "Distributor PN"
	1    3700 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 4000 3800 4000
Wire Wire Line
	3800 4000 3800 4300
$Comp
L MOSFET_N Q10
U 1 1 5673EEED
P 4400 4500
F 0 "Q10" H 4410 4670 60  0000 R CNN
F 1 "MOSFET_N" H 4410 4350 60  0000 R CNN
F 2 "" H 4400 4500 60  0001 C CNN
F 3 "" H 4400 4500 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 4400 4500 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 4400 4500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4400 4500 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 4400 4500 60  0001 C CNN "Distributor PN"
	1    4400 4500
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q11
U 1 1 5673EEF7
P 5100 4500
F 0 "Q11" H 5110 4670 60  0000 R CNN
F 1 "MOSFET_N" H 5110 4350 60  0000 R CNN
F 2 "" H 5100 4500 60  0001 C CNN
F 3 "" H 5100 4500 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 5100 4500 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 5100 4500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5100 4500 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 5100 4500 60  0001 C CNN "Distributor PN"
	1    5100 4500
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q12
U 1 1 5673EF01
P 5800 4500
F 0 "Q12" H 5810 4670 60  0000 R CNN
F 1 "MOSFET_N" H 5810 4350 60  0000 R CNN
F 2 "" H 5800 4500 60  0001 C CNN
F 3 "" H 5800 4500 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 5800 4500 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 5800 4500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5800 4500 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 5800 4500 60  0001 C CNN "Distributor PN"
	1    5800 4500
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q13
U 1 1 5673EF0B
P 6500 4500
F 0 "Q13" H 6510 4670 60  0000 R CNN
F 1 "MOSFET_N" H 6510 4350 60  0000 R CNN
F 2 "" H 6500 4500 60  0001 C CNN
F 3 "" H 6500 4500 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 6500 4500 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 6500 4500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6500 4500 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 6500 4500 60  0001 C CNN "Distributor PN"
	1    6500 4500
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q14
U 1 1 5673EF15
P 7200 4500
F 0 "Q14" H 7210 4670 60  0000 R CNN
F 1 "MOSFET_N" H 7210 4350 60  0000 R CNN
F 2 "" H 7200 4500 60  0001 C CNN
F 3 "" H 7200 4500 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 7200 4500 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 7200 4500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7200 4500 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 7200 4500 60  0001 C CNN "Distributor PN"
	1    7200 4500
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q15
U 1 1 5673EF1F
P 7900 4500
F 0 "Q15" H 7910 4670 60  0000 R CNN
F 1 "MOSFET_N" H 7910 4350 60  0000 R CNN
F 2 "" H 7900 4500 60  0001 C CNN
F 3 "" H 7900 4500 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 7900 4500 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 7900 4500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7900 4500 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 7900 4500 60  0001 C CNN "Distributor PN"
	1    7900 4500
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q16
U 1 1 5673EF29
P 8600 4500
F 0 "Q16" H 8610 4670 60  0000 R CNN
F 1 "MOSFET_N" H 8610 4350 60  0000 R CNN
F 2 "" H 8600 4500 60  0001 C CNN
F 3 "" H 8600 4500 60  0001 C CNN
F 4 "Fairchild Semiconductor" H 8600 4500 60  0001 C CNN "Manufacturer"
F 5 "2N7000TA" H 8600 4500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 8600 4500 60  0001 C CNN "Distributor"
F 7 "512-2N7000TA" H 8600 4500 60  0001 C CNN "Distributor PN"
	1    8600 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 4000 4500 4300
Wire Wire Line
	5200 4000 5200 4300
Wire Wire Line
	5900 4000 5900 4300
Wire Wire Line
	6600 4000 6600 4300
Wire Wire Line
	7300 4000 7300 4300
Wire Wire Line
	8000 4000 8000 4300
Wire Wire Line
	8700 4000 8700 4300
Wire Wire Line
	3500 6200 3800 6200
Connection ~ 3500 4500
Wire Wire Line
	4200 6200 4500 6200
Connection ~ 4200 4500
Wire Wire Line
	4900 6200 5200 6200
Connection ~ 4900 4500
Wire Wire Line
	5600 6200 5900 6200
Connection ~ 5600 4500
Wire Wire Line
	6300 6200 6600 6200
Connection ~ 6300 4500
Wire Wire Line
	7000 6200 7300 6200
Connection ~ 7000 4500
Wire Wire Line
	7700 6200 8000 6200
Connection ~ 7700 4500
Wire Wire Line
	8400 6200 8700 6200
Connection ~ 8400 4500
Connection ~ 4100 4900
Connection ~ 4800 5000
Connection ~ 5500 5100
Connection ~ 6200 5200
Connection ~ 6900 5300
Connection ~ 7600 5400
Connection ~ 8300 5500
Connection ~ 9000 5600
Wire Wire Line
	3350 6600 9000 6600
Wire Wire Line
	9000 6600 9000 6400
Wire Wire Line
	8300 6400 8300 6600
Connection ~ 8300 6600
Wire Wire Line
	7600 6400 7600 6600
Connection ~ 7600 6600
Wire Wire Line
	6900 6400 6900 6600
Connection ~ 6900 6600
Wire Wire Line
	6200 6400 6200 6600
Connection ~ 6200 6600
Wire Wire Line
	5500 6400 5500 6600
Connection ~ 5500 6600
Wire Wire Line
	4800 6400 4800 6600
Connection ~ 4800 6600
Wire Wire Line
	4100 6400 4100 6600
Connection ~ 4100 6600
Wire Wire Line
	3350 3500 3350 6600
$Comp
L GND #PWR7
U 1 1 56740A22
P 3800 5800
F 0 "#PWR7" H 3800 5800 30  0001 C CNN
F 1 "GND" H 3800 5730 30  0001 C CNN
F 2 "" H 3800 5800 60  0001 C CNN
F 3 "" H 3800 5800 60  0001 C CNN
	1    3800 5800
	1    0    0    -1  
$EndComp
Wire Wire Line
	3800 4700 3800 5800
Wire Wire Line
	8700 4700 8700 5600
Wire Wire Line
	8700 5600 3800 5600
Connection ~ 3800 5600
Wire Wire Line
	8000 4700 8000 5600
Connection ~ 8000 5600
Wire Wire Line
	7300 4700 7300 5600
Connection ~ 7300 5600
Wire Wire Line
	6600 4700 6600 5600
Connection ~ 6600 5600
Wire Wire Line
	5900 4700 5900 5600
Connection ~ 5900 5600
Wire Wire Line
	5200 4700 5200 5600
Connection ~ 5200 5600
Wire Wire Line
	4500 4700 4500 5600
Connection ~ 4500 5600
$EndSCHEMATC
