class MessageParser():
    def __init__(self):
        self.buffer = bytearray(b"")

    def parse(self, byte_buffer):
        splitted = byte_buffer.split(b',')
        result = []
        if not len(splitted):
            # Nothing to process, return empty result
            return result

        if not len(splitted[0]):
            # Nothing before first separator, discard current buffer
            self.buffer.clear()

        if len(self.buffer):
            # Extend current buffer with more data
            self.buffer.extend(splitted[0])
            if len(self.buffer) == 4:
                # Now we have a complete message
                result.append(int(self.buffer.decode("ascii"), 16))
                self.buffer.clear()

        # Iterate over all valid messages and try to parse value as hex
        for msg in [x for x in splitted[1:] if len(x) == 4]:
            try:
                value = int(msg.decode("ascii"), 16)
                result.append(value)
            except ValueError:
                pass
        
        # Add incomplete message in the end of byte_buffer to local buffer (if it's empty)
        if not len(self.buffer) and len(splitted[-1]) != 4:
            self.buffer.extend(splitted[-1])

        return result