apt install python3 python3-pip python3-venv

echo "token = 'INSERT YOUR TOKEN'" > src/config.py
echo "cluster = 'mongodb://localhost:27017/'" >> src/config.py

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirments.txt

python3 src/bot.py &
