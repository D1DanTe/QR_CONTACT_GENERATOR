import tkinter as tk

root = tk.Tk()
root.title("Проверка Tkinter")
root.geometry("400x200")

label = tk.Label(root, text="Tkinter работает!")
label.pack(pady=50)

root.mainloop()