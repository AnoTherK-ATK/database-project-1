# import some lib
import pandas as pd
import numpy as np
import os
from unidecode import unidecode


#read lookup data
lk_cap = pd.read_excel("data/lookup_cap.xlsx")
lk_lh = pd.read_excel("data/lookup_loai_hinh.xlsx")
lk_lt = pd.read_excel("data/lookup_loai_truong.xlsx")
lk_pgd = pd.read_excel("data/lookup_pgd.xlsx")

#read data
gdtx = pd.read_excel("data/data_gdtx.xlsx")
mn = pd.read_excel("data/data_mn.xlsx")
th = pd.read_excel("data/data_th.xlsx")
thcs = pd.read_excel("data/data_thcs.xlsx")
thpt = pd.read_excel("data/data_thpt.xlsx")

def xx(leng):
    ans = ""
    for i in range(leng):
        ans += "X"
    return ans

def inslk(a, f, table, leng):
    for index, row in a.iterrows():
        # ma = unidecode(str(row["ma_" + table]))
        # print(ma)
        # ten = unidecode(str(row["ten_" + table]))
        
        ma = str(row["ma_" + table])
        ten = str(row["ten_" + table])
        
        if(ten == "nan"):
            ten = "NULL"
        f.write("INSERT INTO " + table + " VALUES (" + "'" + ma + "'" + ", '" + ten + "');\n")

def lookup():
    f = open("data/lookup.sql", "w", encoding = "utf-8")
    inslk(lk_cap, f, "cap", 2)
    inslk(lk_lt, f, "lt", 6)
    inslk(lk_lh, f, "lh", 5)
    inslk(lk_pgd, f, "pgd", 3)

def ins(arr, name, cap):
    with open("data/" + name + ".sql", "w", encoding="utf-8") as f:
        f.write("USE truonghoc;\n")
        for index, row in arr.iterrows():
            # ma = unidecode(str(row["ma_truong"]))
            # ten = unidecode(str(row["ten_truong"]))
            # dc = unidecode(str(row["dia_chi"]))
            
            ma = str(row["ma_truong"])
            ten = str(row["ten_truong"])
            dc = str(row["dia_chi"])
            
            if(dc == "nan"):
                dc = unidecode("Không có")
            lh = unidecode(str(row["loai_hinh"]))
            if(lh == "nan"):
                lh = xx(5)
            lt = unidecode(str(row["loai_truong"]))
            if(lt == "nan"):
                lt = xx(6)
            pgd = unidecode(str(row["phong_gd"]))
            if(pgd == "nan"):
                pgd = xx(3)
            f.write("INSERT INTO ds_truong VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');\n".format(ma, ten, dc, lh, lt, pgd, cap))
            # f.write("NHỮNG CHỮ CÓ DẤU")

lookup() 
ins(gdtx, "gdtx", "TX")
ins(mn, "mn", "MN")
ins(th, "th", "TH")
ins(thcs, "thcs", "CS")
ins(thpt, "thpt", "PT")