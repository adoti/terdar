import websocket_manager
#import trade_sizer as ts
import tkinter as tk
from tkinter import ttk
import trade_sizer as ts

tickers = ["DOGE-PERP","BTC-PERP","ETH-PERP","SXP-PERP","DEFI-PERP","XMR-PERP"]

ws = websocket_manager.WebsocketManager(tickers[0])

def change_subscription(*args):
	print(tickers_var.get())
	ws.change_sub(tickers_var.get())

window = tk.Tk()

price_p = tk.Label(text=str(0))
price_p.pack()

target_var = tk.StringVar()
exit_var = tk.StringVar()

tickers_var = tk.StringVar()
tickers_var.trace("w",change_subscription)
tickers_var.set(tickers[0])

ticker_dropdown = tk.OptionMenu(window,tickers_var,*tickers)

target_price = ttk.Entry(window, width = 10, textvariable = target_var)
exit_price = ttk.Entry(window, width = 10, textvariable = exit_var)

ticker_dropdown.pack()
target_price.pack()
exit_price.pack()

def update():
	price_p.config(text=str(ws.msg))
	window.after(200,update)

def init():
	ws.connect()
	window.after(200, update)
#connect should actually activate on button press

init()
window.mainloop()

#here, we'll add all the elements to the window
#we'll update them all in the update() function
