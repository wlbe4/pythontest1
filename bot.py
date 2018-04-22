import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
bBuildKnight = 1
total_own_sites = 0
total_knights = 0
total_archers = 0
sites = {}
num_sites = int(input())
target_units=num_sites*2

for i in range(num_sites):
	site_id, x, y, radius = [int(j) for j in input().split()]
	sites[site_id] = {"pos":(x,y),"radius":radius, "is_barracks":0,"owner":-1,
                  	"turns_before_new_set":-1,"creep_type":-1}
def build_knight(siteId):
	print("BUILD %d BARRACKS-KNIGHT"%siteId)
def build_archer(siteId):
	print("BUILD %d BARRACKS-ARCHER"%siteId)
def move_to(x,y):
	print("MOVE %d %d"%(x,y))

def move_nearest(pos):
	min_dist = 10000.0 # Just a big number
	for s in sites:
    	if(sites[s]["owner"] == -1): # Currently only go to nearest empty sites
        	cdist = math.sqrt((pos[0]-sites[s]["pos"][0])**2+(pos[1]-sites[s]["pos"][1])**2)
        	if(cdist<min_dist):
            	min_dist = cdist
            	ns = sites[s]
	move_to(ns["pos"][0], ns["pos"][1])
    
# game loop
while True:
	train_sites = ""
	# touched_site: -1 if none
	gold, touched_site = [int(i) for i in input().split()]
	for i in range(num_sites):
    	# ignore_1: used in future leagues
    	# ignore_2: used in future leagues
    	# structure_type: -1 = No structure, 2 = Barracks
    	# owner: -1 = No structure, 0 = Friendly, 1 = Enemy
    	site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
    	sites[site_id]["is_barracks"] = structure_type == 2
    	sites[site_id]["owner"] = owner
    	sites[site_id]["turns_before_new_set"] = param_1
    	sites[site_id]["creep_type"] = param_2
    	if(owner == 0):
        	total_own_sites += 1
        	if(param_1 == 0):
            	train_sites += " %s"%(site_id)
       	 
	num_units = int(input())
	units = {}
	for i in range(num_units):
    	# unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
    	x, y, owner, unit_type, health = [int(j) for j in input().split()]
    	units[i] = {"pos":(x,y),"unit_type":unit_type, "health":health}
    	if(unit_type == -1):
        	if(owner == 0):
            	mqid = i
        	else:
            	eqid = i
    	elif(owner == 0):
        	if(unit_type == 0):
            	total_knights+=4
        	else:
            	total_archers+=2
	# Write an action using print
	# To debug:
	if(total_knights + total_archers < target_units):
    	if(touched_site == -1):
        	move_nearest(units[mqid]["pos"])
    	elif(bBuildKnight):
        	build_knight(touched_site)
        	bBuildKnight = 0
    	else:
        	build_archer(touched_site)
        	bBuildKnight = 1
	else:    
    	print("WAIT")
	# First line: A valid queen action
	# Second line: A set of training instructions
	print("TRAIN%s"%train_sites)

