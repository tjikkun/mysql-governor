#!/usr/bin/python                                                                                                                                            
                                                                                                                                                             
import os                                                                                                                                                    
import pprint 
import sys
import getopt
import shutil
import stat
import glob
import grp
import pwd
import yum
import time
import math

import lve_diagnostic
from lve_diagnostic import *
import copy_directory
from copy_directory import *
import exec_command
from exec_command import *
import mysql_lib
from mysql_lib import *
from pwd import getpwnam  
from grp import getgrnam  
from distutils import version
from distutils.version import StrictVersion

SOURCE="/usr/share/lve/dbgovernor/"

def get_cl_num():
    result = exec_command("rpm -q --qf \"%{version}\n\" `rpm -q --whatprovides /etc/redhat-release`")
    return result[0]

def recursive_file_permissions(path,uid=-1,gid=-1):
	for item in glob.glob(path+'/*'):
		if os.path.isdir(item):
			recursive_file_permissions(os.path.join(path,item),uid,gid)
		else:
			try:
				os.chown(os.path.join(path,item),uid,gid)
			except:
				print('File permissions on {0} not updated due to error.')


def touch(fname):
	try:
		os.utime(fname, None)
	except:
		open(fname, 'a').close()


def getItem(txt1, txt2, op):
	try:
    		i1 = int(txt1)
	except ValueError:
    		i1 = -1
	try:
    		i2 = int(txt2)
	except ValueError:
    		i2 = -1
	if i1 == -1 or i2 == -1:
		if op == 0:
			return txt1>txt2
		else:
			return txt1<txt2
	else:
		if op == 0:
			return i1>i2
		else:
			return i1<i2

	
#Compare version of types xx.xx.xxx... and yyy.yy.yy.y..
#if xxx and yyy is numbers, than comapre as numbers
#else - comapre as strings
def verCompare (base, test):
	base = base.split(".")
	test = test.split(".")
	if(len(base)>len(test)):
		ln = len(test)
	else:
		ln = len(base)
	for i in range(ln):
		if getItem(base[i],test[i],0):
			return 1
		if getItem(base[i],test[i],1):
			return -1
	if len(base)==len(test):	
		return 0
	elif len(base)>len(test):
		return 1
	else:
		return 0

def installPythonMysql():
	if cp.name == "Plesk" and verCompare (cp.version, "10") >= 0:
		print "No need in MySQL-python"
	elif cp.name == "cPanel":
		print "No need in MySQL-python"
	elif cp.name == "InterWorx":
		print "No need in MySQL-python"
	elif cp.name == "ISPManager":	
		print "No need in MySQL-python"
	elif cp.name == "DirectAdmin":
		yb = yum.YumBase()
                if yb.rpmdb.searchNevra(name="MySQL-python"):
                    print "MySQL-python already installed"
                else:
	            exec_command("yum install -y MySQL-python --disableexcludes=all")        
	else:
		print "Current panel unsupported. Panel name: "+cp.name+" version: "+cp.version


def usage():
	print ''                                                                                                                                             
        print 'Use following syntax to manage DBGOVERNOR istall utility:'                                                                                                       
        print sys.argv[0]+" [OPTIONS]"                                                                                                                       
        print 'Options:'                                                                                                                                     
        print " -i | --install             : install MySQL for db-governor"                                                                 
        print " -d | --delete              : delete MySQL for db-governor"                                                                  
	print "    | --install-beta        : install MySQL beta for governor or update beta if exists newer beta version  "
	print " -c | --clean-mysql         : clean MySQL packages list (after governor installation)"
	print " -m | --clean-mysql-delete  : clean cl-MySQL packages list (after governor deletion)"
	print " -u | --upgrade             : install MySQL with mysql_upgrade_command"
        print " -t | --dbupdate            : update UserMap file"

def check_leave_pid():
	if cp.name == "Plesk" and verCompare (cp.version, "10") >= 0:
		if os.path.exists(SOURCE+"utils/check_mysql_leave_pid_other.sh"):
            	    exec_command(SOURCE+"utils/check_mysql_leave_pid_other.sh")
	elif cp.name == "cPanel":
		if os.path.exists(SOURCE+"cpanel/check_mysql_leave_pid.sh"):
            	    exec_command(SOURCE+"cpanel/check_mysql_leave_pid.sh")
	elif cp.name == "InterWorx":
		if os.path.exists(SOURCE+"utils/check_mysql_leave_pid_other.sh"):
            	    exec_command(SOURCE+"utils/check_mysql_leave_pid_other.sh")
	elif cp.name == "ISPManager":	
		if os.path.exists(SOURCE+"utils/check_mysql_leave_pid_other.sh"):
            	    exec_command(SOURCE+"utils/check_mysql_leave_pid_other.sh")
	elif cp.name == "DirectAdmin":
		if os.path.exists(SOURCE+"utils/check_mysql_leave_pid_other.sh"):
            	    exec_command(SOURCE+"utils/check_mysql_leave_pid_other.sh")
	else:
		if os.path.exists(SOURCE+"utils/check_mysql_leave_pid_other.sh"):
            	    exec_command(SOURCE+"utils/check_mysql_leave_pid_other.sh")

