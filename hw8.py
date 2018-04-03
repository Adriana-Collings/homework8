import numpy as np
import scr.FigureSupport as FigSupport
import scr.StatisticalClasses as Stat


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(self._id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:  # equivalent to cohort
    def __init__(self, id, prob_head, n_games):
        self._gameRewards = []  # create an empty list where rewards will be stored
        self._listofgames = []
        self._loss_probability = []
        self._nGame = n_games
        self._probHead = prob_head

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id * n_games + n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

    def simulate(self):
        return GameOutcomes(self)

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_game_rewards(self):
        return self._gameRewards

    def plot_reward(self):
        return self._gameRewards

    def money_lost(self):  # equivalent to get_reward
        return sum(i < 0 for i in self._gameRewards) / len (self._gameRewards)

    def get_loss_prob(self):  # equivalent to get ave reward
        return self._loss_probability # gameRewards and loss probability should be equivalent


class LossProbability:
    def __init__(self,id, prob_head, n_games):
        self._loss_probability = []

        for n in range (n_games):
            # create a new game
            game_set = SetOfGames(id * n_games + n, prob_head=prob_head,n_games=n_games)
            # store the loss prob
            self._loss_probability.append(game_set.money_lost())

    def simulate(self):
        return LossOutcomes(self)

    def get_loss_prob(self):
        return self._loss_probability

    def ave_loss_prob(self):
        return sum(self._loss_probability) / len(self._loss_probability)


class GameOutcomes:
    def __init__(self, simulated_game):
        self._simulatedGame = simulated_game
        self._sumStat_gameRewards = \
            Stat.SummaryStat('Game Rewards', self._simulatedGame.get_game_rewards())

    def get_ave_game_rewards(self):
        return self._sumStat_gameRewards.get_mean()

    def get_ci_game_rewards(self, alpha):
        return self._sumStat_gameRewards.get_t_CI(alpha)


class LossOutcomes:
    def __init__(self, simulated_game):
        self._simulatedGame = simulated_game
        self._sumStat_moneyLost =\
            Stat.SummaryStat('Money Lost', self._simulatedGame.get_loss_prob())

    def get_ave_money_lost(self):
        return self._sumStat_moneyLost.get_mean()

    def get_ci_money_lost(self, alpha):
        return self._sumStat_moneyLost.get_t_CI(alpha)


class MultiSetofGames:
    """simulates multiple sets of games"""

    def __init__(self, ids, n_games, prob_head):
        self._ids = ids
        self._nGame = n_games
        self._probHead = prob_head

        self._multiGameRewards = []  # two dimensional list of game rewards from each simulated set of games
        self._meanMultiGameRewards = []  # list of mean game rewards for each set of games
        self._sumStat_meanMultiGameRewards = None

        self._multiGameMoneyLost = []
        self._meanMultiGameMoneyLost = []
        self._sumStat_meanMultiMoneyLost = None

    def simulate(self):
        for i in range(len(self._ids)):
            # create a set of games
            setofgames = SetOfGames(self._ids[i], self._probHead[i], self._nGame[i])
            output = setofgames.simulate()
            self._multiGameRewards.append(setofgames.get_ave_reward())
            self._meanMultiGameRewards.append(output.get_ave_game_rewards())
        self._sumStat_meanMultiGameRewards = Stat.SummaryStat('Mean Game Rewards', self._meanMultiGameRewards)

        for j in range(len(self._ids)):
            lossprobability = LossProbability(self._ids[j], self._probHead[j], self._nGame[j])
            out = lossprobability.simulate()
            self._multiGameMoneyLost.append(lossprobability.ave_loss_prob())
            self._meanMultiGameMoneyLost.append(out.get_ave_money_lost())
        self._sumStat_meanMultiMoneyLost = Stat.SummaryStat('Mean Money Lost', self._meanMultiGameMoneyLost)

# Rewards
    def get_set_of_games_mean_reward(self, setofgames_index):
        return self._meanMultiGameRewards[setofgames_index]

    def get_set_of_games_ci_mean_rewards(self, setofgames_index, alpha):
        st = Stat.SummaryStat('', self._multiGameRewards[setofgames_index])
        return st.get_t_CI(alpha)

    def get_all_mean_reward(self):
        return self._meanMultiGameRewards

    def get_overall_mean_reward(self):
        return self._sumStat_meanMultiGameRewards.get_mean()


    def get_set_of_games_pi_rewards(self, setofgames_index, alpha):
        st = Stat.SummaryStat('', self._multiGameRewards[setofgames_index])
        return st.get_PI(alpha)

    def get_ci_mean_reward(self,alpha):
        return self._sumStat_meanMultiGameRewards.get_t_CI(alpha)

    def get_pi_mean_reward(self, alpha):
        return self._sumStat_meanMultiGameRewards.get_PI(alpha)

# Loss probability
    def get_set_of_games_mean_money_lost(self, setofgames_index):
        return self._meanMultiGameMoneyLost[setofgames_index]

    def get_set_of_games_ci_mean_money_lost(self, setofgames_index, alpha):
        st= Stat.SummaryStat('', self._multiGameMoneyLost[setofgames_index])
        return st.get_t_CI(alpha)

    def get_set_of_games_pi_money_lost (self, setofgames_index, alpha):
        st = Stat.SummaryStat ('', self._multiGameRewards[setofgames_index])
        return st.get_PI(alpha)

    def get_all_mean_money_lost(self):
        return self._meanMultiGameMoneyLost

    def get_overall_money_lost(self):
        return self._sumStat_meanMultiMoneyLost.get_mean()

    def get_ci_money_lost(self,alpha):
        return self._sumStat_meanMultiMoneyLost.get_t_CI(alpha)

    def get_pi_money_lost(self, alpha):
        return self._sumStat_meanMultiMoneyLost.get_PI(alpha)



# run trail of 1000 games to calculate expected reward
games = SetOfGames(id=1, prob_head=0.5, n_games=1000)
# print the average reward
# print('Expected reward when the probability of head is 0.5:', games.get_ave_reward())
# print('The minimum reward you can expect to see when playing this game is', np.amin(games.plot_reward()))
# print('The maximum reward you can expect to see when playing this game is', np.amax(games.plot_reward()))
# print('The probability that you lose money in this game is', games.money_lost())

#FigSupport.graph_histogram(
#    observations=games.plot_reward(),
#    title='Histogram of Average Rewards',
#    x_label='Reward Amount',
#    y_label='Instances of Reward Amount'
# )

NUM_SIM_GAMES = 10  # CHANGE THIS TO 1000
PROB_HEAD = 0.45
N_GAMES = 100
# problem 1: Confidence interval:
multiGame = MultiSetofGames(ids=range(NUM_SIM_GAMES),
                            n_games=[N_GAMES]*NUM_SIM_GAMES,
                            prob_head=[PROB_HEAD]*NUM_SIM_GAMES)
multiGame.simulate()




