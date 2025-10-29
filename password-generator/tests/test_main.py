"""Tests for Password Generator"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import main


def test_imports():
    """Test that main module can be imported"""
    assert hasattr(main, 'generate_password')
    assert hasattr(main, 'calculate_password_strength')


def test_generate_password_default():
    """Test password generation with defaults"""
    password = main.generate_password()
    assert len(password) == 12
    assert isinstance(password, str)


def test_generate_password_length():
    """Test custom password length"""
    password = main.generate_password(length=20)
    assert len(password) == 20


def test_generate_password_only_lowercase():
    """Test password with only lowercase"""
    password = main.generate_password(
        use_uppercase=False,
        use_digits=False,
        use_special=False
    )
    assert password.islower()


def test_password_strength_weak():
    """Test weak password detection"""
    score, strength = main.calculate_password_strength("abc")
    assert score <= 2


def test_password_strength_strong():
    """Test strong password detection"""
    score, strength = main.calculate_password_strength("Abc123!@#xyz")
    assert score >= 4


def test_password_min_length():
    """Test minimum password length enforcement"""
    with pytest.raises(ValueError):
        main.generate_password(length=2)
