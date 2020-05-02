import re
from pprint import pprint
import csv

with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# print(str(contacts_list))

pattern_fls = r"'(\b[УМНЛП]\w{1,}\b)\s?'?,?\s?'?(\b[ОВАИ]\w{1,})\s?'?,?\s?'?(\b[ВГРА]\w{1,})?"
match = re.findall(pattern_fls, str(contacts_list))
#print(match)

pattern_org = r'ФНС|Минфин'
matc = re.findall(pattern_org, str(contacts_list))
#print(matc)

pos_list = []
for line in contacts_list:
    pattern_pos = r"\b\w{7,}\s\w{6,}\s–?\s?\w{7,}\s\w{6,}\s\w{10,}\s\w{1,}\s\w{10,}(\s\w{8,}\s\w{6,}\s\w{1,}\s\w{1,}\s\w{1,}\s\w{1,}\s\w{1,}\s\w{1,}\s\w{1,})?"
    mat = re.search(pattern_pos, str(line))
    pos_list.append(mat)

num_list = []
pattern_num = r"(\+7|8)\s?\(?\d{3}\)?\s?\-?\d{3}\-?\d{2}\-?\d{2}(\s*\(?доб.\s*\d{4}\)?)?"
for line in contacts_list:
    mat = re.search(pattern_num, str(line))
    try:
        pattern = re.compile("(\+7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\-?(\d{2})\-?(\d{2})(\s*\(?(доб.\s*\d{4})\)?)?")
        sub_pattern = r"+7(\2)\3-\4-\5\7"
        nums_cor = pattern.sub(sub_pattern, mat.group())
        num_list.append(nums_cor)
    except AttributeError:
        num_list.append('')
# print(num_list)

email_list = []
for line in contacts_list:
    pattern = r"\w{1,}.?\w{1,}?@\w{1,}.ru"
    m = re.search(pattern, str(line))
    try:
        email_list.append(m.group())
    except AttributeError:
        email_list.append('')
# print(email_list)

first = contacts_list.pop(0)
new_list = []
new_list.append(first)
#print(new_list)

for i in range(0, 8):
    fls = list(match[i])
    try:
        org = matc[i]
        fls.append(org)
    except IndexError:
        fls.append('')
    try:
        pos = pos_list[i]
        fls.append(pos.group())
    except AttributeError:
        fls.append('')
    fls.append(num_list[i])
    fls.append(email_list[i])
    new_list.append(fls)

#print(new_list)

for i in range(0, 9):
    try:
        if new_list[i][0] == new_list[i + 1][0]:
            a, b = new_list[i], new_list[i + 1]
            new_list.pop(new_list.index(a))
            new_list.pop(new_list.index(b))
            new_line = []
            for i in zip(a, b):
                if i[0] == i[1]:
                    new_line.append(i[0])
                elif i[0] == '':
                    new_line.append(i[1])
                elif i[1] == '':
                    new_line.append(i[0])
            new_list.append(new_line)

        elif new_list[i][0] == new_list[i + 2][0]:
            a, b = new_list[i], new_list[i + 2]
            new_list.pop(new_list.index(a))
            new_list.pop(new_list.index(b))
            new_line = []
            for i in zip(a, b):
                if i[0] == i[1]:
                    new_line.append(i[0])
                elif i[0] == '':
                    new_line.append(i[1])
                elif i[1] == '':
                    new_line.append(i[0])
            new_list.append(new_line)

    except IndexError:
        pass

with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_list)