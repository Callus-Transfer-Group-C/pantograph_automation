# Likely will need to write a connection check for the raspberry pi before
# any testing.
#
# Also, this will be heavily dependant on the rpi version, as pi5 has different
# gpio control than earlier versions.
#
# Long story short, whatever we write will not be backwards compatible. And that's okay!!

from pantograph_control import drivers

motor = drivers.Servo()

motor.position(65)