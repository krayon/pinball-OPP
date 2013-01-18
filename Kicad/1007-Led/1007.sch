EESchema Schematic File Version 2  date 1/18/2013 3:13:57 PM
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
LIBS:1007-cache
EELAYER 25  0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 1
Title "LED"
Date "8 may 2012"
Rev "-"
Comp "Open Pinball Project"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	1300 4000 1300 4050
Connection ~ 2100 3200
Connection ~ 1800 4050
Wire Wire Line
	2100 3000 2100 4050
Wire Wire Line
	1600 4000 1600 4100
Wire Wire Line
	1500 2700 1600 2700
Wire Wire Line
	1600 2700 1600 3200
Wire Wire Line
	1600 3200 2100 3200
Wire Wire Line
	1500 2500 2100 2500
Wire Wire Line
	2100 2500 2100 2600
Connection ~ 1600 4050
Wire Wire Line
	1800 4050 1800 4000
Wire Wire Line
	2100 4050 1300 4050
$Comp
L PWR_FLAG #FLG01
U 1 1 4FA96A10
P 1800 4000
F 0 "#FLG01" H 1800 4095 30  0001 C CNN
F 1 "PWR_FLAG" H 1800 4180 30  0000 C CNN
	1    1800 4000
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 4FA969B9
P 1600 4100
F 0 "#PWR02" H 1600 4100 30  0001 C CNN
F 1 "GND" H 1600 4030 30  0001 C CNN
	1    1600 4100
	1    0    0    -1  
$EndComp
$Comp
L LED D1
U 1 1 4FA968F5
P 2100 2800
F 0 "D1" H 2100 2900 50  0000 C CNN
F 1 "LED" H 2100 2700 50  0000 C CNN
	1    2100 2800
	0    1    1    0   
$EndComp
$Comp
L CONN_2 P1
U 1 1 4FA968D0
P 1150 2600
F 0 "P1" V 1100 2600 40  0000 C CNN
F 1 "CONN_2" V 1200 2600 40  0000 C CNN
	1    1150 2600
	-1   0    0    1   
$EndComp
$Comp
L TST P3
U 1 1 4FA968B6
P 1600 4000
F 0 "P3" H 1600 4300 40  0000 C CNN
F 1 "TST" H 1600 4250 30  0000 C CNN
	1    1600 4000
	1    0    0    -1  
$EndComp
$Comp
L TST P2
U 1 1 4FA968AF
P 1300 4000
F 0 "P2" H 1300 4300 40  0000 C CNN
F 1 "TST" H 1300 4250 30  0000 C CNN
	1    1300 4000
	1    0    0    -1  
$EndComp
$EndSCHEMATC
