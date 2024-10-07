import time
import tkinter as tk
from tkinter import ttk
from tools import *

# 输入验证函数
def is_valid_binary_string(input_str):
    return all(char in '01' for char in input_str)

def ascii_str_to_binary_str_list(ascii_str):
    return [bin(ord(char))[2:].zfill(8) for char in ascii_str]

def binary_str_list_to_ascii_str(binary_str_list):
    return "".join([chr(int(binary_str, 2)) for binary_str in binary_str_list])


root = tk.Tk()
root.title("S-DES加解密工具")
root.geometry("400x300")

encryption_frame = ttk.Frame(root)
decryption_frame = ttk.Frame(root)
brute_force_cracking_frame = ttk.Frame(root)

def show_encryption_frame():
    decryption_frame.pack_forget()
    brute_force_cracking_frame.pack_forget()
    encryption_frame.pack(fill='both',expand=True)

def show_decryption_frame():
    encryption_frame.pack_forget()
    brute_force_cracking_frame.pack_forget()
    decryption_frame.pack(fill='both',expand=True)

def show_brute_force_creaking_frame():
    encryption_frame.pack_forget()
    decryption_frame.pack_forget()
    brute_force_cracking_frame.pack(fill='both',expand=True)

# 顶部导航按钮
nav_frame = ttk.Frame(root)
nav_frame.pack(side="top",fill="x")

encrypt_button = ttk.Button(nav_frame, text="加密", command=show_encryption_frame)
encrypt_button.pack(side="left", padx=5, pady=5)

decrypt_button = ttk.Button(nav_frame, text="解密", command=show_decryption_frame)
decrypt_button.pack(side="left", padx=5, pady=5)

brute_force_cracking_button = ttk.Button(nav_frame, text="暴力破解", command=show_brute_force_creaking_frame)
brute_force_cracking_button.pack(side="left", padx=5, pady=5)

# 加密界面组件
p_label = ttk.Label(encryption_frame, text="请输入明文 :")
p_label.pack(pady=5)

p_entry = ttk.Entry(encryption_frame)
p_entry.pack(pady=5)

k_label = ttk.Label(encryption_frame, text="请输入密钥 :")
k_label.pack(pady=5)

k_entry = ttk.Entry(encryption_frame)
k_entry.pack(pady=5)

encrypt_result_label = ttk.Label(encryption_frame, text="加密结果:")
encrypt_result_label.pack(pady=5)

# 加密函数
def encrypt():
    p_str = p_entry.get()
    k_str = k_entry.get()

    if not is_valid_binary_string(k_str):
        encrypt_result_label.config(text="输入有误，请输入只包含 0 和 1 的字符串。")
        return

    #判断明文是ASCII码还是二进制数
    is_binary_plaintext = all(char in '01' for char in p_str)
    if is_binary_plaintext:
        P = [int(char) for char in p_str]
        K = [int(char) for char in k_str]
        print(P)
        IP = initial_permutation(P)
        subkey1, subkey2 = key_Generation(K)
        step3 = tow_round_encryption(IP, subkey1, subkey2)
        C = inverse_initial_permutation(step3)
        encrypt_result_label.config(text=f"加密结果: {C}")
    else:
        binary_plaintext_list = ascii_str_to_binary_str_list(p_str)
        encrypted_binary_chunks = []
        for binary_chunk in binary_plaintext_list:
            P = [int(char) for char in binary_chunk]
            K = [int(char) for char in k_str]
            IP = initial_permutation(P)
            subkey1, subkey2 = key_Generation(K)
            step3 = tow_round_encryption(IP, subkey1, subkey2)
            encrypted_chunk = inverse_initial_permutation(step3)
            encrypted_binary_chunks.append("".join(map(str, encrypted_chunk)))
        ascii_str = binary_str_list_to_ascii_str(encrypted_binary_chunks)
        print(ascii_str)
        encrypt_result_label.config(text=f"加密结果：{ascii_str}")

encrypt_button = ttk.Button(encryption_frame, text="加密", command=encrypt)
encrypt_button.pack(pady=10)

# 解密界面组件
c_label = ttk.Label(decryption_frame, text="请输入密文 :")
c_label.pack(pady=5)

c_entry = ttk.Entry(decryption_frame)
c_entry.pack(pady=5)

k_label_decrypt = ttk.Label(decryption_frame, text="请输入密钥 :")
k_label_decrypt.pack(pady=5)

k_entry_decrypt = ttk.Entry(decryption_frame)
k_entry_decrypt.pack(pady=5)

decrypt_result_label = ttk.Label(decryption_frame, text="解密结果:")
decrypt_result_label.pack(pady=5)

# 解密函数
def decrypt():
    c_str = c_entry.get()
    k_str = k_entry_decrypt.get()

    if not is_valid_binary_string(k_str):
        decrypt_result_label.config(text="输入有误，请输入只包含 0 和 1 的字符串。")
        return

    is_binary_plaintext = all(char in '01' for char in c_str)
    if is_binary_plaintext:
        C = [int(char) for char in c_str]
        K = [int(char) for char in k_str]
        s1 = initial_permutation(C)
        subkey1, subkey2 = key_Generation(K)
        s2 = tow_round_decryption(s1, subkey1, subkey2)
        P = inverse_initial_permutation(s2)
        decrypt_result_label.config(text=f"解密结果: {P}")
    else:
        binary_ciphertext_list = ascii_str_to_binary_str_list(c_str)
        decrypted_binary_chunks = []
        for binary_chunk in binary_ciphertext_list:
            C = [int(char) for char in binary_chunk]
            K = [int(char) for char in k_str]
            s1 = initial_permutation(C)
            subkey1, subkey2 = key_Generation(K)
            s2 = tow_round_decryption(s1, subkey1, subkey2)
            decrypted_chunk = inverse_initial_permutation(s2)
            decrypted_binary_chunks.append("".join(map(str,decrypted_chunk)))
        decrypted_ascii_str = binary_str_list_to_ascii_str(decrypted_binary_chunks)
        decrypt_result_label.config(text=f"解密结果：{decrypted_ascii_str}")


decrypt_button = ttk.Button(decryption_frame, text="解密", command=decrypt)
decrypt_button.pack(pady=10)

# 暴力界面组件
P_label = ttk.Label(brute_force_cracking_frame, text="请输入明文 :")
P_label.pack(pady=5)

P_entry = ttk.Entry(brute_force_cracking_frame)
P_entry.pack(pady=5)

C_label = ttk.Label(brute_force_cracking_frame, text="请输入密文 :")
C_label.pack(pady=5)

C_entry = ttk.Entry(brute_force_cracking_frame)
C_entry.pack(pady=5)

brute_result_label = ttk.Label(brute_force_cracking_frame, text="破解结果:")
brute_result_label.pack(pady=5)

def brute():
    p_str = P_entry.get()
    c_str = C_entry.get()
    if not is_valid_binary_string(c_str) or not is_valid_binary_string(p_str):
        decrypt_result_label.config(text="输入有误，请输入只包含 0 和 1 的字符串。")
        return

    start_time = time.time()
    aa = brute_force_cracking(p_str,c_str)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"破解用时：{elapsed_time}秒")
    brute_result_label.config(text=f"解密结果：{aa}")

brute_force_cracking_button = ttk.Button(brute_force_cracking_frame, text="破解", command=brute)
brute_force_cracking_button.pack(pady=10)

# 默认显示加密界面
show_encryption_frame()

# 运行主循环
root.mainloop()