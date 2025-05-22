import tkinter as tk
from tkinter import ttk
from search_documents import search_documents

def recommend_documents():
    purpose = purpose_var.get()
    field = field_var.get()
    material = material_var.get()
    college = college_var.get()
    date = entry_date.get().strip() or None

    # Rules: map "purpose" + "field" to type/category
    doc_type = None
    category = field if field else None

    if purpose == "Project":
        doc_type = "Research"
    elif purpose == "Study":
        doc_type = "Book"
    elif purpose == "Publication":
        doc_type = "Article"

    results = search_documents(
        keyword="",  # empty keyword, we rely on filters
        doc_type=doc_type,
        category=category,
        college=college,
        date_filter=date
    )

    result_box.delete(1.0, tk.END)

    if results:
        result_box.insert(tk.END, f"📘 Recommended Documents ({len(results)} found):\n\n")
        for i, doc in enumerate(results, 1):
            result_text = f"{i}. Title: {doc['title']}\n" \
                          f"   Author: {doc['author']}\n" \
                          f"   Date: {doc['date']}\n" \
                          f"   Type: {doc['type']}, Category: {doc['category']}, College: {doc['college']}\n" \
                          f"   Keywords: {', '.join(doc['keywords'])}\n" \
                          f"   Abstract: {doc['abstract']}\n\n"
            result_box.insert(tk.END, result_text)
    else:
        result_box.insert(tk.END, "⚠️ No suitable recommendations found. Try changing preferences.")

# GUI Setup
root = tk.Tk()
root.title("📚 Expert System Library Assistant")
root.geometry("800x600")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.X)

# Purpose
ttk.Label(frame, text="What is your purpose?").grid(row=0, column=0, sticky=tk.W)
purpose_var = ttk.Combobox(frame, values=["", "Study", "Project", "Publication"], width=20)
purpose_var.grid(row=0, column=1, sticky=tk.W)

# Field
ttk.Label(frame, text="Field of interest:").grid(row=1, column=0, sticky=tk.W)
field_var = ttk.Combobox(frame, values=["", "Math", "Science", "Computer"], width=20)
field_var.grid(row=1, column=1, sticky=tk.W)

# Material
ttk.Label(frame, text="Preferred material:").grid(row=2, column=0, sticky=tk.W)
material_var = ttk.Combobox(frame, values=["", "Book", "Article", "Research"], width=20)
material_var.grid(row=2, column=1, sticky=tk.W)

# College
ttk.Label(frame, text="College (optional):").grid(row=3, column=0, sticky=tk.W)
college_var = ttk.Combobox(frame, values=["", "College of Computer Science"], width=30)
college_var.grid(row=3, column=1, sticky=tk.W)

# Date
ttk.Label(frame, text="Published date (YYYY or YYYY-MM):").grid(row=4, column=0, sticky=tk.W)
entry_date = ttk.Entry(frame, width=20)
entry_date.grid(row=4, column=1, sticky=tk.W)

# Recommend button
ttk.Button(frame, text="🤖 Recommend", command=recommend_documents).grid(row=5, column=0, columnspan=2, pady=10)

# Result display
result_box = tk.Text(root, wrap=tk.WORD)
result_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
