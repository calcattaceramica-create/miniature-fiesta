#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Launcher - Simple Version
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_window():
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("400x300")
    
    label = tk.Label(root, text="If you see this, Tkinter works!", font=("Arial", 14))
    label.pack(pady=50)
    
    button = tk.Button(root, text="Click Me", command=lambda: messagebox.showinfo("Success", "Button works!"))
    button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    try:
        test_window()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

