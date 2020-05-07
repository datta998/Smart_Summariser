# Core Packages
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog
import os
import csv
import hashlib
# NLP Pkgs 
from spacy_summarization import text_summarizer
from gensim.summarization import summarize
from nltk_summarization import nltk_summarizer

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

a = dict()
b = dict()
def main_account_screen():
	global login_screen
	login_screen = Tk()
	login_screen.geometry("800x600")
	login_screen.title("Account Login")
	Top = Frame(login_screen)
	Top.pack(side=TOP, fill=X)
	Form = Frame(login_screen, height=100)
	Form.pack()

	label_title = Label(Top, text = "Enter the Login Details", font=('arial', 15), bg="#808080", bd=15)
	label_title.pack(fill=X)

	global username_verify
	global password_verify
	global username_login_entry
	global password_login_entry

	lbl_username = Label(Form, text = "Username:", font=('arial', 12), bd=15)
	lbl_username.grid(row=0)
	Label(Top, text="").pack()
		
	lbl_password = Label(Form, text="Password:",font=('arial',12), bd=15)
	lbl_password.grid(row=1)


	username_verify = StringVar()
	password_verify = StringVar()
	global username
	global password

	username_login_entry = Entry(Form, textvariable=username_verify, font=(1))
	username_login_entry.grid(row=0, column=1)
	password_login_entry = Entry(Form, textvariable=password_verify, show="*", font=(1))
	password_login_entry.grid(row=1, column=1)
		    
	Button(text="Login",command = login_verify, width=20, height=2, bd=5).place(x=350, y=200)
	Label(text="").pack()
	Button(text="Sign Up", height=2, width=20,command = register, bg="green", fg="white", bd=5).place(x=350, y=260)
	Button(text="Admin",height=2,width=20, command=admin_login,bd=5, bg="#ff5e57", fg="white").place(x=350,y=320)

	login_screen.mainloop()
	    


def login_verify():
	username1 = username_verify.get()
	password1 = password_verify.get()
	username_login_entry.delete(0, END)
	password_login_entry.delete(0, END)
	flag = False
	file_obj = open("acc_details1.csv", "r" )    
	file_reader = csv.reader(file_obj)
	for row in file_reader:
		if row[1] == username1:
			flag = True
			user_found = [row[1],row[2]]
			if user_found[1] == password1:
				start()
			else:	
				password_not_recognised()
				break
	if flag==False :
		user_not_found_screen()				
	file_obj.close()


def login_success():
    	global login_success_screen
    	login_success_screen = Toplevel(login_screen)
    	login_success_screen.title("Success")
    	login_success_screen.geometry("150x100")
    	Label(login_success_screen, text="Login Success").pack()
    	Button(login_success_screen, text="OK", command=delete_login_success).pack()

# Designing popup for login invalid password

def password_not_recognised():

	global password_not_recog_screen
	password_not_recog_screen = Toplevel(login_screen)
	password_not_recog_screen.title("UnSuccessful Login")
	password_not_recog_screen.geometry("150x100")
	Label(password_not_recog_screen, text="Invalid Password !").pack()
	Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

# Designing popup for user not found
 
def user_not_found_screen():
	global user_not_found_screen
	user_not_found_screen = Tk()
	user_not_found_screen.title("Unsuccessful Login")
	user_not_found_screen.geometry("150x100")	
	Label(user_not_found_screen, text="Invalid Username !").pack()
	Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Deleting popups

def delete_login_success():
	login_success_screen.destroy()


def delete_password_not_recognised():
	password_not_recog_screen.destroy()


def delete_user_not_found_screen():
	user_not_found_screen.destroy()


def delete_record():

	global username_verify_a_tb3
	global fullname_verify_a_tb3
	global tab3_ad
	un_tb3 = username_verify_a_tb3.get()
	fn_tb3 = fullname_verify_a_tb3.get() 
	index=find_pri(un_tb3,"Primary.txt") #fiindexrst checks if it exists or not
	if index == -1:
		label_unsuccess_del = Label(tab3_ad, text = "No  such valid Record !", font=('arial', 15), bg="#ff7675", bd=10)
		label_unsuccess_del.pack(fill=X)
	else: #if exists, then delete
		index=0
		with open("Primary.txt",'r+') as file:
			line=file.readline()	#reads one line
			while line: #while file is not empty
				words=line.split("|") #unpack
				if words[0]==un_tb3: #checks if there is match of PK and input
					file.seek(index,0) #move file pointer to beginning of that record
					file.write("*") #write * to indicate it doesnt exist
					break
				else: #if not found, then take next line pointer position and read nextline
					index=file.tell() #
					line=file.readline()
		label_success_del = Label(tab3_ad, text = "Successfully Deleted !", font=('arial', 15), bg="green", bd=10)
		label_success_del.pack(fill=X)






