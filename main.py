import websocket_manager
import trade_sizer as ts
import tkinter as tk
from tkinter import ttk
import trade_sizer as ts
import keys
import rest_client as rc

tickers = ["DOGE-PERP",
	"BTC-PERP",
	"ETH-PERP",
	"SXP-PERP",
	"DEFI-PERP",
	"XMR-PERP",
	"DOT-PERP",
	"LTC-PERP",
	"LINK-PERP",
	"GRT-PERP",
	"AAVE-PERP",
	"SOL-PERP",
	"SRM-PERP"]
ftx = rc.FtxClient(keys.API_KEY, keys.API_SECRET)
bankroll = ftx.get_usd_value()

trade = ts.Trade()

def change_subscription(*args):
	print(tickers_var.get())
	target_var.set(0)
	exit_var.set(0)
	trade = ts.Trade()
	ws.change_sub(tickers_var.get())

def change_target(*args):
	print(f"target changed: {target_var.get()}")
	trade.update_target(target_var.get())

def change_exit(*args):
	print(f"exit changed: {exit_var.get()}")
	trade.update_exit(exit_var.get())

def change_risk(*args):
	print(f"risk% changed: {risk_percent_var.get()}%")
	print(f"risk$ updated: {risk_percent_var.get()*bankroll/100}")
	trade.update_risk(risk_percent_var.get()*bankroll/100)

ws = websocket_manager.WebsocketManager(tickers[0])

window = tk.Tk()

#live price
price_label = tk.Label(text="Price:")
price_label.grid(row=0,column=0,sticky="E")
price_p = tk.Label(text=str(0))
price_p.grid(row=0,column=1,sticky="W")

#target
target_label = tk.Label(text="Target:")
target_label.grid(row=1,column=0,sticky="E")
target_var = tk.DoubleVar()
target_var.trace("w",change_target)
target_price = ttk.Entry(window, width = 10, textvariable = target_var)
target_price.grid(row=1,column=1)

#stoploss price
exit_label = tk.Label(text="Stop Loss:")
exit_label.grid(row=2,column=0,sticky="E")
exit_var = tk.DoubleVar()
exit_var.trace("w",change_exit)
exit_price = ttk.Entry(window, width = 10, textvariable = exit_var)
exit_price.grid(row=2,column=1)
dir_p = tk.Label(text="")
dir_p.grid(row=2,column=2)


#live R
rr_label = tk.Label(text="R/R:")
rr_label.grid(row=3,column=0,sticky="E")
rr_p = tk.Label(text=str(0))
rr_p.grid(row=3,column = 1,sticky="W")

#Bankroll
br_label = tk.Label(text="Bankroll:")
br_label.grid(row=4,column=0,sticky="E")
br_p = tk.Label(text="$"+str(ts.round_d(bankroll,2)))
br_p.grid(row=4,column=1,sticky="W")

#risk%
risk_label = tk.Label(text="Risk %")
risk_label.grid(row=5,column=0,sticky="E")
risk_percent_var = tk.DoubleVar()
risk_percent_var.trace("w",change_risk)
risk_percent = ttk.Entry(window, width = 10, textvariable = risk_percent_var)
risk_percent.grid(row=5,column=1)

#risk usd
risku_label = tk.Label(text="Risk $/Reward $")
risku_label.grid(row=6,column=0,sticky="E")
risk_p = tk.Label(text=str(0))
risk_p.grid(row=6,column=1,sticky="W")
reward_p = tk.Label(text=str(0))
reward_p.grid(row=6,column=2,sticky="W")

#position size
position_label = tk.Label(text="Position Size:")
position_label.grid(row=7,column=0,sticky="E")
position_p = tk.Label(text=str(0))
position_p.grid(row=7,column=1,sticky="W")

#tickers dropdown - create var, trace, default, and option menu
tickers_var = tk.StringVar()
tickers_var.trace("w",change_subscription)
tickers_var.set(tickers[0])
ticker_dropdown = tk.OptionMenu(window,tickers_var,*tickers)
ticker_dropdown.grid(row=0, column=2)


def update():
	bankroll = ftx.get_usd_value()
	trade.update_entry(ws.msg)
	trade.set_dir()
	price_p.config(text=str(ws.msg))
	risk_p.config(text="$"+str(trade.exit_return()))
	reward_p.config(text="$"+str(trade.target_return()))
	rr_p.config(text=str(trade.get_rr()))
	position_p.config(text=str(trade.get_position_size()))
	dir_p.config(text=str(trade.get_dir()))
	window.after(200,update)

def init():
	ws.connect()
	window.after(200, update)

init()
window.mainloop()

#here, we'll add all the elements to the window
#we'll update them all in the update() function
