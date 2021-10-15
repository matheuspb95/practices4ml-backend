import re
from fastapi import HTTPException


regex = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "name": r'[A-Za-z]{2,25}( [A-Za-z]{2,25})?',
    "password": r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%.*#?&])[A-Za-z\d@$!#%.*?&]{6,20}$'
}

def check(regex, value):
    if(re.fullmatch(regex, value)):
        return True
    else:
        return False

def check_obj(obj):
    for key in obj.dict().keys():
        if(not check(regex[key], obj.dict()[key])):
            raise HTTPException(
                status_code=400, detail="{key} invalid".format(key=key))

