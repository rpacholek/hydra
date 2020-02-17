import unittest

from hydra.core.communication.network.message import Message, MessageProcessor, MessageException


# Message class is abstract therefore provide a simple implementation
class SimpleMessage(Message):
    def __init__(self):
        self.data = ({"test": "test"}, "string with utf-8: łąćżęć", [])

    def loads_message(self, header, body, attachments):
        self.data = (header, body, attachments)

    def dumps_message(self):
        return self.data

    @staticmethod
    def get_message_type():
        return "TestType"


class SimpleMessage2(Message):
    def __init__(self):
        self.data = ({"test": "test"}, "string with utf-8: łąćżęć", [])

    def loads_message(self, header, body, attachments):
        self.data = (header, body, attachments)

    def dumps_message(self):
        return self.data

    @staticmethod
    def get_message_type():
        return "OtherTestType"

# Tests


class TestSimpleMessage(unittest.TestCase):
    def setUp(self):
        self.message = SimpleMessage()

    def test_serialize_deserialize(self):
        result = SimpleMessage().loads(self.message.dumps())
        assert result.data == self.message.data

    def test_process(self):
        data = self.message.dumps()
        typename, _, _, _ = Message.process(data)
        assert typename == self.message.get_message_type()


class TestMessage(unittest.TestCase):
    def test_encode_decode(self):
        header = {"test": "test", "test2": "2"}
        body = "teststringąśðæśłćńþœπœę©"
        attachments = []

        encoded = Message._encode(header, body, attachments)
        header2, body2, attachments2 = Message._decode(encoded)

        assert header == header2
        assert body == body2
        assert attachments == attachments2


class TestMessageProcessor(unittest.TestCase):
    def setUp(self):
        self.message1 = SimpleMessage()
        self.message1.loads_message({"test1": "test1"}, "a string", [])
        self.message2 = SimpleMessage2()
        self.message1.loads_message({"test2": "test2"}, "a string2", [])

    def test_constructor(self):
        mp = MessageProcessor(SimpleMessage, SimpleMessage2)
        msg1 = mp.loads(self.message1.dumps())
        assert msg1.get_message_type() == self.message1.get_message_type()

        msg2 = mp.loads(self.message2.dumps())
        assert msg2.get_message_type() == self.message2.get_message_type()

    def test_register(self):
        mp = MessageProcessor()
        mp.register(SimpleMessage)
        msg1 = mp.loads(self.message1.dumps())
        assert msg1.get_message_type() == self.message1.get_message_type()

        with self.assertRaises(MessageException):
            msg2 = mp.loads(self.message2.dumps())

        mp.register(SimpleMessage2)
        msg2 = mp.loads(self.message2.dumps())
        assert msg2.get_message_type() == self.message2.get_message_type()
