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
    result = result.to_eng_string()
    if result.endswith(".0"):
        result = result.replace(".0", "")
    return result


def process_operator(oper):
    stored_operator = cache.get("oper")
    a = cache.get("a")
    b = cache.get("b")
    if stored_operator:
        if not b:
            cache.set("oper", oper)
            return a
        elif a and b:
            a = arithmetic_operations(a, b, stored_operator)
            cache.set("a", a)
            cache.set("oper", oper)
            cache.delete("b")
            return a
    else:
        if a:
            if a.endswith(".") or a in "-":
                return a
            elif a in "-" and a not in oper:
                cache.delete("a")
                return "0"
            else:
                cache.set("oper", oper)
                return a
        elif not a:
            if oper in "-":
                cache.set("a", oper)
                return oper
            return "0"


# def process_digit(digit):
#     a = cache.get("a")
#     b = cache.get("b")
#     operator = cache.get("oper")
#     if operator and b:
#         if digit in ".":
#             if digit in b:
#                 return b
#             else:
#                 b += digit
#                 cache.set("b", b)
#                 return b
#         else:
#             b += digit
#             cache.set("b", b)
#             return b
#     elif operator and not b:
#         if digit in ".":
#             b = "0" + digit
#             cache.set("b", b)
#             return b
#         else:
#             b = digit
#             cache.set("b", b)
#             return b
#     elif a and not operator:
#         if digit in "." and digit in a:
#                 return a
#         elif digit in "." and a in "-":
#                 return a
#         else:
#             a += digit
#             cache.set("a", a)
#             return a
#     elif not a:
#         if digit in ".":
#             a = "0" + digit
#             cache.set("a", a)
#             return a
#         else:
#             a = digit
#             cache.set("a", a)
#             return a

def process_digit(digit):
    a = cache.get("a")
    b = cache.get("b")
    operator = cache.get("oper")
    if operator:
        pass
    else:
        pass


def process_command(command):
    if command in "c":
        cache.clear()
        return "0"
    elif command in "=":
        a = cache.get("a")
        b = cache.get("b")
        stored_operator = cache.get("oper")
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
