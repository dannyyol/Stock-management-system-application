from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import random
import time
import datetime
import sqlite3
import os
import random

def main():
    root = Tk()
    app = Inventory(root)


conn = sqlite3.connect("mystore.db")
c = conn.cursor()
create_inventory = "CREATE TABLE IF NOT EXISTS inventory(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, stock NUMERIC NOT NULL, cp NUMERIC NOT NULL, sp NUMERIC NOT NULL,\
    totalcp NUMERIC NOT NULL, totalsp NUMERIC NOT NULL, assumed_profit NUMERIC NOT NULL, vendor TEXT, vendor_phonenumber INTEGER)"
c.execute(create_inventory)
conn.commit()
conn.close

create_transactions = "CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT, inventory_id INTEGER, name TEXT, quantity INTEGER, amount INTEGER, date DATE)"
c.execute(create_transactions)
conn.commit()
conn.close


# Inventory lists like session
product_list =[]
product_price =[]
product_quantity= []
product_id= []

# list for labels
labels_list =[]
date = datetime.datetime.now().date()
class Inventory():
    
    def __init__(self, master):
        # variable
        checkvar = IntVar()
        E_discount = IntVar()


        def checkDiscount():
            if (checkvar.get()==1):
                self.discountE.configure(state=NORMAL)
                self.discountE.focus()
                self.discountC.delete('0', END)
                self.discountE.insert(END, "")
            elif(checkvar.get()==0):
                self.discountE.configure(state=DISABLED)
                self.discountE.insert(END, 0)
                
        def vProduct(event):
            global sd
            searchSd = self.listbox.curselection()[0]      
            sd = self.listbox.get(searchSd)
            
            self.enterIdE.delete(0,END)
            self.enterIdE.insert(END, sd[0])

        def change():
            # get the amount given by the custormer
            self.amount_given = float(self.changeE.get())
            self.out_total = float(sum(product_price))

            self.to_give = self.amount_given - self.out_total

            # label
            self.current_amount = Label(self.leftFrame, text="Change #: " + str(self.to_give), font=('arial 18 bold'), bg= "white" ,fg="red")
            self.current_amount.place(x=0,y=390)


        def ajax ():
            self.get_id = self.enterIdE.get()
            query = "SELECT * FROM inventory WHERE id=?"
            result = c.execute(query,(self.get_id,))
            for self.r in result:
                self.get_id = self.r[0]
                self.get_name = self.r[1]
                self.get_stock = self.r[2]
                self.get_price = self.r[4]

            self.productName.configure(text="Product Name: " + str(self.get_name))
            self.priceL.configure(text="Price #: " + str(self.get_price))
            
            # Create The quantity and discount label

            
            self.quantityL =  Label(self.leftFrame, text ="Enter Quantity", font=("arial 12 bold"), bg='lightblue')
            self.quantityL.place(x=0, y=220)

            self.quantityE =  Entry(self.leftFrame, width=32, bd=5, font=("arial 12 bold"), bg='lightblue')
            self.quantityE.place(x=137, y=220)
            self.quantityE.focus()

            self.discountC = Checkbutton(self.leftFrame, text='',  variable = checkvar,  onvalue=1, offvalue=0, font=('arial', 18, 'bold'), \
            bg='lightblue', command=checkDiscount).place(x=0, y=250)

            self.discountL =  Label(self.leftFrame, text ="Enter Discount", font=("arial 12 bold"), bg='lightblue')
            self.discountL.place(x=20, y=260)

            self.discountE =  Entry(self.leftFrame, width=31, textvariable = E_discount, bd=5, font=("arial 12 bold"), bg='lightblue',state = DISABLED)
            self.discountE.place(x=145, y=260)
            # self.discountE.insert(END, 0)

            # # Add to cart

            self.addtocartButton = Button(self.leftFrame, text="Add To Cart", width=22, height=2, bg='orange', command= addToCart)
            self.addtocartButton.place(x=272, y=300)

            # # generate bill and change
            self.changeL =  Label(self.leftFrame, text ="Given Amount", font=("arial 12 bold"), bg='lightblue')
            self.changeL.place(x=0, y=350)

            self.changeE =  Entry(self.leftFrame, width=32, bd=5, font=("arial 12 bold"), bg='powder blue')
            self.changeE.place(x=137, y=350)

            # # Button Change
            self.changeButton = Button(self.leftFrame, text="Calculate Change", width=22, height=2, bg='orange', command=change)
            self.changeButton.place(x=272, y=390)
            
            self.billButton = Button(self.leftFrame, text="Generate Bill", width=60, height=2, bg='red',fg="white", command=generate_bill)
            self.billButton.place(x=5, y=438)

            

            # ====================================

        def addToCart():
            # get the quantity and value from the database
            
            self.quantityValue = int(self.quantityE.get())
            if self.quantityValue > int(self.get_stock):
               tkinter.messagebox.showinfo("Error", "Not too many products in our database")
            else:
                # calculate the price
                self.final_price =( float(self.quantityValue) * float(self.get_price)) - (float(self.discountE.get()))
                product_list.append(self.get_name)
                product_price.append(self.final_price)
                product_quantity.append(self.quantityValue)
                product_id.append(self.get_id)
                DateofOrder = StringVar()
                
                # DateofOrder.set(time.strftime("%d-%m-%Y"))
                # f = open("Cart Items/"+DateofOrder.get()+'.'+'txt', "a+")
                # f.write("\n"+ self.get_name + "\t\t" + str(self.final_price) + "\t\t" + str(self.quantityValue))
                
                self.x_index=0
                self.y_index = 1
                self.y_i = 1000
                self.counter =0 

                self.label_1 = Label(self.frameCanvas, text='Product', font=('arial, 16 bold'), fg ='orange', bg="lightblue")
                self.label_1.grid(row= 0, column=0, sticky="ew", padx=(0,80))

                self.label_2 = Label(self.frameCanvas, text='Quality', font=('arial, 16 bold'), fg ='orange', bg="lightblue")
                self.label_2.grid(row= 0, column=1, padx=(0,80))

                self.label_3 = Label(self.frameCanvas, text='Price', font=('arial, 16 bold'),fg ='orange', bg="lightblue")
                self.label_3.grid(row= 0, column=2)
                
                
                # for i in range(20): 
                for self.p in product_list:
                    self.tempName = Label(self.frameCanvas, text=str(product_list[self.counter]), font=("arial 12 bold"), fg ="black", bg="lightblue")
                    self.tempName.grid(row=self.y_index, column=0, padx=(0,40))

                    labels_list.append(self.tempName)
                    
                    self.tempQuantity = Label(self.frameCanvas, text=str(product_quantity[self.counter]), font=("arial 12 bold"), fg ="black", bg="lightblue")
                    self.tempQuantity.grid(row=self.y_index, column=1, padx=(0,40))

                    labels_list.append(self.tempQuantity)
            
                    self.tempPrice = Label(self.frameCanvas, text=str(product_price[self.counter]), font=("arial 12 bold"), fg ="black", bg="lightblue")
                    self.tempPrice.grid(row=self.y_index, column=2)

                    labels_list.append(self.tempPrice)

                    self.totalL = Label(self.frameCanvas, text='', font=('arial, 18 bold'),fg ='orange', bg="lightblue")
                    self.totalL.grid(row= self.y_i, column=0, pady=(300,0))

                    self.master.bind("<Return>",ajax)
                    self.master.bind("<Up>", addToCart)
                    self.master.bind("<space>", generate_bill)

                    self.y_index += 1
                    self.x_index +=1
                    self.counter +=1
                   
                    self.totalL.configure(text="Total: #" + str(sum(product_price)))
                    
                    self.quantityL.place_forget()
                    self.quantityE.place_forget()
                    self.discountE.place_forget()
                    self.discountL.place_forget()
                    self.addtocartButton.destroy()
                    self.productName.configure(text="")
                    self.priceL.configure(text="")

                    # Autofocus to enter ID and delete
                    self.enterIdE.focus()
                    self.enterIdE.delete(0, END)
                    self.discountE.delete(0, END)
                    self.discountE.insert(END, 0)
                    
                self.y_i +=1

                
                 # put the frame in the canvas
                self.canvas.create_window(0, 0, anchor='nw', window=self.frameCanvas)
                # make sure everything is displayed before configuring the scrollregion
                self.canvas.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox('all'), yscrollcommand=self.scroll_y.set,xscrollcommand = self.scroll_x.set)
                self.canvas.grid(row=0, column=0)
                self.scroll_x.grid(row=1, column=0, sticky="ew")
                self.scroll_y.grid(row=0, column=1, sticky="ns")

        # generate bill and recreasing stock
        def generate_bill():
            # create the billbefore updating to database
            directory= "C:/Users/USER/Desktop/Python_Projects/Inventory/invoice/" + str(date) +"/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            # template
            company = "\t\t\t\tDannyyol Company PVt, Ltd,\n"
            address = "\t\t\t\tAdebayo,Adehun Ado-Ekiti\n"
            phone = "\t\t\t\t\t08032385253\n"
            sample = "\t\t\t\t\tInvoice\n"
            dt = "\t\t\t\t\t" +str(date)

            table_header = "\n\n\t\t\t----------------------------------------\n\t\t\tSN.\tProduct\t\tQty\t\tAmount\n\t\t\t----------------------------------------"
            final =company +address + phone + sample +dt + "\n" + table_header
            # open a file to write
            file_name = str(directory)+str(random.randrange(5000,10000)) + ".rtf"
            f = open(file_name, 'w')
            f.write(final)
            # fill items bought
            r=1
            i=0
            for t in product_list:
                f.write("\n\t\t\t" + str(r) + "\t" + str(product_list[i] + ".......")[:7] + "\t\t" +str(product_quantity[i]) + "\t\t" + str(product_price[i]))
                i += 1
                r += 1
            f.write("\n\n\t\t\tTotal:#"+str(sum(product_price)))
            f.write("\n\t\t\tThanks for visiting.")
            os.startfile(file_name, "print")
            f.close()
            # decrease the stock
            self.x = 0
        
            for t in product_list:
                initial = "SELECT * FROM inventory WHERE id =?"
                result = c.execute(initial, (product_id[self.x],))
                print("get: " + str(product_id[self.x]))
                for r in result:
                    self.old_stock = r[2]
                    
                self.new_stock = int(self.old_stock) - int(product_quantity[self.x])
                print("old stock: " + str(self.old_stock) + " newstock: " +(str(product_quantity[self.x])))
                sql = "UPDATE inventory SET stock=? WHERE id =?"
                c.execute(sql, (self.new_stock, product_id[self.x]))
                conn.commit()
                sql2 = "INSERT INTO transactions (inventory_id, name, quantity, amount, date) VALUES (?,?,?,?,?)"
                c.execute(sql2, (product_id[self.x], product_list[self.x], product_quantity[self.x], product_price[self.x], date))
                
                conn.commit()
                self.x +=1
            
            for a in labels_list:
                a.destroy()
            del(product_list[:])
            del(product_quantity[:])
            del(product_price[:])
            del(product_id[:])
            # self.current_amount.configure(text='')
            self.changeE.delete(0,END)
            self.enterIdE.focus()
            tkinter.messagebox.showinfo("Success", "Done everything smoothly")
        

        def loadAgain():
            self.listbox.delete(0, END)
            totalP = "SELECT count(*) FROM inventory"
            t= c.execute(totalP,)
            for totalR in t:
                tr = totalR[0]
            self.listbox.insert(END, "NUMBER OF ITEMS STRORED IS  " + str(tr), str())

            displayAll = "SELECT id, name, stock, cp, sp, totalcp, totalsp FROM inventory"
            resultD = c.execute(displayAll,)
            for r in resultD:
                self.listbox.insert(END, r, str())

        def clear():
            # self.productName.place_forget()
            for a in labels_list:
                a.destroy()
            del(product_list[:])
            del(product_quantity[:])
            del(product_price[:])
            del(product_id[:])
            self.totalL.configure(text="")

                
        # ++++++++++++++++++++++++++++++++++++calculator function===============
        text_input = StringVar()
        operator =""
            
        def btnClick(numbers):
            global operator
            operator =operator + str(numbers)
            text_input.set(operator)

        def btnClear():
            global operator
            operator =""
            text_input.set("")

        def btnEquals():
            global operator
            sumup =str(eval(operator))
            text_input.set(sumup)
            operator=""
        
        def openTrans():
            self.newWindow = Toplevel(self.master)
            self.master.withdraw()
            self.app = Transaction(self.newWindow)
            

        def openUpdate():
            self.newWindow = Toplevel(self.master)
            self.master.withdraw()
            self.app = UpdateToDatabase(self.newWindow)

        def fExit():
            iExit = tkinter.messagebox.askyesno("Exit Inventory System", "Confirm if you want to exit")
            if( iExit > 0):
                self.master.destroy()
                return

        

        self.master = master
        self.master.title("Inventory Management Systems")
        self.master.geometry('1350x750+0+0')
        self.master.configure(background= "Cadet Blue")
        self.frame = Frame(self.master)
        self.frame.pack()

        self.Tops =Frame(self.frame, bg= 'Cadet Blue', bd=20, pady=15, padx=25, relief=RIDGE)
        self.Tops.pack(side = TOP)
        self.labelTitle = Label(self.Tops, font =('arial', 60, 'bold'), text = "Inventory Managment Systems", bd=21, padx=30, bg='Cadet Blue', fg ='CornSilk', justify=CENTER)
        self.labelTitle.grid(row=0, column=0)

        self.rightFrame = Frame(self.frame, bd= 10, relief = GROOVE, height=500, bg="lightblue")
        self.rightFrame.pack(side = RIGHT)
        
        self.leftFrame = Frame(self.frame, bg = "lightblue", bd=10, relief= RIDGE, width=950, height=500)
        self.leftFrame.pack(side=LEFT)

        self.middleFrame = Frame(self.leftFrame, bg = 'Cadet Blue', bd =10, relief= RIDGE, width=430, height=500)
        self.middleFrame.pack(side = RIGHT)

        self.middleFrameTop = Frame(self.middleFrame, bg = 'Cadet Blue', relief= RIDGE, width=430, height=400)
        self.middleFrameTop.pack(side = BOTTOM)

        self.middleFrameListbox = Frame(self.middleFrameTop, bg = 'Cadet Blue', bd =10, relief= RIDGE, width=430, height=160)
        self.middleFrameListbox.pack(side = TOP)

        self.buttonFrame = Frame(self.middleFrameTop, bg = 'Cadet Blue', bd =5, relief = RIDGE, width=430, height=50)
        self.buttonFrame.pack(side= BOTTOM)

        self.calcFrame = Frame(self.middleFrameTop, bg= "Cadet Blue", bd=5, width=430, height=300)
        self.calcFrame.pack(side = TOP)


        self.leftFrameTop = Frame(self.leftFrame, bg= 'Powder Blue', bd=5, relief = RIDGE, width=550, height=100)
        self.leftFrameTop.pack(side=TOP)

        self.leftFrameBottom = Frame(self.leftFrame, bg= 'lightblue', relief = RIDGE, width=550, height=400)
        self.leftFrameBottom.pack(side=TOP)
       
        self.canvas = Canvas(self.rightFrame, width=409, height=455, bg="lightblue")  
        self.canvas.pack(side=BOTTOM)
        self.scroll_x = Scrollbar(self.rightFrame, orient= HORIZONTAL, command=self.canvas.xview)
        self.scroll_y = Scrollbar(self.rightFrame, orient="vertical", command=self.canvas.yview)


        self.frameCanvas = Frame(self.canvas,width=431,height=500, bg="lightblue")
        self.frameCanvas.pack(side=BOTTOM)
        
        #enter stuff
        self.enterId = Label(self.leftFrameTop, text="Enter Product's ID", font=('arial 16 bold'), bg='lightblue')
        self.enterId.grid(row=0, column=0)

        self.enterIdE = Entry(self.leftFrameTop, width=19,bd=5, font=('arial 16 bold'), bg='powder blue')
        self.enterIdE.grid(row=0, column=1)
        self.enterIdE.focus()

        self.searchBtn = Button(self.leftFrameTop, font=('arial, 10 bold'), text="Search", width=22,height=2, bg='orange', command=ajax)
        self.searchBtn.grid(row=1, column=1, pady=(5,10), sticky="E")

        self.productName = Label(self.leftFrameBottom, text='', font=('arial, 18 bold'), bg="lightblue", fg ='red')
        self.productName.grid(row=0, column=0, pady=(30,0))

        self.priceL = Label(self.leftFrameBottom, text='', font=('arial, 18 bold'), bg='lightblue', fg ='red')
        self.priceL.grid(row=1, column=0)

        # scroll
        self.scrollbar = Scrollbar(self.middleFrameListbox)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.listbox =Listbox(self.middleFrameListbox, width = 38, height=7, bg="Cadet Blue", fg= "white", bd=4, font=('arial', 12, 'bold'),\
            yscrollcommand=self.scrollbar.set)
            
        self.listbox.insert(0, "ID have reached up to: " + str(max_id))
        # self.txtReceipt.pack(side=RIGHT)
        self.listbox.bind('<<ListboxSelect>>', vProduct)
        self.listbox.grid(row=0, column=0, padx=0, ipadx=20)

        self.scrollbar.config(command= self.listbox.yview)

        #
        # ----------------------------------Button-------------------------------------
        # =========================Calculator---------------------------------------
        self.txtDisplay =Entry(self.calcFrame, width = 45, justify=RIGHT, bg="white", textvariable=text_input, bd=4, font=('arial', 12, 'bold'))
        self.txtDisplay.grid(row=0, column=0, columnspan=4, pady=1)
        self.txtDisplay.insert(0, "0")

        self.btn7 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '7', \
            bg='Cadet Blue', command= lambda:btnClick(7)).grid(row=2, column=0)

        self.btn8 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '8', \
            bg='Cadet Blue', command= lambda:btnClick(8)).grid(row=2, column=1)

        self.btn9 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '9', \
            bg='Cadet Blue', command= lambda:btnClick(9)).grid(row=2, column=2)

        self.btnAdd = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '+', \
            bg='Cadet Blue', command= lambda:btnClick("+")).grid(row=2, column=3)

        # ----------------------------------Button-------------------------------------
        self.btn4 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '4', \
            command= lambda:btnClick(4)).grid(row=3, column=0)

        self.btn5 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '5', \
            command= lambda:btnClick(5)).grid(row=3, column=1)

        self.btn6 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '6', \
            command= lambda:btnClick(6)).grid(row=3, column=2)

        self.btnSubstract = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '-', \
            bg='Cadet Blue', command= lambda:btnClick("-")).grid(row=3, column=3)
            # ----------------------------------Button-------------------------------------
        self.btn1 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '1', \
            command= lambda:btnClick(1)).grid(row=4, column=0)

        self.btn2 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '2', \
            command= lambda:btnClick(2)).grid(row=4, column=1)

        self.btn3 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '3', \
            command= lambda:btnClick(3)).grid(row=4, column=2)

        self.btnMultiplication = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '*', \
            bg='Cadet Blue', command= lambda:btnClick('*')).grid(row=4, column=3)

            # ----------------------------------Button-------------------------------------
        self.btn0 = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '0', \
            bg='Cadet Blue', command= lambda:btnClick(0)).grid(row=5, column=0)

        self.btnClear = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = 'C', \
            bg='Cadet Blue', command= btnClear).grid(row=5, column=1)

        self.btnEquals = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '=', \
            bg='Cadet Blue', command= btnEquals).grid(row=5, column=2)

        self.btnDiv = Button(self.calcFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 16, 'bold'), width=4, text = '/', \
            bg='Cadet Blue', command= lambda:btnClick("/")).grid(row=5, column=3)

