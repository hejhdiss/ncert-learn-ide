import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup

class PackageManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Package Manager")
        self.root.geometry("800x600")
        self.create_widgets()

    def log_output(self, message, clear=False):
        """Logs messages to the output text area."""
        if clear:
            self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)  # Auto-scroll to the bottom

    def create_widgets(self):
        """Creates the main UI components."""
        # Search bar
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(search_frame, text="Search for packages:").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_pypi).pack(side="left", padx=5)

        # Results list with scrollbar
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.result_listbox = tk.Listbox(self.result_frame, bg="#1e1e1e", fg="white", height=20)
        self.result_listbox.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(self.result_frame, orient="vertical", command=self.result_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_listbox.config(yscrollcommand=scrollbar.set)

        # Output text area
        self.output_text = scrolledtext.ScrolledText(self.root, height=10, bg="#1e1e1e", fg="white")
        self.output_text.pack(fill="both", padx=10, pady=5)

    def search_pypi(self):
        """Searches PyPI for packages matching the query."""
        query = self.search_entry.get().strip()
        if not query:
            self.log_output("Please enter a package name or keyword to search.", clear=True)
            return

        self.log_output(f"Searching PyPI for '{query}'...", clear=True)
        try:
            # Fetch search results from PyPI
            url = f"https://pypi.org/search/?q={query}"
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            # Parse HTML response
            soup = BeautifulSoup(response.text, "html.parser")
            package_elements = soup.find_all("a", class_="package-snippet")

            if not package_elements:
                self.log_output("No packages found matching your query.", clear=False)
                return

            # Display package names
            self.result_listbox.delete(0, tk.END)
            for element in package_elements:
                package_name = element.find("span", class_="package-snippet__name").text.strip()
                package_version = element.find("span", class_="package-snippet__version").text.strip()
                self.result_listbox.insert(tk.END, f"{package_name} ({package_version})")
                self.log_output(f"Found: {package_name} ({package_version})")

        except Exception as e:
            self.log_output(f"Error during search: {e}", clear=False)

    def run(self):
        """Runs the Tkinter main loop."""
        self.root.mainloop()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = PackageManagerApp(root)
    app.run()
