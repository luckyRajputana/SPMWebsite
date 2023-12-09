echo "BUILD START"
apt-get install libpq-dev
pip install -r requirements.txt
python3.9 manage.py collectstatic
echo "BUILD END"