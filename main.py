import tkinter as tk
import serial
import threading
import random
import sys
import tkinter.messagebox

pack_flag = "01110011"    #symbol 's'
dest_addr = "0000"
src_addr = "0000"


class Ports:
    def __init__(self):
        self.status = None
        try:
            self.sender = serial.Serial(port='COM1')
            self.sender_info = 'Sender - COM1'
            self.receiver = serial.Serial(port='COM2')
            self.receiver_info = 'Receiver - COM2'
        except serial.SerialException:
            try:
                self.sender = serial.Serial(port='COM3')
                self.sender_info = 'Sender - COM3'
                self.receiver = serial.Serial(port='COM4')
                self.receiver_info = 'Receiver - COM4'
            except serial.SerialException:
                tkinter.messagebox.showerror("Error.",
                                             "There is a problem with ports.")
                self.status = 'Error'

    def write_str_in_port(self, text) -> None:
        for i in range(0, len(text)):
            self.sender.write(data=text[i].encode())

    def read_from_port(self) -> str:
        byte = self.receiver.read(size=1)
        return byte.decode()


ports = Ports()
if ports.status == 'Error':
    sys.exit()

gui = tk.Tk()
gui.title('COM-ports transmitter')
gui.geometry('620x400')
gui.resizable(width=False, height=False)
gui.configure(background="#C0C0C0")


