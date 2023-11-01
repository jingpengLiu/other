# 1、获取jasper的页面
# 2、下载对应的sites
# 3、下载对应的protein
# 4、创建一个文件夹把sites和protein存到里面
import time

import requests
from bs4 import BeautifulSoup
import os
import shutil
import re


# 得到对应url的html页面
def get_html(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
    }
    html = requests.get(url, headers=header)
    html = html.text
    return html


# 得到protein 网站的html
def get_sequence_html(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
    }
    html = requests.get(url, headers=header)
    html = html.text
    return html


# 得到蛋白名字
def get_name(html):
    soup = BeautifulSoup(html, "lxml")
    name = soup.find(attrs={'id': 'profile-detail'})
    name = name.find_all('td')
    name = name[1].text
    return name


# 得到蛋白地址
def get_uniprot_url(html):
    soup = BeautifulSoup(html, "lxml")
    soup = soup.find_all('div', attrs={'class': 'col-md-8'})[2]
    soup = soup.find_all('a')[1]
    url = soup.get("href")
    return url


# 得到蛋白序列url
def get_sequence_url(url):
    key = url.split("/")[4]
    str = f"https://rest.uniprot.org/uniprotkb/{key}.fasta"
    return str

# 保存数据
def save_data(number, protein_name, protein_sequence, dna_name, target_sequence):
    dir = f"./jasper_data/{number}"
    if os.path.exists(dir):
        print("文件夹已存在")
    else:
        os.makedirs(dir)
    with open (f"{dir}/{dna_name}.sites", "w+") as f:
        f.write(target_sequence)
    with open(f"{dir}/{protein_name}.fasta", "w+") as f:
        f.write(protein_sequence)

# 下载dna_sequence
def download_sequence(html):
    if re.findall("FASTA file", html):
        soup = BeautifulSoup(html, "lxml")
        a_tag = soup.find_all('a' , attrs={"target": "_blank"})
        url = a_tag[11].get('href')
        url = f"https://jaspar.genereg.net{url}"
        myfile = requests.get(url)
        target_sequence = myfile.text
        return target_sequence
    else:
        return False


if __name__ == '__main__':
    number = 1
    with open("./jasper_at.txt") as infile:
        targets = infile.readlines()
        for target in targets:
            if target[0] == '>':
                try:
                    time.sleep(1)
                    html = get_html(f"https://jaspar.genereg.net/matrix/{target[1:9]}/") # 获得jasper网站html
                    target_sequence = download_sequence(html)
                    if target_sequence == False:
                        continue
                    else:
                        name = get_name(html) # 从jasper网站中得到蛋白名称
                        url = get_uniprot_url(html) # 得到对应蛋白uniprot网站地址
                        sequence_url = get_sequence_url(url) # 得到对应蛋白序列地址
                        uniprot_sequence = get_sequence_html(sequence_url) # 得到蛋白序列html
                        save_data(number, name, uniprot_sequence, target[1:9], target_sequence)
                        print(number, name, target[1:9])
                        number += 1
                except Exception:
                    print(Exception)
                    continue


