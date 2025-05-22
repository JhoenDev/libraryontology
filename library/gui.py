from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox
from search_documents import search_documents

def run_search():
    keyword = entry_keyword.get().strip()
    doc_type = type_var.get() or None
    category = category_var.get() or None
    college = college_var.get() or None
    date_filter = entry_date.get().strip() or None

    if not keyword:
        messagebox.showwarning("Input Needed", "Please enter a keyword.")
        return

    results = search_documents(keyword, doc_type, category, college, date_filter)
    display_results(results, keyword)

def browse_documents():
    doc_type = type_var.get() or None
    category = category_var.get() or None
    college = college_var.get() or None
    date_filter = entry_date.get().strip() or None

    results = search_documents("", doc_type, category, college, date_filter)
    display_results(results)

def display_results(results, keyword=None):
    result_box.configure(state='normal')
    result_box.delete(1.0, tk.END)

    if results:
        if keyword:
            header = f"📚 Found {len(results)} Recommended Documents related to \"{keyword}\":\n\n"
            result_box.insert(tk.END, header)

        for i, doc in enumerate(results, 1):
            result_text = f"{i}. Title: {doc.get('title', 'N/A')}\n" \
                          f"   Author: {doc.get('author', 'N/A')}\n" \
                          f"   Date: {doc.get('date', 'N/A')}\n" \
                          f"   Type: {doc.get('type', 'N/A')}, " \
                          f"Category: {doc.get('category', 'N/A')}, " \
                          f"College: {doc.get('college', 'Unknown')}\n" \
                          f"   Keywords: {', '.join(doc.get('keywords', []))}\n" \
                          f"   Abstract: {doc.get('abstract', 'N/A')}\n\n"
            result_box.insert(tk.END, result_text)
    else:
        if keyword:
            result_box.insert(tk.END, f"No matching documents found for \"{keyword}\".")
        else:
            result_box.insert(tk.END, "No documents found.")

    result_box.configure(state='disabled')

# Create main window with theme
root = ThemedTk(theme="clearlooks")
root.title("📚 Library Document Recommender")
root.geometry("850x650")

# Apply style
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("TCombobox", font=("Segoe UI", 10))

# Title
title_label = ttk.Label(root, text="Library Document Recommender", font=("Segoe UI", 16, "bold"))
title_label.pack(pady=(20, 10))

# Input frame
frame_input = ttk.LabelFrame(root, text="What topic are you looking for?", padding=15)
frame_input.pack(fill=tk.X, padx=20, pady=10)

# Keyword
ttk.Label(frame_input, text="Keywords:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_keyword = ttk.Entry(frame_input, width=50)
entry_keyword.grid(row=0, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

# Filters
ttk.Label(frame_input, text="Type (Optional):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
type_var = ttk.Combobox(frame_input, values=["", "Article", "Book", "Research"], width=20)
type_var.grid(row=1, column=1, sticky=tk.W, padx=5)

ttk.Label(frame_input, text="Category (Optional):").grid(row=1, column=2, sticky=tk.W, padx=5)
category_var = ttk.Combobox(frame_input, values=["", "Math", "Science", "Computer"], width=20)
category_var.grid(row=1, column=3, sticky=tk.W, padx=5)

ttk.Label(frame_input, text="College (Optional):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
college_var = ttk.Combobox(frame_input, values=["", "College of Engineering", "College of Computer Science", "College of Law"], width=30)
college_var.grid(row=2, column=1, sticky=tk.W, padx=5)

ttk.Label(frame_input, text="Date (YYYY or YYYY-MM):").grid(row=2, column=2, sticky=tk.W, padx=5)
entry_date = ttk.Entry(frame_input, width=20)
entry_date.grid(row=2, column=3, sticky=tk.W, padx=5)

# Buttons
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)

btn_search = ttk.Button(frame_buttons, text="🔍 Search Documents", command=run_search)
btn_search.grid(row=0, column=0, padx=10)

btn_browse = ttk.Button(frame_buttons, text="📂 Browse All Documents", command=browse_documents)
btn_browse.grid(row=0, column=1, padx=10)

# Results frame
frame_results = ttk.Frame(root)
frame_results.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

scrollbar = ttk.Scrollbar(frame_results)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_box = tk.Text(frame_results, wrap=tk.WORD, font=("Segoe UI", 10), yscrollcommand=scrollbar.set, state='disabled')
result_box.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=result_box.yview)

# Start the GUI
root.mainloop()
