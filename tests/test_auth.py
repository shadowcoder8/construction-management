import pytest
import os
from fastapi import HTTPException
from backend.auth import authenticate_admin

def test_authenticate_admin_success(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin_test")
    monkeypatch.setenv("ADMIN_PASSWORD", "secure_password")

    result = authenticate_admin("admin_test", "secure_password")
    assert result == {"message": "Login successful"}

def test_authenticate_admin_invalid_username(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin_test")
    monkeypatch.setenv("ADMIN_PASSWORD", "secure_password")

    with pytest.raises(HTTPException) as exc_info:
        authenticate_admin("wrong_admin", "secure_password")
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid username or password"

def test_authenticate_admin_invalid_password(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin_test")
    monkeypatch.setenv("ADMIN_PASSWORD", "secure_password")

    with pytest.raises(HTTPException) as exc_info:
        authenticate_admin("admin_test", "wrong_password")
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid username or password"

def test_authenticate_admin_missing_env(monkeypatch):
    monkeypatch.delenv("ADMIN_USERNAME", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)

    with pytest.raises(HTTPException) as exc_info:
        authenticate_admin("admin_test", "secure_password")
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Server configuration error"
