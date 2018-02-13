import pytest

class MessageParser():
    def __init__(self):
        self.buffer = bytearray(b"")

    def parse(self, byte_buffer):
        splitted = byte_buffer.split(b',')
        result = []
        if not len(splitted):
            print("nothing splitted")
            return result

        if not len(splitted[0]):
            print("new message, clear buffer")
            self.buffer.clear()

        if len(self.buffer):
            self.buffer.extend(splitted[0])
            print("extend " + str(splitted[0]))
            print("check " + str(self.buffer))
            if len(self.buffer) == 4:
                result.append(int(self.buffer.decode("ascii"), 16))
                self.buffer.clear()
            #else:
            #self.buffer.clear()    

        for msg in [x for x in splitted[1:] if len(x) == 4]:
            try:
                print("adding val: " + str(msg))
                value = int(msg.decode("ascii"), 16)
                result.append(value)
            except ValueError:
                pass
        
        if not len(self.buffer) and len(splitted[-1]) != 4:
            print("add " + str(splitted[-1]))
            self.buffer.extend(splitted[-1])

        return result


@pytest.fixture
def message_parser():
    return MessageParser()

class Test_ParsesNoMessages:
    def test_empty_buffer(self):
        assert [] == message_parser().parse(b"")

    def test_badly_formatted_message_no_separator(self):
        assert [] == message_parser().parse(b"1234")

    def test_badly_formatted_message_too_short(self):
        assert [] == message_parser().parse(b",123")
        assert [] == message_parser().parse(b",12")
        assert [] == message_parser().parse(b",1")
    
    def test_badly_formatted_message_too_long(self):
        assert [] == message_parser().parse(b",12345")
        assert [] == message_parser().parse(b",1234597987987")
    
    def test_only_separator(self):
        assert [] == message_parser().parse(b",")
        assert [] == message_parser().parse(b",,,,,")

    def test_multiple_bad(self):
        assert [] == message_parser().parse(b",3,A2,123")

    def test_first_is_bad(self):        
        assert [] == message_parser().parse(b"ABC,")

    def test_not_hex(self):
        assert [] == message_parser().parse(b",DEFG")

class Test_ParsesMessagesDecodesAsHexNoChunks:
    def test_single_message(self):
        assert [0xA234] == message_parser().parse(b",A234")

    def test_two_messages(self):
        assert [0xA234, 0x0001] == message_parser().parse(b",A234,0001")

    def test_bunch_of_messages(self):
        assert [0xA234, 0x0001, 0x1234, 0x1337, 0xBEEF, 0xBABE] == message_parser(
            ).parse(b",A234,0001,1234,1337,BEEF,BABE")

    def test_bad_ones_in_between(self):
        assert [0x1111, 0xFFFF] == message_parser().parse(b",1111,12,345,1,12345,8282828282828,FFFF")

    def test_bad_one_in_beginning(self):
        assert [0xFFFF] == message_parser().parse(b"123,FFFF")

    def test_bad_one_in_the_end(self):
        assert [0xFFFF] == message_parser().parse(b",FFFF,1")

    def test_spaces_are_not_accepted(self):
        assert [0x1234] == message_parser().parse(b",1234, DEFG")

class Test_ParsesMessagesInTwo:
    def test_single_message_in_two_chunks(self):
        parser = message_parser()
        parser.parse(b",12")
        assert [0x1234] == parser.parse(b"34")

    def test_single_message_in_multiple_chunks(self):
        parser = message_parser()
        parser.parse(b",1")
        parser.parse(b"2")
        parser.parse(b"3")
        assert [0x1234] == parser.parse(b"4")

    def test_single_message_in_two_chunks_with_bad_formatting_too_much(self):
        parser = message_parser()
        parser.parse(b",12")
        assert [] == parser.parse(b"345")

    def test_single_message_in_two_chunks_with_bad_formatting_too_little(self):
        parser = message_parser()
        parser.parse(b",12")
        assert [] == parser.parse(b"3,")


    def test_multiple_messages_in_chunks_with_bad_formatting(self):
        parser = message_parser()
        parser.parse(b",1234,56")
        assert [0x1111] == parser.parse(b",1111")

    def test_multiple_chunks_with_single_byte_in_each_bad_formatted(self):
        parser = message_parser()
        parser.parse(b",")
        parser.parse(b"1")
        parser.parse(b"2")
        parser.parse(b"3")
        assert [0x1234] == parser.parse(b"4")

# TODO: above case is debatable, should probably wait for separator to consider chunked message to be valid