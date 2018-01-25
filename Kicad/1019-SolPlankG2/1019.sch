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
LIBS:1019-cache
EELAYER 25 0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 1
Title "Solenoid Plank (Gen 2)"
Date "23 jan 2018"
Rev "-"
Comp "Open Pinball Project"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MOSFET_N Q5
U 1 1 4F78A22C
P 7600 5500
F 0 "Q5" H 7610 5670 60  0000 R CNN
F 1 "MOSFET_N" H 7610 5350 60  0000 R CNN
F 2 "commonlib:00_to220_vert_gds" H 7600 5500 60  0001 C CNN
F 3 "" H 7600 5500 60  0001 C CNN
F 4 "International Rectifier" H 7600 5500 60  0001 C CNN "Manufacturer"
F 5 "IRL540NPBF" H 7600 5500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7600 5500 60  0001 C CNN "Distributor"
F 7 "942-IRL540NPBF" H 7600 5500 60  0001 C CNN "Distributor PN"
	1    7600 5500
	-1   0    0    -1  
$EndComp
$Comp
L spade_187 P10
U 1 1 4F789F3A
P 6750 5850
F 0 "P10" H 6750 5950 40  0000 C CNN
F 1 "SPADE_187" H 6750 5850 40  0000 C CNN
F 2 "commonlib:00_th1x2x200" H 6750 5850 60  0001 C CNN
F 3 "" H 6750 5850 60  0001 C CNN
F 4 "Keystone" H 6750 5850 60  0001 C CNN "Manufacturer"
F 5 "1285" H 6750 5850 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6750 5850 60  0001 C CNN "Distributor"
F 7 "534-1285" H 6750 5850 60  0001 C CNN "Distributor PN"
	1    6750 5850
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q2
U 1 1 55B161EC
P 4700 5500
F 0 "Q2" H 4710 5670 60  0000 R CNN
F 1 "MOSFET_N" H 4710 5350 60  0000 R CNN
F 2 "commonlib:00_to220_vert_gds" H 4700 5500 60  0001 C CNN
F 3 "" H 4700 5500 60  0001 C CNN
F 4 "International Rectifier" H 4700 5500 60  0001 C CNN "Manufacturer"
F 5 "IRL540NPBF" H 4700 5500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4700 5500 60  0001 C CNN "Distributor"
F 7 "942-IRL540NPBF" H 4700 5500 60  0001 C CNN "Distributor PN"
	1    4700 5500
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q1
U 1 1 55B16200
P 4100 5500
F 0 "Q1" H 4110 5670 60  0000 R CNN
F 1 "MOSFET_N" H 4110 5350 60  0000 R CNN
F 2 "commonlib:00_to220_vert_gds" H 4100 5500 60  0001 C CNN
F 3 "" H 4100 5500 60  0001 C CNN
F 4 "International Rectifier" H 4100 5500 60  0001 C CNN "Manufacturer"
F 5 "IRL540NPBF" H 4100 5500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4100 5500 60  0001 C CNN "Distributor"
F 7 "942-IRL540NPBF" H 4100 5500 60  0001 C CNN "Distributor PN"
	1    4100 5500
	1    0    0    -1  
$EndComp
$Comp
L GNDPWR #PWR01
U 1 1 55B17AB3
P 6750 6400
F 0 "#PWR01" H 6750 6450 40  0001 C CNN
F 1 "GNDPWR" H 6750 6320 40  0000 C CNN
F 2 "" H 6750 6400 60  0000 C CNN
F 3 "" H 6750 6400 60  0000 C CNN
	1    6750 6400
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q6
U 1 1 55B17B88
P 8200 5500
F 0 "Q6" H 8210 5670 60  0000 R CNN
F 1 "MOSFET_N" H 8210 5350 60  0000 R CNN
F 2 "commonlib:00_to220_vert_gds" H 8200 5500 60  0001 C CNN
F 3 "" H 8200 5500 60  0001 C CNN
F 4 "International Rectifier" H 8200 5500 60  0001 C CNN "Manufacturer"
F 5 "IRL540NPBF" H 8200 5500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 8200 5500 60  0001 C CNN "Distributor"
F 7 "942-IRL540NPBF" H 8200 5500 60  0001 C CNN "Distributor PN"
	1    8200 5500
	-1   0    0    -1  
