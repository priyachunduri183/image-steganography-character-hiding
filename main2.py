import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
import pyttsx3

engine = pyttsx3.init()

img_path = None
stego_image_path = "stego_image.png"   # ✅ CHANGED TO PNG

# ---------------- TEXT TO SPEECH ----------------
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------- SELECT IMAGE ----------------
def select_image():
    global img_path
    img_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if img_path:
        messagebox.showinfo("Image Selected", "Image selected successfully")

# ---------------- HIDE CHARACTER ----------------
def hide_character():
    if not img_path:
        messagebox.showerror("Error", "Please select an image")
        return

    char = char_entry.get()
    if len(char) != 1:
        messagebox.showerror("Error", "Enter exactly ONE character")
        return

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (256, 256))

    ascii_val = ord(char)
    binary = format(ascii_val, '08b')

    flat_img = img.flatten()

    for i in range(8):
        flat_img[i] = (flat_img[i] & 0b11111110) | int(binary[i])

    stego_img = flat_img.reshape((256, 256))
    cv2.imwrite(stego_image_path, stego_img)   # ✅ SAVED AS PNG

    messagebox.showinfo("Success", "Character hidden successfully in stego_image.png")

# ---------------- EXTRACT CHARACTER ----------------
def extract_character():
    img = cv2.imread(stego_image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        messagebox.showerror("Error", "Stego image not found")
        return

    flat_img = img.flatten()

    binary = ""
    for i in range(8):
        binary += str(flat_img[i] & 1)

    char = chr(int(binary, 2))
    result_label.config(text=f"Hidden Character: {char}")
    speak(char)

# ---------------- UI ----------------
root = Tk()
root.title("Image Steganography with Speech")
root.geometry("450x350")

Label(root, text="Character Steganography", font=("Arial", 16)).pack(pady=10)

Button(root, text="Select Image", command=select_image, width=20).pack(pady=5)

Label(root, text="Enter Character to Hide:").pack()
char_entry = Entry(root, width=10, font=("Arial", 14))
char_entry.pack(pady=5)

Button(root, text="Hide Character", command=hide_character, width=20).pack(pady=10)
Button(root, text="Extract Character", command=extract_character, width=20).pack(pady=10)

result_label = Label(root, text="", font=("Arial", 14), fg="green")
result_label.pack(pady=10)

root.mainloop()