def search():
	global username_verify_a_tb2
	global fullname_verify_a_tb2
	global search_entry
	un_search = username_verify_a_tb2.get()
	fn_search = fullname_verify_a_tb2.get()
	index=find_sec(fn_search,un_search,"Secondary.txt")	#search it exists in secondary file first
	print(index)
	if index == -1:
		print("Not found")
	else:
		index=find_pri(un_search,"Primary.txt")	#search it in primary file if present then return address
		print("Address:",index)
		if index == -1:
			search_entry.insert(tk.END,"No Record !\n")
		else:
			search_entry.insert(tk.END,"Record Found !\n")
			with open("Record.txt",'r') as file1:
				file1.seek(index)	#seek(offset,from) from=0(beg),1(current),2(end) by default 0
				line=file1.readline()
				line=line.rstrip('\n')
				words=line.split("|")	#unpack
				search_entry.insert(tk.END,"FullName:"+words[0]+"\nUsername: "+words[1]+"\nCountry: "+words[4])




def find_pri(key,fname):	#searching for key
	with open(fname,'r') as file:
		for line in file:
			words=line.split("|")
			if(words[0]==key):	#search key i.e usn(PK)
					position=int(words[1]) 
					return position
			else:
				pass
	return -1

######## SECONDARY INDEX FILE ###############

def find_sec(key1,key2,fname):
	with open(fname,'r') as file:
		for line in file:
			line=line.rstrip('\n')
			words=line.split("|")
			if(words[0]==key1 and words[1]==key2):
				return (5)
			else:
				pass
	return -1


### CHECK if file is empty ############
def file_is_empty(fname): #function to check file is empty or not
	return os.stat(fname).st_size==0

##########################################
####FUCNTION TO SORT THE INDEX RECORDS ###
##########################################
def key_sort(fname):
	t=list()
	fin=open(fname,'r')
	for line in fin:
		line=line.rstrip('\n')
		words=line.split('|')
		t.append((words[0],words[1])) #0-key,1-other, sortin based on key.
		#print(t)
	fin.close()
	t.sort()
	with open("temp.txt",'w') as fout:
		for pkey,addr in t:
			pack=pkey+"|"+addr
			#print(pack)
			fout.write(pack+'\n')
	os.remove(fname)
	os.rename("temp.txt",fname)





# Implementing event on register button
def register_user():
	fullname_info = fullname_verify.get()
	username_info = username_verify.get()
	password_info = password_verify.get()
	gender_info = var.get()
	country_info = c.get()
	
	file = open ("acc_details1.csv", "a")
	file.write(fullname_info + "," + username_info + "," + password_info + "," + str(gender_info) + "," + country_info + "\n")

	file.close()

	label_success = Label(register_screen, text = "Registration is Successful!", font=('arial', 15), bg="green", bd=10)
	label_success.pack(fill=X)

	buff = fullname_info + "|" + username_info + "|" + password_info + "|" + str(gender_info) + "|" + country_info 
	file1 = open("Record.txt","a")
	pos=file1.tell()	#get position before writing for address
	file1.write(buff)
	file1.write("\n")
	#ADDING PRIMARY KEYS
	pri_rec=username_info+"|"+str(pos) #pack primary key and reference address
	file2 = open("Primary.txt",'a+')	#Primary key, USN
	file_empty=file_is_empty("Primary.txt")
	if file_empty: #empty file write directly. no sorting required
		file2.write(pri_rec)
		file2.write('\n')
		file2.close()
	else:
		file2.write(pri_rec)
		file2.write('\n')
		file2.close()
		key_sort("Primary.txt")
	#ADDING SECONDARY KEYS
	file3 = open("Secondary.txt",'a+')	#Primary key, USN
	file_empty=file_is_empty("Secondary.txt")
	sec_rec=fullname_info+"|"+username_info #pack secondary key and primary key. SK can repeat and address of secondary.
	if file_empty: #empty file write directly. no sorting required
		file3.write(sec_rec)
		file3.write('\n')
	#	file3.close()
	else:
		file3.write(sec_rec)
		file3.write('\n')
	#	file3.close()
		key_sort("Secondary.txt")




