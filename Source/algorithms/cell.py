class Cell:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.value = -1
        self.element = []
        self.is_discovered = False
        self.is_breeze = False
        self.is_stench = False
        self.is_whiff = False
        self.is_glow = False
        self.is_scream = False
        self.is_safe = False
        self.direction = None

    # Getters
    def get_discovery(self):
        return self.is_discovered

    def get_breeze(self):
        return self.is_breeze

    def get_stench(self):
        return self.is_stench

    def get_whiff(self):
        return self.is_whiff

    def get_glow(self):
        return self.is_glow

    def get_scream(self):
        return self.is_scream

    def get_safe(self):
        return self.is_safe

    # Setters
    def set_discovery(self):
        self.is_discovered = True

    def set_breeze(self):
        self.is_breeze = True

    def set_stench(self):
        self.is_stench = True

    def set_whiff(self):
        self.is_whiff = True

    def set_glow(self):
        self.is_glow = True

    def set_scream(self):
        self.is_scream = True

    def set_safe(self):
        self.is_safe = True

    # Removers
    def remove_discovery(self):
        self.is_discovered = False

    def remove_breeze(self):
        self.is_breeze = False

    def remove_stench(self):
        self.is_stench = False

    def remove_whiff(self):
        self.is_whiff = False

    def remove_glow(self):
        self.is_glow = False

    def remove_scream(self):
        self.is_scream = False

    def remove_safe(self):
        self.is_safe = False
