import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import font as tkFont
import os
import backend
import random

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # fonts
        self.helv20 = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
        self.times15 = tkFont.Font(family='Times', size=15, weight=tkFont.BOLD)
        self.times12nb = tkFont.Font(family='Times', size=12, weight=tkFont.BOLD)
        self.helv10 = tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD)
        self.helv15 = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # navbar with buttons
        navbar = tk.Frame(container, bg="#C0C0C0")
        navbar.grid(row=0, column=0, sticky='nsew')
        #os.chdir(os.getcwd()+r"\icons")
        logo = PhotoImage(file="logo.png").subsample(2,2)
        logo_label = tk.Label(navbar, image=logo, bg="#C0C0C0")
        logo_label.image = logo
        logo_label.pack(side='left')
        logo_heading = tk.Label(navbar, text="WORD STACK", font=self.helv20, bg="#C0C0C0")
        logo_heading.pack(side='left', padx=(10,0))

        voteimg = PhotoImage(file="upvote.png").subsample(2,2)
        top_button=ttk.Button(navbar, image=voteimg, command=lambda: self.show_frame("TopNWordsPage"))
        top_button.image = voteimg
        top_button.pack(side='right')

        searchimg = PhotoImage(file="search.png").subsample(2,2)
        search_button=ttk.Button(navbar, image=searchimg, command=lambda: self.show_frame("PageOne"))
        search_button.image = searchimg
        search_button.pack(side='right')

        homeimg = PhotoImage(file="home.png").subsample(2,2)
        home_button=ttk.Button(navbar, image=homeimg, command=lambda: self.show_frame("StartPage"))
        home_button.image = homeimg
        home_button.pack(side='right')

        self.frames={}
        for F in (StartPage,PageOne,RevisionPage,TopNWordsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()




class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self,parent)
        #tk.Frame.config(self, bg="red")
        tk.Frame.grid_columnconfigure(self, 0, weight=1)
        tk.Frame.grid_columnconfigure(self, 4, weight=1)
        # word-add frame
        word_frame = tk.LabelFrame(self, text="Add New Words", font=controller.helv15)
        word_frame.grid(row=1, column=1,pady=30, padx=(0,20), ipadx=10)
        # word-add structure and child widgets
        body_af = tk.Frame(word_frame)
        body_af.pack(fill='both', expand=True)
        body_af.pack_propagate(False)
        laf1 = tk.Label(body_af, text='Word set:', font=controller.helv10)
        laf1.grid(row=1, column=1, sticky='ne', padx=10, pady=(10,0))
        laf2 = tk.Label(body_af, text='Words:', font=controller.helv10)
        laf2.grid(row=2, column=1, sticky='ne', padx=10, pady=10)
        laf3 = tk.Label(body_af, text='Custom:', font=controller.helv10)
        laf3.grid(row=3, column=1, sticky='ne', padx=10)
        self.eaf1 = tk.Entry(body_af, width=55)   #set name entry widget
        self.eaf1.grid(row=1, column=2, pady=(10,0))
        self.eaf2 = tk.Text(body_af, height=10, width=40)    #word textbox entry widget
        self.eaf2.grid(row=2, column=2, pady=10)
        self.eaf3 = tk.Text(body_af, height=5, width=40)    #custom definitions textbox widget
        self.eaf3.grid(row=3, column=2)
        self.add_button=ttk.Button(body_af, text="Add", command=self.get_items)
        self.add_button.grid(row=4, column=1, columnspan=2, pady=20)

        # wordlist frame
        wordlist_frame = tk.LabelFrame(self, height=600, text="Revise", font=controller.helv15)
        wordlist_frame.grid(row=1, column=2, pady=30, padx=(0,20))
        # word-list frame structure and child widgets
        body_wf = tk.Frame(wordlist_frame)
        body_wf.pack(pady=0)

        refresh_button1 = tk.Button(body_wf, text="Refresh", command=self.populate_listbox)
        refresh_button1.grid(row=0, column=0, columnspan=2, sticky='e', padx=(0,5), pady=(0,5))

        self.listbox = tk.Listbox(body_wf, width=50, height=18,  background=wordlist_frame.cget("bg"))
        #self.listbox.pack(side='left', fill='y')
        self.listbox.grid(row=1, column=0)
        self.scrollbar = tk.Scrollbar(body_wf)
        #self.scrollbar.pack(side='left', fill='y')
        self.scrollbar.grid(row=1, column=1, stick='nsew')
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.populate_listbox()
        revbutton = ttk.Button(wordlist_frame, text='Revise', command=lambda: controller.show_frame('RevisionPage'))
        revbutton.pack(pady=(5,12))

        # last revised frame
        lr_frame = tk.LabelFrame(self, text="Log", font=controller.helv15)
        lr_frame.grid(row=1, column=3, pady=30)
        # last revised structure and child widgets
        refresh_button2 = tk.Button(lr_frame, text="Refresh", command=self.show_history)
        refresh_button2.grid(row=0, column=0, sticky='e', padx=(0,5), pady=(0,5))

        self.his_container = tk.Frame(lr_frame, width=250, height=335, bg="blue")
        self.his_container.grid(row=1, column=0)
        self.his_container.grid_propagate(False)
        self.show_history()


    def get_items(self):
        '''------------------------------------------------------------------------------
        1.0 means that the input should be read from line one, character zero
        The end part means to read until the end of the text box is reached and
        -1c deletes 1 character from end as by default the text box adds a newline at end.
        ----------------------------------------------------------------------------------'''
        setname = self.eaf1.get()
        textboxdata=self.eaf2.get("1.0", 'end-1c')
        customboxdata=self.eaf3.get("1.0",'end-1c')
        if setname!='' and textboxdata!='':
            x=backend.workonwords(setname,textboxdata,customboxdata)
            if not x:
                pass
            else:
                nfwrds=""
                for i in x:
                    nfwrds=nfwrds+i+', '
                messagebox.showinfo("Not Found", nfwrds)
        else:
            messagebox.showwarning("Warning","You have left some fields blank")

    def populate_listbox(self):
        self.listbox.delete(0,'end')    #clearing listbox beforte populating
        listbox_items = backend.getallsets()
        for i in range(len(listbox_items)):
            self.listbox.insert(tk.END, listbox_items[i][0])

    def getlistboxvalue(self):
        clicked_item = self.listbox.curselection()
        selected_set = self.listbox.get(clicked_item)
        backend.date_update(selected_set)
        return(selected_set)


    def onFrameConfigure3(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.his_canvas.configure(scrollregion=self.his_canvas.bbox("all"))
    def FrameWidth3(self, event):
        canvas_width = event.width
        self.his_canvas.itemconfig(self.his_canvas_frame, width = canvas_width)

    def show_history(self):
        # getting last revised history dictionary
        his_list = backend.history()
        # destroying children widgets
        children = self.his_container.winfo_children()
        for child in children:
            child.destroy()

        # creating children widgets
        self.his_canvas = tk.Canvas(self.his_container, width=250, height=335)
        result_frame = tk.Frame(self.his_canvas)
        rscb = tk.Scrollbar(self.his_container, orient="vertical", command=self.his_canvas.yview)
        self.his_canvas.configure(yscrollcommand=rscb.set)

        rscb.pack(side='right', fill='y')
        self.his_canvas.pack(side='left')
        self.his_canvas_frame = self.his_canvas.create_window((1,1),window=result_frame, anchor="nw",tags="result_frame")

        result_frame.bind("<Configure>", self.onFrameConfigure3)
        self.his_canvas.bind('<Configure>', self.FrameWidth3)

        self.hiscol1head = tk.Label(result_frame, text='Set', bg='#C0C0C0', fg='black', font=self.controller.helv10)
        self.hiscol1head.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        self.hiscol2head = tk.Label(result_frame, text='Last Revised On', bg='#C0C0C0', fg='black', font=self.controller.helv10)
        self.hiscol2head.grid(row=0, column=1, sticky='nsew', padx=1, pady=1)

        for row_ in range(len(his_list)):
            wf =tk.Frame(result_frame, bg='#E0E0E0')
            wf.grid(row=row_+1, column=0, sticky='nsew', padx=1, pady=1)
            self.label5 = tk.Label(wf, text=his_list[row_][0], bg='#E0E0E0')
            self.label5.pack(side='left', padx=(5,0))

            mf = tk.Frame(result_frame, bg='#E0E0E0')
            mf.grid(row=row_+1, column=1, sticky='nsew', padx=1, pady=1)
            self.label6 = tk.Label(mf, text=his_list[row_][1], bg='#E0E0E0')
            self.label6.pack(side='left', padx=(5,0))

        result_frame.grid_columnconfigure(0, weight=1)
        result_frame.grid_columnconfigure(1, weight=3)



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        notebook = ttk.Notebook(self)
        # creating tabs
        self.tab1 = tk.Frame(notebook)
        self.tab2 = tk.Frame(notebook)
        # adding tabs to Notebook
        notebook.add(self.tab1, text='Search a Word')
        notebook.add(self.tab2, text='View by Alphabets')
        notebook.pack(fill='both', expand=True)
        # adding widgets to tab 1
        search_frame = tk.Frame(self.tab1)
        search_frame.pack(side='top')
        search_label = tk.Label(search_frame, text='Enter word or part of it', font=controller.helv10)
        search_label.pack(pady=10)
        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(pady=(0,10))
        submit1 = ttk.Button(search_frame, text='Search', command=self.wordsearch)
        submit1.pack()

        self.container = tk.Frame(self.tab1)
        self.container.pack(side='bottom', fill='both', expand=True, padx=(20,0), pady=15)

        # adding widgets to tab 2
        checkbox_container = tk.LabelFrame(self.tab2, text='Words begining from: ', font=controller.helv10)
        checkbox_container.pack(pady=10)
        alphabets=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
                    'Q','R','S','T','U','V','W','X','Y','Z']
        alpha_counter = 0
        self.vars=[]
        for row in range(2):
            for column in range(13):
                var = tk.IntVar()
                self.cb = tk.Checkbutton(checkbox_container, text=alphabets[alpha_counter], variable=var)
                self.cb.grid(row=row, column=column)
                self.vars.append(var)
                alpha_counter +=1

        submit2 = ttk.Button(self.tab2, text='View Words', command=self.letter_search)
        submit2.pack()

        self.container2 = tk.Frame(self.tab2)
        self.container2.pack(side='bottom', fill='both', expand=True, padx=(20,0), pady=15)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

    # same thing for tab2
    def onFrameConfigure2(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))
    def FrameWidth2(self, event):
        canvas_width = event.width
        self.canvas2.itemconfig(self.canvas2_frame, width = canvas_width)


    def wordsearch(self):
        # getting matching words with definition from database
        word=self.search_entry.get()
        wm_dictionary = backend.search_by_word(word)
        l = list(wm_dictionary.keys())
        # destroying children widgets
        children = self.container.winfo_children()
        for child in children:
            child.destroy()

        # creating children widgets
        self.canvas = tk.Canvas(self.container)
        result_frame = tk.Frame(self.canvas)
        rscb = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=rscb.set)

        rscb.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas_frame = self.canvas.create_window((1,1),window=result_frame, anchor="nw",tags="result_frame")

        result_frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind('<Configure>', self.FrameWidth)

        self.col1head = tk.Label(result_frame, text='WORD', bg='#C0C0C0', fg='black', font=self.controller.helv10)
        self.col1head.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        self.col2head = tk.Label(result_frame, text='MEANING', bg='#C0C0C0', fg='black', font=self.controller.helv10)
        self.col2head.grid(row=0, column=1, sticky='nsew', padx=1, pady=1)

        for row_ in range(len(l)):
            wf =tk.Frame(result_frame, bg='#E0E0E0')
            wf.grid(row=row_+1, column=0, sticky='nsew', padx=1, pady=1)
            self.label = tk.Label(wf, text=l[row_], bg='#E0E0E0')
            self.label.pack()

            mf = tk.Frame(result_frame, bg='#E0E0E0')
            mf.grid(row=row_+1, column=1, sticky='nsew', padx=1, pady=1)
            self.label2 = tk.Message(mf, text=wm_dictionary[l[row_]], bg='#E0E0E0', width=900)
            self.label2.pack(side='left', padx=10)

        result_frame.grid_columnconfigure(0, weight=1)
        result_frame.grid_columnconfigure(1, weight=3)

    def letter_search(self):
        selected_letters=[]
        for var in range(len(self.vars)):
            if self.vars[var].get()==1:
                letter = chr(97+var)
                selected_letters.append(letter)
        wm_dictionary2 = backend.search_by_letter(selected_letters)
        l2= list(wm_dictionary2.keys())
        # destroying children widgets
        children = self.container2.winfo_children()
        for child in children:
            child.destroy()

        # creating children widgets
        self.canvas2 = tk.Canvas(self.container2)
        result_frame = tk.Frame(self.canvas2)
        rscb = tk.Scrollbar(self.container2, orient="vertical", command=self.canvas2.yview)
        self.canvas2.configure(yscrollcommand=rscb.set)

        rscb.pack(side='right', fill='y')
        self.canvas2.pack(side='left', fill='both', expand=True)
        self.canvas2_frame = self.canvas2.create_window((1,1),window=result_frame, anchor="nw",tags="result_frame")

        result_frame.bind("<Configure>", self.onFrameConfigure2)
        self.canvas2.bind('<Configure>', self.FrameWidth2)

        self.col1head2 = tk.Label(result_frame, text='WORD', bg='#C0C0C0', fg='black', font=self.controller.helv10)
        self.col1head2.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        self.col2head2 = tk.Label(result_frame, text='MEANING', bg='#C0C0C0', fg='black', font=self.controller.helv10)
        self.col2head2.grid(row=0, column=1, sticky='nsew', padx=1, pady=1)

        for row_ in range(len(l2)):
            wf =tk.Frame(result_frame, bg='#E0E0E0')
            wf.grid(row=row_+1, column=0, sticky='nsew', padx=1, pady=1)
            self.label3 = tk.Label(wf, text=l2[row_], bg='#E0E0E0')
            self.label3.pack()

            mf = tk.Frame(result_frame, bg='#E0E0E0')
            mf.grid(row=row_+1, column=1, sticky='nsew', padx=1, pady=1)
            self.label4 = tk.Message(mf, text=wm_dictionary2[l2[row_]], bg='#E0E0E0', width=900)
            self.label4.pack(side='left', padx=10)

        result_frame.grid_columnconfigure(0, weight=1)
        result_frame.grid_columnconfigure(1, weight=3)


class RevisionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.heading = tk.Label(self, text='', font=controller.helv20)
        self.heading.grid(row=0, column=2, pady=10)

        previmg=PhotoImage(file="prev.png").subsample(3,3)
        prev=tk.Button(self, image=previmg, borderwidth=0, command=self.prevfunc)
        prev.image = previmg
        prev.grid(row=1, column=1)

        word_frame = tk.Frame(self, bd=3, width=500, height=200, relief=tk.GROOVE)
        word_frame.grid(row=1, column=2, pady=20, padx=30)
        word_frame.grid_propagate(False)
        vote = tk.Button(word_frame, text='Vote', command=self.votefunc)
        vote.grid(row=0, column=3)
        self.wlb=tk.Label(word_frame, text="", font=controller.helv20)
        self.wlb.grid(row=1, column=0, columnspan=2)
        word_frame.grid_columnconfigure(1, weight=1)
        word_frame.grid_rowconfigure(1, weight=1)


        nextimg = PhotoImage(file='next.png').subsample(3,3)
        next=tk.Button(self, image=nextimg, borderwidth=0, command=self.nextfunc)
        next.image = nextimg
        next.grid(row=1, column=3)

        check=tk.Button(self, text="Check Meaning", command=self.meaningfunc)
        check['font']=controller.helv15
        check.grid(row=2, column=2)

        meaning_frame = tk.Frame(self, bd=3, width=500, height=300, relief=tk.GROOVE)
        meaning_frame.grid(row=3, column=2, pady=20)
        meaning_frame.grid_propagate(False)

        note="**Key bindings: <- for previous, -> for next, space to see meaning."
        note=tk.Label(self, text=note, fg="red")
        note.grid(row=4, column=1, columnspan=3)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # adding meaning text area
        tbscb = tk.Scrollbar(meaning_frame)
        tbscb.pack(side='right', fill='y')
        self.meaningtb=tk.Text(meaning_frame, width=60, height=17, wrap=tk.WORD)
        self.meaningtb.pack(side='left')
        self.meaningtb.config(state=tk.DISABLED)
        self.meaningtb.config(yscrollcommand=tbscb.set)
        tbscb.config(command=self.meaningtb.yview)


    def tkraise(self, aboveThis=None):
        try:
            start_page = self.controller.frames['StartPage']
            self.setname = start_page.getlistboxvalue()
            self.heading.configure(text=self.setname)
            self.wlb.config(text="Lets Start...")
            self.dict2 = backend.extract_word_meaning(self.setname)
            self.listkeys=list(self.dict2.keys())
            random.shuffle(self.listkeys)
            self.ptr = -1
            super().tkraise(aboveThis)
        except:
            messagebox.showwarning("Warning","Select a set first")

    def nextfunc(self):
        self.ptr += 1
        self.cleanup_textbox()
        try:
            word=self.listkeys[self.ptr]
            self.wlb.config(text=word)
        except:
            self.wlb.config(text="NO MORE WORDS !!")

    def prevfunc(self):
        self.ptr -= 1
        self.cleanup_textbox()
        try:
            word=self.listkeys[self.ptr]
            self.wlb.config(text=word)
        except:
            self.wlb.config(text="NO MORE WORDS !!")

    def cleanup_textbox(self):
        self.meaningtb.config(state=tk.NORMAL)
        self.meaningtb.delete('1.0', tk.END)
        self.meaningtb.config(state=tk.DISABLED)

    def meaningfunc(self):
        '''----------------
        1. enable state
        2. clear text area
        3. insert text
        4. disable state
        --------------------'''
        try:
            key=self.listkeys[self.ptr]
            meaning=self.dict2[key]
            self.meaningtb.config(state=tk.NORMAL)
            self.meaningtb.delete('1.0', tk.END)
            self.meaningtb.insert('1.0', meaning)
            self.meaningtb.config(state=tk.DISABLED)
        except:
            self.meaningtb.insert('1.0', "No more words")

    def votefunc(self):
        if self.ptr > -1 and self.ptr < len(self.listkeys):
            backend.vote_update(self.listkeys[self.ptr])
            print('success')
        else:
            pass

class TopNWordsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.dict = backend.most_voted()
        self.lw = list(self.dict.keys())
        self.ptr = -1

        self.heading = tk.Label(self, text='Most Voted Words', font=controller.helv20)
        self.heading.grid(row=0, column=2, pady=10)

        previmg=PhotoImage(file="prev.png").subsample(3,3)
        prev=tk.Button(self, image=previmg, borderwidth=0, command=self.prevfunc)
        prev.image = previmg
        prev.grid(row=1, column=1)

        word_frame = tk.Frame(self, bd=3, width=500, height=200, relief=tk.GROOVE)
        word_frame.grid(row=1, column=2, pady=20, padx=30)
        word_frame.grid_propagate(False)
        voteup = tk.Button(word_frame,text="Vote"+chr(8593), bg="#228b22")
        voteup.grid(row=0, column=0)
        votedown = tk.Button(word_frame,text="Vote "+chr(8595), bg="#DC143C")
        votedown.grid(row=0, column=3)
        self.wlb=tk.Label(word_frame, text="Lets start...", font=controller.helv20)
        self.wlb.grid(row=1, column=0, columnspan=2)
        word_frame.grid_columnconfigure(1, weight=1)
        word_frame.grid_rowconfigure(1, weight=1)

        nextimg = PhotoImage(file='next.png').subsample(3,3)
        next=tk.Button(self, image=nextimg, borderwidth=0, command=self.nextfunc)
        next.image = nextimg
        next.grid(row=1, column=3)

        check=tk.Button(self, text="Check Meaning", command=self.meaningfunc)
        check['font']=controller.helv15
        check.grid(row=2, column=2)

        meaning_frame = tk.Frame(self, bd=3, width=500, height=300, relief=tk.GROOVE)
        meaning_frame.grid(row=3, column=2, pady=20)
        meaning_frame.grid_propagate(False)

        note="**Key bindings: <- for previous, -> for next, space to see meaning."
        note=tk.Label(self, text=note, fg="red")
        note.grid(row=4, column=1, columnspan=3)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # adding meaning text area
        tbscb = tk.Scrollbar(meaning_frame)
        tbscb.pack(side='right', fill='y')
        self.meaningtb=tk.Text(meaning_frame, width=60, height=17, wrap=tk.WORD)
        self.meaningtb.pack(side='left')
        self.meaningtb.config(state=tk.DISABLED)
        self.meaningtb.config(yscrollcommand=tbscb.set)
        tbscb.config(command=self.meaningtb.yview)

    def nextfunc(self):
        self.ptr += 1
        self.cleanup_textbox()
        try:
            word=self.lw[self.ptr]
            self.wlb.config(text=word)
        except:
            self.wlb.config(text="NO MORE WORDS !!")

    def prevfunc(self):
        self.ptr -= 1
        self.cleanup_textbox()
        try:
            word=self.lw[self.ptr]
            self.wlb.config(text=word)
        except:
            self.wlb.config(text="NO MORE WORDS !!")

    def cleanup_textbox(self):
        self.meaningtb.config(state=tk.NORMAL)
        self.meaningtb.delete('1.0', tk.END)
        self.meaningtb.config(state=tk.DISABLED)

    def meaningfunc(self):
        '''----------------
        1. enable state
        2. clear text area
        3. insert text
        4. disable state
        --------------------'''
        try:
            key=self.lw[self.ptr]
            meaning=self.dict[key]
            self.meaningtb.config(state=tk.NORMAL)
            self.meaningtb.delete('1.0', tk.END)
            self.meaningtb.insert('1.0', meaning)
            self.meaningtb.config(state=tk.DISABLED)
        except:
            self.meaningtb.insert('1.0', "No more words")






app = MainApplication()
app.geometry("1280x720")
app.mainloop()
