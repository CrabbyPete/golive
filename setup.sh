sudo apt update
if ( ! sudo apt update ); then
  echo "Update failed"
  exit 1
fi

sudo apt upgrade -y
sudo apt install -y git emacs-nox python3-pip python3-venv

python3 -m venv venv --system-site-packages
./venv/bin/activate

git clone https://github.com/CrabbyPete/golive.git
cd golive/src
pip3 pip install open-gopro
cd

sudo cp /etc/golive.service /etc/systemd/system
sudo chmod 666 /etc/systemd/system/golive.service
sudo systemctl enable golive
sudo systemctl start golive