def install_mysql():
	if cp.name == "Plesk" and verCompare (cp.version, "10") >= 0:
		exec_command_out(SOURCE+"plesk/install-db-governor.sh --install")
	elif cp.name == "cPanel":
		# install hook for CPanel to patch Apache's suexec and suphp
		exec_command_out(SOURCE+"cpanel/db_governor-clear-old-hook")
		exec_command_out(SOURCE+"cpanel/install-db-governor --force")		
	elif cp.name == "InterWorx":
		exec_command_out(SOURCE+"iworx/install-db-governor.sh --install")
	elif cp.name == "ISPManager":	
		exec_command_out(SOURCE+"ispmanager/install-db-governor.sh --install")
	elif cp.name == "DirectAdmin":
		exec_command_out(SOURCE+"da/install-db-governor.sh --install")
	else:
		print "Current panel unsupported. Panel name: "+cp.name+" version: "+cp.version

def update_user_map_file():
	if cp.name == "Plesk" and verCompare (cp.version, "10") >= 0:
		exec_command(SOURCE+"utils/empty_action.sh")
	elif cp.name == "cPanel":
		exec_command(SOURCE+"utils/dbgovernor_map")
	elif cp.name == "InterWorx":
		exec_command(SOURCE+"utils/empty_action.sh")
	elif cp.name == "ISPManager":	
		exec_command(SOURCE+"utils/empty_action.sh")
	elif cp.name == "DirectAdmin":
		exec_command(SOURCE+"da/dbgovernor_map.py")
	else:
		exec_command(SOURCE+"utils/empty_action.sh")

def install_dbmap_update():
        update_user_map_file(); 

def install_db_user_mapfile_cron():
        if os.path.exists("/usr/share/lve/dbgovernor/utils/dbgovernor-usermap-cron"):
		shutil.copy2("/usr/share/lve/dbgovernor/utils/dbgovernor-usermap-cron", "/etc/cron.d/dbgovernor-usermap-cron")

def delete_db_user_mapfile_cron():
        if os.path.exists("/usr/share/lve/dbgovernor/utils/dbgovernor-usermap-cron"):
                os.remove("/usr/share/lve/dbgovernor/utils/dbgovernor-usermap-cron")

def install_mysql_beta():
        exec_command_out(SOURCE+"other/set_fs_suid_dumpable.sh")
	if cp.name == "Plesk" and verCompare (cp.version, "10") >= 0:
                check_leave_pid()
		exec_command_out(SOURCE+"plesk/install-db-governor.sh --install")
                install_db_user_mapfile_cron()
	elif cp.name == "cPanel":
		# install hook for CPanel to patch Apache's suexec and suphp
                check_leave_pid()
		exec_command_out(SOURCE+"cpanel/db_governor-clear-old-hook")
		exec_command_out(SOURCE+"cpanel/install-db-governor-stable")
		exec_command_out(SOURCE+"cpanel/install-mysql-disabler.sh")
		exec_command_out(SOURCE+"cpanel/cpanel-install-hooks")		
		exec_command_out(SOURCE+"cpanel/upgrade-mysql-disabler.sh")
		install_db_user_mapfile_cron()
	elif cp.name == "InterWorx":
                check_leave_pid()
		exec_command_out(SOURCE+"iworx/install-db-governor.sh --install")
                install_db_user_mapfile_cron()
	elif cp.name == "ISPManager":	
                check_leave_pid()
		exec_command_out(SOURCE+"ispmanager/install-db-governor.sh --install")
                install_db_user_mapfile_cron()
	elif cp.name == "DirectAdmin":
                check_leave_pid()
		exec_command_out(SOURCE+"da/install-db-governor.sh --install")
                install_db_user_mapfile_cron()
	else:
                check_leave_pid()
                exec_command_out(SOURCE+"other/install-db-governor.sh --install")
                install_db_user_mapfile_cron()

