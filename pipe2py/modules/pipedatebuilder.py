# pipedatebuilder.py
#

from pipe2py import util
from pipe2py.lib.dotdict import DotDict
from datetime import datetime, timedelta


def pipe_datebuilder(context=None, _INPUT=None, conf=None, **kwargs):
    """This source builds a date and yields it forever.

    Keyword arguments:
    context -- pipeline context
    _INPUT -- XXX
    conf:
        DATE -- date

    Yields (_OUTPUT):
    date
    """
    conf = DotDict(conf)

    for item in _INPUT:
        date = util.get_value(conf['DATE'], DotDict(item), **kwargs).lower()

        if date.endswith(' day') or date.endswith(' days'):
            count = int(date.split(' ')[0])
            date = (datetime.today() + timedelta(days=count)).timetuple()
        elif date.endswith(' year') or date.endswith(' years'):
            count = int(date.split(' ')[0])
            date = datetime.today().replace(year = datetime.today().year + count).timetuple()
        elif date == 'today':
            date = datetime.today().timetuple()
        elif date == 'tomorrow':
            date = (datetime.today() + timedelta(days=1)).timetuple()
        elif date == 'yesterday':
            date = (datetime.today() + timedelta(days=-1)).timetuple()
        elif date == 'now':  # todo: is this allowed by Yahoo?
            date = datetime.now().timetuple()  # better to use utcnow?
        else:
            for df in util.ALTERNATIVE_DATE_FORMATS:
                try:
                    date = datetime.strptime(date, df).timetuple()
                    break
                except:
                    pass
            else:
                pass

            # todo: raise an exception: unexpected date format
        yield date
