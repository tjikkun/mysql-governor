#!/bin/bash

mysqlTypeFileSet="/usr/share/lve/dbgovernor/mysql.type"

function checkFile(){
	if [ ! -e "$1" ]; then
		echo "Installtion error file ---$1---- does not exists"
		exit 1
	fi
}

function installDb(){
	SQL_VERSION=$1
	
	CL=`echo -n "cl5"`
	CL6=`uname -a | grep "\.el6\."`
	if [ -n "$CL6" ]; then
	    CL=`echo -n "cl6"`
	    if [ -e /etc/my.cnf ]; then
        	sed '/userstat/d' -i /etc/my.cnf
	        sed '/userstat_running/d' -i /etc/my.cnf
	    fi
	fi
    yum clean all
	if [ "$SQL_VERSION" == "auto" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/mysql-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	   mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
	  yum install mysql mysql-server mysql-libs mysql-devel mysql-bench  --nogpgcheck -y
	fi
	if [ "$SQL_VERSION" == "mysql50" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mysql-5.0-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	    mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
	  yum install cl-MySQL-meta cl-MySQL-meta-client cl-MySQL-meta-devel --nogpgcheck -y
	  ln -sf /etc/init.d/mysql /etc/init.d/mysqld
	fi
	if [ "$SQL_VERSION" == "mysql51" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mysql-5.1-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	   mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
	  yum install cl-MySQL-meta cl-MySQL-meta-client cl-MySQL-meta-devel --nogpgcheck -y
	  ln -sf /etc/init.d/mysql /etc/init.d/mysqld
	fi
	if [ "$SQL_VERSION" == "mysql55" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mysql-5.5-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	   mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
	  yum install cl-MySQL-meta cl-MySQL-meta-client cl-MySQL-meta-devel libaio --nogpgcheck -y
	  ln -sf /etc/init.d/mysql /etc/init.d/mysqld
	fi
	if [ "$SQL_VERSION" == "mysql56" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mysql-5.6-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	   mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
	  yum install cl-MySQL-meta cl-MySQL-meta-client cl-MySQL-meta-devel libaio --nogpgcheck -y
	  ln -sf /etc/init.d/mysql /etc/init.d/mysqld
	fi
	if [ "$SQL_VERSION" == "mariadb55" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mariadb-5.5-common.repo
	  yum install cl-MariaDB-meta cl-MariaDB-meta-client cl-MariaDB-meta-devel libaio --nogpgcheck -y
	fi

	if [ ! -e /etc/my.cnf.bkp ]; then
	    cp -f /etc/my.cnf /etc/my.cnf.bkp
	fi
	sed /userstat/d -i /etc/my.cnf
	/sbin/service mysqld restart
	echo "Giving mysqld a few seconds to start up...";
	sleep 5;

	IS_GOVERNOR=`rpm -qa governor-mysql`
	if [ -n "$IS_GOVERNOR" ]; then
		/sbin/service db_governor restart
		echo "DB-Governor installed/updated...";
	fi

	echo "Installation mysql for db_governor completed"
}

function installDbTest(){
	SQL_VERSION=$1
	
	CL=`echo -n "cl5"`
	CL6=`uname -a | grep "\.el6\."`
	if [ -n "$CL6" ]; then
	    CL=`echo -n "cl6"`
	    if [ -e /etc/my.cnf ]; then
        	sed '/userstat/d' -i /etc/my.cnf
	        sed '/userstat_running/d' -i /etc/my.cnf
	    fi
	fi
    yum clean all
	if [ "$SQL_VERSION" == "auto" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/mysql-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	   mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
	  yum install mysql mysql-server mysql-libs mysql-devel mysql-bench  --nogpgcheck -y --enablerepo=cloudlinux-updates-testing
	fi
	if [ "$SQL_VERSION" == "mysql50" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mysql-5.0-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	    mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
	  yum install cl-MySQL-meta cl-MySQL-meta-client cl-MySQL-meta-devel --nogpgcheck -y --enablerepo=cloudlinux-updates-testing
	  ln -sf /etc/init.d/mysql /etc/init.d/mysqld
	fi
	if [ "$SQL_VERSION" == "mysql51" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mysql-5.1-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	   mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
	  yum install cl-MySQL-meta cl-MySQL-meta-client cl-MySQL-meta-devel --nogpgcheck -y --enablerepo=cloudlinux-updates-testing
	  ln -sf /etc/init.d/mysql /etc/init.d/mysqld
	fi
	if [ "$SQL_VERSION" == "mysql55" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mysql-5.5-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	   mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
	  yum install cl-MySQL-meta cl-MySQL-meta-client cl-MySQL-meta-devel libaio --nogpgcheck -y --enablerepo=cloudlinux-updates-testing
	  ln -sf /etc/init.d/mysql /etc/init.d/mysqld
	fi
	if [ "$SQL_VERSION" == "mysql56" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mysql-5.6-common.repo
	  if [ -e /usr/libexec/mysqld ]; then
	   mv -f /usr/libexec/mysqld /usr/libexec/mysqld.bak
          fi
      yum install cl-MySQL-meta cl-MySQL-meta-client cl-MySQL-meta-devel libaio --nogpgcheck -y --enablerepo=cloudlinux-updates-testing
	  ln -sf /etc/init.d/mysql /etc/init.d/mysqld
	fi
	if [ "$SQL_VERSION" == "mariadb55" ]; then
	  wget -O /etc/yum.repos.d/cl-mysql.repo  http://repo.cloudlinux.com/other/$CL/mysqlmeta/cl-mariadb-5.5-common.repo
	  yum install cl-MariaDB-meta cl-MariaDB-meta-client cl-MariaDB-meta-devel libaio --nogpgcheck -y --enablerepo=cloudlinux-updates-testing
	fi

	if [ ! -e /etc/my.cnf.bkp ]; then
	    cp -f /etc/my.cnf /etc/my.cnf.bkp
	fi
	sed /userstat/d -i /etc/my.cnf
	/sbin/service mysqld restart
	echo "Giving mysqld a few seconds to start up...";
	sleep 5;

	IS_GOVERNOR=`rpm -qa governor-mysql`
	if [ -n "$IS_GOVERNOR" ]; then
		/sbin/service db_governor restart
		echo "DB-Governor installed/updated...";
	fi

	echo "Installation mysql for db_governor completed"
}
