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

#create dictionary
dcap = {}
dlh = {}
dlt = {}
dpgd = {}
#null data
def xx(leng):
    ans = ""
    for i in range(leng):
        ans += "X"
    return ans

#insert all the table
def inslk(a, f, table, leng, d):
    for index, row in a.iterrows():
        ma = str(row["ma_" + table])
        ten = str(row["ten_" + table])
        if(ten == "nan"):
            ten = "NULL"
        d[ten] = ma
        f.write("INSERT INTO " + table + " VALUES (" + "'" + ma + "'" + ", '" + ten + "');\n")

#insert lookup table
def lookup():
    f = open("data/lookup.sql", "w", encoding = "utf-8")
    f.write("USE truonghoc;\n")
    inslk(lk_cap, f, "cap", 2, dcap)
    inslk(lk_lt, f, "lt", 6, dlt)
    inslk(lk_lh, f, "lh", 5, dlh)
    inslk(lk_pgd, f, "pgd", 3, dpgd)

#insert to main table
def ins(arr, name, cap):
    with open("data/" + name + ".sql", "w", encoding="utf-8") as f:
        f.write("USE truonghoc;\n")
        for index, row in arr.iterrows():
            ma = str(row["ma_truong"])
            ten = str(row["ten_truong"])
            dc = str(row["dia_chi"])
            
            if(dc == "nan"):
                dc = unidecode("Không có")
            lh = unidecode(str(row["loai_hinh"]))
            if(lh == "nan"):
                lh = xx(5)
            lh = dlh[lh]
            lt = unidecode(str(row["loai_truong"]))
            if(lt == "nan"):
                lt = xx(6)
            lt = dlt[lt]
            pgd = unidecode(str(row["phong_gd"]))
            if(pgd == "nan"):
                pgd = xx(3)
            pgd = dpgd[pgd]
            f.write("INSERT INTO ds_truong VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');\n".format(ma, ten, dc, lh, lt, pgd, cap))

lookup() 
ins(gdtx, "gdtx", "TX")
ins(mn, "mn", "MN")
ins(th, "th", "TH")
ins(thcs, "thcs", "CS")
ins(thpt, "thpt", "PT")