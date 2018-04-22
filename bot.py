import sys
import math
import collections

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
sites = {}
mines = {}
distanesFromBase = collections.OrderedDict()
bCalcDistFromBase = True
num_sites = int(input())
target_units=20
nKnights = int(0.5+0.25*(num_sites/2))
nArchers = int(0.5+0.25*(num_sites/2))
nGiants  = 0 #int(0.5+0.3*(num_sites/2))
nTowers  = int(0.5+0.25*(num_sites/2))
nTotalTargetSites = nKnights + nArchers + nGiants + nTowers
bBuildTower = False
firstTowerSite = 0
buildCounter = 0
lastBuilt = -1
for i in range(num_sites):
    site_id, x, y, radius = [int(j) for j in input().split()]
    sites[site_id] = {"pos":(x,y),"radius":radius, "is_barracks":0,"owner":-1,
                    "turns_before_new_set":-1,"creep_type":-1}

def build_knight(siteId):
    print("BUILD %d BARRACKS-KNIGHT"%siteId)
def build_archer(siteId):
    print("BUILD %d BARRACKS-ARCHER"%siteId)
def build_giant(siteId):
    print("BUILD %d BARRACKS-GIANT"%siteId)
def build_tower(siteId):
    print("BUILD %d TOWER"%siteId)
def build_mine(siteId):
    print("BUILD %d MINE"%siteId)    
def move_to(x,y):
    print("MOVE %d %d"%(x,y))
def log(msg):
    #pass
    print("Debug: %s"%msg, file=sys.stderr)
    
def move_nearest(pos):
    min_dist = 10000.0 # Just a big number
    for s in sites:
        if(sites[s]["owner"] == -1): # Currently only go to nearest empty sites
            cdist = math.sqrt((pos[0]-sites[s]["pos"][0])**2+(pos[1]-sites[s]["pos"][1])**2)
            #log("Check site %s at distance %s"%(sites[s],cdist))
            if(cdist<min_dist):
                min_dist = cdist
                ns = sites[s]
                #log("Fonnd site %s at distance %s"%(ns,min_dist))
    move_to(ns["pos"][0], ns["pos"][1])

lastTrained = 0    
def check_mines():
    for m in mines:
        if(mines[m] < 3):
            build_mine(m)
            mines[m] = mines[m] + 1
            return 0
    return 1
    
