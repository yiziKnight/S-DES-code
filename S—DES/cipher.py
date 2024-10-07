import tkinter as tk
from tkinter import ttk
from tools import *

# 输入验证函数
def is_valid_binary_string(input_str):
    return all(char in '01' for char in input_str)

root = tk.Tk()
root.title("S-DES加解密工具")
root.geometry("400x300")

encryption_frame = ttk.Frame(root)
decryption_frame = ttk.Frame(root)

def show_encryption_frame():
    decryption_frame.pack_forget()
    encryption_frame.pack(fill='both',expand=True)

def show_decryption_frame():
    encryption_frame.pack_forget()
    decryption_frame.pack(fill='both',expand=True)

# 顶部导航按钮
nav_frame = ttk.Frame(root)
nav_frame.pack(side="top",fill="x")

encrypt_button = ttk.Button(nav_frame, text="加密", command=show_encryption_frame)
encrypt_button.pack(side="left", padx=5, pady=5)

decrypt_button = ttk.Button(nav_frame, text="解密", command=show_decryption_frame)
decrypt_button.pack(side="left", padx=5, pady=5)

# 加密界面组件
p_label = ttk.Label(encryption_frame, text="请输入明文 (0 和 1):(8位)")
p_label.pack(pady=5)

p_entry = ttk.Entry(encryption_frame)
p_entry.pack(pady=5)

k_label = ttk.Label(encryption_frame, text="请输入密钥 (0 和 1):(10位)")
k_label.pack(pady=5)

k_entry = ttk.Entry(encryption_frame)
k_entry.pack(pady=5)

encrypt_result_label = ttk.Label(encryption_frame, text="加密结果:")
encrypt_result_label.pack(pady=5)

# 加密函数
def encrypt():
    p_str = p_entry.get()
    k_str = k_entry.get()

    if not is_valid_binary_string(p_str) or not is_valid_binary_string(k_str):
        encrypt_result_label.config(text="输入有误，请输入只包含 0 和 1 的字符串。")
        return

    P = [int(char) for char in p_str]
    K = [int(char) for char in k_str]
    IP = initial_permutation(P)
    subkey1, subkey2 = key_Generation(K)
    step3 = tow_round_encryption(IP, subkey1, subkey2)
    C = inverse_initial_permutation(step3)
    encrypt_result_label.config(text=f"加密结果: {C}")

encrypt_button = ttk.Button(encryption_frame, text="加密", command=encrypt)
encrypt_button.pack(pady=10)

# 解密界面组件
c_label = ttk.Label(decryption_frame, text="请输入密文 (0 和 1):")
c_label.pack(pady=5)

c_entry = ttk.Entry(decryption_frame)
c_entry.pack(pady=5)

k_label_decrypt = ttk.Label(decryption_frame, text="请输入密钥 (0 和 1):")
k_label_decrypt.pack(pady=5)

k_entry_decrypt = ttk.Entry(decryption_frame)
k_entry_decrypt.pack(pady=5)

decrypt_result_label = ttk.Label(decryption_frame, text="解密结果:")
decrypt_result_label.pack(pady=5)

# 解密函数
def decrypt():
    c_str = c_entry.get()
    k_str = k_entry_decrypt.get()

    if not is_valid_binary_string(c_str) or not is_valid_binary_string(k_str):
        decrypt_result_label.config(text="输入有误，请输入只包含 0 和 1 的字符串。")
        return

    C = [int(char) for char in c_str]
    K = [int(char) for char in k_str]
    s1 = initial_permutation(C)
    subkey1, subkey2 = key_Generation(K)
    s2 = tow_round_decryption(s1, subkey1, subkey2)
    P = inverse_initial_permutation(s2)
    decrypt_result_label.config(text=f"解密结果: {P}")

decrypt_button = ttk.Button(decryption_frame, text="解密", command=decrypt)
decrypt_button.pack(pady=10)

# 默认显示加密界面
show_encryption_frame()

# 运行主循环
root.mainloop()
