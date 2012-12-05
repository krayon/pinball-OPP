EESchema Schematic File Version 2  date 12/5/2012 11:19:56 AM
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
LIBS:1008-cache
EELAYER 25  0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 5
Title "Display Driver"
Date "5 dec 2012"
Rev "A"
Comp "Open Pinball Project"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
NoConn ~ 3100 7650
NoConn ~ 2900 7650
NoConn ~ 2700 7650
NoConn ~ 2500 7650
$Comp
L TST P107
U 1 1 50A823B7
P 3100 7650
F 0 "P107" H 3100 7950 40  0000 C CNN
F 1 "TST" H 3100 7900 30  0000 C CNN
	1    3100 7650
	1    0    0    -1  
$EndComp
$Comp
L TST P106
U 1 1 50A823B5
P 2900 7650
F 0 "P106" H 2900 7950 40  0000 C CNN
F 1 "TST" H 2900 7900 30  0000 C CNN
	1    2900 7650
	1    0    0    -1  
$EndComp
$Comp
L TST P105
U 1 1 50A823B2
P 2700 7650
F 0 "P105" H 2700 7950 40  0000 C CNN
F 1 "TST" H 2700 7900 30  0000 C CNN
	1    2700 7650
	1    0    0    -1  
$EndComp
$Comp
L TST P104
U 1 1 50A823A8
P 2500 7650
F 0 "P104" H 2500 7950 40  0000 C CNN
F 1 "TST" H 2500 7900 30  0000 C CNN
	1    2500 7650
	1    0    0    -1  
$EndComp
Text Notes 2450 7250 0    60   ~ 0
Mounting Holes
Text Notes 1500 7250 0    60   ~ 0
Fiducials
$Sheet
S 2800 1250 600  300 
U 509EF7B0
F0 "disp3" 60
F1 "1008.disp3.sch" 60
$EndSheet
$Sheet
S 1750 1250 600  300 
U 509EF789
F0 "disp2" 60
F1 "1008.disp2.sch" 60
$EndSheet
$Sheet
S 700  1250 600  300 
U 5094A811
F0 "disp1" 60
F1 "1008.disp1.sch" 60
$EndSheet
$Sheet
S 700  750  600  300 
U 5094A63B
F0 "processor" 60
F1 "1008.proc.sch" 60
$EndSheet
NoConn ~ 1900 7650
NoConn ~ 1700 7650
NoConn ~ 1500 7650
$Comp
L TST P103
U 1 1 4F79A529
P 1900 7650
F 0 "P103" H 1900 7950 40  0000 C CNN
F 1 "TST" H 1900 7900 30  0000 C CNN
	1    1900 7650
	1    0    0    -1  
$EndComp
$Comp
L TST P102
U 1 1 4F79A521
P 1700 7650
F 0 "P102" H 1700 7950 40  0000 C CNN
F 1 "TST" H 1700 7900 30  0000 C CNN
	1    1700 7650
	1    0    0    -1  
$EndComp
$Comp
L TST P101
U 1 1 4F79A514
P 1500 7650
F 0 "P101" H 1500 7950 40  0000 C CNN
F 1 "TST" H 1500 7900 30  0000 C CNN
	1    1500 7650
	1    0    0    -1  
$EndComp
$EndSCHEMATC
