#!/bin/bash
export MAAS_DBUSER=maasdbuser
export MAAS_DBPASS=pass01
export MAAS_DBNAME=maas
sudo -u postgres psql -c "CREATE USER \"$MAAS_DBUSER\" WITH ENCRYPTED PASSWORD '$MAAS_DBPASS'"
sudo -u postgres createdb -O "$MAAS_DBUSER" "$MAAS_DBNAME"
echo "host    $MAAS_DBNAME    $MAAS_DBUSER    0/0     md5" | sudo tee -a /etc/postgresql/12/main/pg_hba.conf
sudo maas init region+rack --database-uri "postgres://$MAAS_DBUSER:$MAAS_DBPASS@localhost/$MAAS_DBNAME"