class Window:
    def __init__(self, text, r, c, dflt_txt=''):
        self.sent_bytes = 0
        self.received_bytes = 0
        self.pack_length = 0
        self.fcs = ""
        self.fcs_length = 0

        self.pack = ""
        self.packs = ""

        self.dflt_txt = dflt_txt
        self.text = self.dflt_txt
        self.str = self.dflt_txt
        self.enter_flag = False
        self.label = tk.Label(gui, text=text, font=("Times New Roman", 12), background="#C0C0C0")
        self.label.grid(row=r, column=c, sticky='w')
        self.frame = tk.Frame(gui, width=300, height=150, highlightbackground="#808080")
        self.frame.grid(row=r + 1, column=c)
        self.listbox = tkinter.Listbox(self.frame, bg='#E0E0E0', font=("Courier New", 8), fg='black',
                                       highlightcolor='#A0A0A0', highlightthickness=3,
                                       selectbackground='#404040', activestyle=tkinter.NONE, width=40)
        self.scrollbar = tk.Scrollbar(self.frame, width=20)
        self.scrollbar.grid(row=r + 1, column=c + 1, sticky='ns')
        self.scrollbar.grid_propagate(False)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.grid(row=r + 1, column=c)

    def fcs_former(self, length_int, pack):     #?????????????????????????? fcs
        r0 = 0
        r1 = 0
        r2 = 0
        r3 = 0
        r4 = 0
        print("Pack before: ", pack)
        #_________________________________________________________________________________________
        if length_int == 1:
            self.fcs_length = 2
            pack = str(r0) + str(r1) + pack
            print("Pack coding: ", pack)
            if int(pack[2]) % 2 == 0:
                r0 = 0
                r1 = 0
            else:
                r0 = 1
                r1 = 1
            self.fcs = str(r0) + str(r1)
            pack = str(r0) + str(r1) + pack[2:]
            return pack
        #_________________________________________________________________________________________
        if 2 <= length_int <= 4:
            self.fcs_length = 3
            pack = str(r0) + str(r1) + pack[:1] + str(r2) + pack[1:]
            print("Pack coding: ", pack)

            i = 0
            j = 0
            s = 0
            while(i < len(pack)):
                s = s + int(pack[i])
                i = i + 2
            if s % 2 == 0:
                r0 = 0
            else:
                r0 = 1

            i = 1
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                j = j + 1
                if j == 2:
                    j = 0
                    i = i + 3
                else:
                    i = i + 1
            if s % 2 == 0:
                r1 = 0
            else:
                r1 = 1

            i = 3
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                j = j + 1
                if j == 4:
                    j = 0
                    i = i + 3
                else:
                    i = i + 1
            if s % 2 == 0:
                r2 = 0
            else:
                r2 = 1

            self.fcs = str(r0) + str(r1) + str(r2)
            pack = str(r0) + str(r1) + pack[2] + str(r2) + pack[4:]
            return pack
        #_________________________________________________________________________________________
        if 5 <= length_int <= 11:
            self.fcs_length = 4
            pack = str(r0) + str(r1) + pack[:1] + str(r2) + pack[1:4] + str(r3) + pack[4:]
            print("Pack coding: ", pack)

            i = 0
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                i = i + 2
            if s % 2 == 0:
                r0 = 0
            else:
                r0 = 1

            i = 1
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                j = j + 1
                if j == 2:
                    j = 0
                    i = i + 3
                else:
                    i = i + 1
            if s % 2 == 0:
                r1 = 0
            else:
                r1 = 1

            i = 3
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                j = j + 1
                if j == 4:
                    j = 0
                    i = i + 5
                else:
                    i = i + 1
            if s % 2 == 0:
                r2 = 0
            else:
                r2 = 1

            i = 7
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                j = j + 1
                if j == 8:
                    j = 0
                    i = i + 9
                else:
                    i = i + 1
            if s % 2 == 0:
                r3 = 0
            else:
                r3 = 1

            self.fcs = str(r0) + str(r1) + str(r2) + str(r3)
            pack = str(r0) + str(r1) + pack[2] + str(r2) + pack[4:7] + str(r3) + pack[8:]
            return pack
        # _________________________________________________________________________________________
        if length_int >= 12:
            self.fcs_length = 5
            pack = str(r0) + str(r1) + pack[:1] + str(r2) + pack[1:4] + str(r3) + pack[4:11] + str(r4) + pack[11:]
            print("Pack coding: ", pack)

            i = 0
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                i = i + 2
            if s % 2 == 0:
                r0 = 0
            else:
                r0 = 1

            i = 1
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                j = j + 1
                if j == 2:
                    j = 0
                    i = i + 3
                else:
                    i = i + 1
            if s % 2 == 0:
                r1 = 0
            else:
                r1 = 1

            i = 3
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                j = j + 1
                if j == 4:
                    j = 0
                    i = i + 5
                else:
                    i = i + 1
            if s % 2 == 0:
                r2 = 0
            else:
                r2 = 1

            i = 7
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                j = j + 1
                if j == 8:
                    j = 0
                    i = i + 9
                else:
                    i = i + 1
            if s % 2 == 0:
                r3 = 0
            else:
                r3 = 1

            i = 15
            j = 0
            s = 0
            while (i < len(pack)):
                s = s + int(pack[i])
                j = j + 1
                if j == 16:
                    j = 0
                    i = i + 17
                else:
                    i = i + 1
            if s % 2 == 0:
                r4 = 0
            else:
                r4 = 1

            self.fcs = str(r0) + str(r1) + str(r2) + str(r3) + str(r4)
            pack = str(r0) + str(r1) + pack[2] + str(r2) + pack[4:7] + str(r3) + pack[8:15] + str(r4) + pack[16:]
            return pack

    def length_former(self, length_int):
        length_str = ""
        while(length_int > 0):
            length_str = str(length_int % 2) + length_str
            length_int = length_int // 2
        while(len(length_str) < 4):
            length_str = "0" + length_str
        return length_str

    def bit_stuffing(self, data):
        start_find = 9
        while True:
            print("start_find = ", start_find)
            index = data.find("011100", start_find)
            if index == -1:
                return data
            data1 = data[0: index + 6]
            data2 = data[index + 6:]
            data = data1 + "0" + data2
            start_find = index + 4
        #return data

    def pack_creator(self, length_str, pack):
        pack = pack_flag + dest_addr + src_addr + length_str + pack + self.fcs
        pack = self.bit_stuffing(pack)
        self.packs = self.packs + pack

    def add_symbol(self, symbol):
        self.listbox.delete(tk.END)
        self.text = self.text + symbol
        self.str = self.str + symbol
        self.listbox.insert(tk.END, self.text)
        self.listbox.yview_moveto(1)

    def enter_pushed(self):
        self.text = ""
        self.listbox.insert(tk.END, self.text)
        self.listbox.yview_moveto(1)

    def input_symbol(self, symbol):
        global flag
        flag = 0
        if symbol:

            if symbol != '\n':
                self.add_symbol(symbol)
                self.pack = self.pack + symbol
                self.sent_bytes += 1
                self.pack_length += 1

        if symbol == '\n' and self.sent_bytes != 0:
            if self.pack != "":
                length_str = self.length_former(self.pack_length)
                self.pack = self.fcs_former(self.pack_length, self.pack)
                print("Pack after: ", self.pack)
                print("FCS: ", self.fcs)
                self.pack_creator(length_str, self.pack)
                self.pack = ""
            self.pack_length = 0

            self.sent_bytes = 0
            self.packs = self.packs + '\n'
            print("packs = ", self.packs)
            ports.write_str_in_port(self.packs)
            self.packs = ""
            self.str = ""
            self.fcs_length = 0
            self.fcs = ""
            self.enter_pushed()

        if self.sent_bytes % 15 == 0 and self.sent_bytes != 0:  # ?????? ???????????????? ???? ????, ?????????? ?????????? ?????????????? ???? ?????????????????? ???????????? ?? ???????? ??????????

            length_str = self.length_former(self.pack_length)
            self.pack = self.fcs_former(self.pack_length, self.pack)
            print("Pack after: ", self.pack)
            print("FCS: ", self.fcs)
            self.pack_creator(length_str, self.pack)
            self.pack = ""
            self.pack_length = 0
            self.str = ""
            self.fcs_length = 0
            self.fcs = ""

        if self.sent_bytes % 40 == 0 and self.sent_bytes != 0:
            self.enter_pushed()

    def output_symbol(self, symbol):
        if symbol == '\n':
            self.enter_pushed()
        self.add_symbol(symbol)

    def status_text(self, text):
        self.add_symbol(text)
        self.enter_pushed()


