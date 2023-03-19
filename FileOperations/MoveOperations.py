import os
import heapq
import random
import shutil
from os.path import exists
from datetime import datetime, timedelta
from tqdm import tqdm



def rename_files(folder_path):
    i = 1
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                new_filename = str(i) + ".jpg"
            elif filename.endswith(".png"):
                new_filename = str(i) + ".png"
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
            i += 1


def special_rename_files(path):  # I'm going to fix this later
    files = os.listdir(path)
    files.sort()
    for i, file_name in enumerate(files):
        new_file_name = ""
        if i < 26:
            new_file_name = chr(ord('a') + i) + ".txt"
        else:
            first_char = chr(ord('a') + (i // 26) - 1)
            second_char = chr(ord('a') + (i % 26))
            new_file_name = first_char + "_" + second_char + ".txt"
            if(exists(f'{path}/{new_file_name}')):
                pass
            else:
                os.rename(os.path.join(path, file_name), os.path.join(path, new_file_name))

def change_extension(folder_path):
    if os.path.exists(folder_path):
        old_extension = input("Enter the extensions that need to be changed:")
        new_extension = input("Enter the extension to be changed:")

        for filename in os.listdir(folder_path):
            if filename.endswith(old_extension):
                new_filename = filename.replace(old_extension, new_extension)
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
    else:
        new_folder_path = input("Yanlış dosya yolu girildi. Dosya yolunu tekrar giriniz: ")
        if new_folder_path.lower() == 'esc':
            return  # programdan çıkış yap
        else:
            change_extension(new_folder_path)

def move_largest_files(src_folder, dst_folder, top_n):
    files = [(os.path.join(src_folder, file), os.path.getsize(os.path.join(src_folder, file))) for file in os.listdir(src_folder)]
    largest_files = heapq.nlargest(top_n, files, key=lambda file: file[1])
    for file in largest_files:
        os.rename(file[0], os.path.join(dst_folder, os.path.basename(file[0])))


def move_random_files2(src_folder, dst_folder, num_files):
    files = [os.path.join(src_folder, file) for file in os.listdir(src_folder)]
    random_files = random.sample(files, num_files)
    for file in random_files:
        os.rename(file, os.path.join(dst_folder, os.path.basename(file)))


def move_by_size(src_folder, dst_folder, size_limit):  # size_limit parameter must be MegaByte
    size_limit = size_limit * 1024 * 1024  # convert to bytes
    for file_name in os.listdir(src_folder):
        file_path = os.path.join(src_folder, file_name)
        if os.path.getsize(file_path) > size_limit:
            dst_path = os.path.join(dst_folder, file_name)
            os.rename(file_path, dst_path)


def move_files_by_date(src_dir, dest_dir, date):
    target_date = datetime.strptime(date, '%Y-%m-%d')
    for file_name in os.listdir(src_dir):
        file_path = os.path.join(src_dir, file_name)
        file_date = datetime.fromtimestamp(os.path.getctime(file_path))
        # Dosya oluşturulma, belirlenen tarihten sonra ise
        if file_date >= target_date:
            # Dosyayı hedef klasöre taşı
            os.rename(file_path, dest_dir)

def move_random_files(src_folder, dst_folder, num_files, file_extension=None):
    """
    Move random files from one folder to another.
    src_folder:     The source folder where files are located.
    dst_folder:     The destination folder where files will be moved to.
    num_files:      Number of files to move.
    file_extension: The extension of files that will be moved.
    """
    if not os.path.exists(src_folder):
        raise ValueError(f"Source folder {src_folder} does not exist.")
    if not os.path.exists(dst_folder):
        raise ValueError(f"Destination folder {dst_folder} does not exist.")
    if not os.path.isdir(src_folder):
        raise ValueError(f"{src_folder} is not a folder.")
    if not os.path.isdir(dst_folder):
        raise ValueError(f"{dst_folder} is not a folder.")
    if num_files <= 0:
        raise ValueError(f"num_files({num_files}) can't be less than 1.")
    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f)) and (file_extension is None or f.endswith(file_extension))]
    if num_files > len(files):
        raise ValueError(f"num_files({num_files}) can't be greater than number of files({len(files)}).")
    selected_files = random.sample(files, num_files)

    for file in selected_files:
        src_file = os.path.join(src_folder, file)
        dst_file = os.path.join(dst_folder, file)
        os.rename(src_file, dst_file)



def without_extension(_fileName):
    without_ext = os.path.splitext(_fileName)[0]
    return without_ext


def get_extension(_fileName):
    ext = os.path.splitext(_fileName)[1]
    return ext


def move_common_files(src1, src2, dst):
    src1_files = os.listdir(src1)
    print(src1_files)
    src1_files_wo_ext = []
    for x in range(0, len(src1_files)):
        src1_files_wo_ext.append(without_extension(src1_files[x]))
    print(src1_files_wo_ext)

    src2_files_wo_ext = []
    src2_files = os.listdir(src2)
    for y in range(0, len(src2_files)):
        src2_files_wo_ext.append(without_extension(src2_files[y]))
    print(src2_files_wo_ext)
    common_files = set(src1_files_wo_ext) & set(src2_files_wo_ext)
    print(len(common_files))
    for x in range(0, len(common_files)):
        src1_path = os.path.join(src1, file_name)
        print(src1_path)
        src2_path = os.path.join(src2, file_name)
        print(src2_path)
        dst_path = os.path.join(dst, file_name)
        print(dst_path)
        src1_ext = os.path.splitext(src1_path)[1]
        src2_ext = os.path.splitext(src2_path)[1]
        if src1_ext != src2_ext:
           # os.rename(src1_path, dst_path)
            os.rename(src2_path, dst_path)

def get_folder_ext_types(_path):
    ext_types = []
    folder_files = os.listdir(_path)
    for xy in range(0, len(os.listdir(_path))):
        if get_extension(folder_files[xy]) not in ext_types:
            ext_types.append(get_extension(folder_files[xy]))
        else:
            pass
    return ext_types


def copy_or_transport_spesify_ext_files(_path, _dest_path, _spc_ext, method = True):
    total_files = len(os.listdir(_path))
    spc_ext_files = []
    for xq in range(0, total_files):
        if os.listdir(_path)[xq] == _spc_ext:
            spc_ext_files.append(os.listdir(_path)[xq])

    processed_files = len(spc_ext_files)

    with tqdm(total = processed_files) as pbar:
        for xx in range(0, total_files):
            file_name = os.listdir(_path)[xx]
            if get_extension(file_name) == _spc_ext:
                if method:
                    shutil.copy(f'{_path}/{file_name}', _dest_path)
                else:
                    shutil.move(f'{_path}/{file_name}', _dest_path)
                    total_files -= 1
                pbar.update(1)



folder_path = ''
dest_path = ''
copy_or_transport_spesify_ext_files(folder_path, dest_path, '.AAE', 0)


#print(get_folder_ext_types(folder_path))

#for x in range(0, len(os.listdir(folder_path))):
#    #print(get_extension(os.listdir(folder_path)[x]))
#    file_name = os.listdir(folder_path)[x]
#    if get_extension(file_name) == '.PNG':
#        print("Hello ")
#        shutil.copy(f'{folder_path}/{file_name}', dest_path)
#    else:
#        pass
#


# move_common_files('../Person1', '../Person2', '../Person3')
# change_extension(input("File Path:"))
# move_largest_files('Person2','Person1' , 15)
# move_random_files('Person1', 'Person2', 20)
# special_rename_files('Person3')
# move_files_by_date(src_dir, dest_dir, "2022-01-01")
# move_by_size(src_folder, dst_folder, 100)




