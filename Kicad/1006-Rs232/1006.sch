EESchema Schematic File Version 2  date 1/18/2013 3:12:57 PM
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
LIBS:1006-cache
EELAYER 25  0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 1
Title "RS232 Interface"
Date "27 apr 2012"
Rev "-"
Comp "Open Pinball Project"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Connection ~ 5150 2100
Wire Wire Line
	5150 2000 5150 2100
Wire Wire Line
	4650 1600 4650 1500
Wire Wire Line
	4650 1500 4400 1500
Wire Wire Line
	4400 1500 4400 1600
Connection ~ 4800 3750
Wire Wire Line
	4650 3750 4800 3750
Wire Wire Line
	5300 2200 5100 2200
Wire Wire Line
	5100 2200 5100 2500
Wire Wire Line
	5100 2500 4250 2500
Connection ~ 4800 2900
Wire Wire Line
	4800 2900 5300 2900
Wire Wire Line
	5300 2100 4250 2100
Wire Wire Line
	2900 2600 2400 2600
Wire Wire Line
	2400 2600 2400 2700
Wire Wire Line
	2900 2400 2000 2400
Wire Wire Line
	2200 1800 2700 1800
Wire Wire Line
	2700 1800 2700 2200
Wire Wire Line
	2700 2200 2900 2200
Wire Wire Line
	2900 2100 2900 1900
Wire Wire Line
	2900 1900 2500 1900
Wire Wire Line
	2900 2300 2500 2300
Wire Wire Line
	2200 2200 2200 2300
Wire Wire Line
	2000 2800 2300 2800
Wire Wire Line
	2300 2800 2300 2500
Wire Wire Line
	2300 2500 2900 2500
Wire Wire Line
	2400 3100 2400 3200
Wire Wire Line
	4800 2200 4800 3900
Wire Wire Line
	4250 2200 5000 2200
Wire Wire Line
	5000 2200 5000 2300
Wire Wire Line
	5000 2300 5300 2300
Connection ~ 4800 2200
Wire Wire Line
	4250 2300 4700 2300
Wire Wire Line
	4700 2300 4700 3500
Wire Wire Line
	4700 3500 5300 3500
Wire Wire Line
	4250 2600 5200 2600
Wire Wire Line
	5200 2600 5200 2400
Wire Wire Line
	5200 2400 5300 2400
Wire Wire Line
	5300 3300 4900 3300
Wire Wire Line
	4900 3300 4900 2400
Wire Wire Line
	4900 2400 4250 2400
Wire Wire Line
	4400 2100 4400 2000
Connection ~ 4400 2100
Wire Wire Line
	4950 2050 4950 2100
Connection ~ 4950 2100
$Comp
L GND #PWR01
U 1 1 4F9AF5C7
P 4650 1600
F 0 "#PWR01" H 4650 1600 30  0001 C CNN
F 1 "GND" H 4650 1530 30  0001 C CNN
	1    4650 1600
	1    0    0    -1  
$EndComp
$Comp
L C C5
U 1 1 4F9AF590
P 4400 1800
F 0 "C5" H 4450 1900 50  0000 L CNN
F 1 "1uF" H 4450 1700 50  0000 L CNN
	1    4400 1800
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 4F9AF017
P 4650 3750
F 0 "#FLG02" H 4650 3845 30  0001 C CNN
F 1 "PWR_FLAG" H 4650 3930 30  0000 C CNN
	1    4650 3750
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG03
U 1 1 4F9AF008
P 4950 2050
F 0 "#FLG03" H 4950 2145 30  0001 C CNN
F 1 "PWR_FLAG" H 4950 2230 30  0000 C CNN
	1    4950 2050
	1    0    0    -1  
$EndComp
NoConn ~ 5300 3700
NoConn ~ 5300 3600
NoConn ~ 5300 3400
NoConn ~ 5300 3200
NoConn ~ 5300 3100
NoConn ~ 5300 3000
$Comp
L DB9 J1
U 1 1 4F9AED42
P 5750 3300
F 0 "J1" H 5750 3850 70  0000 C CNN
F 1 "DB9" H 5750 2750 70  0000 C CNN
	1    5750 3300
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P1
U 1 1 4F9AECEA
P 5650 2250
F 0 "P1" V 5600 2250 50  0000 C CNN
F 1 "CONN_4" V 5700 2250 50  0000 C CNN
	1    5650 2250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 4F9AEC98
P 4800 3900
F 0 "#PWR04" H 4800 3900 30  0001 C CNN
F 1 "GND" H 4800 3830 30  0001 C CNN
	1    4800 3900
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR05
U 1 1 4F9AEC81
P 5150 2000
F 0 "#PWR05" H 5150 2090 20  0001 C CNN
F 1 "+5V" H 5150 2090 30  0000 C CNN
	1    5150 2000
	1    0    0    -1  
$EndComp
NoConn ~ 4250 2700
NoConn ~ 4250 2800
NoConn ~ 2900 2800
NoConn ~ 2900 2700
$Comp
L GND #PWR06
U 1 1 4F9AEC5A
P 2400 3200
F 0 "#PWR06" H 2400 3200 30  0001 C CNN
F 1 "GND" H 2400 3130 30  0001 C CNN
	1    2400 3200
	1    0    0    -1  
$EndComp
$Comp
L C C3
U 1 1 4F9AEC4D
P 2400 2900
F 0 "C3" H 2450 3000 50  0000 L CNN
F 1 "1uF" H 2450 2800 50  0000 L CNN
	1    2400 2900
	1    0    0    -1  
$EndComp
$Comp
L C C1
U 1 1 4F9AEC37
P 2000 2600
F 0 "C1" H 2050 2700 50  0000 L CNN
F 1 "1uF" H 2050 2500 50  0000 L CNN
	1    2000 2600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR07
U 1 1 4F9AEC23
P 2200 2300
F 0 "#PWR07" H 2200 2300 30  0001 C CNN
F 1 "GND" H 2200 2230 30  0001 C CNN
	1    2200 2300
	1    0    0    -1  
$EndComp
$Comp
L C C2
U 1 1 4F9AEBE9
P 2200 2000
F 0 "C2" H 2250 2100 50  0000 L CNN
F 1 "1uF" H 2250 1900 50  0000 L CNN
	1    2200 2000
	1    0    0    -1  
$EndComp
$Comp
L C C4
U 1 1 4F9AEBC5
P 2500 2100
F 0 "C4" H 2550 2200 50  0000 L CNN
F 1 "1uF" H 2550 2000 50  0000 L CNN
	1    2500 2100
	1    0    0    -1  
$EndComp
$Comp
L TRS322ECN U1
U 1 1 4F9AEB5E
P 3600 2450
F 0 "U1" H 3600 3000 60  0000 C CNN
F 1 "TRS322ECN" V 3600 2450 60  0000 C CNN
	1    3600 2450
	1    0    0    -1  
$EndComp
$EndSCHEMATC
