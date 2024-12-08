import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import keyword
import re
dghffh=''
class NCERTLearnIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("NCERT Learn IDE")
        self.root.geometry("800x600")  


        # Main menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.root.iconbitmap(r"./assert.ico") 
        

        # File menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu.add_cascade(label="File", menu=file_menu)

        # Run menu
        run_menu = tk.Menu(self.menu, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_file)
        self.menu.add_cascade(label="Run", menu=run_menu)

        # View menu
        view_menu = tk.Menu(self.menu, tearoff=0)
        view_menu.add_command(label="Dark Theme", command=self.set_dark_theme)
        view_menu.add_command(label="Light Theme", command=self.set_light_theme)
        self.menu.add_cascade(label="View", menu=view_menu)
        about_menu = tk.Menu(self.menu, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about_tab)
        self.menu.add_cascade(label="About", menu=about_menu)

        # Tab Control
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")
        self.root.bind("<F5>", self.run_file_key)
        


    def new_file(self):
        new_tab = self.create_tab("Untitled")
        self.tab_control.add(new_tab, text="Untitled")
        self.tab_control.select(new_tab)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("HTML Files", "*.html"),("C Files", "*.c"),("C++ Files", "*.cpp"),("Text Files","*.txt"), ("Readme Files","*.readme"),( "Markdown Files","*.md"), ("JSON Files","*.json"), ("XML Files","*.xml"),("CSS Files",".css"),("JavaScript Files",".js") ,("All Files", "*.*")])
        if file_path:
            # Read the content of the file
            with open(file_path, "r") as file:
                content = file.read()

            # Create a new tab with the file content
            new_tab = self.create_tab(file_path, content)

            # Select the newly created tab
            self.tab_control.select(new_tab)
   
    def show_about_tab(self):
        # Create a new tab
        about_tab = tk.Frame(self.tab_control)
        self.tab_control.add(about_tab, text="About")

        # Add content to the tab
        label = tk.Label(about_tab, text="NCERT Learn IDE\nVersion 1.0\nCreated for learning and coding\nBy Muhammed Shafin P.", font=("Arial", 12))
        label.pack(pady=20)

        # Add a close button
        close_button = tk.Button(about_tab, text="Close", bg="red", fg="white",
                                 command=lambda: self.close_tab(about_tab))
        close_button.pack(pady=10)

        # Switch to the new tab
        self.tab_control.select(about_tab)

    def close_tab(self, tab):
        """Remove a specific tab."""
        self.tab_control.forget(tab)




    def save_file(self):
        current_tab = self.tab_control.nametowidget(self.tab_control.select())
        file_path = current_tab.file_path
        if file_path == "Untitled":
            self.save_as_file()
        else:
            self._write_to_file(file_path, current_tab.text_widget.get("1.0", "end-1c"))

    def save_as_file(self):
        current_tab = self.tab_control.nametowidget(self.tab_control.select())
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("HTML Files", "*.html"),("C Files", "*.c"),("C++ Files", "*.cpp"),("Text Files","*.txt"), ("Readme Files","*.readme"),( "Markdown Files","*.md"), ("JSON Files","*.json"), ("XML Files","*.xml"),("CSS Files",".css"),("JavaScript Files",".js") ,("All Files", "*.*")])
        if file_path:
            current_tab.file_path = file_path
            self._write_to_file(file_path, current_tab.text_widget.get("1.0", "end-1c"))
            self.tab_control.tab(current_tab, text=os.path.basename(file_path))
    def run_file_key(self, event=None):
        """Trigger the run_file method when F5 is pressed."""
        self.root.focus_set()  # Ensure focus is on the main window
        self.run_file()
    def write_paths_to_files(self,file_path, gcc_path, gpp_path):
        # Write GCC and G++ paths to text files
        with open("gccpath.txt", "w") as f:
            f.write(gcc_path)
        
        with open("gppath.txt", "w") as f:
            f.write(gpp_path)
        
        # Write the file path to be compiled
        if file_path.endswith(".c"):
            with open("inputc.txt", "w") as f:
                f.write(file_path)
        elif file_path.endswith(".cpp"):
            with open("inputcpp.txt", "w") as f:
                f.write(file_path)

    def run_file(self):
        current_tab = self.tab_control.nametowidget(self.tab_control.select())
        file_path = current_tab.file_path
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script

        # Ensure correct paths for Python, GCC, and G++
        python_path = os.path.join(script_dir, "python","venv","Scripts", "python.exe")
        gcc_path = os.path.join(script_dir, "gcc", 'bin', "gcc.exe")
        gpp_path = os.path.join(script_dir, "gcc", 'bin', "g++.exe")
        self.write_paths_to_files(file_path, gcc_path, gpp_path)

        # Check if executables exist
        if not os.path.exists(python_path):
            self.show_terminal_output("", f"Python executable not found at {python_path}/nPLease use NCERT Learn IDE Reset Python Environmet to restore python environment.", current_tab)
            return
        if not os.path.exists(gcc_path):
            self.show_terminal_output("", f"GCC executable not found at {gcc_path}", current_tab)
            return
        if not os.path.exists(gpp_path):
            self.show_terminal_output("", f"G++ executable not found at {gpp_path}", current_tab)
            return

        # Handle Untitled file and save
        if file_path == "Untitled":
            self.save_as_file()
            file_path = current_tab.file_path
                    # Write paths to text files




        # Running Python file
        elif file_path.endswith(".py"):
            self.save_file()
            try:
                # Use a list for arguments to avoid issues with spaces in paths
                process = subprocess.run(
                    [python_path, file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                self.show_terminal_output(f'>>>{process.stdout}', process.stderr, current_tab)
            except Exception as e:
                self.show_terminal_output("", f"Failed to run Python file: {str(e)}", current_tab)

        # Running HTML file
        elif file_path.endswith(".html"):
            self.save_file()
            os.startfile(file_path)

        # Compile and run C file using GCC in PowerShell
        elif file_path.endswith(".c"):
            self.save_file()
            self.show_terminal_output("Use Ncert Learn IDE C Runner To Get Result.\n", "", current_tab)
            


        # Compile and run C++ file using G++ in PowerShell
        elif file_path.endswith(".cpp"):
            self.save_file()
            self.show_terminal_output("Use Ncert Learn IDE C++ Runner To Get Result.\n", "", current_tab)
            


        # Handle other file types like .txt, .md, etc.
        elif file_path.endswith((".txt", ".readme", ".md", ".json", ".xml", ".css", "js")):
            try:
                self.save_file()  # Save the file without attempting to run
                self.show_terminal_output("File saved successfully.\n", "", current_tab)
            except Exception as e:
                self.show_terminal_output("", f"Failed to save file: {str(e)}", current_tab)

        else:
            self.save_file()
            self.show_terminal_output("Unsupported File", "Cannot run this type of file. You can save it instead.", current_tab)
            self.save_file()
        



    def show_terminal_output(self, stdout, stderr, parent_tab):
        # Check if the terminal frame already exists, if not, create one
        if not hasattr(self, "terminal_frame"):
            # Create a frame at the bottom for the terminal output
            self.terminal_frame = tk.Frame(self.root, bg="gray", height=200)
            self.terminal_frame.pack(side=tk.BOTTOM, fill=tk.X)

            # Add a close button
            close_button = tk.Button(self.terminal_frame, text="X", bg="red", fg="white", relief="flat", 
                                    command=self.close_terminal_output)
            close_button.pack(side=tk.RIGHT, padx=5, pady=5)

            # Create the terminal Text widget
            self.terminal = tk.Text(self.terminal_frame, wrap=tk.NONE, bg="black", fg="white", font=("Courier", 12))
            self.terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.terminal.config(state=tk.DISABLED)

            # Add vertical and horizontal scrollbars
            v_scrollbar = tk.Scrollbar(self.terminal_frame, orient=tk.VERTICAL, command=self.terminal.yview)
            h_scrollbar = tk.Scrollbar(self.terminal_frame, orient=tk.HORIZONTAL, command=self.terminal.xview)
            self.terminal["yscrollcommand"] = v_scrollbar.set
            self.terminal["xscrollcommand"] = h_scrollbar.set

            # Pack the scrollbars
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

            # Make the frame resizable vertically by dragging
            self.terminal_frame.pack_propagate(False)
            self.terminal_frame.bind("<ButtonPress-1>", self.start_resize)
            self.terminal_frame.bind("<B1-Motion>", self.perform_resize)

            # Enable mouse wheel scrolling
            self.terminal.bind("<MouseWheel>", lambda event: self.on_mouse_wheel(event, self.terminal))

            # Access the top-level window (Tk) from the parent frame
            parent_window = parent_tab.winfo_toplevel()

            # Bind the close event to the parent window (Tk) close
            parent_window.protocol("WM_DELETE_WINDOW", lambda: self.close_terminal_output(parent_window))

        # Store a reference to the parent tab
        self.terminal_frame.parent_tab = parent_tab

        # Enable the terminal for editing to add new content
        self.terminal.config(state=tk.NORMAL)

        # Insert the output (stdout) and errors (stderr)
        self.terminal.insert(tk.END, stdout)
        if stderr:
            self.terminal.insert(tk.END, f"\nERROR:\n{stderr}")

        # Scroll to the bottom
        self.terminal.yview(tk.END)

        # Disable the terminal to make it read-only
        self.terminal.config(state=tk.DISABLED)


    def close_terminal_output(self, parent_window=None):
        # Check if the parent window is valid and exists before calling destroy
        if parent_window and parent_window.winfo_exists():
            parent_window.destroy()

        # Only destroy terminal_frame if it exists and is still part of the application
        if hasattr(self, "terminal_frame") and self.terminal_frame:
            self.terminal_frame.destroy()
            del self.terminal_frame


    def start_resize(self, event):
        self.resize_start_y = event.y

    def perform_resize(self, event):
        delta_y = event.y - self.resize_start_y
        new_height = max(50, self.terminal_frame.winfo_height() + delta_y)
        self.terminal_frame.config(height=new_height)
        self.resize_start_y = event.y

    def on_mouse_wheel(self, event):
        self.terminal.yview_scroll(-1 * (event.delta // 120), "units")



    # Ensure terminal closes when the tab is closed
    def on_tab_close(self, tab):
        if hasattr(self, "terminal_frame") and self.terminal_frame.parent_tab == tab:
            self.close_terminal_output()



    def set_light_theme(self):
        for tab_id in self.tab_control.tabs():
            tab = self.tab_control.nametowidget(tab_id)
            tab.text_widget.configure(bg="white", fg="black", insertbackground="black")
    def set_dark_theme(self):
        for tab_id in self.tab_control.tabs():
            tab = self.tab_control.nametowidget(tab_id)
            tab.text_widget.configure(bg="black", fg="white", insertbackground="black")








    def create_tab(self, file_path, content=""):
        # Create a frame for the tab content
        frame = ttk.Frame(self.tab_control)
        frame.file_path = file_path 
        global dghffh
        dghffh =file_path  # Store the file path in the frame

        # Create a Text widget for editing
        text_widget = tk.Text(frame, wrap="none", undo=True)
        text_widget.pack(side="left", expand=1, fill="both", padx=5, pady=5)
        frame.text_widget = text_widget
        # Add auto-completion for Python files
        if file_path.endswith(".py"):
            text_widget.bind("<KeyRelease>", lambda event: self.pyautocomplete(event, text_widget))
        if file_path.endswith((".html", ".css", ".js",".xml")):
            text_widget.bind("<KeyRelease>", lambda event: self.htmlautocomplete(event, text_widget))
        if file_path.endswith((".c", ".cpp")):
            text_widget.bind("<KeyRelease>", lambda event: self.cautocomplete(event, text_widget))
        if file_path.endswith(".xml"):
            text_widget.bind("<KeyRelease>", lambda event: self.xmlautocomplete(event, text_widget))


        # Define the tags for highlighting with advanced colors
        text_widget.tag_configure("keyword", foreground="#0000CD")
        text_widget.tag_configure("comment", foreground="#006400")
        text_widget.tag_configure("string", foreground="#8B0000")
        text_widget.tag_configure("function", foreground="#8A2BE2")
        text_widget.tag_configure("class", foreground="#00008B")
        text_widget.tag_configure("import_lib", foreground="#20B2AA")
        text_widget.tag_configure("import_func", foreground="#FF6347")
        text_widget.tag_configure("variable", foreground="#006400")
        text_widget.tag_configure("number", foreground="#FF1493")
        text_widget.tag_configure("operator", foreground="#FF4500")
        text_widget.tag_configure("html_tag", foreground="#A52A2A")
        text_widget.tag_configure("html_attr", foreground="#D2691E")
        text_widget.tag_configure("html_comment", foreground="#808080")
        text_widget.tag_configure("html_string", foreground="#DC143C")
        text_widget.tag_configure("js_keyword", foreground="#0000CD")
        text_widget.tag_configure("js_function", foreground="#32CD32")
        text_widget.tag_configure("js_comment", foreground="#2F4F4F")
        # Syntax highlighting tags for C and C++ files
        text_widget.tag_configure("c_keyword", foreground="#0000CD")
        text_widget.tag_configure("c_comment", foreground="#006400")
        text_widget.tag_configure("c_string", foreground="#8B0000")
        text_widget.tag_configure("c_function", foreground="#8A2BE2")
        text_widget.tag_configure("c_number", foreground="#FF1493")
        text_widget.tag_configure("c_operator", foreground="#FF4500")
        text_widget.tag_configure("css_selector", foreground="#00008B")
        text_widget.tag_configure("css_property", foreground="#8A2BE2")
        text_widget.tag_configure("css_value", foreground="#FF4500")
        text_widget.tag_configure("css_comment", foreground="#006400")

        # Syntax highlighting tags for Markdown files
        text_widget.tag_configure("markdown_header", foreground="#00008B")
        text_widget.tag_configure("markdown_bold", foreground="#8B0000")
        text_widget.tag_configure("markdown_italic", foreground="#006400")

        # Syntax highlighting tags for JSON and XML
        text_widget.tag_configure("json_key", foreground="#8A2BE2")
        text_widget.tag_configure("json_string", foreground="#8B0000")
        text_widget.tag_configure("json_number", foreground="#FF1493")
        text_widget.tag_configure("xml_tag", foreground="#A52A2A")
        text_widget.tag_configure("xml_attr", foreground="#D2691E")
        text_widget.tag_configure("xml_string", foreground="#DC143C")
        # Define tags for special characters like () [] {} <>
        text_widget.tag_configure("double_quotes", foreground="#FF1493")  # For ""
        text_widget.tag_configure("single_quotes", foreground="#8A2BE2")  # For ''
        text_widget.tag_configure("triple_double_quotes", foreground="#32CD32")  # For """ """
        text_widget.tag_configure("triple_single_quotes", foreground="#FFD700")  # For ''' '''
        text_widget.tag_configure("html_tag", foreground="#A52A2A")  # For < >
        text_widget.tag_configure("html_end_tag", foreground="#A52A2A")  # For </>


        # Insert content if available
        if content:
            text_widget.insert("1.0", content)

            # Apply syntax highlighting after inserting content
            self.syntax_highlight(text_widget)

        # Add vertical scroll buttons (Up and Down buttons)
        up_button = ttk.Button(frame, text="↑", width=2, command=lambda: self.scroll_up(text_widget))
        down_button = ttk.Button(frame, text="↓", width=2, command=lambda: self.scroll_down(text_widget))

        # Position the buttons on the right side of the frame
        up_button.pack(side="right", pady=(5, 0), anchor="n")
        down_button.pack(side="right", pady=(0, 5), anchor="s")

        # Add left and right buttons for horizontal scrolling
        left_button = ttk.Button(frame, text="←", width=2, command=lambda: self.scroll_left(text_widget))
        right_button = ttk.Button(frame, text="→", width=2, command=lambda: self.scroll_right(text_widget))

        # Position the horizontal buttons at the bottom
        left_button.pack(side="bottom", padx=5, anchor="w")
        right_button.pack(side="bottom", padx=5, anchor="e")

        run_button = ttk.Button(frame, text="Run", command=lambda: self.run_file())
        run_button.pack(side="bottom", pady=(10, 5))
        increase_button = ttk.Button(frame, text="+", command=lambda: self.increase_font_size(text_widget))
        decrease_button = ttk.Button(frame, text="-", command=lambda: self.decrease_font_size(text_widget))

# Position the buttons on the top right corner
        increase_button.pack(side="top", padx=5, pady=5, anchor="ne")
        decrease_button.pack(side="top", padx=5, pady=5, anchor="ne")

        # Enable mouse scroll wheel to work with the Text widget (for vertical scrolling)
        text_widget.bind("<MouseWheel>", lambda event: self.on_mouse_wheel(event, text_widget))
        text_widget.bind("<Control-s>", lambda event: self.save_file())
        text_widget.bind("<F5>", lambda event: self.run_file())

        # Set the tab title based on the file name or "Untitled"
        tab_name = os.path.basename(file_path) if file_path != "Untitled" else "Untitled"

        # Add the tab to the notebook with a close button
        self.tab_control.add(frame, text=tab_name)


        # Create a close button and attach it to the tab
        close_button = tk.Button(
            frame,
            text="X",
            command=lambda: self.close_tab(frame),
            relief="flat",
            bg="red",
            fg="white",
            width=2
        )
        # Adjust placement to move it further down
        close_button.place(relx=0.98, rely=0.5, anchor="ne")  # Move halfway down the right side

        # Return the created frame
        return frame
    def increase_font_size(self, text_widget):
        current_font = text_widget.cget("font")  # Get the current font setting
        if current_font:
            font_parts = current_font.split()
            if len(font_parts) > 1:
                current_size = int(font_parts[1])  # Get current font size from the second element
            else:
                current_size = 10  # Default font size if not found
        else:
            current_size = 10  # Default font size if no font is set

        new_size = current_size + 2  # Increase font size by 2
        text_widget.config(font=("Arial", new_size))  # Set the new font size

    def decrease_font_size(self, text_widget):
        current_font = text_widget.cget("font")  # Get the current font setting
        if current_font:
            font_parts = current_font.split()
            if len(font_parts) > 1:
                current_size = int(font_parts[1])  # Get current font size from the second element
            else:
                current_size = 10  # Default font size if not found
        else:
            current_size = 10  # Default font size if no font is set

        new_size = current_size - 2  # Decrease font size by 2
        if new_size >= 6:  # Ensure the font size doesn't go too small
            text_widget.config(font=("Arial", new_size))  # Set the new font size
    def xmlautocomplete(self, event, text_widget):
        """
        Automatically complete parentheses, brackets, braces, and quotes when typing in Python files.
        Places the cursor between the opening and closing characters after insertion.
        Handles backspace correctly.
        """
        char = event.char  # Get the character typed
        cursor_index = text_widget.index(tk.INSERT)  # Get the current cursor position

        # Define pairs of opening and closing characters
        matching_pairs = {
            '<': '>',
            '<>': '</>',
            '<!--':' -->',
            '"': '"',
            "'": "'",
            '(': ')',
            '[': ']',
            '{': '}',
            '<?': '?>',
            '<!': '>',
            '<?xml:':'?>',
            '<?':'?>',
            

        }

        # If the character is an opening character
        if char in matching_pairs:
            if char == '<':  # Special handling for '<' which can lead to tag insertion
                text_widget.insert(cursor_index, matching_pairs[char])
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                return "break"  # Prevent default insert behavior for opening '<'
            else:
                # Insert the closing character for the respective pair
                text_widget.insert(cursor_index, matching_pairs[char])
                # Move the cursor back between the characters
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                return "break"  # Prevent the default insert behavior

        # If the character is a closing character (e.g., ')', '>', '"', etc.)
        elif char in matching_pairs.values():
            prev_char = text_widget.get(f"{cursor_index} - 1c", cursor_index)

            # If the previous character is the corresponding opening character, do not insert the closing character
            if prev_char in matching_pairs and matching_pairs[prev_char] == char:
                return "break"  # Prevent inserting the closing character

        # Handle backspace behavior for matching pairs (single characters and HTML tags)
        if event.keysym == 'BackSpace':
            prev_char = text_widget.get(f"{cursor_index} - 1c", cursor_index)

            # Handle backspace for single character pairs (like '(', '[', etc.)
            if prev_char in matching_pairs:
                next_char = text_widget.get(f"{cursor_index} + 1c", f"{cursor_index} + 2c")
                if next_char == matching_pairs[prev_char]:  # If it's the matching closing character
                    text_widget.delete(f"{cursor_index} - 1c", f"{cursor_index} + 2c")
                    text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                    return "break"  # Stop the default backspace behavior

            # Handle backspace for HTML tag pairs (like '<div>' and '</div>', etc.)
            if prev_char == '>' and text_widget.get(f"{cursor_index} - 2c", cursor_index) == '<':
                # This is the closing tag, delete both opening and closing tag
                text_widget.delete(f"{cursor_index} - 2c", f"{cursor_index} + 1c")
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 2c")
                return "break"

            elif prev_char == '-' and text_widget.get(f"{cursor_index} - 2c", cursor_index) == '<' and text_widget.get(f"{cursor_index} + 1c", f"{cursor_index} + 2c") == '-':
                # This is the comment end '-->', delete both start and end
                text_widget.delete(f"{cursor_index} - 4c", f"{cursor_index} + 3c")
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 4c")
                return "break"

        return None   # Prevent inserting the closing character if it's already matched


    def htmlautocomplete(self, event, text_widget):
        """
        Automatically complete parentheses, brackets, braces, and quotes when typing in Python files.
        Places the cursor between the opening and closing characters after insertion.
        Handles backspace correctly.
        """
        char = event.char  # Get the character typed
        cursor_index = text_widget.index(tk.INSERT)  # Get the current cursor position

        # Define pairs of opening and closing characters
        matching_pairs = {
            '<': '>',
            '<>': '</>',
            '<!--':' -->',
            '"': '"',
            "'": "'",
            '(': ')',
            '[': ']',
            '{': '}',
            '<!DOCTYPE': '>',
            '<!DOCTYPE html': '>',
            '<!DOCTYPE html PUBLIC': '>',
            '<!DOCTYPE html SYSTEM': '>',
            '<!DOCTYPE svg': '>',            
            '<!DOCTYPE svg PUBLIC': '>',            
            '<!DOCTYPE svg SYSTEM': '>',            
            '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"': '>',
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"': '>',
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"': '>',
            '<!':'>',
            '<!DOCTYPE': '>',
            '<!ELEMENT': '>',
            '<!ATTLIST': '>',
            '<!ENTITY': '>',
            '<!NOTATION': '>',
            '<!ELEMENT': '>',
            '<!ATTLIST': '>',
            '<!ENTITY': '>',
            '<!NOTATION': '>', 
            

        }

        # If the character is an opening character
        if char in matching_pairs:
            if char == '<':  # Special handling for '<' which can lead to tag insertion
                text_widget.insert(cursor_index, matching_pairs[char])
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                return "break"  # Prevent default insert behavior for opening '<'
            else:
                # Insert the closing character for the respective pair
                text_widget.insert(cursor_index, matching_pairs[char])
                # Move the cursor back between the characters
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                return "break"  # Prevent the default insert behavior

        # If the character is a closing character (e.g., ')', '>', '"', etc.)
        elif char in matching_pairs.values():
            prev_char = text_widget.get(f"{cursor_index} - 1c", cursor_index)

            # If the previous character is the corresponding opening character, do not insert the closing character
            if prev_char in matching_pairs and matching_pairs[prev_char] == char:
                return "break"  # Prevent inserting the closing character

        # Handle backspace behavior for matching pairs (single characters and HTML tags)
        if event.keysym == 'BackSpace':
            prev_char = text_widget.get(f"{cursor_index} - 1c", cursor_index)

            # Handle backspace for single character pairs (like '(', '[', etc.)
            if prev_char in matching_pairs:
                next_char = text_widget.get(f"{cursor_index} + 1c", f"{cursor_index} + 2c")
                if next_char == matching_pairs[prev_char]:  # If it's the matching closing character
                    text_widget.delete(f"{cursor_index} - 1c", f"{cursor_index} + 2c")
                    text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                    return "break"  # Stop the default backspace behavior

            # Handle backspace for HTML tag pairs (like '<div>' and '</div>', etc.)
            if prev_char == '>' and text_widget.get(f"{cursor_index} - 2c", cursor_index) == '<':
                # This is the closing tag, delete both opening and closing tag
                text_widget.delete(f"{cursor_index} - 2c", f"{cursor_index} + 1c")
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 2c")
                return "break"

            elif prev_char == '-' and text_widget.get(f"{cursor_index} - 2c", cursor_index) == '<' and text_widget.get(f"{cursor_index} + 1c", f"{cursor_index} + 2c") == '-':
                # This is the comment end '-->', delete both start and end
                text_widget.delete(f"{cursor_index} - 4c", f"{cursor_index} + 3c")
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 4c")
                return "break"

        return None   # Prevent inserting the closing character if it's already matched

   
    def pyautocomplete(self, event, text_widget):
        """
        Automatically complete parentheses, brackets, braces, and quotes when typing in Python files.
        Places the cursor between the opening and closing characters after insertion.
        Handles backspace correctly.
        """
        char = event.char  # Get the character typed
        cursor_index = text_widget.index(tk.INSERT)  # Get the current cursor position

        # Define pairs of opening and closing characters
        matching_pairs = {
            '(': ')',
            '[': ']',
            '{': '}',
            "'": "'",
            '"': '"',
            '"""':'"""'
        }

        # If the character is an opening character
           # If the character is an opening character
        if char in matching_pairs:
            if char == '<':  # Special handling for '<' which can lead to tag insertion
                text_widget.insert(cursor_index, matching_pairs[char])
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                return "break"  # Prevent default insert behavior for opening '<'
            else:
                # Insert the closing character for the respective pair
                text_widget.insert(cursor_index, matching_pairs[char])
                # Move the cursor back between the characters
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                return "break"  # Prevent the default insert behavior

        # If the character is a closing character (e.g., ')', '>', '"', etc.)
        elif char in matching_pairs.values():
            prev_char = text_widget.get(f"{cursor_index} - 1c", cursor_index)

            # If the previous character is the corresponding opening character, do not insert the closing character
            if prev_char in matching_pairs and matching_pairs[prev_char] == char:
                return "break"  # Prevent inserting the closing character

        # Handle backspace behavior for matching pairs (single characters and HTML tags)
        if event.keysym == 'BackSpace':
            prev_char = text_widget.get(f"{cursor_index} - 1c", cursor_index)

            # Handle backspace for single character pairs (like '(', '[', etc.)
            if prev_char in matching_pairs:
                next_char = text_widget.get(f"{cursor_index} + 1c", f"{cursor_index} + 2c")
                if next_char == matching_pairs[prev_char]:  # If it's the matching closing character
                    text_widget.delete(f"{cursor_index} - 1c", f"{cursor_index} + 2c")
                    text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                    return "break"  # Stop the default backspace behavior

            # Handle backspace for HTML tag pairs (like '<div>' and '</div>', etc.)
            if prev_char == '>' and text_widget.get(f"{cursor_index} - 2c", cursor_index) == '<':
                # This is the closing tag, delete both opening and closing tag
                text_widget.delete(f"{cursor_index} - 2c", f"{cursor_index} + 1c")
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 2c")
                return "break"

            elif prev_char == '-' and text_widget.get(f"{cursor_index} - 2c", cursor_index) == '<' and text_widget.get(f"{cursor_index} + 1c", f"{cursor_index} + 2c") == '-':
                # This is the comment end '-->', delete both start and end
                text_widget.delete(f"{cursor_index} - 4c", f"{cursor_index} + 3c")
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 4c")
                return "break"

        return None   # Prevent inserting the closing character if it's already matched
    def cautocomplete(self, event, text_widget):
        """
        Automatically complete parentheses, brackets, braces, and quotes when typing in Python files.
        Places the cursor between the opening and closing characters after insertion.
        Handles backspace correctly.
        """
        char = event.char  # Get the character typed
        cursor_index = text_widget.index(tk.INSERT)  # Get the current cursor position

        # Define pairs of opening and closing characters
        matching_pairs = {
            '(': ')',
            '[': ']',
            '{': '}',
            "'": "'",
            '"': '"',
            '<':'>'

        }

        # If the character is an opening character
           # If the character is an opening character
        if char in matching_pairs:
            if char == '<':  # Special handling for '<' which can lead to tag insertion
                text_widget.insert(cursor_index, matching_pairs[char])
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                return "break"  # Prevent default insert behavior for opening '<'
            else:
                # Insert the closing character for the respective pair
                text_widget.insert(cursor_index, matching_pairs[char])
                # Move the cursor back between the characters
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                return "break"  # Prevent the default insert behavior

        # If the character is a closing character (e.g., ')', '>', '"', etc.)
        elif char in matching_pairs.values():
            prev_char = text_widget.get(f"{cursor_index} - 1c", cursor_index)

            # If the previous character is the corresponding opening character, do not insert the closing character
            if prev_char in matching_pairs and matching_pairs[prev_char] == char:
                return "break"  # Prevent inserting the closing character

        # Handle backspace behavior for matching pairs (single characters and HTML tags)
        if event.keysym == 'BackSpace':
            prev_char = text_widget.get(f"{cursor_index} - 1c", cursor_index)

            # Handle backspace for single character pairs (like '(', '[', etc.)
            if prev_char in matching_pairs:
                next_char = text_widget.get(f"{cursor_index} + 1c", f"{cursor_index} + 2c")
                if next_char == matching_pairs[prev_char]:  # If it's the matching closing character
                    text_widget.delete(f"{cursor_index} - 1c", f"{cursor_index} + 2c")
                    text_widget.mark_set(tk.INSERT, f"{cursor_index} - 1c")
                    return "break"  # Stop the default backspace behavior

            # Handle backspace for HTML tag pairs (like '<div>' and '</div>', etc.)
            if prev_char == '>' and text_widget.get(f"{cursor_index} - 2c", cursor_index) == '<':
                # This is the closing tag, delete both opening and closing tag
                text_widget.delete(f"{cursor_index} - 2c", f"{cursor_index} + 1c")
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 2c")
                return "break"

            elif prev_char == '-' and text_widget.get(f"{cursor_index} - 2c", cursor_index) == '<' and text_widget.get(f"{cursor_index} + 1c", f"{cursor_index} + 2c") == '-':
                # This is the comment end '-->', delete both start and end
                text_widget.delete(f"{cursor_index} - 4c", f"{cursor_index} + 3c")
                text_widget.mark_set(tk.INSERT, f"{cursor_index} - 4c")
                return "break"

        return None   # Prevent inserting the closing character if it's already matched












    def syntax_highlight(self, text_widget):
        # Get the content of the Text widget
        content = text_widget.get("1.0", "end-1c")


        # Remove previous tags
        for tag in text_widget.tag_names():
            text_widget.tag_remove(tag, "1.0", "end")

        # Apply highlighting based on regex patterns
        self.highlight_python_syntax(text_widget, content)
        self.highlight_html_syntax(text_widget, content)
        self.highlight_js_syntax(text_widget, content)
        self.highlight_c_cpp_syntax(text_widget, content)
        self.highlight_markdown_syntax(text_widget, content)
        self.highlight_json_syntax(text_widget, content)
        self.highlight_xml_syntax(text_widget, content)
        self.highlight_css_syntax(text_widget, content)
    def highlight_c_cpp_syntax(self, text_widget, content):
        global dghffh
        if not dghffh.endswith((".c","cpp")):
            return

    # C/C++ Keywords
        c_cpp_keywords = r"\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b"
        self.highlight_syntax(text_widget, content, c_cpp_keywords, "c_keyword")

        # C/C++ Strings
        c_cpp_strings = r"(['\"])(?:(?=(\\?))\2.)*?\1"
        self.highlight_syntax(text_widget, content, c_cpp_strings, "c_string")

        # C/C++ Comments
        c_cpp_single_comments = r"//.*"
        self.highlight_syntax(text_widget, content, c_cpp_single_comments, "c_comment")

        c_cpp_multiline_comments = r"/\*.*?\*/"
        self.highlight_syntax(text_widget, content, c_cpp_multiline_comments, "c_comment")

        # C/C++ Numbers
        c_cpp_numbers = r"\b\d+(\.\d+)?\b"
        self.highlight_syntax(text_widget, content, c_cpp_numbers, "c_number")

        # C/C++ Operators
        c_cpp_operators = r"[+\-*/%&|^~<>!]"
        self.highlight_syntax(text_widget, content, c_cpp_operators, "c_operator")
    def highlight_css_syntax(self, text_widget, content):
        global dghffh
        if not dghffh.endswith(".css"):
            return
        css_selectors = r"[.#]?[a-zA-Z][\w\-]*"
        css_properties = r"[a-zA-Z\-]+(?=\s*:)"
        css_values = r":\s*[^;]+;"
        css_comments = r"/\*.*?\*/"

        self.highlight_syntax(text_widget, content, css_selectors, "css_selector")
        self.highlight_syntax(text_widget, content, css_properties, "css_property")
        self.highlight_syntax(text_widget, content, css_values, "css_value")
        self.highlight_syntax(text_widget, content, css_comments, "css_comment")

    def highlight_markdown_syntax(self, text_widget, content):
        global dghffh
        if not dghffh.endswith(".md"):
            return
        # Headers
        markdown_headers = r"^(#+)\s.*"
        self.highlight_syntax(text_widget, content, markdown_headers, "markdown_header")

        # Bold Text
        markdown_bold = r"\*\*(.*?)\*\*"
        self.highlight_syntax(text_widget, content, markdown_bold, "markdown_bold")

        # Italic Text
        markdown_italic = r"\*(.*?)\*"
        self.highlight_syntax(text_widget, content, markdown_italic, "markdown_italic")
    def highlight_json_syntax(self, text_widget, content):
        global dghffh
        if not dghffh.endswith(".json"):
            return
        # Keys
        json_keys = r"\".*?\"\s*:"
        self.highlight_syntax(text_widget, content, json_keys, "json_key")

        # Strings
        json_strings = r"\".*?\""
        self.highlight_syntax(text_widget, content, json_strings, "json_string")

        # Numbers
        json_numbers = r"\b\d+(\.\d+)?\b"
        self.highlight_syntax(text_widget, content, json_numbers, "json_number")
    def highlight_xml_syntax(self, text_widget, content):
        global dghffh
        if not dghffh.endswith(".xml"):
            return
        # Tags
        xml_tags = r"</?[\w\-]+>"
        self.highlight_syntax(text_widget, content, xml_tags, "xml_tag")

        # Attributes
        xml_attrs = r"\b\w+\s*="
        self.highlight_syntax(text_widget, content, xml_attrs, "xml_attr")

        # Strings
        xml_strings = r"\".*?\""
        self.highlight_syntax(text_widget, content, xml_strings, "xml_string")



    


    def highlight_python_syntax(self, text_widget, content):
        global dghffh
        if not dghffh.endswith(".py"):
            return
        # Python Keywords
        python_keywords = r"\b(" + "|".join(keyword.kwlist) + r")\b"
        self.highlight_syntax(text_widget, content, python_keywords, "keyword")

        # Python Functions (def)
        python_functions = r"\bdef\s+(\w+)\b"
        self.highlight_syntax(text_widget, content, python_functions, "function")

        # Python Classes (class)
        python_classes = r"\bclass\s+(\w+)\b"
        self.highlight_syntax(text_widget, content, python_classes, "class")

        # Python Strings (single and double quotes)
        python_strings = r"(['\"])(?:(?=(\\?))\2.)*?\1"
        self.highlight_syntax(text_widget, content, python_strings, "string")

        # Python Comments (single-line and multi-line)
        python_single_comments = r"#.*"
        self.highlight_syntax(text_widget, content, python_single_comments, "comment")

        python_multiline_comments = r"('''.*?'''|\"\"\".*?\")"
        self.highlight_syntax(text_widget, content, python_multiline_comments, "comment")

        # Python Imports (libraries)
        python_imports = r"\bimport\s+(\w+)"
        self.highlight_syntax(text_widget, content, python_imports, "import_lib")

        # Imported Functions (from ... import ...)
        python_import_functions = r"\bfrom\s+(\w+)\s+import\s+(\w+)"
        self.highlight_syntax(text_widget, content, python_import_functions, "import_func")

        # Highlight Functions of Imported Libraries
        python_imported_function_calls = r"(\b\w+\.\w+\()"
        self.highlight_syntax(text_widget, content, python_imported_function_calls, "import_func")

        # Python Numbers (integers and floats)
        python_numbers = r"\b\d+(\.\d+)?\b"
        self.highlight_syntax(text_widget, content, python_numbers, "number")

        # Python Operators
        python_operators = r"[\+\-\*/%&|\^~<>!]"
        self.highlight_syntax(text_widget, content, python_operators, "operator")

    def highlight_html_syntax(self, text_widget, content):
        global dghffh
        if not dghffh.endswith(".html"):
            return
        # HTML Tags
        html_tags = r"</?([a-zA-Z]+)[^>]*>"
        self.highlight_syntax(text_widget, content, html_tags, "html_tag")

        # HTML Attributes
        html_attrs = r'([a-zA-Z0-9\-]+)='
        self.highlight_syntax(text_widget, content, html_attrs, "html_attr")

        # HTML Comments
        html_comments = r"<!--.*?-->"
        self.highlight_syntax(text_widget, content, html_comments, "html_comment")

        # HTML Strings (for attribute values)
        html_strings = r"(['\"])(?:(?=(\\?))\2.)*?\1"
        self.highlight_syntax(text_widget, content, html_strings, "html_string")

    def highlight_js_syntax(self, text_widget, content):
        global dghffh
        if not dghffh.endswith(".js"):
            return
        # JavaScript Keywords
        js_keywords = r"\b(function|return|var|let|const|if|else|for|while|new|try|catch|break|continue|debugger)\b"
        self.highlight_syntax(text_widget, content, js_keywords, "js_keyword")

        # JavaScript Functions
        js_functions = r"\b\w+(?=\()"
        self.highlight_syntax(text_widget, content, js_functions, "js_function")

        # JavaScript Comments
        js_comments = r"//.*|/\*.*?\*/"
        self.highlight_syntax(text_widget, content, js_comments, "js_comment")

    def highlight_syntax(self, text_widget, content, pattern, tag):
        matches = re.finditer(pattern, content)
        for match in matches:
            text_widget.tag_add(tag, f"1.0+{match.start()}c", f"1.0+{match.end()}c")









    def scroll_up(self, text_widget):
        # Scroll up by one line
        text_widget.yview_scroll(-1, "units")

    def scroll_down(self, text_widget):
        # Scroll down by one line
        text_widget.yview_scroll(1, "units")

    def scroll_left(self, text_widget):
        # Scroll left by one unit
        text_widget.xview_scroll(-1, "units")

    def scroll_right(self, text_widget):
        # Scroll right by one unit
        text_widget.xview_scroll(1, "units")


    def on_mouse_wheel(self, event, text_widget):
        """Handle mouse wheel scrolling in the Text widget."""
        if event.delta:
            text_widget.yview_scroll(-1 if event.delta > 0 else 1, "units")
        else:  # For macOS
            text_widget.yview_scroll(-1 if event.num == 4 else 1, "units")


    def close_tab(self, frame):
        """Close the tab and remove its associated content."""
        self.tab_control.forget(frame)  # Remove the tab from the notebook






    def _write_to_file(self, file_path, content):
        with open(file_path, "w") as file:
            file.write(content)

if __name__ == "__main__":
    root = tk.Tk()
    ide = NCERTLearnIDE(root)
    root.mainloop()