class Status_Window:
    def __init__(self, text, r, c, dflt_txt=''):
        self.dflt_txt = dflt_txt
        self.text = self.dflt_txt
        self.str = self.dflt_txt
        self.enter_flag = False
        self.label = tk.Label(gui, text=text, font=("Times New Roman", 12), background="#C0C0C0")
        self.label.grid(row=r, column=c, sticky='w')
        self.frame = tk.Frame(gui, width=300, height=150, highlightbackground="#808080")
        self.frame.grid(row=r + 1, column=c)
        self.textbox = tkinter.Text(self.frame, bg='#E0E0E0', font=("Courier New", 8), fg='black',
                                       highlightcolor='#A0A0A0', highlightthickness=3, height=12,
                                       selectbackground='#404040', width=40, state="disabled")
        self.scrollbar = tk.Scrollbar(self.frame, width=20)
        self.scrollbar.grid(row=r + 1, column=c + 1, sticky='ns')
        self.scrollbar.grid_propagate(False)
        self.textbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.textbox.yview)
        self.textbox.grid(row=r + 1, column=c)
        self.textbox.tag_configure("RED", foreground="red")
        self.textbox.tag_configure("BLUE", foreground="blue")

    def add_symbol(self, symbol):
        self.textbox.delete(tk.END)
        self.text = self.text + symbol
        self.str = self.str + symbol
        self.textbox.insert(tk.END, self.text)
        self.textbox.yview_moveto(1)

    def enter_pushed(self):
        self.text = ""
        self.textbox.insert(tk.END, self.text)
        self.textbox.yview_moveto(1)

    def output_symbol(self, symbol):
        if symbol == '\n':
            self.enter_pushed()
        self.add_symbol(symbol)

    def status_text(self, text):
        self.add_symbol(text)
        self.enter_pushed()


input_window = Window(text='Input:', r=0, c=0)
output_window = Window(text='Output:', r=0, c=3)
status_window = Status_Window(text='Status:', r=2, c=0)

parity_change_label = tk.Label(gui, text='Parity:', font=("Times New Roman", 12), background="#C0C0C0")
parity_change_label.grid(row=2, column=3, sticky='w')

