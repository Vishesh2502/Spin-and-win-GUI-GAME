import tkinter as tk
import random
import requests

# Define the colors used in the game
WHITE = "#ffffff"
BLACK = "#000000"
RED = "#ff0000"

# Define the font used for displaying messages on the screen
FONT = ("Sans-serif", 12, "bold")

# Define the segments of the wheel and their corresponding prizes
segments = ["INR 5 Coupon", "INR 10 Coupon", "INR 15 Coupon", "INR 70 Coupon", "INR 100 Coupon","INR 12 Coupon"]
positions = [[399, 90], [600, 234], [620, 460], [399, 549], [130, 460], [160, 234]]

# Define a function to generate a coupon code from the Fampay API
def generate_coupon(amount):
    coupon_code = ""
    response = requests.get(f"https://fampay.in/api/coupons/{amount}")
    if response.status_code == 200:
        coupon_code = response.json().get("coupon_code")
    return coupon_code

# Define a function to spin the wheel and update the display with the result
def spin_wheel():
    # Disable the spin button to prevent multiple spins
    spin_button.config(state=tk.DISABLED)
    spin_button.config(state=tk.NORMAL)
    
    # Rotate the wheel randomly
    angle = random.randint(0, 360)
    canvas.itemconfig(wheel, start=angle)
    canvas.update()
    
    # Determine which segment the wheel landed on and display the corresponding prize
    segment_index = int(angle / 60)
    prize_label.config(text=segments[segment_index])
    
    # Generate a coupon code for the prize and display it
    coupon_code = generate_coupon(segments[segment_index].split()[1])
    coupon_label.config(text=coupon_code)
    
    # Enable the spin button again
    spin_button.config(state=tk.NORMAL)

# Create the main window and canvas
window = tk.Tk()
window.title("Spin-to-Win")
canvas = tk.Canvas(window, width=800, height=600, bg="ORANGE")

# Draw the wheel on the canvas
wheel = canvas.create_arc(50, 50, 750, 750, start=0, extent=60, fill="WHITE")
for i in range(1, 6):
    canvas.create_arc(50, 50, 750, 750, start=i*60, extent=60, fill="GREEN")
for i in range(len(positions)):
    if i < len(segments):
        canvas.create_text(positions[i][0], positions[i][1], text=segments[i], font=FONT)
    else:
        print("Error: segment list index out of range")

# Create labels for the prize and coupon code
prize_label = tk.Label(window, text="", font=FONT, fg=RED)
coupon_label = tk.Label(window, text="", font=FONT, fg=BLACK)

# Create a button to spin the wheel
spin_button = tk.Button(window, text="Spin", font=FONT, command=spin_wheel)

# Pack the widgets onto the window
canvas.pack()
prize_label.pack()
coupon_label.pack()
spin_button.pack()

# Start the main event loop
window.mainloop()
