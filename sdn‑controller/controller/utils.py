import hashlib

def watermark_ok(student_id="890302124", salt="NeoDDaBRgX5a9",
                 expected="c71113166c53deab112639414771caff4e55ae1eea2c8cf5b6a6dcb83bc33cc1"):
    return (hashlib.sha256((student_id+salt).encode()).hexdigest() == expected)
