def allowed_extension(filename):
    ext=filename[-3:]
    extensions=['jpg','png','JPG','PNG','peg']
    if not ext in extensions:
        return False
    else:
        return True