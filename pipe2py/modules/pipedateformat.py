# pipedateformat.py
#

import time
from datetime import datetime
from pipe2py.lib.dotdict import DotDict
from pipe2py import util


def pipe_dateformat(context=None, _INPUT=None, conf=None, **kwargs):
    """This source formats a date.

    Keyword arguments:
    context -- pipeline context
    _INPUT -- source generator
    conf:
        format -- date format

    Yields (_OUTPUT):
    formatted date
    """
    conf = DotDict(conf)
    date_format = conf.get('format', **kwargs)

    for item in _INPUT:
        s = item
        if isinstance(s, basestring):
            for df in util.ALTERNATIVE_DATE_FORMATS:
                try:
                    s = datetime.strptime(s, df).timetuple()
                    break
                except:
                    pass
            else:
                # todo: raise an exception: unexpected date format
                pass
        try:
            s = time.strftime(date_format, s)   # todo: check all PHP formats are covered by Python
        except TypeError:
            #silent error handling e.g. if item is not a date
            continue

        yield s
