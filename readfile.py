def read_from_file(filename):
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        i = 0

        m = int(lines[i].split("=")[1])
        i += 1

        n = list(map(int, lines[i].split("=")[1].split()))
        i += 1

        if lines[i] != "c =":
            raise Exception("Очікується 'c ='")
        i += 1

        c = []
        for _ in range(m):
            row = list(map(float, lines[i].split()))
            if len(row) != m:
                raise Exception("Неправильний рядок у матриці C")
            c.extend(row)
            i += 1

        if lines[i] != "r =":
            raise Exception("Очікується 'r ='")
        i += 1

        r = []
        for _ in range(m):
            row = list(map(float, lines[i].split()))
            if len(row) != m:
                raise Exception("Неправильний рядок у матриці R")
            r.extend(row)
            i += 1

        t = float(lines[i].split("=")[1])
        i += 1

        d = float(lines[i].split("=")[1])

        return m, n, c, r, t, d, None

    except Exception as e:
        return None, None, None, None, None, None, str(e)