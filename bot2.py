import sys
import math
from collections import OrderedDict
from operator import itemgetter
'''
Issues: 
1. Many mines are built
2. Some times stuck between 2 sites like a ping pong
3. When enemy creeps touch my site I have just built, I am stuck in a loop building again and they destroy again...
'''
units = []
sites = []

sites_ordered_distances = []

# structure_type: -1 = No structure, 0 = Goldmine, 1 = Tower, 2 = Barracks
STRUCTURE_NONE      = -1
STRUCTURE_GOLDMINE  =  0
STRUCTURE_TOWER     =  1
STRUCTURE_BARRACKS  =  2

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
my_queen_id         = -1
b_enable_log        = True
game_strategy       = {}

SITE_TYPE_GOLDMINE  =  0
SITE_TYPE_TOWER     =  1
SITE_TYPE_KNIGHT    =  2
SITE_TYPE_ARCHER    =  3
SITE_TYPE_GIANT     =  4

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
                    "income_rate":-1,
                    "creep_type":-1,
                    "gold_remaining":-1,
                    "max_mine_size":-1,
                    "structure_type":-1,
                    "gold_mines_count":0
                    } )

def log(msg):
    if(b_enable_log):
        print("Debug: %s"%msg, file=sys.stderr)
def build_knight(siteId,touched_site):
    if(siteId == touched_site):        print("BUILD %d BARRACKS-KNIGHT"%siteId)
    else:        print("MOVE %s %s"%(sites[siteId]["pos"][0],sites[siteId]["pos"][1]))
def build_archer(siteId,touched_site):
    if(siteId == touched_site):        print("BUILD %d BARRACKS-ARCHER"%siteId)
    else:        print("MOVE %s %s"%(sites[siteId]["pos"][0],sites[siteId]["pos"][1]))
def build_giant(siteId,touched_site):
    if(siteId == touched_site):        print("BUILD %d BARRACKS-GIANT"%siteId)
    else:        print("MOVE %s %s"%(sites[siteId]["pos"][0],sites[siteId]["pos"][1]))
def build_tower(siteId,touched_site):
    if(siteId == touched_site):        print("BUILD %d TOWER"%siteId)
    else:        print("MOVE %s %s"%(sites[siteId]["pos"][0],sites[siteId]["pos"][1]))
def build_mine(siteId,touched_site):
    if(siteId == touched_site):        print("BUILD %d MINE"%siteId)   
    else:        print("MOVE %s %s"%(sites[siteId]["pos"][0],sites[siteId]["pos"][1]))

def update_sites(site_id, gold_remaining, max_mine_size, structure_type, owner, param_1, param_2):
    global sites    
    #log("site_id = %s gold_remaining = %s"%(site_id,gold_remaining)) 
    sites[site_id]['gold_remaining'] = gold_remaining
    sites[site_id]['max_mine_size'] = max_mine_size
    sites[site_id]['structure_type'] = structure_type
    sites[site_id]['owner'] = owner
    sites[site_id]['turns_before_new_set'] = param_1
    sites[site_id]['income_rate'] = param_1 # When type is a mine, param_1 tells the income_rate
    sites[site_id]['creep_type'] = param_2
    if(owner == OWNER_NONE):  sites[site_id]['gold_mines_count'] = 0

def get_my_total_sites():
    my_sites_count_dict = {
    SITE_TYPE_GOLDMINE : [],
    SITE_TYPE_TOWER    : [],
    SITE_TYPE_KNIGHT   : [],
    SITE_TYPE_ARCHER   : [],
    SITE_TYPE_GIANT    : []
    }

    for i in range(len(sites)):
        if(sites[i]["owner"] == OWNER_FRIENDLY):
            if(sites[i]["structure_type"] == STRUCTURE_GOLDMINE):
                my_sites_count_dict[SITE_TYPE_GOLDMINE].append(i)
            elif(sites[i]["structure_type"] == STRUCTURE_TOWER):
                my_sites_count_dict[SITE_TYPE_TOWER].append(i)
            elif(sites[i]["structure_type"] == STRUCTURE_BARRACKS):
                if(sites[i]["creep_type"] == UNIT_KNIGHT):
                    my_sites_count_dict[SITE_TYPE_KNIGHT].append(i)
                elif(sites[i]["creep_type"] == UNIT_ARCHER):
                    my_sites_count_dict[SITE_TYPE_ARCHER].append(i)
                elif(sites[i]["creep_type"] == UNIT_GIANT):
                    my_sites_count_dict[SITE_TYPE_GIANT].append(i)             
    return my_sites_count_dict

def clear_units_list():
    units = [] # Clear prev units list

def update_units(x, y, owner, unit_type, health):
    global my_base_pos
    units.append( { "pos":[x,y],
                    "owner": owner,
                    "type": unit_type,
                    "health": health
                  } )
    if(owner == OWNER_FRIENDLY and unit_type == UNIT_QUEEN):   
        my_queen_pos = [x,y] 
        if(my_base_pos[0] == -1): # update base possision only once    
            my_base_pos = my_queen_pos

def get_my_total_creeps():
    my_units_count_dict = {UNIT_QUEEN:0,UNIT_GIANT:0,UNIT_ARCHER:0,UNIT_KNIGHT:0}
    for i in range(len(units)):
        if(units[i]["owner"] == OWNER_FRIENDLY):
            my_units_count_dict[units[i]["type"]] += 1
    return my_units_count_dict

def distance(pos1,pos2):
    return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)


def build_sorted_sites_by_distances():
    if(len(sites_ordered_distances) == 0):
        log("Call build_sorted_sites_by_distances")
        for s in range(len(sites)):
            sites[s]["dist_from_start"] = int(distance(my_base_pos,sites[s]["pos"]))
        for x in sorted (sites, key=itemgetter ('dist_from_start')):
            sites_ordered_distances.append(x)
            #log(x)

