import datetime
print('1111111')
with open('m.txt','a+') as f:
    f.write(str(datetime.datetime.now()) + '\\n')
f.close()
