import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class FolderStructureAnalyzer:
    def __init__(self, folder_path, exclude_folders=None):
        self.folder_path = folder_path
        self.structure_lines = []
        self.exclude_folders = set(exclude_folders or [])

    def validate_folder(self):
        if not os.path.isdir(self.folder_path):
            raise NotADirectoryError(f"Directory not found: {self.folder_path}")

    def analyze(self):
        self.validate_folder()
        for root, dirs, files in os.walk(self.folder_path):
            dirs[:] = [d for d in dirs if d not in self.exclude_folders]
            level = root.replace(self.folder_path, '').count(os.sep)
            indent = ' ' * 4 * level
            self.structure_lines.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                self.structure_lines.append(f"{subindent}{f}")

    def get_structure_text(self):
        return '\n'.join(self.structure_lines)

class FolderStructureApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Folder Structure Analyzer')

        # Folder path input
        self.folder_label = tk.Label(root, text='Folder Path:')
        self.folder_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.folder_entry = tk.Entry(root, width=60)
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = tk.Button(root, text='Browse', command=self.browse_folder)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Exclude folders input
        self.exclude_label = tk.Label(root, text='Exclude Subfolders (comma separated):')
        self.exclude_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        self.exclude_entry = tk.Entry(root, width=60)
        self.exclude_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Analyze button
        self.analyze_button = tk.Button(root, text='Analyze', command=self.analyze_folder)
        self.analyze_button.grid(row=2, column=1, sticky='ew', padx=5, pady=10)

        # Output text area
        self.output_text = scrolledtext.ScrolledText(root, width=80, height=30)
        self.output_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)

    def analyze_folder(self):
        folder_path = self.folder_entry.get().strip()
        exclude_input = self.exclude_entry.get().strip()
        exclude_folders = [name.strip() for name in exclude_input.split(',')] if exclude_input else []

        analyzer = FolderStructureAnalyzer(folder_path, exclude_folders)
        try:
            analyzer.analyze()
            structure_text = analyzer.get_structure_text()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, structure_text)
        except Exception as e:
            messagebox.showerror('Error', str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderStructureApp(root)
    root.mainloop()
