# !/usr/bin/env python3
import pytest
from model import *


def test_scope():
    a, b, c = object(), object(), object()
    parent = Scope()
    parent['foo'] = a
    parent['bar'] = b
    assert parent['bar'] == b


def test_scope_parent():
    a, b, c = object(), object(), object()
    parent = Scope()
    parent['foo'] = a
    parent['bar'] = b
    scope = Scope(parent)
    assert scope['bar'] == b


def test_scope_error():
    a, b, c = object(), object(), object()
    parent = Scope()
    parent['foo'] = abra    
    parent['bar'] = b
    scope = Scope(parent)
    with pytest.raises(KeyError):
        _ = scope['zoo']


def test_function_definition():
    scope = Scope()
    func = FunctionDefinition("foo", Function([], []))
    func.evaluate(scope)
    assert scope['foo']


def test_conditional():
    cond = Conditional(Number(0), [Number(0)], [Number(1)])
    scope = Scope()
    check = cond.evaluate(scope)
    assert check.value == 1


def test_print(capsys):
    scope = Scope()
    value = Print(Number(1))
    value.evaluate(scope)
    captured = capsys.readouterr()
    assert captured.out == '1\n'


def test_read(monkeypatch):
    scope = Scope()
    fun_name = Read('test_fun')
    monkeypatch.setattr('builtins.input', lambda: '0')
    result = fun_name.evaluate(scope)
    assert result.value == 0


def test_function_call(capsys):
    s = Scope()
    arg = [Print(BinaryOperation(Reference("a"), "*", Reference("b")))]
    operation1 = FunctionDefinition("func_name", Function(["a", "b"], arg))
    arg = [Number(10), BinaryOperation(Number(1), "+", Number(2))]
    operation2 = FunctionCall(Reference("func_name"), arg)
    operation1.evaluate(s)
    operation2.evaluate(s)
    assert capsys.readouterr().out == '30\n'


def test_reference():
    scope = Scope()
    scope['fun_name'] = 366
    assert Reference('fun_name').evaluate(scope) == 366


def test_binary_operation():
    scope = Scope()
    arg1 = Number(239)
    arg2 = Number(366)
    assert BinaryOperation(arg1, '+', arg2).evaluate(scope).value == 605


def test_unary_operation():
    scope = Scope()
    arg = Number(-366)
    assert UnaryOperation('-', arg).evaluate(scope).value == 366


def test_factorial():
    scope = Scope()
    condition = BinaryOperation(Reference('n'), '>', Number(1))
    is_true = [BinaryOperation(FunctionCall(
        Reference('factorial'), [BinaryOperation(Reference('n'), '-', Number(
            1))]), '*', Reference('n'))]
    is_false = [Number(1)]
    body = [Conditional(condition, is_true, is_false)]
    factorial = FunctionDefinition('factorial', Function(['n'], body))
    factorial.evaluate(scope)
    fact_6 = FunctionCall(Reference('factorial'), [Number(6)])

    result = fact_6.evaluate(scope).value
    assert result == 720


if __name__ == "__main__":
    pytest.main()
