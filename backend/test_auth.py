import pytest
import os
from fastapi import HTTPException
from backend.auth import authenticate_admin

def test_authenticate_admin_success(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "admin123")
    assert authenticate_admin("admin", "admin123") == {"message": "Login successful"}

def test_authenticate_admin_invalid_username(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "admin123")
    with pytest.raises(HTTPException) as exc_info:
        authenticate_admin("wrongadmin", "admin123")
    assert exc_info.value.status_code == 401

def test_authenticate_admin_invalid_password(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "admin123")
    with pytest.raises(HTTPException) as exc_info:
        authenticate_admin("admin", "wrongpassword")
    assert exc_info.value.status_code == 401

def test_authenticate_admin_invalid_both(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "admin123")
    with pytest.raises(HTTPException) as exc_info:
        authenticate_admin("wrongadmin", "wrongpassword")
    assert exc_info.value.status_code == 401

def test_authenticate_admin_unconfigured_credentials(monkeypatch):
    monkeypatch.delenv("ADMIN_USERNAME", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    with pytest.raises(HTTPException) as exc_info:
        authenticate_admin("admin", "admin123")
    assert exc_info.value.status_code == 500

def test_authenticate_admin_missing_one_credential(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    with pytest.raises(HTTPException) as exc_info:
        authenticate_admin("admin", "admin123")
    assert exc_info.value.status_code == 500
