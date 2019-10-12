import errno, os, winreg, logging
LOG_FILENAME = 'BonjourUninstall.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()

if proc_arch == 'x86' and not proc_arch64:
    arch_keys = {0}
elif proc_arch == 'x86' or proc_arch == 'amd64':
    arch_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
else:
    raise Exception("Unhandled arch: %s" % proc_arch)

flag=1

for arch_key in arch_keys:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | arch_key)
    for i in range(0, winreg.QueryInfoKey(key)[0]):
        skey_name = winreg.EnumKey(key, i)
        skey = winreg.OpenKey(key, skey_name)
        try:
            temp = winreg.QueryValueEx(skey, 'DisplayName')[0]
            if temp=="Bonjour":
                #print(winreg.QueryValueEx(skey, 'DisplayName')[0])
                logging.debug(winreg.QueryValueEx(skey, 'DisplayName')[0])
                #print("uninstall str : ",winreg.QueryValueEx(skey, 'UninstallString')[0])
                logging.debug("uninstall str : %s",winreg.QueryValueEx(skey, 'UninstallString')[0])
                x=os.system(winreg.QueryValueEx(skey, 'UninstallString')[0])
                flag=x
        except OSError as e:
            if e.errno == errno.ENOENT:
                # DisplayName doesn't exist in this skey
                pass
        finally:
            skey.Close()

if flag==0:
    logging.debug("Bonjour Found and Uninstalled successfully")
    #print("Bonjour Found and Uninstalled successfully")
elif flag==1602:
    logging.debug("Bonjour found and User cancelled uninstallation")
    #print("Bonjour and User Cancelled Installation")
else:
    logging.debug("Bonjour Not found")
    #print("Bonjour Not found")
