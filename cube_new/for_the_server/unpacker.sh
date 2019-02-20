new_dir_name=`date "+%b%d%H%M" | tr '[:upper:]' '[:lower:]'`
mkdir $new_dir_name
tar -zxvf ~/tray/current.tar.gz -C $new_dir_name
chown -R www-data $new_dir_name
chgrp -R www-data $new_dir_name
ln -sfn $new_dir_name current
systemctl restart apache2



