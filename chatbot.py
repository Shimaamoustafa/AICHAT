from tkinter import *
import json
from difflib import get_close_matches
from tkinter import simpledialog

# The with statement ensures that the file is properly closed after its suite finishes, even if an exception is raised. This is a context manager that handles opening and closing the file.
def load_knowledge_base(file_path: str) -> dict: #Reading from the knowledge Base returns a dictionary
    with open(file_path, 'r') as file:  # opening json file (file_path) and giving it reading access 'r'
        data: dict = json.load(file)  # my data will be a Dictionary that will be filled from the json file
    return data

def save_knowledge_base(file_path: str, data: dict): #writing new Knowledge in the Knowledge Base it takes json file path and data as a Dictionary (Question and its answer)
    with open(file_path, 'w') as file:  # opening json file (file_path) and giving it writing access 'w'
        json.dump(data, file, indent=2)  # This line uses the json.dump function from the json module to write the dictionary data to the file.

def find_best_match(user_question: str, questions: list[str]) -> str | None: # take User Question And Compare it to The Questions in the Knowledge Base Return Matches or None
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.8)  # Make List of matches and with similarity with cutoff = 0.6
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def process_user_input():
    user_question = user_input_text.get("1.0", END).lower().strip()#بترجع الي دخله اليوسر من من الاول للاخر مع حزف اي مسافه
    if not user_question:
        return#تتاكد لو كان المستخدم مدخلش حاجه بترجع من غير ما تنفذ
    best_match = find_best_match(user_question, [q["question"] for q in knowledge_base["questions"]])
    response_text.delete("1.0", END)# بنحذف اي نص موجود مكان الاجابه 
    if best_match:#لو وجد اجابه مشابهه  يعرضها
        answer = get_answer_for_question(best_match, knowledge_base)
        response_text.insert(END, f"Bot: {answer}\n")
    else:#بتعرض رساله للمستخدم انه ليس لعنده رد ويطلب من المستخدم الاجابه ليتعلمها عن تريق صندوق ادخال
        response_text.insert(END, "Bot: I don't know the answer. Can you teach me?\n")
        new_answer = simpledialog.askstring("Input", "Type the answer or write down skip")
        if new_answer and new_answer.lower() != "skip":#لو تامستخدم ادخل اجابه يضيفها البوت لستخدامها لاحقا
            knowledge_base["questions"].append({"question": user_question, "answer": new_answer})
            save_knowledge_base("knowledge_base.json", knowledge_base)
            response_text.insert(END, "Bot: Thank you, I have learned a new response.\n")

def reset_input():
    user_input_text.delete("1.0", END)
    response_text.delete("1.0", END)

def chat_bot():
    global user_input_text, response_text, knowledge_base

    gui = Tk()
    gui.geometry('1000x800')
    gui.title("chatbot")
    gui.resizable(False, False)
    gui.config(background='#F5F5F5')

    knowledge_base = load_knowledge_base('knowledge_base.json')

    Label(gui, text="Ask a question:", background='#F5F5F5', foreground='#333333', font=('Arial', 14)).pack(pady=10)
    user_input_text = Text(gui, height=5, width=50, font=('Arial', 12))
    user_input_text.pack(pady=20)#.pack(pady=10): .pack(): This is a geometry manager method in Tkinter that organizes widgets in blocks before placing them in the parent widget.
    #pady=10: Adds padding of 10 pixels vertically (top and bottom) around the labe

    ask_button = Button(gui, text="Ask", command=process_user_input, bg='purple', fg='blue', font=('Arial', 12), relief=FLAT)
    ask_button.pack(pady=10)
    ask_button.config(width=10, height=2, borderwidth=1, relief="solid")

    reset_button = Button(gui, text="Reset", command=reset_input, bg='pink', fg='white', font=('Arial', 12), relief=FLAT)
    reset_button.pack(pady=10)
    reset_button.config(width=10, height=2, borderwidth=1, relief="solid")

    response_text = Text(gui, height=8, width=80, font=('Arial', 12))
    response_text.pack(pady=20)

    gui.mainloop()

if _name_ == '_main_':
    chat_bot()