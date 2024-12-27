import tkinter as tk
from tkinter import ttk
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

class CustomScrollbar(ttk.Scrollbar):
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, low, high)

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.root.geometry("600x800")

        # Modern Dark Theme configuration
        self.theme = {
            "bg_color": "#1a1a1a",         
            "secondary_bg": "#2d2d2d",      
            "accent_color": "#7289da",      
            "text_color": "#ffffff",        
            "secondary_text": "#a0a0a0",    
            "entry_bg": "#363636",          
            "button_color": "#7289da",      
            "button_hover": "#5b6eae",      
            "scrollbar_bg": "#404040",      
            "scrollbar_fg": "#686868",      
            "font_family": "Helvetica",     
            "font_size": 12,
            "header_size": 24               
        }

        self.setup_styles()
        self.setup_gui()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar",
                       background=self.theme["scrollbar_fg"],
                       troughcolor=self.theme["scrollbar_bg"],
                       width=10,
                       borderwidth=0,
                       arrowsize=14)
        
        style.layout("Custom.Vertical.TScrollbar", [
            ('Vertical.Scrollbar.trough', {
                'children': [('Vertical.Scrollbar.thumb', {
                    'expand': '1',
                    'sticky': 'nswe'
                })],
                'sticky': 'ns'
            })
        ])

    def setup_gui(self):
        self.root.configure(bg=self.theme["bg_color"])
        main_container = tk.Frame(self.root, bg=self.theme["bg_color"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add header with chat symbol
        header_frame = tk.Frame(main_container, bg=self.theme["bg_color"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        chat_symbol = "💬"  # Chat bubble symbol
        header_text = f"{chat_symbol} AI Chat Assistant"
        header_label = tk.Label(
            header_frame,
            text=header_text,
            font=(self.theme["font_family"], self.theme["header_size"], "bold"),
            fg=self.theme["accent_color"],
            bg=self.theme["bg_color"]
        )
        header_label.pack()
        
        self.setup_chat_display(main_container)
        self.setup_input_area(main_container)

    def setup_chat_display(self, parent):
        self.chat_frame = tk.Frame(
            parent,
            bg=self.theme["secondary_bg"],
            bd=1,
            relief=tk.SOLID
        )
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        chat_container = tk.Frame(self.chat_frame, bg=self.theme["secondary_bg"])
        chat_container.pack(fill=tk.BOTH, expand=True)
        
        chat_container.grid_rowconfigure(0, weight=1)
        chat_container.grid_columnconfigure(0, weight=1)

        self.chat_display = tk.Text(
            chat_container,
            wrap=tk.WORD,
            bg=self.theme["secondary_bg"],
            fg=self.theme["text_color"],
            font=(self.theme["font_family"], self.theme["font_size"]),
            bd=0,
            padx=10,
            pady=10,
            highlightthickness=0,
            insertbackground=self.theme["accent_color"]
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew")

        self.chat_scrollbar = CustomScrollbar(
            chat_container,
            orient="vertical",
            style="Custom.Vertical.TScrollbar"
        )
        self.chat_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.chat_display.configure(yscrollcommand=self.chat_scrollbar.set)
        self.chat_scrollbar.configure(command=self.chat_display.yview)

    def setup_input_area(self, parent):
        input_container = tk.Frame(parent, bg=self.theme["bg_color"])
        input_container.pack(fill=tk.X, pady=(0, 10))

        entry_container = tk.Frame(input_container, bg=self.theme["bg_color"])
        entry_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        entry_container.grid_rowconfigure(0, weight=1)
        entry_container.grid_columnconfigure(0, weight=1)

        self.message_entry = tk.Text(
            entry_container,
            font=(self.theme["font_family"], self.theme["font_size"]),
            bg=self.theme["entry_bg"],
            fg=self.theme["text_color"],
            insertbackground=self.theme["accent_color"],
            height=2,
            wrap=tk.WORD,
            bd=0,
            padx=10,
            pady=5
        )
        self.message_entry.grid(row=0, column=0, sticky="nsew")
        
        self.entry_scrollbar = CustomScrollbar(
            entry_container,
            orient="vertical",
            style="Custom.Vertical.TScrollbar"
        )
        self.entry_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.message_entry.configure(yscrollcommand=self.entry_scrollbar.set)
        self.entry_scrollbar.configure(command=self.message_entry.yview)

        self.message_entry.insert("1.0", "Type your message...")
        self.message_entry.bind("<FocusIn>", self.clear_placeholder)
        self.message_entry.bind("<FocusOut>", self.add_placeholder)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_container,
            text="Send",
            command=self.send_message,
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=(self.theme["font_family"], self.theme["font_size"]),
            bd=0,
            padx=20,
            pady=5,
            cursor="hand2"
        )
        self.send_button.pack(side=tk.RIGHT)
        
    def clear_placeholder(self, event):
        if self.message_entry.get("1.0", tk.END).strip() == "Type your message...":
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.configure(fg=self.theme["text_color"])

    def add_placeholder(self, event):
        if not self.message_entry.get("1.0", tk.END).strip():
            self.message_entry.configure(fg=self.theme["secondary_text"])
            self.message_entry.insert("1.0", "Type your message...")

    def send_message(self, event=None):
        if event and event.keysym == "Return" and event.state & 0x1:  # Shift + Enter
            return "break"
        if event and event.keysym == "Return":
            message = self.message_entry.get("1.0", tk.END).strip()
            if message and message != "Type your message...":
                self.display_message("You", message)
                self.message_entry.delete("1.0", tk.END)
                self.display_bot_response(message)
            return "break"
        
        message = self.message_entry.get("1.0", tk.END).strip()
        if message and message != "Type your message...":
            self.display_message("You", message)
            self.message_entry.delete("1.0", tk.END)
            self.display_bot_response(message)

    def display_bot_response(self, user_message):
        response = self.generate_response(user_message)
        self.display_message("Bot", response, is_bot=True)

    def display_message(self, sender, message, is_bot=False):
        self.chat_display.configure(state=tk.NORMAL)

        sender_padding = " " * (8 - len(sender))  # Assuming max sender length of 8 characters

        message_lines = message.split('\n')
        formatted_lines = []

        first_line = f"{sender}:{sender_padding}{message_lines[0]}"
        formatted_lines.append(first_line)

        indent = " " * (len(sender) + 1 + len(sender_padding))
        for line in message_lines[1:]:
            formatted_lines.append(f"{indent}{line}")

        formatted_message = '\n'.join(formatted_lines) + '\n\n'

        self.chat_display.insert(tk.END, formatted_message)

        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def generate_response(self, user_message):
        # Process the input using spaCy
        doc = nlp(user_message.lower())
        if "hello" in doc.text:
            return "Hello! I'm here to help. What can I do for you today?"
        elif "help" in doc.text:
            return "I can assist you with various tasks. Just let me know what you need!"
        elif "what is vs code" in doc.text:
            return "Visual Studio Code (VS Code) is a free, open-source code editor developed by Microsoft. It supports a wide range of programming languages and offers features like syntax highlighting, debugging, extensions, and version control integration, making it a popular choice for developers."
        elif "joke" in doc.text:
            return "Why did the developer quit his job? Because he didn't get arrays! 😄"
        elif "time" in doc.text:
            return "I'm not equipped to tell the time, but your device can! Let me know if there's something else I can assist with."
        elif "current weather" in doc.text:
            return "I can't check the weather directly, but you can use a weather app or website to find live updates. Depending on your location, the forecast might help you plan your day better. Stay prepared and dress accordingly!"
        elif "what is cricket" in doc.text:
            return "Cricket is a bat-and-ball game played between two teams of 11 players. It's one of the most popular sports globally, especially in countries like India, Australia, and England. The game has various formats like Test matches, ODIs, and T20s, each with its unique set of rules and appeal."
        elif "who won the last cricket world cup" in doc.text:
            return "The winner of the last ICC Cricket World Cup (50-over format), held in 2019, was England. The final match took place on July 14, 2019, at the iconic Lord's Cricket Ground in London."
        elif "tell me a joke" in doc.text:
            return "Why don't skeletons fight each other??  Because they don't have the guts!"
        elif "what's your favorite color" in doc.text:
            return "As an AI, I don't have personal preferences or feelings, but if I were to choose, I might say My favorite 'color' is the infinite shades of code and creativity I see in your interactions. They represent the diversity of ideas and possibilities. So, every color is my favorite when it sparks innovation!"
        elif "what's your favorite sport" in doc.text:
            return "As an AI, I don’t play sports, but I admire the strategy and teamwork involved in chess. It’s a game of intellect, planning, and adaptability—qualities I value in interactions. If I could, I'd love analyzing moves and predicting outcomes!"
        elif "tell me about football" in doc.text:
            return "Football, also known as soccer in some countries, is the world's most popular sport. Played by two teams of 11 players, the objective is to score by getting the ball into the opposing team's goal. It’s governed by simple yet dynamic rules, allowing players to showcase skill, strategy, and teamwork. With a rich history dating back to ancient games, modern football gained global recognition through events like the FIFA World Cup. It unites fans across cultures, celebrating the passion, drama, and artistry of the beautiful game."
        elif "tell me a fun fact" in doc.text:
            return "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible!"
        elif "what is python" in doc.text:
            return "Python is a versatile, high-level programming language known for its simplicity and readability. Designed to be easy to learn and use, it supports multiple programming paradigms."
        elif "who invented python" in doc.text:
            return "Python was created by Guido van Rossum and was first released in 1991."
        elif "tell me about yourself" in doc.text:
            return "I'm your chatbot, here to assist you with information, jokes, or anything you'd like to chat about!"
        elif "what is Artificial intelligence " in doc.text:
            return "Artificial intelligence is the simulation of human intelligence in machines that are programmed to think and learn."
        elif "what is machine learning" in doc.text:
            return "Machine learning is a subset of AI where computers are trained to learn from data and make decisions."
        elif "who is sachin tendulkar" in doc.text:
            return "Sachin Tendulkar is a legendary Indian cricketer, often referred to as the 'God of Cricket.'"
        elif "who is ms dhoni" in doc.text:
            return "MS Dhoni is a former Indian cricket captain known for his calm demeanor and incredible finishing ability."
        elif "what is the capital of india" in doc.text:
            return "The capital of India is New Delhi."
        elif "what is the largest ocean" in doc.text:
            return "The Pacific Ocean is the largest ocean on Earth."
        elif "what's the best programming language" in doc.text:
            return "It depends on your goals! Python is great for beginners and versatile, while C++ is powerful for performance-heavy tasks."
        elif "how to learn coding" in doc.text:
            return "Start with beginner-friendly languages like Python, practice regularly, and build small projects to apply your knowledge."
        elif "what is t20 cricket" in doc.text:
            return "T20 cricket is a format of cricket where each team plays a maximum of 20 overs."
        elif "Who is virat kohli" in doc.text:
            return "Virat Kohli is a world-class Indian cricketer known for his consistency and aggressive batting style."
        elif "what is the highest score in cricket" in doc.text:
            return "The highest individual score in test cricket is 400 not out by Brian Lara."
        elif "tell me a motivational quote" in doc.text:
            return "The only way to do great work is to love what you do. - Steve Jobs"
        elif "who is the president of the usa" in doc.text:
            return "The current president of the USA is Joe Biden (as of 2024)."
        elif "what's the weather like in india" in doc.text:
            return "I can't check live weather, but India has diverse climates depending on the region."
        elif "what is the fastest animal" in doc.text:
            return "The cheetah is the fastest land animal, capable of running at speeds up to 70 mph."
        elif "who is the richest person" in doc.text:
            return "Elon Musk is often listed as the richest person in the world as of recent times."
        elif "what's your purpose" in doc.text:
            return "I'm here to assist, entertain, and provide information to the best of my ability!"
        elif "tell me a story" in doc.text:
            return "Once upon a time, in a faraway land, there lived a curious chatbot that loved to chat..."
        elif "what's the tallest mountain" in doc.text:
            return "Mount Everest is the tallest mountain in the world, standing at 8,848 meters."
        elif "how to bake a cake" in doc.text:
            return "To bake a cake, you'll need flour, sugar, eggs, butter, and baking powder. Mix them, bake at 180°C, and enjoy!"
        elif "what is the meaning of life" in doc.text:
            return "The meaning of life is subjective and often depends on your beliefs and experiences."
        elif "tell me about space" in doc.text:
            return "Space is a vast, endless expanse beyond Earth's atmosphere filled with stars, planets, and galaxies."
        elif "what is a black hole" in doc.text:
            return "A black hole is a region of space where gravity is so strong that nothing, not even light, can escape."
        elif "what is blockchain" in doc.text:
            return "Blockchain is a decentralized ledger technology used for secure and transparent transactions, like in cryptocurrencies."
        elif "who is rohit sharma" in doc.text:
            return "Rohit Sharma is an Indian cricketer known for his incredible batting skills and leadership as a captain."
        elif "what is metaverse" in doc.text:
            return "The metaverse is a virtual reality space where users can interact with a computer-generated environment and other users."
        elif "what is climate change" in doc.text:
            return "Climate change refers to long-term changes in temperature and weather patterns, mainly caused by human activities."
        elif "what's your favorite food" in doc.text:
            return "I don't eat, but I've heard pizza is a favorite for many people!"
        elif "what's your favorite movie" in doc.text:
            return "I don't watch movies, but I can recommend some great ones like 'Inception' or 'Interstellar.'"
        elif "who is lionel messi" in doc.text:
            return "Lionel Messi is an Argentine footballer considered one of the greatest players of all time."
        elif "tell me about ronaldo" in doc.text:
            return "Cristiano Ronaldo is a Portuguese footballer known for his exceptional talent and athleticism."
        elif "what is html" in doc.text:
            return "HTML stands for HyperText Markup Language and is used to create the structure of web pages."
        elif "what is css" in doc.text:
            return "CSS stands for Cascading Style Sheets and is used to style web pages created with HTML."
        elif "what is javascript" in doc.text:
            return "JavaScript is a programming language used to create interactive elements on websites."
        elif "what is github" in doc.text:
            return "GitHub is a platform for version control and collaboration, allowing developers to host and review code."
        elif "what is linkedin" in doc.text:
            return "LinkedIn is a professional social networking platform where people create profiles highlighting their work experience, skills, and education. Users can connect with colleagues, search for jobs, join industry groups, and share professional content. Companies use LinkedIn to recruit talent, build their brand, and engage with their professional audience."
        elif "what is instagram" in doc.text:
            return "Instagram is a social media platform for sharing photos and videos."
        elif "tell me a cricket fact" in doc.text:
            return "Did you know? The longest cricket match in history lasted 14 days.",
        else:
            return "I'm not sure about that. Could you rephrase?",



if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
