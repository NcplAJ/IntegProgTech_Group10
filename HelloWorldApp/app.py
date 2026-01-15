import tkinter as tk

app = tk.Tk()
app.title("Hello World APp")
app.geometry("300x200")

label = tk.Label(app, text = "Hello, World!", font=("Arial", 16))
label.pack(pady = 20)

def on_button_click():
    label.config(text="You clicked the button!")

button = tk.Button(app, text="Click Me!", command = on_button_click)
button.pack(pady=10)

app.mainloop()