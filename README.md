# Creating MAAS and juju

## Creating MAAS

Documentation can be found [here](https://maas.io/docs/snap/3.1/ui/maas-installation)

1. Create an MAAS VM
2. Install maas
            
        sudo snap install maas
            
4. install postgresql

       sudo apt install -y postgresql
            
6. configure postgressql

        #!/bin/bash
        export MAAS_DBUSER=maasdbuser
        export MAAS_DBPASS=pass01
        export MAAS_DBNAME=maas
        sudo -u postgres psql -c "CREATE USER \"$MAAS_DBUSER\" WITH ENCRYPTED PASSWORD '$MAAS_DBPASS'"
        sudo -u postgres createdb -O "$MAAS_DBUSER" "$MAAS_DBNAME"
        echo "host    $MAAS_DBNAME    $MAAS_DBUSER    0/0     md5" | sudo tee -a /etc/postgresql/12/main/pg_hba.conf
        sudo maas init region+rack --database-uri "postgres://$MAAS_DBUSER:$MAAS_DBPASS@localhost/$MAAS_DBNAME"

6. Create MAAS admin user

        sudo maas createadmin --username admin --password pass01 --email irzan@juniper.net

7. login into MAAS GUI, and continue the configuration

        http://<ip_of_maas>:5240/MAAS

8. Set the following parameter
    - DNS forwarder
    - sync boot image
    - add ssh public keys for admin
    - set DHCP DNS server
    - add and set space
    - enable DHCP (under subnet)
9. from the CLI, check the status of MAAS

        sudo maas status


## Creating juju controller
1. Create VM for juju client
2. install juju client into the VM

        sudo snap install juju --classic
3. Create file maas-clouds.yaml with the following content

        clouds:
            lab1:
                type: maas
                auth-types: [oauth1]
                endpoint: http://10.1.100.2:5240/MAAS

4. Open ssh session into maas, and get the api key

        sudo maas apikey --username=admin

5. on juju client VM, create file maas-creds.yaml, and add the api key into it

        credentials:
            lab1:
                anyuser:
                auth-type: oauth1
                maas-oauth: <api_key>

6. add MAAS cloud using the following command

        juju add-cloud --local lab1 ./maas-cloud.yaml

7. set the credential using the following command

       juju add-credential lab1 -f ./maas-creds.yaml

8. Create a VM, with 4G RAM/40G HDD, and add it into MAAS, comission it, and  set tags=juju to this VM

9. Run the following command to bootstrap a juju controller, it will automatically deploy a VM and install juju controller into this VM

        juju bootstrap --constraints  tags=juju lab1

10. Do the following to check the controller status

        juju status
        juju controllers