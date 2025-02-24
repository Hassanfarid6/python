
# Conditional Statement

marks = int(input('marks : '))

if(marks >= 101 ):
    print("Does not exsist")
if(marks >= 90 and marks < 101):
    print("A+ Grade!!")
elif(marks >= 80 and marks < 90):
    print("A1 Grade!!")
elif(marks >= 70 and marks < 80):
    print("A Grade!!")
elif(marks >= 60 and marks < 70):
    print("B Grade!!")
elif(marks >= 50 and marks < 60):
    print("C Grade!!")
elif(marks >= 40 and marks < 50):
    print("D Grade!!")
else:
    print("Fail")