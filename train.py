from agent import Agent
from functions import *
import sys
import matplotlib.pyplot as plt
import time

if len(sys.argv) != 4:
    print("Usage: python train.py [stock] [window] [episodes]")
    exit()

stock_name, window_size, episode_count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

agent = Agent(window_size)
data = get_stock_data(stock_name, '2019/12/16', '2019/12/21')
train_data_size = len(data) - 1
batch_size = 64
profits = []

for e in range(episode_count + 1):
    print("Episode " + str(e) + "/" + str(episode_count))
    state = get_state(data, 0, window_size + 1)

    total_profit = 0
    agent.inventory = []
    start = time.time()

    for t in range(train_data_size):
        action = agent.act(state)

        # sit
        next_state = get_state(data, t + 1, window_size + 1)
        reward = 0
        # buy
        if action == 1:
            agent.inventory.append(data[t])
            print("Ep " + str(e) + "/" + str(episode_count) + ":" + str(t) + "\t" + "Buy: " + format_price(data[t]))
        # sell
        elif action == 2 and len(agent.inventory) > 0:
            bought_price = agent.inventory.pop(0)
            reward = max(data[t] - bought_price, 0)
            total_profit += data[t] - bought_price
            print("Ep " + str(e) + "/" + str(episode_count) + ":" + str(t) + "\t" + "Sell: " + format_price(data[t]) + " | Profit: " + format_price(data[t] - bought_price))

        done = t == train_data_size - 1
        agent.memory.append((state, action, reward, next_state, done))
        state = next_state

        if done:
            end = time.time()
            print("--------------------------------")
            print("Total Profit: " + format_price(total_profit))
            print("Time Elapsed: " + format_time(end - start))
            print("--------------------------------")
            profits.append(total_profit)

        if len(agent.memory) > batch_size:
            agent.replay_experience(batch_size)

    if e % 100 == 0:
        agent.model.save('model/model_ep' + str(e))

plt.plot(profits)
plt.show()
