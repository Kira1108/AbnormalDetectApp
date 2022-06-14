from datetime import datetime
import hashlib

  
def md5_id():
    str2hash = str(datetime.now().timestamp())
    return hashlib.md5(str2hash.encode()).hexdigest()



