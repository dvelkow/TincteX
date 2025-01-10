import tkinter as tk
from tkinter import ttk
import random
from sentences import SENTENCES

class ChromolexiaTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Chromolexia Translator")
        
        # Dictionary mapping letters to colors
        self.color_map = {
            'A': '#FF0000',  # Red
            'B': '#00FF00',  # Green
            'C': '#0000FF',  # Blue
            'D': '#FFFF00',  # Yellow
            'E': '#FF00FF',  # Magenta
            'F': '#00FFFF',  # Cyan
            'G': '#556B2F',  # Dark Olive Green
            'H': '#CCFF00',  # Yellow-Green
            'I': '#008000',  # Dark Green
            'J': '#FF1493',  # Deep Pink
            'K': '#FFD700',  # Gold
            'L': '#4B0082',  # Indigo
            'M': '#808080',  # Gray
            'N': '#00CED1',  # Dark Turquoise
            'O': '#48494B',  # Iron
            'P': '#FF746C',  # Pastel Red
            'Q': '#FFA500',  # Orange
            'R': '#B22222',  # Fire Brick
            'S': '#4682B4',  # Steel Blue
            'T': '#000000',  # Black
            'U': '#A0522D',  # Sienna
            'V': '#66CDAA',  # Medium Aquamarine
            'W': '#BA55D3',  # Medium Orchid
            'X': '#CD853F',  # Peru
            'Y': '#DB7093',  # Pale Violet Red
            'Z': '#F8DE7E'   # Mellow Yellow
        }
        
        self.show_letters = True
        self.show_input = True
        self.setup_gui()
        
    def setup_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input area frame (for hiding/showing)
        self.input_frame = ttk.Frame(main_frame)
        self.input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Input label and text area
        input_label = ttk.Label(self.input_frame, text="Type your text:", font=('Arial', 12))
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_text = tk.Text(self.input_frame, height=3, width=50, font=('Arial', 12))
        self.input_text.grid(row=1, column=0, pady=(0, 10))
        self.input_text.bind('<KeyRelease>', self.on_text_change)
        
        # Translation area
        translation_label = ttk.Label(main_frame, text="Color Translation:", font=('Arial', 12))
        translation_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # Canvas for color blocks
        self.canvas = tk.Canvas(main_frame, height=100, width=600, bg='white')
        self.canvas.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, sticky=tk.W)
        
        # Random sentence button
        random_btn = ttk.Button(buttons_frame, text="Generate Random Sentence", 
                              command=self.generate_random_sentence)
        random_btn.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # Legend toggle button
        self.show_legend_var = tk.BooleanVar(value=False)
        legend_btn = ttk.Checkbutton(buttons_frame, text="Show Color Legend", 
                                   variable=self.show_legend_var, 
                                   command=self.toggle_legend)
        legend_btn.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        # Letters toggle button
        self.show_letters_var = tk.BooleanVar(value=True)
        letters_btn = ttk.Checkbutton(buttons_frame, text="Show Letters", 
                                    variable=self.show_letters_var, 
                                    command=self.toggle_letters)
        letters_btn.grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        
        # Hide input toggle button
        self.show_input_var = tk.BooleanVar(value=True)
        input_btn = ttk.Checkbutton(buttons_frame, text="Show Input Area", 
                                  variable=self.show_input_var, 
                                  command=self.toggle_input)
        input_btn.grid(row=0, column=3, sticky=tk.W)
        
        # Legend frame (hidden by default)
        self.legend_frame = ttk.Frame(main_frame)
        self.legend_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=10)
        self.create_legend()
        self.legend_frame.grid_remove()
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
    def create_legend(self):
        # Create color blocks with letters in a grid
        row, col = 0, 0
        for letter, color in self.color_map.items():
            frame = ttk.Frame(self.legend_frame)
            frame.grid(row=row, column=col, padx=5, pady=2)
            
            canvas = tk.Canvas(frame, width=20, height=20, bg=color)
            canvas.grid(row=0, column=0, padx=(0, 5))
            
            label = ttk.Label(frame, text=letter)
            label.grid(row=0, column=1)
            
            col += 1
            if col > 6:  # 7 items per row
                col = 0
                row += 1
    
    def toggle_legend(self):
        if self.show_legend_var.get():
            self.legend_frame.grid()
        else:
            self.legend_frame.grid_remove()
            
    def toggle_letters(self):
        self.show_letters = self.show_letters_var.get()
        self.on_text_change()
    
    def toggle_input(self):
        if self.show_input_var.get():
            self.input_frame.grid()
        else:
            self.input_frame.grid_remove()
    
    def generate_random_sentence(self):
        """Generate and insert a random sentence into the input text area"""
        sentence = random.choice(SENTENCES)
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", sentence)
        self.on_text_change()
    
    def on_text_change(self, event=None):
        # Clear canvas
        self.canvas.delete("all")
        
        # Get text and convert to uppercase
        text = self.input_text.get("1.0", "end-1c").upper()
        
        # Draw color blocks
        block_width = 30
        x = 10
        y = 10
        max_width = self.canvas.winfo_width() - block_width
        
        for char in text:
            if char in self.color_map:
                # Draw colored block
                self.canvas.create_rectangle(x, y, x + block_width, y + block_width, 
                                          fill=self.color_map[char], outline='black')
                # Draw letter if enabled
                if self.show_letters:
                    self.canvas.create_text(x + block_width/2, y + block_width/2, 
                                          text=char, font=('Arial', 12))
            elif char == ' ':
                # Add space between blocks
                x += block_width + 5
            
            # Move to next position if character was processed
            if char in self.color_map:
                x += block_width + 5
            
            # Move to next line if needed
            if x > max_width:
                x = 10
                y += block_width + 5

def main():
    root = tk.Tk()
    root.title("Chromolexia Translator")
    app = ChromolexiaTranslator(root)
    root.mainloop()

if __name__ == "__main__":
    main()