def create_user_admin():
	global tab1_ad
	fullname_info_a = fullname_verify_a.get()
	username_info_a = username_verify_a.get()
	password_info_a = password_verify_a.get()
	gender_info_a = var_a.get()
	country_info_a = c_a.get()
	####
	#username_login_entry.delete(0, END) 
	#password_login_entry.delete(0, END)
	####
	file_a = open ("acc_details1.csv", "a")
	file_a.write(fullname_info_a + "," + username_info_a + "," + password_info_a + "," + str(gender_info_a) + "," + country_info_a + "\n")

	file_a.close()

	label_success_a = Label(tab1_ad, text = "Registration is Successful!", font=('arial', 15), bg="green", bd=10)
	label_success_a.pack(fill=X)

	buff_a = fullname_info_a + "|" + username_info_a + "|" + password_info_a + "|" + str(gender_info_a) + "|" + country_info_a 
	file1_a = open("Record.txt","a")
	pos_a=file1_a.tell()	#get position before writing for address
	file1_a.write(buff_a)
	file1_a.write("\n")
	#ADDING PRIMARY KEYS
	pri_rec_a=username_info_a+"|"+str(pos_a) #pack primary key and reference address
	file2_a = open("Primary.txt",'a+')	#Primary key, USN
	file_empty_a=file_is_empty("Primary.txt")
	if file_empty_a: #empty file write directly. no sorting required
		file2_a.write(pri_rec_a)
		file2_a.write('\n')
		file2_a.close()
	else:
		file2_a.write(pri_rec_a)
		file2_a.write('\n')
		file2_a.close()
		key_sort("Primary.txt")
	#ADDING SECONDARY KEYS
	file3_a = open("Secondary.txt",'a+')	#Primary key, USN
	file_empty_a=file_is_empty("Secondary.txt")
	sec_rec_a=fullname_info_a+"|"+username_info_a #pack secondary key and primary key. SK can repeat and address of secondary.
	if file_empty_a: #empty file write directly. no sorting required
		file3_a.write(sec_rec_a)
		file3_a.write('\n')
		file3_a.close()
	else:
		file3_a.write(sec_rec_a)
		file3_a.write('\n')
		file3.close()
		key_sort("Secondary.txt")



def func_log():

	register_screen.destroy()
	main_account_screen()

def func_log_admin():
	admin_page.destroy()
	main_account_screen()

def register():
	login_screen.destroy()
	global register_screen
	register_screen = Tk()
	register_screen.title("Registration Page")
	register_screen.geometry("800x600")
	label_0 = Label(register_screen, text="Registration form",width=20,font=("bold", 20))
	label_0.place(x=90,y=53)

	global username_verify
	global password_verify
	global username_login_entry
	global password_login_entry
	global fullname_verify
	global var
	global c

	fullname_verify = StringVar()
	username_verify = StringVar()
	password_verify = StringVar()
	var = IntVar()
	c = StringVar()


	label_1 = Label(register_screen, text="FullName",width=20,font=("bold", 10))
	label_1.place(x=80,y=130)

	entry_1 = Entry(register_screen, textvariable=fullname_verify, font=(1))
	entry_1.place(x=240,y=130)

	label_2 = Label(register_screen, text="Username",width=20,font=("bold", 10))
	label_2.place(x=79,y=180)

	entry_2 = Entry(register_screen,textvariable=username_verify, font=(1))
	entry_2.place(x=240,y=180)

	label_3 = Label(register_screen, text="Password",width=20,font=("bold", 10))
	label_3.place(x=77,y=230)

	entry_3 = Entry(register_screen,textvariable=password_verify, show="*", font=(1))
	entry_3.place(x=240,y=230)

	label_4 = Label(register_screen, text="Gender",width=20,font=("bold", 10))
	label_4.place(x=70,y=290)
	var = IntVar()
	Radiobutton(register_screen, text="Male",padx = 5, variable=var, value=1).place(x=235,y=290)
	Radiobutton(register_screen, text="Female",padx = 20, variable=var, value=2).place(x=290,y=290)

	label_4 = Label(register_screen, text="Country",width=20,font=("bold", 10))
	label_4.place(x=72,y=345)

	list1 = ['India','USA','UK','Japan','Canada','Australia'];
	c=StringVar()
	droplist=OptionMenu(register_screen,c, *list1)
	droplist.config(width=15)
	c.set('  Select your Country') 
	droplist.place(x=240,y=340)
	"""
	label_4 = Label(register_screen, text="Programming",width=20,font=("bold", 10))
	label_4.place(x=85,y=330)
	var1 = IntVar()
	Checkbutton(register_screen, text="java", variable=var1).place(x=235,y=330)
	var2 = IntVar()
	Checkbutton(register_screen, text="python", variable=var2).place(x=290,y=330)
	"""
	Button(register_screen, text='Register', command=register_user,width=20, height=2, bg='green',fg='white',bd=5).place(x=260,y=440)
	Button(register_screen, text='Login', command=func_log,width=20, height=2,bd=5).place(x=260,y=490)
	
	register_screen.mainloop()


