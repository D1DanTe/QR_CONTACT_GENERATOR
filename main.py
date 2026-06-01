import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

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
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr.add_data(current_vcard)
    qr.make(fit=True)

    current_qr_image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    preview = current_qr_image.resize((350, 350))
    photo = ImageTk.PhotoImage(preview)

    qr_label.configure(image=photo)
    qr_label.image = photo

    status_label.config(
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

        status_label.config(
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
        filetypes=[("vCard", "*.vcf")]
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(current_vcard)

        status_label.config(
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
        entry.delete(0, tk.END)

    qr_label.configure(image="")
    qr_label.image = None

    current_qr_image = None
    current_vcard = ""

    status_label.config(
        text="Статус: Форма очищена"
    )


root = tk.Tk()
root.title("QR Contact Generator")
root.geometry("1250x800")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="QR Contact Generator",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

left_frame = tk.Frame(main_frame)
left_frame.pack(side="left", padx=20, pady=20)

right_frame = tk.Frame(main_frame)
right_frame.pack(side="right", padx=20, pady=20)

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
    row = tk.Frame(left_frame)
    row.pack(fill="x", pady=4)

    label = tk.Label(
        row,
        text=field,
        width=15,
        anchor="w"
    )
    label.pack(side="left")

    entry = tk.Entry(
        row,
        width=45
    )
    entry.pack(side="left")

    entries[field] = entry

generate_btn = tk.Button(
    left_frame,
    text="Сгенерировать QR",
    width=30,
    command=generate_qr
)
generate_btn.pack(pady=(20, 5))

save_btn = tk.Button(
    left_frame,
    text="Сохранить PNG",
    width=30,
    command=save_qr
)
save_btn.pack(pady=5)

save_vcf_btn = tk.Button(
    left_frame,
    text="Сохранить VCF",
    width=30,
    command=save_vcf
)
save_vcf_btn.pack(pady=5)

clear_btn = tk.Button(
    left_frame,
    text="Очистить форму",
    width=30,
    command=clear_form
)
clear_btn.pack(pady=5)

qr_label = tk.Label(
    right_frame,
    text="QR-код появится здесь",
    font=("Arial", 12)
)
qr_label.pack(pady=20)

status_label = tk.Label(
    right_frame,
    text="Статус: Готов к работе",
    font=("Arial", 11)
)
status_label.pack(pady=10)

root.mainloop()