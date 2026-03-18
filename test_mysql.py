import MySQLdb

common_passwords = ['', 'root', 'admin', 'password', '1234', '12345', '123456', 'mysql', 'Chetan', 'chetan']

def test_passwords():
    for pwd in common_passwords:
        try:
            db = MySQLdb.connect(host='localhost', user='root', passwd=pwd)
            cursor = db.cursor()
            cursor.execute('CREATE DATABASE IF NOT EXISTS agri_portal_db;')
            print(f'SUCCESS_PASSWORD:{pwd}')
            return
        except Exception as e:
            pass
    print("PASSWORD_NOT_FOUND")

if __name__ == '__main__':
    test_passwords()
