
from random import randint
import random


# Variables
ct_bias = 60
t_bias = 40

# Classes


class Player:
    """
    Class for cs player.
    Contains:-
    Name
    Rating [0-200]
    """

    def __init__(self, name, r=None):
        self.name = name
        self.rating = r
        if r is None:
            r = randint(0, 200)
        if r < 0:
            self.rating = 0
        elif r > 200:
            self.rating = 200
        else:
            self.rating = r


    def incRating(self):
        if self.rating < 200:
            self.rating += 1

    def decRating(self):
        if self.rating > 0:
            self.rating -= 1


class Team:
    """
    Class for CS team.
    Contains:-
    teamName
    teamRating
    teamPlayers
    """

    def __init__(self,name):
        self.teamName = name
        self.teamRating = 0
        self.teamPlayers =[]


    def calcRating(self):
        """Calculate average rating of players in team -> team rating"""
        totalRat = sum(player.rating for player in self.teamPlayers)
        numPlyrs = len(self.teamPlayers)
        self.teamRating = round(totalRat / numPlyrs)

    def addPlayer(self,plyr):
        self.teamPlayers.append(plyr)


class Match:
    """
    Class for matches
    Contains:-
    mID
    teamA
    teamB
    bestOf
    maps
    rounds
    """

    def __init__(self,mID,teamA,teamB,bo=1,maps=None,friendly=False):
        self.mID = mID
        assert isinstance(teamA, Team)
        self.teamA = teamA
        assert isinstance(teamB, Team)
        self.teamB = teamB
        self.bestOf = bo
        self.maps = maps
        if self.maps is None:
            self.maps = []
        self.friendly = friendly

    def addMap(self,name):
        if len(self.maps) <= self.bestOf:
            new_map = Map(name, self.teamA, self.teamB,self.friendly)
            self.maps.append(new_map)
        else:
            print('Too many maps')

    def removeMap(self,map):
        self.maps.remove(map)

    def knifeRound(self):
        chance_A = 0
        chance_B = 0
        while chance_A == chance_B:
            chance_A = random.random()
            chance_B = random.random()
            #First team returned will be CT (assumes winner chooses CT)
            if chance_A > chance_B:
                self.knife = self.teamA.teamName
                return "a"
            else:
                self.knife = self.teamB.teamName
                return "b"




    def simulateall(self):

        start_ct = self.knifeRound()
        winner = "Temp"
        for map in self.maps:
            map.simulate(start_ct)
            if start_ct == "a":
                start_ct = "b"
            else:
                start_ct = "a"
            if winner == map.winner.teamName:
                break
            winner = map.winner.teamName









class Map:

    def __init__(self,name,team_a,team_b,full_rounds=False):
        self.name = name
        self.team_a = team_a
        self.team_b = team_b
        self.rounds = []
        self.team_a_score = 0
        self.team_b_score = 0
        self.winner = None
        self.full_rounds = full_rounds

    def getname(self):
        return self.name

    def getteam_a(self):
        return self.team_a.teamName

    def getteam_b(self):
        return self.team_b.teamName

    def playround(self,ct_side):
        if ct_side is "a":
            ct = self.team_a
            t = self.team_b
        elif ct_side is "b":
            ct = self.team_b
            t = self.team_a
        else:
            return
        new_round = Round(1,self,ct,t)
        new_round.simulate()
        self.rounds.append(new_round)

    def simulate(self,ct="a"):
        # Play first half
        for i in range(15):
            self.playround(ct)

        # Swap Teams
        if ct == "a":
            ct = "b"
        else:
            ct = "a"

        # Play second half
        for i in range(15):
            self.playround(ct)
            check = self.countscore()
            if check == "Done":
                break
        print("TEAM A (" + str(self.team_a.teamName) + "): " + str(self.team_a_score))
        print("TEAM B (" + str(self.team_b.teamName) + "): " + str(self.team_b_score))

    def countscore(self):
        count_a = 0
        count_b = 0
        for rnd in self.rounds:
            if rnd.winner is self.team_a:
                count_a += 1
            else:
                count_b += 1
        self.team_a_score = count_a
        self.team_b_score = count_b
        if count_a >= 16:
            self.winner = self.team_a
            return "Done"
        elif count_b >= 16:
            self.winner = self.team_b
            return "Done"
        else:
            # Change this when draws have been implemented
            self.winner = self.team_b









class Round:

    def __init__(self,rid,map,team_ct,team_t):
        self.rid = rid
        self.map = map
        self.team_ct = team_ct
        self.team_t = team_t
        self.winner = None


    def simulate(self):
        p_ct = (self.team_ct.teamRating / 2) * 60 * random.random()
        p_t = (self.team_t.teamRating / 2) * 40 * random.random()
        if p_ct >= p_t:
            self.winner = self.team_ct
        else:
            self.winner = self.team_t






#sum(c.A for c in c_list)
# Team Testing

p1 = Player('PlayerOne')
p2 = Player('PlayerTwo')
p3 = Player('PlayerThree')
p4 = Player('PlayerFour')
p5 = Player('PlayerFive')
p6 = Player('PlayerSix')
p7 = Player('PlayerSeven')
p8 = Player('PlayerEight')
p9 = Player('PlayerNine')
p10 = Player('PlayerTen')

t1 = Team('SuperTEAM')
t1.addPlayer(p1)
t1.addPlayer(p2)
t1.addPlayer(p3)
t1.addPlayer(p4)
t1.addPlayer(p5)
t1.calcRating()

t2 = Team('We Suck :<')
t2.addPlayer(p6)
t2.addPlayer(p7)
t2.addPlayer(p8)
t2.addPlayer(p9)
t2.addPlayer(p10)
t2.calcRating()



# Let's try a little battle, BO3





#test_map = Map("de_dust2",)
m1 = Match(1,t1,t2,3)

m1.addMap("de_dust2")
m1.addMap("de_nuke")
m1.addMap("de_inferno")

m1.simulateall()

tmp = m1.maps[0].winner.teamName
print(tmp)
tmp = m1.maps[1].winner.teamName
print(tmp)
if m1.maps[2].winner is not None:
    tmp = m1.maps[2].winner.teamName
    print(tmp)
#tmp = m1.maps[2].winner.teamName
#print(tmp)

print(t1.teamRating)
print(t2.teamRating)
