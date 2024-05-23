#!/usr/bin/env python3
# a monadic parser
from typing import Any, Callable, Tuple, Generator
from functools import wraps


class Context:
    def __init__(self, s="", pos=0):
        self.s = s.strip()
        self.pos = pos

    def at(self):
        if self.pos >= len(self.s):
            return None
        return self.s[self.pos]

    def pick(self) -> str:
        i = self.at()
        if i is None:
            raise ParsingError("Error", self)
        return i

    def next(self):
        return Context(self.s, self.pos+1)

    def copy(self):
        return Context(self.s, self.pos)

    def __repr__(self):
        line_no = 0
        cols = 0
        last_line = ""
        for line in self.s.split("\n"):
            line_no += 1
            if self.pos < cols + len(line) + 1:
                # hit the line
                return f"{line_no}:{self.pos - cols + 1}: {line}"
            cols += len(line) + 1  # including the ending \n
            last_line = line
        line_no -= 1
        f"{line_no}:{len(last_line)+1}: {last_line}"

    def rest_str(self):
        return self.s[self.pos:]


class ParsingError(Exception):
    pass


ParserF = Callable[[Context], Tuple[Any, Context]]


class Parser:
    def parse(self, context: Context) -> (Any, Context):
        return None, context

    def __or__(self, other: "Parser") -> "Parser":
        @FuncParser
        def result(context: Context):
            try:
                return self.parse(context)
            except ParsingError:
                return other.parse(context)

        return result

    @staticmethod
    def ret(data):
        @FuncParser
        def r(context):
            return data, context
        return r

    def bind(self, f: Callable[[Any], "Parser"]) -> "Parser":
        @FuncParser
        def bound(context):
            a, context = self.parse(context)
            return f(a).parse(context)
        return bound

    @staticmethod
    def pick() -> "Parser":
        @FuncParser
        def parse(context):
            return context.pick(), context
        return parse

    @staticmethod
    def next() -> "Parser":
        @FuncParser
        def parse(context):
            return context, context.next()
        return parse


class FuncParser(Parser):
    def __init__(self, f: ParserF):
        self.f = f

    def parse(self, context: Context) -> (Any, Context):
        return self.f(context)


def reduce(g) -> Parser:
    try:
        m_a = g.__next__()
    except StopIteration as err:
        return err.value

    return m_a.bind(lambda a: reduce(g.partial_apply(a)))


def do(f: Callable[..., Generator[Parser, Any, Parser]]) -> Parser:
    @wraps(f)
    @FuncParser
    def parse(context: Context):
        class _Generator:
            class _Null:
                pass

            def __init__(self, generator):
                self._generator = generator
                self._x = _Generator._Null

            def __next__(self):
                if self._x is not _Generator._Null:
                    x = self._x
                    self._x = _Generator._Null
                    return self._generator.send(x)
                return next(self._generator)

            def __iter__(self):
                return self

            def send(self, x):
                return self._generator.send(x)

            def partial_apply(self, x):
                self._x = x
                return self

            def __repr__(self):
                return f"Generator {self._generator.__repr__()}"
        return reduce(_Generator(f())).parse(context)
    return parse


class Sat(Parser):
    def __init__(self, p):
        self.p = p

    def parse(self, context: Context):
        ch = context.pick()
        if self.p(ch):
            return ch, context.next()
        raise ParsingError(f"Unexpected Char: {ch}", context)


class Char(Parser):
    def __init__(self, c):
        self.c = c

    def parse(self, context: Context):
        return Sat(lambda x: x == self.c).parse(context)


class String(Parser):
    def __init__(self, s):
        self.s = s

    def parse(self, context: Context):
        for ch in self.s:
            _, context = Char(ch).parse(context)
        return self.s, context


class Many(Parser):
    def __init__(self, p):
        self.p = p

    def parse(self, context: Context):
        return (many1(self.p) | self.ret([])).parse(context)


def many1(p) -> Parser:
    @do
    def m():
        x = yield p
        xs = yield Many(p)
        return Parser.ret([x] + xs)
    return m


@FuncParser
def space(context):
    return Many(Sat(lambda x: x in " \t\n\r")).parse(context)


def token(p):
    @do
    def m():
        a = yield p
        yield space
        return Many.ret(a)
    return m


class Symb(Parser):
    def __init__(self, s):
        self.s = s

    def parse(self, context: Context):
        return token(String(self.s)).parse(context)


def operator(pop, pn1, pn2):
    @do
    def result():
        n1 = yield pn1
        op = yield pop
        n2 = yield pn2
        return Parser.ret(op(n1, n2))
    return result


@FuncParser
def expr(context):
    return (addop(term, expr) | term).parse(context)


@FuncParser
def term(context):
    return (mulop(factor, term) | factor).parse(context)


@FuncParser
def factor(context):
    @do
    def m():
        yield Symb("(")
        n = yield expr
        yield Symb(")")
        return Parser.ret(n)
    return (digits | m).parse(context)


@FuncParser
def digits(context):
    one = Sat(lambda z: z in "1234567890.")
    x, context = token(many1(one)).parse(context)
    return eval("".join(x)), context


def addop(pn1, pn2):
    @do
    def plus():
        yield Symb("+")
        return Parser.ret(lambda a, b: a + b)

    @do
    def minus():
        yield Symb("-")
        return Parser.ret(lambda a, b: a - b)
    return operator(plus | minus, pn1, pn2)


def mulop(pn1, pn2):
    @do
    def times():
        yield Symb("*")
        return Parser.ret(lambda a, b: a * b)

    @do
    def divide():
        yield Symb("/")
        return Parser.ret(lambda a, b: a / b)
    return operator(times | divide, pn1, pn2)


def main():
    while True:
        line = input("> ")
        if line == "":
            break
        try:
            value, ctx = expr.parse(Context(line))
            if ctx.rest_str() != "":
                print("Extra input at: ", ctx)
            else:
                print(value)
        except ParsingError as e:
            print(e)


if __name__ == '__main__':
    main()

