import websocket_manager
import trade_sizer as ts
import tkinter as tk
from tkinter import ttk
import trade_sizer as ts

tickers = ["DOGE-PERP","BTC-PERP","ETH-PERP","SXP-PERP","DEFI-PERP","XMR-PERP"]
bankroll = 25 #dollars

trade = ts.Trade()

def change_subscription(*args):
	print(tickers_var.get())
	target_var.set(0)
	exit_var.set(0)
	ws.change_sub(tickers_var.get())

def change_target(*args):
	print(f"target changed: {target_var.get()}")
	trade.update_target(target_var.get())

def change_exit(*args):
	print(f"exit changed: {exit_var.get()}")
	trade.update_exit(exit_var.get())

def change_risk(*args):
	print(f"risk% changed: {risk_percent_var.get()}")
	print(f"risk$ updated: {risk_percent_var.get()*bankroll}")
	trade.update_risk(risk_percent_var.get()*bankroll)

ws = websocket_manager.WebsocketManager(tickers[0])

window = tk.Tk()

#labels
price_p = tk.Label(text=str(0))
price_p.pack()
risk_p = tk.Label(text=str(0))
risk_p.pack()
reward_p = tk.Label(text=str(0))
reward_p.pack()
rr_p = tk.Label(text=str(0))
rr_p.pack()
position_p = tk.Label(text=str(0))
position_p.pack()
dir_p = tk.Label(text="")
dir_p.pack()

#target, exit, & risk vars & traces
target_var = tk.DoubleVar()
exit_var = tk.DoubleVar()
risk_percent_var = tk.DoubleVar()
target_var.trace("w",change_target)
exit_var.trace("w",change_exit)
risk_percent_var.trace("w",change_risk)

#tickers dropdown - create var, trace, default, and option menu
tickers_var = tk.StringVar()
tickers_var.trace("w",change_subscription)
tickers_var.set(tickers[0])
ticker_dropdown = tk.OptionMenu(window,tickers_var,*tickers)
ticker_dropdown.pack()

#target, exit, & risk fields + pack
target_price = ttk.Entry(window, width = 10, textvariable = target_var)
exit_price = ttk.Entry(window, width = 10, textvariable = exit_var)
risk_percent = ttk.Entry(window, width = 10, textvariable = risk_percent_var)
target_price.pack()
exit_price.pack()
risk_percent.pack()

def update():
	trade.update_entry(ws.msg)
	trade.set_dir()
	price_p.config(text="price: $" + str(ws.msg))
	risk_p.config(text="risk: $" + str(trade.exit_return()))
	reward_p.config(text="reward: $" + str(trade.target_return()))
	rr_p.config(text="R/R: " + str(trade.get_rr()))
	position_p.config(text="position size: " + str(trade.get_position_size()))
	dir_p.config(text="direction: " + str(trade.get_dir()))
	window.after(200,update)

def init():
	ws.connect()
	window.after(200, update)

init()
window.mainloop()

#here, we'll add all the elements to the window
#we'll update them all in the update() function
