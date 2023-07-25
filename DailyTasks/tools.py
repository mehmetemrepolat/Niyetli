from Niyetli.database.db_connector import Database

# Ben buradaki listelerde işlem yaparak veri elde etmeye çalışacağım.
def index_distinct_elements(lst, index): # Liste ver, hangi index'leri gruplaması gerektiğini ver.
    if not all(isinstance(item, list) for item in lst):
        lst = [list(item) for item in lst]
    indexed_groups = []
    counter = 0
    pointer = ""
    for x in range(0, len(lst)):
        if lst[x][index] != pointer:
            pointer = lst[x][index]  # Eşitledik.
            indexed_groups.append([lst[x][index], x])  # burada x. indexteki elamanı ekledik.
            counter += 1
        else:
            pass
    return indexed_groups  # Farklı index gruplarını sana versin


print(index_distinct_elements(my_list, 2))


