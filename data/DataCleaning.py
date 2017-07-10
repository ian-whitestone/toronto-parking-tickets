import config
import logging as log
import numpy

def check_int(**kwargs):
    """Function to check if the field is an integer and convert if necessary"""
    int_check = isinstance(kwargs['val'], int )
    val = kwargs['val']
    if int_check == False:
        try:
            val = int(kwargs['val'])
        except Exception as e:
            log.debug('Unable to convert %s to an integer due to error %s' %
            (val, e))
            val = None
    return val

def check_varchar(**kwargs):
    """Function to check if the field is the correct length and trunctuate if necessary"""
    val = kwargs['val']
    try:
        cleaned_val = str(val)[0:kwargs['length']]
        cleaned_val = cleaned_val.replace('\\','')
    except Exception as e:
        log.debug('Unable to convert %s to a string due to error %s' %
                (val, e))
        cleaned_val = None
    return cleaned_val

def check_text(**kwargs):
    """Function to check if the field is a strubg"""
    val = kwargs['val']
    try:
        cleaned_val = str(val)
        cleaned_val = cleaned_val.replace('\\','')
    except Exception as e:
        log.debug('Unable to convert %s to a string due to error %s' %
                (val, e))
        cleaned_val = None
    return cleaned_val

def check_char(**kwargs):
    """Function to check if the field is the correct length and trunctuate if necessary
        Also checks if it is a string and converts if necessary.
    """

    val = kwargs['val']
    str_check = isinstance(kwargs['val'], ( str, basestring ) )
    val = kwargs['val']
    if str_check == False:
        try:
            val = str(kwargs['val'])
            val = val.replace('\\','')
        except Exception as e:
            log.debug('Unable to convert %s to a string due to error %s' %
                    (val, e))
            return None
    cleaned_val = val[0:kwargs['length']]
    return cleaned_val

def do_none(**kwargs):
    return kwargs['val']
