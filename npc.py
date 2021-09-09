from random import randint
from string import ascii_uppercase


class CreateNewNpc:
    def __init__(self, len_x, len_y, npc_view_range, npc_count, default_strength):
        self.len_x = len_x
        self.len_y = len_y
        self.npc_view_range = npc_view_range
        self.npc_count = npc_count
        self.default_strength = default_strength

    def create_new(self, npc_count: int):
        npc_name_index = 0
        npc_details = {}

        # Creates the designated amount of NPCs
        for i in range(npc_count):
            if self.default_strength < 2:
                exit('Default strength cannot be below two')

            npc_name = self.make_name(npc_name_index)
            npc_name_index += 1

            # Generates the coordinates of the NPC
            x_pos = randint(-self.len_x, self.len_x)
            y_pos = randint(-self.len_y, self.len_y)

            # Inputs all the details into one dictionary
            npc_details[f"NPC {npc_name}"] = (x_pos, y_pos, int(self.default_strength))

        return npc_details

    # Naming is A - Z, A2 - Z2, A3 - Z3 and so on

    @staticmethod
    def make_name(npc_name_index):
        try:
            npc_name = ascii_uppercase[npc_name_index]
        except IndexError:
            alphabet_iterations = npc_name_index // len(ascii_uppercase) + 1
            remainder = npc_name_index % len(ascii_uppercase)
            npc_name = ascii_uppercase[remainder] + str(alphabet_iterations)

        return npc_name


class Fight:
    def __init__(self, win_exponent, strength_gain_divisor):
        self.win_exponent = win_exponent
        self.strength_gain_divisor = strength_gain_divisor

    def fight(self, npc1, npc1stren, npc2, npc2stren, npc_details):

        npc1_attack, npc2_attack, attacks = self.get_attacks(npc1stren, npc2stren)

        if max(attacks) == npc2_attack:
            winner = npc2
            winner_stren = npc2stren

            loser_stren = npc1stren
            del npc_details[npc1]
        else:
            winner = npc1
            winner_stren = npc1stren

            loser_stren = npc2stren
            del npc_details[npc2]

        print(f'{winner} Won!')
        winner_stren += loser_stren / self.strength_gain_divisor

        return winner, int(winner_stren)

    # Chance to win grows exponentially the more strength the npc has.

    def get_attacks(self, npc1stren, npc2stren):
        chance_to_win_npc1 = int(npc1stren ** self.win_exponent)
        chance_to_win_npc2 = int(npc2stren ** self.win_exponent)

        npc1_attack = randint(0, chance_to_win_npc1)
        npc2_attack = randint(0, chance_to_win_npc2)
        attacks = [npc2_attack, npc1_attack]

        return npc1_attack, npc2_attack, attacks

