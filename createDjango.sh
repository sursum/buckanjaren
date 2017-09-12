#! /bin/bash
REALPATH=`realpath $0`
SCRIPT_DIRNAME=`dirname ${REALPATH}`
PROJNAME=$1
echo "SCRIPT_DIRNAME: "$SCRIPT_DIRNAME
echo "PROJNAME: "$PROJNAME
PROJDIR=$2    # Empty means / (root)
PROJ_ENV_PATH=
DATABASE=$PROJNAME
POSTGRES_VERSION=
POSTGRES_CONF_FILE=/etc/postgresql/9.*/main/pg_hba.conf
psswd=sursum69

Usage () {
  printf "$0 project_name project_directory"
}

cd /

if [[ -z "$PROJNAME" ]]; then
  echo "No PROJNAME given! ..."
  Usage
  exit 1
fi

# Make a project directory
if [[ -d "$PROJDIR" ]]; then
  echo "Project Direcory already exist! Exiting ..."
  Usage
  exit 1
fi
if [[ -z "$PROJDIR" ]]; then
  PROJDIR=${PROJNAME}env
fi

setup_django () {
  echo "Setup Django..."
  #. ./settings.py


  source $PROJ_ENV_PATH/bin/activate
  echo "activated virtenv from directory: " `pwd`
  cd /${PROJDIR}

  django-admin startproject $PROJNAME .

  SETTINGS_PY="./${PROJNAME}/settings.py"
  echo "SETTINGS_PY: "$SETTINGS_PY
  sed -i "s/sqlite3/postgresql_psycopg2/" ${SETTINGS_PY}
  sed -i "s/'NAME': os.path.join(BASE_DIR, 'db.*//" ${SETTINGS_PY}
  sed -i "/'ENGINE': 'django.db.backends/a 'NAME': '${PROJNAME}'," ${SETTINGS_PY}
  sed -i "/'NAME': '${PROJNAME}',/a 'USER': '${PROJNAME}'," ${SETTINGS_PY}
  sed -i "/'USER': '${PROJNAME}',/a 'PASSWORD': '${psswd}'," ${SETTINGS_PY}
  sed -i "/'PASSWORD': '${psswd}',/a 'HOST': 'localhost'," ${SETTINGS_PY}
  sed -i "/'HOST': 'localhost',/a 'PORT': ''," ${SETTINGS_PY}
  #sed -i "/STATIC_URL='\/static\/',/a STATIC_ROOT = os.path.join(BASE_DIR, 'static')" ${SETTINGS_PY}
  sed -i "/STATIC_URL = /a STATIC_ROOT = os.path.join(BASE_DIR, 'static')" ${SETTINGS_PY}
  sed -ie "s|'UTC'|'Europe/Stockholm'|g" ${SETTINGS_PY}
  sed -ie "s|ALLOWED_HOSTS = \[\]|ALLOWED_HOSTS = ['localhost', '127.0.0.1']|" ${SETTINGS_PY}

  ### Deactivate virtual environment
  deactivate
  echo "deactivated virtual environment ${PROJNAME}"
}

setup_db () { # Make manual
  echo "Setup DB..."
  cd /

  # # Database server setup
  # sed -i "s/peer/md5/" ${POSTGRES_CONF_FILE}
  

  # Database setup
  SETUP_SQL=${SCRIPT_DIRNAME}/django_setup_DB.sql
  cp ${SCRIPT_DIRNAME}/django_setup_DB.tmpl $SETUP_SQL
  
  sed -i "s|PROJNAME|${PROJNAME}|g" ${SETUP_SQL}

  echo "PSQL:"
  /usr/sbin/service postgresql start
  /usr/sbin/service postgresql status

  echo "Running DB setup"
  # psql -U postgres -d database_name -c "SELECT c_defaults  FROM user_info WHERE c_uid = 'testuser'"
  su - postgres -c "psql -U postgres -f '${SCRIPT_DIRNAME}/django_setup_DB.sql'"
  whoami

  echo "done"
}

migrateDB () {
  echo "MIGRATEDB..."
  echo "Starting in directory: " `pwd`
  echo "I am: " `whoami`
  cd /

  # Set Postgres conf file to enable md5 instead of peer
  # as to enable django user local connection to database
  POSTGRES_VERSION=`psql -V | sed 's|psql.* \([0-9.]*\)[.][0-9]*.*|\1|'`
  echo "POSTGRES_VERSION: "$POSTGRES_VERSION
  POSTGRES_CONF_FILE="/etc/postgresql/${POSTGRES_VERSION}/main/pg_hba.conf"

  sed -i 's/\(^local[ ]*all[ ]* postgres[ ]*\) peer/\1 md5/' ${POSTGRES_CONF_FILE}
  echo ${POSTGRES_CONF_FILE}

  # Restart Postgres DB
  /usr/sbin/service postgresql restart
  /usr/sbin/service postgresql status

  source $PROJ_ENV_PATH/bin/activate
  echo "activated virtenv from directory: " `pwd`
  cd ${PROJDIR}
  echo "working from directory: " `pwd`
  echo "makemigrations..."
  python manage.py makemigrations
  echo "migrate..."
  python manage.py migrate
  #echo "MIGRATEDB..."
  #python manage.py createsuperuser
  #python manage.py syncdb
  deactivate
}

addGit () {
  # add to Git
  source $PROJ_ENV_PATH/bin/activate
  cd $PROJDIR

  pip3 freeze > requirements.txt

  git add requirements.txt
  git commit -m 'Committed requirements'

  printf "${PROJNAME}/\n*.pyc\n" > .gitignore
  git add .gitignore
  git commit -m 'Added a gitignore file'

  git add
  git commit -m 'Created project skeleton'

}

installation () {
  echo "installation..."
  apt-get -y update
  apt-get -y install postgresql postgresql-contrib
  apt-get -y install python3-pip python3-dev libpq-dev
  pip3 install --upgrade pip
  pip3 install virtualenv 
  
  sudo -u $SUDO_USER mkdir ${PROJDIR}
  cd $PROJDIR
  pwd

  # init Git from PROJDIR
  #cd $PROJDIR
  # git init

  # Create a virtual environment and activate
  virtualenv --python=python3 $PROJ_ENV_PATH --distribute

  source $PROJ_ENV_PATH/bin/activate
  
  # Install Django
  sudo -u $SUDO_USER pip3 install django django-toolbelt psycopg2 markdown
  django-admin --version
  python -c "import psycopg2"

  ### Deactivate virtual environment
  deactivate
  echo "deactivated virtual environment ${PROJNAME}"

  echo "Started virtual environment ${PROJNAME}"
  echo "Created new directory: "`ls -l`
}

main () {
  ### installation
  echo "SCRIPT_DIRNAME: "$SCRIPT_DIRNAME
  echo "PROJNAME: "$PROJNAME

  PROJ_ENV_PATH=$PROJDIR/$PROJNAME

  installation
  setup_django
  setup_db
  migrateDB



  echo "To test installation:"
  echo "Start virtual env ${PROJNAME}"
  echo "source /$PROJDIR/$PROJNAME/bin/activate"
  echo "Start webserver ${PROJNAME}:"
  echo "> python manage.py runserver 0.0.0.0:8000"

}


touch $SCRIPT_DIRNAME/$0.log

main $PROJNAME $PROJDIR > $SCRIPT_DIRNAME/$0.log 2>&1 &
exit
