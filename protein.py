import csv
# 获取所有种类的氨基酸
with open("D:/2022/常用生物工具/蛋白组/IRGSP-1.0_protein_2022-09-01.fasta") as f:
    line_list = f.readlines()
    all_protein_type = ""
    for line in line_list:
        if line[0] != ">":
            for char in line:
                if char not in all_protein_type and char != "\n" :
                    all_protein_type += char
        else:
            continue

    print(all_protein_type)