import codecs
import csv
from decimal import Decimal
import wx

app = wx.App()

filename = wx.FileSelector('Choose a CSV file', wildcard='*.csv')

if filename.endswith('.csv'):
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        results = []
        for row in csvreader:
            if row[0] == 'A':
                new = True
                for result in results:
                    if result[0] == row[33]:
                        pieces = row[10].replace(' ', '').split('\\')
                        result[1] = result[1] + int(pieces[0])
                        result[2] = result[2] + int(pieces[1])
                        result[3] = result[3] + Decimal(row[11])

                        new = False
                        break
                if new:
                    pieces = row[10].replace(' ', '').split('\\')
                    result = [row[33], int(pieces[0]), int(pieces[1]), Decimal(row[11])]
                    results.append(result)
        results.sort()
        with codecs.open(filename[0:-4] + '.txt', 'w', 'utf-8') as f:
            f.write('Valsts \t(Cik vietas iziet) \\ (Cik vietas kopā)\t\tkg\n\n')
            for result in results:
                f.write(result[0] + '\t' + str(result[1]) + ' \\ ' + str(result[2]) + '\t\t\t' + str(result[3]) + '\n')

app.MainLoop()
 
