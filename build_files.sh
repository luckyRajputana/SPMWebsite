echo "BUILD START"
yum install postgresql-devel
yes | pip install -r requirements.txt
yes | python3.9 manage.py collectstatic
echo "BUILD END"