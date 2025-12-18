import os
from tkinter import Tk, Label, Button, filedialog, messagebox
from PIL import Image, ImageTk
class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600") 
        self.image_label = Label(root)
        self.image_label.pack(expand=True)
        nav_frame = Frame(root)
        nav_frame.pack(side="bottom", pady=10)
        self.prev_button = Button(nav_frame, text="Previous", command=self.prev_image)
        self.prev_button.pack(side="left", padx=10)
        self.next_button = Button(nav_frame, text="Next", command=self.next_image)
        self.next_button.pack(side="right", padx=10)
        self.exit_button = Button(nav_frame, text="Exit", command=root.destroy)
        self.exit_button.pack(side="bottom", pady=5)
        self.load_button = Button(root, text="Load Folder", command=self.load_images)
        self.load_button.place(relx=0.95, rely=0.02, anchor="ne")
        self.images = []
        self.index = 0
    def load_images(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if not folder:
            messagebox.showerror("Error", "No folder selected!")
            return
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp')
        self.images = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(supported_formats)]
        if not self.images:
            messagebox.showerror("Error", "No supported images found in the folder!")
            return
        self.index = 0
        self.show_image()
    def show_image(self):
        if not self.images:
            return
        img_path = self.images[self.index]
        img = Image.open(img_path)
        w, h = img.size
        max_w, max_h = self.root.winfo_width()-50, self.root.winfo_height()-150
        ratio = min(max_w/w, max_h/h, 1)
        new_size = (int(w*ratio), int(h*ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_img)
        self.root.title(f"Image Viewer - {os.path.basename(img_path)} ({self.index+1}/{len(self.images)})")
    def next_image(self):
        if not self.images:
            return
        self.index = (self.index + 1) % len(self.images)
        self.show_image()
    def prev_image(self):
        if not self.images:
            return
        self.index = (self.index - 1) % len(self.images)
        self.show_image()
if __name__ == "__main__":
    from tkinter import Frame
    root = Tk()
    viewer = ImageViewer(root)
    root.mainloop()