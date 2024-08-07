import tkinter as tk
from tkinter import *
from tkinter import ttk
# Küresel değişkenler
hesap = []
s1 = []
yeni_islem = True
yuzde = False
gecmis = []
def yaz(x):
    global yeni_islem
    if yeni_islem:
        giris.delete(0, 'end')
        yeni_islem = False
    s = len(giris.get())
    giris.insert(s, str(x))

def islemler(x):
    global hesap
    global s1
    global yuzde
    global yeni_islem

    if yeni_islem and x not in "+-*/%":
        giris.delete(0, 'end')
        yeni_islem = False

    if x in "+-*/":
        try:
            s1.append(float(giris.get()))
        except ValueError:
            giris.delete(0, 'end')
            giris.insert(0, "Hata")
            return
        hesap.append(x)
        giris.delete(0, 'end')
    elif x == "%":
        yuzde = True
        try:
            s1.append(float(giris.get()))
        except ValueError:
            giris.delete(0, 'end')
            giris.insert(0, "Hata")
            return
        giris.delete(0, 'end')
    else:
        giris.insert(END, x)

def hesapla():
    global s1
    global hesap
    global yuzde
    global yeni_islem
    global gecmis
    try:
        if yuzde:
            yuzde_degeri = float(giris.get())
            s1[-1] = (yuzde_degeri / 100) * s1[-1]
            yuzde = False
        else:
            s1.append(float(giris.get()))

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
                    giris.delete(0, 'end')
                    giris.insert(0, "Hata: Sıfıra bölme")
                    hesap = []
                    s1 = []
                    yeni_islem = True
                    return
            elif hesap[i-1] == '*':
                sonuc *= s1[i]

        sonuc_str = str(sonuc)
        if sonuc % 1 == 0:
            sonuc_str = str(int(sonuc))
        # İşlem geçmişine ekleme

        islem_str = ' '.join(f"{s1[i]} {hesap[i]}" for i in range(len(hesap))) + f" {s1[-1]} = {sonuc_str}"

        gecmis.append(islem_str)
        giris.delete(0, 'end')
        giris.insert(0, sonuc_str)
        hesap = []
        s1 = []
        yeni_islem = True  # Yeni işlem başladığını belirt
    except ValueError:
        giris.delete(0, 'end')
        giris.insert(0, "Hata")
        hesap = []
        s1 = []
        yeni_islem = True  # Yeni işlem başladığını belirt

def sil():
    giris.delete(len(giris.get()) - 1)

def temizle():
    global hesap
    global s1
    global yeni_islem
    giris.delete(0, 'end')
    hesap = []
    s1 = []
    yeni_islem = True

window = Tk()
window.title('Hesap Makinası')
window.geometry("300x400")
window.configure(background='black')
window.resizable(width=False, height=False)


def ikinci_pencere():
    ikinci_pencere= tk.Frame(window, bg="black" ,bd=2,relief="ridge")
    ikinci_pencere.place(x=1, y=1,width=80, height=100)
    Label=tk.Label(ikinci_pencere, text="Pia",fg="red",bg="black",font=("Times", 24))
    Label.place(x=15, y=35,width=40, height=30)
    Button(ikinci_pencere, width=1, text="...", fg="black", font=("Helvetica", 9),  background='white',command=ikinci_pencere.destroy).place(height=15,x=1, y=1)

def gecmisi_goster():
    global gecmis
    gecmisi_goster =tk.Frame(window,bg="black")
    gecmisi_goster.place(x=180, y=0,width=140, height=200)
    

    listbox = tk.Listbox(gecmisi_goster,width=18 ,fg="white",bd=0,bg="black",background="black",relief="flat",highlightbackground="black",highlightcolor="black")
    listbox.pack(expand=True, fill='both')
    listbox.place(x=3, y=25)
    
    for item in gecmis:
        listbox.insert(END, item)

    def kopyala():
        secilen = listbox.get(listbox.curselection())
        giris.delete(0, 'end')
        giris.insert(0, secilen.split(' = ')[0])
        gecmisi_goster.destroy()

    Button(gecmisi_goster, width=8, text="Kopyala", fg="white", font=("Helvetica", 13),  background='black',highlightbackground="black",highlightcolor="black",highlightthickness=0,relief="flat",command=kopyala).place(height=18,x=20, y=170)
   
    
    Button(gecmisi_goster, width=1, text="⟳", fg="white", font=('FontAwesome', 9),  background='black',highlightbackground="black",highlightcolor="black",highlightthickness=2,relief="flat",command=gecmisi_goster.destroy).place(height=15,x=92, y=2)
    


