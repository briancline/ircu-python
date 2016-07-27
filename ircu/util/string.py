def irc_split(line):
    """Split an event line, with any trailing free-form text as one item."""
    try:
        rest_pos = line.index(' :')
        bits = line[0:rest_pos].split(' ') + [line[rest_pos + 2:]]
    except ValueError:
        bits = line.split(' ')
    return bits


def irc_buffer_lines(buf):
    eol_idx = buf.find('\n')
    while eol_idx >= 0:
        line = buf[0:eol_idx]
        line = line.rstrip('\r\n')
        buf = buf[eol_idx + 1:]
        eol_idx = buf.find('\n')
        yield buf, line