def install_mysql_beta_testing():
        exec_command_out(SOURCE+"other/set_fs_suid_dumpable.sh")
	if cp.name == "Plesk" and verCompare (cp.version, "10") >= 0:
                check_leave_pid()
		exec_command_out(SOURCE+"plesk/install-db-governor-beta.sh --install")
                install_db_user_mapfile_cron()
	elif cp.name == "cPanel":
		# install hook for CPanel to patch Apache's suexec and suphp
                check_leave_pid()
		exec_command_out(SOURCE+"cpanel/db_governor-clear-old-hook")
		exec_command_out(SOURCE+"cpanel/install-db-governor-beta")
                exec_command_out(SOURCE+"cpanel/install-mysql-disabler.sh")
                exec_command_out(SOURCE+"cpanel/cpanel-install-hooks")		
                exec_command_out(SOURCE+"cpanel/upgrade-mysql-disabler.sh")
                install_db_user_mapfile_cron()
	elif cp.name == "InterWorx":
                check_leave_pid()
		exec_command_out(SOURCE+"iworx/install-db-governor-beta.sh --install")
                install_db_user_mapfile_cron()
	elif cp.name == "ISPManager":	
                check_leave_pid()
		exec_command_out(SOURCE+"ispmanager/install-db-governor-beta.sh --install")
                install_db_user_mapfile_cron()
	elif cp.name == "DirectAdmin":
                check_leave_pid()
		exec_command_out(SOURCE+"da/install-db-governor-beta.sh --install")
                install_db_user_mapfile_cron()
	else:
                check_leave_pid()
                exec_command_out(SOURCE+"other/install-db-governor-beta.sh --install")
                install_db_user_mapfile_cron()


def delete_mysql():
	if cp.name == "Plesk" and verCompare (cp.version, "10") >= 0:		
                delete_db_user_mapfile_cron()
                exec_command_out(SOURCE+"plesk/install-db-governor.sh --delete")
	elif cp.name == "cPanel":
                delete_db_user_mapfile_cron()
                exec_command_out(SOURCE+"cpanel/cpanel-delete-hooks")
		if os.path.exists("/etc/mysqlupdisable"):
			os.remove("/etc/mysqlupdisable")
                if os.path.exists("/var/cpanel/rpm.versions.d/cloudlinux.versions"):
			os.remove("/var/cpanel/rpm.versions.d/cloudlinux.versions")
                if os.path.exists("/etc/cpupdate.conf.governor"):
                        if os.path.exists("/etc/cpupdate.conf"):
                                os.remove("/etc/cpupdate.conf")
                        os.rename("/etc/cpupdate.conf.governor", "/etc/cpupdate.conf")
                if version.LooseVersion(cp.version) < version.LooseVersion("11.36"):
		        exec_command_out("/scripts/mysqlup --force")
                else:
                        exec_command_out("/scripts/upcp --force")
                if os.path.exists("/scripts/check_cpanel_rpms"):
                        exec_command_out("/scripts/check_cpanel_rpms --fix --targets=MySQL50,MySQL51,MySQL55,MySQL56")
	elif cp.name == "InterWorx":		
                delete_db_user_mapfile_cron()
                exec_command_out(SOURCE+"iworx/install-db-governor.sh --delete")
	elif cp.name == "ISPManager":
                delete_db_user_mapfile_cron()
                exec_command_out(SOURCE+"ispmanager/install-db-governor.sh --delete")
	elif cp.name == "DirectAdmin":
                delete_db_user_mapfile_cron()
		exec_command_out(SOURCE+"da/install-db-governor.sh --delete")
	else:
                delete_db_user_mapfile_cron()
                exec_command_out(SOURCE+"other/install-db-governor.sh --delete")


def cp_supported():
	if cp.name == "Plesk" and verCompare (cp.version, "10") >= 0:		
		return True
	if cp.name in ("cPanel", "InterWorx", "ISPManager", "DirectAdmin"):
		return True
	return False

def remove_specific_package(pname, yb):
        #print "Looking for " + pname
	if yb.rpmdb.searchNevra(name=pname):
	    exec_command("rpm -e --justdb --nodeps " + pname)
	#else:
	    #print pname + " not installed"

