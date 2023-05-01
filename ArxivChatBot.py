from llama_index import GPTSimpleVectorIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from base import ArxivReader_mod_search,ArxivReader_mod
import os
import openai
from tkinter import *
from configparser import ConfigParser
import webbrowser




#Read our config file and get colors
parser = ConfigParser()
parser.read("keys.ini")
api_key = parser.get('keys', 'api_key')

os.environ['OPENAI_API_KEY'] = str(api_key)


###load the reader
loader = ArxivReader_mod()

# GUI
root = Tk()
root.title("Chatbot")
root.geometry('750x890')

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

global index


# Send function
def send():
	global index
	txt.insert(END, "\n")
	send = "You: " + e.get()
	txt.insert(END, "\n" + send)

	user = e.get().lower()

	response = str(index.query(user))
	txt.insert(END, "\n")

######	response = response.replace('.', '\n')
	string = response.strip()
	txt.insert(END, f'\nBot:{string}')

	e.delete(0, END)

def load_query():
	 global documents, loader, ArxivReader_mod_search,ArxivReader_mod
	 query = str(entry_query.get())
	 max_query = int(entry_files.get())
	 dummy = radio_query.get()
	 if dummy == 'Relevance':
		 search_query_int = 0

	 if dummy == "LastUpdated":
		 search_query_int = 1

	 if dummy == "SubmittedDate":
		 search_query_int = 2

	 print(dummy)




	 documents = loader.load_data(search_query=query,
								  max_results= max_query,
								  search_criterion = search_query_int)
	 index = GPTSimpleVectorIndex.from_documents(documents)
	 index.save_to_disk('index.json')

#	 index = GPTSimpleVectorIndex.load_from_disk('index.json')


def produce_files():
	query =  str(entry_query.get())
	max_query = int(entry_files.get())
	loader1 = ArxivReader_mod_search()

	# set up the type of query
	dummy = str(radio_query.get())
	if dummy == 'Relevance':
		search_query_int = 0

	if dummy == "LastUpdated":
		search_query_int = 1

	if dummy == "SubmittedDate":
		search_query_int = 2


	loader1.load_data(search_query=query,
					  max_results=max_query, search_criterion = search_query_int)

def params():
	query = str(entry_query.get())
	max_query = int(entry_files.get())

def open_browser(e):
	webbrowser.open_new("http://arxiv.org")




my_frame = Frame(root)
my_frame.pack()

label_query = Label(my_frame, text="Query:",font=FONT)
label_query.grid(row=0,column=0,padx=(60,0))

entry_query = Entry(my_frame,font=FONT)
entry_query.grid(row=0,column=1)

load_button = Button(my_frame, text='Load Query for OpenAI',font=FONT, command= load_query )
load_button.grid(row=0,column=2)


load_button_produce = Button(my_frame, text='Load for Produce files',font=FONT, command= params )
load_button_produce.grid(row=1,column=2)

label_files =  Label(my_frame, text="No Files:",font=FONT)
label_files.grid(row=1,column=0,padx=(60,0))

entry_files = Entry(my_frame,font=FONT)
entry_files.grid(row=1,column=1)

MODE = [
	("Relevance", "Relevance"),
	("LastUpdated", "LastUpdated"),
	("SubmittedDate", "SubmittedDate")
]
radio_query= StringVar()
radio_query.set("Relevance")

search_criterion =  Label(my_frame, text="Search Criterion:",font=FONT)
search_criterion.grid(row=2,column=0)

i = 1
global radios
radios = [];
for text, mode in MODE:
	i = i + 1
	radio = Radiobutton(my_frame, text=text,font=FONT_BOLD,  variable=radio_query, value=mode)
	radio.grid(row=i, column=1,sticky=W)
	radios.append(radio)


my_frame1 = Frame(root)
my_frame1.pack(pady=(0,0))


label1 = Label(my_frame1 , bg=BG_COLOR,fg=TEXT_COLOR,text="Welcome",font=FONT_BOLD,pady=10, width=30, height=1)
label1.grid(row=0,column=0,columnspan=2)


my_scrollbar = Scrollbar(my_frame1, orient = VERTICAL)

txt = Text(my_frame1 , bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60, yscrollcommand= my_scrollbar.set )
txt.grid(row=1, column=0, columnspan=2,padx=0)

my_scrollbar.config(command = txt.yview)
my_scrollbar.grid(row=1, column=2 ,rowspan=10,  sticky=N+S+W)

# Set up Menu
my_menu = Menu(root)
root.configure(menu=my_menu)

options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Arxiv Papers", menu=options_menu)
options_menu.add_command(label= "Arxiv Browser ", command=lambda: open_browser(1) )
options_menu.add_command(label= "Produce Files ", command=produce_files )



#scrollbar = Scrollbar(txt)
#scrollbar.place(relheight=1, relx=0.974)


e = Entry(my_frame1, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)

send = Button(my_frame1 , text="Send", font=FONT_BOLD, bg=BG_GRAY,
			command=send).grid(row=2, column=1)




###create an index of the data for the AI to be able to read
global index
index =GPTSimpleVectorIndex.load_from_disk('index.json')




root.mainloop()
