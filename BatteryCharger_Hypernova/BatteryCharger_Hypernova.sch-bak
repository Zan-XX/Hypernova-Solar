EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Simulation_SPICE:VSIN V_AC
U 1 1 62E4D079
P 1050 1550
F 0 "V_AC" H 1180 1550 50  0001 L CNN
F 1 "240V 60 Hz" H 1180 1505 50  0001 L CNN
F 2 "" H 1050 1550 50  0001 C CNN
F 3 "~" H 1050 1550 50  0001 C CNN
F 4 "Y" H 1050 1550 50  0001 L CNN "Spice_Netlist_Enabled"
F 5 "V" H 1050 1550 50  0001 L CNN "Spice_Primitive"
F 6 "" H 1180 1459 50  0000 L CNN "Spice_Model"
	1    1050 1550
	1    0    0    -1  
$EndComp
$Comp
L Device:Transformer_1P_1S T1
U 1 1 62E4D98E
P 2100 1550
F 0 "T1" H 2100 1839 50  0000 C CNN
F 1 "1.64:1" H 2100 1840 50  0001 C CNN
F 2 "" H 2100 1550 50  0001 C CNN
F 3 "~" H 2100 1550 50  0001 C CNN
	1    2100 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	1050 1350 1700 1350
Wire Wire Line
	1050 1750 1700 1750
$Comp
L Device:D_Bridge_+-AA D1
U 1 1 62E57352
P 2950 1550
F 0 "D1" H 3294 1596 50  0001 L CNN
F 1 "FBR" H 3294 1550 50  0000 L CNN
F 2 "" H 2950 1550 50  0001 C CNN
F 3 "~" H 2950 1550 50  0001 C CNN
	1    2950 1550
	1    0    0    -1  
$EndComp
$Comp
L Device:CP1 C1
U 1 1 62E599BA
P 3650 1550
F 0 "C1" H 3765 1550 50  0000 L CNN
F 1 "CP1" H 3765 1505 50  0001 L CNN
F 2 "" H 3650 1550 50  0001 C CNN
F 3 "~" H 3650 1550 50  0001 C CNN
	1    3650 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 1200 3650 1400
Wire Wire Line
	2500 1350 2500 1250
Wire Wire Line
	2500 1250 2950 1250
Wire Wire Line
	3250 1550 3250 1200
Wire Wire Line
	3250 1200 3650 1200
Wire Wire Line
	2650 1900 2650 1550
Wire Wire Line
	3650 1700 3650 1900
Wire Wire Line
	3650 1900 2650 1900
Wire Wire Line
	2500 1750 2500 1850
Wire Wire Line
	2500 1850 2950 1850
$Comp
L power:Earth #PWR?
U 1 1 62E763F0
P 3650 1950
F 0 "#PWR?" H 3650 1700 50  0001 C CNN
F 1 "Earth" H 3650 1800 50  0001 C CNN
F 2 "" H 3650 1950 50  0001 C CNN
F 3 "~" H 3650 1950 50  0001 C CNN
	1    3650 1950
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R_SHUNT
U 1 1 62E5FF1E
P 4050 1200
F 0 "R_SHUNT" V 3937 1200 50  0000 C CNN
F 1 "R_US" V 3936 1200 50  0001 C CNN
F 2 "" V 4090 1190 50  0001 C CNN
F 3 "~" H 4050 1200 50  0001 C CNN
	1    4050 1200
	0    1    1    0   
$EndComp
Wire Wire Line
	3900 1200 3650 1200
Connection ~ 3650 1200
Wire Wire Line
	4200 1200 4650 1200
Wire Wire Line
	4650 1900 3650 1900
Connection ~ 3650 1900
$Comp
L power:Earth_Protective #PWR?
U 1 1 62E6C31C
P 1050 1750
F 0 "#PWR?" H 1300 1500 50  0001 C CNN
F 1 "Earth_Protective" H 1500 1600 50  0001 C CNN
F 2 "" H 1050 1650 50  0001 C CNN
F 3 "~" H 1050 1650 50  0001 C CNN
	1    1050 1750
	1    0    0    -1  
$EndComp
Connection ~ 1050 1750
Wire Wire Line
	3650 1900 3650 1950
Text GLabel 3250 1100 0    50   Input ~ 0
V_DC
$Comp
L Device:Voltage_Divider_CenterPin3 RN1
U 1 1 62E69C2D
P 4650 1550
F 0 "RN1" H 4570 1550 50  0000 R CNN
F 1 "R1-220k R2-10k" H 4570 1505 50  0001 R CNN
F 2 "" V 5125 1550 50  0001 C CNN
F 3 "~" H 4850 1550 50  0001 C CNN
	1    4650 1550
	1    0    0    -1  
$EndComp
Text GLabel 4800 1550 2    50   Input ~ 0
V_sense
Wire Wire Line
	4650 1900 4650 1800
Wire Wire Line
	4650 1300 4650 1200
Wire Wire Line
	4650 1200 5300 1200
Connection ~ 4650 1200
Wire Wire Line
	4650 1900 5300 1900
Connection ~ 4650 1900
Text GLabel 3800 1200 1    50   Input ~ 0
I_sense+
Text GLabel 4300 1200 1    50   Input ~ 0
I_sense-
Wire Wire Line
	3250 1100 3250 1200
Connection ~ 3250 1200
Text GLabel 1050 1250 0    50   Input ~ 0
V_AC
Wire Wire Line
	1050 1250 1050 1350
Connection ~ 1050 1350
Text Notes 1000 2400 0    79   ~ 0
For Vr = +- 1V, C1 must be ~~200 mF\nV_sense and I_sense will range from 0V to 5V
$EndSCHEMATC
