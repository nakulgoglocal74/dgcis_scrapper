def check_hsn(hsn):
    hsn = str(hsn)
    if ((len(hsn) % 2) != 0):
        hsn = '0' + str(hsn)
    return hsn