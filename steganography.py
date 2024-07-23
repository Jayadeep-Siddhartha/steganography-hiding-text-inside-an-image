

# from tkinter import *
# from tkinter import filedialog
# import tkinter as tk
# from PIL import Image, ImageTk
# import os

# root = Tk()
# root.title("Steganography - Hiding a Text in an Image")
# root.geometry("700x500+150+100")
# root.resizable(False, False)
# root.configure(bg="#2f4155")

# def showImage():
#     global filename
#     filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("PNG File", "*.png"), ("JPG File", "*.jpg"), ("All File", "*.*")))
#     img = Image.open(filename)
#     img = ImageTk.PhotoImage(img)
#     lbl.configure(image=img, width=250, height=250)
#     lbl.image = img

# def hideData():
#     global secret
#     msg = text1.get(1.0, END)
#     secret = hide_message(filename, msg)

# def showData():
#     clear_msg = reveal_message(filename)
#     text1.delete(1.0, END)
#     text1.insert(END, clear_msg)

# def saveImage():
#     new_filename = os.path.join("hidden.png")
#     secret.save(new_filename)

# def hide_message(image_path, message):
#     img = Image.open(image_path)
#     binary_message = ''.join(format(ord(char), '08b') for char in message)
#     binary_message += '1111111111111110'  # End marker

#     data_index = 0
#     img_data = list(img.getdata())

#     for i in range(len(img_data)):
#         pixel = list(img_data[i])
#         for j in range(3):  # Iterate over RGB values
#             if data_index < len(binary_message):
#                 pixel[j] = pixel[j] & ~1 | int(binary_message[data_index])
#                 data_index += 1
#         img_data[i] = tuple(pixel)

#     img.putdata(img_data)
#     return img

# def reveal_message(image_path):
#     img = Image.open(image_path)
#     img_data = list(img.getdata())

#     binary_message = ""
#     for pixel in img_data:
#         for value in pixel[:3]:  # Only use RGB values
#             binary_message += str(value & 1)

#     binary_chunks = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
#     message = ""
#     for chunk in binary_chunks:
#         if chunk == '11111111':  # End marker
#             break
#         message += chr(int(chunk, 2))

#     return message

# # Icon
# image_path = r"C:\Users\jayad\OneDrive\Desktop\Files\Projects\Steganography\Image.jpg"
# image_icon = PhotoImage(file=image_path)
# root.iconphoto(False, image_icon)

# # Logo
# logo_path = r"C:\Users\jayad\OneDrive\Desktop\Files\Projects\Steganography\Image.jpg"
# logo = PhotoImage(file=logo_path)
# Label(root, text="Steganography", bg="#2f4155", fg="white", font="Arial 25 bold").place(x=225, y=20)

# # First Frame
# f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
# f.place(x=10, y=80)

# lbl = Label(f, bg="black")
# lbl.place(x=40, y=10)

# # Second Frame
# f2 = Frame(root, bd=3, width=340, height=280, bg="White", relief=GROOVE)
# f2.place(x=350, y=80)

# text1 = Text(f2, font="Roboto 20", bg="white", fg="black", relief=GROOVE)
# text1.place(x=0, y=0, width=320, height=295)

# scrollbar = Scrollbar(f2)
# scrollbar.place(x=320, y=0, height=300)
# scrollbar.configure(command=text1.yview)
# text1.configure(yscrollcommand=scrollbar.set)

# # Third Frame
# f3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
# f3.place(x=10, y=370)

# Button(f3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showImage).place(x=20, y=30)
# Button(f3, text="Save Image", width=10, height=2, font="arial 14 bold", command=saveImage).place(x=180, y=30)
# Label(f3, text="Picture,Image,Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

# # Fourth Frame
# f4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
# f4.place(x=360, y=370)

# Button(f4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=hideData).place(x=20, y=30)
# Button(f4, text="Show Data", width=10, height=2, font="arial 14 bold", command=showData).place(x=180, y=30)
# Label(f4, text="Picture,Image,Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

# root.mainloop()

from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os

root = Tk()
root.title("Steganography - Hiding a Text in an Image")
root.geometry("710x530+150+100")
root.resizable(False, False)
root.configure(bg="#2f4155")

def showImage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("PNG File", "*.png"), ("JPG File", "*.jpg"), ("All File", "*.*")))
    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img, width=250, height=250)
    lbl.image = img

