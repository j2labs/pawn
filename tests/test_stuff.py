import pytest

from pawn.servers import Server

def test_server():
    s = Server()
    assert s is not None