$EndComp
$Comp
L TST P1
U 1 1 55B18CB8
P 900 6200
F 0 "P1" H 900 6500 40  0000 C CNN
F 1 "TST" H 900 6450 30  0000 C CNN
F 2 "commonlib:00_mtg_hole-2-56" H 900 6200 60  0001 C CNN
F 3 "~" H 900 6200 60  0000 C CNN
	1    900  6200
	1    0    0    -1  
$EndComp
NoConn ~ 900  6200
$Comp
L GND #PWR02
U 1 1 5A54E4EB
P 8500 6400
F 0 "#PWR02" H 8500 6150 50  0001 C CNN
F 1 "GND" H 8500 6250 50  0000 C CNN
F 2 "" H 8500 6400 50  0001 C CNN
F 3 "" H 8500 6400 50  0001 C CNN
	1    8500 6400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 5A5514B5
P 3800 6400
F 0 "#PWR03" H 3800 6150 50  0001 C CNN
F 1 "GND" H 3800 6250 50  0000 C CNN
F 2 "" H 3800 6400 50  0001 C CNN
F 3 "" H 3800 6400 50  0001 C CNN
	1    3800 6400
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 5A552676
P 3800 5850
F 0 "R2" V 3880 5850 50  0000 C CNN
F 1 "100K" V 3800 5850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 3730 5850 50  0001 C CNN
F 3 "" H 3800 5850 50  0001 C CNN
	1    3800 5850
	-1   0    0    1   
$EndComp
$Comp
L R R3
U 1 1 5A552AF7
P 4400 5850
F 0 "R3" V 4480 5850 50  0000 C CNN
F 1 "100K" V 4400 5850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 4330 5850 50  0001 C CNN
F 3 "" H 4400 5850 50  0001 C CNN
	1    4400 5850
	-1   0    0    1   
$EndComp
$Comp
L R R6
U 1 1 5A552B84
P 7900 5850
F 0 "R6" V 7980 5850 50  0000 C CNN
F 1 "100K" V 7900 5850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 7830 5850 50  0001 C CNN
F 3 "" H 7900 5850 50  0001 C CNN
	1    7900 5850
	-1   0    0    1   
$EndComp
$Comp
L R R7
U 1 1 5A552C04
P 8500 5850
F 0 "R7" V 8580 5850 50  0000 C CNN
F 1 "100K" V 8500 5850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 8430 5850 50  0001 C CNN
F 3 "" H 8500 5850 50  0001 C CNN
	1    8500 5850
	-1   0    0    1   
$EndComp
Wire Wire Line
	4200 4200 4200 5300
Wire Wire Line
	4800 4300 4800 5300
Wire Wire Line
	4200 5700 4200 6200
Wire Wire Line
	4800 6200 4800 5700
Wire Wire Line
	8100 4500 8100 5300
Wire Wire Line
	7500 4600 7500 5300
Wire Wire Line
	8100 6200 8100 5700
Wire Wire Line
	7500 6200 7500 5700
Wire Wire Line
	3900 5500 3800 5500
Wire Wire Line
	4500 5500 4400 5500
Wire Wire Line
	4400 6300 4400 6000
Wire Wire Line
	7800 5500 7900 5500
Wire Wire Line
	7900 4000 7900 5700
Wire Wire Line
	7900 6000 7900 6300
Wire Wire Line
	8400 5500 8500 5500
Wire Wire Line
	8500 3900 8500 5700
Connection ~ 8500 5500
Connection ~ 7900 5500
Connection ~ 4400 5500
Connection ~ 3800 5500
Wire Wire Line
	7900 6300 9700 6300
Connection ~ 8500 6300
Wire Wire Line
	3600 6300 6000 6300
Connection ~ 3800 6300
Wire Wire Line
	4200 6200 9300 6200
Connection ~ 4800 6200
Connection ~ 7500 6200
Wire Wire Line
	3800 6000 3800 6400
