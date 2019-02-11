from ymmsl import Reference

from libmuscle.mcp.message import Message


def test_create() -> None:
    sender = Reference('sender.port')
    receiver = Reference('receiver.port')
    parameter_overlay = (6789).to_bytes(2, 'little', signed=True)
    data = (12345).to_bytes(2, 'little', signed=True)
    msg = Message(sender, receiver, parameter_overlay, data)
    assert msg.sender == sender
    assert msg.receiver == receiver
    assert msg.parameter_overlay == parameter_overlay
    assert msg.data == data
