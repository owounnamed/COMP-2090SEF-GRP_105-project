import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from database import DatabaseManager
from services import RestaurantService, EmbeddedMapService
from models import Review
from utils import PIL_AVAILABLE, MAP_AVAILABLE, Image, ImageTk, tkintermapview


class UniEatsApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("UniEats - Food Review Application")
        self.geometry("1380x820")
        self.minsize(1240, 760)
        self.configure(bg="#f5f7fb")

        self.setup_styles()

        self.db = DatabaseManager()
        self.restaurant_service = RestaurantService(self.db)
        self.map_service = EmbeddedMapService()

        self.current_image_path = ""
        self.current_restaurants = []
        self.admin_review_rows = []
        self.deleted_review_rows = []
        self.preview_image_ref = None
        self.admin_preview_image_ref = None

        self.create_widgets()
        self.load_restaurants()
        self.load_admin_reviews()
        self.load_deleted_reviews()
        self.show_map_in_gui()

    def setup_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TNotebook", background="#f5f7fb")
        style.configure("TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold"))
        style.configure("Card.TLabelframe", background="#ffffff")
        style.configure("Card.TLabelframe.Label", background="#ffffff", font=("Segoe UI", 11, "bold"))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TLabel", background="#f5f7fb", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), background="#f5f7fb", foreground="#1f2d3d")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 11), background="#f5f7fb", foreground="#52606d")

    def create_widgets(self):
        header = tk.Frame(self, bg="#f5f7fb")
        header.pack(fill="x", padx=16, pady=(14, 6))

        ttk.Label(header, text="UniEats", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Food review and restaurant discovery app for Mong Kok and Ho Man Tin",
            style="SubHeader.TLabel"
        ).pack(anchor="w", pady=(2, 0))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=14, pady=10)

        self.user_tab = tk.Frame(notebook, bg="#f5f7fb")
        self.map_tab = tk.Frame(notebook, bg="#f5f7fb")
        self.admin_tab = tk.Frame(notebook, bg="#f5f7fb")

        notebook.add(self.user_tab, text="User Panel")
        notebook.add(self.map_tab, text="Map")
        notebook.add(self.admin_tab, text="Admin Panel")

        self.create_user_tab()
        self.create_map_tab()
        self.create_admin_tab()

    def create_user_tab(self):
        filter_card = ttk.LabelFrame(self.user_tab, text="Search & Recommendation", style="Card.TLabelframe")
        filter_card.pack(fill="x", padx=12, pady=10)

        top_frame = tk.Frame(filter_card, bg="#ffffff")
        top_frame.pack(fill="x", padx=12, pady=10)

        ttk.Label(top_frame, text="Area:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.area_var = tk.StringVar(value="All")
        ttk.Combobox(top_frame, textvariable=self.area_var, values=["All", "Mong Kok", "Ho Man Tin"], width=14, state="readonly").grid(row=0, column=1, padx=4)

        ttk.Label(top_frame, text="Cuisine:").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.cuisine_var = tk.StringVar(value="All")
        ttk.Combobox(top_frame, textvariable=self.cuisine_var, values=["All", "Chinese", "Cafe", "Japanese", "Thai", "Korean", "Western"], width=14, state="readonly").grid(row=0, column=3, padx=4)

        ttk.Label(top_frame, text="Max Budget:").grid(row=0, column=4, padx=6, pady=6, sticky="w")
        self.budget_var = tk.StringVar(value="200")
        tk.Entry(top_frame, textvariable=self.budget_var, width=10, relief="solid", bd=1).grid(row=0, column=5, padx=4)

        ttk.Label(top_frame, text="Sort By:").grid(row=0, column=6, padx=6, pady=6, sticky="w")
        self.sort_var = tk.StringVar(value="Rating")
        ttk.Combobox(top_frame, textvariable=self.sort_var, values=["Rating", "Price", "Name"], width=12, state="readonly").grid(row=0, column=7, padx=4)

        ttk.Button(top_frame, text="Apply Filters", command=self.apply_filters).grid(row=0, column=8, padx=6)
        ttk.Button(top_frame, text="Random Pick", command=self.show_random_recommendation).grid(row=0, column=9, padx=6)
        ttk.Button(top_frame, text="Similar Recommendation", command=self.show_similar_recommendations).grid(row=0, column=10, padx=6)
        ttk.Button(top_frame, text="Show on Map", command=self.show_filtered_map_in_gui).grid(row=0, column=11, padx=6)

        content = tk.Frame(self.user_tab, bg="#f5f7fb")
        content.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        left_frame = ttk.LabelFrame(content, text="Restaurant List", style="Card.TLabelframe")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right_frame = ttk.LabelFrame(content, text="Review & Photo", style="Card.TLabelframe")
        right_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))

        left_inner = tk.Frame(left_frame, bg="#ffffff")
        left_inner.pack(fill="both", expand=True, padx=12, pady=12)

        self.restaurant_listbox = tk.Listbox(
            left_inner,
            width=66,
            height=28,
            font=("Segoe UI", 10),
            bd=1,
            relief="solid",
            selectbackground="#dbeafe",
            selectforeground="#111827"
        )
        self.restaurant_listbox.pack(fill="both", expand=True)
        self.restaurant_listbox.bind("<<ListboxSelect>>", self.display_reviews)

        right_inner = tk.Frame(right_frame, bg="#ffffff")
        right_inner.pack(fill="both", expand=True, padx=12, pady=12)

        form = tk.Frame(right_inner, bg="#ffffff")
        form.pack(fill="x")

        tk.Label(form, text="Username", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(form, width=34, relief="solid", bd=1)
        self.username_entry.grid(row=0, column=1, pady=5, sticky="w")

        tk.Label(form, text="Rating (1-5)", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.rating_entry = tk.Entry(form, width=34, relief="solid", bd=1)
        self.rating_entry.grid(row=1, column=1, pady=5, sticky="w")

        tk.Label(form, text="Comment", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="nw", pady=5)
        self.comment_text = tk.Text(form, width=38, height=6, relief="solid", bd=1, font=("Segoe UI", 10))
        self.comment_text.grid(row=2, column=1, pady=5, sticky="w")

        # Photo is optional. User can still submit without it.
        tk.Label(form, text="Photo (optional)", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        photo_button_row = tk.Frame(form, bg="#ffffff")
        photo_button_row.grid(row=3, column=1, sticky="w", pady=5)
        ttk.Button(photo_button_row, text="Choose Photo", command=self.choose_image).pack(side="left")
        ttk.Button(photo_button_row, text="Delete Photo", command=self.clear_selected_image).pack(side="left", padx=(8, 0))

        self.image_label = tk.Label(form, text="No image selected", bg="#ffffff", fg="#4b5563")
        self.image_label.grid(row=4, column=1, sticky="w")

        tk.Label(form, text="Photo Preview", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=5, column=0, sticky="nw", pady=6)
        self.photo_preview_label = tk.Label(form, text="No photo", width=20, height=5, relief="solid", bd=1, bg="#f9fafb")
        self.photo_preview_label.grid(row=5, column=1, sticky="w", pady=6)

        button_row = tk.Frame(right_inner, bg="#ffffff")
        button_row.pack(fill="x", pady=(8, 4))
        ttk.Button(button_row, text="Submit Review", command=self.submit_review).pack(side="left")

        review_card = tk.Frame(right_inner, bg="#ffffff")
        review_card.pack(fill="both", expand=True, pady=(10, 0))
        tk.Label(review_card, text="Saved Reviews", bg="#ffffff", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.review_text = tk.Text(review_card, width=48, height=18, relief="solid", bd=1, font=("Segoe UI", 10))
        self.review_text.pack(fill="both", expand=True, pady=(6, 0))

    def create_map_tab(self):
        top_card = ttk.LabelFrame(self.map_tab, text="OpenStreetMap View", style="Card.TLabelframe")
        top_card.pack(fill="both", expand=True, padx=12, pady=12)

        controls = tk.Frame(top_card, bg="#ffffff")
        controls.pack(fill="x", padx=12, pady=10)

        ttk.Button(controls, text="Show All Restaurants", command=self.show_map_in_gui).pack(side="left", padx=(0, 8))
        ttk.Button(controls, text="Show Filtered Restaurants", command=self.show_filtered_map_in_gui).pack(side="left", padx=(0, 8))
        ttk.Button(controls, text="Show Selected Restaurant", command=self.show_selected_restaurant_on_map).pack(side="left")

        map_frame = tk.Frame(top_card, bg="#ffffff")
        map_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        if MAP_AVAILABLE:
            self.map_widget = tkintermapview.TkinterMapView(map_frame, width=1200, height=620, corner_radius=8)
            self.map_widget.pack(fill="both", expand=True)
            self.map_widget.set_position(22.3180, 114.1740)
            self.map_widget.set_zoom(15)
            self.map_service.set_map_widget(self.map_widget)
        else:
            self.map_widget = None
            text = "Embedded map requires tkintermapview.\n\nInstall it with:\npy -m pip install tkintermapview"
            tk.Label(map_frame, text=text, bg="#ffffff", fg="#b91c1c", font=("Segoe UI", 12)).pack(expand=True)

    def create_admin_tab(self):
        self.admin_login_frame = tk.Frame(self.admin_tab, bg="#f5f7fb")
        self.admin_content_frame = tk.Frame(self.admin_tab, bg="#f5f7fb")

        self.build_admin_login_frame()
        self.build_admin_content_frame()
        self.show_admin_login_screen()

    def build_admin_login_frame(self):
        card = ttk.LabelFrame(self.admin_login_frame, text="Admin Login", style="Card.TLabelframe")
        card.pack(padx=220, pady=100, fill="x")

        inner = tk.Frame(card, bg="#ffffff")
        inner.pack(fill="x", padx=20, pady=20)

        # Simple login only. Good enough for this project.
        tk.Label(inner, text="Username", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8)
        self.admin_login_username = tk.Entry(inner, width=30, relief="solid", bd=1)
        self.admin_login_username.grid(row=0, column=1, sticky="w", pady=8)

        tk.Label(inner, text="Password", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8)
        self.admin_login_password = tk.Entry(inner, width=30, relief="solid", bd=1, show="*")
        self.admin_login_password.grid(row=1, column=1, sticky="w", pady=8)

        self.admin_login_message = tk.Label(inner, text="Default login: test / test", bg="#ffffff", fg="#4b5563")
        self.admin_login_message.grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 12))

        ttk.Button(inner, text="Login", command=self.admin_login).grid(row=3, column=0, columnspan=2, sticky="w")

    def build_admin_content_frame(self):
        top_card = ttk.LabelFrame(self.admin_content_frame, text="Restaurant Management", style="Card.TLabelframe")
        top_card.pack(fill="x", padx=12, pady=10)

        top = tk.Frame(top_card, bg="#ffffff")
        top.pack(fill="x", padx=12, pady=10)

        labels = ["Name", "Area", "Cuisine", "Budget", "Latitude", "Longitude"]
        i = 0
        while i < len(labels):
            ttk.Label(top, text=labels[i] + ":").grid(row=i // 3, column=(i % 3) * 2, padx=6, pady=6, sticky="w")
            i = i + 1

        self.admin_name = tk.Entry(top, width=20, relief="solid", bd=1)
        self.admin_name.grid(row=0, column=1, padx=4)

        self.admin_area = ttk.Combobox(top, values=["Mong Kok", "Ho Man Tin"], width=17, state="readonly")
        self.admin_area.grid(row=0, column=3, padx=4)

        self.admin_cuisine = ttk.Combobox(top, values=["Chinese", "Cafe", "Japanese", "Thai", "Korean", "Western"], width=17, state="readonly")
        self.admin_cuisine.grid(row=0, column=5, padx=4)

        self.admin_budget = tk.Entry(top, width=20, relief="solid", bd=1)
        self.admin_budget.grid(row=1, column=1, padx=4)

        self.admin_lat = tk.Entry(top, width=20, relief="solid", bd=1)
        self.admin_lat.grid(row=1, column=3, padx=4)

        self.admin_lon = tk.Entry(top, width=20, relief="solid", bd=1)
        self.admin_lon.grid(row=1, column=5, padx=4)

        action_row = tk.Frame(top_card, bg="#ffffff")
        action_row.pack(fill="x", padx=12, pady=(0, 12))
        ttk.Button(action_row, text="Add Restaurant", command=self.admin_add_restaurant).pack(side="left", padx=(0, 8))
        ttk.Button(action_row, text="Update Selected", command=self.admin_update_restaurant).pack(side="left", padx=(0, 8))
        ttk.Button(action_row, text="Delete Selected", command=self.admin_delete_selected_restaurant).pack(side="left", padx=(0, 8))
        ttk.Button(action_row, text="Logout", command=self.admin_logout).pack(side="right")

        bottom = tk.Frame(self.admin_content_frame, bg="#f5f7fb")
        bottom.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        left = ttk.LabelFrame(bottom, text="Restaurants", style="Card.TLabelframe")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right = ttk.LabelFrame(bottom, text="All Reviews", style="Card.TLabelframe")
        right.pack(side="right", fill="both", expand=True, padx=(8, 0))

        left_inner = tk.Frame(left, bg="#ffffff")
        left_inner.pack(fill="both", expand=True, padx=12, pady=12)

        right_inner = tk.Frame(right, bg="#ffffff")
        right_inner.pack(fill="both", expand=True, padx=12, pady=12)

        self.admin_restaurant_listbox = tk.Listbox(left_inner, width=66, height=28, font=("Segoe UI", 10), bd=1, relief="solid")
        self.admin_restaurant_listbox.pack(fill="both", expand=True)
        self.admin_restaurant_listbox.bind("<<ListboxSelect>>", self.fill_admin_form_from_selection)

        self.admin_review_listbox = tk.Listbox(right_inner, width=70, height=14, font=("Segoe UI", 10), bd=1, relief="solid")
        self.admin_review_listbox.pack(fill="x")
        self.admin_review_listbox.bind("<<ListboxSelect>>", self.display_admin_review_preview)

        delete_frame = tk.Frame(right_inner, bg="#ffffff")
        delete_frame.pack(fill="x", pady=(10, 8))

        tk.Label(delete_frame, text="Delete Reason (optional)", bg="#ffffff", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.admin_delete_reason_entry = tk.Entry(delete_frame, relief="solid", bd=1)
        self.admin_delete_reason_entry.pack(fill="x", pady=(4, 8))
        ttk.Button(delete_frame, text="Delete Selected Review", command=self.admin_delete_selected_review).pack(anchor="w")

        tk.Label(right_inner, text="Selected Review Photo", bg="#ffffff", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(8, 4))
        self.admin_photo_preview_label = tk.Label(right_inner, text="No photo", width=26, height=6, relief="solid", bd=1, bg="#f9fafb")
        self.admin_photo_preview_label.pack(anchor="w")

        self.admin_review_info = tk.Text(right_inner, width=70, height=6, relief="solid", bd=1, font=("Segoe UI", 10))
        self.admin_review_info.pack(fill="x", pady=(8, 10))

        deleted_card = ttk.LabelFrame(right_inner, text="Deleted Review History", style="Card.TLabelframe")
        deleted_card.pack(fill="both", expand=True)

        deleted_inner = tk.Frame(deleted_card, bg="#ffffff")
        deleted_inner.pack(fill="both", expand=True, padx=10, pady=10)

        self.deleted_review_listbox = tk.Listbox(deleted_inner, width=70, height=8, font=("Segoe UI", 10), bd=1, relief="solid")
        self.deleted_review_listbox.pack(fill="both", expand=True)

    def show_admin_login_screen(self):
        self.admin_content_frame.pack_forget()
        self.admin_login_frame.pack(fill="both", expand=True)

    def show_admin_content_screen(self):
        self.admin_login_frame.pack_forget()
        self.admin_content_frame.pack(fill="both", expand=True)

    def admin_login(self):
        username = self.admin_login_username.get().strip()
        password = self.admin_login_password.get().strip()

        if username == "test" and password == "test":
            self.admin_login_password.delete(0, tk.END)
            self.admin_login_message.config(text="Login successful.", fg="#166534")
            self.show_admin_content_screen()
        else:
            self.admin_login_message.config(text="Wrong username or password.", fg="#b91c1c")

    def admin_logout(self):
        self.admin_login_username.delete(0, tk.END)
        self.admin_login_password.delete(0, tk.END)
        self.admin_login_message.config(text="Default login: test / test", fg="#4b5563")
        self.show_admin_login_screen()

    def load_restaurants(self, restaurants=None):
        self.restaurant_listbox.delete(0, tk.END)
        self.admin_restaurant_listbox.delete(0, tk.END)

        if restaurants is None:
            self.current_restaurants = self.restaurant_service.get_all_restaurants()
        else:
            self.current_restaurants = restaurants

        self.restaurant_service.refresh_graph()

        for restaurant in self.current_restaurants:
            text = restaurant.display_text()
            self.restaurant_listbox.insert(tk.END, text)
            self.admin_restaurant_listbox.insert(tk.END, "ID " + str(restaurant.id) + " - " + text)

    def load_admin_reviews(self):
        self.admin_review_listbox.delete(0, tk.END)
        self.admin_review_rows = self.db.get_all_reviews()

        for row in self.admin_review_rows:
            review_id = row[0]
            restaurant_name = row[1]
            username = row[2]
            rating = row[3]
            comment = row[4]
            image_path = row[5]

            image_text = "No image"
            if image_path:
                image_text = os.path.basename(image_path)

            line = (
                "Review ID " + str(review_id)
                + " | " + str(restaurant_name)
                + " | " + str(username)
                + " | Rating " + str(rating)
                + " | " + str(comment)
                + " | " + image_text
            )
            self.admin_review_listbox.insert(tk.END, line)

        self.clear_admin_preview()

    def load_deleted_reviews(self):
        self.deleted_review_listbox.delete(0, tk.END)
        self.deleted_review_rows = self.db.get_deleted_reviews()

        for row in self.deleted_review_rows:
            deleted_id = row[0]
            original_review_id = row[1]
            restaurant_name = row[2]
            username = row[3]
            delete_reason = row[7]

            if delete_reason is None or delete_reason == "":
                delete_reason = "No reason"

            line = (
                "Deleted ID " + str(deleted_id)
                + " | Review ID " + str(original_review_id)
                + " | " + str(restaurant_name)
                + " | " + str(username)
                + " | Reason: " + str(delete_reason)
            )
            self.deleted_review_listbox.insert(tk.END, line)

    def get_selected_restaurant(self):
        selection = self.restaurant_listbox.curselection()
        if not selection:
            return None
        return self.current_restaurants[selection[0]]

    def get_selected_admin_restaurant(self):
        selection = self.admin_restaurant_listbox.curselection()
        if not selection:
            return None
        return self.current_restaurants[selection[0]]

    def display_photo_preview(self, image_path):
        if image_path == "" or not os.path.exists(image_path):
            self.preview_image_ref = None
            self.photo_preview_label.config(image="", text="No photo")
            return

        if PIL_AVAILABLE:
            try:
                image = Image.open(image_path)
                image.thumbnail((180, 120))
                photo = ImageTk.PhotoImage(image)
                self.preview_image_ref = photo
                self.photo_preview_label.config(image=photo, text="")
                return
            except Exception:
                pass

        try:
            photo = tk.PhotoImage(file=image_path)
            self.preview_image_ref = photo
            self.photo_preview_label.config(image=photo, text="")
        except Exception:
            self.preview_image_ref = None
            self.photo_preview_label.config(image="", text="Preview not available")

    def display_admin_photo_preview(self, image_path):
        if image_path == "" or not os.path.exists(image_path):
            self.admin_preview_image_ref = None
            self.admin_photo_preview_label.config(image="", text="No photo")
            return

        if PIL_AVAILABLE:
            try:
                image = Image.open(image_path)
                image.thumbnail((220, 150))
                photo = ImageTk.PhotoImage(image)
                self.admin_preview_image_ref = photo
                self.admin_photo_preview_label.config(image=photo, text="")
                return
            except Exception:
                pass

        try:
            photo = tk.PhotoImage(file=image_path)
            self.admin_preview_image_ref = photo
            self.admin_photo_preview_label.config(image=photo, text="")
        except Exception:
            self.admin_preview_image_ref = None
            self.admin_photo_preview_label.config(image="", text="Preview not available")

    def clear_selected_image(self):
        self.current_image_path = ""
        self.image_label.config(text="No image selected")
        self.display_photo_preview("")

    def clear_admin_preview(self):
        self.admin_preview_image_ref = None
        self.admin_photo_preview_label.config(image="", text="No photo")
        self.admin_review_info.delete("1.0", tk.END)
        self.admin_delete_reason_entry.delete(0, tk.END)

    def apply_filters(self):
        area = self.area_var.get()
        cuisine = self.cuisine_var.get()
        budget = None

        budget_text = self.budget_var.get().strip()
        if budget_text != "":
            if not budget_text.isdigit():
                messagebox.showerror("Error", "Budget must be a whole number.")
                return
            budget = int(budget_text)

        filtered_restaurants = self.restaurant_service.filter_restaurants(area, cuisine, budget)
        sorted_restaurants = self.restaurant_service.sort_restaurants(filtered_restaurants, self.sort_var.get())
        self.load_restaurants(sorted_restaurants)
        self.review_text.delete("1.0", tk.END)
        self.display_photo_preview("")
        self.show_filtered_map_in_gui()

    def display_reviews(self, event=None):
        restaurant = self.get_selected_restaurant()
        if restaurant is None:
            return

        review_rows = self.db.get_reviews_by_restaurant(restaurant.id)
        self.review_text.delete("1.0", tk.END)
        self.review_text.insert(tk.END, "Reviews for " + restaurant.name + "\n")
        self.review_text.insert(tk.END, "=" * 45 + "\n")

        if len(review_rows) == 0:
            self.review_text.insert(tk.END, "No reviews yet.\n")
            self.display_photo_preview("")
            return

        first_valid_image = ""

        for row in review_rows:
            review = Review(row[1], row[2], row[3], row[4], row[5])
            self.review_text.insert(tk.END, str(review) + "\n")
            self.review_text.insert(tk.END, "-" * 45 + "\n")

            if first_valid_image == "":
                if row[5] and os.path.exists(row[5]):
                    first_valid_image = row[5]

        self.display_photo_preview(first_valid_image)

    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )

        if file_path:
            self.current_image_path = file_path
            self.image_label.config(text=os.path.basename(file_path))
            self.display_photo_preview(file_path)

    def submit_review(self):
        restaurant = self.get_selected_restaurant()
        if restaurant is None:
            messagebox.showwarning("Warning", "Please select a restaurant first.")
            return

        username = self.username_entry.get().strip()
        rating_text = self.rating_entry.get().strip()
        comment = self.comment_text.get("1.0", tk.END).strip()

        if username == "" or rating_text == "" or comment == "":
            messagebox.showwarning("Warning", "Please fill in username, rating, and comment.")
            return

        try:
            rating = float(rating_text)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number between 1 and 5.")
            return

        saved_image_path = ""
        if self.current_image_path != "":
            saved_image_path = self.restaurant_service.save_image(self.current_image_path)

        review = Review(restaurant.id, username, rating, comment, saved_image_path)
        self.db.add_review(review)

        # Reset form after saving.
        self.current_image_path = ""
        self.image_label.config(text="No image selected")
        self.username_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        self.comment_text.delete("1.0", tk.END)
        self.display_photo_preview("")

        self.load_restaurants()
        self.load_admin_reviews()
        self.load_deleted_reviews()
        self.display_reviews()
        self.show_map_in_gui()
        messagebox.showinfo("Success", "Review submitted successfully.")

    def display_admin_review_preview(self, event=None):
        selection = self.admin_review_listbox.curselection()
        if not selection:
            self.clear_admin_preview()
            return

        row = self.admin_review_rows[selection[0]]
        image_path = row[5]

        self.display_admin_photo_preview(image_path)
        self.admin_review_info.delete("1.0", tk.END)
        self.admin_review_info.insert(tk.END, "Restaurant: " + str(row[1]) + "\n")
        self.admin_review_info.insert(tk.END, "User: " + str(row[2]) + "\n")
        self.admin_review_info.insert(tk.END, "Rating: " + str(row[3]) + "\n")
        self.admin_review_info.insert(tk.END, "Comment: " + str(row[4]) + "\n")

    def show_random_recommendation(self):
        recommendation = self.restaurant_service.random_recommendation(self.current_restaurants)
        if recommendation is None:
            messagebox.showinfo("Random Recommendation", "No restaurant available.")
            return

        messagebox.showinfo("Random Recommendation", recommendation.display_text())

    def show_similar_recommendations(self):
        restaurant = self.get_selected_restaurant()
        if restaurant is None:
            messagebox.showwarning("Warning", "Please select a restaurant first.")
            return

        recommended = self.restaurant_service.recommend_by_history(restaurant.id)
        if len(recommended) == 0:
            messagebox.showinfo("Recommendation", "No similar restaurants found.")
            return

        lines = []
        for restaurant_item in recommended:
            lines.append(restaurant_item.display_text())
        messagebox.showinfo("Similar Restaurants", "\n".join(lines))

    def show_map_in_gui(self):
        restaurants = self.restaurant_service.get_all_restaurants()
        if len(restaurants) == 0:
            messagebox.showwarning("Warning", "No restaurants to display on the map.")
            return

        if self.map_service.show_restaurants_on_map(restaurants) is False:
            return

    def show_filtered_map_in_gui(self):
        if len(self.current_restaurants) == 0:
            messagebox.showwarning("Warning", "No filtered restaurants to display on the map.")
            return

        first = self.current_restaurants[0]
        self.map_service.show_restaurants_on_map(self.current_restaurants, first.latitude, first.longitude)

    def show_selected_restaurant_on_map(self):
        restaurant = self.get_selected_restaurant()
        if restaurant is None:
            messagebox.showwarning("Warning", "Please select a restaurant first.")
            return

        self.map_service.show_restaurants_on_map([restaurant], restaurant.latitude, restaurant.longitude)

    def fill_admin_form_from_selection(self, event=None):
        restaurant = self.get_selected_admin_restaurant()
        if restaurant is None:
            return

        self.admin_name.delete(0, tk.END)
        self.admin_name.insert(0, restaurant.name)
        self.admin_area.set(restaurant.area)
        self.admin_cuisine.set(restaurant.cuisine)

        self.admin_budget.delete(0, tk.END)
        self.admin_budget.insert(0, str(restaurant.price_level))

        self.admin_lat.delete(0, tk.END)
        self.admin_lat.insert(0, str(restaurant.latitude))

        self.admin_lon.delete(0, tk.END)
        self.admin_lon.insert(0, str(restaurant.longitude))

    def admin_add_restaurant(self):
        try:
            name = self.admin_name.get().strip()
            area = self.admin_area.get().strip()
            cuisine = self.admin_cuisine.get().strip()
            budget = int(self.admin_budget.get().strip())
            latitude = float(self.admin_lat.get().strip())
            longitude = float(self.admin_lon.get().strip())

            if name == "" or area == "" or cuisine == "":
                raise ValueError("Please fill in all restaurant fields.")

            self.db.add_restaurant(name, area, cuisine, budget, latitude, longitude)
            self.load_restaurants()
            self.show_map_in_gui()
            messagebox.showinfo("Admin", "Restaurant added successfully.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def admin_update_restaurant(self):
        restaurant = self.get_selected_admin_restaurant()
        if restaurant is None:
            messagebox.showwarning("Warning", "Please select a restaurant first.")
            return

        try:
            name = self.admin_name.get().strip()
            area = self.admin_area.get().strip()
            cuisine = self.admin_cuisine.get().strip()
            budget = int(self.admin_budget.get().strip())
            latitude = float(self.admin_lat.get().strip())
            longitude = float(self.admin_lon.get().strip())

            if name == "" or area == "" or cuisine == "":
                raise ValueError("Please fill in all restaurant fields.")

            self.db.update_restaurant(restaurant.id, name, area, cuisine, budget, latitude, longitude)
            self.load_restaurants()
            self.load_admin_reviews()
            self.load_deleted_reviews()
            self.show_map_in_gui()
            messagebox.showinfo("Admin", "Restaurant updated successfully.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def admin_delete_selected_restaurant(self):
        restaurant = self.get_selected_admin_restaurant()
        if restaurant is None:
            messagebox.showwarning("Warning", "Please select a restaurant to delete.")
            return

        answer = messagebox.askyesno("Confirm", "Delete restaurant: " + restaurant.name + "?")
        if answer:
            self.db.delete_restaurant(restaurant.id)
            self.load_restaurants()
            self.load_admin_reviews()
            self.load_deleted_reviews()
            self.review_text.delete("1.0", tk.END)
            self.display_photo_preview("")
            self.show_map_in_gui()
            messagebox.showinfo("Admin", "Restaurant deleted successfully.")

    def admin_delete_selected_review(self):
        selection = self.admin_review_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a review first.")
            return

        review_id = self.admin_review_rows[selection[0]][0]
        delete_reason = self.admin_delete_reason_entry.get().strip()
        self.db.delete_review(review_id, delete_reason)
        self.load_restaurants()
        self.load_admin_reviews()
        self.load_deleted_reviews()
        self.display_reviews()
        self.show_map_in_gui()
        messagebox.showinfo("Admin", "Review deleted successfully.")
