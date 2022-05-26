""" Clase encargada de comprobar cuestiones relacionada con la escala de Fujita ampliada """


class FujitaScaleHelper:

    """ Velocidades minimas y maximas en MPH para la Escala de Fujita Ampliada (EF)"""
    EF0_MIN_SPEED = 65
    EF0_MAX_SPEED = 85
    EF1_MIN_SPEED = 86
    EF1_MAX_SPEED = 110
    EF2_MIN_SPEED = 111
    EF2_MAX_SPEED = 135
    EF3_MIN_SPEED = 136
    EF3_MAX_SPEED = 165
    EF4_MIN_SPEED = 166
    EF4_MAX_SPEED = 200
    EF5_MIN_SPEED = 201

    """ Metodo de la clase FujitaScaleHelper encargado de comprobar si una velocidad dada se corresponde 
    con la contemplada para dicha escala """
    def check_speed_by_fujita_scale(self, value, scale):
        if scale == "EF0" and self.EF0_MIN_SPEED <= value <= self.EF0_MAX_SPEED:
            return True
        elif scale == "EF1" and self.EF1_MIN_SPEED <= value <= self.EF1_MAX_SPEED:
            return True
        elif scale == "EF2" and self.EF2_MIN_SPEED <= value <= self.EF2_MAX_SPEED:
            return True
        elif scale == "EF3" and self.EF3_MIN_SPEED <= value <= self.EF3_MAX_SPEED:
            return True
        elif scale == "EF4" and self.EF4_MIN_SPEED <= value <= self.EF4_MAX_SPEED:
            return True
        elif scale == "EF5" and value >= self.EF5_MIN_SPEED:
            return True
        return False

    """ Metodo de la clase FujitaScaleHelper encargado de proporcionar la velocidad media de una escala dada """
    def get_speed_by_fujita_scale(self, scale):
        if scale == "EF0":
            return (self.EF0_MIN_SPEED + self.EF0_MAX_SPEED) / 2
        elif scale == "EF1":
            return (self.EF1_MIN_SPEED + self.EF1_MAX_SPEED) / 2
        elif scale == "EF2":
            return (self.EF2_MIN_SPEED + self.EF2_MAX_SPEED) / 2
        elif scale == "EF3":
            return (self.EF3_MIN_SPEED + self.EF3_MAX_SPEED) / 2
        elif scale == "EF4":
            return (self.EF4_MIN_SPEED + self.EF4_MAX_SPEED) / 2
        elif scale == "EF5":
            return self.EF5_MIN_SPEED
