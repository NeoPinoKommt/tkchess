from tkinter import *
import sympy as sp
from PIL import Image, ImageTk
from io import BytesIO
from increchess import *


"""
tila pitää sisällään preamblen latexin näyttöön
iteroitaessa sanakirja läpi ja yhdistettäessä ne .join komennolla,
lisää r eli raw joka stringin eteen kuten
TODO
cut trailing spaces from latex input
sanitize self.strvar and finally get rid of it
to change it into dictionary item
    -one place to access for moves, no need for erotus in parsemoves
"""


tila = {
    r"\documentclass{standalone}": True,
    r"\usepackage{skak}": True,
    #r"\usepackage{xskak}": True,
    r"\begin{document}": True,
    #r"\usetextfig" #pgn notation shown as text
    #r"\usesymfig" #pgn notation shown with symbols
    r"\newgame": True,
    #r"\newchessgame": True,
    #r"\notationon": True,
    #r"\moveron": True,
    #r"\xskakset{style=styleC}"
    #r"\styleC"
    #r"\mainline{1.e4 e5 2. Nf3 Nc6 3.Bb5}\\"
    #r"" + self.strvar.get() +
    #r"\mainline{" + self.strvar.get() + r"}\\"
    #r"\hidemoves{" + self.strvar.get() + r"}\\": False,
    
    #r"\fenboard{1q3kr1/3rb2p/p3Q3/8/1p6/8/PPP3PP/4R2K w - - 0 26}": False,
    #r"\showonlywhite"
    #r"\notationoff"
    
    r"\WhiteEmptySquare": True #see chessfss.pdf
    #r"\showinverseboard": False,
    #r"\showboard": True,
    #r"\[ \showboard \]"
    #r"\end{figure}",
}

tila_end = {
    r"\showinverseboard": False,
    r"\showboard": True

}



class Root():
    def __init__(self, master):
        """
        initialize and set grid layout
        """
        self.master = master
        master.geometry("800x700")
        self.strvar = StringVar()
        self.label = Label(master)
        self.entry = Entry(master, textvariable = self.strvar, width = 80)


        #self.strvar.set(r"\mainline{1.e4 e5 2. Nf3 Nc6 3.Bb5}\\")
        self.strvar.set(r"1.e4 e5 2.Nf3 Nc6 3.Bb5")
        self.button = Button(text = "pgn draw", command = self.to_latex)
        self.button2 = Button(text = "flip", command = self.inverse)
        #self.button3 = Button(text = "computer", command = computer_move(self.strvar.get()))
        self.button4 = Button(text = "test", command = lambda:[parsemoves(self.strvar.get()), self.strvar.set(sanstila["sanssit"]), self.to_latex()])

        self.entry.grid(row=0, columnspan=4, sticky=W+E)
        self.button.grid(row=0, column=5)
        self.button2.grid(row=0, column=6)
        #self.button3.grid(row=0, column=7)
        self.button4.grid(row=0, column=8)
        self.label.grid(row=3, column=1, columnspan=12, ipadx=20, padx=20, sticky=W+E)



    def inverse(self):
        if tila_end[r"\showinverseboard"] == False:
            tila_end[r"\showinverseboard"] = True
            tila_end[r"\showboard"] = False
        else:
            tila_end[r"\showinverseboard"] = False
            tila_end[r"\showboard"] = True
        #print(preamblecreator()) #debugging print, outcommented most of the time
        self.to_latex()


    def preamblecreator(self): #add arguments which are calling options
        """
        this function creates the preamble for sympy.preview
        TODO:
        -remove showboard from tila and add it here separately so that you can 
        add  self.strvar.get() in preamble
        """
        str_amble = ""
        for key in tila:
            #print(key)
            #print(key, '->', tila[key])
            if tila[key] == True:
                str_amble += key
        #str_amble += r"\showboard" + ","
        str_amble += r"\hidemoves{" + self.strvar.get() + r"}\\"
        for key in tila_end:
            if tila_end[key] == True:
                str_amble += key
        #print(str_amble)
        """
        for item in tila.items():
            print(item)
            print(type(item))
        """
        return str_amble



    def to_latex(self):
        expr = " "
        #print(self.strvar.get())
        preamble = self.preamblecreator()
        pgn = self.strvar.get()
        #This creates a ByteIO stream and saves there the output of sympy.preview
        f = BytesIO()
        #the_color = "{" + self.master.cget('bg')[1:].upper()+"}"
        #print("pagecolor vari: {}".format(the_color))
        try:
            sp.preview(expr, euler = False, preamble = preamble, viewer = "BytesIO", output = "ps", outputbuffer=f)
        except:
            print("Latex error propably, check sympy.preview input")
            pass
        f.seek(0)
        #Open the image as if it were a file. This works only for .ps!
        img = Image.open(f)
        #See note at the bottom
        img.load(scale = 5)
        img = img.resize((int(img.size[0]/2),int(img.size[1]/2)),Image.BILINEAR)
        photo = ImageTk.PhotoImage(img)
        self.label.config(image = photo)
        self.label.image = photo
        f.close()


master = Tk()
root   = Root(master)
master.mainloop()