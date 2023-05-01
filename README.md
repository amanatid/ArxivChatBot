# ArxivChatBot

## **Short Intro**

We create an ArxivChatBot App  using Python/Tkinter, llama_index, Langchain and OpenAI  where  it is trained on a specific query, the number of files and a specific criterion. Also, we store the pdf files and their abstracts. This is  an extension of the repo ArxivTkinter. Our ChatBot is trained based on three parameters:
1. Search query
2. Number of files
3. Search criterion:
    - a)Relevance 
    - b)Last updated 
    - c)Submitt Date 
    
In addition, from the main menu, you can access the Arxiv browser 
and store the pdf papers and their abstracts. 



### **Quick Start**  
- Provide the api-key in the file keys.ini
- Run the ArxivChatBot.py
- Input Query,number of files and choose relevance, last updated or submitted date
- Train the ChatBot  by pressing button "Load Query for OpenAI "
- Exports the pdf files and their abstracts  in the directory papers using the menu 
  and pressing the button  "Load for produce files"

We are using the default chat model from OpenAI ChatGPT-4.

### Issues
It is a bit slow to load the files and train  along with the response from Chatbot engine.
Also, we tried to make a standalone Tkinter app  using auto_to_py.exe but it seems 
windows are poping up. This is possibly due to multithreading since  machine leanring
techniques are used.


### **References**
1. https://github.com/StanfordVL/arxivbot/
2. https://github.com/emptycrown/llama-hub/blob/main/loader_hub/papers/arxiv/
3. https://llamahub.ai/l/papers-arxiv

