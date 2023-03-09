<h1> TÜRKÇE </h1>

Dosya Operasyonları; dosyaların yeniden adlandırılması, uzantılarının değiştirilmesi, dosyaların taşınması ve kopyalanması gibi dosya yönetimi görevleri için çeşitli fonksiyonlar içerir. Ayrıca, en büyük dosyaların belirli bir klasörden diğerine taşınması, rastgele dosyaların taşınması, belirli bir boyuttan büyük dosyaların taşınması ve belirli bir tarihten sonra oluşturulan dosyaların taşınması gibi özellikleri de vardır.
Fonksiyonlar arasında dosya adlarını değiştirme, dosyaların boyutlarına göre sıralanması ve en büyük n dosyanın taşınması gibi işlemler yapmak için yardımcı işlevler de yer almaktadır. Örneğin, move_largest_files işlevi, en büyük n dosyanın kaynak klasörden hedef klasöre taşınmasını sağlar.
Bu program, dosya yönetimi görevlerini otomatikleştirmek için kullanılabilir ve birçok farklı senaryoda yararlıdır, örneğin, büyük dosyaların taşınması, belirli bir tarihten sonra oluşturulan dosyaların taşınması veya rastgele dosyaların taşınması gibi senaryolarda işleri kolaylaştırabilir.



**1. rename_files(folder_path):** Bu fonksiyon, bir klasördeki tüm görüntü dosyalarının isimlerini, 1'den başlayarak sıralı bir şekilde yeniden adlandırır. Yeni dosya adları, dosyanın orijinal uzantısına bağlı olarak ".jpg" veya ".png" uzantısına sahip olur.
**2. special_rename_files(path):** Bu fonksiyon, bir klasördeki tüm dosyaların adlarını alfabetik olarak "a.txt", "b.txt" vb. şeklinde başlayarak sıralı bir şekilde yeniden adlandırır. "z.txt" dosyasından sonra, fonksiyon dosyaları "aa.txt", "ab.txt", "ac.txt" vb. şeklinde iki harfli isimlerle adlandırır.
**3. change_extension(folder_path, old_extension, new_extension):** Bu fonksiyon, bir klasördeki belirli bir uzantıya sahip (eski_uzanti) tüm dosyaların uzantısını yeni bir uzantıya (yeni_uzanti) değiştirir.
**4. move_largest_files(src_folder, dst_folder, top_n):** Bu fonksiyon, kaynak klasörden en büyük n dosyayı hedef klasöre taşır.
**5. move_random_files2(src_folder, dst_folder, num_files):** Bu fonksiyon, kaynak klasörden belirtilen sayıda dosyayı rastgele olarak hedef klasöre taşır.
**6. move_by_size(src_folder, dst_folder, size_limit):** Bu fonksiyon, belirtilen boyuttan büyük tüm dosyaları kaynak klasörden hedef klasöre taşır.
**7. move_files_by_date(src_dir, dest_dir, date):** Bu fonksiyon, belirtilen tarihte veya daha sonra oluşturulan tüm dosyaları kaynak klasörden hedef klasöre taşır.
**8. move_random_files(src_folder, dst_folder, num_files, file_extension=None):** Bu fonksiyon, belirtilen sayıda dosyayı rastgele olarak kaynak klasörden hedef klasöre taşır. İsteğe bağlı olarak, uzanti parametresi kullanılarak taşınacak dosyaların uzantısı belirtilebilir.
**9. without_extension(_fileName):** Bu fonksiyon dosyanın uzantısı olmadan ismini döndürür.
**10. get_extension(_fileName):** Bu fonksiyon dosyanın uzantısını döndürür.
**11. move_common_files(src1, src2, dst):** Bu fonksiyon kaynak klasör 1 ve kaynak klasör 2'deki tüm dosyaları bir hedef klasöre taşır. Eğer her iki kaynak klasöründe aynı isimde dosyalar varsa, dosya kaynak klasör 1'den hedef klasöre taşınır. Eğer aynı dosya hedef klasörde mevcutsa, kaynak klasör 2'deki dosya sayısal bir ek ile yeniden adlandırılır ve daha sonra hedef klasöre taşınır.




<h1> ENGLISH </h1>
**1. rename_files(folder_path):** This function renames all image files in a folder with a new name in sequential order starting from 1. The new file names have a ".jpg" or ".png" extension depending on the original extension of the file.
**2. special_rename_files(path):** This function renames all files in a folder with names in alphabetical order, starting from "a.txt", "b.txt", etc. After "z.txt", the function uses two letters to name the files, such as "aa.txt", "ab.txt", "ac.txt", etc.
**3. change_extension(folder_path, old_extension, new_extension):** This function changes the extension of all files with a specific extension (old_extension) in a folder to a new extension (new_extension).
**4. move_largest_files(src_folder, dst_folder, top_n):** This function moves the largest n files from a source folder to a destination folder.
**5. move_random_files2(src_folder, dst_folder, num_files):** This function moves a specified number of files randomly from a source folder to a destination folder.
**6. move_by_size(src_folder, dst_folder, size_limit):** This function moves all files larger than a specified size from a source folder to a destination folder.
**7. move_files_by_date(src_dir, dest_dir, date):** This function moves all files from a source directory that were created on or after a specified date to a destination directory.
**8. move_random_files(src_folder, dst_folder, num_files, file_extension=None):** This function moves a specified number of files randomly from a source folder to a destination folder. An optional file_extension parameter can be used to specify the extension of the files that will be moved.
**9. without_extension(_fileName):** This function returns the name of a file without the extension.
**10. get_extension(_fileName):** This function returns the extension of a file.
**11. move_common_files(src1, src2, dst):** This function moves all files from source folder 1 and source folder 2 to a destination folder. If there are files with the same name in both source folders, the file in source folder 1 is moved to the destination folder. If the same file exists in the destination folder, the file in source folder 2 is renamed with a numeric suffix and then moved to the destination folder.