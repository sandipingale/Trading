# **Digital Ocean Droplet process**
1. Login to droplet using root 
2. Use Putty or ssh from command prompt\
 ```
    ssh root@your_server_ip
 ```
 3. Create new user, it will ask few information along with password\
 ```
    adduser tiadmin
 ```
 4. As root, run this command to add your new user to the sudo group\
 ```
    usermod -aG sudo tiadmin
 ```
 5. On the server, as the root user, enter the following command to temporarily switch to the new user\
 ```
    su - tiadmin
 ```
 6. login with new user
 ```
    ssh tiadmin@your_server_ip
 ```
 7. Setup basic firewall\
 ```
    sudo ufw app list
    sudo ufw allow OpenSSH
    sudo ufw enable
    sudo ufw status
```

# **Install the Packages from the Ubuntu Repositories**
1. Update local apt packages\
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
```
2. Create PostgreSQL Database and user\
``` 
    sudo -u postgres psql
    CREATE DATABASE trading;
    CREATE USER tidbuser WITH PASSWORD '*****';
    ALTER ROLE  tidbuser SET client_encoding TO 'utf8';
    ALTER ROLE tidbuser SET default_transaction_isolation TO read committed';
    ALTER ROLE tidbuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE  TRADING TO tidbuser;
```

# **Create Python venv**
 ```
    sudo -H pip3 install --upgrade pip
    sudo -H pip3 install virtualenv
    mkdir myproject
    cd myproject
    virtualenv myprojectenv
    source myprojectenv/bin/activate
 ```

# **install and configure django and project**
1. Install django and dependencies\
``` 
    pip install django gunicorn psycopg2
    git clone https://github.com/sandipingale/Trading.git
```
For gi clone it will ask user and password, for password give token
2. export below environment variables, replace passwords with actuals\
```
    export gmail_password=*******
    export mysql_enabled=True
    export mydbname=trading
    export mydbuser=tidbuser
    export mydbpassword=********
    export mydbhost=localhost
```
3. Django migrations, create super user and stati files
```
    cd /home/tiadmin/Trading/investment
    python manage.py makemigrations
    python anage.py migrate
    manage.py createsuperuser 
    python manage.py collectstatic
```
4. Create an exception for port 8000 by typing:\
```
    sudo ufw allow 8000
```
5. Start the django server\
```
    manage.py runserver 0.0.0.0:8000
```
6. In browser you can launch with below url
```
    http://server_domain_or_IP:8000
```

# **Test Gunicorn ability**
 ```
    cd /home/tiadmin/Trading/investment
    gunicorn --bind 0.0.0.0:8000 investment.wsgi
```
3. This will start Gunicorn on the same interface that the Django development server was running on. You can go back and test the app again.

# **Create Gunicorn systemd service file**
1. Create the gunicorn file
```[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=tiadmin
Group=tiadmin
WorkingDirectory=/home/tiadmin/Trading/investment
ExecStart=/home/tiadmin/myproject/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/tiadmin/Trading/investment/investment.sock investment.wsgi:application

[Install]
WantedBy=multi-user.target
```
2. With that, our systemd service file is complete. Save and close it now. We can now start the Gunicorn service we created and enable it so that it starts at boot:
```
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```
3. Check the gunicorn socket file
```
sudo systemctl status gunicorn
```

4. Next, check for the existence of the investment.sock file within your project directory:
```
ls -lrt /home/tiadmin/Trading/investment/investment.sock
```

5. If the systemctl status command indicated that an error occurred or if you do not find the investment.sock file in the directory, it’s an indication that Gunicorn was not able to start correctly. Check the Gunicorn process logs by typing:
```
sudo journalctl -u gunicorn
```
6. If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process by typing:
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

# **Configure NGINX**
1. Create the configuration file as below
```
server {
#    listen 80;
    server_name tradeandinvest.in;
    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/tradeandinvest.in/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/tradeandinvest.in/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot



    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/tiadmin/Trading/investment;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/tiadmin/Trading/investment/investment.sock;
    }
}
```
2. Test the nginx configurations file
```
    sudo nginx -t
```

3. Restart the nginx 
```
    sudo systemctl restart nginx
```

4. Allow the firewall
```
    sudo ufw delete allow 8000
    sudo ufw allow 'Nginx Full'
```

# **Restarting nginx and gunicorn
```
sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo nginx -t && sudo systemctl restart nginx
```








