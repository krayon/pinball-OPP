EESchema Schematic File Version 2  date 1/18/2013 3:11:53 PM
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
LIBS:1004-cache
EELAYER 25  0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 1
Title "LED Driver"
Date "24 apr 2012"
Rev "-"
Comp "Open Pinball Project"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Connection ~ 7400 2650
Wire Wire Line
	7600 2650 5900 2650
Connection ~ 2600 4600
Wire Wire Line
	6600 4600 1600 4600
Connection ~ 5300 4600
Connection ~ 4800 4600
Connection ~ 7250 4150
Wire Wire Line
	7250 2650 7250 4150
Connection ~ 7000 4350
Wire Wire Line
	7700 4050 7700 4350
Wire Wire Line
	7700 4350 6000 4350
Wire Wire Line
	7500 4050 7500 4450
Wire Wire Line
	7500 4450 5800 4450
Wire Wire Line
	5800 4450 5800 3900
Wire Wire Line
	6900 4050 6900 4250
Wire Wire Line
	6100 3600 6100 4250
Wire Wire Line
	6100 3600 5800 3600
Wire Wire Line
	6700 3300 6600 3300
Wire Wire Line
	6600 3300 6600 3100
Wire Wire Line
	6600 3100 6200 3100
Wire Wire Line
	6200 3100 6200 3300
Wire Wire Line
	6200 3300 5800 3300
Connection ~ 4200 4600
Wire Wire Line
	4200 4600 4200 3900
Wire Wire Line
	6700 3500 6600 3500
Wire Wire Line
	6600 3500 6600 4600
Wire Wire Line
	5900 3150 5900 3800
Wire Wire Line
	5900 3800 5800 3800
Wire Wire Line
	5800 3500 5900 3500
Wire Wire Line
	6400 2550 6400 3200
Connection ~ 3700 4600
Wire Wire Line
	4200 3900 4450 3900
Connection ~ 3000 4000
Wire Wire Line
	2900 3600 3000 3600
Wire Wire Line
	3000 3600 3000 4600
Connection ~ 2300 3900
Wire Wire Line
	2200 3500 2300 3500
Wire Wire Line
	2300 3500 2300 4600
Wire Wire Line
	1500 3800 1600 3800
Wire Wire Line
	1500 3400 1600 3400
Wire Wire Line
	2200 3700 2400 3700
Wire Wire Line
	2400 3700 2400 4200
Wire Wire Line
	2400 4200 4000 4200
Wire Wire Line
	4000 4200 4000 3700
Wire Wire Line
	4000 3700 4450 3700
Wire Wire Line
	3600 3500 4450 3500
Wire Wire Line
	2200 3300 4450 3300
Wire Wire Line
	1500 3200 4450 3200
Wire Wire Line
	2900 3400 4450 3400
Wire Wire Line
	4450 3600 3900 3600
Wire Wire Line
	3900 3600 3900 4100
Wire Wire Line
	3900 4100 1700 4100
Wire Wire Line
	1700 4100 1700 3600
Wire Wire Line
	1700 3600 1500 3600
Wire Wire Line
	4450 3800 4100 3800
Wire Wire Line
	4100 3800 4100 4300
Wire Wire Line
	4100 4300 3100 4300
Wire Wire Line
	3100 4300 3100 3800
Wire Wire Line
	3100 3800 2900 3800
Wire Wire Line
	1600 3400 1600 4600
Wire Wire Line
	2200 3900 2300 3900
Connection ~ 1600 3800
Wire Wire Line
	2900 4000 3000 4000
Connection ~ 2300 4600
Wire Wire Line
	3700 4600 3700 3700
Wire Wire Line
	3700 3700 3600 3700
Connection ~ 3000 4600
Connection ~ 6400 2650
Connection ~ 5900 3500
Wire Wire Line
	6400 3200 5800 3200
Connection ~ 6400 3200
Wire Wire Line
	6400 3600 6400 4600
Connection ~ 6400 4600
Wire Wire Line
	5800 3400 6200 3400
Wire Wire Line
	6200 3400 6200 4150
Wire Wire Line
	6200 4150 6800 4150
Wire Wire Line
	6800 4150 6800 4050
Wire Wire Line
	6100 4250 7600 4250
Wire Wire Line
	7600 4250 7600 4050
Connection ~ 6900 4250
Wire Wire Line
	5800 3700 6000 3700
Wire Wire Line
	6000 3700 6000 4350
Wire Wire Line
	7000 4050 7000 4350
Wire Wire Line
	7100 4050 7100 4150
Wire Wire Line
	7100 4150 7800 4150
Wire Wire Line
	7800 4150 7800 4050
Connection ~ 4600 4600
Connection ~ 5100 4600
Connection ~ 6900 2650
Wire Wire Line
	2600 4600 2600 4750