List = ['PARITY_NONE', 'PARITY_EVEN', 'PARITY_ODD', 'PARITY_MARK', 'PARITY_SPACE']
option = tk.StringVar(gui)
option.set('PARITY_NONE')
parity_menu = tk.OptionMenu(gui, option, *List)
parity_menu.grid(row=3, column=3)


def debit_stuffing(pack, row):
    start_find = 9
    indexs = []
    j = 0
    while True:
        indexs.append(pack.find("0111000", start_find))
        if indexs[j] == -1:
            j -= 1
            status_window.textbox.config(state="normal")
            status_window.textbox.insert(tk.END, pack)
            while j >= 0 and indexs[j] != -1:
                status_window.textbox.insert("%d.%d" % (row, indexs[j] + 6), "0", "RED")
                j -= 1
            if len(pack[20:len(pack)]) == 5:
                status_window.textbox.delete("%d.%d" % (row, 23), "%d.%d" % (row, 25))
                status_window.textbox.insert("%d.%d" % (row, 25), pack[23] + pack[24], "BLUE")
            status_window.textbox.insert(tk.END, "\n")
            status_window.textbox.config(state="disabled")
            return pack
        pack1 = pack[0: indexs[j] + 6]
        pack2 = pack[indexs[j] + 7:]
        pack = pack1 + pack2
        start_find = indexs[j] + 4
        j += 1
    #return pack


def inverter(number):
    if number == 0:
        return 1
    else:
        return 0


def fcs_comparator(old_fcs, new_fcs):
    i = len(old_fcs) - 1
    index = 0
    st = len(old_fcs) - 1
    while i >= 0:
        if int(old_fcs[i]) != int(new_fcs[i]):
            index = index + 2 ** st
        i -= 1
        st -= 1
    return index


def errorer(pack, fcs_length):
    chance = random.randint(1, 100)
    print("Chance: ", chance)
    if chance > 50:
        i = random.randint(0, len(pack) - fcs_length)
        print("Error index: ", i)
        if i == 0:
            pack = str(inverter(int(pack[i]))) + pack[(i + 1):]
        else:
            pack = pack[:(i - 1)] + str(inverter(int(pack[i]))) + pack[i:]
        return pack
    else:
        return pack