Wire Wire Line
	8500 6000 8500 6400
$Comp
L CONN_8 P8
U 1 1 5A67673D
P 6450 2250
F 0 "P8" V 6400 2250 60  0000 C CNN
F 1 "CONN_8" V 6500 2250 60  0000 C CNN
F 2 "commonlib:00_th1x8x100-lock" H 6450 2250 60  0001 C CNN
F 3 "" H 6450 2250 60  0000 C CNN
	1    6450 2250
	-1   0    0    1   
$EndComp
$Comp
L Conn_01x22 J2
U 1 1 5A678335
P 8600 2400
F 0 "J2" H 8600 3500 50  0000 C CNN
F 1 "Conn_01x22" H 8600 1200 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x22_Pitch2.54mm" H 8600 2400 50  0001 C CNN
F 3 "" H 8600 2400 50  0001 C CNN
	1    8600 2400
	1    0    0    1   
$EndComp
$Comp
L +5V #PWR04
U 1 1 5A679840
P 8000 1200
F 0 "#PWR04" H 8000 1290 20  0001 C CNN
F 1 "+5V" H 8000 1350 30  0000 C CNN
F 2 "" H 8000 1200 60  0001 C CNN
F 3 "" H 8000 1200 60  0001 C CNN
	1    8000 1200
	1    0    0    -1  
$EndComp
Wire Wire Line
	8000 1200 8000 1300
Wire Wire Line
	8000 1300 8400 1300
$Comp
L GND #PWR05
U 1 1 5A67AABA
P 7750 1200
F 0 "#PWR05" H 7750 950 50  0001 C CNN
F 1 "GND" H 7750 1050 50  0000 C CNN
F 2 "" H 7750 1200 50  0001 C CNN
F 3 "" H 7750 1200 50  0001 C CNN
	1    7750 1200
	1    0    0    -1  
$EndComp
Wire Wire Line
	8400 1400 7900 1400
Wire Wire Line
	7900 1400 7900 1100
Wire Wire Line
	7900 1100 7750 1100
Wire Wire Line
	7750 1100 7750 1200
$Comp
L MOSFET_N Q4
U 1 1 5A67F13D
P 5900 5500
F 0 "Q4" H 5910 5670 60  0000 R CNN
F 1 "MOSFET_N" H 5910 5350 60  0000 R CNN
F 2 "commonlib:00_to220_vert_gds" H 5900 5500 60  0001 C CNN
F 3 "" H 5900 5500 60  0001 C CNN
F 4 "International Rectifier" H 5900 5500 60  0001 C CNN "Manufacturer"
F 5 "IRL540NPBF" H 5900 5500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5900 5500 60  0001 C CNN "Distributor"
F 7 "942-IRL540NPBF" H 5900 5500 60  0001 C CNN "Distributor PN"
	1    5900 5500
	1    0    0    -1  
$EndComp
$Comp
L MOSFET_N Q3
U 1 1 5A67F147
P 5300 5500
F 0 "Q3" H 5310 5670 60  0000 R CNN
F 1 "MOSFET_N" H 5310 5350 60  0000 R CNN
F 2 "commonlib:00_to220_vert_gds" H 5300 5500 60  0001 C CNN
F 3 "" H 5300 5500 60  0001 C CNN
F 4 "International Rectifier" H 5300 5500 60  0001 C CNN "Manufacturer"
F 5 "IRL540NPBF" H 5300 5500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5300 5500 60  0001 C CNN "Distributor"
F 7 "942-IRL540NPBF" H 5300 5500 60  0001 C CNN "Distributor PN"
	1    5300 5500
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 5A67F14D
P 5000 5850
F 0 "R4" V 5080 5850 50  0000 C CNN
F 1 "100K" V 5000 5850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 4930 5850 50  0001 C CNN
F 3 "" H 5000 5850 50  0001 C CNN
	1    5000 5850
	-1   0    0    1   
$EndComp
$Comp
L R R5
U 1 1 5A67F153
P 5600 5850
F 0 "R5" V 5680 5850 50  0000 C CNN
F 1 "100K" V 5600 5850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 5530 5850 50  0001 C CNN
F 3 "" H 5600 5850 50  0001 C CNN
	1    5600 5850
	-1   0    0    1   
