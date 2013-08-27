"""

Text Editor

Note that text styles such as color, font, and text size are not preserved
after re-opening a saved file because the file is saved in plain text format
and the tags are properties of Tkinter.

author: Joe Stepp
last modified: August 2013
github.com/Paradox0

"""

import tkinter
import tkinter.colorchooser
import os
from tkinter import ttk, filedialog, TclError
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font, families

class Application(tkinter.Tk):
    """
    main app
    """

    def __init__(self, parent):
        """calls initialization methods"""

        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.createwidgets()

    def createwidgets(self):
        """sets ups widgets"""

        self.grid()
        self.font = Font(family="Verdana", size=10)

        # main menubar
        self.menubar = tkinter.Menu(self.parent)
        self.config(menu=self.menubar)
        # list of fonts on the system
        self.fontoptions = families(self.parent)

        self.fileMenu = tkinter.Menu(self.menubar, tearoff=0)
        self.editMenu = tkinter.Menu(self.menubar, tearoff=0)
        self.fsubmenu = tkinter.Menu(self.editMenu, tearoff=0)
        self.ssubmenu = tkinter.Menu(self.editMenu, tearoff=0)

        # adds fonts to the font submenu and associates lambda functions
        for option in self.fontoptions:
            self.fsubmenu.add_command(label=option, command = lambda: self.font.configure(family=option))

        # adds values to the size submenu and associates lambda functions
        for value in range(1,31):
            self.ssubmenu.add_command(label=str(value), command = lambda: self.font.configure(size=value))

        # adding commands to the menus
        self.fileMenu.add_command(label="New", command=self.new)
        self.fileMenu.add_command(label="Open", command=self.open)
        self.fileMenu.add_command(label="Save", command=self.save)
        self.fileMenu.add_command(label="Exit", command=self.exit)
        self.editMenu.add_command(label="Color", command=self.color)
        self.editMenu.add_cascade(label="Font", underline=0, menu=self.fsubmenu)
        self.editMenu.add_cascade(label="Size", underline=0, menu=self.ssubmenu)
        self.editMenu.add_command(label="Bold", command=self.bold)
        self.editMenu.add_command(label="Italic", command=self.italic)
        self.editMenu.add_command(label="Underline", command=self.underline)
        self.editMenu.add_command(label="Overstrike", command=self.overstrike)
        self.editMenu.add_command(label="Undo", command=self.undo)
        self.editMenu.add_command(label="Redo", command=self.redo)

        # adds menus as cascades to the menubar
        self.menubar.add_cascade(label="File", menu=self.fileMenu, underline=0)
        self.menubar.add_cascade(label="Edit", menu=self.editMenu, underline=0)

        # main text widgets
        self.text = ScrolledText(self, state='normal', height=30, wrap='word', font = self.font, pady=2, padx=3, undo=True)
        self.text.grid(column=0, row=0, sticky='NSEW')

        # Frame configuration

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, True)

    #logic

    def new(self):
        """Creates a new window to replace the current one. Does not preserve  text in the old window!"""
        app = Application(None)
        app.title('Text Editor')
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

    def bold(self):
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

    def italic(self):
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

    def underline(self):
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

    def overstrike(self):
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

    def undo(self):
        """Undo function"""
        try:
            self.text.edit_undo()
        except TclError:
            pass

    def redo(self):
        """Redo function"""
        try:
            self.text.edit_redo()
        except TclError:
            pass

    def open(self):
        """Opens a file dialog to open a plain text file."""
        filename = tkinter.filedialog.askopenfilename()

        with open(filename) as f:
            text = f.read()

        self.text.delete("1.0", "end")
        self.text.insert('insert', text)

    def save(self):
        """Opens a file dialog to save the text in plain text format."""
        text = self.text.get("1.0", "end")
        filename = tkinter.filedialog.asksaveasfilename()

        with open(filename, 'w') as f:
            f.write(text)

    def exit(self):
        """Exits the program."""
        self.quit()

if __name__ == "__main__":
    app = Application(None)
    app.title('Text Editor')
    app.option_add('*tearOff', False)
    app.mainloop()