def admin_login():

	global label_admin_name
	global label_admin_pass
	global admin_entry
	global admin_pass_entry
	global admin_verify
	global admin_pass_verify
	global admin_login
	admin_verify = StringVar()
	admin_pass_verify = StringVar()


	login_screen.destroy()
	admin_login = Tk()
	admin_login.geometry("800x600")
	admin_login.title("Admin Login Page")
	
	top_admin = Frame(admin_login,width=800, height=100, bg="#3d3d3d")
	top_admin.pack(side=TOP)
	label_admin_title = Label(top_admin, text = "ADMIN LOGIN PAGE", font=('arial', 17), bg="#3d3d3d", fg="white")
	label_admin_title.place(x=315 , y=30)	

	label_admin_name = Label(admin_login,text="Admin",font=('arial', 12), bd=15)
	label_admin_name.place(x=163,y=190)
	admin_entry = Entry(admin_login,textvariable=admin_verify, font=(1))
	admin_entry.place(x=300,y=200)
	
	label_admin_pass = Label(admin_login,text="Password",font=('arial', 12), bd=15)
	label_admin_pass.place(x=160,y=268)
	admin_pass_entry = Entry(admin_login,textvariable=admin_pass_verify, show="*", font=(1))
	admin_pass_entry.place(x=300,y=280)

	Button(admin_login,text="Login",width=12,height=2, bd=5,command=admin_login_verify).place(x=350,y=350)

	admin_login.mainloop()


def admin_login_verify():
	
	admin_name = admin_entry.get()
	admin_pass = admin_pass_entry.get()
	flag = False
	file = open("admin.csv","r")

	#file.write(admin_name + "," + admin_pass +"\n")
	reader_admin = csv.reader(file)

	for ad in reader_admin:
		if ad[0] == admin_name:
			flag = True
			if ad[1] == admin_pass:
				admin_page()
			else:
				password_not_recognised()
				break

	if flag == False:
		user_not_found_screen()
	file.close()





