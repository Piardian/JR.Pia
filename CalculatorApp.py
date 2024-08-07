import tkinter as tk
from tkinter import *
from tkinter import ttk
import requests
import math
from datetime import datetime, timedelta
# Küresel değişkenler
hesap = []
s1 = []
yeni_islem = True
yuzde = False
gecmis = []
class Screen1:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator(Basic)")
        self.master.geometry("300x400")
        self.master.configure(background='black')
        self.master.resizable(width=False, height=False)

        self.giris = tk.Entry(self.master, width=29, bd=4, justify=RIGHT, font=('Times', 19))
        self.giris.place(height=60, width=275, x=13, y=20)

        self.master.bind("<Tab>", lambda event: "break")
        self.giris.bind("<FocusIn>", lambda event: "break")
        self.giris.bind("<Button-1>", lambda event: "break")

        self.master.bind("<Return>", lambda event: self.hesapla())
        self.master.bind("<KP_Divide>", lambda event: self.islemler("/"))
        self.master.bind("<KP_Multiply>", lambda event: self.islemler("*"))
        self.master.bind("<KP_Subtract>", lambda event: self.islemler("-"))
        self.master.bind("<KP_Add>", lambda event: self.islemler("+"))
        self.master.bind("<percent>", lambda event: self.islemler("%"))
        self.master.bind("<BackSpace>", lambda event: self.sil())
        self.master.bind("<KP_Enter>", lambda event: self.hesapla())
        self.master.bind("<Key>", lambda event: self.klavye_islemleri(event))
        self.master.bind("<O>", lambda event: self.Octune(event))

        buttons = [
            {"text": "1", "command": lambda: self.yaz(1), "pos": (15, 160)},
            {"text": "2", "command": lambda: self.yaz(2), "pos": (85, 160)},
            {"text": "3", "command": lambda: self.yaz(3), "pos": (155, 160)},
            {"text": "4", "command": lambda: self.yaz(4), "pos": (15, 220)},
            {"text": "5", "command": lambda: self.yaz(5), "pos": (85, 220)},
            {"text": "6", "command": lambda: self.yaz(6), "pos": (155, 220)},
            {"text": "7", "command": lambda: self.yaz(7), "pos": (15, 280)},
            {"text": "8", "command": lambda: self.yaz(8), "pos": (85, 280)},
            {"text": "9", "command": lambda: self.yaz(9), "pos": (155, 280)},
            {"text": ".", "command": lambda: self.yaz("."), "pos": (155, 340)},
            {"text": "0", "command": lambda: self.yaz(0), "pos": (15, 340), "width": 10},
            {"text": "x", "command": lambda: self.islemler("*"), "pos": (155, 100)},
            {"text": "÷", "command": lambda: self.islemler("/"), "pos": (85, 100)},
            {"text": "%", "command": lambda: self.islemler("%"), "pos": (15, 100)},
            {"text": "+", "command": lambda: self.islemler("+"), "pos": (225, 280)},
            {"text": "-", "command": lambda: self.islemler("-"), "pos": (225, 220)},
            {"text": "=", "command": self.hesapla, "pos": (225, 340)},
            {"text": "C", "command": self.temizle, "pos": (225, 100)},
            {"text": "⌫", "command": self.sil, "pos": (225, 160)},
        ]

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))

        for button in buttons:
            width = button.get("width", 4)
            ttk.Button(self.master, width=width, text=button["text"], command=button["command"]).place(height=44, x=button["pos"][0], y=button["pos"][1])

        Button(self.master, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=self.ikinci_pencere).place(height=15, x=1, y=1)
        Button(self.master, width=1,  text="⟳", fg="white", font=('FontAwesome', 9),  background='black',highlightbackground="black",highlightcolor="black",
        highlightthickness=0,relief="flat",command=self.gecmisi_goster).place(height=15,x=275, y=3)

    def yaz(self, x):
        global yeni_islem
        if yeni_islem:
            self.giris.delete(0, 'end')
            yeni_islem = False
        s = len(self.giris.get())
        self.giris.insert(s, str(x))

    def islemler(self, x):
        global hesap
        global s1
        global yuzde
        global yeni_islem

        if yeni_islem and x not in "+-*/%":
            self.giris.delete(0, 'end')
            yeni_islem = False

        if x in "+-*/":
            try:
                s1.append(float(self.giris.get()))
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append(x)
            self.giris.delete(0, 'end')
        elif x == "%":
            yuzde = True
            try:
                s1.append(float(self.giris.get()))
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            self.giris.delete(0, 'end')
        else:
            self.giris.insert(END, x)

    def hesapla(self):
        global s1
        global hesap
        global yuzde
        global yeni_islem
        global gecmis

        try:
            if yuzde:
                yuzde_degeri = float(self.giris.get())
                s1[-1] = (yuzde_degeri / 100) * s1[-1]
                yuzde = False
            else:
                s1.append(float(self.giris.get()))

            sonuc = s1[0]
            for i in range(1, len(s1)):
                if hesap[i-1] == '+':
                    sonuc += s1[i]
                elif hesap[i-1] == '-':
                    sonuc -= s1[i]
                elif hesap[i-1] == '/':
                    if s1[i] != 0:
                        sonuc /= s1[i]
                    else:
                        self.giris.delete(0, 'end')
                        self.giris.insert(0, "Hata: Sıfıra bölme")
                        hesap = []
                        s1 = []
                        yeni_islem = True
                        return
                elif hesap[i-1] == '*':
                    sonuc *= s1[i]
            if sonuc.is_integer():
             sonuc = int(sonuc)
            sonuc_str = str(sonuc)
            if sonuc % 1 == 0:
                sonuc_str = str(int(sonuc))
            islem_str = ' '.join(f"{s1[i]} {hesap[i]}" for i in range(len(hesap))) + f" {s1[-1]} = {sonuc_str}"

            gecmis.append(islem_str)

            self.giris.delete(0, 'end')
            self.giris.insert(0, sonuc_str)
            hesap = []
            s1 = []
            yeni_islem = True  # Yeni işlem başladığını belirt
        except ValueError:
            self.giris.delete(0, 'end')
            self.giris.insert(0, "Hata")
            hesap = []
            s1 = []
            yeni_islem = True  # Yeni işlem başladığını belirt

    def sil(self):
        self.giris.delete(len(self.giris.get()) - 1)

    def temizle(self):
        global hesap
        global s1
        global yeni_islem
        self.giris.delete(0, 'end')
        hesap = []
        s1 = []
        yeni_islem = True
    
    def goto_advanced(self):
        self.master.withdraw()
        AdvancedCalculator(tk.Toplevel(self.master))

    def goto_screen2(self):
        self.master.withdraw()
        screen2 = Screen2(tk.Toplevel(self.master))
    
    def goto_screen3(self):
        self.master.withdraw()
        screen3 = Screen3(tk.Toplevel(self.master))    

    def goto_screen4(self):
        self.master.withdraw()
        screen4 = Screen4(tk.Toplevel(self.master)) 
        
    def goto_screen5(self):
        self.master.withdraw()
        screen5 = Screen5(tk.Toplevel(self.master))

    def goto_screen6(self):
        self.master.withdraw()
        screen6 = Screen6(tk.Toplevel(self.master))

    def goto_screen7(self):
        self.master.withdraw()
        screen7 = Screen7(tk.Toplevel(self.master))       
    
    def ikinci_pencere(self):
     ikinci_pencere = tk.Frame(self.master, bg="black", bd=2, relief="sunken")
     ikinci_pencere.place(x=1, y=1, width=100, height=280)
     label = tk.Label(ikinci_pencere, text="√", fg="pink", bg="black", font=("Roboto", 15))
     label.place(x=60, y=25, width=30, height=25)  
     label = tk.Label(ikinci_pencere, text="📏", fg="white", bg="black", font=("Roboto", 15))
     label.place(x=60, y=60, width=30, height=25)  
     label = tk.Label(ikinci_pencere, text="💧", fg="lightblue", bg="black", font=("Roboto", 15))
     label.place(x=60, y=95, width=30, height=25)  
     label = tk.Label(ikinci_pencere, text="⚖️", fg="gray", bg="black", font=("Roboto", 15))
     label.place(x=60, y=130, width=30, height=25)  
     label = tk.Label(ikinci_pencere, text="💱", fg="lightgreen", bg="black", font=("Roboto", 15))
     label.place(x=60, y=165, width=30, height=25)  
     label = tk.Label(ikinci_pencere, text="₿", fg="orange", bg="black", font=("Roboto", 15))
     label.place(x=60, y=203, width=30, height=25)
     label = tk.Label(ikinci_pencere, text="🕙", fg="white", bg="black", font=("Roboto", 15))
     label.place(x=60, y=235, width=30, height=25)  
    
     destroy_button = tk.Button(ikinci_pencere, width=1, text="...", fg="black", font=("Helvetica", 7), background='white', command=ikinci_pencere.destroy)
     destroy_button.place(height=15, x=0, y=0)
     scr1_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Roboto", 11), background='white', text="Length", command=self.goto_screen2)
     scr1_button.place(height=20, x=0, y=65)  
     scr2_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Futura", 11), background='white', text="Liquid ", command=self.goto_screen3)
     scr2_button.place(height=20, x=0, y=100)  
     scr3_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Lato", 11), background='white', text="Mass", command=self.goto_screen4)
     scr3_button.place(height=20, x=0, y=135)  
     scr4_button = tk.Button(ikinci_pencere, width=7, fg="black", font=("Helvetica", 9), background='white', text="Exchange", command=self.goto_screen5)
     scr4_button.place(height=20, x=0, y=170) 
     scr5_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Montserrat", 11), background='white', text="Cyrpto", command=self.goto_screen6)
     scr5_button.place(height=20, x=0, y=205)  
     scr6_button = tk.Button(ikinci_pencere, width=7, fg="black", font=("Helvetica", 9), background='white', text="Advanced", command=self.goto_advanced)
     scr6_button.place(height=20, x=0, y=30)
     scr7_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Helvetica", 12), background='white', text="Time", command=self.goto_screen7)
     scr7_button.place(height=20, x=0, y=240)
     
    
    
    def gecmisi_goster(self):
     
        global gecmis

        gecmisi_goster =tk.Frame(self.master,bg="black")
        gecmisi_goster.place(x=180, y=0,width=140, height=200)
    

        listbox = tk.Listbox(gecmisi_goster,width=20,font=("Montserrat", 9),fg="white",bd=0,bg="black",background="black",relief="flat",highlightbackground="black",highlightcolor="black")
        listbox.pack(expand=True, fill='both')
        listbox.place(x=3, y=20)
    
        for item in gecmis:
         listbox.insert(END, item)

        def kopyala(self):
            self.giris.delete(0, 'end')
            secilen = listbox.get(listbox.curselection())
            self.giris.insert(0, secilen.split(' = ')[0])
            gecmisi_goster.destroy()

        Button(gecmisi_goster, width=8, text="Kopyala", fg="white", font=("Helvetica", 13),  background='black',highlightbackground="black",highlightcolor="black",highlightthickness=0,relief="flat",command=kopyala).place(height=18,x=20, y=170)
   
    
        Button(gecmisi_goster, width=1, text="⟳", fg="white", font=('FontAwesome', 9),  background='black',highlightbackground="black",highlightcolor="black",highlightthickness=2,relief="flat",command=gecmisi_goster.destroy).place(height=15,x=92, y=2)
    
    
    def Octune(self, event):
        if event.char == 'O' or event.char == 'o':
            self.giris.insert(tk.END, "Ez")

    def klavye_islemleri(self, event):
        if event.char in '0123456789':
            self.yaz(event.char)
        elif event.char in '+-*/%':
            self.islemler(event.char)
        elif event.char == '\r':
            self.hesapla()
        elif event.char == '.':
            self.yaz('.')
        elif event.char == 'o':
            self.Octune(event)

class AdvancedCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator (Advanced)")
        self.master.geometry("510x400")
        self.master.configure(background='black')
        self.master.resizable(width=False, height=False)
        
        global yeni_islem
        global hesap
        global s1
        global yuzde

        hesap = []
        s1 = []
        yeni_islem = True
        yuzde = False

        self.giris = tk.Entry(self.master, width=29, bd=4, justify=RIGHT, font=('Times', 19))
        self.giris.place(height=60, width=483, x=13, y=20)

        self.master.bind("<Tab>", lambda event: "break")
        self.giris.bind("<FocusIn>", lambda event: "break")
        self.giris.bind("<Button-1>", lambda event: "break")

        self.master.bind("<Return>", lambda event: self.hesapla())
        self.master.bind("<KP_Divide>", lambda event: self.islemler("/"))
        self.master.bind("<KP_Multiply>", lambda event: self.islemler("*"))
        self.master.bind("<KP_Subtract>", lambda event: self.islemler("-"))
        self.master.bind("<KP_Add>", lambda event: self.islemler("+"))
        self.master.bind("<percent>", lambda event: self.islemler("%"))
        self.master.bind("<BackSpace>", lambda event: self.sil())
        self.master.bind("<KP_Enter>", lambda event: self.hesapla())
        self.master.bind("<Key>", lambda event: self.klavye_islemleri(event))
        self.master.bind("<O>", lambda event: self.Octune(event))

        buttons = [
            {"text": "i", "command": lambda: self.yaz("i"), "pos": (15, 340)},
            {"text": "sin", "command": lambda: self.islemler("sin"), "pos": (15, 100)},
            {"text": "cos", "command": lambda: self.islemler("cos"), "pos": (15, 160)},
            {"text": "tan", "command": lambda: self.islemler("tan"), "pos": (15, 220)},
            {"text": "cot", "command": lambda: self.islemler("cot"), "pos": (15, 280)},
            {"text": "(", "command": lambda: self.islemler("("), "pos": (85, 340)},
            {"text": "π", "command": lambda: self.islemler("π"), "pos": (85, 100)},
            {"text": "x", "command": lambda: self.yaz("x"), "pos": (85, 160)},
            {"text": "√", "command": lambda: self.islemler("√"), "pos": (85, 220)},
            {"text": "log", "command": lambda: self.islemler("log"), "pos": (85, 280)},
            {"text": ")", "command": lambda: self.islemler(")"), "pos": (155, 340)},
            {"text": "e", "command": lambda: self.islemler("e"), "pos": (155, 100)},
            {"text": "x³", "command": lambda: self.islemler("x³"), "pos": (155, 160)},
            {"text": "x²", "command": lambda: self.islemler("x²"), "pos": (155, 220)},
            {"text": "x!", "command": lambda: self.islemler("x!"), "pos": (155, 280)},
            {"text": "1", "command": lambda: self.yaz(1), "pos": (225, 160)},
            {"text": "2", "command": lambda: self.yaz(2), "pos": (295, 160)},
            {"text": "3", "command": lambda: self.yaz(3), "pos": (365, 160)},
            {"text": "4", "command": lambda: self.yaz(4), "pos": (225, 220)},
            {"text": "5", "command": lambda: self.yaz(5), "pos": (295, 220)},
            {"text": "6", "command": lambda: self.yaz(6), "pos": (365, 220)},
            {"text": "7", "command": lambda: self.yaz(7), "pos": (225, 280)},
            {"text": "8", "command": lambda: self.yaz(8), "pos": (295, 280)},
            {"text": "9", "command": lambda: self.yaz(9), "pos": (365, 280)},
            {"text": ".", "command": lambda: self.yaz("."), "pos": (365, 340)},
            {"text": "0", "command": lambda: self.yaz(0), "pos": (225, 340), "width": 10},
            {"text": "x", "command": lambda: self.islemler("*"), "pos": (365, 100)},
            {"text": "÷", "command": lambda: self.islemler("/"), "pos": (295, 100)},
            {"text": "%", "command": lambda: self.islemler("%"), "pos": (225, 100)},
            {"text": "+", "command": lambda: self.islemler("+"), "pos": (435, 280)},
            {"text": "-", "command": lambda: self.islemler("-"), "pos": (435, 220)},
            {"text": "=", "command": self.hesapla, "pos": (435, 340)},
            {"text": "C", "command": self.temizle, "pos": (435, 100)},
            {"text": "⌫", "command": self.sil, "pos": (435, 160)},
        ]

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))

        for button in buttons:
            width = button.get("width", 4)
            ttk.Button(self.master, width=width, text=button["text"], command=button["command"]).place(height=44, x=button["pos"][0], y=button["pos"][1])
            self.ikinci_pencere_button = tk.Button(master, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=self.ikinci_pencere)
            self.ikinci_pencere_button.place(height=15, x=1, y=1)
            
        

    def yaz(self, x):
        global yeni_islem
        if yeni_islem:
            self.giris.delete(0, 'end')
            yeni_islem = False
        s = len(self.giris.get())
        self.giris.insert(s, str(x))

    def islemler(self, x):
        global hesap
        global s1
        global yuzde
        global yeni_islem

        if yeni_islem and x not in "+-*/%()":
            self.giris.delete(0, 'end')
            yeni_islem = False

        if x in "+-*/":
            try:
                s1.append(self.giris.get())
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append(x)
            self.giris.delete(0, 'end')
        elif x == "%":
            yuzde = True
            try:
                s1.append(self.giris.get())
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            self.giris.delete(0, 'end')
        elif x == "x²":
            try:
                s1.append(f"({self.giris.get()})**2")
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append("")
            self.hesapla()
        elif x == "x³":
            try:
                s1.append(f"({self.giris.get()})**3")
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append("")
            self.hesapla()
        elif x == "√":
            try:
                s1.append(f"math.sqrt({self.giris.get()})")
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append("")
            self.hesapla()
        elif x == "sin":
            try:
                s1.append(f"math.sin(math.radians({self.giris.get()}))")
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append("")
            self.hesapla()
        elif x == "cos":
            try:
                s1.append(f"math.cos(math.radians({self.giris.get()}))")
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append("")
            self.hesapla()
        elif x == "tan":
            try:
                s1.append(f"math.tan(math.radians({self.giris.get()}))")
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append("")
            self.hesapla()
        elif x == "cot":
            try:
                s1.append(f"1/math.tan(math.radians({self.giris.get()}))")
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append("")
            self.hesapla()
        elif x == "π":
            self.yaz(math.pi)
        elif x == "e":
            self.yaz(math.e)
        elif x == "log":
            try:
                s1.append(f"math.log10({self.giris.get()})")
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append("")
            self.hesapla()
        elif x == "x!":
            try:
                s1.append(f"math.factorial({self.giris.get()})")
            except ValueError:
                self.giris.delete(0, 'end')
                self.giris.insert(0, "Hata")
                return
            hesap.append("")
            self.hesapla()
        elif x in "()":
            self.yaz(x)
        else:
            self.giris.insert(END, x)

    def hesapla(self):
        global s1
        global hesap
        global yuzde
        global yeni_islem

        try:
            if yuzde:
                yuzde_degeri = float(self.giris.get())
                s1[-1] = f"({s1[-1]}*{yuzde_degeri}/100)"
                yuzde = False
            else:
                if len(hesap) == 0 or hesap[-1] != "":
                    s1.append(self.giris.get())

            hesap_str = "".join([f"{s1[i]}{hesap[i]}" for i in range(len(hesap))])
            if len(s1) > len(hesap):
                hesap_str += s1[-1]

            sonuc = eval(hesap_str)
            sonuc_str = str(sonuc)
            if sonuc % 1 == 0:
                sonuc_str = str(int(sonuc))

            self.giris.delete(0, 'end')
            self.giris.insert(0, sonuc_str)
            hesap = []
            s1 = []
            yeni_islem = True
        except (ValueError, SyntaxError):
            self.giris.delete(0, 'end')
            self.giris.insert(0, "Hata")
            hesap = []
            s1 = []
            yeni_islem = True

    def sil(self):
        self.giris.delete(len(self.giris.get()) - 1)

    def temizle(self):
        global hesap
        global s1
        global yeni_islem
        self.giris.delete(0, 'end')
        hesap = []
        s1 = []
        yeni_islem = True

    def klavye_islemleri(self, event):
        if event.char in '0123456789':
            self.yaz(event.char)
        elif event.char in '+-*/%()':
            self.islemler(event.char)
        elif event.char == '\r':
            self.hesapla()
        elif event.char == '.':
            self.yaz('.')
            
    def Octune(self,event):
        a=self.giris.get()
        try:
            if a[:2]=='0x':
                self.giris.delete(0, 'end')
                self.giris.insert(0, str(int(a, 16)))
            elif a[:2]=='0b':
                self.giris.delete(0, 'end')
                self.giris.insert(0, str(int(a, 2)))
            elif a[:2]=='0o':
                self.giris.delete(0, 'end')
                self.giris.insert(0, str(int(a, 8)))
        except:
            pass

    def goto_screen1(self):
        self.master.withdraw()
        screen1 = Screen1(tk.Toplevel(self.master))   

    def goto_advanced(self):
        self.master.withdraw()
        AdvancedCalculator = AdvancedCalculator(tk.Toplevel(self.master))

    def ikinci_pencere(self):
        ikinci_pencere = tk.Frame(self.master, bg="black", bd=2, relief="sunken")
        ikinci_pencere.place(x=1, y=1, width=100, height=70)
        label = tk.Label(ikinci_pencere, text="🟰", fg="purple", bg="black", font=("Roboto", 15))
        label.place(x=60, y=25, width=30, height=25)
        destroy_button = tk.Button(ikinci_pencere, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=ikinci_pencere.destroy)
        destroy_button.place(height=15, x=0, y=0)
        scr1_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Roboto", 8), background='white', text="Calculator", command=self.goto_screen1)
        scr1_button.place(height=18, x=1, y=30)
                    


