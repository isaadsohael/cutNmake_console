import os
from PIL import Image


def crop_action(img_dir):
    img = Image.open(img_dir)
    save_dir = "/".join(img_dir.split("/")[:-1])
    img_name = img_dir.split("/")[-1].split(".")[0]
    img_extension = img_dir.split("/")[-1].split(".")[-1]
    right = img.crop((int(img.width / 2), 0, img.width, img.height))
    right.save(f"{save_dir}/{img_name}.1.{img_extension}")
    left = img.crop((0, 0, int(img.width / 2), img.height))
    left.save(f"{save_dir}/{img_name}.2.{img_extension}")


class Manga:
    def __init__(self, path):
        self.path = path

    def crop(self):
        chapters = os.listdir(self.path)
        chapters.sort(key=lambda y: float(y.split()[-1]))
        for ch in chapters:
            pages = os.listdir(f"{self.path}/{ch}")
            lw = Image.open(f"{self.path}/{ch}/{pages[0]}").width
            for pg in pages[1:]:
                cw = Image.open(f"{self.path}/{ch}/{pg}").width
                if cw < lw:
                    lw = cw
            for pg in pages:
                cp = Image.open(f"{self.path}/{ch}/{pg}")
                if cp.width > (lw * 1.50):
                    crop_action(f"{self.path}/{ch}/{pg}")
                    cp.close()
                    os.remove(f"{self.path}/{ch}/{pg}")

    def make_pdf(self, volumes_path):
        limit = int(input("how many volumes : "))
        pdf_name = input("manga name : ")
        extension = input("extension name : ")
        volumes = os.listdir(volumes_path)
        count = int(input(f'starting {extension} : '))
        while volumes:
            pages = []
            fsize = Image.open(
                volumes_path + "/" + volumes[0] + "/" + os.listdir(volumes_path + "/" + volumes[0])[0] + "/" +
                [x for x in
                 os.listdir(volumes_path + "/" + volumes[0] + "/" + os.listdir(volumes_path + "/" + volumes[0])[0])][
                    0]).size
            for v in range(limit):
                try:
                    chapters = os.listdir(volumes_path + "/" + volumes[v])
                    chapters.sort(key=lambda y: float(y.split()[-1]))
                    for ch in chapters:
                        pages.extend(Image.open(y).convert('RGB') for y in
                                     [f'{volumes_path}/{volumes[v]}/{ch}/{x}' for x in
                                      os.listdir(f"{volumes_path}/{volumes[v]}/{ch}")])
                except IndexError:
                    pass
            pdf_dir = self.path + "/" + "pdfs"
            if not os.path.exists(self.path + "/" + "pdfs"):
                os.mkdir(pdf_dir)
            name = f"{pdf_name}_{extension}_{count}"
            pages = [x.transform(size=(fsize[0], fsize[1]),
                                 method=Image.EXTENT,
                                 data=(int(-(fsize[0] - x.width) / 2), int(-(fsize[1] - x.height) / 2),
                                       (x.width + int((fsize[0] - x.width) / 2)),
                                       x.height + int((fsize[1] - x.height) / 2)),
                                 fillcolor=(255, 255, 255)) for x in pages]
            pages[0].save(f"{pdf_dir}/{name}.pdf", save_all=True, append_images=pages[1:])
            count += 1
            pages.clear()
            for v in range(limit):
                try:
                    volumes.remove(volumes[v])
                except IndexError:
                    pass


while True:
    print('\x1B[3m'+"""
        App by Saad Ibne Sohael
    """+'\x1B[0m')
    path = input("path of manga : ").replace("\\", "/")
    if path == 'q':
        exit()
    manga = Manga(path)
    print("""
        Type c to Crop
        Type p to make pdf
        Type q to Quit
    """)
    cmd = input(">> ")

    if manga == 'q' or cmd == 'q':
        exit()

    if cmd == "c":
        manga.crop()
        print("\nCrop Done")
    elif cmd == "p":
        manga.make_pdf(input("path of folder containing volumes : ").replace("\\", "/"))
        print("\nPdf Done")
    else:
        print("\nplease type correctly!")