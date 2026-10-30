import pytest

from app import app, init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Membuat test client dengan database sementara."""
    monkeypatch.chdir(tmp_path)
    app.config["TESTING"] = True

    init_db()

    with app.test_client() as test_client:
        yield test_client


def test_halaman_login_dapat_dibuka(client):
    """Memastikan halaman login dapat diakses."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Portal Login" in response.data


def test_login_berhasil(client):
    """Memastikan pengguna dengan kredensial benar dapat login."""
    response = client.post(
        "/",
        data={
            "username": "admin",
            "password": "supersecret",
        },
    )

    assert response.status_code == 200
    assert b"Login Berhasil!" in response.data


def test_login_gagal_password_salah(client):
    """Memastikan login ditolak ketika password salah."""
    response = client.post(
        "/",
        data={
            "username": "admin",
            "password": "passwordsalah",
        },
    )

    assert response.status_code == 200
    assert b"Login Gagal!" in response.data


def test_login_gagal_username_tidak_dikenal(client):
    """Memastikan login ditolak untuk username yang tidak terdaftar."""
    response = client.post(
        "/",
        data={
            "username": "penggunaasing",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert b"Login Gagal!" in response.data


def test_login_gagal_username_kosong(client):
    """Memastikan login ditolak ketika username kosong."""
    response = client.post(
        "/",
        data={
            "username": "",
            "password": "supersecret",
        },
    )

    assert response.status_code == 200
    assert b"Login Gagal!" in response.data


def test_login_gagal_password_kosong(client):
    """Memastikan login ditolak ketika password kosong."""
    response = client.post(
        "/",
        data={
            "username": "admin",
            "password": "",
        },
    )

    assert response.status_code == 200
    assert b"Login Gagal!" in response.data


def test_login_mencegah_sql_injection(client):
    """Memastikan input SQL Injection tidak dapat melewati autentikasi."""
    response = client.post(
        "/",
        data={
            "username": "' OR '1'='1",
            "password": "' OR '1'='1",
        },
    )

    assert response.status_code == 200
    assert b"Login Gagal!" in response.data
