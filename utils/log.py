#!/usr/bin/env python
from xtermcolor import colorize

def enum(**enums):
    return type('Enum', (), enums)

ansi_color= enum(
    green=2,
    blue = 69,
    red = 52,
    cyan=30,
    purple=26,
    orange=166,
    light_green=154
    )

def log(message, type = None, ansi= ansi_color.blue, tag = ''):
    
    if type == 'info':
        print colorize(message, ansi = ansi_color.blue)
    elif type == 'success':
        print colorize(message, ansi = ansi_color.green)
    elif type == 'warning':
        print colorize(message, ansi = ansi_color.orange)
    elif type == 'error':   
        print colorize(message, ansi = ansi_color.red)
    elif type == 'custom':
        print colorize(message, ansi = ansi)
    else:
        print message

def green(message):
    print colorize(message, ansi = ansi_color.green)
     
def red(message):
    print colorize(message, ansi = ansi_color.red)

def blue(message):
    print colorize(message, ansi = ansi_color.blue)

def orange(message):
    print colorize(message, ansi = ansi_color.orange)