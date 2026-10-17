"""Modul pengujian untuk endpoint Flask."""
import pytest
from app import app, init_db

@pytest.fixture
def client():
    """Fixture untuk mengonfigurasi test client Flask."""
    app.config["TESTING"] = True
    init_db()
    with app.test_client() as client:
        yield client

def test_halaman_utama_get(client):
    """Memastikan halaman login dapat dimuat dengan metode GET."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Portal Login" in response.data

def test_login_berhasil(client):
    """Memastikan login berhasil dengan kredensial default admin."""
    response = client.post(
        "/",
        data={"username": "admin", "password": "supersecret"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Login Berhasil!".encode("utf-8") in response.data

def test_login_gagal(client):
    """Memastikan login ditolak jika username atau password salah."""
    response = client.post(
        "/",
        data={"username": "fulan", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Login Gagal!".encode("utf-8") in response.data