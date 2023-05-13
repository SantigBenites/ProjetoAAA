import gym
from Game.chess import Game
from ReiforcementLearning.RLplayer import RLPlayer
from StockFish.StockFishplayer import StockFishPlayer

learning_rate = 0.01
n_episodes = 100_000
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
final_epsilon = 0.1


env = gym.make('kungFuChess-v0')
player1 = RLPlayer()
for episode in range(n_episodes):
    obs, info = env.reset()
    done = False

    # play one episode
    while not done:
        action = agent.get_action(obs)
        next_obs, reward, terminated, truncated, info = env.step(action)

        # update the agent
        agent.update(obs, action, reward, terminated, next_obs)

        # update if the environment is done and the current obs
        done = terminated or truncated
        obs = next_obs

    agent.decay_epsilon()
