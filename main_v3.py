import customtkinter as ctk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageFont

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

current_qr_image = None
current_vcard = ""


def clean_phone(phone):
    for ch in [" ", "-", "(", ")"]:
        phone = phone.replace(ch, "")
    return phone


def build_vcard():
    first_name = entries["Имя"].get().strip()
    last_name = entries["Фамилия"].get().strip()
    middle_name = entries["Отчество"].get().strip()

    company = entries["Компания"].get().strip()
    position = entries["Должность"].get().strip()

    phone1 = clean_phone(entries["Телефон 1"].get().strip())
    phone2 = clean_phone(entries["Телефон 2"].get().strip())
    phone3 = clean_phone(entries["Телефон 3"].get().strip())

    email = entries["Email"].get().strip()

    telegram = entries["Telegram"].get().strip().replace("@", "")
    whatsapp = entries["WhatsApp"].get().strip().replace("+", "")
    instagram = entries["Instagram"].get().strip().replace("@", "")

    website = entries["Сайт"].get().strip()

    vcard = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{last_name};{first_name};{middle_name};;;",
        f"FN:{first_name} {middle_name} {last_name}",
    ]

    if company:
        vcard.append(f"ORG:{company}")

    if position:
        vcard.append(f"TITLE:{position}")

    if phone1:
        vcard.append(f"TEL;TYPE=CELL:{phone1}")

    if phone2:
        vcard.append(f"TEL;TYPE=CELL:{phone2}")

    if phone3:
        vcard.append(f"TEL;TYPE=CELL:{phone3}")

    if email:
        vcard.append(f"EMAIL:{email}")

    if website:
        if not website.startswith(("http://", "https://")):
            website = "https://" + website

        vcard.append(f"URL:{website}")

    if telegram:
        vcard.append(f"URL:https://t.me/{telegram}")

    if whatsapp:
        vcard.append(f"URL:https://wa.me/{whatsapp}")

    if instagram:
        vcard.append(f"URL:https://instagram.com/{instagram}")

    vcard.append("END:VCARD")

    return "\r\n".join(vcard)


def generate_qr():
    global current_qr_image
    global current_vcard

    first_name = entries["Имя"].get().strip()
    last_name = entries["Фамилия"].get().strip()
    phone1 = entries["Телефон 1"].get().strip()

    if not first_name:
        messagebox.showerror("Ошибка", "Заполните поле Имя.")
        return

    if not last_name:
        messagebox.showerror("Ошибка", "Заполните поле Фамилия.")
        return

    if not phone1:
        messagebox.showerror("Ошибка", "Заполните поле Телефон 1.")
        return

    current_vcard = build_vcard()

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(current_vcard)
    qr.make(fit=True)

    current_qr_image = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    draw = ImageDraw.Draw(current_qr_image)

    qr_width, qr_height = current_qr_image.size

    logo_size = 80

    x1 = (qr_width - logo_size) // 2
    y1 = (qr_height - logo_size) // 2
    x2 = x1 + logo_size
    y2 = y1 + logo_size

    draw.rectangle(
        [x1, y1, x2, y2],
        fill="white"
    )

    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            18
        )
    except Exception:
        font = ImageFont.load_default()

    text = "CA-МАРК"

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (qr_width - text_width) // 2
    text_y = (qr_height - text_height) // 2

    draw.text(
        (text_x, text_y),
        text,
        fill="black",
        font=font
    )

    preview = current_qr_image.resize((420, 420))

    photo = ImageTk.PhotoImage(preview)

    qr_label.configure(
        image=photo,
        text=""
    )

    qr_label.image = photo

    status_label.configure(
        text="Статус: QR-код успешно создан"
    )


def save_qr():
    global current_qr_image

    if current_qr_image is None:
        messagebox.showwarning(
            "Внимание",
            "Сначала сгенерируйте QR-код."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG файлы", "*.png")]
    )

    if file_path:
        current_qr_image.save(file_path)

        status_label.configure(
            text="Статус: PNG сохранён"
        )

        messagebox.showinfo(
            "Готово",
            "QR-код сохранён."
        )