def remove_sepcific_mysql(mname, yb):
        remove_specific_package(mname + "-server", yb)
        remove_specific_package(mname + "-shared", yb)
        remove_specific_package(mname + "-devel", yb)
        remove_specific_package(mname + "-bench", yb)
        remove_specific_package(mname + "-test", yb)
        remove_specific_package(mname + "-client", yb)
        remove_specific_package(mname + "-libs", yb)
        remove_specific_package(mname + "-compat", yb)
        remove_specific_package(mname + "", yb)

def remove_mysql_justdb():
        yb = yum.YumBase()
        remove_sepcific_mysql('cpanel-MySQL', yb)
        remove_sepcific_mysql('MySQL', yb)
        remove_sepcific_mysql('MySQL50', yb)
        remove_sepcific_mysql('MySQL51', yb)
        remove_sepcific_mysql('MySQL55', yb)
        remove_sepcific_mysql('MySQL56', yb)
        remove_sepcific_mysql('MariaDB', yb)
        remove_sepcific_mysql('mariadb', yb)
        print "Cleaning of MySQL packages completed"

def remove_mysql_justdb_cl():
        yb = yum.YumBase()
        remove_sepcific_mysql('cl-MySQL', yb)
        remove_sepcific_mysql('cl-mariadb', yb)
        remove_sepcific_mysql('mysql', yb)

        remove_sepcific_mysql('cl-MySQL-meta', yb)
        remove_sepcific_mysql('cl-MySQL-meta-client', yb)
        remove_sepcific_mysql('cl-MySQL-meta-devel', yb)
        remove_sepcific_mysql('cl-MariaDB-meta', yb)
        remove_sepcific_mysql('cl-MariaDB-meta-client', yb)
        remove_sepcific_mysql('cl-MariaDB-meta-devel', yb)
        remove_sepcific_mysql('cl-MySQL50', yb)
        remove_sepcific_mysql('cl-MySQL51', yb)
        remove_sepcific_mysql('cl-MySQL55', yb)
        remove_sepcific_mysql('cl-MySQL56', yb)
        remove_sepcific_mysql('cl-MariaDB55', yb)

        print "Cleaning of cl-MySQL packages completed"

def delete_governor_rpm():
    exec_command_out("rpm -e governor-mysql")
    
def newLveCtl(version1):
    return StrictVersion("1.4") <= StrictVersion(version1)
    


def numProc(s):
    try:
        return int(s)
    except ValueError:
        return 0
                        
                        

def set_bad_lve_container():
    if os.path.exists("/usr/sbin/lvectl"):
	clver = get_cl_num()
	result0 = exec_command("/usr/sbin/lvectl version | cut -d\"-\" -f1")
	if len(result0)>0 and newLveCtl(result0[0])==True:
	    result1 = exec_command("/usr/sbin/lvectl limits 3 | sed -n 2p | sed -e 's/\s\+/ /g' | cut -d' ' -f3")
	    result2 = exec_command("/usr/sbin/lvectl limits default | sed -n 2p | sed -e 's/\s\+/ /g' | cut -d' ' -f3")
	    if result1 == result2 or len(result1) == 0:
		result3 = exec_command("cat /proc/cpuinfo | grep processor | wc -l")
		cpu_lim=800
		if(len(result3)>0):
		    cpu_lim = numProc(result3[0]) * 100
		exec_command_out("/usr/sbin/lvectl set 3 --speed=" + str(int(math.ceil(float(cpu_lim)/4))) + "% --io=1024 --nproc=0 --pmem=0 --mem=0 --vmem=0 --maxEntryProcs=0 --save-all-parameters")
	else:
	    result = exec_command("/usr/sbin/lvectl limits 3")
	    if len(result)==1:
		if clver=="5":
		    exec_command_out("/usr/sbin/lvectl set 3 --cpu=25 --ncpu=1 --io=1024 --mem=0 --vmem=0 --maxEntryProcs=0 --save-all-parameters")
		else:
    		    exec_command_out("/usr/sbin/lvectl set 3 --cpu=25 --ncpu=1 --io=1024 --nproc=0 --pmem=0 --mem=0 --vmem=0 --maxEntryProcs=0 --save-all-parameters")  
    		return
	    result1 = exec_command("/usr/sbin/lvectl limits 3 | sed -n 2p | sed -e 's/\s\+/ /g' | cut -d' ' -f3")
	    result2 = exec_command("/usr/sbin/lvectl limits default | sed -n 2p | sed -e 's/\s\+/ /g' | cut -d' ' -f3")
	    if result1 == result2:
		if clver=="5":
		    exec_command_out("/usr/sbin/lvectl set 3 --cpu=25 --ncpu=1 --io=1024 --mem=0 --vmem=0 --maxEntryProcs=0 --save-all-parameters")
		else:
    		    exec_command_out("/usr/sbin/lvectl set 3 --cpu=25 --ncpu=1 --io=1024 --nproc=0 --pmem=0 --mem=0 --vmem=0 --maxEntryProcs=0 --save-all-parameters")