$EndComp
Wire Wire Line
	5100 5500 5000 5500
Wire Wire Line
	5000 3900 5000 5700
Wire Wire Line
	5700 5500 5600 5500
Wire Wire Line
	5600 4000 5600 5700
Wire Wire Line
	5600 6300 5600 6000
Connection ~ 5600 5500
Connection ~ 5000 5500
Wire Wire Line
	5000 6300 5000 6000
Connection ~ 4400 6300
Connection ~ 5000 6300
Wire Wire Line
	5400 5700 5400 6200
Connection ~ 5400 6200
Wire Wire Line
	6000 5700 6000 6200
Connection ~ 6000 6200
Wire Wire Line
	6300 4400 6300 6200
Connection ~ 6300 6200
Wire Wire Line
	6650 6050 6650 6200
Connection ~ 6650 6200
Wire Wire Line
	6850 6050 6850 6200
Connection ~ 6850 6200
Wire Wire Line
	6750 6200 6750 6400
Connection ~ 6750 6200
Wire Wire Line
	7200 4400 7200 6200
Connection ~ 7200 6200
$Comp
L MOSFET_N Q7
U 1 1 5A68161A
P 8800 5500
F 0 "Q7" H 8810 5670 60  0000 R CNN
F 1 "MOSFET_N" H 8810 5350 60  0000 R CNN
F 2 "commonlib:00_to220_vert_gds" H 8800 5500 60  0001 C CNN
F 3 "" H 8800 5500 60  0001 C CNN
F 4 "International Rectifier" H 8800 5500 60  0001 C CNN "Manufacturer"
F 5 "IRL540NPBF" H 8800 5500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 8800 5500 60  0001 C CNN "Distributor"
F 7 "942-IRL540NPBF" H 8800 5500 60  0001 C CNN "Distributor PN"
	1    8800 5500
	-1   0    0    -1  
$EndComp
$Comp
L MOSFET_N Q8
U 1 1 5A681624
P 9400 5500
F 0 "Q8" H 9410 5670 60  0000 R CNN
F 1 "MOSFET_N" H 9410 5350 60  0000 R CNN
F 2 "commonlib:00_to220_vert_gds" H 9400 5500 60  0001 C CNN
F 3 "" H 9400 5500 60  0001 C CNN
F 4 "International Rectifier" H 9400 5500 60  0001 C CNN "Manufacturer"
F 5 "IRL540NPBF" H 9400 5500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 9400 5500 60  0001 C CNN "Distributor"
F 7 "942-IRL540NPBF" H 9400 5500 60  0001 C CNN "Distributor PN"
	1    9400 5500
	-1   0    0    -1  
$EndComp
$Comp
L R R8
U 1 1 5A68162A
P 9100 5850
F 0 "R8" V 9180 5850 50  0000 C CNN
F 1 "100K" V 9100 5850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 9030 5850 50  0001 C CNN
F 3 "" H 9100 5850 50  0001 C CNN
	1    9100 5850
	-1   0    0    1   
$EndComp
$Comp
L R R9
U 1 1 5A681630
P 9700 5850
F 0 "R9" V 9780 5850 50  0000 C CNN
F 1 "100K" V 9700 5850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 9630 5850 50  0001 C CNN
F 3 "" H 9700 5850 50  0001 C CNN
	1    9700 5850
	-1   0    0    1   
$EndComp
Wire Wire Line
	9300 6200 9300 5700
Wire Wire Line
	8700 6200 8700 5700
Wire Wire Line
	9000 5500 9100 5500
Wire Wire Line
	9100 3800 9100 5700
Wire Wire Line
	9100 6300 9100 6000
Wire Wire Line
	9600 5500 9700 5500
Wire Wire Line
	9700 3700 9700 5700
Connection ~ 9700 5500
Connection ~ 9100 5500
Wire Wire Line
	9700 6300 9700 6000
Connection ~ 8100 6200
Connection ~ 8700 6200
Connection ~ 9100 6300
Wire Wire Line
	6900 3000 8400 3000