def admin_page():

	admin_login.destroy()
	admin_page = Tk()
	admin_page.geometry("800x600")
	"""
	global lbl_username_tab4
	global username_login_entry_1_tab4
	global lbl_pass_tab4
	global passname_login_entry_1_tab4
	global username_verify_14
	global pass_verify_14
	global display_filename_tab4
	username_verify_14 = StringVar()
	pass_verify_14 = StringVar()
	"""
	global tab1_ad
	global tab3_ad
	tab_control_admin = ttk.Notebook(admin_page)
	tab1_ad = ttk.Frame(tab_control_admin)
	tab2_ad = ttk.Frame(tab_control_admin)
	tab3_ad = ttk.Frame(tab_control_admin)
	

	# ADD TABS TO NOTEBOOK
	tab_control_admin.add(tab1_ad, text=f'{"Add":^40s}')
	tab_control_admin.add(tab2_ad, text=f'{"Search":^40s}')
	tab_control_admin.add(tab3_ad, text=f'{"Delete":^40s}')
	 

	tab_control_admin.pack(expand=1, fill="both")
	"""
	display_details = ScrolledText(admin_page, height = 10)
	display_details.grid(row=0,column=0, columnspan=3,padx=5,pady=5)	


	display_file_btn = Button(admin_page, text="Display",command=search_file_user, width=12,bg='#03A9F4',fg='#fff')
	display_file_btn.grid(row=19, column=1)

	clear_file_btn = Button(admin_page, text="Reset", command=clear_text_file, width=12,bg='#03A9F4',fg='#fff')
	clear_file_btn.grid(row=27, column=1)
	"""

	global username_verify_a
	global password_verify_a
	global username_login_entry_a
	global password_login_entry_a	
	global fullname_verify_a
	global var_a
	global c_a

	fullname_verify_a = StringVar()
	username_verify_a = StringVar()
	password_verify_a = StringVar()
	var_a = IntVar()
	c_a = StringVar()


	label_1_a = Label(tab1_ad, text="FullName",width=20,font=("bold", 10))
	label_1_a.place(x=80,y=130)

	entry_1_a = Entry(tab1_ad, textvariable=fullname_verify_a, font=(1))
	entry_1_a.place(x=240,y=130)

	label_2_a = Label(tab1_ad, text="Username",width=20,font=("bold", 10))
	label_2_a.place(x=79,y=180)

	entry_2_a = Entry(tab1_ad,textvariable=username_verify_a, font=(1))
	entry_2_a.place(x=240,y=180)

	label_3_a = Label(tab1_ad, text="Password",width=20,font=("bold", 10))
	label_3_a.place(x=77,y=230)

	entry_3_a = Entry(tab1_ad,textvariable=password_verify_a, show="*", font=(1))
	entry_3_a.place(x=240,y=230)

	label_4_a = Label(tab1_ad, text="Gender",width=20,font=("bold", 10))
	label_4_a.place(x=70,y=290)
	var_a = IntVar()
	Radiobutton(tab1_ad, text="Male",padx = 5, variable=var_a, value=1).place(x=235,y=290)
	Radiobutton(tab1_ad, text="Female",padx = 20, variable=var_a, value=2).place(x=290,y=290)

	label_4 = Label(tab1_ad, text="Country",width=20,font=("bold", 10))
	label_4.place(x=72,y=345)

	list1_a = ['India','USA','UK','Japan','Canada','Australia'];
	c_a=StringVar()
	droplist_a=OptionMenu(tab1_ad,c_a, *list1_a)
	droplist_a.config(width=15)
	c_a.set('  Select your Country') 
	droplist_a.place(x=240,y=340)
	"""
	label_4 = Label(register_screen, text="Programming",width=20,font=("bold", 10))
	label_4.place(x=85,y=330)
	var1 = IntVar()
	Checkbutton(register_screen, text="java", variable=var1).place(x=235,y=330)
	var2 = IntVar()
	Checkbutton(register_screen, text="python", variable=var2).place(x=290,y=330)
	"""
	Button(tab1_ad, text='Create', command=create_user_admin,width=20, height=2, bg='green',fg='white',bd=5).place(x=260,y=440)
	Button(tab1_ad, text='Log Out', command=func_log_admin,width=20, height=2, bg='#03A9F4',fg='#fff',bd=5).place(x=260,y=500)
	
	#SEARCH TAB
	global username_verify_a_tb2
	global fullname_verify_a_tb2
	global search_entry

	username_verify_a_tb2 = StringVar()
	fullname_verify_a_tb2 = StringVar()
	label_un = Label(tab2_ad, text="Username",width=20,font=("bold", 10))
	label_un.place(x=80,y=60)

	entry_un = Entry(tab2_ad, textvariable=username_verify_a_tb2, font=(1))
	entry_un.place(x=240,y=60)

	label_name = Label(tab2_ad, text="FullName",width=20,font=("bold", 10))
	label_name.place(x=80,y=100)

	entry_name = Entry(tab2_ad,textvariable=fullname_verify_a_tb2, font=(1))
	entry_name.place(x=240,y=100)
	
	search_entry = ScrolledText(tab2_ad,height=15, width=760)# Initial was Text(window)
	search_entry.place(x=15, y=140) 

	Button(tab2_ad, text="Search", command=search, width=20, height=2,bd=5).place(x=250, y=400)

	#DELETE TAB
	global username_verify_a_tb3
	global fullname_verify_a_tb3
	global delete_entry

	username_verify_a_tb3 = StringVar()
	fullname_verify_a_tb3 = StringVar()
	label_un3 = Label(tab3_ad, text="Username",width=20,font=("bold", 10))
	label_un3.place(x=80,y=60)

	entry_un3 = Entry(tab3_ad, textvariable=username_verify_a_tb3, font=(1))
	entry_un3.place(x=240,y=60)

	label_name3 = Label(tab3_ad, text="FullName",width=20,font=("bold", 10))
	label_name3.place(x=80,y=100)

	entry_name3 = Entry(tab3_ad,textvariable=fullname_verify_a_tb3, font=(1))
	entry_name3.place(x=240,y=100)
	


	Button(tab3_ad, text="Delete", command=delete_record, width=20, height=2,bd=5).place(x=250, y=400)


	admin_page.mainloop()





