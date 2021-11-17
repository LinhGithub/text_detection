import tkinter as tk
from tkinter.constants import NS, NSEW, NW
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter import messagebox
from PIL import ImageTk,Image

import glob, os

from numpy import maximum, record
import api
from tkinter.ttk import *
import time
from threading import *
import export_excel

PHOTOS = []
get_lst_image_all = []

def open_folder():
    folder_path = askdirectory()
    if not folder_path:
        return
    list_file_path = api.get_list_file_path_from_folder(folder_path)

    txt_edit.delete(1.0, tk.END)
    text = "\n".join(list_file_path)
    txt_edit.insert(tk.END, text)
    root.title(f"Bài tập ứng dụng phân tích khuôn mặt - {folder_path}")

    txt_edit.update_idletasks()
    frame_canvas1.config(width=380,
                height=380)

def clear_frame():
   for widgets in frame_images.winfo_children():
      widgets.destroy()

def recognize(PHOTOS):
    try:
        clear_frame()
        lst_image_all = []
        text = txt_edit.get(1.0, tk.END)
        list_file_path = text.split('\n')
        num_of_file_path = len(list_file_path) - 1
        if num_of_file_path > 0:
            for i in range(0, num_of_file_path):
                file_path = list_file_path[i]
                get_lst_image = api.crop_image(file_path)
                for item in get_lst_image:
                    lst_image_all.append(item)

                percentage = int((i+1)/num_of_file_path * 100)
                progress['value'] = percentage
                txt['text'] = str(progress['value']) + '%'
                root.update_idletasks()
            
            Ox = 1
            newPhoto_label = [tk.Label() for i in range(len(lst_image_all))]
            lstNote_text = [tk.Entry() for i in range(len(lst_image_all))]
            for file in lst_image_all:
                displayImg(file.get('file_path'), Ox, newPhoto_label, lstNote_text, file.get('note'), PHOTOS)
                Ox+=1
            get_lst_image_all.clear()
            for item in lst_image_all:
                get_lst_image_all.append(item)

            frame_images.update_idletasks()
            frame_canvas.config(width=380,
                        height=380)
            canvas.configure(scrollregion=canvas.bbox('all'), height=380)
        else:
            messagebox.showinfo('Thông báo!', 'Bạn chưa chọn thư mục ảnh nào!!!')
    except Exception as err:
        messagebox.showinfo('Thông báo!', 'Bạn chưa chọn thư mục ảnh nào!!!')

def displayImg(path,Ox,newPhoto_label,lstNote_text, note,photos):
    image = Image.open(path)
    photo = ImageTk.PhotoImage(image.resize((70,50)))
    photos.append(photo)#keep references!
    newPhoto_label[Ox-1] = tk.Label(frame_images,image=photo)
    newPhoto_label[Ox-1].grid(row=Ox, column=0, pady = 10, padx=(20,5),sticky='nw')
    entryText = tk.StringVar()
    lstNote_text[Ox-1] = tk.Entry( frame_images, textvariable=entryText, width=45 )
    # lstNote_text[Ox-1].bind("<Key>", lambda a: "break")
    lstNote_text[Ox-1].grid(row=Ox, column=1, padx=(0,10))
    entryText.set(note)

def export_excel_new():
    try:
        num_of_file_path = len(get_lst_image_all)
        if num_of_file_path == 0:
            messagebox.showinfo('Thông báo!', 'Không có dữ liệu để lưu!!!')
        else:
            new_lst = []
            list_img = []
            get_lst_image_all.pop()
            for item in get_lst_image_all:
                img = []
                img.append(item.get('file_path'))
                img.append(item.get('note'))
                list_img.append(img)
            header = ["Path file", 'Note']
            new_lst.append(header)
            new_lst.extend(list_img)
            if len(list_img) > 0:
                default_name = 'Thông tin phân tích chữ từ ảnh'
                export_excel.export_excel(default_name, new_lst)
                messagebox.showinfo('Thông báo!', 'Xuất file excel thành công.')
            else:
                messagebox.showinfo('Thông báo!', 'Bạn chưa chọn thư mục ảnh nào!!!')

    except Exception as err:
        messagebox.showinfo('Thông báo!', 'Bạn chưa chọn thư mục ảnh nào!!!')

