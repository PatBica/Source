import shutil
import os
import wx
import glob
import pdfplumber
import re

result = ''

app = wx.App()

dialog = wx.DirDialog(None, 'Choose a folder')
if dialog.ShowModal() == wx.ID_OK:
    folder = dialog.GetPath()

    files = glob.glob(folder + '\\*.pdf')

    if not os.path.exists(folder+'\\DONE\\'):
        print(folder+'\\DONE\\')
        os.makedirs(folder+'\\DONE\\')

    for file in files:
        with pdfplumber.open(file) as pdf:
            awb = None
            decl = None
            kg = None
            pcs = None

            for page in pdf.pages:
                text = page.get_text_layout().to_string()

                if not awb:
                    awb = re.search(pattern=r'\s[0-9]{10}\s', string=text)
                    if awb:
                        awb = awb.group().strip()

                if not decl:
                    decl = re.search(pattern=r'\s22LV[0-9]{14}\s', string=text)
                    if decl:
                        decl = decl.group().strip()

                if not kg:
                    kg = re.search(pattern=r'\s[0-9]+\.[0-9]{3}\s', string=text)
                    if kg:
                        kg = kg.group().strip()

                if not pcs:
                    i = 0
                    text = text.split('\n')
                    for line in text:
                        if line.find('Iepakojumu kopskaits (6)') != -1 or line.find('6. Iepakojumu kopskaits') != -1:
                            line = list(filter(None, text[i+1].split(' ')))
                            if len(line) == 5 or len(line) == 3:
                                pcs = line[1]
                                break
                        else:
                            i += 1

        if awb and decl and kg and pcs:
            # print(awb, decl, kg, pcs)
            try:
                if len(awb) == 10 and len(decl) == 18 and re.match(r'^[0-9]+.[0-9]{3}$', kg) and isinstance(int(pcs), int):
                    result += str(awb) + "\n" + str(decl) + "\t" + str(kg).replace('.', ',') + "\t" + str(pcs) + "\n"
                    i = file.rindex("\\")
                    shutil.move(file, file[0:i + 1] + "DONE" + file[i:])
            except ValueError:
                continue

    with open(folder + r'\results.txt', 'w') as f:
        f.write(result)