def fcs_deformer(pack):
    r0 = 0
    r1 = 0
    r2 = 0
    r3 = 0
    r4 = 0
    if len(pack) == 5:
        fcs_length = 2
        pack = errorer(pack, fcs_length)
        old_fcs = pack[3:]
        pack = pack[:3]
        print("Data after errorer: ", pack)
        print("Old FCS: ", old_fcs)

        pack = str(r0) + str(r1) + pack[2:]
        print("Pack coding: ", pack)

        i = 0
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            i = i + 2
        if s % 2 == 0:
            r0 = 0
        else:
            r0 = 1

        i = 1
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 2:
                j = 0
                i = i + 3
            else:
                i = i + 1
        if s % 2 == 0:
            r1 = 0
        else:
            r1 = 1
        new_fcs = str(r0) + str(r1)
        print("New FCS: ", new_fcs)
        index = fcs_comparator(old_fcs, new_fcs)
        print("Index: ", index)
        if index == 0:
            print("New Data and FCS: ", pack)
            pack = pack[2]
            return pack
        else:
            index -= 1
            if index == 0:
                pack = str(inverter(int(pack[index]))) + pack[(index + 1):]
            else:
                pack = pack[:index] + str(inverter(int(pack[index]))) + pack[index + 1:]
            print("New Data and FCS: ", pack)
            pack = pack[2]
            return pack

    if 8 <= len(pack) <= 10:
        fcs_length = 3
        pack = errorer(pack, fcs_length)
        print("Data and fcs after errorer: ", pack)
        old_fcs = pack[-3:]
        pack = pack[:-3]
        print("Data after errorer: ", pack)
        print("Old FCS: ", old_fcs)

        pack = str(r0) + str(r1) + pack[2] + str(r2) + pack[4:]
        print("Pack coding: ", pack)

        i = 0
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            i = i + 2
        if s % 2 == 0:
            r0 = 0
        else:
            r0 = 1

        i = 1
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 2:
                j = 0
                i = i + 3
            else:
                i = i + 1
        if s % 2 == 0:
            r1 = 0
        else:
            r1 = 1

        i = 3
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 4:
                j = 0
                i = i + 5
            else:
                i = i + 1
        if s % 2 == 0:
            r2 = 0
        else:
            r2 = 1

        new_fcs = str(r0) + str(r1) + str(r2)
        pack = str(r0) + str(r1) + pack[2] + str(r2) + pack[4:]

        print("New FCS: ", new_fcs)
        index = fcs_comparator(old_fcs, new_fcs)
        print("Index: ", index)
        if index == 0:
            print("New Data and FCS: ", pack)
            pack = pack[2] + pack[4:]
            return pack
        else:
            index -= 1
            if index == 0:
                pack = str(inverter(int(pack[index]))) + pack[(index + 1):]
            else:
                pack = pack[:index] + str(inverter(int(pack[index]))) + pack[index + 1:]
            print("New Data and FCS: ", pack)
            pack = pack[2] + pack[4:]
            return pack

    if 13 <= len(pack) <= 19:
        fcs_length = 4
        pack = errorer(pack, fcs_length)
        print("Data and fcs after errorer: ", pack)
        old_fcs = pack[-4:]
        pack = pack[:-4]
        print("Data after errorer: ", pack)
        print("Old FCS: ", old_fcs)

        pack = str(r0) + str(r1) + pack[2] + str(r2) + pack[4:7] + str(r3) + pack[8:]
        print("Pack coding: ", pack)

        i = 0
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            i = i + 2
        if s % 2 == 0:
            r0 = 0
        else:
            r0 = 1

        i = 1
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 2:
                j = 0
                i = i + 3
            else:
                i = i + 1
        if s % 2 == 0:
            r1 = 0
        else:
            r1 = 1

        i = 3
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 4:
                j = 0
                i = i + 5
            else:
                i = i + 1
        if s % 2 == 0:
            r2 = 0
        else:
            r2 = 1

        i = 7
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 8:
                j = 0
                i = i + 9
            else:
                i = i + 1
        if s % 2 == 0:
            r3 = 0
        else:
            r3 = 1

        new_fcs = str(r0) + str(r1) + str(r2) + str(r3)
        pack = str(r0) + str(r1) + pack[2] + str(r2) + pack[4:7] + str(r3) + pack[8:]

        print("New FCS: ", new_fcs)
        index = fcs_comparator(old_fcs, new_fcs)
        print("Index: ", index)
        if index == 0:
            print("New Data and FCS: ", pack)
            pack = pack[2] + pack[4:7] + pack[8:]
            return pack
        else:
            index -= 1
            if index == 0:
                pack = str(inverter(int(pack[index]))) + pack[(index + 1):]
            else:
                pack = pack[:index] + str(inverter(int(pack[index]))) + pack[index + 1:]
            print("New Data and FCS: ", pack)
            pack = pack[2] + pack[4:7] + pack[8:]
            return pack

    if len(pack) >= 22:
        fcs_length = 5
        pack = errorer(pack, fcs_length)
        print("Data and fcs after errorer: ", pack)
        old_fcs = pack[-5:]
        pack = pack[:-5]
        print("Data after errorer: ", pack)
        print("Old FCS: ", old_fcs)

        pack = str(r0) + str(r1) + pack[2] + str(r2) + pack[4:7] + str(r3) + pack[8:15] + str(r4) + pack[16:]
        print("Pack coding: ", pack)

        i = 0
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            i = i + 2
        if s % 2 == 0:
            r0 = 0
        else:
            r0 = 1

        i = 1
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 2:
                j = 0
                i = i + 3
            else:
                i = i + 1
        if s % 2 == 0:
            r1 = 0
        else:
            r1 = 1

        i = 3
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 4:
                j = 0
                i = i + 5
            else:
                i = i + 1
        if s % 2 == 0:
            r2 = 0
        else:
            r2 = 1

        i = 7
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 8:
                j = 0
                i = i + 9
            else:
                i = i + 1
        if s % 2 == 0:
            r3 = 0
        else:
            r3 = 1

        i = 15
        j = 0
        s = 0
        while (i < len(pack)):
            s = s + int(pack[i])
            j = j + 1
            if j == 16:
                j = 0
                i = i + 17
            else:
                i = i + 1
        if s % 2 == 0:
            r4 = 0
        else:
            r4 = 1

        new_fcs = str(r0) + str(r1) + str(r2) + str(r3) + str(r4)
        pack = str(r0) + str(r1) + pack[2] + str(r2) + pack[4:7] + str(r3) + pack[8:15] + str(r4) + pack[16:]

        print("New FCS: ", new_fcs)
        index = fcs_comparator(old_fcs, new_fcs)
        print("Index: ", index)
        if index == 0:
            print("New Data and FCS: ", pack)
            pack = pack[2] + pack[4:7] + pack[8:15] + pack[16:]
            return pack
        else:
            index -= 1
            if index == 0:
                pack = str(inverter(int(pack[index]))) + pack[(index + 1):]
            else:
                pack = pack[:index] + str(inverter(int(pack[index]))) + pack[index + 1:]
            print("New Data and FCS: ", pack)
            pack = pack[2] + pack[4:7] + pack[8:15] + pack[16:]
            return pack



