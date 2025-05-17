import tkinter as tk
from tkinter import ttk
import random

class TaiXiuBot:
    def __init__(self, master):
        self.master = master
        self.master.title("Bot chơi Tài Xỉu Khang Osaka")
        self.master.geometry("450x500")

        # Biến trạng thái
        self.color_xanh = "#26a1ff"
        self.color_do = "#f94168"
        self.color_bg = "#f0f0f0"
        self.color_bg_label = "#282a2d"
        self.von = 100000
        self.cuoc_mac_dinh = 0
        self.cuoc_hien_tai = 0
        self.lua_chon = ""
        self.dang_thua = False
        self.chuoi_1324 = [1, 3, 2, 4]
        self.vi_tri_1324 = 0
        self.chien_thuat = tk.StringVar(value="Bot gợi ý")
        self.lua_chon_tay = tk.StringVar(value="Tài")

        # Giao diện người dùng
        tk.Label(master, text="Nhập vốn (VND):", bg=self.color_bg).pack()
        vcmd = (self.master.register(self.chi_nhap_so), "%P")
        self.entry_von = tk.Entry(self.master, validate="key", validatecommand=vcmd)
        self.entry_von.pack()
        #self.entry_von.insert(0, "{:,}".format(self.von))  # Hiển thị vốn ban đầu
        # Cập nhật số vốn mỗi khi người dùng nhập
        self.entry_von.bind("<KeyRelease>", self.format_entry)

        tk.Label(master, text="Chọn chiến thuật: ", bg=self.color_bg).pack()
        self.combo_chien_thuat = ttk.Combobox(master, textvariable=self.chien_thuat,
                                              values=["Bot gợi ý", "Gấp thếp", "1-3-2-4", "Đánh đều tay", "Tự chọn Tài/Xỉu"],
                                              state="readonly")
        self.combo_chien_thuat.pack()
        self.combo_chien_thuat.bind("<<ComboboxSelected>>", self.on_chien_thuat_change)

        # Tùy chọn tay người dùng (ẩn mặc định)
        self.frame_tu_chon = tk.Frame(master)
        tk.Label(self.frame_tu_chon, text="Chọn Tài hoặc Xỉu:", bg=self.color_bg).pack()
        tk.Radiobutton(self.frame_tu_chon, text="Tài", variable=self.lua_chon_tay, value="Tài").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(self.frame_tu_chon, text="Xỉu", variable=self.lua_chon_tay, value="Xỉu").pack(side=tk.LEFT, padx=10)

        # Nút bắt đầu
        self.btn_batdau = tk.Button(master, text="Bắt đầu cược", command=self.bat_dau)
        self.btn_batdau.pack(pady=10)

        # Thông báo
        self.label_thongbao = tk.Label(master, text="", font=("Arial", 12, "bold", ), bg=self.color_bg)
        self.label_thongbao.pack()

        self.label_cuoc = tk.Label(master, text="")
        self.label_cuoc.pack()

        self.label_von = tk.Label(master, text="")
        self.label_von.pack()

        # Nút kết quả
        # Nút kết quả (cho vào frame riêng để sắp đẹp)
        self.frame_ket_qua = tk.Frame(master)
        self.btn_hup = tk.Button(self.frame_ket_qua, text="Húp", command=self.hup, background=self.color_xanh)
        self.btn_gay = tk.Button(self.frame_ket_qua, text="Gãy", command=self.gay, background=self.color_do)
        #self.btn_hup.pack(side=tk.LEFT, padx=10, pady=5)
        #self.btn_gay.pack(side=tk.LEFT, padx=10, pady=5)
        self.frame_ket_qua.pack()

        # Lịch sử
        tk.Label(master, text="\nLịch sử cược:").pack()
        self.text_lich_su = tk.Text(master, height=10, width=60)
        self.text_lich_su.pack()
        self.text_lich_su.tag_config("win", background=self.color_xanh)
        self.text_lich_su.tag_config("lose", background=self.color_do)

        self.master.configure(bg=self.color_bg)
    # Hàm format_tien:
    def format_tien(self, so):
        return "{:,}".format(so)

    def format_entry(self, event=None):
        value = self.entry_von.get().replace(",", "").strip()
        if value.isdigit():
            formatted = "{:,}".format(int(value))
            self.entry_von.delete(0, tk.END)
            self.entry_von.insert(0, formatted)
        elif value == "":
            return
        else:
            self.entry_von.delete(0, tk.END)
    def chi_nhap_so(self, value):
        value = value.replace(",", "")
        return value.isdigit() or value == ""

    def on_chien_thuat_change(self, event=None):
        if self.chien_thuat.get() == "Tự chọn Tài/Xỉu":
            self.frame_tu_chon.pack()
        else:
            self.frame_tu_chon.pack_forget()
    def cap_nhat_von(self):
        try:
            self.entry_von.delete(0, tk.END)
            self.entry_von.insert(0, self.format_tien(self.von))
            self.von = int(self.entry_von.get().replace(",", "").strip())

        except:
            pass

    def bat_dau(self):
        try:
            self.von = int(self.entry_von.get().replace(",", "").strip())
            if self.von <= 0:
                raise ValueError
        except ValueError:
            self.label_thongbao.config(text="Nhập vốn đê !")
            return

        self.cuoc_mac_dinh = int(self.von * 0.01)
        self.cuoc_hien_tai = self.cuoc_mac_dinh
        self.vi_tri_1324 = 0

        #self.entry_von.config(state="disabled")
        self.combo_chien_thuat.config(state="disabled")
        self.btn_batdau.config(state="disabled")
        self.frame_tu_chon.pack_forget()
        self.btn_hup.pack(side=tk.LEFT, padx=10, pady=5)
        self.btn_gay.pack(side=tk.LEFT, padx=10, pady=5)
        self.frame_ket_qua.pack()
        self.de_xuat()

    def de_xuat(self):
        chien_thuat = self.chien_thuat.get()

        if chien_thuat == "Bot gợi ý":
            self.lua_chon = random.choice(["Tài", "Xỉu"])
        elif chien_thuat == "Gấp thếp":
            self.lua_chon = "Tài"
        elif chien_thuat == "Đánh đều tay":
            self.lua_chon = "Xỉu"
            self.cuoc_hien_tai = self.cuoc_mac_dinh
        elif chien_thuat == "1-3-2-4":
            he_so = self.chuoi_1324[self.vi_tri_1324]
            self.cuoc_hien_tai = he_so * self.cuoc_mac_dinh
            self.lua_chon = "Tài"
        elif chien_thuat == "Tự chọn Tài/Xỉu":
            self.lua_chon = self.lua_chon_tay.get()
            self.cuoc_hien_tai = self.cuoc_mac_dinh

        # Gợi ý
        self.label_thongbao.config(text=f"Chiến thuật: \n{chien_thuat} → {self.lua_chon}")
        self.label_cuoc.config(text=f"Cược đề xuất: {self.format_tien(self.cuoc_hien_tai)} VND")
        self.label_von.config(text=f"Vốn còn lại: {self.format_tien(self.von)} VND")

        # Hiện nút
        self.btn_hup.pack(pady=5)
        self.btn_gay.pack(pady=5)

    def hup(self):
        self.von += self.cuoc_hien_tai
        self.cap_nhat_von()
        if self.chien_thuat.get() == "1-3-2-4":
            if self.vi_tri_1324 < 3:
                self.vi_tri_1324 += 1
            else:
                self.vi_tri_1324 = 0
        else:
            self.cuoc_hien_tai = self.cuoc_mac_dinh

        self.ghi_lich_su("Húp", self.format_tien(self.cuoc_hien_tai))
        self.de_xuat()

    def gay(self):
        self.von -= self.cuoc_hien_tai
        self.cap_nhat_von()
        if self.chien_thuat.get() in ["Bot gợi ý", "Gấp thếp"]:
            self.cuoc_hien_tai *= 2
        elif self.chien_thuat.get() == "1-3-2-4":
            self.vi_tri_1324 = 0
        elif self.chien_thuat.get() == "Tự chọn Tài/Xỉu":
            self.cuoc_hien_tai = self.cuoc_mac_dinh

        if self.von <= 0:
            self.label_thongbao.config(text="Hết vốn!")
            self.label_cuoc.config(text="Chơi tiếp Không ?.")
            self.label_von.config(text="Cờ bạc người không chơi là người thắng")
            self.btn_hup.pack_forget()
            self.btn_gay.pack_forget()
            self.btn_batdau.config(state="active")
            return

        if self.cuoc_hien_tai > self.von:
            self.cuoc_hien_tai = self.von

        self.ghi_lich_su("Gãy", self.format_tien(self.cuoc_hien_tai))
        self.de_xuat()

    def ghi_lich_su(self, ket_qua, tien):
        if ket_qua == "Húp":
            text = f"✅ Húp +{tien} VND\n"
            self.text_lich_su.insert(tk.END, text, "win")
        else:
            text = f"❌ Gãy -{tien} VND\n"
            self.text_lich_su.insert(tk.END, text, "lose")
        self.text_lich_su.see(tk.END)
    
    

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = TaiXiuBot(root)
    root.mainloop()
