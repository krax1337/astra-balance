git pull

echo "token = 'INSERT YOUR TOKEN'" > src/config.py

python3 -m venv venv

source venv/bin/activate

pip3 -i requirments.txt

python3 src/bot.py &