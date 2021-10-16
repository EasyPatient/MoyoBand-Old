def read_rfid():
    # nfc.setup()

    # nfc_result = nfc.loop()
    a = ""
    nfc_result = bytearray([0xfa, 0x12, 0x73, 0xcb, 0xc2, 0x7e])

    output = ":".join([format(i, "x") for i in list(nfc_result)])

    return output
