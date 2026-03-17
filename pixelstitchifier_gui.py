#!/usr/bin/env python3
"""Simple GUI wrapper for pixelstitchifier - easier for non-technical users."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading

from src.pixelstitchifier.converter import PixelstitchifierConverter


class PixelstitchifierGUI:
    """Simple GUI for cross-stitch pattern generation."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("pixelstitchifier - Cross-Stitch Pattern Generator")
        self.root.geometry("600x500")
        
        self.input_file = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create GUI elements."""
        # Title
        title = tk.Label(
            self.root, 
            text="pixelstitchifier Cross-Stitch Pattern Generator",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)
        
        # File selection
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10, padx=20, fill='x')
        
        self.file_label = tk.Label(file_frame, text="No file selected", fg="gray")
        self.file_label.pack(side='left', padx=5)
        
        tk.Button(
            file_frame,
            text="Select Image",
            command=self.select_file,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side='right')
        
        # Options frame
        opts_frame = tk.LabelFrame(self.root, text="Options", padx=20, pady=20)
        opts_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # DMC matching
        self.use_dmc = tk.BooleanVar(value=True)
        tk.Checkbutton(
            opts_frame,
            text="Match to DMC thread colors",
            variable=self.use_dmc,
            font=("Arial", 11)
        ).pack(anchor='w', pady=5)
        
        # Pixelate option
        self.pixelate = tk.BooleanVar(value=False)
        tk.Checkbutton(
            opts_frame,
            text="Convert photo to pixel art first (recommended for photos)",
            variable=self.pixelate,
            font=("Arial", 11)
        ).pack(anchor='w', pady=5)
        
        # Preset selection
        preset_frame = tk.Frame(opts_frame)
        preset_frame.pack(anchor='w', pady=10)
        
        tk.Label(preset_frame, text="Preset:", font=("Arial", 11)).pack(side='left', padx=5)
        
        self.preset = tk.StringVar(value="photo")
        presets = ["photo", "landscape", "portrait", "detailed"]
        preset_menu = ttk.Combobox(
            preset_frame,
            textvariable=self.preset,
            values=presets,
            state='readonly',
            width=15
        )
        preset_menu.pack(side='left')
        
        # Info text
        info_text = tk.Label(
            opts_frame,
            text="Presets:\n"
                 "• photo - General photos (64 colors)\n"
                 "• landscape - Scenic photos (48 colors)\n"
                 "• portrait - People (56 colors)\n"
                 "• detailed - High detail (72 colors)",
            justify='left',
            fg="gray",
            font=("Arial", 9)
        )
        info_text.pack(anchor='w', pady=10)
        
        # Generate button
        self.generate_btn = tk.Button(
            self.root,
            text="Generate Pattern",
            command=self.generate_pattern,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            state='disabled'
        )
        self.generate_btn.pack(pady=20, padx=20, fill='x')
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="Select an image to get started",
            fg="gray",
            font=("Arial", 10)
        )
        self.status_label.pack()
    
    def select_file(self):
        """Open file dialog to select image."""
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.input_file = Path(filename)
            self.file_label.config(text=self.input_file.name, fg="black")
            self.generate_btn.config(state='normal')
            self.status_label.config(
                text="Ready to generate pattern",
                fg="green"
            )
    
    def generate_pattern(self):
        """Generate cross-stitch pattern in background thread."""
        if not self.input_file:
            messagebox.showerror("Error", "Please select an image first")
            return
        
        # Disable button during processing
        self.generate_btn.config(state='disabled')
        self.status_label.config(text="Generating pattern...", fg="blue")
        
        # Run in thread to prevent GUI freeze
        thread = threading.Thread(target=self._generate)
        thread.daemon = True
        thread.start()
    
    def _generate(self):
        """Background thread for pattern generation."""
        try:
            converter = PixelstitchifierConverter(
                use_dmc=self.use_dmc.get(),
                pixelate=self.pixelate.get(),
                art_preset=self.preset.get()
            )
            
            output_path = converter.convert(self.input_file)
            
            # Update GUI from main thread
            self.root.after(0, self._on_success, output_path)
            
        except Exception as e:
            self.root.after(0, self._on_error, str(e))
    
    def _on_success(self, output_path):
        """Handle successful generation."""
        self.generate_btn.config(state='normal')
        self.status_label.config(text="✓ Pattern generated!", fg="green")
        
        message = f"Pattern saved to:\n{output_path}\n\n"
        if self.pixelate.get():
            pixelated_path = output_path.parent / f"{output_path.stem.replace('_pattern', '')}_pixelated{output_path.suffix}"
            message += f"Pixelated image saved to:\n{pixelated_path}"
        
        messagebox.showinfo("Success", message)
    
    def _on_error(self, error_msg):
        """Handle generation error."""
        self.generate_btn.config(state='normal')
        self.status_label.config(text="✗ Error occurred", fg="red")
        messagebox.showerror("Error", f"Failed to generate pattern:\n{error_msg}")


def main():
    """Run GUI application."""
    root = tk.Tk()
    app = PixelstitchifierGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
