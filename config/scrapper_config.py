def check_hsn(hsn):
    if ((len(str(hsn)) % 2) != 0):
        hsn = '0' + str(hsn)
    else:
        return hsn