Connection ~ 7250 2650
$Comp
L SPADE_187 P17
U 1 1 4F771B79
P 7500 2450
F 0 "P17" H 7500 2550 40  0000 C CNN
F 1 "SPADE_187" H 7500 2450 40  0000 C CNN
F 4 "Keystone" H 7500 2450 60  0001 C CNN "Manufacturer"
F 5 "1285" H 7500 2450 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7500 2450 60  0001 C CNN "Distributor"
F 7 "534-1285" H 7500 2450 60  0001 C CNN "Distributor PN"
	1    7500 2450
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG01
U 1 1 4F761609
P 2600 4600
F 0 "#FLG01" H 2600 4695 30  0001 C CNN
F 1 "PWR_FLAG" H 2600 4780 30  0000 C CNN
	1    2600 4600
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 4F761600
P 6900 2650
F 0 "#FLG02" H 6900 2745 30  0001 C CNN
F 1 "PWR_FLAG" H 6900 2830 30  0000 C CNN
	1    6900 2650
	1    0    0    -1  
$EndComp
$Comp
L TST P16
U 1 1 4F7615C4
P 1700 5400
F 0 "P16" H 1700 5700 40  0000 C CNN
F 1 "TST" H 1700 5650 30  0000 C CNN
	1    1700 5400
	1    0    0    -1  
$EndComp
$Comp
L TST P15
U 1 1 4F7615BF
P 1500 5400
F 0 "P15" H 1500 5700 40  0000 C CNN
F 1 "TST" H 1500 5650 30  0000 C CNN
	1    1500 5400
	1    0    0    -1  
$EndComp
$Comp
L TST P14
U 1 1 4F7615B7
P 1300 5400
F 0 "P14" H 1300 5700 40  0000 C CNN
F 1 "TST" H 1300 5650 30  0000 C CNN
	1    1300 5400
	1    0    0    -1  
$EndComp
$Comp
L TST P13
U 1 1 4F7615B0
P 1100 5400
F 0 "P13" H 1100 5700 40  0000 C CNN
F 1 "TST" H 1100 5650 30  0000 C CNN
	1    1100 5400
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P12
U 1 1 4F761375
P 7650 3700
F 0 "P12" V 7600 3700 50  0000 C CNN
F 1 "CONN_4" V 7700 3700 50  0000 C CNN
F 4 "Molex" H 7650 3700 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 7650 3700 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7650 3700 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 7650 3700 60  0001 C CNN "Distributor PN"
	1    7650 3700
	0    -1   -1   0   
$EndComp
$Comp
L SPADE_187 P10
U 1 1 4F7612B7
P 5200 4400
F 0 "P10" H 5200 4500 40  0000 C CNN
F 1 "SPADE_187" H 5200 4400 40  0000 C CNN
F 4 "Keystone" H 5200 4400 60  0001 C CNN "Manufacturer"
F 5 "1285" H 5200 4400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5200 4400 60  0001 C CNN "Distributor"
F 7 "534-1285" H 5200 4400 60  0001 C CNN "Distributor PN"
	1    5200 4400
	1    0    0    -1  
$EndComp
$Comp
L CONN_2 P8
U 1 1 4F7611ED
P 2550 3900
F 0 "P8" V 2500 3900 40  0000 C CNN
F 1 "CONN_2" V 2600 3900 40  0000 C CNN
F 4 "Molex" H 2550 3900 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 2550 3900 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 2550 3900 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 2550 3900 60  0001 C CNN "Distributor PN"
	1    2550 3900
	-1   0    0    1   
$EndComp
$Comp
L CONN_2 P7
U 1 1 4F7611EA
P 1850 3800
F 0 "P7" V 1800 3800 40  0000 C CNN
F 1 "CONN_2" V 1900 3800 40  0000 C CNN
F 4 "Molex" H 1850 3800 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 1850 3800 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 1850 3800 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 1850 3800 60  0001 C CNN "Distributor PN"
	1    1850 3800
	-1   0    0    1   
$EndComp
$Comp
L CONN_2 P6
U 1 1 4F7611E6
P 1150 3700
F 0 "P6" V 1100 3700 40  0000 C CNN
F 1 "CONN_2" V 1200 3700 40  0000 C CNN
F 4 "Molex" H 1150 3700 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 1150 3700 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 1150 3700 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 1150 3700 60  0001 C CNN "Distributor PN"
	1    1150 3700
	-1   0    0    1   
$EndComp
$Comp
L CONN_2 P5
U 1 1 4F7611E3
P 3250 3600
F 0 "P5" V 3200 3600 40  0000 C CNN
F 1 "CONN_2" V 3300 3600 40  0000 C CNN
F 4 "Molex" H 3250 3600 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 3250 3600 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 3250 3600 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 3250 3600 60  0001 C CNN "Distributor PN"
	1    3250 3600
	-1   0    0    1   
$EndComp
$Comp
L CONN_2 P4
U 1 1 4F7611DF
P 2550 3500
F 0 "P4" V 2500 3500 40  0000 C CNN
F 1 "CONN_2" V 2600 3500 40  0000 C CNN
F 4 "Molex" H 2550 3500 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 2550 3500 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 2550 3500 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 2550 3500 60  0001 C CNN "Distributor PN"
	1    2550 3500
	-1   0    0    1   