Text Label 8200 3000 0    60   ~ 0
P0.0
Wire Wire Line
	7000 2900 8400 2900
Text Label 8200 2900 0    60   ~ 0
P0.1
Wire Wire Line
	7100 2800 8400 2800
Wire Wire Line
	7200 2700 8400 2700
Text Label 8200 2800 0    60   ~ 0
P0.2
Text Label 8200 2700 0    60   ~ 0
P0.3
Wire Wire Line
	6800 2200 8400 2200
Wire Wire Line
	6800 2100 8400 2100
Wire Wire Line
	6800 2000 8400 2000
Wire Wire Line
	6800 1900 8400 1900
Text Label 8200 2200 0    60   ~ 0
P1.0
Text Label 8200 2100 0    60   ~ 0
P1.1
Text Label 8200 2000 0    60   ~ 0
P1.2
Text Label 8200 1900 0    60   ~ 0
P1.3
Wire Wire Line
	8000 2600 8400 2600
Wire Wire Line
	7900 2500 8400 2500
Wire Wire Line
	7800 2400 8400 2400
Wire Wire Line
	7700 2300 8400 2300
Text Label 8200 2600 0    60   ~ 0
P0.4
Text Label 8200 2500 0    60   ~ 0
P0.5
Text Label 8200 2400 0    60   ~ 0
P0.6
Text Label 8200 2300 0    60   ~ 0
P0.7
Wire Wire Line
	7600 1800 8400 1800
Wire Wire Line
	7500 1700 8400 1700
Wire Wire Line
	7400 1600 8400 1600
Wire Wire Line
	7300 1500 8400 1500
Text Label 8200 1800 0    60   ~ 0
P1.4
Text Label 8200 1700 0    60   ~ 0
P1.5
Text Label 8200 1600 0    60   ~ 0
P1.6
Text Label 8200 1500 0    60   ~ 0
P1.7
Wire Wire Line
	9700 3700 8000 3700
Wire Wire Line
	8000 3700 8000 2600
Wire Wire Line
	9100 3800 7900 3800
Wire Wire Line
	7900 3800 7900 2500
Wire Wire Line
	8500 3900 7800 3900
Wire Wire Line
	7800 3900 7800 2400
Wire Wire Line
	7900 4000 7700 4000
Wire Wire Line
	7700 4000 7700 2300
Text Label 8200 3400 0    60   ~ 0
P4.0
Text Label 8200 3300 0    60   ~ 0
P4.1
Text Label 8200 3200 0    60   ~ 0
P4.2
Text Label 8200 3100 0    60   ~ 0
P4.3
Wire Wire Line
	6900 3000 6900 2600
Wire Wire Line
	6900 2600 6800 2600
Wire Wire Line
	7000 2900 7000 2500
Wire Wire Line
	7000 2500 6800 2500
Wire Wire Line
	7100 2800 7100 2400
Wire Wire Line
	7100 2400 6800 2400
Wire Wire Line
	7200 2700 7200 2300
Wire Wire Line
	7200 2300 6800 2300
$Comp
L PWR_FLAG #FLG06
U 1 1 5A68D4D5
P 3600 6200
F 0 "#FLG06" H 3600 6295 30  0001 C CNN
F 1 "PWR_FLAG" H 3600 6380 30  0000 C CNN
F 2 "" H 3600 6200 60  0001 C CNN
F 3 "" H 3600 6200 60  0001 C CNN
	1    3600 6200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3600 6300 3600 6200
$Comp
L PWR_FLAG #FLG07
U 1 1 5A68D7AF
P 7000 6100
F 0 "#FLG07" H 7000 6195 30  0001 C CNN
F 1 "PWR_FLAG" H 7000 6280 30  0000 C CNN
F 2 "" H 7000 6100 60  0001 C CNN
F 3 "" H 7000 6100 60  0001 C CNN
	1    7000 6100
	1    0    0    -1  
$EndComp
Wire Wire Line
	7000 6100 7000 6200
