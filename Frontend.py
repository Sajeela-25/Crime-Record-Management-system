#!/usr/bin/env python
# coding: utf-8

# In[5]:


import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from tkinter import font as tkfont
import hashlib  # For password hashing
from datetime import datetime

# Dark criminal/murder-themed color scheme
BG_COLOR = "#121212"       # Almost black background
HEADER_COLOR = "#8B0000"   # Dark red (blood-like)
BUTTON_COLOR = "#B22222"   # Firebrick red
ACCENT_COLOR = "#FF4500"   # Orange-red accent
TEXT_COLOR = "#E0E0E0"     # Light gray text
ENTRY_BG = "#2A2A2A"       # Dark gray entry background
TREE_HEADER = "#450000"    # Dark red tree header
TREE_ODD = "#1E1E1E"       # Slightly lighter black
TREE_EVEN = "#252525"      # Dark gray
SELECTION_COLOR = "#8B0000" # Dark red for selections

class ModernButton(ttk.Button):
    """Custom styled button for consistent look"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(style='Modern.TButton')

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        
        # Configure login window as a toplevel
        self.login_window = tk.Toplevel(root)
        self.login_window.title("Admin Login")
        self.login_window.geometry("450x350")
        self.login_window.resizable(False, False)
        self.login_window.configure(bg=BG_COLOR)
        self.login_window.grab_set()  # Make it modal
        self.login_window.focus_set()  # Ensure it gets focus
        
        # Center the window
        window_width = 450
        window_height = 350
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Custom styles
        self.style = ttk.Style()
        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, font=('Segoe UI', 11))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        self.style.configure('Modern.TButton', background=BUTTON_COLOR, foreground='white', 
                           borderwidth=1, focusthickness=3, focuscolor='none')
        self.style.map('Modern.TButton', 
                     background=[('active', ACCENT_COLOR), ('pressed', '#FF6347')],
                     foreground=[('active', 'white'), ('pressed', 'white')])
        
        # Header with crime tape effect
        header_frame = tk.Frame(self.login_window, bg=HEADER_COLOR, height=80)
        header_frame.pack(fill=tk.X)
        
        # Crime tape effect using text
        crime_tape = tk.Label(header_frame, text="CRIME SCENE - DO NOT CROSS " * 3, 
                             font=('Courier', 10, 'bold'), bg='black', fg='yellow')
        crime_tape.pack(fill=tk.X)
        
        title_font = tkfont.Font(family="Impact", size=18, weight="bold")
        tk.Label(header_frame, text="CRIME RECORD SYSTEM", font=title_font, 
                bg=HEADER_COLOR, fg="black").pack(pady=10)
        
        # Login form container
        form_frame = tk.Frame(self.login_window, bg=BG_COLOR, padx=30, pady=30)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form title with warning icon
        title_frame = tk.Frame(form_frame, bg=BG_COLOR)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        tk.Label(title_frame, text="⚠", font=('Segoe UI', 14), 
                bg=BG_COLOR, fg=ACCENT_COLOR).pack(side=tk.LEFT)
        tk.Label(title_frame, text="RESTRICTED ACCESS", font=('Segoe UI', 14, 'bold'), 
                bg=BG_COLOR, fg=ACCENT_COLOR).pack(side=tk.LEFT, padx=5)
        
        # Username
        ttk.Label(form_frame, text="Username:").grid(row=1, column=0, sticky='e', pady=8)
        self.username_entry = ttk.Entry(form_frame, width=25, font=('Segoe UI', 10))
        self.username_entry.grid(row=1, column=1, pady=8, padx=10)
        
        # Password
        ttk.Label(form_frame, text="Password:").grid(row=2, column=0, sticky='e', pady=8)
        self.password_entry = ttk.Entry(form_frame, width=25, show="*", font=('Segoe UI', 10))
        self.password_entry.grid(row=2, column=1, pady=8, padx=10)
        
        # Buttons with danger styling
        btn_frame = tk.Frame(form_frame, bg=BG_COLOR)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ModernButton(btn_frame, text="LOGIN", command=self.authenticate).pack(side=tk.LEFT, padx=10)
        ModernButton(btn_frame, text="CANCEL", command=self.root.destroy).pack(side=tk.LEFT, padx=10)
        
        # Focus on username field
        self.username_entry.focus_set()
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda event: self.authenticate())
        
        # Create admin table if not exists
        self.create_admin_table()
    
    def create_admin_table(self):
        conn = None
        try:
            # Using your specified connection string
            conn = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=DESKTOP-7AP2LDP;'
                'DATABASE=projectdb;'
                'Trusted_Connection=yes;'
            )
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='AdminUsers' AND xtype='U')
                CREATE TABLE AdminUsers (
                    UserID INT IDENTITY(1,1) PRIMARY KEY,
                    Username NVARCHAR(50) NOT NULL,
                    PasswordHash NVARCHAR(128) NOT NULL,
                    Salt NVARCHAR(50) NOT NULL,
                    FullName NVARCHAR(100),
                    LastLogin DATETIME
                )
            """)
            
            # Check if default admin exists
            cursor.execute("SELECT COUNT(*) FROM AdminUsers")
            if cursor.fetchone()[0] == 0:
                # Create default admin (username: admin, password: admin123)
                salt = "somesaltvalue"
                password = "admin123"
                hashed_password = self.hash_password(password, salt)
                cursor.execute("""
                    INSERT INTO AdminUsers (Username, PasswordHash, Salt, FullName)
                    VALUES (?, ?, ?, ?)
                """, "admin", hashed_password, salt, "System Administrator")
                conn.commit()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize admin system: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def hash_password(self, password, salt):
        """Hash the password with the salt using SHA-512"""
        return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    
    def authenticate(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Validation Error", "Please enter both username and password")
            return
        
        conn = None
        try:
            # Using your specified connection string
            conn = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=DESKTOP-7AP2LDP;'
                'DATABASE=projectdb;'
                'Trusted_Connection=yes;'
            )
            cursor = conn.cursor()
            
            # Get user record
            cursor.execute("SELECT PasswordHash, Salt FROM AdminUsers WHERE Username = ?", username)
            result = cursor.fetchone()
            
            if result:
                stored_hash, salt = result
                input_hash = self.hash_password(password, salt)
                
                if input_hash == stored_hash:
                    # Update last login
                    cursor.execute("""
                        UPDATE AdminUsers 
                        SET LastLogin = GETDATE() 
                        WHERE Username = ?
                    """, username)
                    conn.commit()
                    
                    self.login_window.destroy()
                    self.on_login_success(username)
                else:
                    messagebox.showerror("Access Denied", "Invalid credentials")
            else:
                messagebox.showerror("Access Denied", "Invalid credentials")
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Authentication failed: {str(e)}")
        finally:
            if conn:
                conn.close()

class CrimeRecordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Crime Record Management System")
        self.root.geometry("1280x800")
        self.root.configure(bg=BG_COLOR)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom styles for dark theme
        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=5)
        self.style.configure('Modern.TButton', background=BUTTON_COLOR, foreground='white', 
                           borderwidth=1, focusthickness=3, focuscolor='none')
        self.style.map('Modern.TButton', 
                     background=[('active', ACCENT_COLOR), ('pressed', '#FF6347')],
                     foreground=[('active', 'white'), ('pressed', 'white')])
        
        self.style.configure('Treeview', font=('Segoe UI', 10), rowheight=25, 
                           background=TREE_ODD, fieldbackground=TREE_ODD, foreground=TEXT_COLOR)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), 
                           background=TREE_HEADER, foreground='white')
        self.style.map('Treeview', background=[('selected', SELECTION_COLOR)])
        
        # Hide main window until login
        self.root.withdraw()
        
        # Show login window
        self.show_login()
    
    def show_login(self):
        LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self, username):
        # Show main window after successful login
        self.root.deiconify()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with crime tape effect
        header_frame = tk.Frame(main_frame, bg=HEADER_COLOR, height=90)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Crime tape effect
        crime_tape = tk.Label(header_frame, text="CRIME SCENE - DO NOT CROSS " * 3, 
                             font=('Courier', 10, 'bold'), bg='black', fg='yellow')
        crime_tape.pack(fill=tk.X, pady=(5, 0))
        
        title_font = tkfont.Font(family="Impact", size=22, weight="bold")
        tk.Label(header_frame, text="CRIME RECORD MANAGEMENT SYSTEM", 
                font=title_font, bg=HEADER_COLOR, fg="black").pack(pady=10)
        
        # User info with warning symbol
        user_frame = tk.Frame(header_frame, bg=HEADER_COLOR)
        user_frame.pack(side=tk.RIGHT, padx=20)
        tk.Label(user_frame, text="☠", font=('Segoe UI', 12), 
                bg=HEADER_COLOR, fg="black").pack(side=tk.LEFT)
        user_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        tk.Label(user_frame, text=f"USER: {username.upper()}", font=user_font, 
                bg=HEADER_COLOR, fg="black").pack(side=tk.LEFT, padx=5)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg=BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - controls
        left_panel = tk.Frame(content_frame, bg=BG_COLOR, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Database connection
        self.conn = self.create_connection()
        if not self.conn:
            return
        self.cursor = self.conn.cursor()
        
        # Get all tables from the database
        try:
            self.cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
            self.tables = [row[0] for row in self.cursor.fetchall()]
            if not self.tables:
                messagebox.showinfo("Information", "No tables found in the database")
                self.tables = ["No tables found"]
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch tables: {str(e)}")
            self.tables = ["Crime", "Victim", "Petitioner", "Criminal", "Evidence", "Arrested"]
        
        # Table selection with danger styling
        table_frame = tk.LabelFrame(left_panel, text="SELECT TABLE", font=('Segoe UI', 10, 'bold'), 
                                  bg=BG_COLOR, fg=ACCENT_COLOR, padx=10, pady=10,
                                  relief=tk.GROOVE, borderwidth=2)
        table_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.selected_table = tk.StringVar()
        self.selected_table.set(self.tables[0] if self.tables else "")
        
        self.table_dropdown = ttk.Combobox(table_frame, textvariable=self.selected_table, 
                                         values=self.tables, state="readonly", font=('Segoe UI', 10))
        self.table_dropdown.pack(fill=tk.X, pady=5)
        self.table_dropdown.bind("<<ComboboxSelected>>", self.load_table_data)
        
        # Search with danger styling
        search_frame = tk.LabelFrame(left_panel, text="SEARCH RECORDS", font=('Segoe UI', 10, 'bold'), 
                                   bg=BG_COLOR, fg=ACCENT_COLOR, padx=10, pady=10,
                                   relief=tk.GROOVE, borderwidth=2)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Segoe UI', 10))
        search_entry.pack(fill=tk.X, pady=5)
        search_entry.bind('<Return>', self.search_records)
        
        ModernButton(search_frame, text="SEARCH", command=self.search_records).pack(fill=tk.X, pady=5)
        
        # CRUD Operations with danger styling
        crud_frame = tk.LabelFrame(left_panel, text="DATA OPERATIONS", font=('Segoe UI', 10, 'bold'), 
                                 bg=BG_COLOR, fg=ACCENT_COLOR, padx=10, pady=10,
                                 relief=tk.GROOVE, borderwidth=2)
        crud_frame.pack(fill=tk.X, pady=(0, 15))
        
        ModernButton(crud_frame, text="ADD NEW RECORD", command=self.open_add_dialog).pack(fill=tk.X, pady=5)
        ModernButton(crud_frame, text="EDIT SELECTED RECORD", command=self.open_edit_dialog).pack(fill=tk.X, pady=5)
        ModernButton(crud_frame, text="DELETE SELECTED RECORD", command=self.delete_record).pack(fill=tk.X, pady=5)
        ModernButton(crud_frame, text="REFRESH DATA", command=self.load_table_data).pack(fill=tk.X, pady=5)
        
        # System controls
        sys_frame = tk.LabelFrame(left_panel, text="SYSTEM", font=('Segoe UI', 10, 'bold'), 
                                bg=BG_COLOR, fg=ACCENT_COLOR, padx=10, pady=10,
                                relief=tk.GROOVE, borderwidth=2)
        sys_frame.pack(fill=tk.X)
        
        ModernButton(sys_frame, text="LOGOUT", command=self.logout).pack(fill=tk.X, pady=5)
        ModernButton(sys_frame, text="EXIT", command=self.root.destroy).pack(fill=tk.X, pady=5)
        
        # Right panel - data display
        right_panel = tk.Frame(content_frame, bg=BG_COLOR)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Treeview frame with danger styling
        tree_frame = tk.LabelFrame(right_panel, text="RECORDS", font=('Segoe UI', 10, 'bold'), 
                                 bg=BG_COLOR, fg=ACCENT_COLOR, padx=10, pady=10,
                                 relief=tk.GROOVE, borderwidth=2)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview with improved display
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Configure tags for striped rows
        self.tree.tag_configure('evenrow', background=TREE_EVEN)
        self.tree.tag_configure('oddrow', background=TREE_ODD)
        
        # Status bar with danger styling
        self.status_var = tk.StringVar()
        self.status_var.set("READY")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, 
                            anchor=tk.W, bg=HEADER_COLOR, fg='black', font=('Segoe UI', 9, 'bold'))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load initial data
        self.load_table_data()
    
    def logout(self):
        """Logout the current user and return to login screen"""
        # Clear the main application
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Close database connection
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        
        # Show login window again
        self.root.withdraw()
        self.show_login()
    
    def create_connection(self):
        try:
            # Using your specified connection string
            conn = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=DESKTOP-7AP2LDP;'
                'DATABASE=projectdb;'
                'Trusted_Connection=yes;'
            )
            return conn
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            return None
    
    def load_table_data(self, event=None):
        table_name = self.selected_table.get()
        
        if not table_name or table_name == "No tables found":
            return
            
        self.status_var.set(f"LOADING DATA FROM {table_name}...")
        self.root.update()
            
        try:
            # Clear existing data
            self.tree.delete(*self.tree.get_children())
            
            # Clear existing columns
            for col in self.tree["columns"]:
                self.tree.heading(col, text="")
                self.tree.column(col, width=0)
            
            # Get columns and their data types
            self.cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)
            columns_info = self.cursor.fetchall()
            
            # Configure tree columns
            columns = [col[0] for col in columns_info]
            self.tree["columns"] = columns
            self.tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
            
            # Set column headings and widths with appropriate sizing
            for col_name, data_type, max_length in columns_info:
                self.tree.heading(col_name, text=col_name, anchor=tk.W)
                
                # Set column width based on data type and content
                if data_type in ('varchar', 'char', 'nvarchar'):
                    width = min(250, max(100, (max_length or 20) * 9))  # Scale based on max length
                elif data_type in ('int', 'smallint', 'tinyint'):
                    width = 80
                elif data_type in ('date', 'datetime'):
                    width = 120
                else:
                    width = 100
                
                self.tree.column(col_name, width=width, anchor=tk.W)
            
            # Fetch and insert data with proper formatting
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            
            for i, row in enumerate(rows):
                formatted_row = []
                for j, value in enumerate(row):
                    # Format dates and handle NULL values
                    if value is None:
                        formatted_row.append("NULL")
                    elif isinstance(value, datetime):
                        formatted_row.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        formatted_row.append(str(value))
                
                # Add striped row effect
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", tk.END, values=formatted_row, tags=(tag,))
            
            self.status_var.set(f"LOADED {len(rows)} RECORDS FROM {table_name}")
                
        except Exception as e:
            messagebox.showerror("Database Error", f"ERROR LOADING {table_name}: {str(e)}")
            self.status_var.set(f"ERROR: {str(e)}")
    
    def search_records(self, event=None):
        table_name = self.selected_table.get()
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self.load_table_data()
            return
        
        self.status_var.set(f"SEARCHING FOR '{search_term}' IN {table_name}...")
        self.root.update()
        
        try:
            # Get column names
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE 1=0")
            columns = [column[0] for column in self.cursor.description]
            
            # Build search query
            conditions = []
            params = []
            for col in columns:
                conditions.append(f"CONVERT(VARCHAR, {col}) LIKE ?")
                params.append(f"%{search_term}%")
            
            query = f"SELECT * FROM {table_name} WHERE {' OR '.join(conditions)}"
            
            # Clear existing data
            self.tree.delete(*self.tree.get_children())
            
            # Execute search
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            
            for i, row in enumerate(rows):
                formatted_row = []
                for value in row:
                    if value is None:
                        formatted_row.append("NULL")
                    elif isinstance(value, datetime):
                        formatted_row.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        formatted_row.append(str(value))
                
                # Add striped row effect
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", tk.END, values=formatted_row, tags=(tag,))
            
            self.status_var.set(f"FOUND {len(rows)} RECORDS MATCHING '{search_term}'")
                
        except Exception as e:
            messagebox.showerror("Search Error", f"ERROR SEARCHING RECORDS: {str(e)}")
            self.status_var.set(f"SEARCH ERROR: {str(e)}")
    
    def open_add_dialog(self):
        table_name = self.selected_table.get()
        if not table_name or table_name == "No tables found":
            messagebox.showwarning("Warning", "Please select a valid table first")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add New Record - {table_name}")
        dialog.geometry("600x500")
        dialog.grab_set()
        dialog.configure(bg=BG_COLOR)
        
        # Header
        header = tk.Frame(dialog, bg=HEADER_COLOR, height=50)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"ADD NEW RECORD TO {table_name}", font=('Segoe UI', 12, 'bold'), 
                bg=HEADER_COLOR, fg="black").pack(pady=10)
        
        # Form container
        form_container = tk.Frame(dialog, bg=BG_COLOR, padx=20, pady=20)
        form_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas and scrollbar for form
        canvas = tk.Canvas(form_container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        try:
            # Get columns and their properties
            self.cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)
            columns_info = self.cursor.fetchall()
            
            entries = {}
            for i, (col_name, data_type, nullable) in enumerate(columns_info):
                # Skip identity columns
                if data_type == 'int identity':
                    continue
                    
                row_frame = tk.Frame(scrollable_frame, bg=BG_COLOR)
                row_frame.pack(fill=tk.X, pady=5)
                
                ttk.Label(row_frame, text=f"{col_name} ({data_type})", 
                         foreground=ACCENT_COLOR, width=25).pack(side=tk.LEFT, padx=5)
                
                # Create appropriate input widgets based on data type
                if data_type in ('varchar', 'char', 'nvarchar', 'text'):
                    entry = ttk.Entry(row_frame, width=30, font=('Segoe UI', 10))
                elif data_type in ('int', 'smallint', 'tinyint'):
                    entry = ttk.Entry(row_frame, width=15, validate='key', font=('Segoe UI', 10))
                    entry['validatecommand'] = (entry.register(self.validate_int), '%P')
                elif data_type in ('date', 'datetime'):
                    entry_frame = tk.Frame(row_frame, bg=BG_COLOR)
                    entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    entry = ttk.Entry(entry_frame, width=15, font=('Segoe UI', 10))
                    entry.pack(side=tk.LEFT)
                    ModernButton(entry_frame, text="📅", width=3, 
                               command=lambda e=entry: self.open_calendar(e)).pack(side=tk.LEFT, padx=5)
                elif data_type == 'bit':  # Boolean field
                    entry = ttk.Combobox(row_frame, width=5, values=["True", "False"], state="readonly", font=('Segoe UI', 10))
                    entry.set("False")
                else:
                    entry = ttk.Entry(row_frame, width=20, font=('Segoe UI', 10))
                
                if data_type not in ('date', 'datetime'):
                    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                entries[col_name] = entry
            
            # Buttons
            btn_frame = tk.Frame(scrollable_frame, bg=BG_COLOR, pady=20)
            btn_frame.pack(fill=tk.X)
            
            ModernButton(btn_frame, text="SAVE RECORD", command=lambda: self.save_record(dialog, table_name, entries, columns_info)).pack(side=tk.LEFT, padx=10)
            ModernButton(btn_frame, text="CANCEL", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load table structure: {str(e)}")
            dialog.destroy()
    
    def save_record(self, dialog, table_name, entries, columns_info):
        try:
            values = []
            column_names = []
            for col_name, data_type, nullable in columns_info:
                # Skip identity columns
                if data_type == 'int identity':
                    continue
                    
                if col_name not in entries:
                    continue
                    
                value = entries[col_name].get().strip()
                
                # Validate required fields
                if nullable == 'NO' and not value:
                    messagebox.showwarning("Validation Error", 
                                         f"{col_name} is a required field")
                    entries[col_name].focus_set()
                    return
                    
                # Convert data types
                if data_type in ('int', 'smallint', 'tinyint'):
                    value = int(value) if value else None
                elif data_type == 'bit':  # Boolean field
                    value = 1 if value == "True" else 0
                elif data_type in ('date', 'datetime'):
                    try:
                        value = datetime.strptime(value, "%Y-%m-%d")
                    except:
                        pass
                
                values.append(value)
                column_names.append(col_name)
            
            # Build and execute insert query
            placeholders = ", ".join(["?"] * len(values))
            columns_str = ", ".join(column_names)
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            self.cursor.execute(query, values)
            self.conn.commit()
            
            messagebox.showinfo("Success", "Record added successfully")
            dialog.destroy()
            self.load_table_data()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values for fields")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add record: {str(e)}")
    
    def open_edit_dialog(self):
        table_name = self.selected_table.get()
        selected = self.tree.selection()
        
        if not table_name or table_name == "No tables found":
            messagebox.showwarning("Warning", "Please select a valid table first")
            return
            
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to edit")
            return
        
        try:
            # Get selected record data
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Get columns and their properties
            self.cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)
            columns_info = self.cursor.fetchall()
            columns = [col[0] for col in columns_info]
            
            # Create dialog
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Edit Record - {table_name}")
            dialog.geometry("600x500")
            dialog.grab_set()
            dialog.configure(bg=BG_COLOR)
            
            # Header
            header = tk.Frame(dialog, bg=HEADER_COLOR, height=50)
            header.pack(fill=tk.X)
            tk.Label(header, text=f"EDIT RECORD IN {table_name}", font=('Segoe UI', 12, 'bold'), 
                    bg=HEADER_COLOR, fg="black").pack(pady=10)
            
            # Form container
            form_container = tk.Frame(dialog, bg=BG_COLOR, padx=20, pady=20)
            form_container.pack(fill=tk.BOTH, expand=True)
            
            # Canvas and scrollbar for form
            canvas = tk.Canvas(form_container, bg=BG_COLOR, highlightthickness=0)
            scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            entries = {}
            for i, (col_name, data_type, nullable) in enumerate(columns_info):
                row_frame = tk.Frame(scrollable_frame, bg=BG_COLOR)
                row_frame.pack(fill=tk.X, pady=5)
                
                ttk.Label(row_frame, text=f"{col_name} ({data_type})", 
                         foreground=ACCENT_COLOR, width=25).pack(side=tk.LEFT, padx=5)
                
                # Create appropriate input widgets based on data type
                if data_type in ('varchar', 'char', 'nvarchar', 'text'):
                    entry = ttk.Entry(row_frame, width=30, font=('Segoe UI', 10))
                elif data_type in ('int', 'smallint', 'tinyint'):
                    entry = ttk.Entry(row_frame, width=15, validate='key', font=('Segoe UI', 10))
                    entry['validatecommand'] = (entry.register(self.validate_int), '%P')
                elif data_type in ('date', 'datetime'):
                    entry_frame = tk.Frame(row_frame, bg=BG_COLOR)
                    entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    entry = ttk.Entry(entry_frame, width=15, font=('Segoe UI', 10))
                    entry.pack(side=tk.LEFT)
                    ModernButton(entry_frame, text="📅", width=3, 
                               command=lambda e=entry: self.open_calendar(e)).pack(side=tk.LEFT, padx=5)
                elif data_type == 'bit':  # Boolean field
                    entry = ttk.Combobox(row_frame, width=5, values=["True", "False"], state="readonly", font=('Segoe UI', 10))
                else:
                    entry = ttk.Entry(row_frame, width=20, font=('Segoe UI', 10))
                
                # Set initial value
                if i < len(values):
                    if data_type == 'bit':  # Boolean field
                        entry.set("True" if values[i] == "1" or values[i] == 1 or values[i] == "True" else "False")
                    else:
                        entry.insert(0, values[i])
                
                if data_type not in ('date', 'datetime'):
                    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                entries[col_name] = entry
            
            # Buttons
            btn_frame = tk.Frame(scrollable_frame, bg=BG_COLOR, pady=20)
            btn_frame.pack(fill=tk.X)
            
            ModernButton(btn_frame, text="UPDATE RECORD", 
                      command=lambda: self.update_record(dialog, table_name, entries, columns_info, values)).pack(side=tk.LEFT, padx=10)
            ModernButton(btn_frame, text="CANCEL", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load record: {str(e)}")
    
    def update_record(self, dialog, table_name, entries, columns_info, orig_values):
        try:
            # Get primary key column (first column)
            pk_col = columns_info[0][0]
            pk_value = orig_values[0]
            
            # Build SET clause and values
            set_clause = []
            new_values = []
            
            for i, (col_name, data_type, nullable) in enumerate(columns_info[1:], 1):  # Skip PK
                if col_name not in entries:
                    continue
                    
                value = entries[col_name].get().strip()
                
                # Validate required fields
                if nullable == 'NO' and not value:
                    messagebox.showwarning("Validation Error", 
                                         f"{col_name} is a required field")
                    entries[col_name].focus_set()
                    return
                    
                # Convert data types
                if data_type in ('int', 'smallint', 'tinyint'):
                    value = int(value) if value else None
                elif data_type == 'bit':  # Boolean field
                    value = 1 if value == "True" else 0
                elif data_type in ('date', 'datetime'):
                    try:
                        value = datetime.strptime(value, "%Y-%m-%d")
                    except:
                        pass
                
                set_clause.append(f"{col_name} = ?")
                new_values.append(value)
            
            query = f"UPDATE {table_name} SET {', '.join(set_clause)} WHERE {pk_col} = ?"
            self.cursor.execute(query, (*new_values, pk_value))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Record updated successfully")
            dialog.destroy()
            self.load_table_data()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values for fields")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update record: {str(e)}")
    
    def delete_record(self):
        table_name = self.selected_table.get()
        selected = self.tree.selection()
        
        if not table_name or table_name == "No tables found":
            messagebox.showwarning("Warning", "Please select a valid table first")
            return
            
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        try:
            # Get selected record data
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Get primary key column (first column) and its data type
            self.cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table_name}' 
                AND ORDINAL_POSITION = 1
            """)
            pk_col_info = self.cursor.fetchone()
            pk_col = pk_col_info[0]
            pk_data_type = pk_col_info[1].lower()
            pk_value_str = values[0]
            
            # Convert the primary key value to the correct data type
            if pk_data_type in ('int', 'smallint', 'tinyint', 'bigint'):
                try:
                    pk_value = int(pk_value_str)
                except ValueError:
                    messagebox.showerror("Error", "Primary key must be an integer")
                    return
            elif pk_data_type in ('float', 'real', 'decimal', 'numeric'):
                try:
                    pk_value = float(pk_value_str)
                except ValueError:
                    messagebox.showerror("Error", "Primary key must be a number")
                    return
            elif pk_data_type in ('date', 'datetime', 'datetime2', 'smalldatetime'):
                try:
                    pk_value = datetime.strptime(pk_value_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        pk_value = datetime.strptime(pk_value_str, "%Y-%m-%d")
                    except ValueError:
                        messagebox.showerror("Error", "Invalid date format")
                        return
            else:
                pk_value = pk_value_str  # For string types
            
            # Confirm deletion
            if not messagebox.askyesno("Confirm Delete", 
                                     f"PERMANENTLY DELETE THIS RECORD?\n{pk_col}: {pk_value_str}"):
                return
            
            # Execute delete
            self.cursor.execute(f"DELETE FROM {table_name} WHERE {pk_col} = ?", pk_value)
            self.conn.commit()
            
            messagebox.showinfo("Success", "Record deleted permanently")
            self.load_table_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record: {str(e)}")
    
    def validate_int(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def open_calendar(self, entry_widget):
        # Calendar popup for date entry
        top = tk.Toplevel(self.root)
        top.title("Select Date")
        top.geometry("300x250")
        top.configure(bg=BG_COLOR)
        top.resizable(False, False)
        
        def set_date():
            date_str = f"{year_var.get()}-{month_var.get():02d}-{day_var.get():02d}"
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, date_str)
            top.destroy()
        
        # Header
        header = tk.Frame(top, bg=HEADER_COLOR, height=40)
        header.pack(fill=tk.X)
        tk.Label(header, text="SELECT DATE", font=('Segoe UI', 10, 'bold'), 
                bg=HEADER_COLOR, fg="black").pack(pady=5)
        
        # Current date
        now = datetime.now()
        
        # Content frame
        content = tk.Frame(top, bg=BG_COLOR, padx=20, pady=15)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Year
        year_frame = tk.Frame(content, bg=BG_COLOR)
        year_frame.pack(fill=tk.X, pady=5)
        ttk.Label(year_frame, text="Year:", width=8, foreground=ACCENT_COLOR).pack(side=tk.LEFT)
        year_var = tk.IntVar(value=now.year)
        year_spin = ttk.Spinbox(year_frame, from_=1900, to=2100, width=8, textvariable=year_var, 
                  font=('Segoe UI', 10))
        year_spin.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Month
        month_frame = tk.Frame(content, bg=BG_COLOR)
        month_frame.pack(fill=tk.X, pady=5)
        ttk.Label(month_frame, text="Month:", width=8, foreground=ACCENT_COLOR).pack(side=tk.LEFT)
        month_var = tk.IntVar(value=now.month)
        month_spin = ttk.Spinbox(month_frame, from_=1, to=12, width=8, textvariable=month_var, 
                  font=('Segoe UI', 10))
        month_spin.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Day
        day_frame = tk.Frame(content, bg=BG_COLOR)
        day_frame.pack(fill=tk.X, pady=5)
        ttk.Label(day_frame, text="Day:", width=8, foreground=ACCENT_COLOR).pack(side=tk.LEFT)
        day_var = tk.IntVar(value=now.day)
        day_spin = ttk.Spinbox(day_frame, from_=1, to=31, width=8, textvariable=day_var, 
                  font=('Segoe UI', 10))
        day_spin.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Button
        btn_frame = tk.Frame(content, bg=BG_COLOR, pady=15)
        btn_frame.pack(fill=tk.X)
        ModernButton(btn_frame, text="SET DATE", command=set_date).pack()

if __name__ == "__main__":
    root = tk.Tk()
    # Ensure the root window is created but hidden initially
    root.withdraw()
    
    # Start the application
    app = CrimeRecordManager(root)
    
    # Make sure the root window event loop runs
    root.mainloop()


# In[ ]:




