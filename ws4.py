import websocket_manager
import tkinter as tk

ws = websocket_manager.WebsocketManager()
window = tk.Tk()
price_p = tk.Label(text=str(0))
price_p.pack()

def update():
	price_p.config(text=str(ws.msg))
	window.after(200,update)

def init():
	ws.connect()
	cnx_end = tk.Button(window, command = ws.close_connection, text = "close connection")
	cnx_end.pack()
	window.after(200, update)
#connect should actually activate on button press

init()
window.mainloop()

#here, we'll add all the elements to the window
#we'll update them all in the update() function