Connection ~ 7000 6200
$Comp
L PWR_FLAG #FLG08
U 1 1 5A68DAAF
P 8200 1200
F 0 "#FLG08" H 8200 1295 30  0001 C CNN
F 1 "PWR_FLAG" H 8200 1380 30  0000 C CNN
F 2 "" H 8200 1200 60  0001 C CNN
F 3 "" H 8200 1200 60  0001 C CNN
	1    8200 1200
	1    0    0    -1  
$EndComp
Wire Wire Line
	8200 1200 8200 1300
Connection ~ 8200 1300
Wire Wire Line
	7600 1800 7600 4000
Wire Wire Line
	7600 4000 5600 4000
Wire Wire Line
	7500 1700 7500 3900
Wire Wire Line
	7500 3900 5000 3900
Wire Wire Line
	7400 1600 7400 3800
Wire Wire Line
	7400 3800 4400 3800
Wire Wire Line
	4400 3800 4400 5700
Wire Wire Line
	7300 1500 7300 3700
Wire Wire Line
	7300 3700 3800 3700
Wire Wire Line
	3800 3700 3800 5700
Wire Wire Line
	4200 4200 6500 4200
Wire Wire Line
	4800 4300 6500 4300
Wire Wire Line
	6300 4400 6500 4400
Wire Wire Line
	6300 4700 6500 4700
Connection ~ 6300 4700
Wire Wire Line
	5400 5300 5400 4500
Wire Wire Line
	5400 4500 6500 4500
Wire Wire Line
	6000 5300 6000 4600
Wire Wire Line
	6000 4600 6500 4600
Wire Wire Line
	9300 5300 9300 4200
Wire Wire Line
	9300 4200 7000 4200
Wire Wire Line
	8700 5300 8700 4300
Wire Wire Line
	8700 4300 7000 4300
Wire Wire Line
	7200 4400 7000 4400
Wire Wire Line
	7200 4700 7000 4700
Connection ~ 7200 4700
Wire Wire Line
	8100 4500 7000 4500
Wire Wire Line
	7000 4600 7500 4600
$Comp
L TST P2
U 1 1 5A690B5C
P 1100 6200
F 0 "P2" H 1100 6500 40  0000 C CNN
F 1 "TST" H 1100 6450 30  0000 C CNN
F 2 "commonlib:00_mtg_hole-2-56" H 1100 6200 60  0001 C CNN
F 3 "~" H 1100 6200 60  0000 C CNN
	1    1100 6200
	1    0    0    -1  
$EndComp
NoConn ~ 1100 6200
$Comp
L TST P3
U 1 1 5A690C29
P 1300 6200
F 0 "P3" H 1300 6500 40  0000 C CNN
F 1 "TST" H 1300 6450 30  0000 C CNN
F 2 "commonlib:00_mtg_hole-2-56" H 1300 6200 60  0001 C CNN
F 3 "~" H 1300 6200 60  0000 C CNN
	1    1300 6200
	1    0    0    -1  
$EndComp
NoConn ~ 1300 6200
$Comp
L TST P4
U 1 1 5A690C30
P 1500 6200
F 0 "P4" H 1500 6500 40  0000 C CNN
F 1 "TST" H 1500 6450 30  0000 C CNN
F 2 "commonlib:00_mtg_hole-2-56" H 1500 6200 60  0001 C CNN
F 3 "~" H 1500 6200 60  0000 C CNN
	1    1500 6200
	1    0    0    -1  
$EndComp
NoConn ~ 1500 6200
$Comp
L R R1
U 1 1 5A691014
P 6150 6300
F 0 "R1" V 6230 6300 50  0000 C CNN
F 1 "0" V 6150 6300 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 6080 6300 50  0001 C CNN
F 3 "" H 6150 6300 50  0001 C CNN
	1    6150 6300
	0    1    1    0   
$EndComp
Connection ~ 5600 6300
Wire Wire Line
	6300 6300 6750 6300