def save_vcf():
    global current_vcard

    if not current_vcard:
        messagebox.showwarning(
            "Внимание",
            "Сначала сгенерируйте QR-код."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".vcf",
        filetypes=[("VCF файлы", "*.vcf")]
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(current_vcard)

        status_label.configure(
            text="Статус: Контакт сохранён"
        )

        messagebox.showinfo(
            "Готово",
            "Контакт сохранён."
        )


def clear_form():
    global current_qr_image
    global current_vcard

    for entry in entries.values():
        entry.delete(0, "end")

    qr_label.configure(
        image=None,
        text="QR-код появится здесь"
    )

    current_qr_image = None
    current_vcard = ""

    status_label.configure(
        text="Статус: Форма очищена"
    )


app = ctk.CTk()
app.title("CA-МАРК | QR Contact Generator")
app.geometry("1350x850")
app.resizable(False, False)

header_frame = ctk.CTkFrame(
    app,
    corner_radius=15
)
header_frame.pack(
    fill="x",
    padx=20,
    pady=(20, 10)
)

title_label = ctk.CTkLabel(
    header_frame,
    text="CA-МАРК | QR Contact Generator",
    font=("Arial", 28, "bold")
)
title_label.pack(pady=(15, 5))

subtitle_label = ctk.CTkLabel(
    header_frame,
    text="Создавайте QR-коды визиток быстро и удобно",
    font=("Arial", 14)
)
subtitle_label.pack(pady=(0, 15))

content_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
content_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

left_card = ctk.CTkFrame(
    content_frame,
    corner_radius=15
)

left_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)

right_card = ctk.CTkFrame(
    content_frame,
    corner_radius=15
)

right_card.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(10, 0)
)

contact_title = ctk.CTkLabel(
    left_card,
    text="Информация о контакте",
    font=("Arial", 20, "bold")
)

contact_title.pack(
    pady=(20, 20)
)

fields = [
    "Имя",
    "Фамилия",
    "Отчество",
    "Компания",
    "Должность",
    "Телефон 1",
    "Телефон 2",
    "Телефон 3",
    "Email",
    "Telegram",
    "WhatsApp",
    "Instagram",
    "Сайт"
]

entries = {}

for field in fields:

    row = ctk.CTkFrame(
        left_card,
        fg_color="transparent"
    )

    row.pack(
        fill="x",
        padx=20,
        pady=4
    )

    label = ctk.CTkLabel(
        row,
        text=field,
        width=120,
        anchor="w"
    )

    label.pack(
        side="left",
        padx=(0, 10)
    )

    entry = ctk.CTkEntry(
        row,
        width=300,
        height=34
    )

    entry.pack(
        side="left",
        fill="x",
        expand=True
    )

    entries[field] = entry

button_frame = ctk.CTkFrame(
    left_card,
    fg_color="transparent"
)

button_frame.pack(
    pady=25
)

generate_btn = ctk.CTkButton(
    button_frame,
    text="Сгенерировать QR",
    command=generate_qr,
    width=180,
    height=45,
    fg_color="#1565FF",
    hover_color="#0B4BD4"
)

generate_btn.grid(
    row=0,
    column=0,
    padx=5
)

save_png_btn = ctk.CTkButton(
    button_frame,
    text="Сохранить PNG",
    command=save_qr,
    width=160,
    height=45,
    fg_color="#10B981",
    hover_color="#059669"
)

save_png_btn.grid(
    row=0,
    column=1,
    padx=5
)

save_vcf_btn = ctk.CTkButton(
    button_frame,
    text="Сохранить VCF",
    command=save_vcf,
    width=160,
    height=45,
    fg_color="#7C3AED",
    hover_color="#6D28D9"
)

save_vcf_btn.grid(
    row=0,
    column=2,
    padx=5
)

clear_btn = ctk.CTkButton(
    button_frame,
    text="Очистить",
    command=clear_form,
    width=120,
    height=45,
    fg_color="#EF4444",
    hover_color="#DC2626"
)

clear_btn.grid(
    row=0,
    column=3,
    padx=5
)


qr_title = ctk.CTkLabel(
    right_card,
    text="QR-код визитки",
    font=("Arial", 20, "bold")
)

qr_title.pack(
    pady=(20, 20)
)

qr_label = ctk.CTkLabel(
    right_card,
    text="QR-код появится здесь",
    width=450,
    height=450
)

qr_label.pack(
    pady=(20, 10)
)

brand_label = ctk.CTkLabel(
    right_card,
    text="CA-МАРК",
    font=("Arial", 24, "bold")
)

brand_label.pack(
    pady=(5, 15)
)

status_label = ctk.CTkLabel(
    right_card,
    text="Статус: Готов к работе",
    font=("Arial", 13)
)

status_label.pack(
    pady=5
)

footer = ctk.CTkFrame(
    app,
    corner_radius=15
)

footer.pack(
    fill="x",
    padx=20,
    pady=(0, 20)
)

footer_label = ctk.CTkLabel(
    footer,
    text="Обязательные поля: Имя, Фамилия, Телефон 1",
    font=("Arial", 12)
)

footer_label.pack(
    pady=10
)

app.mainloop()