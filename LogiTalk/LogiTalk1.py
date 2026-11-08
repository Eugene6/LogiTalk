import base64
import io
import socket
import threading
import time
from tkinter import filedialog
from socket import socket, AF_INET, SOCK_STREAM

from customtkinter import *
from datetime import datetime
from PIL import Image, ImageTk


class MainWindow(CTk):
    def __init__(self, sock, username):
        super().__init__()

        self.sock = sock
        self.username = username
        self.geometry("400x300")
        self.label = None

        # ---панель бокова---

        self.menu_frame = CTkFrame(self, width = 30, height = self.winfo_height(), fg_color="#eae6ff")
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x = 0, y = 0)

        self.is_show_menu = False
        self.speed_animate_menu = -5

        self.btn = CTkButton(self, text='▶️', command= self.toggle_show_menu, width=20, font=("Helvetica", 20, "bold"), fg_color='#eae6ff',
                                   text_color='#6753cc')
        self.btn.place(x=0, y=0)

        # ---зона чату---

        self.chat_field = CTkScrollableFrame(self, fg_color="#ffffff")
        self.chat_field.place(x=0, y=0)

        self.user_avatar = CTkImage(Image.open("6388000.png").resize((30, 30)))

        self.message_entry = CTkEntry(self, placeholder_text = "Send message...", height = 40, font= ("Helvetica", 15, "bold"), fg_color='#eae6ff',
                                   border_color='#eae6ff',
                                   text_color='#6753cc', placeholder_text_color='#6753cc')
        self.message_entry.place(x=0, y=0)

        self.send_button = CTkButton(self, text = ">", width = 50, height = 40, font=("Helvetica", 30, "bold"), fg_color='#eae6ff', command= self.send_message,
                                   border_color='#eae6ff',
                                   text_color='#6753cc')
        self.send_button.place(x=0, y=0)
        self.img_button = CTkButton(self, text="IMG", width=50, height=40, font=("Helvetica", 20, "bold"),
                                     fg_color='#eae6ff',
                                     border_color='#eae6ff',
                                     text_color='#6753cc',
                                    command=self.open_image)
        self.img_button.place(x=0, y=0)
        self.addptive_ui()



        try:
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Не вдалося підключитися до сервера: {e}")

    def addptive_ui(self):

        self.menu_frame.configure(height=self.winfo_height())
        self.chat_field.place(x= self.menu_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width()-self.menu_frame.winfo_width()-20,
                                  height=self.winfo_height()-40)

        self.send_button.place(x=self.winfo_width() - 100, y=self.winfo_height() - 40)
        self.img_button.place(x=self.winfo_width() - 50, y=self.winfo_height() - 40)
        self.message_entry.place(x=self.menu_frame.winfo_width(), y=self.send_button.winfo_y())
        self.message_entry.configure(
            width=self.winfo_width() - self.menu_frame.winfo_width() - self.send_button.winfo_width()
        )

        self.after(50, self.addptive_ui)

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_animate_menu *= -1
            self.btn.configure(text='▶️')
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= -1
            self.btn.configure(text='◀️')
            self.show_menu()
            self.label = CTkLabel(self.menu_frame, text='Name:', text_color="#6753cc", font=("Helvetica", 15, "bold"))
            self.label.pack(pady=30)
            self.entry = CTkEntry(self.menu_frame)
            self.entry.pack()
            self.save_button = CTkButton(self.menu_frame, text="Save", width=50, height=40, font=("Helvetica", 20, "bold"),
                                        fg_color='#b9aef5',
                                        border_color='#eae6ff',
                                        text_color='#6753cc',  command=self.save_name)
            self.save_button.pack(pady = (15,0))
            self.avatar_button = CTkButton(
                self.menu_frame, text="Change Avatar", width=120, height=35,
                font=("Helvetica", 15, "bold"),
                fg_color='#b9aef5', text_color='#6753cc',
                command=self.change_avatar
            )
            self.avatar_button.pack(pady=(5, 0))


    def show_menu(self):
        current_width = self.menu_frame.winfo_width()
        new_width = current_width + self.speed_animate_menu
        self.menu_frame.configure(width=new_width)

        # Умови продовження анімації
        if (not new_width >= 200 and self.is_show_menu) or \
                (new_width >= 30 and not self.is_show_menu):
            self.after(10, self.show_menu)  # Оновлення кожні 10 мс
        # Видалення віджетів при закритті
        elif new_width < 30 and not self.is_show_menu:
            for widget_name in ["label", "entry", "save_button", "avatar_button"]:
                widget = getattr(self, widget_name, None)
                if widget:
                    widget.destroy()
                    setattr(self, widget_name, None)

    def add_message(self, text, img = None, avatar = None):
        message_frame = CTkFrame(self.chat_field, fg_color='white')
        message_frame.pack(pady=5, anchor='w', fill='x')
        time_str = datetime.now().strftime("%H:%M")
        wrapleng_size = self.winfo_width() - self.menu_frame.winfo_width() - 40

        if not avatar:
            avatar = self.user_avatar
        avatar_label = CTkLabel(message_frame, image=avatar, text="")
        avatar_label.pack(side='left', padx=5)

        wrapleng_size = self.winfo_width() - self.menu_frame.winfo_width() - 100
        text_label = CTkLabel(
            message_frame,
            text=f"{text}\n[{time_str}]",
            wraplength=wrapleng_size,
            anchor='w',
            justify='left',
            text_color='black'
        )
        text_label.pack(side='left', padx=10, pady=5)

        if img:
            CTkLabel(message_frame, image=img, text="").pack(side='left', padx=5)

        else:
            CTkLabel(message_frame, text=text, wraplength=wrapleng_size,
                     text_color='white', image=img, compound='top',
                     justify='left').pack(padx=10, pady=5)

    def save_name(self):
        new_name = self.entry.get()
        if new_name:
            old_name = self.username
            self.username = new_name
            self.add_message(f"[SYSTEM] Імʼя змінено: {old_name} → {self.username}")

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.add_message(f"{self.username}: {message}")

            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.send(data.encode("utf-8"))
            except:
                pass

            self.message_entry.delete(0, END)

    def reconnect(self):
        while True:
            try:
                self.add_message("[Система] Спроба перепідключення...")
                self.sock = socket(AF_INET, SOCK_STREAM)
                self.sock.connect((self.server_host, self.server_port))
                hello = f"TEXT@{self.username}@[SYSTEM] {self.username} знову у чаті!\n"
                self.sock.send(hello.encode("utf-8"))
                self.add_message("[Система] З'єднання відновлено!")
                threading.Thread(target=self.recv_message, daemon=True).start()
                break
            except:
                self.add_message("[Система] Помилка підключення. Спробую через 5 сек...")
                time.sleep(5)

    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    self.add_message("[Система] Втрачено зв'язок із сервером.")
                    self.reconnect()
                    break
                buffer += chunk.decode("utf-8", errors = "ignore")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n",1)
                    self.handle_line(line.strip())
            except:
                self.add_message("[Система] З'єднання розірвано.")
                self.reconnect()
                break

    def handle_line(self, line):
        if not line:
            return

        parts = line.split("@",3)
        msg_type = parts[0]
        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(f"{author}: {message}")
        elif msg_type == "IMAGE":
            if len(parts) >= 4:
                autor = parts[1]
                filename = parts[2]
                img = parts[3]
                try:
                    img_data = base64.b64decode(img)
                    pil_img = Image.open(io.BytesIO(img_data))
                    ctk_tk = CTkImage(pil_img, size=(300, 300))
                    self.add_message(f"{autor}: Надіслав зображення {filename}", img=ctk_tk)

                except Exception as e:
                    self.add_message("Помилка відобрадення зображення")

    def open_image(self):
        file_path = filedialog.askopenfilename(
            title="Виберіть зображення",
            filetypes=[("Зображення", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        img = Image.open(file_path)
        img.thumbnail((150, 150))
        tk_img = CTkImage(light_image=img, dark_image=img, size=img.size)
        self.add_message(f"{self.username} надіслав фото:", img=tk_img)

    def change_avatar(self):
        file_path = filedialog.askopenfilename(
            title="Виберіть аватарку",
            filetypes=[("Зображення", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if file_path:
            try:
                img = Image.open(file_path).resize((30, 30))
                self.user_avatar = CTkImage(img)
                self.add_message("[Система] Аватарку змінено ✅")
            except Exception as e:
                self.add_message(f"[Система] Помилка завантаження аватарки: {e}")

class RegisterWindow(CTk):
    def __init__(self):
        super().__init__()
        self.username = None
        self.title('Приєднатися до сервера')
        self.geometry('300x300')
        CTkLabel(self, text='Вхід в LogiTalk', text_color='#6753cc', font=('Arial', 20, 'bold')).pack(pady=40)
        self.name_entry = CTkEntry(self, placeholder_text='Введіть імʼя')
        self.name_entry.pack()

        self.host_entry = CTkEntry(self, placeholder_text='Введіть хост сервера localhost')
        self.host_entry.pack(pady=5)

        self.port_entry = CTkEntry(self, placeholder_text='Введіть порт сервера 12334 ')
        self.port_entry.pack()

        self.submit_button = CTkButton(self, text='Приєднатися', fg_color='#6753cc', command=self.start_chat)
        self.submit_button.pack(pady=5)

    def start_chat(self):
        self.username = self.name_entry.get().strip()
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((self.host_entry.get(), int(self.port_entry.get())))
            hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався(лась) до чату!\n"
            self.sock.send(hello.encode('utf-8'))

            self.destroy()

            win = MainWindow(self.sock, self.username)
            win.mainloop()


        except Exception as e:
            print(f"Не вдалося підключитися до сервера: {e}")

RegisterWindow().mainloop()