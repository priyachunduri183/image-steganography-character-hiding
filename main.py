import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3

# Global variables
image = None
stego_image = None
hidden_char = ""

# Select image
def select_image():
    global image
    path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")])
    if path:
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(gray, (128, 128))
        messagebox.showinfo("Success", "Image loaded and converted to grayscale")

# Hide character using LSB
def hide_character():
    global stego_image, hidden_char
    if image is None:
        messagebox.showerror("Error", "Select an image first")
        return

    char = char_entry.get()
    if len(char) != 1:
        messagebox.showerror("Error", "Enter only ONE character")
        return

    hidden_char = char
    stego_image = image.copy()
    binary = format(ord(char), '08b')

    for i in range(8):
        stego_image[0][i] = (stego_image[0][i] & 254) | int(binary[i])

    messagebox.showinfo("Success", "Character hidden successfully")

# Retrieve character
def retrieve_character():
    if stego_image is None:
        messagebox.showerror("Error", "No hidden data found")
        return

    bits = ""
    for i in range(8):
        bits += str(stego_image[0][i] & 1)

    char = chr(int(bits, 2))
    result_label.config(text=f"Hidden Character: {char}")
    speak(char)

# Convert text to speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# GUI setup
root = tk.Tk()
root.title("Image Steganography with Speech")
root.geometry("400x300")

tk.Button(root, text="Select Image", command=select_image, width=25).pack(pady=10)

tk.Label(root, text="Enter character to hide:").pack()
char_entry = tk.Entry(root, width=10)
char_entry.pack(pady=5)

tk.Button(root, text="Hide Character", command=hide_character, width=25).pack(pady=10)
tk.Button(root, text="Retrieve Character", command=retrieve_character, width=25).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