# #########################

        self.accountButton = Button(self.buttonFrame, padx=16,pady=2, bd=7, fg= "black", font=('arial', 10, 'bold'), width=4, text = 'Account', \
            bg='Cadet Blue', command=openTrans).grid(row=0, column=1, sticky=W)
        
        self.addButton = Button(self.buttonFrame, padx=16,pady=2, bd=7, fg= "black", font=('arial', 10, 'bold'), width=4, text = 'Add', \
            bg='Cadet Blue', command=openUpdate).grid(row=0, column=2, sticky=W)
        
        self.reloadButton = Button(self.buttonFrame, padx=16,pady=2, bd=7, fg= "black", font=('arial', 10, 'bold'), width=4, text = 'Reload', \
            bg='Cadet Blue', command=loadAgain).grid(row=0, column=3, sticky=W)
        self.clearButton = Button(self.buttonFrame, padx=16,pady=2, bd=7, fg= "black", font=('arial', 10, 'bold'), width=4, text = 'Clear', \
            bg='Cadet Blue',command=clear).grid(row=0, column=4, sticky=W)
        
        self.exitButton = Button(self.buttonFrame, padx=16,pady=2, bd=7, fg= "black", font=('arial', 10, 'bold'), width=4, text = 'Exit', \
            bg='Cadet Blue', command= fExit).grid(row=0, column=5, sticky=W)

        # listbox display

        
