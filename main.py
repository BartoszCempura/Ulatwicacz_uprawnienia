import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ułatwiacz uprawnień")
        self.geometry("600x800")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title_label = ctk.CTkLabel(
            self,
            text="Wklej tutaj nazwy lokacji",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.textbox = ctk.CTkTextbox(self)
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")

        bottom_frame.grid_columnconfigure(0, weight=2)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)

        start_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        start_frame.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        start_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(start_frame)
        self.input_entry.grid(row=0, column=0, pady=(0, 5), sticky="ew")

        button_1 = ctk.CTkButton(start_frame, text="kopiuj", command=self.copy_input_to_clipboard)
        button_1.grid(row=1, column=0, pady=(5, 0), sticky="ew")

        middle_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        middle_frame.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        middle_frame.grid_columnconfigure(0, weight=1)

        button_2 = ctk.CTkButton(middle_frame, text="Góra", command=self.prev_line)
        button_2.grid(row=0, column=0, pady=(0, 5), sticky="ew")

        button_3 = ctk.CTkButton(middle_frame, text="Dół", command=self.next_line)
        button_3.grid(row=1, column=0, pady=(5, 0), sticky="ew")

        end_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        end_frame.grid(row=0, column=2, padx=5, pady=10, sticky="ew")
        end_frame.grid_columnconfigure(0, weight=1)

        button_4 = ctk.CTkButton(end_frame, text="Usuń powtórzenia", command=self.remove_duplicates)
        button_4.grid(row=0, column=0, pady=(0, 5), sticky="ew")

        button_5 = ctk.CTkButton(end_frame, text="Sortuj", command=self.sort)
        button_5.grid(row=1, column=0, pady=(5, 0), sticky="ew")

    def remove_duplicates(self):
        text = self.textbox.get("1.0", "end-1c").strip()
        if not text:
            return

        lines = text.splitlines()

        seen = set()
        unique_lines = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)

        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", "\n".join(unique_lines))
        self.sort()

    def sort(self):
        text = self.textbox.get("1.0", "end-1c").strip()
        if not text:
            return

        lines = text.splitlines()
        lines = sorted(lines, key=str.lower)

        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", "\n".join(lines))

        self.select_first_line()
        self.copy_selected_line_to_entry()

    def select_first_line(self):
            self.textbox.tag_remove("sel", "1.0", "end")
            self.textbox.tag_add("sel", "1.0", "1.end")
            self.textbox.mark_set("insert", "1.end")
            self.textbox.see("1.0")

    def copy_selected_line_to_entry(self):
        try:
            selected_text = self.textbox.get("sel.first", "sel.last")
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, selected_text)
        except:
            pass

    def next_line(self):
        try:
            start = self.textbox.index("sel.first linestart")
            next_start = self.textbox.index(f"{start} +1 line")
            next_end = self.textbox.index(f"{next_start} lineend")

            self.textbox.tag_remove("sel", "1.0", "end")
            self.textbox.tag_add("sel", next_start, next_end)
            self.textbox.mark_set("insert", next_end)
            self.textbox.see(next_start)

            self.copy_selected_line_to_entry()
        except:
            pass

    def prev_line(self):
        try:
            start = self.textbox.index("sel.first linestart")
            prev_start = self.textbox.index(f"{start} -1 line")
            prev_end = self.textbox.index(f"{prev_start} lineend")

            self.textbox.tag_remove("sel", "1.0", "end")
            self.textbox.tag_add("sel", prev_start, prev_end)
            self.textbox.mark_set("insert", prev_end)
            self.textbox.see(prev_start)

            self.copy_selected_line_to_entry()
        except:
            pass

    def copy_input_to_clipboard(self):
        text = self.input_entry.get()
        if not text:
            return

        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

if __name__ == "__main__":
    app = App()
    app.mainloop()