def remove_repo_file():
        if os.path.exists("/etc/yum.repos.d/cl-mysql.repo"):
                os.remove("/etc/yum.repos.d/cl-mysql.repo") 

def remove_mysqlclients():
	if os.path.exists("/usr/share/lve/dbgovernor/remove-mysqlclient"):
	    exec_command_out("/usr/share/lve/dbgovernor/remove-mysqlclient")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def warn_message():
        print bcolors.WARNING + "!!!Before making any changing with database make sure that you have reserve copy of users data!!!"+ bcolors.ENDC
        print bcolors.FAIL + "!!!!!!!!!!!!!!!!!!!!!!!!!!Ctrl+C for cancellation of installation!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"+ bcolors.ENDC
        print bcolors.OKGREEN + "Instruction: how to create whole database backup - " + bcolors.OKBLUE +"http://docs.cloudlinux.com/index.html?backing_up_mysql.html"+ bcolors.ENDC
        time.sleep(10)

def fix_libmygcc():
	if os.path.exists("/usr/lib64/mysql/libmygcc.a"):
		os.rename("/usr/lib64/mysql/libmygcc.a", "/usr/lib64/mysql/libmygcc.a.bak")
	if os.path.exists("/usr/lib/mysql/libmygcc.a"):
		os.rename("/usr/lib/mysql/libmygcc.a", "/usr/lib/mysql/libmygcc.a.bak")
		

cp = get_cp()
try:
	opts, args = getopt.getopt(sys.argv[1:], "hidcmut", ["help", "install", "delete", "install-beta", "clean-mysql", "clean-mysql-delete", "upgrade", "dbupdate", "update-mysql-beta"])
except getopt.GetoptError, err:
	# print help information and exit:
	print str(err) # will print something like "option -a not recognized"
	usage()
	sys.exit(2)
	                                                          
for o, a in opts:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-i", "--install"):
                warn_message()
                remove_mysqlclients()
            	remove_mysql_justdb()
                remove_mysql_justdb_cl()
		install_mysql_beta()
                set_bad_lve_container()
                if os.path.exists("/usr/share/lve/dbgovernor/chk-mysqlclient"):
		    exec_command_out("/usr/share/lve/dbgovernor/chk-mysqlclient")
                installPythonMysql()
                install_dbmap_update()
		fix_libmygcc()
	elif o in ("-u", "--upgrade"):
                warn_message()
		remove_mysqlclients()
		remove_mysql_justdb_cl()
		install_mysql_beta()
		remove_mysql_justdb()
                set_bad_lve_container()
		if os.path.exists("/usr/bin/mysql_upgrade"):
		    exec_command_out("/usr/bin/mysql_upgrade")
		if os.path.exists("/usr/share/lve/dbgovernor/chk-mysqlclient"):
		    exec_command_out("/usr/share/lve/dbgovernor/chk-mysqlclient")
                if os.path.exists("/usr/bin/alt-php-mysql-reconfigure"):                                                                                                                                                                     
                    exec_command_out("/usr/bin/alt-php-mysql-reconfigure") 
                install_dbmap_update()
		fix_libmygcc()
	elif o in ("-d", "--delete"):
                remove_repo_file()
		remove_mysql_justdb_cl()
                delete_mysql()
                delete_governor_rpm()
	elif o in ("--install-beta",):
    		warn_message()
                remove_mysqlclients()
                remove_mysql_justdb_cl()
                remove_mysql_justdb()
		install_mysql_beta_testing()
                set_bad_lve_container()
                if os.path.exists("/usr/share/lve/dbgovernor/chk-mysqlclient"):
		    exec_command_out("/usr/share/lve/dbgovernor/chk-mysqlclient")
                installPythonMysql()
                install_dbmap_update()
		fix_libmygcc()
	elif o in ("--update-mysql-beta",):
		print "Option is deprecated. Use --install-beta instead"
	elif o in ("c", "--clean-mysql"):
                remove_mysql_justdb()
	elif o in ("m", "--clean-mysql-delete"):
		remove_mysql_justdb_cl()
        elif o in ("t", "--dbupdate"):
		update_user_map_file()
	else:
		usage()
		sys.exit(2)
