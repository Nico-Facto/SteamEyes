import os 
class secureLog():
    try :
        sqlLogUser= os.environ['sqlLogUser']
        sqlLogPass= os.environ['sqlLogPass']
        sqlLogHost= os.environ['sqlLogHost']
        sqlLogDatabase= os.environ['sqlLogDatabase']
        sqlLogPort='3306'
        print("Cloud Sec Env loaded")
    except:
        from lib.sec_local import secureLog_local
        sqlLogUser, sqlLogPass, sqlLogHost, sqlLogDatabase, sqlLogPort = secureLog_local().get_var_env() 
        print("Local Sec Env loaded")
