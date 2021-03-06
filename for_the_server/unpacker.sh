new_dir_name=`date "+%b%d%H%M" | tr '[:upper:]' '[:lower:]'`
mkdir $new_dir_name
tar -zxvf ~/tray/current.tar.gz -C $new_dir_name
chown -R www-data $new_dir_name
chgrp -R www-data $new_dir_name
ln -sfn $new_dir_name current
staging_dir=/tmp/cube-server
mkdir -p /tmp/cube-server
chown -R www-data $staging_dir
chgrp -R www-data $staging_dir
systemctl restart apache2
rm -f ~/tray/current.tar.gz


