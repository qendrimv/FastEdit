import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from os import listdir
import re

root = tk.Tk()
root.title('FastEdit')
w = 900
h = 400

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = (ws/2) - (w/2)
y = (hs/2) - (h/2) 

root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.configure(background='black')
root.minsize(900, 400)

canvas1 = tk.Canvas(root, width=300, bg="grey")
canvas1.pack(fill=tk.BOTH, side=LEFT, expand=True)

canvas2 = tk.Canvas(root, width=600, bg="black")
canvas2.pack(fill=tk.BOTH, side=LEFT, expand=True)


def popup(message, lst):
    window = tk.Toplevel()
    window.geometry('500x300+480+300')
    window.configure(background='#696969')
    label = tk.Label(window, text=message, fg='white', bg='#696969', wraplength=250)
    # label = tk.Label(window, text="Test")
    label.pack(padx=100, pady=100)

    tk.Button(window, text="Cancel", fg='white', bg='#696969', command=window.destroy).place(relx=0.2, rely=0.9, anchor=CENTER)
    tk.Button(window, text="Save", fg='white', bg='#696969', command=lambda:save_file(lst, window)).place(relx=0.8, rely=0.9, anchor=CENTER)


def error_message(title="File not found", message="File not loaded or not found"):
    messagebox.showerror(title, message)

def infoPopup(message):
    window = tk.Toplevel()
    window.geometry('500x300+480+300')
    window.configure(background='#696969')
    tk.Label(window, text=message, fg='white', bg='#696969', wraplength=250).pack(padx=100, pady=100)

    tk.Button(window, text="OK", fg='white', bg='#696969', command=window.destroy).place(relx=0.8, rely=0.9, anchor=CENTER)


def duplicate(name):

    try:
        fopen = open(name, 'r', errors='ignore')
        f = fopen.readlines()
        fopen.close()
        newf = list(set(f))
        popup(f"{len(f) - len(newf)} duplicate lines have been removed", newf)
    except:
        error_message()


def get_all_txt(folder, text):

    try:
        all_files = listdir(folder)
        txtFiles = [f"{folder}/{file}" for file in all_files if '.txt' in file]
        for txt in txtFiles:
            text.insert(END, txt+'\n')
    except:
        error_message(title='Invalid Folder', message='Couldn\'t extract any txt files. Make sure the folder path is correct!')


def merge_files(paths):
    try:
        paths = paths.split('\n')
        paths = [path for path in paths if path not in ['', ' ']]
        if not paths:
            raise Exception
        bigfile = []
        numFiles = 0
        for path in paths:
            try:
                bigfile += [line.replace('\n', '') + '\n' for line in open(path, 'r', errors='ignore').readlines()]
                numFiles+=1
            except:
                error_message(message=f"The following file was not found or couldn't be open: {path}")

        popup(f'{numFiles} files have been merged successfully. The new file contains {len(bigfile)} lines', bigfile)
    except:
        error_message(title='No paths found', message="You have to load the txt files before merging them!")


def split_file(path, folder, lines_per_file):
    try:
        smallfile = None
        files = 0
        with open(path, 'r', errors='ignore') as bigfile:
            for lineno, line in enumerate(bigfile):
                if lineno % int(lines_per_file) == 0:
                    if smallfile:
                        smallfile.close()
                    name = path.split('/')[-1].split('.')[0]
                    small_filename = folder + '/' + name + '_{}.txt'.format(lineno + int(lines_per_file))
                    smallfile = open(small_filename, "w")
                    files += 1
                smallfile.write(line)
            if smallfile:
                smallfile.close()
            infoPopup(f"File has been split into {files} different parts")
    except:
        error_message()


def regex_editor(path, regex, option_selected):
    try:
        lines = open(path, 'r', errors='ignore').readlines()
        if option_selected=='Save Lines Matching Regex':
            results = [line.replace('\n', '') + '\n' for line in lines if bool(re.match(fr"{regex}", line))]
        else:
            results = [line.replace('\n', '') + '\n' for line in lines if not(bool(re.match(fr"{regex}", line)))]
        popup(f"{len(lines) - len(results)} lines have been removed", results)
    except:
        error_message()


