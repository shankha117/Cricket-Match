from commons import KIRAT, NODHI, HENRA, RUMRAH
from score_generator import weighted_choice_binary_tree
from functools import wraps


class Match(object):

    def __init__(self):
        self.total_balls_left = 24
        self.curent_ball = 0
        self.target = 40
        self.winner = None
        self.score_board = {KIRAT.NAME: {"SCORE": 0, "PLAYING": True, "BALLS_PLAYED": 0},
                            NODHI.NAME: {"SCORE": 0, "PLAYING": True, "BALLS_PLAYED": 0},
                            HENRA.NAME: {"SCORE": 0, "PLAYING": False, "BALLS_PLAYED": 0},
                            RUMRAH.NAME: {"SCORE": 0, "PLAYING": False, "BALLS_PLAYED": 0}}
        self.wickets = 3
        self.remaining_batsman = [KIRAT, NODHI, HENRA, RUMRAH]
        self.scores = ['Dot', '1', '2', '3', '4', '5', '6', 'Out']
        self.striker = KIRAT
        self.non_striker = NODHI

    def start(self):
        cur_score = 0

        while self.curent_ball < self.total_balls_left:
            cur_score = weighted_choice_binary_tree(self.striker.SCORE_PROBABILITY)
            self.commentry(self.striker, self.non_striker, cur_score, self.curent_ball)

            # print('current_ball -- {0} target --- {1} wickets---- {2}'.format(self.curent_ball, self.target,
            #                                                                   self.wickets))

            self.curent_ball += 1

            if self.match_ended():
                self.results()
                break

            import time
            time.sleep(.5)

    def match_ended(self):

        """
        CONDITIONS to check is match is running or not
        """
        #######
        # bangalore wins
        #######
        # chased the target

        if self.target < 0 and self.curent_ball < self.total_balls_left:
            self.winner = "BANGALORE"
            return True

        #######
        # chennai wins
        #######

        if self.wickets <= 0 and self.target > 1:
            self.winner = "CHENNAI"
            return True

        if self.target > 0 and self.curent_ball >= self.total_balls_left:
            self.winner = "CHENNAI"
            return True

        #######
        # MATCH DRAW
        #######

        if self.target == 0 and self.curent_ball == self.total_balls_left:
            self.winner = "DRAW"
            return True

        return False

    # this method swaps the strikers
    def swap_strikers(self, striker, non_striker):
        self.striker = non_striker
        self.non_striker = striker

    def find_next_batsman(self, batsman_out, non_striker):

        # decrease the remaining wicket count by 1
        self.wickets -= 1

        self.score_board[batsman_out.NAME]["PLAYING"] = False
        if self.wickets > 0:
            next_batsman = next(
                (elem for elem in self.remaining_batsman if elem not in [batsman_out, non_striker]),
                None)

            # remove the batsman from remaining_batsman list
            self.remaining_batsman.remove(batsman_out)

            # update the score board for batsman playing
            self.score_board[next_batsman.NAME]["PLAYING"] = True

            return next_batsman

        else:
            return None

    def _update_striker(f):
        # wrap the function
        @wraps(f)
        def decoretor(inst, striker, non_striker, cur_score, cur_ball):
            f(inst, striker, non_striker, cur_score, cur_ball)

            """
            CONDITIONS to update the striker and non-striker
            """
            # condition 1:

            # if batsman is out at the last end of the over
            # then new batsman will be non_striker and non_striker will be striker
            if cur_score == 7 and (cur_ball + 1) % 6 == 0:
                os.system('figlet "OUT" -f bubble | lolcat')
                next_striker = inst.find_next_batsman(striker, non_striker)
                inst.swap_strikers(next_striker, non_striker)  # swap
                return

            # condition 2:

            # if the batsman is out in the middle of the over
            # the new batsman will be on strike
            if cur_score == 7:
                os.system('figlet "OUT" -f bubble | lolcat')
                next_striker = inst.find_next_batsman(striker, non_striker)
                inst.swap_strikers(non_striker, next_striker)  # swap
                return

            # condition 3:

            # if the batsman scores a [DOT,2,4,6] in the end of the over
            # then striker will be non_striker and non_striker will be striker
            if (cur_score % 2) == 0 and (cur_ball + 1) % 6 == 0:
                inst.swap_strikers(striker, non_striker)  # swap
                return

            # condition 4:

            # if the batsman scores [1,3,5] in the in the end of the over
            # then maintain the same order
            if (cur_score % 2) != 0 and (cur_ball + 1) % 6 == 0:
                return  # DO NOT swap

            # condition 5:

            # if the batsman scores [1,3,5] in the in the end of the over
            # then striker will be non_striker and non_striker will be striker
            if (cur_score % 2) != 0:
                inst.swap_strikers(striker, non_striker)  # swap
                return

            # condition 6:

            # if the batsman scores a [DOT,2,4,6] in the middle of the over
            # then maintain the same order
            return  # DO NOT swap

        return decoretor

    def results(self):

        # print(self.score_board)

        print("\n\n")
        # os.system('figlet "OUT" -f bubble | lolcat')
        if not self.winner == "DRAW":
            print('{0} wins by {1} wicket and {2} balls remaining'.format(self.winner, self.wickets,
                                                                          self.total_balls_left - self.curent_ball))

        else:
            print("------------ MATCH DRAW ---------")
            print('total balls played - {0} and total runs to chase ---- {1}'.format(self.curent_ball, self.target))

        print("\n\nFINAL RESULT--------")
        print("------------------------")

        for i in self.score_board:
            if self.score_board[i]['PLAYING']:
                print('{0} - {1}* ({2} balls)'.format(i, self.score_board[i]['SCORE'],
                                                      self.score_board[i]['BALLS_PLAYED']))
            else:
                print('{0} - {1} ({2} balls)'.format(i, self.score_board[i]['SCORE'],
                                                     self.score_board[i]['BALLS_PLAYED']))

    @_update_striker
    def commentry(self, striker, non_striker, cur_score, cur_ball):

        if cur_score == 7:
            print('{0} {1} is OUT'.format(str(int(cur_ball / 6)) + "." + str((cur_ball % 6 + 1)), striker.NAME))
        else:
            print('{0} {1} scores {2} run'.format(str(int(cur_ball / 6)) + "." + str((cur_ball % 6 + 1)), striker.NAME,
                                                  self.scores[cur_score]))

        self.score_board[striker.NAME]["BALLS_PLAYED"] += 1
        # update the score for each batsman and also the target
        if cur_score not in [0, 7]:
            # update the score board for batsman
            self.score_board[striker.NAME]["SCORE"] += cur_score

            # update the target
            self.target -= cur_score


if __name__ == "__main__":
    import os

    os.system('toilet -f small " MATCH  STARTED " | boxes -d scroll | lolcat')

    # print("MATCH STARTED------- \n\n")

    Match().start()