result =c.execute("SELECT Max(id) from inventory")
for r in result:
    max_id = r[0]
    
class UpdateToDatabase():
    
    def search(self, *args, **kwargs):
        sql = "SELECT * FROM inventory WHERE id = ? OR name LIKE ?"
        # sql = "SELECT * FROM inventory WHERE( name LIKE '%'||?||'%')"
        search_result = c.execute(sql, (self.idEntry_6.get(), self.nameEntry_1.get()))
        for r in search_result:
            self.n1 = r[1]
            self.n2 = r[2]
            self.n3 = r[3]
            self.n4 = r[4]
            self.n5 = r[5]
            self.n6 = r[6]
            self.n7 = r[7]
            self.n8 = r[8]
            self.n9 = r[9]
            
        conn.commit()
        
        self.nameEntry_1.delete(0, END)
        self.stockEntry_2.delete(0, END)
        self.costpriceEntry_3.delete(0, END)
        self.sellingpriceEntry_4.delete(0, END)
        self.vendornameEntry_5.delete(0, END)
        self.vendorphonenumberEntry_6.delete(0, END)
        self.totalcpEntry_3.delete(0, END)
        self.totalspriceEntry_4.delete(0, END)
        

        self.nameEntry_1.insert(0, str(self.n1))
        self.stockEntry_2.insert(0, str(self.n2))
        self.costpriceEntry_3.insert(0, str(self.n3))
        self.sellingpriceEntry_4.insert(0, str(self.n4))
        #self.nameEntry_1.insert(0, str(self.n6))
        self.totalcpEntry_3.insert(0, str(self.n5))
        self.totalspriceEntry_4.insert(0, str(self.n6))
        self.vendornameEntry_5.insert(0, str(self.n8))
        self.vendorphonenumberEntry_6.insert(0, str(self.n9))
        
        # self.n1 = r[1]
    def ClearAll(self, *args, **kwargs):
        num = max_id + 1
        self.nameEntry_1.delete(0, END)
        self.stockEntry_2.delete(0, END)
        self.costpriceEntry_3.delete(0, END)
        self.sellingpriceEntry_4.delete(0, END)
        self.totalcpEntry_3.delete(0, END)
        self.totalspriceEntry_4.delete(0, END)
        self.vendornameEntry_5.delete(0, END)
        self.vendorphonenumberEntry_6.delete(0, END)
        self.idEntry_6.delete(0, END)


    def get_items(self, *args, **kwargs):

        self.name = self.nameEntry_1.get()
        self.stock = self.stockEntry_2.get()
        self.cp = self.costpriceEntry_3.get()
        self.sp = self.sellingpriceEntry_4.get()
        self.vendor = self.vendornameEntry_5.get()
        self.vendor_phone = self.vendorphonenumberEntry_6.get()

        if self.name =='' or float(self.stock=='') or float(self.cp=='') or float(self.sp==''):
            tkinter.messagebox.showinfo("Error", "Please fill all the entries")
        else:
            self.totalcp = float(self.cp) * float(self.stock)
            self.totalsp = float(self.sp) * float(self.stock)
            self.assumed_profit = float(self.totalsp - self.totalcp)
            sql = "INSERT INTO inventory(name, stock, cp, sp, totalcp, totalsp, assumed_profit, \
                vendor, vendor_phonenumber) VALUES(?,?,?,?,?,?,?,?,?)"
            c.execute(sql, (self.name, self.stock, self.cp, self.sp, self.totalcp,self.totalsp, self.assumed_profit, \
                self.vendor, self.vendor_phone))
            conn.commit()
            # self.txtReceipt.insert(END, "\n\nInserted " + str(self.name) +" into the database with " + str(self.idEntry_6.get()))
            tkinter.messagebox.showinfo("Success", str(self.name) +" added into the database with id " + str(self.idEntry_6.get()))
            self.reload()

    
    def update(self, *args, **kwargs):
        self .u1 = self.nameEntry_1.get()
        self .u2 = self.stockEntry_2.get()
        self .u3 = self.costpriceEntry_3.get()
        self .u4 = self.sellingpriceEntry_4.get()
        self .u5 = self.totalcpEntry_3.get()
        self .u6 = self.totalspriceEntry_4.get()
        self .u7 = self.vendornameEntry_5.get()
        self.u8 = self.vendorphonenumberEntry_6.get()

        query = "UPDATE inventory SET name = ?, stock=?, cp=?, sp=?, totalcp=?, totalsp=?, vendor=?, vendor_phonenumber=? WHERE id=?"
        c.execute(query, (self.u1,self.u2,self.u3,self.u4,self.u5,self.u6,self.u7,self.u8, self.idEntry_6.get()))
        conn.commit()
        tkinter.messagebox.showinfo("Success", "Update to database")
    

    def fExit(self, *args, **kwargs):
            iExit = tkinter.messagebox.askyesno("Exit Inventory System", "Confirm if you want to exit")
            if( iExit > 0):
                self.master.destroy()
                return
        
    def reload(self, *args, **kwargs):
        global tr
        self.txtReceipt.delete(0, END)
        totalP = "SELECT count(*) FROM inventory"
        t= c.execute(totalP,)
        for totalR in t:
            tr = totalR[0]
    
        self.txtReceipt.insert(0, "ID have reached up to: " + str(max_id) + ', (' + str(tr) +' Items stored in database)' + str(), str())

        query = "SELECT * FROM inventory"
        result = c.execute(query,)   
  
        for self.r in result:
            self.get_id = self.r[0]
            self.get_name = self.r[1]
            self.get_stock = self.r[2]
            self.get_cp = self.r[3]
            self.get_sp = self.r[4]
            self.get_totalcp = self.r[5]
            self.get_totalsp = self.r[6]
            self.get_vendor = self.r[7]
            self.get_vendorPhone = self.r[8]
            
            conn.commit()  
            
            self.txtReceipt.insert(END, self.r, str())
        
    def viewProduct(self, event):
        global sd
        searchSd = self.txtReceipt.curselection()[0]      
        sd = self.txtReceipt.get(searchSd)
        
        self.idEntry_6.delete(0,END)
        self.idEntry_6.insert(END, sd[0])
        self.nameEntry_1.delete(0,END)
        self.nameEntry_1.insert(END, sd[1])
     
        self.stockEntry_2.delete(0,END)
        self.stockEntry_2.insert(END, sd[2])

        self.costpriceEntry_3.delete(0,END)
        self.costpriceEntry_3.insert(END, sd[3])

        self.sellingpriceEntry_4.delete(0,END)
        self.sellingpriceEntry_4.insert(END, sd[4])
        self.totalcpEntry_3.delete(0,END)
        self.totalcpEntry_3.insert(END, sd[5])
        self.totalspriceEntry_4.delete(0,END)
        self.totalspriceEntry_4.insert(END, sd[6])

    def deleteProduct(self, *args, **kwargs):
        sql = "DELETE FROM inventory WHERE id =?"
        c.execute(sql, (self.idEntry_6.get(),))
        conn.commit()
        self.ClearAll()
        self.reload()
    
    def BackAgain(self, *args, **kwargs):
        self.newWindow = Toplevel(self.master)
        self.app = Inventory(self.newWindow)
        self.master.withdraw()
        
    def __init__(self, master):
        self.master = master
        self.master.title("Restaurant Management Systems")
        self.master.geometry('1350x750+0+0')
        self.master.configure(background= "Cadet Blue")
        self.frame = Frame(self.master, bg="Powder Blue")
        self.frame.pack()

        self.Tops =Frame(self.frame, bg= 'Cadet Blue', bd=20, padx=25, relief=RIDGE)
        self.Tops.pack(side = TOP)
        self.labelTitle = Label(self.Tops, font =('arial', 60, 'bold'), text = "Inventory Managment Systems", bd=21, padx=30, bg='Cadet Blue', fg ='CornSilk', justify=CENTER)
        self.labelTitle.grid(row=0, column=0)


        self.rightFrame = Frame(self.frame, bg ="powder blue", bd= 10, relief = GROOVE, width=400, height=500)
        self.rightFrame.pack(side = RIGHT)

        self.leftFrame = Frame(self.frame, bg = "Powder Blue", bd=10, relief= RIDGE, width=900, height=500)
        self.leftFrame.pack(side=LEFT)


        self.con = Frame(self.leftFrame, bg = "Powder Blue", bd=10, relief= RIDGE, width= 900)
        self.con.pack(side=TOP)

        self.btnFrame = Frame(self.leftFrame, bg = "Powder Blue", bd=5, relief= RIDGE, width= 500)
        self.btnFrame.pack(side=BOTTOM)
        
        # scroll
        self.scrollbar = Scrollbar(self.rightFrame)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.txtReceipt =Listbox(self.rightFrame, width = 47, height=24, bg="white", bd=4, font=('arial', 12, 'bold'),\
            yscrollcommand=self.scrollbar.set)
            
        self.txtReceipt.insert(0, "ID have reached up to: " + str(max_id))
        self.txtReceipt.bind('<<ListboxSelect>>', self.viewProduct)
        self.txtReceipt.grid(row=0, column=0, padx=0, ipadx=20)

        self.scrollbar.config(command= self.txtReceipt.yview)
        
       

        self.idLabel_6 = Label(self.con, font =('arial', 10, 'bold'),text = "Search Name", bd=21, bg='powder Blue', fg ='black')
        self.idLabel_6.grid(row=0, column=0, sticky=W)
        self.idEntry_6 = Entry(self.con, font =('arial', 10, 'bold'), bd=7, bg='white', insertwidth=2, justify= RIGHT, width=15)
        self.idEntry_6.grid(row=0, column=1, sticky=W)

        self.searchLabel_6 = Button(self.con, font =('arial', 10, 'bold'),text = "Search", bd=5, padx=15, bg='powder Blue', fg ='black', command=self.search) \
            .place(x=290, y=12)
        
        self.nameLabel_1 = Label(self.con, font =('arial', 10, 'bold'),text = "Product Name", bd=21, bg='powder Blue', fg ='black')
        self.nameLabel_1.grid(row=1, column=0, sticky=W)
        self.nameEntry_1 = Entry(self.con, font =('arial', 10, 'bold'), bd=7, bg='white', insertwidth=2, width=30)
        self.nameEntry_1.grid(row=1, column=1, sticky=W)

        self.stockLabel_2 = Label(self.con, font =('arial', 10, 'bold'),text = "Stock", bd=21, bg='powder Blue', fg ='black')
        self.stockLabel_2.grid(row=2, column=0, sticky=W)
        self.stockEntry_2 = Entry(self.con, font =('arial', 10, 'bold'), bd=7, bg='white', insertwidth=2, width=30)
        self.stockEntry_2.grid(row=2, column=1, sticky=W)

        self.costpriceLabel_3 = Label(self.con, font =('arial', 10, 'bold'),text = "Cost Price", bd=21, bg='powder Blue', fg ='black')
        self.costpriceLabel_3.grid(row=3, column=0, sticky=W)
        self.costpriceEntry_3 = Entry(self.con, font =('arial', 10, 'bold'), bd=7, bg='white', insertwidth=2, width=30)
        self.costpriceEntry_3.grid(row=3, column=1, sticky=W)

        self.sellingpriceLabel_4 = Label(self.con, font =('arial', 10, 'bold'),text = "Selling Price", bd=21, bg='powder Blue', fg ='black')
        self.sellingpriceLabel_4.grid(row=4, column=0, sticky=W)
        self.sellingpriceEntry_4 = Entry(self.con, font =('arial', 10, 'bold'), bd=7, bg='white', insertwidth=2,  width=30)
        self.sellingpriceEntry_4.grid(row=4, column=1, sticky=W)

        self.totalcprLabel_3 = Label(self.con, font =('arial', 10, 'bold'),text = " Total Cost Price", bd=21, bg='powder Blue', fg ='black')
        self.totalcprLabel_3.grid(row=5, column=0, sticky=W)
        self.totalcpEntry_3 = Entry(self.con, font =('arial', 10, 'bold'), bd=7, bg='white', insertwidth=2, width=30)
        self.totalcpEntry_3.grid(row=5, column=1, sticky=W)


        self.totalspLabel_4 = Label(self.con, font =('arial', 10, 'bold'),text = "Total Selling Price", bd=21, bg='powder Blue', fg ='black')
        self.totalspLabel_4.grid(row=6, column=0, sticky=W)
        self.totalspriceEntry_4 = Entry(self.con, font =('arial', 10, 'bold'), bd=7, bg='white', insertwidth=2,  width=30)
        self.totalspriceEntry_4.grid(row=6, column=1, sticky=W)

        self.vendornameLabel_5 = Label(self.con, font =('arial', 10, 'bold'),text = "Vendor Name", bd=21, bg='powder Blue', fg ='black')
        self.vendornameLabel_5.grid(row=0, column=2, sticky=W)
        self.vendornameEntry_5 = Entry(self.con, font =('arial', 10, 'bold'), bd=7, bg='white', insertwidth=2, width=30)
        self.vendornameEntry_5.grid(row=0, column=3)

        self.vendorphonenumberLabel_6 = Label(self.con, font =('arial', 10, 'bold'), text = "Vendor Phone Number",  bd=21, bg='powder Blue', fg ='black')
        self.vendorphonenumberLabel_6.grid(row=1, column=2, sticky=W)
        self.vendorphonenumberEntry_6 = Entry(self.con, font =('arial', 10, 'bold'), bd=7, bg='white', insertwidth=2, width=30)
        self.vendorphonenumberEntry_6.grid(row=1, column=3)

        self.addButton = Button(self.btnFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), width=4, text = 'Add', \
            bg='Powder Blue', command = self.get_items).grid(row=6, column=0)
        
        self.updateButton = Button(self.btnFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), width=4, text = 'Update', \
            bg='Powder Blue',command= self.update).grid(row=6, column=1)

        self.reloadButton = Button(self.btnFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), width=4, text = 'Reload', \
            bg='Powder Blue',command= self.reload).grid(row=6, column=2)
        
        self.clearButton = Button(self.btnFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), width=4, text = 'Clear', \
        bg='Powder Blue', command= self.ClearAll).grid(row=6, column=3)

        
        self.deleteButton = Button(self.btnFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), width=4, text = 'Delete', \
        bg='Powder Blue',command= self.deleteProduct).grid(row=6, column=4)

        self.backButton = Button(self.btnFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), width=4, text = 'Back', \
        bg='Powder Blue',command= self.BackAgain).grid(row=6, column=5)
        
        self.exitButton = Button(self.btnFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), width=4, text = 'Exit', \
            bg='Powder Blue', command=self.fExit).grid(row=6, column=6)
  