def start():
	login_screen.destroy()
	window = Tk()
	window.title("Smart_Summarizer")
	window.geometry("800x700")

	# TAB LAYOUT
	tab_control = ttk.Notebook(window)
	
	tab1 = ttk.Frame(tab_control)
	tab2 = ttk.Frame(tab_control)
	tab3 = ttk.Frame(tab_control)
	tab4 = ttk.Frame(tab_control)

	# ADD TABS TO NOTEBOOK
	tab_control.add(tab1, text=f'{"Home":^40s}')
	tab_control.add(tab2, text=f'{"File":^40s}')
	tab_control.add(tab3, text=f'{"URL":^40s}')
	tab_control.add(tab4, text=f'{"Display":^40s}') 

	tab_control.pack(expand=1, fill="both")

	#HOME TAB
	Top1 = Frame(tab1,width=800, height=200, bg="#3d3d3d")
	Top1.pack(side=TOP)
	label_title1 = Label(Top1, text = "Smart-Summariser", font=('arial', 17), bg="#3d3d3d", fg="white")
	label_title1.place(x=300 , y=80)
	Top1.pack_propagate(False)
	Bottom_left = Frame(tab1, width=400, height=500, bg="#4b4b4b")
	Bottom_left.pack(side=LEFT)
	label_title2 = Label(Bottom_left, text = "ABOUT:\n\nThis is a desktop application which is developed\nusing tkinter. It is used to Summarise\nlarge documents, websites, etc.", font=('arial', 10), bg="#4b4b4b", fg="white")
	label_title2.place(x=100, y=550)
	Bottom_left.pack_propagate(False)
	Bottom_right = Frame(tab1, width=400, height=500, bg="#bdc3c7")
	Bottom_right.pack(side=RIGHT)
	#btn_logout = Button(Bottom_right, text="Logout", command=main_account_screen(),bg='#03A9F4',fg='#fff')
	#btn_logout.place(x=100,y=100)
	#Bottom_right.pack_propagate(False)
	
	#FILE TAB
	l1=Label(tab2,text="Open File To Summarize")
	l1.grid(row=1,column=1)
	global displayed_file
	global window_display_text
	displayed_file = ScrolledText(tab2,height=7)# Initial was Text(window)
	displayed_file.grid(row=2,column=0, columnspan=3,padx=5,pady=3)

	# BUTTONS FOR SECOND TAB/FILE READING TAB
	b0=Button(tab2,text="Open File", width=12,command=openfiles,bg='#03A9F4',fg='#fff')
	b0.grid(row=3,column=1,padx=10,pady=10)

	b1=Button(tab2,text="Reset ", width=12,command=clear_text_file,bg='#03A9F4',fg='#fff')
	b1.grid(row=5,column=1,padx=10,pady=10)

	b2=Button(tab2,text="Summarize", width=12,command=get_file_summary,bg='#ff5252',fg='#fff')
	b2.grid(row=4,column=1,padx=10,pady=10)

	#b3=Button(window,text="Clear Result", width=12,command=clear_text_result, bg='#03A9F4',fg='#fff')
	#b3.grid(row=3,column=2,padx=10,pady=10)

	#b4=Button(window,text="Close", width=12,command=window.destroy)
	#b4.grid(row=5,column=2,padx=10,pady=10)


	# Display Screen
	window_display_text = ScrolledText(tab2,height=10)
	window_display_text.grid(row=10,column=0, columnspan=3,padx=5,pady=5)

	# Allows you to edit
	window_display_text.config(state=NORMAL)
	
	#Create File
	#l2=Label(window,text="Create File")
	#l2.grid(row=13,column=0)
	#global fname
	#fname = StringVar()
	#global file_entry_var
	#file_entry_var = StringVar()
	"""create_file_entry = Text(window,height=1 )
	create_file_entry.grid(row=14,column=1)
	#global filename
	
	b5=Button(window,text="Create File", width=12, bg='#03A9F4',fg='#fff')
	b5.grid(row=15,column=1,padx=10,pady=10)
	"""
	global filename_login_entry
	global username_login_entry_1
	global filename_verify
	global username_verify
	global password_verify
	global username_login_entry
	global password_login_entry
	global username_verify_1
	global pass_verify_1
	global passname_login_entry_1
	filename_verify = StringVar()
	username_verify_1 = StringVar()
	pass_verify_1 = StringVar()

	lbl_filename = Label(tab2, text = "File Name: ", font=('arial', 12), bd=15)
	lbl_filename.grid(row=13, column=0)
	filename_login_entry = Entry(tab2, textvariable=filename_verify, font=(1))
	filename_login_entry.grid(row=13, column=1)

	lbl_username = Label(tab2, text = "User Name: ", font=('arial', 12), bd=15)
	lbl_username.grid(row=14, column=0)
	username_login_entry_1 = Entry(tab2, textvariable=username_verify_1, font=(1))
	username_login_entry_1.grid(row=14, column=1)
	
	lbl_pass = Label(tab2, text = "Password: ", font=('arial', 12), bd=15)
	lbl_pass.grid(row=18, column=0)
	passname_login_entry_1 = Entry(tab2, textvariable=pass_verify_1, show="*",font=(1))
	passname_login_entry_1.grid(row=18, column=1)
	
	"""
	lbl_username = Label(window, text = "User Name: ", font=('arial', 12), bd=15)
	lbl_username.grid(row=18, column=0)
	username_login_entry_1 = Entry(window, textvariable=username_verify_1, font=(1))
	username_login_entry_1.grid(row=18, column=1)
	"""
	#password_login_entry = Entry(window, textvariable=password_verify, show="*", font=(1))
	#password_login_entry.grid(row=1, column=1)
  	#Button(text="Register", height="2", width="30",command = register_user, bg="red")
	#global fn
	#fn = filename_verify.get()
	btn_create = Button(tab2, text="Create File", width=20, height=2, command=create_file)
	btn_create.grid(row=20,column=1)
	btn_display = Button(tab2, text="Search File", width=20, height=2, command=search_file)
	btn_display.grid(row=20,column=2)


	# URL TAB

	global url_entry
	global url_display
	global tab3_display_text

	l1=Label(tab3,text="Enter URL To Summarize")
	l1.grid(row=1,column=0)

	raw_entry=StringVar()
	url_entry=Entry(tab3,textvariable=raw_entry,width=50)
	url_entry.grid(row=1,column=1)

	# BUTTONS
	button1=Button(tab3,text="Reset",command=clear_url_entry, width=12,bg='#03A9F4',fg='#fff')
	button1.grid(row=4,column=0,padx=10,pady=10)

	button2=Button(tab3,text="Get Text",command=get_text, width=12,bg='#03A9F4',fg='#fff')
	button2.grid(row=4,column=1,padx=10,pady=10)

	button3=Button(tab3,text="Clear Result", command=clear_url_display,width=12,bg='#03A9F4',fg='#fff')
	button3.grid(row=5,column=0,padx=10,pady=10)

	button4=Button(tab3,text="Summarize",command=get_url_summary, width=12,bg='#ff5252',fg='#fff')
	button4.grid(row=5,column=1,padx=10,pady=10)

	# Display Screen For Result
	url_display = ScrolledText(tab3,height=10)
	url_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


	tab3_display_text = ScrolledText(tab3,height=10)
	tab3_display_text.grid(row=10,column=0, columnspan=3,padx=5,pady=5)

	# DISPLAY TAB

	global lbl_username_tab4
	global username_login_entry_1_tab4
	global lbl_pass_tab4
	global passname_login_entry_1_tab4
	global username_verify_14
	global pass_verify_14
	global display_filename_tab4
	username_verify_14 = StringVar()
	pass_verify_14 = StringVar()
	lbl_username_tab4 = Label(tab4, text = "User Name: ", font=('arial', 12), bd=15)
	lbl_username_tab4.grid(row=14, column=0)
	username_login_entry_1_tab4 = Entry(tab4, textvariable=username_verify_14, font=(1))
	username_login_entry_1_tab4.grid(row=14, column=1)
	
	lbl_pass_tab4 = Label(tab4, text = "Password: ", font=('arial', 12), bd=15)
	lbl_pass_tab4.grid(row=18, column=0)
	passname_login_entry_1_tab4 = Entry(tab4, textvariable=pass_verify_14, show="*",font=(1))
	passname_login_entry_1_tab4.grid(row=18, column=1)

	display_file_btn = Button(tab4, text="Display",command=search_file_user, width=12,bg='#03A9F4',fg='#fff')
	display_file_btn.grid(row=19, column=1)

	display_filename_tab4 = ScrolledText(tab4,height=20,font=12)
	display_filename_tab4.grid(row=25,column=0, columnspan=3,padx=5,pady=3)

	clear_file_btn = Button(tab4, text="Reset", command=clear_text_file, width=12,bg='#03A9F4',fg='#fff')
	clear_file_btn.grid(row=27, column=1)

	window.mainloop()