def output_cycle_read():    # ?????? ?????? ???????????????? ?????????? ???? ???????? ????????????

    status_window.textbox.config(state="normal")
    status_window.textbox.delete("1.0", tkinter.END)
    status_window.status_text(ports.sender_info)
    status_window.textbox.insert(tk.END, "\n")
    status_window.status_text(ports.receiver_info)
    status_window.textbox.insert(tk.END, "\n")
    status_window.textbox.config(state="disabled")

    output_str = ""
    pause = False
    index = 0
    pack = ""
    output_bytes = 0
    while True:
        while not pause:
            read_byte = ports.read_from_port()
            if read_byte == '\n':
                pause = True
                break
                output_str = output_str[0:len(output_str)]
            output_str = output_str + read_byte
        #print("output_str = ", output_str)

        status_window.textbox.config(state="normal")
        status_window.textbox.delete("1.0", tkinter.END)
        status_window.textbox.insert(tk.END, ports.sender_info)
        status_window.textbox.insert(tk.END, "\n")
        status_window.textbox.insert(tk.END, ports.receiver_info)
        status_window.textbox.insert(tk.END, "\n")
        status_window.textbox.config(state="disabled")

        row = 3

        while len(output_str) > len(pack):

            #print("len(output_str) = ", len(output_str))
            #print("len(pack) = ", len(pack))

            index = output_str.find(pack_flag, 1)
            if index != 0 and index != -1:
                pack = output_str[0:index]
                output_str = output_str[index:]
                #print("pack = ", pack)
                pack = debit_stuffing(pack, row)     #!
                row += 1
                #print("debit pack = ", pack)

                data_and_fcs = pack[20: len(pack)]
                print("Data and fcs: ", data_and_fcs)
                data = fcs_deformer(data_and_fcs)
                print("Data: ", data)

                for i in range(0, len(data)):
                    output_window.output_symbol(data[i])
                    output_bytes += 1
                    if output_bytes == 40:
                        output_bytes = 0
                        output_window.enter_pushed()
            else:
                pack = output_str
        pack = output_str
        pack = debit_stuffing(pack, row) #!
        data_and_fcs = pack[20: len(pack)]
        print("Data and fcs: ", data_and_fcs)
        data = fcs_deformer(data_and_fcs)
        print("Data: ", data)
        for i in range(0, len(data)):
            output_window.output_symbol(data[i])
            output_bytes += 1
            if output_bytes == 40:
                output_bytes = 0
                output_window.enter_pushed()
        output_window.enter_pushed()
        output_bytes = 0
        output_str = ""
        pack = ""
        pause = False


output_cycle_read_thread = threading.Thread(target=output_cycle_read)
output_cycle_read_thread.daemon = True
output_cycle_read_thread.start()

input_window.listbox.bind('<Return>', lambda x: input_window.input_symbol('\n'))

input_window.listbox.bind('1', lambda x: input_window.input_symbol('1'))
input_window.listbox.bind('0', lambda x: input_window.input_symbol('0'))

gui.mainloop()
ports.sender.close()
ports.receiver.close()