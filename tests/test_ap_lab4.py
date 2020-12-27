from myproject import application
from announcements import *
import pytest
import tempfile
import os




def test_getUsers(test_client):
    with application.test_client() as test_client:
        response=test_client.get('/user')
        print(response)
        assert response.status_code == 200


def test_getIncorrectUser():
    with application.test_client() as test_client:
        response=test_client.get('/user/not-Taras/')
        print(response)
        assert response.status_code == 404


def test_geCorrectUser():
    with application.test_client() as test_client:
        response=test_client.get('/user/admin/')
        print(response)
        assert response.status_code == 200


def test_getAnnouncementsNearby():
    with application.test_client() as test_client:
        response=test_client.get('/announcement/nearby/')
        assert response.status_code == 200


def test_getCorrectAnnouncementsById():
    with application.test_client() as test_client:
        response=test_client.get('/announcement/1/')
        assert response.status_code == 200


def test_getWrongAnnouncementsById():
    with application.test_client() as test_client:
        response=test_client.get('/announcement/2/')
        assert response.status_code == 404


def test_getAllAnnouncements():
    with application.test_client() as test_client:
        response=test_client.get('/announcement/')
        assert response.status_code == 200