# Clear entry widget
def clear_text():
	entry.delete('1.0',END)

def clear_display_result():
	tab1_display.delete('1.0',END)
	tab4_display.delete('1.0',END)


# Clear Text  with position 1.0
def clear_text_file():
	displayed_file.delete('1.0',END)
	window_display_text.delete('1.0',END)
	filename_login_entry.delete(0,END)
	username_login_entry_1.delete(0,END)
	passname_login_entry_1.delete(0,END)
	display_filename_tab4.delete('1.0',END)
	username_login_entry_1_tab4.delete(0,END)
	passname_login_entry_1_tab4.delete(0,END)
	#tab2_display_text.delete('1.0',END)
	#passname_login_entry_1.delete(0,END)
	#passname_login_entry_1.delete('1.0',END)
	
# Clear Result of Functions
def clear_text_result():
	tab2_display_text.delete('1.0',END)

# Clear For URL
def clear_url_entry():
	url_entry.delete(0,END)

def clear_url_display():
	tab3_display_text.delete('1.0',END)
	url_display.delete('1.0',END)


# Clear entry widget
def clear_compare_text():
	entry1.delete('1.0',END)

def clear_compare_display_result():
	tab1_display.delete('1.0',END)


# Functions for TAB 2 FILE PROCESSER
# Open File to Read and Process
def openfiles():
	file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files",".txt"),("All files","*")))
	read_text = open(file1).read()
	displayed_file.insert(tk.END,read_text)


