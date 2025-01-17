Y = lambda f: (lambda x: x(x))(lambda x: f(lambda y: x(x)(y)))
