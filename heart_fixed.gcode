;PancakePainter v1.4.0 GCODE header start
;Originally generated @ Wed Dec 03 2025 14:24:27 GMT+0100 (CET)
;Modified for Marlin 2.0.7.2 with Z-axis valve control
;Settings used to generate this file:
;----------------------------------------
;botSpeed: 4620
;flattenResolution: 2
;lineEndPreShutoff: 21
;startWait: 197
;endWait: 250
;shadeChangeWait: 20
;useLineFill: false
;useShortest: true
;shapeFillWidth: 1.2
;fillSpacing: 17
;fillAngle: -39
;fillGroupThreshold: 13
;useColorSpeed: false
;botColorSpeed: 6600,5280,5280,3300
;----------------------------------------
;W1 X42 Y210 L485 T0 ;Define Workspace (commented out for Marlin compatibility)
;Adjusted for printer limits: X=200mm, Y=192mm
;Z-axis valve control: Z-10 = open, Z+10 = close
G21 ;Set units to MM
G1 F4620 ;Set Speed
G00 Z10 ;Valve closed (move up)
G4 P1000 ;Pause for 1000 milliseconds
M84 ;Motors off
G00 X1 Y1 ;Help homing
G28 X0 Y0 ;Home All Axis
;PancakePainter header complete
;Starting stroke path #1/1, segments: 25, length: 653, color #1
;Coordinates scaled and centered to fit within X:200mm, Y:192mm
G00 X144.032 Y85.622
G00 Z-10 ;Valve open (move down)
G4 P197 ;Pause for 197 milliseconds
G00 X144.032 Y79.023
G00 X147.493 Y70.482
G00 X150.158 Y66.429
G00 X153.563 Y63.626
G00 X155.279 Y63.289
G00 X158.145 Y63.062
G00 X163.095 Y62.892
G00 X164.645 Y62.877
G00 X167.622 Y62.851
G00 X170.535 Y62.845
G00 X171.894 Y62.892
G00 X173.079 Y65.724
G00 X173.209 Y69.636
G00 X173.36 Y76.823
G00 X174.122 Y85.977
G00 X171.16 Y94.42
G00 X170.427 Y96.62
G00 X166.028 Y101.752
G00 X164.562 Y106.151
G00 X163.095 Y107.618
G00 X157.963 Y118.616
G00 X153.597 Y128.426
G00 X147.698 Y136.212
G00 X146.365 Y135.939
G00 X145.085 Y133.563
G00 X144.012 Y130.679
G00 X143.299 Y128.88
G00 X133.034 Y116.416
G00 X124.235 Y109.817
G00 X119.836 Y107.618
G00 X116.238 Y103.25
G00 X114.519 Y99.151
G00 X113.993 Y94.519
G00 X113.971 Y88.554
G00 X113.971 Y81.222
G00 X115.854 Y78.436
G00 X118.727 Y77.157
G00 X125.702 Y76.823
G00 X127.933 Y76.683
G00 X130.101 Y76.823
G00 X134.5 Y80.489
;Nearing path end, moving to preshutoff position
G00 X137.034 Y84.29
G00 Z10 ;Valve closed (move up)
G00 X137.433 Y84.888
G00 X139.633 Y84.888
G00 X142.125 Y85.547
G00 X144.032 Y85.622
G4 P250 ;Pause for 250 milliseconds
;Completed path #1/1 on color #1
;PancakePainter Footer Start
G4 P1000 ;Pause for 1000 milliseconds
G00 X1 Y1 ;Help homing
G28 X0 Y0 ;Home All Axis
M84 ;Motors off
;PancakePainter Footer Complete