giris = tk.Entry(window, width=29, bd=4, justify=RIGHT, font=('Times', 19))
giris.place(height=60, width=275, x=13, y=20)


# Odağı ve tıklamayı engelleme
window.bind("<Tab>", lambda event: "break")
giris.bind("<FocusIn>", lambda event: "break")
giris.bind("<Button-1>", lambda event: "break")

def secim_degisti(event):
    secilen = secim_var.get()
    print(f"Seçilen: {secilen}")

secim_var = tk.StringVar()

# Seçenekler listesi

def Octune(event):
    
    if event.char == 'O' or event.char == 'o':
        giris.insert(tk.END,"Ez")
        


style = ttk.Style()
style.configure('TButton', font=('Helvetica', 16))

buttons = [
  
    {"text": "1", "command": lambda: yaz(1), "pos": (15, 160)},
    {"text": "2", "command": lambda: yaz(2), "pos": (85, 160)},
    {"text": "3", "command": lambda: yaz(3), "pos": (155, 160)},
    {"text": "4", "command": lambda: yaz(4), "pos": (15, 220)},
    {"text": "5", "command": lambda: yaz(5), "pos": (85, 220)},
    {"text": "6", "command": lambda: yaz(6), "pos": (155, 220)},
    {"text": "7", "command": lambda: yaz(7), "pos": (15, 280)},
    {"text": "8", "command": lambda: yaz(8), "pos": (85, 280)},
    {"text": "9", "command": lambda: yaz(9), "pos": (155, 280)},
    {"text": ".", "command": lambda: yaz("."), "pos": (155, 340)},
    {"text": "0", "command": lambda: yaz(0), "pos": (15, 340), "width": 10},
    {"text": "x", "command": lambda: islemler("*"), "pos": (155, 100)},
    {"text": "÷", "command": lambda: islemler("/"), "pos": (85, 100)},
    {"text": "%", "command": lambda: islemler("%"), "pos": (15, 100)},
    {"text": "+", "command": lambda: islemler("+"), "pos": (225, 280)},
    {"text": "-", "command": lambda: islemler("-"), "pos": (225, 220)},
    {"text": "=", "command": hesapla, "pos": (225, 340)},
    {"text": "C", "command": temizle, "pos": (225, 100)},
    {"text": "⌫", "command": sil, "pos": (225, 160)},
]

# Create buttons
for button in buttons:
    width = button.get("width", 4)
    ttk.Button(window, width=width, text=button["text"], command=button["command"]).place(height=44, x=button["pos"][0], y=button["pos"][1])
Button(window, width=1, text="...", fg="black", font=("Helvetica", 9),  background='white',command=ikinci_pencere).place(height=15,x=1, y=1)
Button(window, width=1,  text="⟳", fg="white", font=('FontAwesome', 9),  background='black',highlightbackground="black",highlightcolor="black",
       highlightthickness=0,relief="flat",command=gecmisi_goster).place(height=15,x=275, y=3)
# Klavye bağlamaları
window.bind("<Return>", lambda event: hesapla())
window.bind("<KP_Divide>", lambda event: islemler("/"))
window.bind("<KP_Multiply>", lambda event: islemler("*"))
window.bind("<KP_Subtract>", lambda event: islemler("-"))
window.bind("<KP_Add>", lambda event: islemler("+"))
window.bind("<percent>", lambda event: islemler("%"))
window.bind("<BackSpace>", lambda event: sil())
window.bind("<KP_Enter>", lambda event: hesapla())
window.bind("<Key>", lambda event: klavye_islemleri(event))
window.bind("<O>", lambda event: Octune(event))
 

def klavye_islemleri(event):
    if event.char in '0123456789':
        yaz(event.char)
    elif event.char in '+-*/%':         
        islemler(event.char)
    elif event.char == '\r':
        hesapla()
    elif event.char == '.':
        yaz('.')
    elif event.char == 'o':
        Octune(event)
        



window.mainloop()
