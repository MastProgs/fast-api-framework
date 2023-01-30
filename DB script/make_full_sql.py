

import os
import datetime

dbname = 'derby_web'
remove_file = [".py", ".sql", ".exe", ".bat", ".spec", "dist", "build"]

folder_list = os.listdir(path="./")
folder_set = set()
for fname in folder_list:
    is_except = False
    for exc in remove_file:
        if exc in fname:
            is_except = True
    
    if is_except:
        pass
    else:
        folder_set.add(fname)
                        

#dt = datetime.datetime.utcnow()
#dtStr = datetime.datetime.strftime(dt, "%Y-%m-%d")

with open("create_all.sql", 'w') as f:
    
    fileCodeList: list[str] = list()
    frontCode = f'''

CREATE DATABASE IF NOT EXISTS `{dbname}`;
USE `{dbname}`;
    
'''

    ENTER = '''
    
'''

    fileCodeList.append(frontCode)
    
    for folder in folder_set:
        with open(folder + "/create.sql", 'r') as fsql:
            fileCodeList.append(ENTER)
            fileCodeList += fsql.readlines()            
            fileCodeList.append(ENTER)
            pass
    
    f.write("".join(fileCodeList))
    
    pass