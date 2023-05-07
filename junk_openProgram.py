import os
from FileOperations import MoveOperations

def program_ac(dosya_yolu):
    try:
        if os.path.exists(dosya_yolu):  # Dosya var mı kontrolü yapılıyor

            file_name_inPath = dosya_yolu.split('/')[-1]
            if '.' in file_name_inPath:
                file_name_inPath = file_name_inPath.split('.')[0]
            files = MoveOperations.get_file_names_inFolder(os.path.dirname(path))
            if file_name_inPath in files:
                os.startfile(dosya_yolu)
        else:
            return "Belirtilen dosya yolu geçerli değil."

    except:
        return "Program açılırken bir hata oluştu."


path = "C:/Users/Emre/Desktop/Niyetli"





program_ac(str(path))  # Internet Explorer açar

#print(os.path.dirname(path))