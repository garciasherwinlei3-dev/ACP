import sqlite3 
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkintermapview import TkinterMapView
from tkinter import messagebox
import requests

DB_FILE = "Disaster_info.db"

def init_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS Disaster_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Disaster_type TEXT,
            Name TEXT,
            Date TEXT,
            Location TEXT,
            Overview TEXT,
            Safety_Tips TEXT)""")
    conn.commit()
    conn.close()
    # ============== HOTLINE INTERFACE ===============
def open_hotline():
    hotline = tk.Toplevel()
    hotline.title("Emergency Hotlines")
    hotline.geometry("500x600")
    hotline.configure(bg="#1f1f1f")

    TITLE_COLOR = "gold"
    TEXT_COLOR = "white"
    BG_BOX = "#111111"

    tk.Label(
        hotline,
        text="📞 Emergency Hotlines",
        font=("Georgia", 20, "bold"),
        fg=TITLE_COLOR,
        bg="#1f1f1f"
    ).pack(pady=15)

    container = tk.Frame(hotline, bg="#1f1f1f")
    canvas = tk.Canvas(container, bg="#1f1f1f", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#1f1f1f")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    container.pack(fill="both", expand=True, padx=10)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    hotlines = [
        ("🚓 Police Hotline", "911"),
        ("🚒 Fire Department", "911"),
        ("🚑 Medical Emergency", "911"),
        ("📞 National Disaster Risk Reduction (NDRRMC)", "02-8911-1406"),
        ("🌊 Philippine Coast Guard", "0917-852-8767"),
        ("🚨 Emergency Traffic Hotline", "136"),
        ("⚡ Meralco Hotline", "16211"),
        ("💧 Maynilad Water Hotline", "1626"),
        ("💧 Manila Water Hotline", "1627"),
        ("📡 Globe Telecom", "211"),
        ("📡 Smart Communications", "888"),
    ]

    for name, number in hotlines:
        box = tk.Frame(scroll_frame, bg=BG_BOX, bd=1, relief="solid")
        box.pack(fill="x", padx=10, pady=7)

        tk.Label(
            box,
            text=name,
            font=("Georgia", 14, "bold"),
            fg="gold",
            bg=BG_BOX,
            anchor="w"
        ).pack(padx=10, pady=(10, 0), fill="x")

        tk.Label(
            box,
            text=f"📱 Contact Number: {number}",
            font=("Georgia", 12),
            fg=TEXT_COLOR,
            bg=BG_BOX,
            anchor="w"
        ).pack(padx=10, pady=(0, 10), fill="x")

        def copy_to_clipboard(num=number):
            hotline.clipboard_clear()
            hotline.clipboard_append(num)

        tk.Button(
            box,
            text="Copy Number",
            bg="gold",
            fg="black",
            command=copy_to_clipboard
        ).pack(pady=5)
    #====================== DISASTER INFO INTERFACE ==============
def open_disaster_info():
    win = tk.Toplevel()
    win.title("Disaster Information")
    win.geometry("1000x750")
    win.configure(bg="white")

    # ===================== HEADER =====================
    tk.Label(
        win,
        text="🌋 Disaster Information (CRUD)",
        font=("Georgia", 22, "bold"),
        fg="black",
        bg="white"
    ).pack(pady=20)

    # ===================== MAIN CONTAINER (Centered) =====================
    main_container = tk.Frame(win, bg="white")
    main_container.pack(expand=True)  # <-- centers content

    # ===================== FORM CONTAINER =====================
    form = tk.Frame(main_container, bg="white")
    form.pack(pady=10)

    # --------- Form Inputs ----------
    labels = ["Disaster Type:", "Name:", "Date:", "Location of Landfall:", "Overview:", "Safety Tips:"]
    
    tk.Label(form, text=labels[0], bg="white").grid(row=0, column=0, sticky="w", pady=3)
    entry_type = tk.Entry(form, width=45)
    entry_type.grid(row=0, column=1, pady=3)

    tk.Label(form, text=labels[1], bg="white").grid(row=1, column=0, sticky="w", pady=3)
    entry_name = tk.Entry(form, width=45)
    entry_name.grid(row=1, column=1, pady=3)

    tk.Label(form, text=labels[2], bg="white").grid(row=2, column=0, sticky="w", pady=3)
    entry_date = tk.Entry(form, width=45)
    entry_date.grid(row=2, column=1, pady=3)

    tk.Label(form, text=labels[3], bg="white").grid(row=3, column=0, sticky="w", pady=3)
    entry_location = tk.Entry(form, width=45)
    entry_location.grid(row=3, column=1, pady=3)

    tk.Label(form, text=labels[4], bg="white").grid(row=4, column=0, sticky="nw", pady=3)
    entry_overview = tk.Text(form, width=45, height=4)
    entry_overview.grid(row=4, column=1, pady=3)

    tk.Label(form, text=labels[5], bg="white").grid(row=5, column=0, sticky="nw", pady=3)
    entry_tips = tk.Text(form, width=45, height=4)
    entry_tips.grid(row=5, column=1, pady=3)

    # ===================== CRUD Functions =====================
    def clear_form():
        entry_type.delete(0, "end")
        entry_name.delete(0, "end")
        entry_date.delete(0, "end")
        entry_location.delete(0, "end")
        entry_overview.delete("1.0", "end")
        entry_tips.delete("1.0", "end")

    def add_data():
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            INSERT INTO Disaster_info (Disaster_type, Name, Date, Location, Overview, Safety_Tips)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry_type.get(),
            entry_name.get(),
            entry_date.get(),
            entry_location.get(),
            entry_overview.get("1.0", "end").strip(),
            entry_tips.get("1.0", "end").strip()
        ))
        conn.commit()
        conn.close()
        load_data()
        clear_form()

    def update_data():
        selected = table.selection()
        if not selected:
            return messagebox.showwarning("Warning", "Select a record to update.")
        record_id = table.item(selected)["values"][0]

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            UPDATE Disaster_info
            SET Disaster_type=?, Name=?, Date=?, Location=?, Overview=?, Safety_Tips=?
            WHERE id=?
        """, (
            entry_type.get(),
            entry_name.get(),
            entry_date.get(),
            entry_location.get(),
            entry_overview.get("1.0", "end").strip(),
            entry_tips.get("1.0", "end").strip(),
            record_id
        ))
        conn.commit()
        conn.close()
        load_data()
        clear_form()

    def delete_data():
        selected = table.selection()
        if not selected:
            return messagebox.showwarning("Warning", "Select a record to delete.")
        record_id = table.item(selected)["values"][0]

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM Disaster_info WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        load_data()
        clear_form()

    # ===================== BUTTONS (Centered) =====================
    btn_frame = tk.Frame(main_container, bg="white")
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Add", width=12, command=add_data).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Update", width=12, command=update_data).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="Delete", width=12, command=delete_data).grid(row=0, column=2, padx=10)
    tk.Button(btn_frame, text="Clear", width=12, command=clear_form).grid(row=0, column=3, padx=10)

    # ===================== TABLE (Centered) =====================
    table_frame = tk.Frame(main_container, bg="white")
    table_frame.pack(pady=10)

    columns = ("ID", "Disaster_Type", "Name", "Date", "Location", "Overview", "Safety_Tips")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=140)

    table.pack(side="left")
    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar.pack(side="right", fill="y")
    table.configure(yscrollcommand=scrollbar.set)

    def load_data():
        for row in table.get_children():
            table.delete(row)
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        for row in c.execute("SELECT * FROM Disaster_info"):
            table.insert("", "end", values=row)
        conn.close()

    def on_select(event):
        selected = table.selection()
        if not selected:
            return
        data = table.item(selected)["values"]
        clear_form()
        entry_type.insert(0, data[1])
        entry_name.insert(0, data[2])
        entry_date.insert(0, data[3])
        entry_location.insert(0, data[4])
        entry_overview.insert("1.0", data[5])
        entry_tips.insert("1.0", data[6])

    table.bind("<<TreeviewSelect>>", on_select)

    init_database()
    load_data()

