import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from Apriori import read_transactions, apriori, generate_association_rules

file_entry = None

def select_file():
    global file_entry
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def print_results_to_text_widget(frequent_itemsets, association_rules, output_text_widget):
    output_text_widget.delete(1.0, tk.END)
    output_text_widget.insert(tk.END, "Frequent Item Sets and Association Rules:\n\n")
    itemset_num = 1
    current_size = len(next(iter(frequent_itemsets.keys())))
    output_text_widget.insert(tk.END, f"ItemSet#{itemset_num}\n")
    
    for itemset, support in frequent_itemsets.items():
        if len(itemset) > current_size:
            itemset_num += 1
            current_size = len(itemset)
            output_text_widget.insert(tk.END, f"\nItemSet#{itemset_num}\n")
        output_text_widget.insert(tk.END, f"{list(itemset)} : Support = {support}\n")

    output_text_widget.insert(tk.END, "\nAssociation Rules:\n")
    for rule in association_rules:
        antecedent = ' ^ '.join(map(str, rule[0]))
        consequent = ' ^ '.join(map(str, rule[1]))
        confidence = round(rule[2] * 100, 2)
        output_text_widget.insert(tk.END, f"{antecedent} => {consequent} : Confidence = {confidence}%\n")

def main():
    def analyze_data():
        global file_entry
        try:
            file_path = file_entry.get()
            min_support_val = int(min_support_entry.get())
            min_confidence_val = float(min_confidence_entry.get()) / 100
            num_records_val = int(num_records_entry.get())
            num_records_val = int(len(open(file_path).readlines()) * num_records_val / 100)
            
            transactions = read_transactions(file_path, num_records_val)
            frequent_itemsets = apriori(transactions, min_support_val)
            association_rules = generate_association_rules(frequent_itemsets, min_confidence_val)
            print_results_to_text_widget(frequent_itemsets, association_rules, output_text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    root = tk.Tk()
    root.title("Association Rule Mining")

    min_support_label = ttk.Label(root, text="Minimum Support Count:")
    min_support_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    min_support_entry = ttk.Entry(root)
    min_support_entry.grid(row=0, column=1, padx=10, pady=5)

    min_confidence_label = ttk.Label(root, text="Minimum Confidence (%):")
    min_confidence_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    min_confidence_entry = ttk.Entry(root)
    min_confidence_entry.grid(row=1, column=1, padx=10, pady=5)

    num_records_label = ttk.Label(root, text="Number of Records to Use (%):")
    num_records_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    num_records_entry = ttk.Entry(root)
    num_records_entry.grid(row=2, column=1, padx=10, pady=5)

    file_label = ttk.Label(root, text="Select CSV File:")
    file_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    global file_entry
    file_entry = ttk.Entry(root)
    file_entry.grid(row=3, column=1, padx=10, pady=5)

    file_button = ttk.Button(root, text="Browse", command=select_file)
    file_button.grid(row=3, column=2, padx=10, pady=5)

    analyze_button = ttk.Button(root, text="Analyze Data", command=analyze_data)
    analyze_button.grid(row=4, columnspan=2, padx=10, pady=10)

    output_text = tk.Text(root, wrap="word", height=20, width=80)
    output_text.grid(row=5, columnspan=3, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()