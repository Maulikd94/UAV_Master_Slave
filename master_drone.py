#!/usr/bin/env python
# -*- coding: utf-8 -*-

#CODE FOR Master Drone

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import datetime

logname = str(time.time())
f = open(logname, 'w')

header = "Data for flight performed on : " + str(time.ctime()) + "\n\n"

f.write(header)


#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='/dev/ttyACM0')
args = parser.parse_args()

connection_string = args.connect

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, baud=9600, wait_ready=True)

def flightdatalog():
	datas = str(datetime.datetime.now().time()) + " :\t"
	datas = datas + "Location : " + str(vehicle.location.global_relative_frame) + "\t"
	datas = datas + "Groundspeed : " + str(vehicle.groundspeed) + "\t"
	datas = datas + "Airspeed : " + str(vehicle.airspeed) + "\n\n"
	f.write(datas)

def fly():
	print "Going to Waypoint 1"				
        Pnew1 = LocationGlobalRelative(43.004565, -78.785302, 5)	#Drones are 10 m apart
        vehicle.simple_goto(Pnew1, groundspeed=5)
	a = 0
	while a <= 25:
		flightdatalog()
		time.sleep(1)
		a = a + 1
	
	print "Going to Waypoint 2"					#15 m north of initial point
        Pnew2 = LocationGlobalRelative(43.004703, -78.785302, 5)	#Drones are 40 m apart
        vehicle.simple_goto(Pnew2, groundspeed=5)
	b = 0
	while b <= 25:
		flightdatalog()
		time.sleep(1)
		b = b + 1

	print "Going to Waypoint 3"					#30 m north of initial point
        Pnew3 = LocationGlobalRelative(43.004835, -78.785302, 5)	#Drones are 70 m apart
        vehicle.simple_goto(Pnew3, groundspeed=5)
	c = 0
	while c <= 25:
		flightdatalog()
		time.sleep(1)
		c = c + 1
		
	print "Going to Waypoint 4"					#45 m north of initial point
        Pnew4 = LocationGlobalRelative(43.004968, -78.785302, 5)	#Drones are 100 m apart
        vehicle.simple_goto(Pnew4, groundspeed=5)
	d = 0
	while d <= 25:
		flightdatalog()
		time.sleep(1)
		d = d + 1

	#print "Going to Waypoint 5"
        #Pnew5 = LocationGlobalRelative(43.005106, -78.785302, 5)
        #vehicle.simple_goto(Pnew5, groundspeed=5)
	#e = 0
	#while e <= 25:
	#	flightdatalog()
	#	time.sleep(1)
	#	e = e + 1

def arm_and_takeoff(TargetAltitude):
        # Arms vehicle and fly to aTargetAltitude.
        print "Basic pre-arm checks"

        # Don't try to arm until autopilot is ready
        while not vehicle.is_armable:
                print " Waiting for vehicle to initialise..."
                time.sleep(1)

        print "Arming motors"
        # Copter should arm in GUIDED mode
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True    

        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:      
                print " Waiting for arming..."
                time.sleep(1)

        print "Taking off!"
        vehicle.simple_takeoff(TargetAltitude) # Take off to target altitude
	ts = time.time()

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
        #  after Vehicle.simple_takeoff will execute immediately).
        while True:
                print " Altitude: ", vehicle.location.global_relative_frame.alt
                #Break and return from function just below target altitude.        
                if (vehicle.location.global_relative_frame.alt >= TargetAltitude*0.95) or (time.time() - ts >= 10): 
                        print "Reached target altitude"
                        break
                time.sleep(1)
		flightdatalog()

def main():
	arm_and_takeoff(5)

	print "Going to initial point"
        Pnew1 = LocationGlobalRelative(43.004565, -78.785408, 5)	#Standby point to the east of 1st point
        vehicle.simple_goto(Pnew1, groundspeed=5)
	ans = int(input("At P0.. Enter 1 when ready.. Wait for 3 seconds and enter 1 on the 2nd drone\n"))
	time.sleep(4)							#To synchronize timing
	
	oo = 1
	while oo == 1:
                try:
                	fly()
			oo = 0                        
                except KeyboardInterrupt:
			break

        print "Returning to Launch Site..."
	vehicle.mode = VehicleMode("RTL")

main()


print "Closing vehicle object"
vehicle.close()