def open_send_safe():
    win = tk.Toplevel()
    win.title("Send Safe/Location")
    win.geometry("500x600")
    win.configure(bg="#1e1e1e")

    tk.Label(
        win, text="Send Safe/Location",
        font=("Times New Roman", 20, "bold"),
        bg="#1e1e1e", fg="white"
    ).pack(pady=10)

    tk.Label(win, text="Your Name:", bg="#1e1e1e", fg="white").pack()
    name_entry = tk.Entry(win, font=("Arial", 12), width=40)
    name_entry.pack(pady=5)

    tk.Label(win, text="Message:", bg="#1e1e1e", fg="white").pack()
    msg_entry = tk.Text(win, font=("Arial", 12), height=3, width=40)
    msg_entry.insert("1.0", "I am safe.")
    msg_entry.pack(pady=5)

    tk.Label(win, text="Detected Location:", bg="#1e1e1e", fg="white").pack()
    location_entry = tk.Entry(win, font=("Arial", 12), width=40)
    location_entry.pack(pady=5)

    tk.Label(win, text="Send To (Number or Email):", bg="#1e1e1e", fg="white").pack()
    contact_entry = tk.Entry(win, font=("Arial", 12), width=40)
    contact_entry.pack(pady=5)

    def detect_location():
        try:
            res = requests.get("https://ipinfo.io/json").json()
            city = res.get("city", "Unknown")
            region = res.get("region", "Unknown")
            country = res.get("country", "Unknown")
            loc = res.get("loc", "")

            full_location = f"{city}, {region}, {country} ({loc})"
            location_entry.delete(0, tk.END)
            location_entry.insert(0, full_location)

            messagebox.showinfo("Success", "Auto-location detected!")

        except:
            messagebox.showerror("Error", "Unable to detect location.\nCheck your internet.")

    tk.Button(
        win, text="Detect My Location",
        bg="#c8442d", fg="white",
        font=("Arial", 12, "bold"), width=18,
        command=detect_location
    ).pack(pady=8)

    def send_message():
        name = name_entry.get()
        msg = msg_entry.get("1.0", tk.END).strip()
        loc = location_entry.get()
        contact = contact_entry.get()

        if not name or not msg or not loc or not contact:
            return messagebox.showerror("Error", "All fields are required.")

        final = f"""
            Message Sent Successfully!

            Name: {name}
            Message: {msg}
            Location: {loc}
            Sent To: {contact}
            """

        messagebox.showinfo("Success", final)

    tk.Button(
        win, text="Send",
        bg="#2e8b57", fg="white",
        font=("Arial", 12, "bold"), width=15,
        command=send_message
    ).pack(pady=15)

    tk.Button(
        win, text="Close",
        bg="gray", fg="white",
        font=("Arial", 12), width=15,
        command=win.destroy
    ).pack()