class Transaction():

    # exit function
    def fExit(self, *args, **kwargs):
        iExit = tkinter.messagebox.askyesno("Exit Inventory System", "Confirm if you want to exit")
        if( iExit > 0):
            self.master.destroy()
            return
    # Funtion
    def loadall(self, *args, **kwargs):
        
        add = []  
        records = self.treeview.get_children()
        self.treeview.delete(*self.treeview.get_children())
        search_date = self.dateEntry.get()
        query = "SELECT SUM(totalsp),SUM(assumed_profit) FROM inventory"
        result = c.execute(query,)
        for i in result:
            total_SP = i[0]
            T_assumed_profit = i[1]

        query = "SELECT SUM(amount) FROM transactions"
        totalAmount = c.execute(query,)
        for i in totalAmount:
            tamount_sold = i[0]
            
        query2 ="SELECT * FROM transactions"
        c.execute(query2,)
        data2 = c.fetchall()
        for r in data2:
            getId = r[1]
            getName=r[2]
            qty_sold = r[3]
            amount = r[4]
            date_sold = r[5]
            re = "SELECT id, name, stock, cp,sp, totalcp,sum(totalsp) FROM inventory WHERE id=?"    
            result = c.execute(re,(getId,)) 
            # inventory loop
       
            for i in result:
                getStock = i[2]
                getCP = i[3]
                getSP = i[4]
                
                remQty = getStock- qty_sold
                totalCP = getCP * qty_sold
                totalSP = getSP *qty_sold
                assumed_profit = totalSP - totalCP 
                
                add.append(assumed_profit)
                total_assumed_profit = T_assumed_profit - sum(add)
            self.treeview.insert('', 'end', text =getName, values =(qty_sold, amount,remQty, assumed_profit,date_sold))
            # self.treeview.delete('0', END)
            
            
            total_amount_pending = total_SP - tamount_sold
            self.totalamountE.configure(text=": #" + str(tamount_sold))
            self.totalamountremE.configure(text = ": #" + str(total_amount_pending))
            self.totalprofitassumedE.configure(text = ": #" + str(sum(add)))
            
            self.totalprofitpendingE.configure(text = ": #" + str(total_assumed_profit))

            

    
    def printDetails(self, *args, **kwargs):
        # self.treeview.delete('0', END)
        add = []  
        records = self.treeview.get_children()
        self.treeview.delete(*self.treeview.get_children())
        search_date = self.dateEntry.get()
        query = "SELECT SUM(totalsp),SUM(assumed_profit) FROM inventory"
        result = c.execute(query,)
        for i in result:
            total_SP = i[0]
            T_assumed_profit = i[1]

        query = "SELECT SUM(amount) FROM transactions WHERE date =?"
        totalAmount = c.execute(query,(search_date,))
        for i in totalAmount:
            tamount_sold = i[0]
        query ="SELECT * FROM transactions WHERE date =?"
        c.execute(query,(search_date,))
        data2 = c.fetchall()
        for r in data2:
            getId = r[1]
            getName=r[2]
            qty_sold = r[3]
            amount = r[4]
            date_sold = r[5]
            re = "SELECT id, name, stock, cp,sp, totalcp,sum(totalsp) FROM inventory WHERE id=?"    
            result = c.execute(re,(getId,)) 
            # inventory loop
            
            for i in result:
                getStock = i[2]
                getCP = i[3]
                getSP = i[4]
                remQty = getStock- qty_sold
                totalCP = getCP * qty_sold
                totalSP = getSP *qty_sold
                assumed_profit = totalSP - totalCP 
                add.append(assumed_profit)
                total_assumed_profit = T_assumed_profit - sum(add)
            self.treeview.insert('', 'end', text =getName, values =(qty_sold, amount,remQty, assumed_profit,date_sold), tags = ('even',))
            # self.treeview.delete('0', END)
            
                
            total_amount_pending = total_SP - tamount_sold
            self.totalamountE.configure(text=": #" + str(tamount_sold))
            self.totalamountremE.configure(text = ": #" + str(total_amount_pending))
            self.totalprofitassumedE.configure(text = ": #" + str(sum(add)))
            
            self.totalprofitpendingE.configure(text = ": #" + str(total_assumed_profit))
            
        
    def BackAgain(self, *args, **kwargs):
        self.newWindow = Toplevel(self.master)
        self.app = Inventory(self.newWindow)
        self.master.withdraw()
        

    def __init__(self, master):
                
        self.master = master
        self.master.title("Restaurant Management Systems")
        self.master.geometry('1350x750+0+0')
        self.master.configure(background= "Cadet Blue")
        self.frame = Frame(self.master, bg="Powder Blue")
        self.frame.pack()

        self.Tops =Frame(self.frame, bg= 'Cadet Blue', bd=20, padx=25, relief=RIDGE)
        self.Tops.pack(side = TOP)
        self.labelTitle = Label(self.Tops, font =('arial', 60, 'bold'), text = "Inventory Managment Systems", bd=21, padx=30, bg='Cadet Blue', fg ='CornSilk', justify=CENTER)
        self.labelTitle.grid(row=0, column=0)

        # default date on load
        dateV = StringVar()
        dateV.set(date)

        self.homeexitFrame = Frame(self.frame, bg="Powder Blue", relief= RIDGE)
        self.homeexitFrame.pack(side=TOP)
        self.mainFrame = Frame(self.frame, bg = "Powder Blue", relief=RIDGE)
        self.mainFrame.pack(side=BOTTOM)
        self.middleFrame = Frame(self.mainFrame, bg = "Powder Blue", relief=RIDGE)
        self.middleFrame.pack(side=TOP)
        self.middleFrame2 = Frame(self.mainFrame, bg = "Powder Blue", relief= RIDGE)
        self.middleFrame2.pack(side=BOTTOM)

        self.tableFrame = Frame(self.middleFrame2, bg = "Powder Blue", width=1000, bd=4, relief= RIDGE)
        self.tableFrame.pack(side=TOP)

        self.totalFrame = Frame(self.middleFrame2, bg = "Powder Blue", relief= RIDGE)
        self.totalFrame.pack(side=BOTTOM)


        self.backButtton = Button(self.homeexitFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), text = 'Back', \
            bg='Powder Blue', command= self.BackAgain).grid(row=0, column=0, padx=(0,1000))

        self.exitButtton = Button(self.homeexitFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), text = 'Exit', \
            bg='Powder Blue', command = self.fExit).grid(row=0, column=1)

        self.dateLabel = Label(self.middleFrame, font =('arial', 10, 'bold'),text = "Search Name", bd=21, bg='powder Blue', fg ='black')
        self.dateLabel.grid(row=1, column=0)
        self.dateEntry =Entry(self.middleFrame, font =('arial', 10, 'bold'), textvariable = dateV, bd=7, bg='white', insertwidth=2,  width=30)
        self.dateEntry.grid(row=1, column=1)
        
        self.searchButton = Button(self.middleFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), text = 'Search', \
            bg='Powder Blue', command = self.printDetails).grid(row=1, column=2)

        self.treeLabel = Label(self.middleFrame, text="Transactions & Details", font=("arial 25"), bg="powder blue")
        self.treeLabel.grid(rows=2, column=0, padx=(0,0))

        self.totalamountL = Label(self.totalFrame, font =('arial', 14, 'bold'),text = "Total Amount Sold", bd=21, bg='powder Blue', fg ='black')
        self.totalamountL.grid(row=1, column=0,sticky=EW)
        self.totalamountE =Label(self.totalFrame, font =('arial', 14, 'bold'), text="", bg='powder Blue')
        self.totalamountE.grid(row=1, column=1)

        self.reloadButtton = Button(self.totalFrame, padx=16,pady=1, bd=7, fg= "black", font=('arial', 12, 'bold'), text = 'Load All', \
            bg='Powder Blue', command=self.loadall).grid(row=1, column=2, padx=(200,200))

        self.totalprofitassumedL = Label(self.totalFrame, font =('arial', 14, 'bold'),text = "Total Profit Assumed", bd=21, bg='powder Blue', fg ='black')
        self.totalprofitassumedL.grid(row=1, column=3,sticky=E, padx=(0,0))
        self.totalprofitassumedE =Label(self.totalFrame, font =('arial', 14, 'bold'), text="", bg='powder Blue')
        self.totalprofitassumedE.grid(row=1, column=4,sticky=E)

        self.totalamountremL = Label(self.totalFrame, font =('arial', 14, 'bold'),text = "Total Amount Pending", bg='powder Blue', fg ='black')
        self.totalamountremL.grid(row=2, column=0,sticky=E)
        self.totalamountremE =Label(self.totalFrame, font =('arial', 14, 'bold'),text="", bg='powder Blue')
        self.totalamountremE.grid(row=2, column=1,sticky=W)

        self.totalprofitpendingL = Label(self.totalFrame, font =('arial', 14, 'bold'),text = "Total Profit Pending", bd=21, bg='powder Blue', fg ='black')
        self.totalprofitpendingL.grid(row=2, column=3,sticky=E)
        self.totalprofitpendingE =Label(self.totalFrame, font =('arial', 14, 'bold'), text="", bg='powder Blue')
        self.totalprofitpendingE.grid(row=2, column=4,sticky=E)

        # self.reloadButton = Button(self.totalFrame, padx=16,pady=2, bd=7, fg= "black", font=('arial', 10, 'bold'), width=4, text = 'Reload', \
        #     bg='Powder Blue').grid(row=1, column=3, sticky=W)

        self.style = ttk.Style()
        
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, justify=CENTER, font=('Calibri', 11)) # Modify
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of
        self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove

        self.treeview = ttk.Treeview(self.tableFrame, height=10, style="mystyle.Treeview",)
        self.treeview["columns"] = ("Item Name", "Quantity Sold", "Amount", \
            "Remaining Quantity", "Assumed Profit")
        self.treeview.column("#0", anchor=CENTER)
        self.treeview.column("#1")
        self.treeview.column("#2")
        self.treeview.column("#3")
        self.treeview.column("#4")
        self.treeview.column("#5")
        self.treeview.pack(fill='both', expand=True, side='left')

        self.scroll_y = ttk.Scrollbar(self.tableFrame, orient="vertical", command=self.treeview.yview)
        self.scroll_y.pack(fill='y', side='right')
        self.treeview.configure(yscrollcommand = self.scroll_y.set)
        self.treeview.heading('#0', text = "Item Name")
        self.treeview.heading('#1', text = "Qty Sold")
        self.treeview.heading('#2', text = "Amount")
        self.treeview.heading('#3', text = "Remaining Qty")
        self.treeview.heading('#4', text = "Assumed Profit")
        self.treeview.heading('#5', text = "Date")
        
        self.treeview.tag_configure('odd', background='#E8E8E8')
        # self.treeview.tag_configure('even', background='#DFDFDF')
        self.treeview.tag_configure('even', background='#fff')

        self.printDetails()
    
    
if __name__ == '__main__':
    main()