def open_file(text_box, addNewEntry=False, countLines=False):

    file = filedialog.askopenfilename(title="Load File",
                               filetypes=(("Load File", "*.txt"), ("All", "*.*")))
    if file and addNewEntry==False:
        text_box.delete(0,END)
        text_box.insert(END, file)

    if file and addNewEntry is True:
        text_box.insert(END, file+'\n')

    if file and countLines is not False:
        try:
            lines = len(open(file, 'r', errors='ignore').readlines())
            countLines['text'] = f"Lines Loaded: {lines}"
        except:
            pass

def select_folder(text_box):

    folder = filedialog.askdirectory(title="Select Folder")

    if folder:
        text_box.delete(0, END)
        text_box.insert(END, folder)


def save_file(lst, popup):

    popup.destroy()
    files = [('Text Document', '*.txt'),
            ('All Files', '*.*')
             ]
    filepath = filedialog.asksaveasfile(title="Save File", filetypes=files, defaultextension=files)
    if filepath:
        with open(filepath.name, 'w') as f:
            for line in lst:
                f.write(line)


def B1():
    for widget in canvas2.winfo_children():
        widget.destroy()
    text_box = StringVar()
    text_box = tk.Entry(canvas2, textvariable=text_box, width=60, fg='white', bg='#696969')
    text_box.place(relx=0.5, rely=0.2, anchor=CENTER)

    tk.Button(canvas2, text='Load File', bg='#696969', fg="white", height=2, command=lambda:open_file(text_box)).place(relx=0.5, rely=0.1, anchor=CENTER)
    duplButton = tk.Button(canvas2, text='Remove Duplicates', bg='#696969', fg="white", height=3, command=lambda:duplicate(text_box.get()))
    duplButton.place(relx=0.5, rely=0.5, anchor=CENTER)


