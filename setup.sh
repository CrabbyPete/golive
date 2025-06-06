sudo apt update
if ( ! sudo apt update ); then
  echo "Update failed"
  exit 1
fi

sudo apt upgrade -y
sudo apt install -y git emacs-nox python3-pip python3-venv ttf-mscorefonts-installer

sudo raspi-config nonint do_i2c 1
sudo apt install -y i2c-tools

python3 -m venv venv --system-site-packages
./venv/bin/activate
pip3 pip install open-gopro luma.oled

git clone https://github.com/CrabbyPete/golive.git


sudo cp /etc/golive.service /etc/systemd/system
sudo chmod 666 /etc/systemd/system/golive.service
sudo systemctl enable golive
sudo systemctl start golive


