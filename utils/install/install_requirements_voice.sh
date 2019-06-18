echo ===============================
echo Devolution - Voice Requirements
echo ===============================
sleep 5
apt-get update
apt-get install python3-pip -y
python3 -m pip install -U discord.py[voice]
python3 -m pip install -U youtube_dl

echo [Devolution] Installing FFMPEG
sleep 5
apt-get install software-properties-common
sudo add-apt-repository ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get install ffmpeg
sudo apt-get install frei0r-plugins
echo
echo [Devolution] Installation Complete!
