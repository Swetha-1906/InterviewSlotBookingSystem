import tkinter as tk

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Smart Traffic Signal Control System")
root.geometry("1000x700")
root.configure(bg="gray20")

roads = ["North", "South", "East", "West"]
signals = {}
current = 0

# ---------------- TITLE ----------------
title = tk.Label(
    root,
    text="SMART TRAFFIC SIGNAL CONTROL SYSTEM",
    font=("Arial", 20, "bold"),
    bg="gray20",
    fg="white"
)
title.pack(pady=10)

status_label = tk.Label(
    root,
    text="Traffic Running...",
    font=("Arial", 14, "bold"),
    bg="gray20",
    fg="cyan"
)
status_label.pack()

# ---------------- CANVAS ----------------
canvas = tk.Canvas(root, width=950, height=580, bg="darkgreen", highlightthickness=0)
canvas.pack(pady=10)

# ---------------- DRAW ROADS ----------------
# Vertical Road
canvas.create_rectangle(390, 0, 560, 580, fill="gray25", outline="")
# Horizontal Road
canvas.create_rectangle(0, 205, 950, 375, fill="gray25", outline="")

# Lane markings
for i in range(0, 580, 40):
    canvas.create_line(475, i, 475, i+20, fill="white", width=3)
for i in range(0, 950, 40):
    canvas.create_line(i, 290, i+20, 290, fill="white", width=3)

# Junction center
canvas.create_rectangle(390, 205, 560, 375, fill="gray35", outline="")

# Zebra crossings
for i in range(390, 560, 20):
    canvas.create_rectangle(i, 180, i+10, 200, fill="white", outline="")
    canvas.create_rectangle(i, 380, i+10, 400, fill="white", outline="")
for i in range(205, 375, 20):
    canvas.create_rectangle(365, i, 385, i+10, fill="white", outline="")
    canvas.create_rectangle(565, i, 585, i+10, fill="white", outline="")

# ---------------- SIGNAL DRAW FUNCTION ----------------
def create_signal(x, y, road):
    # Pole
    canvas.create_rectangle(x+20, y+90, x+30, y+140, fill="black", outline="black")

    # Signal box
    canvas.create_rectangle(x, y, x+50, y+100, fill="black", outline="white", width=2)

    # Lights
    red = canvas.create_oval(x+10, y+10, x+40, y+35, fill="gray20", outline="white")
    amber = canvas.create_oval(x+10, y+38, x+40, y+63, fill="gray20", outline="white")
    green = canvas.create_oval(x+10, y+66, x+40, y+91, fill="gray20", outline="white")

    # Label
    canvas.create_text(x+25, y-10, text=road, fill="white", font=("Arial", 10, "bold"))

    signals[road] = {
        "red": red,
        "amber": amber,
        "green": green
    }

# ---------------- PLACE SIGNALS ----------------
create_signal(450, 40, "North")
create_signal(450, 430, "South")
create_signal(820, 245, "East")
create_signal(80, 245, "West")

# ---------------- UPDATE SIGNAL ----------------
def update_signal(active_road, active_color):
    for road in roads:
        canvas.itemconfig(signals[road]["red"], fill="gray20")
        canvas.itemconfig(signals[road]["amber"], fill="gray20")
        canvas.itemconfig(signals[road]["green"], fill="gray20")

        if road != active_road:
            canvas.itemconfig(signals[road]["red"], fill="red")

    if active_color == "red":
        canvas.itemconfig(signals[active_road]["red"], fill="red")
    elif active_color == "amber":
        canvas.itemconfig(signals[active_road]["amber"], fill="orange")
    elif active_color == "green":
        canvas.itemconfig(signals[active_road]["green"], fill="lime")

    status_label.config(text=f"{active_road} Road → {active_color.upper()}")

# ---------------- TRAFFIC CONTROL ----------------
def run_traffic():
    global current
    road = roads[current]
    update_signal(road, "green")
    root.after(3000, lambda: amber_phase(road))

def amber_phase(road):
    update_signal(road, "amber")
    root.after(1500, lambda: red_phase(road))

def red_phase(road):
    global current
    update_signal(road, "red")
    current = (current + 1) % len(roads)
    root.after(1000, run_traffic)

# ---------------- START ----------------
run_traffic()
root.mainloop()