def create_file():
	global fn
	global un
	global pw
	global hv
	global up
	fn = filename_verify.get()
	un = username_verify_1.get()
	pw = pass_verify_1.get()
	file2 = open("files.csv",'a')
	up = un + pw
	up_hash = hash_func(up)
	b[up_hash] = fn
	file2.write(up_hash + "," + fn + "\n")
	file2.close() 
	
	raw_text_1 = window_display_text.get('1.0',tk.END)
	file3 = open(fn,"w")
	file3.write(raw_text_1)
	file3.close()

	
	fn_un_pw = fn+un+pw
	hv = hash_func(fn_un_pw)
	a[hv] = fn
	file_dict = open("dict.csv","a")
	file_dict.write(hv + "," + fn + "\n")
	file_dict.close()

def search_file():
	global fn_1
	global un_1
	global pw_1
	global key
	a.clear()
	fn_1 = filename_verify.get()
	un_1 = username_verify_1.get()
	pw_1 = pass_verify_1.get()
	fn_un_pw_1 = fn_1 + un_1 + pw_1
	key = hash_func(fn_un_pw_1)
	file_dict = open("dict.csv","r")
	file_reader_1 = csv.reader(file_dict)
	for row in file_reader_1:
		a[row[0]] = row[1]

	if key in a.keys(): 
		f_name = a[key] 
		read_text_1 = open(f_name).read()
		window_display_text.insert(tk.END,read_text_1)
	else: 
		read_text_2 = "File Not Found !"
		window_display_text.insert(tk.END,read_text_2) 
	"""
	file_dict_read = open("dict.csv", "r" )    
	file_reader_1 = csv.reader(file_dict_read)
	

	for row in file_reader_1:
		if row[0] == key:
			hash_found = [row[0],row[1]]
			f_name = hash_found[1]
			#read_text_1 = key + "\n" + hv
			read_text_1 = open(f_name).read()
			window_display_text.insert(tk.END,read_text_1)
		else:
			read_text_2 = "File Not Found !"
			window_display_text.insert(tk.END,read_text_2)
	"""


	"""
	st_1 = ""
	for i in fn_1:
		st_1 = st_1 + str(ord(i))
	hash_value = hash(st_1)
	#hash_value = hash(fn_1)
	f_name = a[hash_value]
	
	"""

def search_file_user():
	global un_2
	global pw_2
	global username_verify_14
	global pass_verify_14
	count_files = 0
	un_2 = username_verify_14.get()
	pw_2 = pass_verify_14.get()
	un_pw = un_2 + pw_2
	un_pw_hash = hash_func(un_pw)
	file_user = open("files.csv","r")
	file_reader_2 = csv.reader(file_user)
	for row in file_reader_2:
		b[row[0]] = row[1]
	file_user.close()

	with open(r"C:\Users\Welcome\Music\fs project myself\files.csv","rt") as f1:
		data1 = csv.reader(f1)
		for row in data1:
			if row[0] == un_pw_hash:
				count_files+=1
				new_line = str(count_files)+str(".")+row[1]+str("\n")
				display_filename_tab4.insert(tk.END,new_line)
		if count_files==0:
			no_file = "No Files Found !"
			display_filename_tab4.insert(tk.END,no_file)
	"""
	for row_file in file_reader_2:
		if un_pw_hash == row_file[0]:
			count_files = count_files + 1
			f_name3 = count_files + ". " + b[un_pw_hash] + "\n"
		display_filename_tab4.insert(tk.END,"hey")
		else:
			read_text5 = "No files Found"
			display_filename_tab4.insert(tk.END,read_text5)	
	"""
	"""
	if un_pw_hash in b.keys():
			display_filename_tab4.insert(tk.END,b[un_pw_hash])
	else:
			display_filename_tab4.insert(tk.END,"No files !")
	"""
def hash_func(f_name1):
	s = ""
	for i in f_name1:
		s = s + str(ord(i))
	#a[s] = f_name1
	return(s)


def display_file():
	u = username_verify_11.get()
	file3 = open("files.csv", "r" )    
	file_read = csv.reader(file3)
	for row in file_read:
		if row[0] == u:
			user_found = [row[0],row[1]]
			result = user_found[1] 
			window_display_text.insert(tk.END,row)						
	file3.close()


def get_file_summary():
	raw_text = displayed_file.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	window_display_text.insert(tk.END,result)

# Fetch Text From Url
def get_text():
	raw_text = str(url_entry.get())
	page = urlopen(raw_text)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	url_display.insert(tk.END,fetched_text)

def get_url_summary():
	raw_text = url_display.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab3_display_text.insert(tk.END,result)	


# COMPARER FUNCTIONS

def use_spacy():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSpacy Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def use_nltk():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = nltk_summarizer(raw_text)
	print(final_text)
	result = '\nNLTK Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def use_gensim():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = summarize(raw_text)
	print(final_text)
	result = '\nGensim Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def use_sumy():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSumy Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)


main_account_screen()