def clear_board_settings():
    game_strategy[SITE_TYPE_GOLDMINE]   = []
    game_strategy[SITE_TYPE_TOWER]      = []
    game_strategy[SITE_TYPE_KNIGHT]     = []
    game_strategy[SITE_TYPE_ARCHER]     = []
    game_strategy[SITE_TYPE_GIANT]      = []

def set_creep_on_board(creep_site,site_id):
    game_strategy[creep_site].append(site_id)

def check_needed_creep(creep_site,site_id,cnt):
    if(len(game_strategy[creep_site]) < cnt):
        set_creep_on_board(creep_site,site_id)
        return True
    return False

def set_game_strategy(gold, touched_site):
    # Set the board and decide how many creeps, gold miners, towers to use and where to locate them
    clear_board_settings()
    same_creeps_count = int(1 + 0.23*num_sites) ## Currently, strategy will be to build same number 
    t_cnt = same_creeps_count
    k_cnt = same_creeps_count
    a_cnt = same_creeps_count
    set_creep_on_board(SITE_TYPE_KNIGHT,sites_ordered_distances[0]["site_id"]) # First set 1 knight so it can start training
    # The order of the if-elif-elif sets which types will be closer to base and which will be further along
    for idx in range(1,num_sites):
        s = sites_ordered_distances[idx]
        # Allocate index 2 for archers
        if(idx != 2 and s["gold_remaining"] > 0 and s["max_mine_size"] > 1 and s["max_mine_size"] != s["gold_mines_count"]): # Take only miners that are bigger than 1
            set_creep_on_board(SITE_TYPE_GOLDMINE,s["site_id"])
        elif(check_needed_creep(SITE_TYPE_ARCHER, s["site_id"],a_cnt)):
            continue
        elif(check_needed_creep(SITE_TYPE_KNIGHT, s["site_id"],a_cnt)):
            continue
        elif(check_needed_creep(SITE_TYPE_TOWER,  s["site_id"],a_cnt)):
            continue

def check_build_need(my_sites, site_type):
    cnt_sites_type = len(my_sites[site_type])
    if(len(game_strategy[site_type]) > cnt_sites_type):
        for a in game_strategy[site_type]:
            if (a not in my_sites[site_type]):
                return cnt_sites_type, a
            elif (site_type == SITE_TYPE_GOLDMINE and sites[a]["income_rate"] < sites[a]["max_mine_size"]):
                return cnt_sites_type-1, a # Still need to build another mine on the same site because we better maximize the total gold miners
    else:
        return cnt_sites_type, -1

def train_strategy(gold,my_sites,my_creeps):
    train_sites = ""
    # Simple training strategy, spead the gold evenly:
    knight_sites = len(my_sites[SITE_TYPE_KNIGHT])
    archer_sites = len(my_sites[SITE_TYPE_ARCHER])
    if(gold <= 180):
        if(archer_sites > 0 and my_creeps[UNIT_ARCHER] < my_creeps[UNIT_KNIGHT]):
            gold_for_knights = 0
            gold_for_archers = gold
        else:            
            gold_for_knights = gold
            gold_for_archers = 0
    else:
        gold_for_knights = int(gold*80/180)
        gold_for_archers = int(gold*100/180)
    for site_id in my_sites[SITE_TYPE_KNIGHT]:
        if(gold_for_knights >= 80):
            train_sites += " %s"%(site_id)
            gold_for_knights -= 80
    gold_for_archers += gold_for_knights # Take residual gold from knight training allocation
    for site_id in my_sites[SITE_TYPE_ARCHER]:
        if(gold_for_archers >= 100):
            train_sites += " %s"%(site_id)
            gold_for_archers -= 100
    print("TRAIN%s"%train_sites)

def apply_stategy(gold, touched_site):
    my_creeps = get_my_total_creeps()
    my_sites = get_my_total_sites()

    archer_sites, s_archer_id = check_build_need(my_sites, SITE_TYPE_ARCHER) 
    knight_sites, s_knight_id = check_build_need(my_sites, SITE_TYPE_KNIGHT) 
    tower_sites, s_tower_id = check_build_need(my_sites, SITE_TYPE_TOWER)
    goldmine_sites, s_mine_id =  check_build_need(my_sites, SITE_TYPE_GOLDMINE)
    # Now that we know what is still needed to be built we can start bulit them by priority
    # Currently, simple strategy: start with the closest.
    # Since set_game_strategy set goldmine and archers first we will start with those.
    # But... Before we do, lets make the first one a knight:
    if(not game_strategy[SITE_TYPE_KNIGHT][0] in my_sites[SITE_TYPE_KNIGHT]):
        build_knight(game_strategy[SITE_TYPE_KNIGHT][0],touched_site)
    elif(goldmine_sites == 1 and archer_sites == 0 and s_archer_id > -1): build_archer(s_archer_id,touched_site)
    elif(s_mine_id > -1):   build_mine(s_mine_id,touched_site)
    elif(s_archer_id > -1): build_archer(s_archer_id,touched_site)
    elif(s_knight_id > -1): build_knight(s_knight_id,touched_site)
    elif(s_tower_id > -1):  build_tower(s_tower_id,touched_site)
    else: print("WAIT")
    train_strategy(gold,my_sites,my_creeps)

def game_logic(gold, touched_site):
    build_sorted_sites_by_distances() # This function will only run once
    set_game_strategy(gold, touched_site) # Decide how to layout the board according current condition
    apply_stategy(gold, touched_site)
    #print("WAIT")
    #print("TRAIN")




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

    game_logic(gold, touched_site)