Connection ~ 6750 6300
Text Label 950  2300 0    60   ~ 0
P4.0
Text Label 950  2200 0    60   ~ 0
P4.1
Text Label 950  2000 0    60   ~ 0
P4.2
$Comp
L CONN_4X2 P5
U 1 1 5A693F87
P 3050 1900
F 0 "P5" H 3050 2150 50  0000 C CNN
F 1 "CONN_4X2" V 3050 1900 40  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x04_Pitch2.54mm" H 3050 1900 60  0001 C CNN
F 3 "" H 3050 1900 60  0000 C CNN
	1    3050 1900
	0    1    1    0   
$EndComp
$Comp
L CONN_4X2 P6
U 1 1 5A693F88
P 3050 3400
F 0 "P6" H 3050 3650 50  0000 C CNN
F 1 "CONN_4X2" V 3050 3400 40  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x04_Pitch2.54mm" H 3050 3400 60  0001 C CNN
F 3 "" H 3050 3400 60  0000 C CNN
	1    3050 3400
	0    1    1    0   
$EndComp
Text Label 1250 2300 0    60   ~ 0
RX
Text Label 1250 2200 0    60   ~ 0
TX
Wire Wire Line
	3100 1500 3100 1200
Wire Wire Line
	2300 1200 3800 1200
Wire Wire Line
	2300 2300 2300 1200
Wire Wire Line
	3200 3000 3200 2900
Wire Wire Line
	3200 2900 3400 2900
Wire Wire Line
	3400 2900 3400 1400
Wire Wire Line
	3400 1400 3200 1400
Wire Wire Line
	3200 1400 3200 1500
Wire Wire Line
	2700 2200 2700 2700
Wire Wire Line
	3100 2700 3100 3000
NoConn ~ 3100 2300
NoConn ~ 3200 2300
NoConn ~ 3100 3800
NoConn ~ 3200 3800
Wire Wire Line
	3000 1500 3000 1300
Wire Wire Line
	3000 1300 2600 1300
Wire Wire Line
	2600 1300 2600 4100
Wire Wire Line
	3000 3000 3000 2800
Wire Wire Line
	3000 2800 2600 2800
Connection ~ 2600 2800
$Comp
L +5V #PWR09
U 1 1 5A693F89
P 2900 1000
F 0 "#PWR09" H 2900 1090 20  0001 C CNN
F 1 "+5V" H 2900 1090 30  0000 C CNN
F 2 "" H 2900 1000 60  0001 C CNN
F 3 "" H 2900 1000 60  0001 C CNN
	1    2900 1000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2900 1000 2900 1500
Wire Wire Line
	2900 1400 2800 1400
Wire Wire Line
	2800 1400 2800 2900
Wire Wire Line
	2800 2900 2900 2900
Wire Wire Line
	2900 2900 2900 3000
Connection ~ 2900 1400
Wire Wire Line
	3000 2300 3000 2600
Wire Wire Line
	3000 2600 2100 2600
Wire Wire Line
	2100 2000 2100 4000
Wire Wire Line
	2900 2500 2900 2300
Wire Wire Line
	1800 2500 2900 2500
Wire Wire Line
	2200 3900 2900 3900
Wire Wire Line
	2900 3900 2900 3800
Connection ~ 2200 2500
Wire Wire Line
	2100 4000 3000 4000
Wire Wire Line
	3000 4000 3000 3800
Connection ~ 2100 2600
Text Label 1250 2000 0    60   ~ 0
SYNCH
Wire Wire Line
	1850 2200 2700 2200
Wire Wire Line
	1850 2000 2100 2000
Wire Wire Line
	3800 2300 4000 2300
Connection ~ 3100 1200
Wire Wire Line
	3800 1200 3800 2300
Wire Wire Line
	3400 2200 4000 2200
$Comp
L +12V1 #PWR010
U 1 1 5A693F8D
P 1800 2500
F 0 "#PWR010" H 1800 2450 20  0001 C CNN
F 1 "+12V1" H 1800 2600 30  0000 C CNN
F 2 "~" H 1800 2500 60  0000 C CNN
F 3 "~" H 1800 2500 60  0000 C CNN
	1    1800 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	2200 2500 2200 3900
