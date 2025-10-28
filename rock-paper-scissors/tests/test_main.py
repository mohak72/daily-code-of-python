"""Tests for Rock Paper Scissors"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


def test_imports():
    """Test that main module can be imported"""
    assert hasattr(main, 'determine_winner')
    assert hasattr(main, 'play_round')
    assert hasattr(main, 'CHOICES')


def test_determine_winner_rock_vs_scissors():
    """Test that Rock beats Scissors"""
    assert main.determine_winner('1', '3') == 'user'
    assert main.determine_winner('3', '1') == 'computer'


def test_determine_winner_paper_vs_rock():
    """Test that Paper beats Rock"""
    assert main.determine_winner('2', '1') == 'user'
    assert main.determine_winner('1', '2') == 'computer'


def test_determine_winner_scissors_vs_paper():
    """Test that Scissors beats Paper"""
    assert main.determine_winner('3', '2') == 'user'
    assert main.determine_winner('2', '3') == 'computer'


def test_determine_winner_draw():
    """Test draw conditions"""
    assert main.determine_winner('1', '1') == 'draw'
    assert main.determine_winner('2', '2') == 'draw'
    assert main.determine_winner('3', '3') == 'draw'


def test_choices_dict():
    """Test that CHOICES dict is properly defined"""
    assert '1' in main.CHOICES
    assert '2' in main.CHOICES
    assert '3' in main.CHOICES
    assert main.CHOICES['1'] == 'Rock'
    assert main.CHOICES['2'] == 'Paper'
    assert main.CHOICES['3'] == 'Scissors'
