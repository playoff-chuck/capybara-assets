import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)
rep("""def db():
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory = sqlite3.Row
    return c
""", """class _DB:
    # sqlite3's own "with conn" only commits/rolls back and never closes:
    # every request leaked a file handle until the 1024 limit was hit.
    def __enter__(self):
        self.c = sqlite3.connect(DB, timeout=10)
        self.c.row_factory = sqlite3.Row
        return self.c
    def __exit__(self, et, ev, tb):
        try:
            if et is None:
                self.c.commit()
            else:
                self.c.rollback()
        finally:
            self.c.close()
        return False

def db():
    return _DB()
""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