def B2():
    for widget in canvas2.winfo_children():
        widget.destroy()
    canvas = tk.Canvas(canvas2, width=600, bg="black")
    canvas.pack(fill=tk.BOTH, side=LEFT, expand=True)

    text_box = StringVar()
    text_box = tk.Entry(canvas, textvariable=text_box, width=60, fg='white', bg='#696969')
    text_box.place(relx=0.58, rely=0.1, anchor=CENTER)
    tk.Button(canvas, text='Select Folder', bg='#696969', fg="white", height=2, command=lambda:select_folder(text_box)).place(relx=0.1, rely=0.1, anchor=CENTER)

    f = tk.Frame(canvas)
    f.place(relx=0.5, rely=0.6, anchor=CENTER)

    scrollbar = Scrollbar(f)
    pathLoader = tk.Text(f, height=15, width=80, fg='white', bg='#696969', yscrollcommand=scrollbar.set)
    scrollbar.config(command=pathLoader.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    pathLoader.pack(side="left")

    tk.Button(canvas, text='Get all txt files from folder', bg='#696969', fg="white", height=2, command=lambda:get_all_txt(text_box.get(), pathLoader)).place(relx=0.2, rely=0.22, anchor=CENTER)
    tk.Button(canvas, text='Add txt file manually', bg='#696969', fg="white", height=2, command=lambda:open_file(pathLoader, addNewEntry=True)).place(relx=0.54, rely=0.22, anchor=CENTER)
    tk.Button(canvas, text='Clear', bg='#696969', fg="white", height=2, command=lambda:pathLoader.delete(1.0, END)).place(relx=0.8, rely=0.22, anchor=CENTER)

    mergeButton = tk.Button(canvas, text='Merge Files', bg='#696969', fg="white", height=2,
                           command=lambda: merge_files(pathLoader.get("1.0",END)))
    mergeButton.place(relx=0.5, rely=0.944, anchor=CENTER)


def B3():
    for widget in canvas2.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(canvas2, width=600, bg="black")
    canvas.pack(fill=tk.BOTH, side=LEFT, expand=True)

    frame = tk.Frame(canvas, background="black")
    frame.place(relx=0.5, rely=0.25, anchor=CENTER)

    text = StringVar()
    text.set("Path: ")
    labelDir = Label(frame, textvariable=text, fg='white', height=4, bg='black')
    labelDir.grid(row=1, column=1)

    path = StringVar()
    text_box = tk.Entry(frame, textvariable=path, width=60, fg='white', bg='#696969')
    text_box.grid(row=1, column=2)

    tk.Button(frame, text='Select Output Folder', bg='#696969', fg="white", height=1,
              command=lambda: select_folder(out_folder)).grid(row=3, column=1)
    out_folder = StringVar()
    out_folder = tk.Entry(frame, textvariable=out_folder, width=53, fg='white', bg='#696969')
    out_folder.grid(row=3, column=2, columnspan=2)


    frame2 = tk.Frame(canvas, background="black")
    frame2.place(relx=0.23, rely=0.55, anchor=CENTER)
    text = StringVar()
    text.set("Lines Per File: ")
    textDir = Label(frame2, textvariable=text, fg='white', height=4, bg='black')
    textDir.grid(row=1, column=1)

    linesPerFile = StringVar()
    linesPerFile = tk.Entry(frame2, textvariable=linesPerFile, fg='white', bg='#696969')
    linesPerFile.grid(row=1, column=2)

    loaded = Label(canvas, text="Lines Loaded: 0", fg='white', bg='black')
    loaded.place(relx=0.75, rely=0.55, anchor=CENTER)

    tk.Button(frame, text='Load File', bg='#696969', fg="white", height=2, command=lambda:open_file(text_box, countLines=loaded)).grid(row=0, column=2)
    tk.Button(canvas, text='Split File', bg='#696969', fg="white", height=2, command=lambda: split_file(path.get(), out_folder.get(), linesPerFile.get())).place(relx=0.5, rely=0.8, anchor=CENTER)

def B4():
    for widget in canvas2.winfo_children():
        widget.destroy()
    
    canvas = tk.Canvas(canvas2, width=600, bg="black")
    canvas.pack(fill=tk.BOTH, side=LEFT, expand=True)
    
    text_box = StringVar()
    text_box = tk.Entry(canvas, textvariable=text_box, width=60, fg='white', bg='#696969')
    text_box.place(relx=0.58, rely=0.2, anchor=CENTER)
    tk.Button(canvas, text='Load File', bg='#696969', fg="white", height=2, command=lambda:open_file(text_box)).place(relx=0.1, rely=0.2, anchor=CENTER)

    frame2 = tk.Frame(canvas, background="black")
    frame2.place(relx=0.23, rely=0.55, anchor=CENTER)
    text = StringVar()
    text.set("Regex: ")
    textDir = Label(frame2, textvariable=text, fg='white', height=4, bg='black')
    textDir.grid(row=1, column=1)

    regex = StringVar()
    regex = tk.Entry(frame2, textvariable=regex, fg='white', bg='#696969')
    regex.grid(row=1, column=2)

    data=['Save Lines Matching Regex', 'Remove Lines Matching Regex']
    var = StringVar()
    var.set('Save Lines Matching Regex')
    p = OptionMenu(canvas, var, *data).place(relx=0.75, rely=0.55, anchor=CENTER)

    tk.Button(canvas, text='Execute', bg='#696969', fg="white", height=2, command=lambda: regex_editor(text_box.get(), regex.get(), var.get())).place(relx=0.5, rely=0.8, anchor=CENTER)



button1 = tk.Button(canvas1, text='Duplicates', bg='#696969', fg="white", height=3, command=lambda:B1()).pack(fill=tk.X)
button2 = tk.Button(canvas1, text='Merge Files', bg='#696969', fg="white", height=3, command=lambda:B2()).pack(fill=tk.X)
button3 = tk.Button(canvas1, text='Split File', bg='#696969', fg="white", height=3, command=lambda:B3()).pack(fill=tk.X)
button4 = tk.Button(canvas1, text='Regex', bg='#696969', fg="white", height=3, command=lambda:B4()).pack(fill=tk.X)

root.mainloop()
