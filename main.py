from warnings import filterwarnings
from npc import Fight, CreateNewNpc
from random import randint, sample
from time import sleep
from logger import logger
filterwarnings('ignore')

# You can change these six constants to whatever you want,
# Although it might take a while for the program to finish if the settings are too high/low.

WAIT_TIME = 0  # time between npc fights
LEN_X = 50  # length of the x coordinate of the map
LEN_Y = 50  # length of the y coordinate of the map
NPC_VIEW_RANGE = 15  # how far an npc has to be to another npc for a fight to begin
NPC_COUNT = 3  # the amount of npcs
DEFAULT_STRENGTH = 5  # the starting strength of every npc
MAX_MOVEMENT_RADIUS = 5  # the highest amount of squares an npc can move
WIN_EXPONENT = 1.3  # how high of a chance an npc has of winning depending on strength (strength^win_exponent)
STRENGTH_GAIN_DIVISOR = 1.3  # the divisor of how much strength the winning npc will gain from the loser npc
OVERIDE_NPC_NAMES = True  # True for player selected names, and false for automated names like npc A and npc U3


def log_prompt():
    while True:
        logbool = input("Log details? (y for yes, n for no) ").lower()
        if logbool == 'y':
            logger(permanent_details, winner)
            print('Details logged')
            break
        elif logbool == 'n':
            print('Details not logged')
            break


def npc_player_name_choice():
    denominator = ','

    while True:
        npc_names = input(f'Give {NPC_COUNT} names for npcs seperated by {denominator} \n> ')
        npc_names_list = npc_names.split(denominator)

        if len(npc_names_list) == NPC_COUNT:
            break
        else:
            print(f"\nThat's not {NPC_COUNT} names!")

    return npc_names_list


if OVERIDE_NPC_NAMES:
    NPC_NAMES_LIST = npc_player_name_choice()
else:
    NPC_NAMES_LIST = False

npc = CreateNewNpc(
    len_x=LEN_X,
    len_y=LEN_Y,
    npc_view_range=NPC_VIEW_RANGE,
    npc_count=NPC_COUNT,
    default_strength=DEFAULT_STRENGTH,
    npc_names_list=NPC_NAMES_LIST


)
fight = Fight(
    win_exponent=WIN_EXPONENT,
    strength_gain_divisor=STRENGTH_GAIN_DIVISOR
)

npc_details = npc.create_new(npc_count=NPC_COUNT)

permanent_details = npc_details.copy()
npcs_alive = len(npc_details)
print_search = True

# This finds all NPCs within distance of variable npc view range
while npcs_alive != 1:

    # Chooses a random npc
    for key, details in sample(npc_details.items(), npcs_alive):

        coordX, coordY, stren = details

        # Chooses another random npc

        for key_, details_ in sample(npc_details.items(), npcs_alive):

            coord_X, coord_Y, stren_ = details_

            # Compares both of them

            if key != key_ and abs(coord_X - coordX) <= NPC_VIEW_RANGE and abs(coord_Y - coordY) <= NPC_VIEW_RANGE and\
                    key in npc_details and key_ in npc_details:

                # if both NPCs are suitable then they fight each other
                print(f"""
    {key}: X=({coordX}), Y=({coordY})   Strength: {stren}
    {key_}: X=({coord_X}), Y=({coord_Y})   Strength: {stren_}
                    """)

                npc_fight_details = fight.fight(
                    npc1=key,
                    npc2=key_,
                    npc1stren=stren,
                    npc2stren=stren_,
                    npc_details=npc_details
                )
                winner, winner_stren = npc_fight_details
                if winner == key:
                    stren = winner_stren
                if winner == key_:
                    stren_ = winner_stren
                winner_update_details = {winner: (coord_X, coord_Y, winner_stren)}

                permanent_details.update(winner_update_details)
                npc_details.update(winner_update_details)
                npcs_alive = len(npc_details)
                sleep(WAIT_TIME)

                print(f"There are {npcs_alive} NPCs left alive")
            break

    # Once all of the in range NPCs have fought each other
    # they will now start moving randomly in hopes of looking for a fight.
    walk_range = 0
    loopvar = 0
    for name, details in npc_details.items():

        dir_x, dir_y, stren = details

        while True:
            x_move = randint(-MAX_MOVEMENT_RADIUS, MAX_MOVEMENT_RADIUS)
            y_move = randint(-MAX_MOVEMENT_RADIUS, MAX_MOVEMENT_RADIUS)
            dir_x += x_move
            dir_y += y_move
            if any([dir_y > LEN_Y, dir_y < -LEN_Y, dir_x > LEN_X, dir_x < -LEN_X]):
                dir_x -= x_move
                dir_y -= y_move
            else:
                break

        npc_details.update({name: (dir_x, dir_y, stren)})
        npc_details.update({name: (dir_x, dir_y, stren)})

try:
    print(f"""{winner} Is victorious, and has {npc_details[winner][2]} strength!""")
except:
    exit("There can't be just 1 npc!")

log_prompt()

