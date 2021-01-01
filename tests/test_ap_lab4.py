from myproject import application
from announcements import *
import pytest
import tempfile
import os
import base64
import json
started = 0


@pytest.fixture()
def test_client():
    global started
    if started == 0:
        os.popen('rm ./test.db')
        os.popen('cp ./clean.db ./test.db')
        started=1
    application.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../test.db'
    application.config['TESTING']=True
    test_client=application.test_client()
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
    assert response.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>403 Forbidden</title>\n<h1>Forbidden</h1>\n<p>User with that name exists!!!</p>\n'


def test_getUsers(test_client):
    response=test_client.get('/user')
    assert response.status_code == 200


def test_getIncorrectUser(test_client):
    response=test_client.get('/user/not-test_user')
    assert response.status_code == 404


def test_geCorrectUser(test_client):
    response=test_client.get('/user/test_user')
    assert response.status_code == 200


def test_loginInCorrectUser(test_client):
    response=test_client.get('/user/login/?username=test_user12345&password=test_pass212345')
    assert response.data == b'Wrong username or password'


#Test loginCorrectUser
def test_loginCorrectUser(test_client):
    response=test_client.get('/user/login/?username=test_user&password=test_pass2')
    assert response.data == b'Ok'


#Testing updated user
def test_updateUser(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'test_user:test_pass2').decode('ascii')}
    response=test_client.put('/user/test_user',content_type='multipart/form-data',data={"firstname": "test_user3", "lastname": "lastname_test3",
                                    "username": "test_user", "password": "test_pass3", "location": 1}, headers=headers)
    assert response.status_code == 308


# Testing creating announcement
def test_createAnnouncement(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'test_user:test_pass2').decode('ascii')}
    response=test_client.post('/announcement/',content_type='multipart/form-data',data={
        'id' : 1,
        'authorid' : 1,
        'name' : 'name_1',
        'description' : 'base_desc',
        'pub_date' :  'today',
        'location' : 1,
        'announcement_type':1
    }, headers=headers)
    assert response.status_code == 200


# Testing upgrading announcement
def test_upgradeAnnouncement(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'test_user:test_pass2').decode('ascii')}
    response=test_client.put('/announcement/1/',content_type='multipart/form-data',data={
        'id' : 1,
        'authorid' : 1,
        'name' : 'name_1',
        'description' : 'updated_desc',
        'pub_date' :  'today',
        'location' : 1,
        'announcement_type':1
    }, headers=headers)
    assert response.status_code == 200


def test_getAllAnnouncements(test_client):
    response=test_client.get('/announcement/')
    assert response.status_code == 200


# Testing
def test_getAnnouncementsNearby(test_client):
    response=test_client.get('/announcement/nearby/1')
    assert response.data == b'[{"announcement_type":1,"authorid":1,"description":"updated_desc","id":1,"location":1,"name":"name_1","pub_date":"today"}]\n'


def test_getCorrectAnnouncementsById(test_client):
    response=test_client.get('/announcement/1/')
    assert response.status_code == 200


def test_getWrongAnnouncementsById(test_client):
    response=test_client.get('/announcement/2/')
    assert response.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>announcement not found</p>\n'


# Testing deleting announcement
def test_deleteAnnouncement(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'test_user:test_pass2').decode('ascii')}
    response=test_client.delete('/announcement/1', headers=headers)
    assert response.status_code == 308


# Testing deleting user
def test_deleteUser(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'test_user:test_pass2').decode('ascii')}
    response=test_client.delete('/user/test_user', headers=headers, follow_redirects = True)
    assert len(response.json) == 6


# Testing logout
def test_logout(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'test_user:test_pass2').decode('ascii')}
    response=test_client.get('/user/logout/',headers=headers)
    assert response.data == b"You are log out"


# Testing deleting wrong user
def test_deleteWrongUser(test_client):
    headers={'Authorization': 'Basic ' + base64.b64encode(b'test_user:test_pass2').decode('ascii')}
    response=test_client.delete('/user/test_user111', headers=headers, follow_redirects = True)
    assert response.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>user not found</p>\n'



    # headers={"Content-Type": "text/html; charset=utf-8"}
    # print(response)
    # assert headers['Content-Type'] == response.headers['content-type']
