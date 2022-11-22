from os import path
from glob import glob
import os , shutil, wx, pdfplumber, re,openpyxl, glob
result = ''
declaration = 'ERROR: Problem getting the \"declaration\"'
awb = 'ERROR: Problem getting the \"AWB\"'
kg = 'ERROR: Problem getting the \"gross weight in kg\"'

app = wx.App()

dialog = wx.DirDialog(None, 'Choose a folder')
if dialog.ShowModal() == wx.ID_OK:
    folder = dialog.GetPath()

    files = glob.glob(folder + '\\*.pdf')
    for file in files:
        position = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                # declaration:
                size8 = page.filter(
                    lambda obj: obj['object_type'] == 'char' and '8.0' in str(obj['size'])).extract_text()
                pos = size8.find('22LV')
                declaration = size8[pos:pos + 18]
                awb = ''
                # AWB:
                text = re.split(r'[ \n]', page.extract_text())
                for code in text:
                    if len(code) == 10:
                        try:
                            awb = int(code)
                            break
                        except ValueError:
                            continue

                # gross weight in kg
                for number in text:
                    if re.match(r'^[0-9]+\.[0-9]{3}$', number):
                        kg = number
                        break
                if not position:
                    text_layout_lines = page.get_text_layout().to_string().split('\n')
                    i = 0
                    for line in text_layout_lines:
                        if line.find('Iepakojumu kopskaits (6)') != -1:
                            position = list(filter(None, text_layout_lines[i+1].split(' ')))[1]
                        elif line.find('Pozīcijas (5)') != -1:
                            position = list(filter(None, text_layout_lines[i+2].split(' ')))[0]
                        elif line.find('6. Iepakojumu kopskaits') != -1:
                            position = list(filter(None, text_layout_lines[i+1].split(' ')))[0]
                        else:
                            i += 1
                            continue
                        break
        try:
            if len(str(awb)) == 10 and len(str(declaration)) == 18 and re.match(r'^[0-9]+\.[0-9]{3}$', kg) and isinstance(int(position), int):
                result +=str(awb) +"\n"+str(declaration)+ "\t" + str(kg) +"\t" + str(position)+ "\n" 
                i = file.rindex("\\")
                shutil.move(file,file[0:i+1]+"Done"+file[i:])
                with open(folder + '\\results.txt', 'w') as f:
                    f.write(result)
        except ValueError:
            None