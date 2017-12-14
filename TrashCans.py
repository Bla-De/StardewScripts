import sys

from ObjectInfo import ObjectInfo
from CSRandom import CSRandom
from Utility import dayToYSD

GarbageLocations = {
    0: [[13, 86], 'Jodi'],  # Jodi
    1: [[19, 89], 'Emily'],  # Emily
    2: [[56, 85], 'Lewis'],  # Lewis
    3: [[108, 91], 'Museum'],  # Museum
    4: [[97, 80], 'Clint'],  # Clint
    5: [[47, 70], 'Gus'],  # Gus
    6: [[52, 63], 'George']  # George
}
seasonDict = {0: 'Spring', 1: 'Summer', 2: 'Fall', 3: 'Winter'}


def random_item_from_season(gameID, day, seedAdd, furnace=False):
    season = (day-1) // 28 % 4
    rand = CSRandom(gameID + day + seedAdd)
    source = [68, 66, 78, 80, 86, 152, 167, 153, 420]

    source.extend({
                      0: [16, 18, 20, 22, 129, 131, 132, 136, 137, 142, 143, 145, 147, 148, 152, 167],
                      1: [128, 130, 131, 132, 136, 138, 142, 144, 145, 146, 149, 150, 155, 396, 398, 400, 402],
                      2: [404, 406, 408, 410, 129, 131, 132, 136, 137, 139, 140, 142, 143, 148, 150, 154, 155],
                      3: [412, 414, 416, 418, 130, 131, 132, 136, 140, 141, 143, 144, 146, 147, 150, 151, 154]
                  }[season])
    if furnace:
        source.extend([334, 335, 336, 338])
    r = rand.next(len(source))
    return source[r]


def check_trash(gameID, day, index, x, y, furnace=False):
    rand = CSRandom(gameID//2 + day + 777 + index)
    min_luck = 0.2
    if rand.sample() < min_luck:
        r = rand.next(10)
        if r == 6:
            ps = random_item_from_season(gameID, day, x*653+y*777, furnace)
        elif r == 8:
            ps = 309 + rand.next(3)
        else:
            ps = {0: 168,
                  1: 167,
                  2: 170,
                  3: 171,
                  4: 172,
                  5: 216,
                  7: 403,
                  9: 153}[r]
        if index == 3 and rand.sample() < min_luck:
            ps = 535
            if rand.sample() < 0.05:
                ps = 749
        if index == 4 and rand.sample() < min_luck:
            ps = 378 + rand.next(3)*2
        if index == 5 and rand.sample() < min_luck:
            return 'DishOfTheDay'
        if index == 6 and rand.sample() < min_luck:
            ps = 223
        return ObjectInfo[ps].split('/')[0]
    return None

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        gameID = int(sys.argv[1])
    else:
        gameID = 143594438
    for day in range(1, 112+1):
        flag = False
        Cans = dayToYSD(day) + "\n"
        for i in range(7):
            can = GarbageLocations[i]
            item = check_trash(gameID,day,i,can[0][0],can[0][1],day > 5)
            if item is not None:
                flag = True
                Cans = Cans + ("\t %s : %s\n" % (can[1],item))
        if flag:
            print(Cans)
