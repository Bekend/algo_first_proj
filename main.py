import tkinter as tk
from tkinter import ttk, messagebox
from BST import BST
from Heap import MaxHeap


class TreeVisualizer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.node_radius = 20
        self.level_height = 80
        self.x_spacing = 200

    def draw_bst(self, root, x, y, level=1):
        if root is None:
            return x
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill="lightblue")
        self.canvas.create_text(x, y, text=f"{root.id}\n{root.name}", font=("Arial", 8))
        offset = self.x_spacing / (2 ** level)
        if root.left:
            left_x = x - offset
            self.canvas.create_line(x, y + self.node_radius,
                                    left_x, y + self.level_height - self.node_radius)
            self.draw_bst(root.left, left_x, y + self.level_height, level + 1)
        if root.right:
            right_x = x + offset
            self.canvas.create_line(x, y + self.node_radius,
                                    right_x, y + self.level_height - self.node_radius)
            self.draw_bst(root.right, right_x, y + self.level_height, level + 1)
        return x

    def draw_heap(self, root, x, y, level=1):
        if root is None:
            return x
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill="lightgreen")
        self.canvas.create_text(x, y, text=f"{root.id}\n{root.priority}", font=("Arial", 8))
        offset = self.x_spacing / (2 ** level)
        if root.left:
            left_x = x - offset
            self.canvas.create_line(x, y + self.node_radius,
                                    left_x, y + self.level_height - self.node_radius)
            self.draw_heap(root.left, left_x, y + self.level_height, level + 1)
        if root.right:
            right_x = x + offset
            self.canvas.create_line(x, y + self.node_radius,
                                    right_x, y + self.level_height - self.node_radius)
            self.draw_heap(root.right, right_x, y + self.level_height, level + 1)
        return x

class PriorityRequestSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Priority Request Management System")
        self.bst = BST()
        self.heap = MaxHeap()
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.create_add_tab()
        self.create_process_tab()
        self.create_search_tab()
        self.create_view_tab()
        self.create_visualization_tab()
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X)
        self.update_status()

    def create_add_tab(self):
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Add Request")
        container = ttk.Frame(self.add_tab)
        container.pack(fill=tk.X, pady=20)
        left_frame = ttk.Frame(container)
        left_frame.pack(side=tk.LEFT, expand=True, padx=10, anchor='n')
        right_frame = ttk.Frame(container)
        right_frame.pack(side=tk.LEFT, expand=True, padx=10, anchor='n')
        ttk.Label(left_frame, text="Add New Request").pack(pady=5)
        ttk.Label(left_frame, text="ID:").pack(pady=2)
        self.id_entry = ttk.Entry(left_frame, width=20)
        self.id_entry.pack(pady=2)
        ttk.Label(left_frame, text="Name:").pack(pady=2)
        self.name_entry = ttk.Entry(left_frame, width=20)
        self.name_entry.pack(pady=2)
        ttk.Label(left_frame, text="Priority:").pack(pady=2)
        self.priority_entry = ttk.Entry(left_frame, width=20)
        self.priority_entry.pack(pady=2)
        self.add_btn = ttk.Button(left_frame, text="Add Request", command=self.add_request)
        self.add_btn.pack(pady=10)
        ttk.Label(right_frame, text="Increase Priority").pack(pady=5)
        ttk.Label(right_frame, text="ID:").pack(pady=2)
        self.inc_id_entry = ttk.Entry(right_frame, width=20)
        self.inc_id_entry.pack(pady=2)
        ttk.Label(right_frame, text="New Priority:").pack(pady=2)
        self.new_priority_entry = ttk.Entry(right_frame, width=20)
        self.new_priority_entry.pack(pady=2)
        self.inc_btn = ttk.Button(right_frame, text="Increase Priority", command=self.increase_priority)
        self.inc_btn.pack(pady=10)
        container.pack_propagate(False)
        container.config(height=250)

    def create_process_tab(self):
        self.process_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.process_tab, text="Process Request")
        ttk.Label(self.process_tab, text="Process the highest priority request:").pack(pady=10)
        self.process_btn = ttk.Button(self.process_tab, text="Process Request", command=self.process_request)
        self.process_btn.pack(pady=10)
        self.result_frame = ttk.LabelFrame(self.process_tab, text="Processed Request")
        self.result_frame.pack(pady=10, padx=10, fill=tk.X)
        ttk.Label(self.result_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.processed_id = ttk.Label(self.result_frame, text="")
        self.processed_id.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.result_frame, text="Priority:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.processed_priority = ttk.Label(self.result_frame, text="")
        self.processed_priority.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    def create_search_tab(self):
        self.search_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.search_tab, text="Search/Delete")
        ttk.Label(self.search_tab, text="Search/Delete by ID:").pack(pady=5)
        ttk.Label(self.search_tab, text="ID:").pack(pady=5)
        self.search_id_entry = ttk.Entry(self.search_tab)
        self.search_id_entry.pack(pady=5)
        btn_frame = ttk.Frame(self.search_tab)
        btn_frame.pack(pady=10)
        self.search_btn = ttk.Button(btn_frame, text="Search", command=self.search_request)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        self.delete_btn = ttk.Button(btn_frame, text="Delete", command=self.delete_request)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        self.search_result_frame = ttk.LabelFrame(self.search_tab, text="Request Details")
        self.search_result_frame.pack(pady=10, padx=10, fill=tk.X)
        ttk.Label(self.search_result_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_result_id = ttk.Label(self.search_result_frame, text="")
        self.search_result_id.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.search_result_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_result_name = ttk.Label(self.search_result_frame, text="")
        self.search_result_name.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.search_result_frame, text="Priority:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_result_priority = ttk.Label(self.search_result_frame, text="")
        self.search_result_priority.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    def create_view_tab(self):
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_tab, text="View Structures")
        ttk.Label(self.view_tab, text="BST Contents (Pre-order):").pack(pady=5)
        self.bst_text = tk.Text(self.view_tab, height=10, width=50)
        self.bst_text.pack(pady=5, padx=10, fill=tk.BOTH)
        ttk.Label(self.view_tab, text="MaxHeap Contents (Level-order):").pack(pady=5)
        self.heap_text = tk.Text(self.view_tab, height=10, width=50)
        self.heap_text.pack(pady=5, padx=10, fill=tk.BOTH)
        self.refresh_btn = ttk.Button(self.view_tab, text="Refresh Views", command=self.update_views)
        self.refresh_btn.pack(pady=10)

    def create_visualization_tab(self):
        self.vis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.vis_tab, text="Visualization")
        bst_frame = ttk.LabelFrame(self.vis_tab, text="BST Structure")
        bst_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.bst_canvas = tk.Canvas(bst_frame, bg="white", height=300)
        self.bst_canvas.pack(fill=tk.BOTH, expand=True)
        heap_frame = ttk.LabelFrame(self.vis_tab, text="MaxHeap Structure")
        heap_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.heap_canvas = tk.Canvas(heap_frame, bg="white", height=300)
        self.heap_canvas.pack(fill=tk.BOTH, expand=True)
        self.add_scrollbars(bst_frame, self.bst_canvas)
        self.add_scrollbars(heap_frame, self.heap_canvas)
        ttk.Button(self.vis_tab, text="Refresh Visualization",
                   command=self.update_visualization).pack(pady=10)

    def add_scrollbars(self, parent, canvas):
        x_scroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=canvas.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        y_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def update_visualization(self):
        self.bst_canvas.delete("all")
        self.heap_canvas.delete("all")
        if self.bst.root:
            bst_visualizer = TreeVisualizer(self.bst_canvas)
            bst_visualizer.draw_bst(self.bst.root, 400, 50)
        if self.heap.root:
            heap_visualizer = TreeVisualizer(self.heap_canvas)
            heap_visualizer.draw_heap(self.heap.root, 400, 50)
        self.bst_canvas.configure(scrollregion=self.bst_canvas.bbox("all"))
        self.heap_canvas.configure(scrollregion=self.heap_canvas.bbox("all"))

    def add_request(self):
        try:
            id = int(self.id_entry.get())
            name = self.name_entry.get()
            priority = int(self.priority_entry.get())
            self.bst.root = self.bst.insertRequest(self.bst.root, id, name)
            self.heap.insert(id, priority)
            self.update_status()
            messagebox.showinfo("Success", "Request added successfully!")
            self.clear_add_entries()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid ID and priority (numbers)")

    def process_request(self):
        result = self.heap.processHighestPriorityRequest(self.bst)
        if result:
            req_id, priority = result
            node = self.bst.searchRequest(self.bst.root, req_id)
            name = node.name if node else "Not found in BST"
            self.processed_id.config(text=str(req_id))
            self.processed_priority.config(text=str(priority))
            self.update_status()
            messagebox.showinfo("Processed", f"Processed request: ID={req_id}, Name={name}, Priority={priority}")
        else:
            messagebox.showinfo("Info", "No requests to process")

    def search_request(self):
        try:
            req_id = int(self.search_id_entry.get())
            node = self.bst.searchRequest(self.bst.root, req_id)
            if node:
                heap_node = self.heap.find_node_by_id(req_id)
                priority = heap_node.priority if heap_node else "Not found in Heap"

                self.search_result_id.config(text=str(node.id))
                self.search_result_name.config(text=node.name)
                self.search_result_priority.config(text=str(priority))
            else:
                messagebox.showinfo("Not Found", "Request ID not found in BST")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid ID (number)")

    def delete_request(self):
        try:
            req_id = int(self.search_id_entry.get())
            self.bst.root = self.bst.deleteRequest(self.bst.root, req_id)

            heap_node = self.heap.find_node_by_id(req_id)
            if heap_node:
                self.rebuild_heap_without_id(req_id)
            self.update_status()
            messagebox.showinfo("Success", f"Request {req_id} deleted from both structures")
            self.clear_search_result()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid ID (number)")

    def increase_priority(self):
        try:
            req_id = int(self.inc_id_entry.get())
            new_priority = int(self.new_priority_entry.get())
            if self.heap.increasePriority(req_id, new_priority):
                messagebox.showinfo("Success", f"Priority for ID {req_id} increased to {new_priority}")
                self.update_status()
                self.clear_priority_entries()
            else:
                messagebox.showerror("Error", "ID not found or new priority not higher than current")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid ID and priority (numbers)")

    def rebuild_heap_without_id(self, req_id):
        nodes = self.heap.printMaxHeap()
        self.heap = MaxHeap()
        for node_id, priority in nodes:
            if node_id != req_id:
                self.heap.insert(node_id, priority)

    def update_status(self):
        bst_size = self.bst.size(self.bst.root) if self.bst.root else 0
        heap_size = self.heap.size
        self.status_var.set(f"BST Size: {bst_size} | Heap Size: {heap_size}")
        self.update_views()
        self.update_visualization()

    def update_views(self):
        self.bst_text.delete(1.0, tk.END)
        if self.bst.root:
            pre_order = self.get_bst_pre_order(self.bst.root)
            for node in pre_order:
                self.bst_text.insert(tk.END, f"ID: {node.id}, Name: {node.name}\n")
        self.heap_text.delete(1.0, tk.END)
        heap_nodes = self.heap.printMaxHeap()
        for node_id, priority in heap_nodes:
            self.heap_text.insert(tk.END, f"ID: {node_id}, Priority: {priority}\n")

    def get_bst_pre_order(self, node):
        if node is None:
            return []
        return [node] + self.get_bst_pre_order(node.left) + self.get_bst_pre_order(node.right)

    def clear_add_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

    def clear_priority_entries(self):
        self.inc_id_entry.delete(0, tk.END)
        self.new_priority_entry.delete(0, tk.END)

    def clear_search_result(self):
        self.search_result_id.config(text="")
        self.search_result_name.config(text="")
        self.search_result_priority.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = PriorityRequestSystem(root)
    root.geometry("1000x800")
    root.mainloop()