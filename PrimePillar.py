#!/usr/bin/env python

#open relevent files
gcode = open("test_cone_no_prime_pil.gcode", 'r')
new_gcode = open("cone_new.gcode", "w")

#write file to a list variable
gcode_list = gcode.readlines()

object_z_height = .2
pillar_z_height = 20

prime_pillar_bool = True
DEBUG = False

#Loop to remove extra extrusion, extrusion inserted with each prime pillar
while  "G1 E120.0000 F90000\n" in gcode_list:
    gcode_list.remove("G1 E120.0000 F90000\n")

for i in range(len(gcode_list)):
    # Get Z layer height of object and assign it to variable
    if "Z =" in gcode_list[i]: object_z_height =  gcode_list[i][16:23]     

    # Open prime pillar gcode file and assign it to a variable
    prime = open("prime_pillar.txt","r")
    prime_list = prime.readlines()
    prime.close()
    

    # Loop to change the prime pillars z height as it grows
    if prime_pillar_bool:
        prime_count = 0
        if DEBUG: print("Creating prime pillar layer")
        for j in range(len(prime_list)):
            if "G1 Z" in prime_list[j] and prime_count == 0:
                prime_count += 1
                del prime_list[j]
                prime_list.insert(j, "G1 Z"+str(pillar_z_height/100)[0:6]+" F1002\n")
            elif "G1 Z" in prime_list[j] and prime_count == 1:
                prime_count += 1
                del prime_list[j]
                prime_list.insert(j, "G1 Z"+str((pillar_z_height+25)/100)[0:6]+" F1002\n")
            elif "G1 Z" in prime_list[j] and prime_count == 2:
                prime_count += 1
                del prime_list[j]
                prime_list.insert(j, "G1 Z"+str(pillar_z_height/100)[0:6]+" F1002\n")
            elif "G1 Z" in prime_list[j] and prime_count == 3:
                prime_count += 1
                del prime_list[j]
                prime_list.insert(j, "G1 Z"+str(object_z_height)[0:6].rstrip()+" F1002")

        #write list with new z values back to prime pillar txt file
        prime = open("prime_pillar.txt", "w")
        prime.write(''.join(str(line) for line in prime_list))
        prime.close()        

    prime_pillar_bool = False

    #Insert prime pillar gcode when file reads a tool change line
    prime = open("prime_pillar.txt","r")
    if gcode_list[i] == "T1\n" or gcode_list[i] == "T0\n":
        if DEBUG: print("prime pillar added.  The pillar height is: " + str(pillar_z_height/100)[0:5])
        gcode_list.insert(i+1,prime.read()+'\n')
        pillar_z_height += 20
        prime_pillar_bool = True
    prime.close()

#write new new gcode to a new file
new_gcode.write(''.join(str(line) for line in gcode_list))

#close remaining files
gcode.close()
new_gcode.close()

