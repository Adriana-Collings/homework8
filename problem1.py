import hw8 as hw8
#import scr.Figuresupport as Fig
#import scr.SamplePathClasses as SamplePathSupport

print("Problem 1: Comparing outcomes in a steady-state scenario (Weight 1): Present to the casino’s owner\n"
      "the change in their reward if they use an unfair coin for which the probability of head is 45%.")

NUM_SIM_GAMES = 10 
PROB_HEAD = 0.5
N_GAMES = 1000

value1 = hw8.MultiSetofGames(ids=range(NUM_SIM_GAMES),
                            n_games=[N_GAMES]*NUM_SIM_GAMES,
                            prob_head=[PROB_HEAD]*NUM_SIM_GAMES)
value1.simulate()

PROB_HEAD2 = 0.45

value2 = hw8.MultiSetofGames(ids=range(NUM_SIM_GAMES),
                             n_games=[N_GAMES]*NUM_SIM_GAMES,
                             prob_head=[PROB_HEAD2]*NUM_SIM_GAMES)
value2.simulate()

change = (value1.get_overall_mean_reward() * -1) - (value2.get_overall_mean_reward() * -1)


print(value1.get_overall_mean_reward())
print(value2.get_overall_mean_reward())

print("The change in reward for the casino owner is:", change, "changing from", value1.get_overall_mean_reward() * -1,
      "with a fair coin to", value2.get_overall_mean_reward() * -1, "with an unfair coin.")