def threading():
    t1 = Thread(target=recognize,args=(PHOTOS,))
    t1.start()

root = tk.Tk()
root.title("Bài tập ứng dụng phân tích khuôn mặt")
root.configure(background='#fcd703')
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(1, minsize=500, weight=1)

frame_main = tk.Frame(root, bg="#69cf9c")
frame_main.grid(sticky='news')
frame_main.grid(row=0, column=3, sticky="news")

frame_main1 = tk.Frame(root, bg="#69cf9c")
frame_main1.grid(sticky='news')
frame_main1.grid(row=0, column=1, sticky="news")

# Create a frame for the canvas with non-zero row&column weights
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
frame_canvas.grid(row=1, column=0, sticky="news", pady=(5, 0))

frame_canvas1 = tk.Frame(frame_main1)
frame_canvas1.grid_rowconfigure(0, weight=1)
frame_canvas1.grid_columnconfigure(0, weight=1)
frame_canvas1.grid(row=1, column=1, sticky="news")

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="white")
canvas.grid(row=0, column=0)

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient='vertical', command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain
frame_images = tk.Frame(canvas, bg="#82d7d9")
canvas.create_window((0, 0), window=frame_images, anchor='nw')

frame_images.update_idletasks()

frame_canvas.config(width=380,
                    height=380)


label1 = tk.Label(frame_main, text="Danh sách các chữ tích được", fg="blue")
label1.grid(row=0, column=0, pady=10, padx=10, sticky='news')

# -------------------------------------------------------

vsb1 = tk.Scrollbar(frame_canvas1, orient='vertical')
vsb1.grid(row=0, column=1, sticky='NSW')

txt_edit = tk.Text(frame_canvas1)
txt_edit.config(yscrollcommand= vsb1.set)
vsb1.configure(command= txt_edit.yview)

txt_edit.bind("<Key>", lambda a: "break")
  
fr_buttons = tk.Frame(root, relief=tk.RAISED)
fr_buttons1 = tk.Frame(root, relief=tk.RAISED)
fr_buttons2 = tk.Frame(root, relief=tk.RAISED)
fr_buttons.configure(background='#e0d8ca')
fr_buttons1.configure(background='#e0d8ca')
fr_buttons2.configure(background="#e07a72")

btn_open = tk.Button(fr_buttons, text="Chọn mục ảnh", command=open_folder,bg='#03cffc', fg="black")
btn_recognize = tk.Button(fr_buttons1, text="Phân tích ảnh", command=threading, bg='#03fc39', fg="black")
btn_excel = tk.Button(fr_buttons2, text="Xuất excel", command=export_excel_new,bg='#dea84b', fg="black")
label2 = tk.Label(frame_main1, text="Danh sách các đường dẫn file ảnh", fg="blue")
label2.grid(row=0, column=1, pady=10, padx=10, sticky='news')

btn_open.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
btn_recognize.grid(row=0, column=0, sticky="ew", padx=5,pady=5)
# btn_excel.grid(row=0, column=0, pady=5, sticky="news")
btn_excel.place(relx=0.5, rely=0.5, anchor='center')

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=0, sticky='W')
fr_buttons1.grid(row=0, column=2, sticky='ns')
fr_buttons2.grid(row=1, column=3, sticky="news")

txt = tk.Label(
    root,
    text='0%'
)

progress = Progressbar(root, orient=tk.HORIZONTAL,
                       length=100, mode='determinate')

progress.grid(row=1, column=1, sticky="nsew")
txt.grid(row=2, column=1, sticky="nsew")

# Set the canvas scrolling region
canvas.configure(scrollregion=canvas.bbox('all'), height=380)

root.attributes('-topmost', True)
root.mainloop()