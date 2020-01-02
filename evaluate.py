from keras.models import load_model
from datetime import date

from State import State
from agent import Agent
from functions import *
import sys

if len(sys.argv) != 3:
	print("Usage: python evaluate.py [stock] [model]")
	exit()

stock_name, model_name = sys.argv[1], sys.argv[2]
model = load_model('model/'+model_name)
state_size = model.layers[0].input.shape.as_list()[1]

stock_data, kospi_data = get_stock_data(stock_name, '2019/12/22', '2019/12/24')
validation_data_size = len(stock_data) - 1
batch_size = 32

state = State(0, stock_data, kospi_data, is_eval=True, target_size=state_size)
agent = Agent(state.size(), True, model_name)
state_instance = state.get_instance(0)
total_profit = 0
agent.inventory = []

for t in range(validation_data_size):
	action = agent.act(state_instance)

	# sit
	next_state = state.get_instance(t + 1)
	reward = 0

	# buy
	if action == 1:
		agent.inventory.append(stock_data[t])
		print("Buy: " + format_price(stock_data[t]))

	# sell
	elif action == 2 and len(agent.inventory) > 0:
		bought_price = agent.inventory.pop(0)
		reward = max(stock_data[t] - bought_price, 0)
		total_profit += stock_data[t] - bought_price
		print("Sell: " + format_price(stock_data[t]) + " | Profit: " + format_price(stock_data[t] - bought_price))

	done = t == validation_data_size - 1
	agent.memory.append((state_instance, action, reward, next_state, done))
	state_instance = next_state

	if done:
		print("--------------------------------")
		print(stock_name + " Total Profit: " + format_price(total_profit))
		print("--------------------------------")
