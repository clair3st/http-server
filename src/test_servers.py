"""Test echo socket communication."""

import pytest
import socket


PARAMS_TABLE = [
    'Yo',
    'This is a longer message, longer than most other messages.',
    'This has sixteen',
    # 'Å´ˆØ¨',
]


@pytest.mark.parametrize("result", PARAMS_TABLE)
def test_message_completion(result):
    """Test table of potential messages for receipt and transmission."""
    from client import client
    # from server import server
    assert client(result) == result
