f = open("C:\\Users\\Meller\\Desktop\\petition_out.xml", "r", -1, "utf-8")
xml = f.read()
f.close()

xml = xml.replace("?ФИО", "Рублев Александр Александрович")
xml = xml.replace("?СЕРИЯ", "4513")
xml = xml.replace("?НОМЕР", "206684")
xml = xml.replace("?ВЫДАН", "Отдел УФМС России по гор Москве в ЗАО")
xml = xml.replace("?ДАТАВЫД", "21.10.2013")
xml = xml.replace("?ДАТАЗАЯВ", "16.03.2017")
xml = xml.replace("?ДАТАУВОЛЬН", "18.03.2017")

f = open('%s/%s' % ("C:\\Users\\Meller\\Desktop", "123.doc"), "w", -1, "utf-8")
f.write(xml)
f.close()