# game loop
while True:
    train_sites = ""
    total_knights_sites = 0
    total_archers_sites = 0
    total_giants_sites = 0
    total_towers_sites = 0
    total_knights = 0
    total_archers = 0
    total_own_sites = 0

    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    log("gold %s, touched_site %s"%(gold, touched_site))
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
            if(structure_type == 1):
                total_towers_sites += 1
            elif(structure_type == 2):
                if(param_2 == 0): total_knights_sites+=1
                if(param_2 == 1): total_archers_sites+=1
                if(param_2 == 2): total_giants_sites+=1
                if(param_1 == 0  and gold >= 100):
                    if(lastTrained == 0 and param_2 == 0):
                        train_sites += " %s"%(site_id)
                        lastTrained = 1
                        gold -= 100
                    if(lastTrained == 1 and param_2 == 1):
                        train_sites += " %s"%(site_id)
                        lastTrained = 0
                        gold -= 100
    
         
    num_units = int(input())
    units = {}
    for i in range(num_units):
        # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
        x, y, owner, unit_type, health = [int(j) for j in input().split()]
        units[i] = {"pos":(x,y),"unit_type":unit_type, "owner":owner, "health":health}
        log("Unit %s"%units[i])
        if(unit_type == -1):
            if(owner == 0):
                mqid = i
            else:
                eqid = i
        elif(owner == 0):
            if(unit_type == 0):
                total_knights+=1
            else:
                total_archers+=1
    if(bCalcDistFromBase):
        pos = units[mqid]["pos"]
        distanesBase = collections.OrderedDict()
        for s in sites:
            cdist = math.sqrt((pos[0]-sites[s]["pos"][0])**2+(pos[1]-sites[s]["pos"][1])**2)
            distanesBase[int(cdist)] = {"site":sites[s],"id":s}
        distanesSorted = sorted(distanesBase)
        bCalcDistFromBase  = False   
        #log("distanesBase: %s"%distanesBase)
        i = 0
        for d in distanesSorted:
            #log("d=%s i=%s"%(d,i))
            distanesFromBase[i] = distanesBase[d]
            i += 1
        towers = []
        knights = []
        archers = []
        all_creeps = {}
        for i in range(nTotalTargetSites,1,-1): # start from far to near
            if(len(towers) < nTowers):
                towers.append(distanesFromBase[i])
                all_creeps[distanesFromBase[i]["id"]] = "t"
            elif(len(archers) < nArchers):
                archers.append(distanesFromBase[i])
                all_creeps[distanesFromBase[i]["id"]] = "a"
            elif(len(knights) < nKnights):
                knights.append(distanesFromBase[i])
                all_creeps[distanesFromBase[i]["id"]] = "k"
        #log("distanesFromBase: %s"%distanesFromBase)
        all_creeps[distanesFromBase[0]["id"]] = "m"
        all_creeps[distanesFromBase[1]["id"]] = "m"
        mines[distanesFromBase[0]["id"]] = 0
        mines[distanesFromBase[1]["id"]] = 0
        log("towers = %s"%towers)
        log("knights = %s"%knights)
        log("archers = %s"%archers)
        log("all_creeps = %s"%all_creeps)
     
    # Write an action using print
    # To debug:
    log("total_knights: %s total_archers: %s num of units: %s"%(total_knights,total_archers,num_units))
    #if(total_knights + total_archers < target_units and total_own_sites < num_sites/2):
    if(total_own_sites < nTotalTargetSites): # Need to build more sites
        bNeedBuild = True
        if(not check_mines()):
            bNeedBuild = False
        if(bNeedBuild and
            touched_site in all_creeps and
            lastBuilt != touched_site
            and sites[touched_site]["owner"] != 0):
                if(all_creeps[touched_site] == 't'):
                    build_tower(touched_site)
                if(all_creeps[touched_site] == 'a'):
                    build_archer(touched_site)
                if(all_creeps[touched_site] == 'k'):
                    build_knight(touched_site)   
                if(all_creeps[touched_site] == 'm'):
                    build_mine(touched_site)
                    mines[touched_site] = 1
                #print("WAIT")
                lastBuilt = touched_site
                bNeedBuild = False
    
        if(bNeedBuild and buildCounter%3 == 0):
            for t in knights:
                if(t["site"]["owner"] != 0):
                    lastBuilt = t["id"]
                    build_knight(t["id"])
                    bNeedBuild = False
                    break
        if(bNeedBuild and buildCounter%3 == 1):
            for t in archers:
                if(t["site"]["owner"] != 0):
                    lastBuilt = t["id"]
                    build_archer(t["id"])
                    bNeedBuild = False
                    break
        if(bNeedBuild and buildCounter%3 == 2):
            for t in towers:
                if(t["site"]["owner"] != 0):
                    lastBuilt = t["id"]
                    build_tower(t["id"])
                    bNeedBuild = False
                    break
        #log("touched_site = %s lastBuilt = %s  touched_site in all_creeps: %s"%(touched_site,lastBuilt,touched_site in all_creeps))
        #if(touched_site in all_creeps):
        #   log("bNeedBuild %s all_creeps[touched_site] = %s"%(bNeedBuild,all_creeps[touched_site]))
        if(touched_site == lastBuilt):
            buildCounter += 1
        if(bNeedBuild):
            if(check_mines()):
                print("WAIT")
    else:
        if(check_mines()):
            print("WAIT")
    ''' - Prev code
    if(total_own_sites < nTotalTargetSites): # Need to build more sites
        if(touched_site == -1 or sites[touched_site]["owner"] == 0):
            move_nearest(units[mqid]["pos"])
        else: # Build waht is missing order by priority
            if(total_towers_sites < nTowers and bBuildTower):
                build_tower(touched_site)
            elif(total_knights_sites < nKnights):
                build_knight(touched_site)
                firstTowerSite = touched_site
            elif(total_archers_sites < nArchers):
                build_archer(touched_site)
            elif(total_giants_sites < nGiants):
                build_giant(touched_site)
            else:
                if(firstTowerSite):
                    p = sites[firstTowerSite]["pos"]
                    move_to(p[0],p[1])
                else:
                    print("WAIT")
            bBuildTower = not bBuildTower
    else:    
        print("WAIT")
    '''
    # First line: A valid queen action
    # Second line: A set of training instructions
    print("TRAIN%s"%train_sites)