def open_dashboard():
    dash = tk.Toplevel()
    dash.title("Dashboard")
    dash.geometry("900x600")

    
    BG_DARK = "#1f1f1f"     
    BG_TEXT_BOX = "#111111"
    BG_LIGHT = "#ffffff"    
    TEXT_COLOR = "white"    
    ACCENT_COLOR = "gold"   

    dash.configure(bg=BG_DARK)
    
    dash.background_image = None 
    content_height = 450 
    
    content_y_start = 151 
    content_height_adjusted = content_height - 1


    top_bar = tk.Frame(dash, bg=BG_DARK, height=70, width=900)
    top_bar.place(x=0, y=0)
    
    features = tk.Frame(dash, bg=BG_DARK, height=80, width=900)
    features.place(x=0, y=70)
    
    content = tk.Frame(dash, bg=BG_LIGHT)
    content.place(x=0, y=content_y_start, width=900, height=content_height_adjusted) 
    
    bg_label = None
    try:
        original_content_image = Image.open("ready2.jpg")
        resized_content_image = original_content_image.resize((900, content_height_adjusted), Image.LANCZOS)
        dash.content_background_image = ImageTk.PhotoImage(resized_content_image)

        bg_label = tk.Label(content, image=dash.content_background_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower() 

    except (FileNotFoundError, ImportError):
        pass
    
    side_width = 200

    side_navigation = tk.Frame(dash, bg=BG_LIGHT, width=side_width, height=600)
    side_navigation.place(x=-side_width, y=0)

    dash.nav_open = False

    def toggle_navigation():
        if dash.nav_open:
            side_navigation.place(x=-side_width, y=30)
            dash.nav_open = False
        else:
            side_navigation.place(x=0, y=30)
            dash.nav_open = True

        side_navigation.lift()
        top_bar.lift()

    
    menu_items = ["Home", "Profile", "Services", "About Us", "Survey/Feedback"]
    for i, item in enumerate(menu_items):
        tk.Button(
            side_navigation, text=item,
            bg=BG_LIGHT, bd=0, anchor="w", font=("Georgia", 12), fg="#333333"
        ).place(x=20, y=50 + i*40)

    
    top_bar.lift() 

    navigation_btn = tk.Button(
        top_bar, text="☰", font=("Georgia", 18),
        bg=BG_DARK, bd=0, command=toggle_navigation, fg=TEXT_COLOR
    )
    navigation_btn.place(x=10, y=15)

    tk.Label(top_bar, text="BE AWARE, BE SAFE",
             font=("Georgia", 26, "bold"), bg=BG_DARK, fg=TEXT_COLOR).place(relx=0.5, y=20, anchor="n")

    
    features.lift() 

    button_width = 30
    button_height = 5
    
    button_style = {"bg": "#333333", "fg": ACCENT_COLOR, "activebackground": "#555555", "activeforeground": "white", "bd": 1}

    def open_evacuation_map():
        map_window = tk.Toplevel(dash)
        map_window.title("Evacuation Map")
        map_window.geometry("900x600")

        map_widget = TkinterMapView(map_window, width= 900, height= 600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)

        map_widget.set_position(14.5995, 120.9842)
        map_widget.set_zoom(12)

        map_widget.set_marker(14.5995, 120.9842, text= "Evacuation Point")

    
    tk.Button(features, text="Evacuation Area", width=button_width, height=button_height, command= open_evacuation_map, **button_style).place(x=10, y=10)

    tk.Button(features, text="Hotline", width=button_width, height=button_height,command=open_hotline, **button_style).place(x=230, y=10)

    tk.Button(features, text="Disaster Info", width=button_width, height=button_height,command=open_disaster_info, **button_style).place(x=450, y=10)

    tk.Button(features, text="Send Safe/Location", width=button_width, height=button_height,command=open_send_safe, **button_style).place(x=670, y=10)


    
    if bg_label:
        content.configure(bg=BG_DARK, highlightbackground=BG_DARK, highlightthickness=0)
    
    
    text_wrapper = tk.Frame(content, bg=BG_TEXT_BOX)
    text_wrapper.pack(pady=10, padx=20, fill=tk.X) 

    tk.Label(text_wrapper, 
             text="ℹ️ About the App: BE AWARE, BE SAFE",
             bg=BG_TEXT_BOX,
             font=("Georgia", 16, "bold"), 
             fg=TEXT_COLOR 
    ).pack(pady=(15, 10)) 

    tk.Label(text_wrapper, 
             text="Welcome to your essential Disaster Preparedness and Response System!",
             bg=BG_TEXT_BOX,
             font=("Georgia", 12),
             wraplength=700, 
             justify=tk.CENTER,
             fg=TEXT_COLOR
    ).pack(pady=7) 

    tk.Label(text_wrapper, 
             text="The BE AWARE, BE SAFE dashboard is your personalized command center designed to provide rapid, reliable information before, during, and after any hazard. Our goal is to ensure you and your family are always prepared and can respond effectively when seconds count.",
             bg=BG_TEXT_BOX,
             font=("Georgia", 12),
             wraplength=700, 
             justify=tk.CENTER,
             fg=TEXT_COLOR
    ).pack(pady=7)
    
    tk.Label(text_wrapper, 
             text="Key Features and Functions:",
             bg=BG_TEXT_BOX,
             font=("Georgia", 14, "underline"),
             fg=TEXT_COLOR
    ).pack(pady=(15, 10)) 

    tk.Label(text_wrapper,
             text="• Evacuation Area: Displays real-time maps, safe zones, and the fastest evacuation routes from your current location.",
             bg=BG_TEXT_BOX, 
             font=("Georgia", 11),
             wraplength=700,
             justify=tk.LEFT,
             fg=TEXT_COLOR
    ).pack(padx=20, pady=5, anchor="w")
    
    tk.Label(text_wrapper,
             text="• Hotline: Provides a categorized list of all necessary emergency and support contact numbers (Police, Fire, Medical, Utilities).",
             bg=BG_TEXT_BOX,
             font=("Georgia", 11),
             wraplength=700,
             justify=tk.LEFT,
             fg=TEXT_COLOR
    ).pack(padx=20, pady=5, anchor="w")
    
    tk.Label(text_wrapper,
             text="• Disaster Info: Access a comprehensive library of guides, checklists, and educational materials for various hazards (floods, earthquakes, fires, storms).",
             bg=BG_TEXT_BOX,
             font=("Georgia", 11),
             wraplength=700,
             justify=tk.LEFT,
             fg=TEXT_COLOR
    ).pack(padx=20, pady=5, anchor="w")

    tk.Label(text_wrapper,
             text="• Send Safe/Location: Allows you to quickly send a pre-set 'I am safe' message or share your current GPS location with your designated emergency contacts.",
             bg=BG_TEXT_BOX,
             font=("Georgia", 11),
             wraplength=700,
             justify=tk.LEFT,
             fg=TEXT_COLOR
    ).pack(padx=20, pady=5, anchor="w")
    
    tk.Label(text_wrapper, 
             text="Remember: BE AWARE of your current status and local threats, and BE SAFE by knowing your action plan and emergency contacts.",
             bg=BG_TEXT_BOX,
             font=("Georgia", 12, "italic"),
             wraplength=700, 
             justify=tk.CENTER,
             fg=TEXT_COLOR
    ).pack(pady=(15, 0))
    
    dash.after(200, side_navigation.lift)


