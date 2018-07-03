from datetime import datetime

__FMT_STRS = ['{}{}{}'.format('%Y-%m-%dT%H:%M:%S', m, z)
              for m in ('', '.%s')
              for z in ('Z', '+0000', '+00:00', '-0000', '-00:00')]
            

def iso_parse(date_str: str) -> datetime:
    for fmt_str in __FMT_STRS:
        try:
            return datetime.strptime(date_str, fmt_str)
        except ValueError:
            pass

    raise ValueError('Date had bad format: {}'.format(date_str))
