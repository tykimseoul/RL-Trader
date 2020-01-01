from keras.models import load_model
from datetime import date

from agent import Agent
from functions import *
import sys

if len(sys.argv) != 3:
	print("Usage: python evaluate.py [stock] [model]")
	exit()

stock_name, model_name = sys.argv[1], sys.argv[2]
model = load_model('model/'+model_name)
window_size = model.layers[0].input.shape.as_list()[1]

agent = Agent(window_size, True, model_name)
data = get_stock_data(stock_name, '2019/12/22', '2019/12/24')
validation_data_size = len(data) - 1
batch_size = 32

state = get_state(data, 0, window_size + 1)
total_profit = 0
agent.inventory = []

for t in range(validation_data_size):
	action = agent.act(state)

	# sit
	next_state = get_state(data, t + 1, window_size + 1)
	reward = 0

	# buy
	if action == 1:
		agent.inventory.append(data[t])
		print("Buy: " + format_price(data[t]))

	# sell
	elif action == 2 and len(agent.inventory) > 0:
		bought_price = agent.inventory.pop(0)
		reward = max(data[t] - bought_price, 0)
		total_profit += data[t] - bought_price
		print("Sell: " + format_price(data[t]) + " | Profit: " + format_price(data[t] - bought_price))

	done = True if t == validation_data_size - 1 else False
	agent.memory.append((state, action, reward, next_state, done))
	state = next_state

	if done:
		print("--------------------------------")
		print(stock_name + " Total Profit: " + format_price(total_profit))
		print("--------------------------------")
