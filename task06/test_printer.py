#!/usr/bin/env python3
import pytest
from printer import *
import textwrap


def test_conditional_if_is_true_list_is_none():
    assert Conditional(
        Number(1), None, []
    ).accept(PrettyPrint()) == 'if (1) {\n}'


def test_conditional_if_if_true_list_is_not_none():
    assert Conditional(
        Number(1), [Print(Number(2))], [Print(Number(3))]
    ).accept(PrettyPrint()) == textwrap.dedent('''\
        if (1) {
            print 2;
        } else {
            print 3;
        }''')


def test_function_definition():
    assert FunctionDefinition(
        'foo', Function([], [])
    ).accept(PrettyPrint()) == 'def foo() {\n}'


def test_print():
    assert Print(
        Number(1)
    ).accept(PrettyPrint()) == 'print 1'


def test_read():
    assert Read('x').accept(PrettyPrint()) == 'read x'


def test_number():
    assert Number(2).accept(PrettyPrint()) == '2'


def test_reference():
    assert Reference('x').accept(PrettyPrint()) == 'x'


def test_bin_operation():
    add = BinaryOperation(Number(2), '+', Number(3))
    assert BinaryOperation(
        Number(1), '*', add
    ).accept(PrettyPrint()) == '(1) * ((2) + (3))'


def test_un_operation():
    assert UnaryOperation(
        '-', Number(111)
    ).accept(PrettyPrint()) == '-(111)'


def test_function_call():
    assert FunctionCall(
        Reference('foo'), [Number(1), Number(2), Number(3)]
    ).accept(PrettyPrint()) == 'foo(1, 2, 3)'


def test_all(capsys):
    pretty_print(FunctionDefinition('main', Function(['arg1'], [
        Read('x'),
        Print(Reference('x')),
        Conditional(
            BinaryOperation(Number(2), '==', Number(3)),
            [
                Conditional(Number(1), [], [])
            ],
            [
                FunctionCall(Reference('exit'), [
                    UnaryOperation('-', Reference('arg1'))
                ])
            ],
        ),
    ])))
    expected = textwrap.dedent('''\
        def main(arg1) {
            read x;
            print x;
            if ((2) == (3)) {
                if (1) {
                }
            } else {
                exit(-(arg1));
            }
        }
    ''')

    assert capsys.readouterr().out == expected


if __name__ == '__main__':
    pytest.main()
