import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

try:
    from PIL import Image, ImageTk
except ModuleNotFoundError as exc:  # Pillow provides JPEG support for Tk
    raise ModuleNotFoundError(
        "Pillow is required to run this viewer. Install it with 'pip install pillow'."
    ) from exc


class BitmapViewer(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Bitmap Viewer")
        self.geometry("960x600")
        self.minsize(720, 480)

        self.selected_dir = tk.StringVar(value="No folder selected")
        self.bitmap_files: list[Path] = []
        self.current_image: tk.PhotoImage | None = None
        self.supported_patterns: tuple[str, ...] = ("*.bmp", "*.dib", "*.jpg", "*.jpeg")

        self._build_widgets()

    def _build_widgets(self) -> None:
        control_frame = tk.Frame(self, padx=8, pady=8)
        control_frame.pack(fill=tk.X)

        choose_btn = tk.Button(control_frame, text="Choose Folder", command=self.choose_folder)
        choose_btn.pack(side=tk.LEFT)

        path_label = tk.Label(control_frame, textvariable=self.selected_dir, anchor="w", padx=12)
        path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        main_frame = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RIDGE)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        list_frame = tk.Frame(main_frame)
        self.file_listbox = tk.Listbox(list_frame, exportselection=False)
        list_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=list_scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox.bind("<<ListboxSelect>>", self._on_file_selected)
        main_frame.add(list_frame, minsize=200)

        preview_frame = tk.Frame(main_frame)
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)

        self.image_label = tk.Label(preview_frame, bg="#303030")
        self.image_label.grid(row=0, column=0, sticky="nsew")

        self.status_var = tk.StringVar(value="Select an image to preview")
        status_label = tk.Label(preview_frame, textvariable=self.status_var, anchor="w", padx=6, pady=6)
        status_label.grid(row=1, column=0, sticky="ew")

        main_frame.add(preview_frame)

    def choose_folder(self) -> None:
        directory = filedialog.askdirectory(title="Select folder with bitmap or JPEG files")
        if not directory:
            return

        image_paths: list[Path] = []
        for pattern in self.supported_patterns:
            image_paths.extend(Path(directory).glob(pattern))
        image_paths.sort(key=lambda path: path.name.lower())

        if not image_paths:
            messagebox.showinfo(
                "Bitmap Viewer",
                "No supported bitmap or JPEG files were found in the chosen folder.",
            )

        self.bitmap_files = image_paths
        self.selected_dir.set(directory)
        self._populate_listbox()

    def _populate_listbox(self) -> None:
        self.file_listbox.delete(0, tk.END)
        for path in self.bitmap_files:
            self.file_listbox.insert(tk.END, path.name)
        self._clear_preview(reset_status=True)

    def _on_file_selected(self, event: tk.Event[tk.Listbox]) -> None:
        if not self.file_listbox.curselection():
            return
        index = self.file_listbox.curselection()[0]
        image_path = self.bitmap_files[index]
        self._show_image(image_path)

    def _show_image(self, image_path: Path) -> None:
        try:
            with Image.open(image_path) as image:
                original_width, original_height = image.width, image.height
                prepared_image = self._prepare_image(image)
        except (FileNotFoundError, OSError) as exc:
            self._clear_preview(reset_status=True)
            messagebox.showerror("Bitmap Viewer", f"Unable to open {image_path.name}: {exc}")
            return

        self.current_image = ImageTk.PhotoImage(prepared_image)
        self.image_label.configure(image=self.current_image)
        self.status_var.set(
            "Viewing: {} (display {}x{}, original {}x{})".format(
                image_path.name,
                self.current_image.width(),
                self.current_image.height(),
                original_width,
                original_height,
            )
        )

    def _prepare_image(self, image: Image.Image) -> Image.Image:
        label_width = self.image_label.winfo_width() or self.image_label.winfo_reqwidth()
        label_height = self.image_label.winfo_height() or self.image_label.winfo_reqheight()

        if label_width <= 1 or label_height <= 1:
            return image.copy()

        new_width = max(1, int(label_width))
        new_height = max(1, int(label_height))

        if image.width == new_width and image.height == new_height:
            return image.copy()

        return image.resize((new_width, new_height), Image.LANCZOS)

    def _clear_preview(self, *, reset_status: bool = False) -> None:
        self.current_image = None
        self.image_label.configure(image="")
        if reset_status:
            self.status_var.set(
                "Select an image to preview" if self.bitmap_files else "No images available"
            )


def main() -> None:
    if not os.environ.get("DISPLAY") and os.name != "nt":
        raise RuntimeError("A graphical display is required to run this application.")
    app = BitmapViewer()
    app.mainloop()


if __name__ == "__main__":
    main()
