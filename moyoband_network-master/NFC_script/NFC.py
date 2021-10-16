from pn532pi import Pn532I2c,Pn532, pn532
import time
import binascii

i2c = Pn532I2c(1)
nfc = Pn532(i2c)

key = bytearray([0xf7,0x9f,0xcb,0xa6])

def setup():
	nfc.begin()
	a = nfc.getFirmwareVersion()
	print("Firmware version: ",(a >> 16) & 0xFF,".",(a >> 8) & 0xFF)
	nfc.setPassiveActivationRetries(0xFF)
	nfc.SAMConfig()
	print("Waiting for a card...\n\n");


def loop():
	success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
	if (success):
		if ( key == uid):
			print("#########This card is key!#########\n")
			print("UID Value: {}\n".format(binascii.hexlify(uid)))
			print("###################################")
			time.sleep(2)
			return True
		else:
			print("Found a card!")
			print("UID Length: {:d}".format(len(uid)))
			print("UID Value: {}\n".format(binascii.hexlify(uid)))
        		# Wait 1 second before continuing
			time.sleep(1)
			return True

if __name__ == '__main__':
	setup()
	found = loop()

	while 1:
		found = loop()