def calculate_max_message_length(image_path):
    img = Image.open(image_path)
    width, height = img.size
    total_pixels = width * height
    max_message_length = (total_pixels * 3) // 8 - 2  # Subtract 2 bytes for the end marker
    return max_message_length

def hideData():
    global secret
    msg = text1.get(1.0, END).strip()
    password = password_entry.get().strip()
    max_message_length = calculate_max_message_length(filename)
    
    if len(msg) > max_message_length:
        info_label.config(text=f"Message is too long! Max length is {max_message_length} characters.")
        return
    
    secret = hide_message(filename, msg, password)
    if secret:
        info_label.config(text="Message hidden successfully!")

def showData():
    password = password_entry.get().strip()
    clear_msg = reveal_message(filename, password)
    text1.delete(1.0, END)
    text1.insert(END, clear_msg)

def saveImage():
    if secret:
        new_filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png"), ("All files", "*.*")])
        if new_filename:
            secret.save(new_filename)
            info_label.config(text="Image saved successfully!")

def xor_encrypt_decrypt(data, key):
    key = (key * ((len(data) // len(key)) + 1))[:len(data)]  # Ensure key is at least as long as data
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key))

def hide_message(image_path, message, password):
    img = Image.open(image_path)
    binary_message = ''.join(format(ord(char), '08b') for char in xor_encrypt_decrypt(message, password))
    binary_message += '1111111111111110'  # End marker

    data_index = 0
    img_data = list(img.getdata())

    for i in range(len(img_data)):
        pixel = list(img_data[i])
        for j in range(3):  # Iterate over RGB values
            if data_index < len(binary_message):
                pixel[j] = pixel[j] & ~1 | int(binary_message[data_index])
                data_index += 1
        img_data[i] = tuple(pixel)

    img.putdata(img_data)
    return img

def reveal_message(image_path, password):
    img = Image.open(image_path)
    img_data = list(img.getdata())

    binary_message = ""
    for pixel in img_data:
        for value in pixel[:3]:  # Only use RGB values
            binary_message += str(value & 1)

    binary_chunks = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ""
    for chunk in binary_chunks:
        if chunk == '11111111':  # End marker
            break
        message += chr(int(chunk, 2))

    return xor_encrypt_decrypt(message, password)

# Icon
image_path = r"C:\Users\jayad\OneDrive\Desktop\Files\Projects\Steganography\Image.jpg"
image_icon = PhotoImage(file=image_path)
root.iconphoto(False, image_icon)

# Logo
logo_path = r"C:\Users\jayad\OneDrive\Desktop\Files\Projects\Steganography\Image.jpg"
logo = PhotoImage(file=logo_path)
Label(root, text="Steganography", bg="#2f4155", fg="white", font="Arial 25 bold").place(x=225, y=20)

# First Frame
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second Frame
f2 = Frame(root, bd=3, width=340, height=280, bg="White", relief=GROOVE)
f2.place(x=350, y=80)

text1 = Text(f2, font="Roboto 20", bg="white", fg="black", relief=GROOVE)
text1.place(x=0, y=0, width=320, height=295)

scrollbar = Scrollbar(f2)
scrollbar.place(x=320, y=0, height=300)
scrollbar.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar.set)

# Password Frame
password_frame = Frame(root, bd=3, bg="#2f4155", width=330, height=50, relief=GROOVE)
password_frame.place(x=180, y=370)

Label(password_frame, text="Password:", bg="#2f4155", fg="yellow", font="Arial 14").place(x=10, y=10)
password_entry = Entry(password_frame, show="*", font="Arial 14")
password_entry.place(x=120, y=10)

# Third Frame
f3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
f3.place(x=15, y=420)

Button(f3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showImage).place(x=20, y=30)
Button(f3, text="Save Image", width=10, height=2, font="arial 14 bold", command=saveImage).place(x=180, y=30)
Label(f3, text="Picture,Image,Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Fourth Frame
f4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
f4.place(x=360, y=420)

Button(f4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=hideData).place(x=20, y=30)
Button(f4, text="Show Data", width=10, height=2, font="arial 14 bold", command=showData).place(x=180, y=30)
Label(f4, text="Picture,Image,Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Info Label
info_label = Label(root, text="", bg="#2f4155", fg="white", font="Arial 12")
info_label.place(x=10, y=480)

root.mainloop()