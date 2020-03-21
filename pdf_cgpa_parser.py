from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import math
from statistics import mode


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def getLongestIncSubArrIndex( arr, n) : 
    m = 1
    l = 1
    maxIndex = 0
    for i in range(1, n) : 
        if (arr[i] > arr[i-1]) : 
            l =l + 1
        else : 
            if (m < l)  : 
                m = l    
                maxIndex = i - m 
            l = 1    
    if (m < l) : 
        m = l 
        maxIndex = n - m   
    return maxIndex,m+maxIndex

path = input('Enter your file path: ')
path = path.replace('\\' ,"\\\\")
all_text = convert_pdf_to_txt(path)

# print(all_text)

all_text = all_text.split("\n")
allowed_grade = [chr(i) for i in range(65,65+26)]
allowed_grade.extend([chr(i)+'+' for i in range(65,65+26)])
allowed_grade.append('Ab')

allowed_number=[]
allowed_number.extend([str(i) for i in range(1,21)])


one_or_two =[]

for i in all_text:
    if len(i) <= 2 and ((i in allowed_grade) or (i in allowed_number) ):
        one_or_two.append(i)

# print(one_or_two)

grade=[]
for i in range(len(one_or_two)):
    if one_or_two[i] in allowed_grade:
        grade.append(one_or_two[i])

for i in grade:
    one_or_two.remove(i)

one_or_two = list(map(int,one_or_two)) 
allowed_number = list(map(int,allowed_number)) 

# print(allowed_number)
# print(one_or_two)
# print(grade)

sno_left,sno_right=getLongestIncSubArrIndex(one_or_two,len(one_or_two))
sno = []
for i in range(sno_left,sno_right):
    sno.append(one_or_two[i])

temp=0
for i in range(sno_left,sno_right):
    one_or_two.pop(i-temp)
    temp+=1
# print(one_or_two)
# print(sno)

A=one_or_two[:len(one_or_two)//2]
B=one_or_two[len(one_or_two)//2:]

# print(A.count(mode(A)))
# print(B.count(mode(B)))

try:
    if A.count(mode(A)) > B.count(mode(B)):
        semester=A
        credits=B       
    else:
        semester=B
        credits=A
except:
    try:
        A.count(mode(A))
        semester=A
        credits=B
    except:
        semester=B
        credits=A

print('Semester:',end=' ')
print(semester)

print('Credits:',end=' ')
print(credits)

print('Grades:',end=' ')
print(grade)

total_credits = sum(credits)
# print (total_credits)

grade_to_gradepoint = {
    'O':10,   
    'A+':9,
    'A':8,
    'B+':7,
    'B':6,
    'C':5,
    'P':4,
    'F':0,
    'Ab':0,
    'I':0
}

gradepoint = list(map(lambda x:grade_to_gradepoint[x],grade))
print('Grade Points:',end=' ')
print(gradepoint)

print('Total Credits:',end=' ')
print(total_credits)

final_pair = zip(credits,gradepoint)
sgpa = 0
for i,j in final_pair:
    sgpa += i*j
sgpa /= total_credits
sgpa = '{0:.2f}'.format(sgpa) 
print('SGPA:',end=' ')
print(sgpa)

