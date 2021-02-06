import websocket_manager
import tkinter as tk

ws = websocket_manager.WebsocketManager()

def update():
	price_p.config(text=str(ws.msg))
	window.after(200,update)

#connect should actually activate on button press
ws.connect()

window = tk.Tk()
price_p = tk.Label(text=str(0))
price_p.pack()
cnx_end = tk.Button(window, command = ws.close_connection, text = "close connection")
cnx_end.pack()
#here, we'll add all the elements to the window
#we'll update them all in the update() function
window.after(200,update)
window.mainloop()