class Screen2:
    def __init__(self, master):
        self.master = master
        self.master.title("Lenght")
        self.master.geometry("293x460")
        self.master.configure(background='black')
        self.master.resizable(width=False, height=False)

        self.giris = tk.Entry(self.master, width=29,  justify=tk.RIGHT, font=('Helvetica', 16))
        self.giris.place(height=60, width=265, x=15, y=22)

        # Sonuç alanı
        self.sonuc_giris = ttk.Entry(self.master, width=29, justify=tk.RIGHT, font=("Helvetica", 16))
        self.sonuc_giris.place(height=60, width=265, x=15, y=90)

        # Seçim baloncuğu için bir StringVar oluştur
        self.secim_var1 = tk.StringVar()
        self.secim_var2 = tk.StringVar()

        # Seçenekler listesi
        secenekler = ["Milimetre", "Santimetre", "Desimetre", "Metre", "Dekametre", "Hektometre", "Kilometre"]

        # 1. Combobox (Seçim baloncuğu) oluştur
        self.combobox1 = ttk.Combobox(self.master, textvariable=self.secim_var1, values=secenekler, state="readonly")
        self.combobox1.bind("<<ComboboxSelected>>", self.secim_degisti)
        self.combobox1.place(width=83, height=17, x=15, y=64)

        # 2. Combobox (Seçim baloncuğu) oluştur
        self.combobox2 = ttk.Combobox(self.master, textvariable=self.secim_var2, values=secenekler, state="readonly")
        self.combobox2.bind("<<ComboboxSelected>>", self.secim_degisti)
        self.combobox2.place(width=83, height=17, x=15, y=132)
       
        
        buttons = [
            {"text": "Dönüştür", "command": self.birim_donustur, "x": 145, "y": 400, "width": 10},
            {"text": "C", "command": self.temizle, "x": 105, "y": 160},
            {"text": "⌫", "command": self.sil, "x": 195, "y": 160},
            {"text": "1", "command": lambda: self.yaz(1), "x": 15, "y": 220},
            {"text": "2", "command": lambda: self.yaz(2), "x": 105, "y": 220},
            {"text": "3", "command": lambda: self.yaz(3), "x": 195, "y": 220},
            {"text": "4", "command": lambda: self.yaz(4), "x": 15, "y": 280},
            {"text": "5", "command": lambda: self.yaz(5), "x": 105, "y": 280},
            {"text": "6", "command": lambda: self.yaz(6), "x": 195, "y": 280},
            {"text": "7", "command": lambda: self.yaz(7), "x": 15, "y": 340},
            {"text": "8", "command": lambda: self.yaz(8), "x": 105, "y": 340},
            {"text": "9", "command": lambda: self.yaz(9), "x": 195, "y": 340},
            {"text": ".", "command": lambda: self.yaz("."), "x": 15, "y": 160},
            {"text": "0", "command": lambda: self.yaz(0), "x": 17, "y": 400, "width": 9}
        ]

        for button in buttons:
            ttk.Button(
                self.master, 
                text=button["text"], 
                command=button["command"], 
                width=button.get("width", 6)
            ).place(height=44, x=button["x"], y=button["y"])


        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))

        self.ikinci_pencere_button = tk.Button(master, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=self.ikinci_pencere)
        self.ikinci_pencere_button.place(height=15, x=1, y=1)

    def yaz(self, x):
        self.giris.insert(tk.END, str(x))

    def secim_degisti(self, event):
        secilen1 = self.secim_var1.get()
        secilen2 = self.secim_var2.get()
        print(f"Seçilen 1: {secilen1}")
        print(f"Seçilen 2: {secilen2}")

    def sil(self):
        self.giris.delete(len(self.giris.get()) - 1)

    def temizle(self):
        self.giris.delete(0, tk.END)
        self.sonuc_giris.delete(0, tk.END)

    def goto_screen1(self):
        self.master.withdraw()
        screen1 = Screen1(tk.Toplevel(self.master))

    def goto_screen3(self):
        self.master.withdraw()
        screen3 = Screen3(tk.Toplevel(self.master))

    
    def goto_screen5(self):
        self.master.withdraw()
        screen5 = Screen5(tk.Toplevel(self.master))

    def goto_screen6(self):
        self.master.withdraw()
        screen6 = Screen6(tk.Toplevel(self.master))        

    def birim_donustur(self):
        try:
            deger = float(self.giris.get())
            birim1 = self.secim_var1.get()
            birim2 = self.secim_var2.get()
            # Önce birimi metreye çevir
            if birim1 == "Kilometre":
                deger_metre = deger * 1000
            elif birim1 == "Hektometre":
                deger_metre = deger * 100
            elif birim1 == "Dekametre":
                deger_metre = deger * 10
            elif birim1 == "Metre":
                deger_metre = deger
            elif birim1 == "Desimetre":
                deger_metre = deger * 0.1
            elif birim1 == "Santimetre":
                deger_metre = deger * 0.01
            elif birim1 == "Milimetre":
                deger_metre = deger * 0.001
            elif birim1 == "Mikrometre":
                deger_metre = deger * 1e-6
            elif birim1 == "Nanometre":
                deger_metre = deger * 1e-9
            elif birim1 == "Pikometre":
                deger_metre = deger * 1e-12
            elif birim1 == "Femtometre":
                deger_metre = deger * 1e-15
            elif birim1 == "Attometre":
                deger_metre = deger * 1e-18
            elif birim1 == "Işık Yılı":
                deger_metre = deger * 9.461e+15
            else:
                sonuc = "Geçersiz birim"
                self.sonuc_giris.delete(0, 'end')
                self.sonuc_giris.insert(0, sonuc)
                return

            # Metreden hedef birime çevir
            if birim2 == "Kilometre":
                sonuc = deger_metre / 1000
            elif birim2 == "Hektometre":
                sonuc = deger_metre / 100
            elif birim2 == "Dekametre":
                sonuc = deger_metre / 10
            elif birim2 == "Metre":
                sonuc = deger_metre
            elif birim2 == "Desimetre":
                sonuc = deger_metre / 0.1
            elif birim2 == "Santimetre":
                sonuc = deger_metre / 0.01
            elif birim2 == "Milimetre":
                sonuc = deger_metre / 0.001
            elif birim2 == "Mikrometre":
                sonuc = deger_metre / 1e-6
            elif birim2 == "Nanometre":
                sonuc = deger_metre / 1e-9
            elif birim2 == "Pikometre":
                sonuc = deger_metre / 1e-12
            elif birim2 == "Femtometre":
                sonuc = deger_metre / 1e-15
            elif birim2 == "Attometre":
                sonuc = deger_metre / 1e-18
            elif birim2 == "Işık Yılı":
                sonuc = deger_metre / 9.461e+15
            else:
                sonuc = "Geçersiz birim"

            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, str(sonuc))
        except ValueError:
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, "Geçersiz giriş")

        self.master.bind("<Return>", lambda event: self.birim_donustur())
        self.master.bind("<BackSpace>", lambda event: self.sil())
        self.master.bind("<KP_Enter>", lambda event: self.birim_donustur())
        self.master.bind("<Key>", lambda event: self.klavye_islemleri(event))

    def klavye_islemleri(self, event):
        if event.char in '0123456789':
            self.yaz(event.char)
        elif event.char == '\r':
            self.birim_donustur()
        elif event.char == '.':
            self.yaz('.')


    def goto_screen4(self):
        self.master.withdraw()
        screen4 = Screen4(tk.Toplevel(self.master))    
    
    def goto_screen5(self):
        self.master.withdraw()
        screen5 = Screen5(tk.Toplevel(self.master))

    def goto_screen7(self):
        self.master.withdraw()
        screen7 = Screen7(tk.Toplevel(self.master))      
 
    def ikinci_pencere(self):
        ikinci_pencere = tk.Frame(self.master, bg="black", bd=2, relief="sunken")
        ikinci_pencere.place(x=1, y=1, width=100, height=250)
        label = tk.Label(ikinci_pencere, text="🟰", fg="purple", bg="black", font=("Roboto", 15))
        label.place(x=60, y=25, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💧", fg="lightblue", bg="black", font=("Roboto", 15))
        label.place(x=60, y=60, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="⚖️", fg="gray", bg="black", font=("Roboto", 15))
        label.place(x=60, y=95, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💱", fg="lightgreen", bg="black", font=("Roboto", 15))
        label.place(x=60, y=130, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="₿", fg="orange", bg="black", font=("Roboto", 15))
        label.place(x=60, y=165, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="🕙", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=200, width=30, height=25) 

        destroy_button = tk.Button(ikinci_pencere, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=ikinci_pencere.destroy)
        destroy_button.place(height=15, x=0, y=0)
        scr1_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Roboto", 8), background='white', text="Calculator", command=self.goto_screen1)
        scr1_button.place(height=18, x=1, y=30)
        scr2_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Futura", 11), background='white', text="Liquid ", command=self.goto_screen3)
        scr2_button.place(height=18, x=1, y=65)
        scr3_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Lato", 11), background='white', text="Mass", command=self.goto_screen4)
        scr3_button.place(height=18, x=1, y=100)
        scr4_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Open Sans", 8), background='white', text="Exchange", command=self.goto_screen5)
        scr4_button.place(height=18, x=1, y=135)  
        scr5_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Montserrat", 11), background='white', text="Cyrpto", command=self.goto_screen6)
        scr5_button.place(height=18, x=1, y=170)
        scr6_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Helvetica", 12), background='white', text="Time", command=self.goto_screen7)
        scr6_button.place(height=20, x=0, y=205)
        
class Screen3:
    def __init__(self, master):
        self.master = master
        self.master.title("Liquid")
        self.master.geometry("293x460")
        self.master.configure(background='black')
        self.master.resizable(width=False, height=False)
        self.giris = tk.Entry(self.master, width=29,  justify=tk.RIGHT, font=('Helvetica', 16))
        self.giris.place(height=60, width=265, x=15, y=22)
        self.giris = tk.Entry(self.master, width=29,  justify=tk.RIGHT, font=('Helvetica', 16))
        self.giris.place(height=60, width=265, x=15, y=22)

        # Sonuç alanı
        self.sonuc_giris = ttk.Entry(self.master, width=29, justify=tk.RIGHT, font=("Helvetica", 16))
        self.sonuc_giris.place(height=60, width=265, x=15, y=90)

        # Seçim baloncuğu için bir StringVar oluştur
        self.secim_var1 = tk.StringVar()
        self.secim_var2 = tk.StringVar()

        # Seçenekler listesi
        secenekler = ["Mililitre","Santilitre","Desilitre","Litre/dm³","Dekalitre","Hektolitre","Ton/m³"]


        # 1. Combobox (Seçim baloncuğu) oluştur
        self.combobox1 = ttk.Combobox(self.master, textvariable=self.secim_var1, values=secenekler, state="readonly")
        self.combobox1.bind("<<ComboboxSelected>>", self.secim_degisti)
        self.combobox1.place(width=83, height=17, x=15, y=64)

        # 2. Combobox (Seçim baloncuğu) oluştur
        self.combobox2 = ttk.Combobox(self.master, textvariable=self.secim_var2, values=secenekler, state="readonly")
        self.combobox2.bind("<<ComboboxSelected>>", self.secim_degisti)
        self.combobox2.place(width=83, height=17, x=15, y=132)
       
      
        buttons = [
            {"text": "Dönüştür", "command": self.birim_donustur, "x": 145, "y": 400, "width": 10},
            {"text": "C", "command": self.temizle, "x": 105, "y": 160},
            {"text": "⌫", "command": self.sil, "x": 195, "y": 160},
            {"text": "1", "command": lambda: self.yaz(1), "x": 15, "y": 220},
            {"text": "2", "command": lambda: self.yaz(2), "x": 105, "y": 220},
            {"text": "3", "command": lambda: self.yaz(3), "x": 195, "y": 220},
            {"text": "4", "command": lambda: self.yaz(4), "x": 15, "y": 280},
            {"text": "5", "command": lambda: self.yaz(5), "x": 105, "y": 280},
            {"text": "6", "command": lambda: self.yaz(6), "x": 195, "y": 280},
            {"text": "7", "command": lambda: self.yaz(7), "x": 15, "y": 340},
            {"text": "8", "command": lambda: self.yaz(8), "x": 105, "y": 340},
            {"text": "9", "command": lambda: self.yaz(9), "x": 195, "y": 340},
            {"text": ".", "command": lambda: self.yaz("."), "x": 15, "y": 160},
            {"text": "0", "command": lambda: self.yaz(0), "x": 17, "y": 400, "width": 9}
        ]

        for button in buttons:
            ttk.Button(
                self.master, 
                text=button["text"], 
                command=button["command"], 
                width=button.get("width", 6)
            ).place(height=44, x=button["x"], y=button["y"])


        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))

        self.ikinci_pencere_button = tk.Button(master, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=self.ikinci_pencere)
        self.ikinci_pencere_button.place(height=15, x=1, y=1)

    def yaz(self, x):
        self.giris.insert(tk.END, str(x))

    def secim_degisti(self, event):
        secilen1 = self.secim_var1.get()
        secilen2 = self.secim_var2.get()
        print(f"Seçilen 1: {secilen1}")
        print(f"Seçilen 2: {secilen2}")

    def sil(self):
        self.giris.delete(len(self.giris.get()) - 1)

    def temizle(self):
        self.giris.delete(0, tk.END)
        self.sonuc_giris.delete(0, tk.END)

    def goto_screen1(self):
        self.master.withdraw()
        screen1 = Screen1(tk.Toplevel(self.master))

    def goto_screen2(self):
        self.master.withdraw()
        screen2 = Screen2(tk.Toplevel(self.master))
        
    def birim_donustur(self):
        try:
            deger = float(self.giris.get())
            birim1 = self.secim_var1.get()
            birim2 = self.secim_var2.get()
            # Önce birimi metreye çevir
            if birim1 == "Ton/m³":
             deger_metre = deger * 1000
            elif birim1 == "Hektolitre":
             deger_metre = deger * 100
            elif birim1 == "Dekalitre)":
             deger_metre = deger * 10
            elif birim1 == "Litre/dm³":
             deger_metre = deger
            elif birim1 == "Desigram":
             deger_metre = deger * 0.1
            elif birim1 == "Santilitre":
             deger_metre = deger * 0.01
            elif birim1 == "Mililitre":
             deger_metre = deger * 0.001

            else:
                sonuc = "Geçersiz birim"
                self.sonuc_giris.delete(0, 'end')
                self.sonuc_giris.insert(0, sonuc)
                return

            if birim2 == "Ton/m³":
             sonuc = deger_metre / 1000
            elif birim2 == "Hektolitre":
             sonuc = deger_metre / 100
            elif birim2 == "Dekalitre":
             sonuc = deger_metre / 10
            elif birim2 == "Litre/dm³":
             sonuc = deger_metre
            elif birim2 == "Desilitre":
             sonuc = deger_metre / 0.1
            elif birim2 == "Santilitre":
             sonuc = deger_metre / 0.01
            elif birim2 == "Mililitre":
             sonuc = deger_metre / 0.001

            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, str(sonuc))
        except ValueError:
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, "Geçersiz giriş")

        self.master.bind("<Return>", lambda event: self.birim_donustur())
        self.master.bind("<BackSpace>", lambda event: self.sil())
        self.master.bind("<KP_Enter>", lambda event: self.birim_donustur())
        self.master.bind("<Key>", lambda event: self.klavye_islemleri(event))

    def klavye_islemleri(self, event):
        if event.char in '0123456789':
            self.yaz(event.char)
        elif event.char == '\r':
            self.birim_donustur()
        elif event.char == '.':
            self.yaz('.')
        

    def goto_screen4(self):
        self.master.withdraw()
        screen4 = Screen4(tk.Toplevel(self.master))    
    

    def goto_screen5(self):
        self.master.withdraw()
        screen5 = Screen5(tk.Toplevel(self.master))

    def goto_screen6(self):
        self.master.withdraw()
        screen6 = Screen6(tk.Toplevel(self.master)) 
    
    def goto_screen7(self):
        self.master.withdraw()
        screen7 = Screen7(tk.Toplevel(self.master))

    def ikinci_pencere(self):
        ikinci_pencere = tk.Frame(self.master, bg="black", bd=2, relief="sunken")
        ikinci_pencere.place(x=1, y=1, width=100, height=240)
        label = tk.Label(ikinci_pencere, text="🟰", fg="purple", bg="black", font=("Roboto", 15))
        label.place(x=60, y=25, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="📏", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=60, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="⚖️", fg="gray", bg="black", font=("Roboto", 15))
        label.place(x=60, y=95, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💱", fg="lightgreen", bg="black", font=("Roboto", 15))
        label.place(x=60, y=130, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="₿", fg="orange", bg="black", font=("Roboto", 15))
        label.place(x=60, y=165, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="🕙", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=200, width=30, height=25) 

        destroy_button = tk.Button(ikinci_pencere, width=1, text="...", fg="black", font=("Helvetica", 7), background='white', command=ikinci_pencere.destroy)
        destroy_button.place(height=15, x=0, y=0)
        scr5_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Montserrat", 8), background='white', text="Calculator", command=self.goto_screen1)
        scr5_button.place(height=20, x=0, y=30)
        scr1_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Roboto", 11), background='white', text="Length", command=self.goto_screen2)
        scr1_button.place(height=20, x=0, y=65)
        scr2_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Futura", 11), background='white', text="Mass", command=self.goto_screen4)
        scr2_button.place(height=20, x=0, y=100)
        scr3_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Lato", 8), background='white', text="Exchange", command=self.goto_screen5)
        scr3_button.place(height=20, x=0, y=135)
        scr4_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Open Sans", 11), background='white', text="Cyrpto", command=self.goto_screen6)
        scr4_button.place(height=20, x=0, y=170)
        scr5_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Helvetica", 12), background='white', text="Time", command=self.goto_screen7)
        scr5_button.place(height=20, x=0, y=205)

class Screen4:
    def __init__(self, master):
        self.master = master
        self.master.title("Mass")
        self.master.geometry("293x460")
        self.master.configure(background='black')
        self.master.resizable(width=False, height=False)
        self.giris = tk.Entry(self.master, width=29,  justify=tk.RIGHT, font=('Helvetica', 16))
        self.giris.place(height=60, width=265, x=15, y=22)
        self.giris = tk.Entry(self.master, width=29,  justify=tk.RIGHT, font=('Helvetica', 16))
        self.giris.place(height=60, width=265, x=15, y=22)

        # Sonuç alanı
        self.sonuc_giris = ttk.Entry(self.master, width=29, justify=tk.RIGHT, font=("Helvetica", 16))
        self.sonuc_giris.place(height=60, width=265, x=15, y=90)

        # Seçim baloncuğu için bir StringVar oluştur
        self.secim_var1 = tk.StringVar()
        self.secim_var2 = tk.StringVar()

        # Seçenekler listesi
        secenekler = ["Miligram","Santigram","Desigram","Kilogram","Dekagram","Hektogram","Ton"]



        # 1. Combobox (Seçim baloncuğu) oluştur
        self.combobox1 = ttk.Combobox(self.master, textvariable=self.secim_var1, values=secenekler, state="readonly")
        self.combobox1.bind("<<ComboboxSelected>>", self.secim_degisti)
        self.combobox1.place(width=83, height=17, x=15, y=64)

        # 2. Combobox (Seçim baloncuğu) oluştur
        self.combobox2 = ttk.Combobox(self.master, textvariable=self.secim_var2, values=secenekler, state="readonly")
        self.combobox2.bind("<<ComboboxSelected>>", self.secim_degisti)
        self.combobox2.place(width=83, height=17, x=15, y=132)
       
      
        buttons = [
            {"text": "Dönüştür", "command": self.birim_donustur, "x": 145, "y": 400, "width": 10},
            {"text": "C", "command": self.temizle, "x": 105, "y": 160},
            {"text": "⌫", "command": self.sil, "x": 195, "y": 160},
            {"text": "1", "command": lambda: self.yaz(1), "x": 15, "y": 220},
            {"text": "2", "command": lambda: self.yaz(2), "x": 105, "y": 220},
            {"text": "3", "command": lambda: self.yaz(3), "x": 195, "y": 220},
            {"text": "4", "command": lambda: self.yaz(4), "x": 15, "y": 280},
            {"text": "5", "command": lambda: self.yaz(5), "x": 105, "y": 280},
            {"text": "6", "command": lambda: self.yaz(6), "x": 195, "y": 280},
            {"text": "7", "command": lambda: self.yaz(7), "x": 15, "y": 340},
            {"text": "8", "command": lambda: self.yaz(8), "x": 105, "y": 340},
            {"text": "9", "command": lambda: self.yaz(9), "x": 195, "y": 340},
            {"text": ".", "command": lambda: self.yaz("."), "x": 15, "y": 160},
            {"text": "0", "command": lambda: self.yaz(0), "x": 17, "y": 400, "width": 9}
        ]

        for button in buttons:
            ttk.Button(
                self.master, 
                text=button["text"], 
                command=button["command"], 
                width=button.get("width", 6)
            ).place(height=44, x=button["x"], y=button["y"])


        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))

        self.ikinci_pencere_button = tk.Button(master, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=self.ikinci_pencere)
        self.ikinci_pencere_button.place(height=15, x=1, y=1)

    def yaz(self, x):
        self.giris.insert(tk.END, str(x))

    def secim_degisti(self, event):
        secilen1 = self.secim_var1.get()
        secilen2 = self.secim_var2.get()
        print(f"Seçilen 1: {secilen1}")
        print(f"Seçilen 2: {secilen2}")

    def sil(self):
        self.giris.delete(len(self.giris.get()) - 1)

    def temizle(self):
        self.giris.delete(0, tk.END)
        self.sonuc_giris.delete(0, tk.END)

    def birim_donustur(self):
        try:
            deger = float(self.giris.get())
            birim1 = self.secim_var1.get()
            birim2 = self.secim_var2.get()
            # Önce birimi metreye çevir
            if birim1 == "Ton":
             deger_metre = deger * 1000
            elif birim1 == "Hektgram":
             deger_metre = deger * 100
            elif birim1 == "Dekagram":
             deger_metre = deger * 10
            elif birim1 == "Kilogram":
             deger_metre = deger
            elif birim1 == "Desigram":
             deger_metre = deger * 0.1
            elif birim1 == "Santigram":
             deger_metre = deger * 0.01
            elif birim1 == "Miligram":
             deger_metre = deger * 0.001
          # elif birim1 == "Mikrometre":
          #     deger_metre = deger * 1e-6
          # elif birim1 == "Nanometre":
          #     deger_metre = deger * 1e-9
          # elif birim1 == "Pikometre":
          #     deger_metre = deger * 1e-12
          # elif birim1 == "Femtometre":
          #     deger_metre = deger * 1e-15
          # elif birim1 == "Attometre":
          #     deger_metre = deger * 1e-18
          # elif birim1 == "Işık Yılı":
          #     deger_metre = deger * 9.461e+15  
            else:
               sonuc = "Geçersiz birim"
               self.sonuc_giris.delete(0, 'end')
               self.sonuc_giris.insert(0, sonuc)
               return
                    # Metreden hedef birime çevir
            if birim2 == "Ton":
             sonuc = deger_metre / 1000
            elif birim2 == "Hektogram":
             sonuc = deger_metre / 100
            elif birim2 == "Dekagram":
             sonuc = deger_metre / 10
            elif birim2 == "Kilogram":
             sonuc = deger_metre
            elif birim2 == "Desigram":
             sonuc = deger_metre / 0.1
            elif birim2 == "Santigram":
             sonuc = deger_metre / 0.01
            elif birim2 == "Miligram":
             sonuc = deger_metre / 0.001 

            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, str(sonuc))
        except ValueError:
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, "Geçersiz giriş")
      
     

    def goto_screen1(self):
        self.master.withdraw()
        screen1 = Screen1(tk.Toplevel(self.master))

    def goto_screen2(self):
        self.master.withdraw()
        screen2 = Screen2(tk.Toplevel(self.master))

    def goto_screen3(self):
        self.master.withdraw()
        screen3 = Screen3(tk.Toplevel(self.master))
    
    def goto_screen5(self):
        self.master.withdraw()
        screen5 = Screen5(tk.Toplevel(self.master))
        
    def goto_screen6(self):
        self.master.withdraw()
        screen6 = Screen6(tk.Toplevel(self.master))

    def goto_screen7(self):
        self.master.withdraw()
        screen7 = Screen7(tk.Toplevel(self.master))               

        self.master.bind("<Return>", lambda event: self.birim_donustur())
        self.master.bind("<BackSpace>", lambda event: self.sil())
        self.master.bind("<KP_Enter>", lambda event: self.birim_donustur())
        self.master.bind("<Key>", lambda event: self.klavye_islemleri(event))
    
    def klavye_islemleri(self, event):
        if event.char in '0123456789':
            self.yaz(event.char)
        elif event.char == '\r':
            self.birim_donustur()
        elif event.char == '.':
            self.yaz('.')

    def ikinci_pencere(self):
        ikinci_pencere = tk.Frame(self.master, bg="black", bd=2, relief="sunken")
        ikinci_pencere.place(x=1, y=1, width=100, height=240)
        label = tk.Label(ikinci_pencere, text="📏", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=60, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💧", fg="lightblue", bg="black", font=("Roboto", 15))
        label.place(x=60, y=95, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="🟰", fg="purple", bg="black", font=("Roboto", 15))
        label.place(x=60, y=25, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💱", fg="lightgreen", bg="black", font=("Roboto", 15))
        label.place(x=60, y=130, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="₿", fg="orange", bg="black", font=("Roboto", 15))
        label.place(x=60, y=165, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="🕙", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=200, width=30, height=25) 
 
        destroy_button = tk.Button(ikinci_pencere, width=1, text="...", fg="black", font=("Helvetica", 7), background='white', command=ikinci_pencere.destroy)
        destroy_button.place(height=15, x=0, y=0)
        scr5_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Montserrat", 8), background='white', text="Calculator", command=self.goto_screen1)
        scr5_button.place(height=20, x=0, y=30)
        scr1_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Roboto", 11), background='white', text="Length", command=self.goto_screen2)
        scr1_button.place(height=20, x=0, y=65)
        scr2_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Futura", 11), background='white', text="Liquid ", command=self.goto_screen3)
        scr2_button.place(height=20, x=0, y=100)
        scr3_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Lato", 8), background='white', text="Exchange", command=self.goto_screen5)
        scr3_button.place(height=20, x=0, y=135)
        scr4_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Open Sans", 11), background='white', text="Cyrpto", command=self.goto_screen6)
        scr4_button.place(height=20, x=0, y=170)
        scr5_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Helvetica", 12), background='white', text="Time", command=self.goto_screen7)
        scr5_button.place(height=20, x=0, y=205)
                 
        
class Screen5:

    def __init__(self, master):
        self.master = master
        self.yeni_islem = True
        self.hesap = []
        self.s1 = []

        # API anahtarınızı buraya ekleyin
        self.API_KEY = '4eecc3612e92a51ef6045107'
        self.BASE_URL = f'https://v6.exchangerate-api.com/v6/{self.API_KEY}/latest'

        self.setup_ui()

    def get_exchange_rate(self, from_currency, to_currency):
        url = f'{self.BASE_URL}/{from_currency}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # HTTPError için kontrol
            data = response.json()
            if data['result'] == 'success':
                return data['conversion_rates'][to_currency]
            else:
                print("API Hatası:", data['error-type'])
                return None
        except requests.exceptions.RequestException as e:
            print(f"HTTP Hatası: {e}")
            return None
        except ValueError:
            print("JSON Decode Hatası")
            return None

    def birim_donustur(self):
        from_currency = self.secim_var1.get()
        to_currency = self.secim_var2.get()
        try:
            amount = float(self.giris.get())
        except ValueError:
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, 'Geçersiz Miktar')
            return

        rate = self.get_exchange_rate(from_currency, to_currency)
        if rate is not None:
            converted_amount = amount * rate
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, str(converted_amount))
        else:
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, 'Hata!')

    def yenile(self):
        from_currency = self.secim_var1.get()
        to_currency = self.secim_var2.get()
        if from_currency and to_currency:
            rate = self.get_exchange_rate(from_currency, to_currency)
            if rate is not None:
                try:
                    amount = float(self.giris.get())
                    converted_amount = amount * rate
                    self.sonuc_giris.delete(0, 'end')
                    self.sonuc_giris.insert(0, str(converted_amount))
                except ValueError:
                    self.sonuc_giris.delete(0, 'end')
                    self.sonuc_giris.insert(0, 'Geçersiz Miktar')
            else:
                self.sonuc_giris.delete(0, 'end')
                self.sonuc_giris.insert(0, 'Hata!')

    def yaz(self, x):
        if self.yeni_islem:
            self.giris.delete(0, 'end')
            self.yeni_islem = False
        s = len(self.giris.get())
        self.giris.insert(s, str(x))

    def sil(self):
        self.giris.delete(len(self.giris.get()) - 1)

    def temizle(self):
        self.hesap = []
        self.s1 = []
        self.yeni_islem = True
        self.giris.delete(0, 'end')
        self.sonuc_giris.delete(0, 'end')
    def setup_ui(self):
        self.master.title('Exchange')
        self.master.geometry("293x460")
        self.master.configure(background='black')
        self.master.resizable(width=False, height=False)

        self.giris = ttk.Entry(self.master, width=29, justify=tk.RIGHT, font=("Helvetica", 16))
        self.giris.place(height=60, width=265, x=15, y=22)

        self.sonuc_giris = ttk.Entry(self.master, width=29, justify=tk.RIGHT, font=("Helvetica", 16))
        self.sonuc_giris.place(height=60, width=265, x=15, y=90)

        self.secim_var1 = tk.StringVar()
        self.secim_var2 = tk.StringVar()

        secenekler = ["USD", "TRY", "EUR", "GBP", "JPY", "CNY", "RUB", "NZD", "CHF", "CAD", "HKD"]

        combobox1 = ttk.Combobox(self.master, textvariable=self.secim_var1, values=secenekler, state="readonly")
        combobox1.bind("<<ComboboxSelected>>", self.secim_degisti)
        combobox1.place(width=60, height=17, x=15, y=64)

        combobox2 = ttk.Combobox(self.master, textvariable=self.secim_var2, values=secenekler, state="readonly")
        combobox2.bind("<<ComboboxSelected>>", self.secim_degisti)
        combobox2.place(width=60, height=17, x=15, y=132)

        self.master.bind("<Tab>", lambda event: "break")
        self.giris.bind("<FocusIn>", lambda event: "break")
        self.giris.bind("<Button-1>", lambda event: "break")
        self.sonuc_giris.bind("<FocusIn>", lambda event: "break")
        self.sonuc_giris.bind("<Button-1>", lambda event: "break")
        combobox1.bind("<FocusIn>", lambda event: "break")
        combobox2.bind("<FocusIn>", lambda event: "break")

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))

        buttons = [
            {"text": "Dönüştür", "command": self.birim_donustur, "x": 145, "y": 400, "width": 10},
            {"text": "C", "command": self.temizle, "x": 105, "y": 160},
            {"text": "⌫", "command": self.sil, "x": 195, "y": 160},
            {"text": "1", "command": lambda: self.yaz(1), "x": 15, "y": 220},
            {"text": "2", "command": lambda: self.yaz(2), "x": 105, "y": 220},
            {"text": "3", "command": lambda: self.yaz(3), "x": 195, "y": 220},
            {"text": "4", "command": lambda: self.yaz(4), "x": 15, "y": 280},
            {"text": "5", "command": lambda: self.yaz(5), "x": 105, "y": 280},
            {"text": "6", "command": lambda: self.yaz(6), "x": 195, "y": 280},
            {"text": "7", "command": lambda: self.yaz(7), "x": 15, "y": 340},
            {"text": "8", "command": lambda: self.yaz(8), "x": 105, "y": 340},
            {"text": "9", "command": lambda: self.yaz(9), "x": 195, "y": 340},
            {"text": ".", "command": lambda: self.yaz("."), "x": 15, "y": 160},
            {"text": "0", "command": lambda: self.yaz(0), "x": 17, "y": 400, "width": 9}
        ]

        for button in buttons:
            ttk.Button(
                self.master,
                text=button["text"],
                command=button["command"],
                width=button.get("width", 6)
            ).place(height=44, x=button["x"], y=button["y"])

        tk.Button(self.master, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=self.ikinci_pencere).place(height=15, x=1, y=1)
        tk.Button(self.master, text="↻", background='white', font=("Times", 15), width=2, command=self.yenile).place(height=23, x=130, y=1)

        self.master.bind("<Return>", lambda event: self.birim_donustur())
        self.master.bind("<BackSpace>", lambda event: self.sil())
        self.master.bind("<KP_Enter>", lambda event: self.birim_donustur())
        self.master.bind("<Key>", lambda event: self.klavye_islemleri(event))

    def klavye_islemleri(self, event):
        if event.char in '0123456789':
            self.yaz(event.char)
        elif event.char == '\r':
            self.birim_donustur()
        elif event.char == '.':
            self.yaz('.')    

    def secim_degisti(self, event):
        secilen1 = self.secim_var1.get()
        secilen2 = self.secim_var2.get()
        print(f"Seçilen 1: {secilen1}")
        print(f"Seçilen 2: {secilen2}")

    def goto_screen1(self):
        self.master.withdraw()
        screen1 = Screen1(tk.Toplevel(self.master))

    def goto_screen2(self):
        self.master.withdraw()
        screen2 = Screen2(tk.Toplevel(self.master))

    def goto_screen3(self):
        self.master.withdraw()
        screen3 = Screen3(tk.Toplevel(self.master))

    def goto_screen4(self):
        self.master.withdraw()
        screen4 = Screen4(tk.Toplevel(self.master))

    def goto_screen6(self):
        self.master.withdraw()
        screen6 = Screen6(tk.Toplevel(self.master))

    def goto_screen7(self):
        self.master.withdraw()
        screen7 = Screen7(tk.Toplevel(self.master))                

    def ikinci_pencere(self):
        ikinci_pencere = tk.Frame(self.master, bg="black", bd=2, relief="sunken")
        ikinci_pencere.place(x=1, y=1, width=100, height=240)
        label = tk.Label(ikinci_pencere, text="📏", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=60, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💧", fg="lightblue", bg="black", font=("Roboto", 15))
        label.place(x=60, y=95, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="⚖️", fg="gray", bg="black", font=("Roboto", 15))
        label.place(x=60, y=130, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="🟰", fg="purple", bg="black", font=("Roboto", 15))
        label.place(x=60, y=25, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="₿", fg="orange", bg="black", font=("Roboto", 15))
        label.place(x=60, y=165, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="🕙", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=200, width=30, height=25)


        destroy_button = tk.Button(ikinci_pencere, width=1, text="...", fg="black", font=("Helvetica", 7), background='white', command=ikinci_pencere.destroy)
        destroy_button.place(height=15, x=0, y=0)
        scr5_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Montserrat", 8), background='white', text="Calculator", command=self.goto_screen1)
        scr5_button.place(height=20, x=0, y=30)
        scr1_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Roboto", 11), background='white', text="Length", command=self.goto_screen2)
        scr1_button.place(height=20, x=0, y=65)
        scr2_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Futura", 11), background='white', text="Liquid ", command=self.goto_screen3)
        scr2_button.place(height=20, x=0, y=100)
        scr3_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Lato", 11), background='white', text="Mass", command=self.goto_screen4)
        scr3_button.place(height=20, x=0, y=135)
        scr4_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Open Sans", 11), background='white', text="Cyrpto", command=self.goto_screen6)
        scr4_button.place(height=20, x=0, y=170)
        scr5_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Helvetica", 12), background='white', text="Time", command=self.goto_screen7)
        scr5_button.place(height=20, x=0, y=205)
                 
class Screen6:

    def __init__(self, master):
        self.master = master
        self.yeni_islem = True
        self.hesap = []
        self.s1 = []
        self.API_KEY = 'kqVBg2uJYb6HHm3vgSinGLRBHgj7EYp3niRIOWXaOYLGk2q6BRIGC5pfMQT2js6M'
        self.BASE_URL = 'https://api.binance.com/api/v3/ticker/price?symbol='

        self.setup_ui()

    def get_binance_price(self, symbol):
        url = f"{self.BASE_URL}{symbol}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return float(data['price'])
        except requests.exceptions.RequestException as e:
            print(f"HTTP Hatası: {e}")
            return None
        except ValueError:
            print("JSON Decode Hatası")
            return None

    def birim_donustur(self):
        from_currency = self.secim_var1.get()
        to_currency = self.secim_var2.get()
        symbol = from_currency + to_currency
        try:
            amount = float(self.giris.get())
        except ValueError:
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, 'Geçersiz Miktar')
            return

        rate = self.get_binance_price(symbol)
        if rate is not None:
            converted_amount = amount * rate
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, str(converted_amount))
        else:
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, 'Hata!')

    def yenile(self):
        from_currency = self.secim_var1.get()
        to_currency = self.secim_var2.get()
        symbol = from_currency + to_currency
        if from_currency and to_currency:
            rate = self.get_binance_price(symbol)
            if rate is not None:
                try:
                    amount = float(self.giris.get())
                    converted_amount = amount * rate
                    self.sonuc_giris.delete(0, 'end')
                    self.sonuc_giris.insert(0, str(converted_amount))
                except ValueError:
                    self.sonuc_giris.delete(0, 'end')
                    self.sonuc_giris.insert(0, 'Geçersiz Miktar')
            else:
                self.sonuc_giris.delete(0, 'end')
                self.sonuc_giris.insert(0, 'Hata!')

    def yaz(self, x):
        if self.yeni_islem:
            self.giris.delete(0, 'end')
            self.yeni_islem = False
        s = len(self.giris.get())
        self.giris.insert(s, str(x))

    def sil(self):
        self.giris.delete(len(self.giris.get()) - 1)

    def temizle(self):
        self.hesap = []
        self.s1 = []
        self.yeni_islem = True
        self.giris.delete(0, 'end')
        self.sonuc_giris.delete(0, 'end')

    def secim_degisti(self, event):
        secilen1 = self.secim_var1.get()
        secilen2 = self.secim_var2.get()
        print(f"Seçilen 1: {secilen1}")
        print(f"Seçilen 2: {secilen2}")
    def klavye_islemleri(self, event):
        if event.char in '0123456789':
            self.yaz(event.char)
        elif event.char == '\r':
            self.birim_donustur()
        elif event.char == '.':
            self.yaz('.')

    def setup_ui(self):
        self.master.title('Cyrpto')
        self.master.geometry("293x460")
        self.master.configure(background='black')
        self.master.resizable(width=False, height=False)

        self.giris = ttk.Entry(self.master, width=29, justify=tk.RIGHT, font=("Helvetica", 16))
        self.giris.place(height=60, width=265, x=15, y=22)

        self.sonuc_giris = ttk.Entry(self.master, width=29, justify=tk.RIGHT, font=("Helvetica", 16))
        self.sonuc_giris.place(height=60, width=265, x=15, y=90)

        self.secim_var1 = tk.StringVar()
        self.secim_var2 = tk.StringVar()

        secenekler1 = ["BTC", "ETH", "BNB", "XRP", "LTC", "SOL", "DOGE", "AVAX", "TRX", "DOT", "WBTC", "MATIC"]
        secenekler2 = ["USDT", "EUR", "TRY", "FDUSD", "USDC"]

        combobox1 = ttk.Combobox(self.master, textvariable=self.secim_var1, values=secenekler1, state="readonly")
        combobox1.bind("<<ComboboxSelected>>", self.secim_degisti)
        combobox1.place(width=60, height=17, x=15, y=64)

        combobox2 = ttk.Combobox(self.master, textvariable=self.secim_var2, values=secenekler2, state="readonly")
        combobox2.bind("<<ComboboxSelected>>", self.secim_degisti)
        combobox2.place(width=60, height=17, x=15, y=132)

        self.master.bind("<Tab>", lambda event: "break")
        self.giris.bind("<FocusIn>", lambda event: "break")
        self.giris.bind("<Button-1>", lambda event: "break")
        self.sonuc_giris.bind("<FocusIn>", lambda event: "break")
        self.sonuc_giris.bind("<Button-1>", lambda event: "break")
        combobox1.bind("<FocusIn>", lambda event: "break")
        combobox2.bind("<FocusIn>", lambda event: "break")

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))

        buttons = [
            {"text": "Dönüştür", "command": self.birim_donustur, "x": 145, "y": 400, "width": 10},
            {"text": "C", "command": self.temizle, "x": 105, "y": 160},
            {"text": "⌫", "command": self.sil, "x": 195, "y": 160},
            {"text": "1", "command": lambda: self.yaz(1), "x": 15, "y": 220},
            {"text": "2", "command": lambda: self.yaz(2), "x": 105, "y": 220},
            {"text": "3", "command": lambda: self.yaz(3), "x": 195, "y": 220},
            {"text": "4", "command": lambda: self.yaz(4), "x": 15, "y": 280},
            {"text": "5", "command": lambda: self.yaz(5), "x": 105, "y": 280},
            {"text": "6", "command": lambda: self.yaz(6), "x": 195, "y": 280},
            {"text": "7", "command": lambda: self.yaz(7), "x": 15, "y": 340},
            {"text": "8", "command": lambda: self.yaz(8), "x": 105, "y": 340},
            {"text": "9", "command": lambda: self.yaz(9), "x": 195, "y": 340},
            {"text": ".", "command": lambda: self.yaz("."), "x": 15, "y": 160},
            {"text": "0", "command": lambda: self.yaz(0), "x": 17, "y": 400, "width": 9}
        ]

        for button in buttons:
            ttk.Button(
                self.master,
                text=button["text"],
                command=button["command"],
                width=button.get("width", 6)
            ).place(height=44, x=button["x"], y=button["y"])

        tk.Button(self.master, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=self.ikinci_pencere).place(height=15, x=1, y=1)
        tk.Button(self.master, text="↻", background='white', font=("Times", 15), width=2, command=self.yenile).place(height=23, x=130, y=1)

        self.master.bind("<Return>", lambda event: self.birim_donustur())
        self.master.bind("<BackSpace>", lambda event: self.sil())
        self.master.bind("<KP_Enter>", lambda event: self.birim_donustur())
        self.master.bind("<Key>", lambda event: self.klavye_islemleri(event))

    def goto_screen1(self):
        self.master.withdraw()
        screen1 = Screen1(tk.Toplevel(self.master))

    def goto_screen2(self):
        self.master.withdraw()
        screen2 = Screen2(tk.Toplevel(self.master))

    def goto_screen3(self):
        self.master.withdraw()
        screen3 = Screen3(tk.Toplevel(self.master))

    def goto_screen4(self):
        self.master.withdraw()
        screen4 = Screen4(tk.Toplevel(self.master))

    def goto_screen5(self):
        self.master.withdraw()
        screen5 = Screen5(tk.Toplevel(self.master))

    def goto_screen7(self):
        self.master.withdraw()
        screen7 = Screen7(tk.Toplevel(self.master))           

    def ikinci_pencere(self):
        ikinci_pencere = tk.Frame(self.master, bg="black", bd=2, relief="sunken")
        ikinci_pencere.place(x=1, y=1, width=100, height=240)
        label = tk.Label(ikinci_pencere, text="📏", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=60, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💧", fg="lightblue", bg="black", font=("Roboto", 15))
        label.place(x=60, y=95, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="⚖️", fg="gray", bg="black", font=("Roboto", 15))
        label.place(x=60, y=130, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💱", fg="lightgreen", bg="black", font=("Roboto", 15))
        label.place(x=60, y=165, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="🟰", fg="purple", bg="black", font=("Roboto", 15))
        label.place(x=60, y=25, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="🕙", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=200, width=30, height=25)

        destroy_button = tk.Button(ikinci_pencere, width=1, text="...", fg="black", font=("Helvetica", 7), background='white', command=ikinci_pencere.destroy)
        destroy_button.place(height=15, x=0, y=0)
        scr5_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Montserrat", 8), background='white', text="Calculator", command=self.goto_screen1)
        scr5_button.place(height=20, x=0, y=30)
        scr1_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Roboto", 11), background='white', text="Length", command=self.goto_screen2)
        scr1_button.place(height=20, x=0, y=65)
        scr2_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Futura", 11), background='white', text="Liquid ", command=self.goto_screen3)
        scr2_button.place(height=20, x=0, y=100)
        scr3_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Lato", 11), background='white', text="Mass", command=self.goto_screen4)
        scr3_button.place(height=20, x=0, y=135)
        scr4_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Open Sans", 8), background='white', text="Exchange", command=self.goto_screen5)
        scr4_button.place(height=20, x=0, y=170)
        scr5_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Helvetica", 12), background='white', text="Time", command=self.goto_screen7)
        scr5_button.place(height=20, x=0, y=205)
          

class Screen7:
    def __init__(self, master):
        self.master = master
        self.master.title("Lenght")
        self.master.geometry("293x460")
        self.master.configure(background='black')
        self.master.resizable(width=False, height=False)

        self.giris = tk.Entry(self.master, width=29,  justify=tk.RIGHT, font=('Helvetica', 16))
        self.giris.place(height=60, width=265, x=15, y=22)

        # Sonuç alanı
        self.sonuc_giris = ttk.Entry(self.master, width=29, justify=tk.RIGHT, font=("Helvetica", 16))
        self.sonuc_giris.place(height=60, width=265, x=15, y=90)

        # Seçim baloncuğu için bir StringVar oluştur
        self.secim_var1 = tk.StringVar()
        self.secim_var2 = tk.StringVar()

        # Seçenekler listesi
        secenekler = ["Salise", "Saniye", "Dakika", "Saat", "Gün", "Hafta", "Ay", "Yıl", "Yüzyıl"]


        # 1. Combobox (Seçim baloncuğu) oluştur
        self.combobox1 = ttk.Combobox(self.master, textvariable=self.secim_var1, values=secenekler, state="readonly")
        self.combobox1.bind("<<ComboboxSelected>>", self.secim_degisti)
        self.combobox1.place(width=83, height=17, x=15, y=64)

        # 2. Combobox (Seçim baloncuğu) oluştur
        self.combobox2 = ttk.Combobox(self.master, textvariable=self.secim_var2, values=secenekler, state="readonly")
        self.combobox2.bind("<<ComboboxSelected>>", self.secim_degisti)
        self.combobox2.place(width=83, height=17, x=15, y=132)
       
        
        buttons = [
            {"text": "Dönüştür", "command": self.birim_donustur, "x": 145, "y": 400, "width": 10},
            {"text": "C", "command": self.temizle, "x": 105, "y": 160},
            {"text": "⌫", "command": self.sil, "x": 195, "y": 160},
            {"text": "1", "command": lambda: self.yaz(1), "x": 15, "y": 220},
            {"text": "2", "command": lambda: self.yaz(2), "x": 105, "y": 220},
            {"text": "3", "command": lambda: self.yaz(3), "x": 195, "y": 220},
            {"text": "4", "command": lambda: self.yaz(4), "x": 15, "y": 280},
            {"text": "5", "command": lambda: self.yaz(5), "x": 105, "y": 280},
            {"text": "6", "command": lambda: self.yaz(6), "x": 195, "y": 280},
            {"text": "7", "command": lambda: self.yaz(7), "x": 15, "y": 340},
            {"text": "8", "command": lambda: self.yaz(8), "x": 105, "y": 340},
            {"text": "9", "command": lambda: self.yaz(9), "x": 195, "y": 340},
            {"text": ".", "command": lambda: self.yaz("."), "x": 15, "y": 160},
            {"text": "0", "command": lambda: self.yaz(0), "x": 17, "y": 400, "width": 9}
        ]

        for button in buttons:
            ttk.Button(
                self.master, 
                text=button["text"], 
                command=button["command"], 
                width=button.get("width", 6)
            ).place(height=44, x=button["x"], y=button["y"])


        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))

        self.ikinci_pencere_button = tk.Button(master, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=self.ikinci_pencere)
        self.ikinci_pencere_button.place(height=15, x=1, y=1)

    def yaz(self, x):
        self.giris.insert(tk.END, str(x))

    def secim_degisti(self, event):
        secilen1 = self.secim_var1.get()
        secilen2 = self.secim_var2.get()
        print(f"Seçilen 1: {secilen1}")
        print(f"Seçilen 2: {secilen2}")

    def sil(self):
        self.giris.delete(len(self.giris.get()) - 1)

    def temizle(self):
        self.giris.delete(0, tk.END)
        self.sonuc_giris.delete(0, tk.END)

    def goto_screen1(self):
        self.master.withdraw()
        screen1 = Screen1(tk.Toplevel(self.master))

    def goto_screen3(self):
        self.master.withdraw()
        screen3 = Screen3(tk.Toplevel(self.master))

    
    def goto_screen5(self):
        self.master.withdraw()
        screen5 = Screen5(tk.Toplevel(self.master))

    def goto_screen6(self):
        self.master.withdraw()
        screen6 = Screen6(tk.Toplevel(self.master))        

    def birim_donustur(self):
        try:
            deger = float(self.giris.get())
            birim1 = self.secim_var1.get()
            birim2 = self.secim_var2.get()
            # Önce birimi metreye çevir
            if birim1 == "Salise":
                deger_saniye = deger * 1e-3
            elif birim1 == "Saniye":
                deger_saniye = deger
            elif birim1 == "Dakika":
                deger_saniye = deger * 60
            elif birim1 == "Saat":
                deger_saniye = deger * 3600
            elif birim1 == "Gün":
                deger_saniye = deger * 86400
            elif birim1 == "Hafta":
                deger_saniye = deger * 604800
            elif birim1 == "Ay":
                deger_saniye = deger * 2.628e+6  # Ortalama 30.44 gün
            elif birim1 == "Yıl":
                deger_saniye = deger * 3.154e+7  # Ortalama yıl uzunluğu
            elif birim1 == "Yüzyıl":
                deger_saniye = deger * 3.154e+9  # Ortalama 100 yıl
            else:
                sonuc = "Geçersiz birim"
                self.sonuc_giris.delete(0, 'end')
                self.sonuc_giris.insert(0, sonuc)
                return

            # Saniyeden hedef birime çevir
            if birim2 == "Salise":
                sonuc = deger_saniye / 1e-3
            elif birim2 == "Saniye":
                sonuc = deger_saniye
            elif birim2 == "Dakika":
                sonuc = deger_saniye / 60
            elif birim2 == "Saat":
                sonuc = deger_saniye / 3600
            elif birim2 == "Gün":
                sonuc = deger_saniye / 86400
            elif birim2 == "Hafta":
                sonuc = deger_saniye / 604800
            elif birim2 == "Ay":
                sonuc = deger_saniye / 2.628e+6  # Ortalama 30.44 gün
            elif birim2 == "Yıl":
                sonuc = deger_saniye / 3.154e+7  # Ortalama yıl uzunluğu
            elif birim2 == "Yüzyıl":
                sonuc = deger_saniye / 3.154e+9  # Ortalama 100 yıl
            else:
                sonuc = "Geçersiz birim"

            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, str(sonuc))
        except ValueError:
            self.sonuc_giris.delete(0, 'end')
            self.sonuc_giris.insert(0, "Geçersiz giriş")

        self.master.bind("<Return>", lambda event: self.birim_donustur())
        self.master.bind("<BackSpace>", lambda event: self.sil())
        self.master.bind("<KP_Enter>", lambda event: self.birim_donustur())
        self.master.bind("<Key>", lambda event: self.klavye_islemleri(event))

    def klavye_islemleri(self, event):
        if event.char in '0123456789':
            self.yaz(event.char)
        elif event.char == '\r':
            self.birim_donustur()
        elif event.char == '.':
            self.yaz('.')


    def goto_screen4(self):
        self.master.withdraw()
        screen4 = Screen4(tk.Toplevel(self.master))    
    
    def goto_screen2(self):
        self.master.withdraw()
        screen2 = Screen2(tk.Toplevel(self.master))  
 
    def ikinci_pencere(self):
        ikinci_pencere = tk.Frame(self.master, bg="black", bd=2, relief="sunken")
        ikinci_pencere.place(x=1, y=1, width=100, height=250)
        label = tk.Label(ikinci_pencere, text="🟰", fg="purple", bg="black", font=("Roboto", 15))
        label.place(x=60, y=25, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="📏", fg="white", bg="black", font=("Roboto", 15))
        label.place(x=60, y=60, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💧", fg="lightblue", bg="black", font=("Roboto", 15))
        label.place(x=60, y=95, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="⚖️", fg="gray", bg="black", font=("Roboto", 15))
        label.place(x=60, y=130, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="💱", fg="lightgreen", bg="black", font=("Roboto", 15))
        label.place(x=60, y=165, width=30, height=25)
        label = tk.Label(ikinci_pencere, text="₿", fg="orange", bg="black", font=("Roboto", 15))
        label.place(x=60, y=203, width=30, height=25)
        

        destroy_button = tk.Button(ikinci_pencere, width=1, text="...", fg="black", font=("Helvetica", 9), background='white', command=ikinci_pencere.destroy)
        destroy_button.place(height=15, x=0, y=0)
        scr1_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Roboto", 8), background='white', text="Calculator", command=self.goto_screen1)
        scr1_button.place(height=18, x=1, y=30)
        scr2_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Futura", 11), background='white', text="Liquid ", command=self.goto_screen3)
        scr2_button.place(height=18, x=1, y=100)
        scr3_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Lato", 11), background='white', text="Mass", command=self.goto_screen4)
        scr3_button.place(height=18, x=1, y=135)
        scr4_button = tk.Button(ikinci_pencere, width=8, fg="black", font=("Open Sans", 8), background='white', text="Exchange", command=self.goto_screen5)
        scr4_button.place(height=18, x=1, y=170)  
        scr5_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Montserrat", 11), background='white', text="Cyrpto", command=self.goto_screen6)
        scr5_button.place(height=18, x=1, y=205)
        scr1_button = tk.Button(ikinci_pencere, width=5, fg="black", font=("Roboto", 11), background='white', text="Length", command=self.goto_screen2)
        scr1_button.place(height=20, x=0, y=65)         
        
class Screen8:
    def __init__(self, master):
        self.master = master
        self.master.title("Tarih Hesaplayıcı")
        self.master.geometry("293x460")
        self.master.configure(background='black')
        self.master.resizable(width=False, height=False)

        self.create_widgets()

    def create_widgets(self):
        # Başlangıç tarihi girişi
        self.start_date_label = tk.Label(self.master, text="Başlangıç Tarihi:", bg='black', fg='white')
        self.start_date_label.place(x=15, y=20)
        self.start_date_entry = tk.Entry(self.master, width=20)
        self.start_date_entry.place(x=15, y=40)
        self.start_date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))

        # Gün sayısı girişi
        self.days_label = tk.Label(self.master, text="Gün Sayısı:", bg='black', fg='white')
        self.days_label.place(x=15, y=70)
        self.days_entry = tk.Entry(self.master, width=20)
        self.days_entry.place(x=15, y=90)

        # Sonuç alanı
        self.result_label = tk.Label(self.master, text="Sonuç:", bg='black', fg='white')
        self.result_label.place(x=15, y=120)
        self.result_entry = tk.Entry(self.master, width=29, justify=tk.RIGHT, font=("Helvetica", 12))
        self.result_entry.place(x=15, y=140, height=40, width=265)

        # İşlem düğmeleri
        ttk.Button(self.master, text="İleri", command=self.add_days).place(x=15, y=190, width=80)
        ttk.Button(self.master, text="Geri", command=self.subtract_days).place(x=105, y=190, width=80)
        ttk.Button(self.master, text="Fark Hesapla", command=self.calculate_difference).place(x=195, y=190, width=80)

        # Sayı tuşları
        buttons = [
            {"text": "7", "x": 15, "y": 230},
            {"text": "8", "x": 105, "y": 230},
            {"text": "9", "x": 195, "y": 230},
            {"text": "4", "x": 15, "y": 280},
            {"text": "5", "x": 105, "y": 280},
            {"text": "6", "x": 195, "y": 280},
            {"text": "1", "x": 15, "y": 330},
            {"text": "2", "x": 105, "y": 330},
            {"text": "3", "x": 195, "y": 330},
            {"text": "0", "x": 15, "y": 380},
            {"text": ".", "x": 105, "y": 380},
            {"text": "C", "x": 195, "y": 380}
        ]

        for button in buttons:
            ttk.Button(
                self.master, 
                text=button["text"], 
                command=lambda x=button["text"]: self.button_click(x),
                width=6
            ).place(height=44, x=button["x"], y=button["y"])

    def button_click(self, value):
        if value == 'C':
            self.days_entry.delete(0, tk.END)
        else:
            self.days_entry.insert(tk.END, value)

    def add_days(self):
        try:
            start_date = datetime.strptime(self.start_date_entry.get(), "%d.%m.%Y")
            days = int(self.days_entry.get())
            result_date = start_date + timedelta(days=days)
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, result_date.strftime("%d.%m.%Y"))
        except ValueError:
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, "Hatalı giriş")

    def subtract_days(self):
        try:
            start_date = datetime.strptime(self.start_date_entry.get(), "%d.%m.%Y")
            days = int(self.days_entry.get())
            result_date = start_date - timedelta(days=days)
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, result_date.strftime("%d.%m.%Y"))
        except ValueError:
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, "Hatalı giriş")

    def calculate_difference(self):
        try:
            start_date = datetime.strptime(self.start_date_entry.get(), "%d.%m.%Y")
            end_date = datetime.strptime(self.days_entry.get(), "%d.%m.%Y")
            difference = abs((end_date - start_date).days)
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, f"{difference} gün")
        except ValueError:
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, "Hatalı giriş")


root = tk.Tk()
screen1 = Screen1(root)

root.mainloop()





