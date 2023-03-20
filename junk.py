import os
import shutil


def without_extension(_fileName):
    without_ext = os.path.splitext(_fileName)[0]
    return without_ext


def get_extension(_fileName):
    ext = os.path.splitext(_fileName)[1]
    return ext


src1 = "JunkFolders/Person1"
src2 = "JunkFolders/Person2"
dst = "JunkFolders/Person3"
method = False

src1_files = os.listdir(src1)
src1_files_wo_ext = []
for x in range(0, len(src1_files)):
    src1_files_wo_ext.append(without_extension(src1_files[x]))
print(src1_files)
print(src1_files_wo_ext)

src2_files_wo_ext = []
src2_files = os.listdir(src2)
for y in range(0, len(src2_files)):
    src2_files_wo_ext.append(without_extension(src2_files[y]))
# print(src2_files_wo_ext)
# Ortak isimdeki dosyaları farklı listeye atar.
common_files = set(src1_files_wo_ext) & set(src2_files_wo_ext)
print("Ortak isimdeki dosyalar:", common_files)
common_files_list = []
for x in common_files:
    common_files_list.append(x)
del common_files  # Delete common files set
print(common_files_list)

# src1 klasörü içerisindeki ortak dosyaları taşıma&kopyalama işlemi
for x in range(0, len(src1_files)):
    if without_extension(src1_files[x]) in common_files_list:
        if method:
            shutil.move(f"{src1}/{src1_files[x]}", dst)
        else:
            shutil.copy(f"{src1}/{src1_files[x]}", dst)

for y in range(0, len(src2_files)):
    if without_extension(src2_files[y]) in common_files_list:
        if method:
            shutil.move(f"{src2}/{src2_files[y]}", dst)
        else:
            shutil.copy(f"{src2}/{src2_files[y]}", dst)

