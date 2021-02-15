import websocket_manager
#import trade_sizer as ts
import tkinter as tk
from tkinter import ttk
import trade_sizer as ts

ws = websocket_manager.WebsocketManager()

window = tk.Tk()

price_p = tk.Label(text=str(0))
price_p.pack()

target_var = tk.StringVar()
exit_var = tk.StringVar()

target_price = ttk.Entry(window, width = 10, textvariable = target_var)
exit_price = ttk.Entry(window, width = 10, textvariable = exit_var)

target_price.pack()
exit_price.pack()

def update():
	price_p.config(text=str(ws.msg))
	window.after(200,update)

def init():
	ws.connect()
	b_close_connection = tk.Button(window, command = ws.close_connection, text = "close connection")
	b_close_connection.pack()
	window.after(200, update)
#connect should actually activate on button press

init()
window.mainloop()

#here, we'll add all the elements to the window
#we'll update them all in the update() function
