#Import All Of The module
from tkinter import *
import sqlite3

root = Tk()
root.title("NOTE ORGANIZER")
root.geometry("690x480")
root.resizable(height=False,width=False)
root.configure(background='green')






#Working function

def EntryInNote():
    global BodyOfNote
    global TitleOfNote
    TitleOfNote = str(titleentry.get())
    BodyOfNote = str(textentry.get(1.0, END))
    titleentry.delete(0, END)
    textentry.delete(1.0, END)
    connect = sqlite3.connect('pass.db')
    c = connect.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS note (
            title text,
            note text
            )""")
    connect.commit()
    connect.close()

    if TitleOfNote != "":
        connect = sqlite3.connect('pass.db')
        c = connect.cursor()
    
        c.execute("INSERT INTO note VALUES (:title, :note)",
                 {
                     'title':TitleOfNote,
                     'note':BodyOfNote
                 }
                 )
        connect.commit()
        connect.close()
        textentry.insert(1.0, "                               .............Successfully saved.............")

    else:
        def delete():
            data=show_lable.get(ACTIVE)
            dataget=data[0:18]
            connect = sqlite3.connect('pass.db')
            c = connect.cursor()
            c.execute("DELETE from note WHERE oid= "+str(dataget))
            connect.commit()
            connect.close()

        def Show():
            global dataget
            data=show_lable.get(ACTIVE)
            dataget=data[0:18]
            def edit():
                connect = sqlite3.connect('pass.db')
                c = connect.cursor()
                c.execute ("""UPDATE note SET 
                          'title' =:header,
                          'note' =:noted
                           WHERE oid =:oidd""",
                           {
                               'header' : show_lable1.get(),
                               'noted' : show_lable2.get(1.0,END),
                               'oidd' : str(dataget)
                           }
                           
                )
                connect.commit()
                connect.close()
            connect = sqlite3.connect('pass.db')
            c = connect.cursor()
            c.execute("SELECT * FROM note WHERE oid ="+dataget)
            window2=Toplevel()
            window2.geometry("320x320")
            window2.resizable(height=FALSE,width=FALSE)
            window2.configure(background='#F6F5AA')
            new_window_button1=Button(window2, text='<< BACK', bg='#F6F5AA',font=('bold',10),fg='black', command=window2.destroy).grid(row=4,padx=(0,0),column=0)
            new_window_button2=Button(window2, text='EDIT', bg='#F6F5AA',font=('bold',10),fg='black', command=edit, width=10).grid(row=4,padx=(164,0),column=2)
            c.execute("SELECT * FROM note WHERE oid ="+dataget)
            all_record=c.fetchall()
            global print_record2
            print_record2=""
            for record in all_record:
                print_record2 += str(record[1])
            global header
            header =""
            for headers in all_record:
                header += str(headers[0])
            show_lable1=Entry(window2, font=("Helvetica", 12), bg='#f5f469', fg='black', justify=CENTER)
            show_lable1.grid(row=0, column=0, columnspan=3, ipadx=68)
            show_lable1.insert(0, header)
            show_lable2=Text(window2, font=("Comic Sans MS", 10), bg='#F6F5AA', fg='black', height=15, width=39, selectbackground="#545300", selectforeground='white')
            show_lable2.grid(row=1, column=0, columnspan=3)
            show_lable2.insert(1.0, print_record2)
            
            connect.commit()
            connect.close()


        window=Toplevel()
        window.geometry('500x480')
        window.resizable(height=FALSE,width=FALSE)
        window.configure(background='green')
        new_window_lbl=Label(window,bg='green', text="LIST OF YOUR NOTES", font=("bold", 16), fg='white').grid(row=0,column=0, padx=(48, 0),ipady=10,columnspan=3)
        new_window_button=Button(window, text='<< BACK', bg='green',font=('bold',10),fg='white', command=window.destroy, width=10).grid(row=2,padx=(22,0),column=0, pady=(0,0))
        opennote=Button(window,text='OPEN NOTE', bg='green',font=('bold',10),fg='white', command=Show, width=10).grid(row=2,column=1, padx=(0, 0), pady=(0,0) )
        connect = sqlite3.connect('pass.db')
        c = connect.cursor()
        c.execute("SELECT *, oid FROM note")
        all_record=c.fetchall()
        global print_record
        print_record=""
        show_lable=Listbox(window,font=('bold', 10), bg='#F6F5AA', fg='black', height=22, width=63, selectbackground='gold', selectforeground='black')
        show_lable.grid(row=1, column=0, columnspan=3,pady=5, padx=(28,0))
        d_b=Button(window,text='DELETE ID', bg='green',font=('bold',10),fg='white', command=delete, width=10).grid(row=2,column=2, padx=(0, 0), pady=(0,0) )
        for record in all_record:
            print_record = str(record[2])+"                 "+str(record[0])
            show_lable.insert(END, print_record)
        connect.commit()
        connect.close()






#GUI for button and labels
title=Label(root,text="NOTE ORGANIZER", font=("bold", 16), bg="green", fg="white", padx=262).grid(row=0, column=0, columnspan=2, pady=(30, 0))
subtitle=Label(root,text="Take or organize your importent note", font=1, bg="green", fg="white").grid(row=1, column=0, columnspan=2, pady=0, padx=(0, 0))

titlebutton=Button(root, text="TITLE :", bg="green", fg="white", font=("bold",11), width=10, height=0).grid(row=2, column=0, columnspan=1, pady=(30, 10), padx=20)
titleentry=Entry(root, bg="#F6F5AA", font=("bold",12), justify=CENTER)
titleentry.grid(row=2, column=1, columnspan=1, pady=(30, 10), ipadx=171, padx=(0,60))

textbutton=Button(root, text="NOTE :", bg="green", fg="white", font=("bold",11), width=10, height=0).grid(row=3, column=0, columnspan=1, pady=(0, 240))
textentry=Text(root, bg="#F6F5AA", font=1, height=15, width=58)
textentry.grid(row=3, column=1, columnspan=1, padx=(0,60), rowspan=2)

showthenote=Button(root, text="INSERT or SHOW", bg="green", fg="white", font=("bold",11), width=16, height=0, command=EntryInNote).grid(row=5, column=1, columnspan=1, pady=(9, 0), padx=(0,70))




#Run the main loop
root.mainloop()