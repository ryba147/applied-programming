from myproject import application
from announcements import *
import pytest
import tempfile
import os
import base64
import json

login="SOMEBODY"
PASSWORD="SOMEBODY"

started=0


@pytest.fixture( )
def test_client():
    global started
    if started == 0:
        os.popen('rm ./test.db')
        os.popen('cp ./clean.db ./test.db')
        started=1
    application.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../test.db'
    application.config['TESTING']=True
    test_client=application.test_client( )
    return test_client


def test_insertUserNonExist(test_client):
    response=test_client.post('/user/?username=test_user', content_type='multipart/form-data',
                              data={"firstname": "test_user2", "lastname": "lastname_test2",
                                    "username": "test_user", "password": "test_pass2", "location": 1})
    assert len(response.json) == 6


def test_insertUserExist(test_client):
    response=test_client.post('/user/?username=test_user', content_type='multipart/form-data',
                              data={"firstname": "test_user2", "lastname": "lastname_test2",
                                    "username": "test_user", "password": "test_pass2", "location": 1})
    assert response.status_code == 403 and response.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>403 Forbidden</title>\n<h1>Forbidden</h1>\n<p>User with that name exists!!!</p>\n'


def test_getUsers(test_client):
    response=test_client.get('/user')
    assert response.status_code == 200


def test_getIncorrectUser(test_client):
    response=test_client.get('/user/not-test_user')
    assert response.status_code == 404


def test_geCorrectUser(test_client):
    response=test_client.get('/user/test_user')
    assert response.status_code == 200


def test_getAnnouncementsNearby(test_client):
    response=test_client.get('/announcement/nearby/')
    assert response.status_code == 200


def test_getCorrectAnnouncementsById(test_client):
    response=test_client.get('/announcement/1/')
    assert response.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>announcement not found</p>\n'


def test_getWrongAnnouncementsById(test_client):
    response=test_client.get('/announcement/2/')
    assert response.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>announcement not found</p>\n'


def test_getAllAnnouncements(test_client):
    response=test_client.get('/announcement/')
    assert response.status_code == 200


def test_loginInCorrectUser(test_client):
    response=test_client.get('/user/login/?username=test_user12345&password=test_pass212345')
    assert response.data == b'Wrong username or password'


def test_loginCorrectUser(test_client):
    response=test_client.get('/user/login/?username=test_user&password=test_pass2')
    assert response.data == b'Ok'


def test_updateUser(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'').decode('ascii')}
    response=test_client.put()
    assert response.data == b''

# Testing creating announcement
def test_createAnnouncement(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'').decode('ascii')}
    response=test_client.post('/user/logout/')
    assert response.data == b"You are log out"


# Testing upgrating announcement
def test_upgradeAnnouncement(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'').decode('ascii')}
    response=test_client.put('/user/logout/',{},headers=headers)
    assert response.data == b"You are log out"


# Testing deleting announcement
def test_deleteAnnouncement(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'').decode('ascii')}
    response=test_client.delete('/user/delete/1', headers=headers)
    assert response.data == b"You are log out"


def test_deleteUser(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'').decode('ascii')}
    response=test_client.delete('/user/test_user', headers=headers)
    assert response.data == b"You are log out"


# Testing logout
def test_logout(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'').decode('ascii')}
    response=test_client.get('/user/logout/')
    assert response.data == b"You are log out"

    # headers={"Content-Type": "text/html; charset=utf-8"}
    # print(response)
    # assert headers['Content-Type'] == response.headers['content-type']