$Comp
L GND #PWR011
U 1 1 5A693F8F
P 2600 4100
F 0 "#PWR011" H 2600 3850 50  0001 C CNN
F 1 "GND" H 2600 3950 50  0000 C CNN
F 2 "" H 2600 4100 50  0001 C CNN
F 3 "" H 2600 4100 50  0001 C CNN
	1    2600 4100
	1    0    0    -1  
$EndComp
$Comp
L R R11
U 1 1 5A693F91
P 1700 2000
F 0 "R11" V 1600 2000 50  0000 C CNN
F 1 "480" V 1700 2000 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 1630 2000 50  0001 C CNN
F 3 "" H 1700 2000 50  0001 C CNN
	1    1700 2000
	0    1    1    0   
$EndComp
$Comp
L R R10
U 1 1 5A693F92
P 1700 2200
F 0 "R10" V 1600 2200 50  0000 C CNN
F 1 "480" V 1700 2200 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 1630 2200 50  0001 C CNN
F 3 "" H 1700 2200 50  0001 C CNN
	1    1700 2200
	0    1    1    0   
$EndComp
Connection ~ 2600 2400
Wire Wire Line
	2600 2400 4000 2400
Connection ~ 2900 1100
Wire Wire Line
	2900 1100 3700 1100
Wire Wire Line
	3700 1100 3700 2500
Wire Wire Line
	3700 2500 4000 2500
$Comp
L CONN_4 P7
U 1 1 5A693F8A
P 4350 2350
F 0 "P7" V 4300 2350 50  0000 C CNN
F 1 "CONN_4" V 4400 2350 50  0000 C CNN
F 2 "commonlib:00_th1x4x100-lock" H 4350 2350 60  0001 C CNN
F 3 "" H 4350 2350 60  0001 C CNN
F 4 "FCI" H 4350 2350 60  0001 C CNN "Manufacturer"
F 5 "68001-436HLF" H 4350 2350 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4350 2350 60  0001 C CNN "Distributor"
F 7 "649-68001-436HLF" H 4350 2350 60  0001 C CNN "Distributor PN"
	1    4350 2350
	1    0    0    -1  
$EndComp
Connection ~ 3400 2200
Wire Wire Line
	2700 2700 3100 2700
Wire Wire Line
	950  2000 1550 2000
Wire Wire Line
	950  2200 1550 2200
Wire Wire Line
	950  2300 2300 2300
Wire Wire Line
	8400 3100 8200 3100
Wire Wire Line
	8400 3200 8200 3200
Wire Wire Line
	8400 3300 8200 3300
Wire Wire Line
	8400 3400 8200 3400
$Comp
L PWR_FLAG #FLG012
U 1 1 5A698F7E
P 2450 2450
F 0 "#FLG012" H 2450 2545 30  0001 C CNN
F 1 "PWR_FLAG" H 2450 2630 30  0000 C CNN
F 2 "" H 2450 2450 60  0001 C CNN
F 3 "" H 2450 2450 60  0001 C CNN
	1    2450 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 2450 2450 2500
Connection ~ 2450 2500
$Comp
L R R12
U 1 1 5A69D2DC
P 1700 1800
F 0 "R12" V 1600 1800 50  0000 C CNN
F 1 "0" V 1700 1800 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical" V 1630 1800 50  0001 C CNN
F 3 "" H 1700 1800 50  0001 C CNN
	1    1700 1800
	0    1    1    0   
$EndComp
Wire Wire Line
	2600 1800 1850 1800
Connection ~ 2600 1800
Text Label 950  1800 0    60   ~ 0
P4.3
Wire Wire Line
	950  1800 1550 1800
Text Notes 1050 1600 0    60   ~ 0
R12 only populated if on\nleft side of PSOC4200
$Comp
L Conn_02x06_Top_Bottom J1
U 1 1 5A69EA86
P 6700 4400
F 0 "J1" H 6750 4700 50  0000 C CNN
F 1 "Conn_02x06_Top_Bottom" H 6750 4000 50  0000 C CNN
F 2 "Libraries:00_th2x6x4.2mm_cheap" H 6700 4400 50  0001 C CNN
F 3 "" H 6700 4400 50  0001 C CNN
	1    6700 4400
	1    0    0    -1  
$EndComp
$EndSCHEMATC
