from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from core import fetch_records, store_record


class SpecimenApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CSC442 Specimen Size Calculator")
        self.geometry("980x620")
        self.configure(bg="#f4f7fb")

        self._build_form()
        self._build_table()
        self.refresh_table()

    def _build_form(self) -> None:
        frame = tk.Frame(self, bg="#f4f7fb", padx=20, pady=20)
        frame.pack(fill="x")

        title = tk.Label(
            frame,
            text="Microscope Size to Real-Life Actual Size",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f7fb",
            fg="#0b2948",
        )
        title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        tk.Label(frame, text="Username", bg="#f4f7fb").grid(row=1, column=0, sticky="w")
        tk.Label(frame, text="Microscope Size", bg="#f4f7fb").grid(
            row=1, column=1, sticky="w"
        )
        tk.Label(frame, text="Magnification", bg="#f4f7fb").grid(
            row=1, column=2, sticky="w"
        )
        tk.Label(frame, text="Unit", bg="#f4f7fb").grid(row=1, column=3, sticky="w")

        self.username_var = tk.StringVar()
        self.microscope_size_var = tk.StringVar()
        self.magnification_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="um")

        tk.Entry(frame, textvariable=self.username_var, width=22).grid(
            row=2, column=0, padx=(0, 10), pady=4
        )
        tk.Entry(frame, textvariable=self.microscope_size_var, width=22).grid(
            row=2, column=1, padx=(0, 10), pady=4
        )
        tk.Entry(frame, textvariable=self.magnification_var, width=22).grid(
            row=2, column=2, padx=(0, 10), pady=4
        )

        unit_combo = ttk.Combobox(
            frame, textvariable=self.unit_var, values=["um", "mm", "cm"], width=12
        )
        unit_combo.grid(row=2, column=3, pady=4)

        save_btn = ttk.Button(
            frame, text="Calculate + Save", command=self.calculate_and_save
        )
        save_btn.grid(row=3, column=0, pady=(12, 0), sticky="w")

        self.result_var = tk.StringVar(value="Actual size will appear here.")
        tk.Label(
            frame,
            textvariable=self.result_var,
            font=("Segoe UI", 11, "bold"),
            bg="#f4f7fb",
            fg="#104b7a",
        ).grid(row=3, column=1, columnspan=3, sticky="w", pady=(12, 0))

    def _build_table(self) -> None:
        table_container = tk.Frame(self, bg="#ffffff", padx=18, pady=18)
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columns = (
            "id",
            "username",
            "microscope_size",
            "magnification",
            "actual_size",
            "unit",
            "created_at",
        )
        self.table = ttk.Treeview(table_container, columns=columns, show="headings")

        headers = {
            "id": "ID",
            "username": "Username",
            "microscope_size": "Microscope Size",
            "magnification": "Magnification",
            "actual_size": "Actual Size",
            "unit": "Unit",
            "created_at": "Created At",
        }

        for col in columns:
            self.table.heading(col, text=headers[col])
            self.table.column(col, width=120, anchor="center")

        self.table.column("username", width=170, anchor="w")
        self.table.column("created_at", width=170, anchor="center")

        self.table.pack(fill="both", expand=True)

    def calculate_and_save(self) -> None:
        try:
            username = self.username_var.get().strip()
            microscope_size = float(self.microscope_size_var.get().strip())
            magnification = float(self.magnification_var.get().strip())
            unitChosen = self.unit_var.get().strip() or "um"

            _, actual_size = store_record(
                username, microscope_size, magnification, unitChosen
            )

            self.result_var.set(f"Actual size: {actual_size:.6f} {unitChosen}")
            self.refresh_table()
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))

    def refresh_table(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)

        for row in fetch_records(limit=150):
            self.table.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["username"],
                    f"{row['microscope_size']:.4f}",
                    f"{row['magnification']:.2f}",
                    f"{row['actual_size']:.6f}",
                    row["unit"],
                    row["created_at"],
                ),
            )


if __name__ == "__main__":
    app = SpecimenApp()
    app.mainloop()
