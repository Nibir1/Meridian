# Mocks for the Input/Output definitions
class MessageTextInput:
    def __init__(self, name, display_name=None, value=None, required=False, info=None):
        self.name = name
        self.value = value

class IntInput:
    def __init__(self, name, display_name=None, value=0):
        self.name = name
        self.value = value

class Output:
    def __init__(self, display_name, name, method):
        self.name = name
        self.method = method