import sys
import math
from collections import OrderedDict
from operator import itemgetter

units = []
sites = []
site_ids = {} # Keep the index to the sites list 
sites_ordered_distances = []
WAIT_STATE          = 0
MOVE_TO_STATE       = 1
BUILD_STATE         = 2
BUILD_MINE_STATE    = 3

# structure_type: -1 = No structure, 0 = Goldmine, 1 = Tower, 2 = Barracks
STRUCTURE_NONE      = -1
STRUCTURE_FRIENDLY  =  0
STRUCTURE_ENEMY     =  1
# owner: -1 = No structure, 0 = Friendly, 1 = Enemy
OWNER_NONE          = -1
OWNER_FRIENDLY      =  0
OWNER_ENEMY         =  1
# unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER, 2 = GIANT
UNIT_QUEEN          = -1
UNIT_KNIGHT         =  0
UNIT_ARCHER         =  1
UNIT_GIANT          =  2
my_base_pos         = [-1,-1]
b_enable_log        = True
game_state          = BUILD_MINE_STATE

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
num_sites = int(input())
for i in range(num_sites):
    site_id, x, y, radius = [int(j) for j in input().split()]
    sites.append( { "site_id":site_id,
                    "dist_from_start":0, 
                    "pos":[x,y], 
                    "radius":radius, 
                    "owner":-1,
                    "turns_before_new_set":-1,
                    "creep_type":-1,
                    "gold_remaining":-1,
                    "max_mine_size":-1,
                    "structure_type":-1,
                    "gold_mines_count":0
                    } )
    site_ids[site_id] = i

def update_sites(site_id, gold_remaining, max_mine_size, structure_type, owner, param_1, param_2):
    i = site_ids[site_id]
    sites[i]['gold_remaining'] = gold_remaining
    sites[i]['max_mine_size'] = max_mine_size
    sites[i]['structure_type'] = structure_type
    sites[i]['owner'] = owner
    sites[i]['turns_before_new_set'] = param_1
    sites[i]['creep_type'] = param_2

def clear_units_list():
    units = [] # Clear prev units list

def update_units(x, y, owner, unit_type, health):
    units.append( { "pos":[x,y],
                    "owner": owner,
                    "type": unit_type,
                    "health": health
                  } )
    if(my_base_pos[0] == -1 and owner == OWNER_FRIENDLY and unit_type == UNIT_QUEEN):
        my_base_pos[0] = x; my_base_pos[1] = y;

def distance(pos1,pos2):
    return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)

def log(msg):
    if(b_enable_log):
        print("Debug: %s"%msg, file=sys.stderr)

def build_sorted_sites_by_distances():
    if(len(sites_ordered_distances) == 0):
        log("Call build_sorted_sites_by_distances")
        for s in range(len(sites)):
            sites[s]["dist_from_start"] = int(distance(my_base_pos,sites[s]["pos"]))
        for x in sorted (sites, key=itemgetter ('dist_from_start')):
            sites_ordered_distances.append(x)
            log(x)

def game_logic(gold, touched_site):
    global game_state,sites_ordered_distances
    build_sorted_sites_by_distances() # This function will only run once
    if(game_state == BUILD_MINE_STATE): # Initially, build the gold miners
        b_mine_build = False
        idx = 0 # Use as index to modify list entry
        for s in sites_ordered_distances:
            log("idx = %s"%idx)
            if(s["gold_remaining"] > 0): 
                if(s["max_mine_size"] > 1 and s["max_mine_size"] != s["gold_mines_count"]): # Take only miners that are bigger than 1
                    if(touched_site == s["site_id"]):
                        print("BUILD %s MINE"%s["site_id"])
                        sites_ordered_distances[idx]["gold_mines_count"] += 1
                    else:
                        print("MOVE %s %s"%(s["pos"][0],s["pos"][1]))
                    b_mine_build = True
                    break
            else:
                break # Stop after the first group of mines (they are always close to base so they are first in list)
            idx += 1
        if(not b_mine_build):
            game_state = BUILD_STATE
    
    if(game_state == BUILD_STATE):
        print("WAIT")
    #print("MOVE 413 603")
    print("TRAIN")




# game loop
while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    for i in range(num_sites):
        # gold_remaining: -1 if unknown
        # max_mine_size: -1 if unknown
        # structure_type: -1 = No structure, 0 = Goldmine, 1 = Tower, 2 = Barracks
        # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
        site_id, gold_remaining, max_mine_size, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
        update_sites(site_id, gold_remaining, max_mine_size, structure_type, owner, param_1, param_2)

    clear_units_list() 
    
    num_units = int(input())
    for i in range(num_units):
        # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER, 2 = GIANT
        x, y, owner, unit_type, health = [int(j) for j in input().split()]
        update_units(x, y, owner, unit_type, health)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # First line: A valid queen action
    # Second line: A set of training instructions
    #print("WAIT")
    #print("TRAIN")
    game_logic(gold, touched_site)