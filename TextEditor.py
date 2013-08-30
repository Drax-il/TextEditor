"""

Text Editor

Note that text styles such as color, font, and text size are not preserved
after re-opening a saved file because the file is saved in plain text format
and the tags are properties of the Tkinter text widget.

author: Joe Stepp
last modified: August 2013
github.com/Paradox0

"""

import os
import tkinter
import tkinter.colorchooser
from tkinter import ttk, filedialog, TclError
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font, families

class Application(tkinter.Tk):
    def __init__(self):
        """Initialize widgets, methods."""

        tkinter.Tk.__init__(self)
        self.grid()

        fontoptions = families(self)
        font = Font(family="Verdana", size=10)

        menubar = tkinter.Menu(self)
        fileMenu = tkinter.Menu(menubar, tearoff=0)
        editMenu = tkinter.Menu(menubar, tearoff=0)
        fsubmenu = tkinter.Menu(editMenu, tearoff=0)
        ssubmenu = tkinter.Menu(editMenu, tearoff=0)

        # adds fonts to the font submenu and associates lambda functions
        for option in fontoptions:
            fsubmenu.add_command(label=option, command = lambda: font.configure(family=option))
        # adds values to the size submenu and associates lambda functions
        for value in range(1,31):
            ssubmenu.add_command(label=str(value), command = lambda: font.configure(size=value))

        # adds commands to the menus
        menubar.add_cascade(label="File",underline=0, menu=fileMenu)
        menubar.add_cascade(label="Edit",underline=0, menu=editMenu)
        fileMenu.add_command(label="New", underline=1,
                             command=self.new, accelerator="Ctrl+N")
        fileMenu.add_command(label="Open", command=self.open, accelerator="Ctrl+O")
        fileMenu.add_command(label="Save", command=self.save, accelerator="Ctrl+S")
        fileMenu.add_command(label="Exit", underline=1,
                             command=exit, accelerator="Ctrl+Q")
        editMenu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        editMenu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        editMenu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        editMenu.add_cascade(label="Font", underline=0, menu=fsubmenu)
        editMenu.add_cascade(label="Size", underline=0, menu=ssubmenu)
        editMenu.add_command(label="Color", command=self.color)
        editMenu.add_command(label="Bold", command=self.bold, accelerator="Ctrl+B")
        editMenu.add_command(label="Italic", command=self.italic, accelerator="Ctrl+I")
        editMenu.add_command(label="Underline", command=self.underline, accelerator="Ctrl+U")
        editMenu.add_command(label="Overstrike", command=self.overstrike, accelerator="Ctrl+T")
        editMenu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        editMenu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        self.config(menu=menubar)

        """Accelerator bindings. The cut, copy, and paste functions are not
        bound to keyboard shortcuts because Windows already binds them, so if
        Tkinter bound them as well whenever you typed ctrl+v the text would be
        pasted twice."""
        self.bind_all("<Control-n>", self.new)
        self.bind_all("<Control-o>", self.open)
        self.bind_all("<Control-s>", self.save)
        self.bind_all("<Control-q>", self.exit)
        self.bind_all("<Control-b>", self.bold)
        self.bind_all("<Control-i>", self.italic)
        self.bind_all("<Control-u>", self.underline)
        self.bind_all("<Control-T>", self.overstrike)
        self.bind_all("<Control-z>", self.undo)
        self.bind_all("<Control-y>", self.redo)

        self.text = ScrolledText(self, state='normal', height=30, wrap='word', font = font, pady=2, padx=3, undo=True)
        self.text.grid(column=0, row=0, sticky='NSEW')

        # Frame configuration
        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, True)

    """Command functions. *args is included because the keyboard bindings pass
    two arguments to the functions, while clicking in the menu passes only 1."""

    def new(self, *args):
        """Creates a new window."""
        app = Application()
        app.title('Python Text Editor')
        app.option_add('*tearOff', False)
        app.mainloop()

    def color(self):
        """Changes selected text color."""
        try:
            (rgb, hx) = tkinter.colorchooser.askcolor()
            self.text.tag_add('color', 'sel.first', 'sel.last')
            self.text.tag_configure('color', foreground=hx)
        except TclError:
            pass

    def bold(self, *args):
        """Toggles bold for selected text."""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "bold" in current_tags:
                self.text.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text.tag_add("bold", "sel.first", "sel.last")
                bold_font = Font(self.text, self.text.cget("font"))
                bold_font.configure(weight="bold")
                self.text.tag_configure("bold", font=bold_font)
        except TclError:
            pass

    def italic(self, *args):
        """Toggles italic for selected text."""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "italic" in current_tags:
                self.text.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text.tag_add("italic", "sel.first", "sel.last")
                italic_font = Font(self.text, self.text.cget("font"))
                italic_font.configure(slant="italic")
                self.text.tag_configure("italic", font=italic_font)
        except TclError:
            pass

    def underline(self, *args):
        """Toggles underline for selected text."""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "underline" in current_tags:
                self.text.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text.tag_add("underline", "sel.first", "sel.last")
                underline_font = Font(self.text, self.text.cget("font"))
                underline_font.configure(underline=1)
                self.text.tag_configure("underline", font=underline_font)
        except TclError:
            pass

    def overstrike(self, *args):
        """Toggles overstrike for selected text."""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "overstrike" in current_tags:
                self.text.tag_remove("overstrike", "sel.first", "sel.last")
            else:
                self.text.tag_add("overstrike", "sel.first", "sel.last")
                overstrike_font = Font(self.text, self.text.cget("font"))
                overstrike_font.configure(overstrike=1)
                self.text.tag_configure("overstrike", font=overstrike_font)
        except TclError:
            pass

    def undo(self, *args):
        """Undo function"""
        try:
            self.text.edit_undo()
        except TclError:
            pass

    def redo(self, *args):
        """Redo function"""
        try:
            self.text.edit_redo()
        except TclError:
            pass

    def copy(self, *args):
        """Copy text"""
        self.clipboard_clear()
        self.clipboard_append(self.text.selection_get())

    def cut(self, *args):
        """Cut text"""
        self.copy
        self.text.delete("sel.first", "sel.last")

    def paste(self, *args):
        """Paste text"""
        focus=self.focus_get()
        insertion = self.selection_get(selection = "CLIPBOARD")
        self.text.insert(0.0, insertion)

    def open(self, *args):
        """Opens a file dialog to open a plain text file."""
        filename = tkinter.filedialog.askopenfilename()

        with open(filename) as f:
            text = f.read()

        self.text.delete("1.0", "end")
        self.text.insert('insert', text)

    def save(self, *args):
        try:
            """Opens a file dialog to save the text in plain text format."""
            text = self.text.get("1.0", "end")
            filename = tkinter.filedialog.asksaveasfilename()

            with open(filename, 'w') as f:
                f.write(text)
        except FileNotFoundError:
            pass

    def exit(self, *args):
        """Exits the program."""
        self.quit()

if __name__ == "__main__":
    app=Application()
    app.title('Python Text Editor')
    app.option_add('*tearOff', False)
    app.mainloop()