$EndComp
$Comp
L CONN_2 P3
U 1 1 4F7611DA
P 1850 3400
F 0 "P3" V 1800 3400 40  0000 C CNN
F 1 "CONN_2" V 1900 3400 40  0000 C CNN
F 4 "Molex" H 1850 3400 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 1850 3400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 1850 3400 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 1850 3400 60  0001 C CNN "Distributor PN"
	1    1850 3400
	-1   0    0    1   
$EndComp
$Comp
L CONN_2 P2
U 1 1 4F7611AE
P 1150 3300
F 0 "P2" V 1100 3300 40  0000 C CNN
F 1 "CONN_2" V 1200 3300 40  0000 C CNN
F 4 "Molex" H 1150 3300 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 1150 3300 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 1150 3300 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 1150 3300 60  0001 C CNN "Distributor PN"
	1    1150 3300
	-1   0    0    1   
$EndComp
$Comp
L SPADE_187 P9
U 1 1 4F760F76
P 4700 4400
F 0 "P9" H 4700 4500 40  0000 C CNN
F 1 "SPADE_187" H 4700 4400 40  0000 C CNN
F 4 "Keystone" H 4700 4400 60  0001 C CNN "Manufacturer"
F 5 "1285" H 4700 4400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 4700 4400 60  0001 C CNN "Distributor"
F 7 "534-1285" H 4700 4400 60  0001 C CNN "Distributor PN"
	1    4700 4400
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P11
U 1 1 4F76092A
P 6950 3700
F 0 "P11" V 6900 3700 50  0000 C CNN
F 1 "CONN_4" V 7000 3700 50  0000 C CNN
F 4 "Molex" H 6950 3700 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 6950 3700 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6950 3700 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 6950 3700 60  0001 C CNN "Distributor PN"
	1    6950 3700
	0    -1   -1   0   
$EndComp
$Comp
L 74LV595 U1
U 1 1 4F760826
P 5150 3600
F 0 "U1" H 5150 4200 60  0000 C CNN
F 1 "74LV595" H 5100 4050 60  0000 C CNN
F 4 "NXP" H 5150 3600 60  0001 C CNN "Manufacturer"
F 5 "74LV595N,112" H 5150 3600 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5150 3600 60  0001 C CNN "Distributor"
F 7 "771-LV595N112" H 5150 3600 60  0001 C CNN "Distributor PN"
	1    5150 3600
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 4F7606FE
P 5900 2900
F 0 "R1" V 5980 2900 50  0000 C CNN
F 1 "10K" V 5900 2900 50  0000 C CNN
F 4 "TE Connectivity" H 5900 2900 60  0001 C CNN "Manufacturer"
F 5 "CFR25J10K" H 5900 2900 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 5900 2900 60  0001 C CNN "Distributor"
F 7 "279-CFR25J10K" H 5900 2900 60  0001 C CNN "Distributor PN"
	1    5900 2900
	1    0    0    -1  
$EndComp
$Comp
L C C1
U 1 1 4F7606E1
P 6400 3400
F 0 "C1" H 6450 3500 50  0000 L CNN
F 1 "10uF" H 6450 3300 50  0000 L CNN
F 4 "TDK" H 6400 3400 60  0001 C CNN "Manufacturer"
F 5 "FK18X5R0J106M" H 6400 3400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 6400 3400 60  0001 C CNN "Distributor"
F 7 "810-FK18X5R0J106M" H 6400 3400 60  0001 C CNN "Distributor PN"
	1    6400 3400
	-1   0    0    1   
$EndComp
$Comp
L +3.3V #PWR03
U 1 1 4F76002B
P 6400 2550
F 0 "#PWR03" H 6400 2510 30  0001 C CNN
F 1 "+3.3V" H 6400 2660 30  0000 C CNN
	1    6400 2550
	1    0    0    -1  
$EndComp
$Comp
L CONN_2 P1
U 1 1 4F75FFF8
P 7050 3400
F 0 "P1" V 7000 3400 40  0000 C CNN
F 1 "CONN_2" V 7100 3400 40  0000 C CNN
F 4 "Molex" H 7050 3400 60  0001 C CNN "Manufacturer"
F 5 "22-23-2021" H 7050 3400 60  0001 C CNN "Manufacturer PN"
F 6 "Mouser" H 7050 3400 60  0001 C CNN "Distributor"
F 7 "538-22-23-2021" H 7050 3400 60  0001 C CNN "Distributor PN"
	1    7050 3400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 4F75FFE2
P 2600 4750
F 0 "#PWR04" H 2600 4750 30  0001 C CNN
F 1 "GND" H 2600 4680 30  0001 C CNN
	1    2600 4750
	1    0    0    -1  
$EndComp
$EndSCHEMATC
