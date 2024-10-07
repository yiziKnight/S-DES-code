import numpy as np


def initial_permutation(Plainntext):# 初始置换
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    P = [Plainntext[i-1] for i in IP]
    return P

def inverse_initial_permutation(data):# 最终置换
    IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
    C = [data[i-1] for i in IP_inv]
    return C

def key_Generation(Key):# 密钥生成
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    key_p10 = [Key[i-1] for i in P10]# P10置换

    left_half = key_p10[:5]
    right_half = key_p10[5:]
    Leftshift1 = [2, 3, 4, 5, 1]
    Leftshift2 = [3, 4, 5, 1, 2]
    shifted_left1 = [left_half[i-1] for i in Leftshift1]
    shifted_right1 = [right_half[i-1] for i in Leftshift1]# 左右两半进行leftshift变换

    # 合并进行P8变换得到子密钥1
    combined_key1 = shifted_left1 + shifted_right1
    k1 = [combined_key1[i-1] for i in P8]

    shifted_left2 = [left_half[i - 1] for i in Leftshift2]
    shifted_right2 = [right_half[i - 1] for i in Leftshift2]  # 左右两半进行leftshift变换

    # 合并进行P8变换得到子密钥2
    combined_key2 = shifted_left2 + shifted_right2
    k2 = [combined_key2[i - 1] for i in P8]
    return k1, k2


def convert_to_binary(n):
    if n == 0:
        return [0, 0]
    elif n == 1:
        return [0, 1]
    elif n == 2:
        return [1, 0]
    elif n == 3:
        return [1, 1]
    else:
        return None

def f_function(data,subkey):
    # 扩展置换
    EPBox = [4, 1, 2, 3, 2, 3, 4, 1]
    EXdata = [data[i-1] for i in EPBox]

    # 加轮密钥
    xored_data = [EXdata[i] ^ subkey[i] for i in range(8)]

    # S盒替换
    sBox1 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 0, 2]
    ]
    sBox2 = [
        [0, 1, 2, 3],
        [2, 3, 1, 0],
        [3, 0, 1, 2],
        [2, 1, 0, 3]
    ]
    left_half = xored_data[:4]
    right_half = xored_data[4:]
    row1 = left_half[0]*2 + left_half[3] # 行
    col1 = left_half[1]*2 + left_half[2] # 列
    sBox1_output = sBox1[row1][col1] # sBox1的输出，为十进制
    sbox1 = convert_to_binary(sBox1_output)

    row2 = right_half[0]*2 + right_half[3]
    col2 = right_half[1]*2 + right_half[2]
    sBox2_output = sBox2[row2][col2]
    sbox2 = convert_to_binary(sBox2_output)

    sBox_output = sbox1 + sbox2
    # 置换
    SPBox = [2, 4, 3, 1]
    output = [sBox_output[i-1] for i in SPBox]
    return output

def tow_round_encryption(data,subkey1,subkey2):
    # 第一轮
    left_half = data[:4]
    right_half = data[4:]
    temp = f_function(right_half,subkey1)
    new_left_half = right_half
    new_right_half = [left_half[i] ^ temp[i] for i in range(4)]
    combined_data = new_left_half + new_right_half

    # 第二轮
    left_half = combined_data[:4]
    right_half = combined_data[4:]
    temp = f_function(right_half, subkey2)
    new_left_half = [left_half[i] ^ temp[i] for i in range(4)]
    new_right_half = right_half
    combined_data = new_left_half + new_right_half
    return combined_data

def tow_round_decryption(data,subkey1,subkey2):
    # 第一轮
    left_half = data[:4]
    right_half = data[4:]
    temp = f_function(right_half,subkey2)
    new_left_half = right_half
    new_right_half = [left_half[i] ^ temp[i] for i in range(4)]
    combined_data = new_left_half + new_right_half

    # 第二轮
    left_half = combined_data[:4]
    right_half = combined_data[4:]
    temp = f_function(right_half, subkey1)
    new_left_half = [left_half[i] ^ temp[i] for i in range(4)]
    new_right_half = right_half
    combined_data = new_left_half + new_right_half
    return combined_data