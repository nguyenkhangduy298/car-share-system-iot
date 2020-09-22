# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import MySQLdb
from database_utils import DatabaseUtils
from main import app
from flask import request, url_for

class Test(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def login(self, username, password):
        tester = app.test_client(self)
        return tester.post('/login', data=dict(name=username,
                                                  password=password), follow_redirects=True)

    def test_login(self):
        response = self.login('customer', 'customer')
        self.assertIn(b'Hello, customer', response.data)

        response = self.login('admin', 'admin')
        self.assertIn(b'Welcome admin', response.data)

        response = self.login('manager', 'manager')
        self.assertIn(b'Welcome manager', response.data)

        response = self.login('engineer', 'engineer')
        self.assertIn(b'Welcome engineer', response.data)

        response = self.login('123123', 'asdasd')
        self.assertIn(b'Cannot find user! Try again', response.data)
        
    # def test_register(self):
    #     tester = app.test_client(self)
    #     reponse = tester.post('/register', data=dict(name='admin1',
    #                                                  password='admin1',
    #                                                  position='admin'),
    #                           follow_redirects=True)
    #     self.assertIn(b'Registered successfully', reponse.data)

    def test_logout(self):
        tester = app.test_client(self)
        reponse = tester.get('/logout', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_bookCalendar(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/customer/bookCalendar', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_searchCarCustomer(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/customer/available', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_cancel(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/customer/cancel', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_bookList(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/customer/bookedList', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_modifycar(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/modifycar', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_addcar(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/addcar', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_removecar(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/addcar', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_searchcar(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/searchcar', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_modifycustomer(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/modifycustomer', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_addcustomer(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/addcustomer', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_removecustomer(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/addcustomer', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_searchcustomer(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/searchcustomer', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_history(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/history', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

    def test_report(self):
        tester = app.test_client(self)
        reponse = tester.get('http://127.0.0.1:5000/admin/report', content_type='html/text')
        self.assertTrue(reponse.status_code, 200)

if __name__ == "__main__":
    unittest.main()
    # searchCustomer.admin()
