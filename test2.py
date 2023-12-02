img_dir = "D:/MANGAS/Ibitsu/Chapter 6.5/36.jpg"
directory = "/".join(img_dir.split("/")[:-1])
name = img_dir.split("/")[-1].split(".")[0]
ext = img_dir.split("/")[-1].split(".")[-1]
print(name+ext)