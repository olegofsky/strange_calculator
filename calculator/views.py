# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache
from decimal import Decimal

OPERATORS = ("/", "*", "-", "+")
DIGITS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.')
COMMAND = ("=", "c")


def main(request):
    cache.clear()
    return render_to_response('index.html', context_instance=RequestContext(request))


def arithmetic_operations(x, y, oper):
    str_x = "Decimal(\"%s\")" % x
    str_y = "Decimal(\"%s\")" % y
    result = eval(" ".join([str_x, oper, str_y]))
    return result.to_eng_string().replace(".0", "")


def process_operator(oper):
    stored_operator = cache.get("oper")
    a = cache.get("a")
    b = cache.get("b")
    if stored_operator:
        if not b:
            cache.set("oper", oper)
            return a
        elif a:
            a = arithmetic_operations(a, b, stored_operator)
            cache.set("a", a)
            cache.set("oper", oper)
            cache.delete("b")
            return a
    else:
        if a:
            if a.endswith(".") or a == "-":
                return a
            else:
                cache.set("oper", oper)
                return a
        elif not a:
            if oper in "-":
                cache.set("a", oper)
                return oper
            else:
                cache.set("a", "0")
                return "0"


def process_digit(digit):
    a = cache.get("a")
    b = cache.get("b")
    operator = cache.get("oper")
    if operator and b:
        if digit in ".":
            if digit in b:
                return b
            else:
                b += digit
                cache.set("b", b)
                return b
        else:
            b += digit
            cache.set("b", b)
            return b
    elif operator and not b:
        if digit in ".":
            b = "0" + digit
            cache.set("b", b)
            return b
        else:
            b = digit
            cache.set("b", b)
            return b
    elif a and not operator:
        if digit in "." and digit in a:
                return a
        elif digit in "." and a in "-":
                return a
        else:
            a += digit
            cache.set("a", a)
            return a
    elif not a:
        if digit in ".":
            a = "0" + digit
            cache.set("a", a)
            return a
        else:
            a = digit
            cache.set("a", a)
            return a


# def process_digit(digit):
#     a = cache.get("a")
#     b = cache.get("b")
#     operator = cache.get("oper")
#     if operator:
#         pass
#     else:
#         pass


def process_command(command):
    if command == "c":
        cache.clear()
        return "0"
    elif command == "=":
        a = cache.get("a")
        b = cache.get("b")
        stored_operator = cache.get("oper")
        if not a:
            return "0"
        elif not b:
            return a
        elif b.replace("0", "") == ".":
            cache.clear()
            return "Error"
        else:
            a = arithmetic_operations(a, b, stored_operator)
            cache.set("a", a)
            return a


def ajax(request):
    input_character = request.GET.get('input_character')
    if input_character in OPERATORS:
        result = process_operator(input_character)
    elif input_character in DIGITS:
        result = process_digit(input_character)
    elif input_character in COMMAND:
        result = process_command(input_character)
    return HttpResponse(result)
