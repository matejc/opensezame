import string


class IPv4Range(object):

    def __init__(self, ip_range):
        self._range = ()
        parts = self._parse_parts(ip_range)
        self._range = self._parse_range(parts)

    def _parse_parts(self, ip_range):
        parts = string.split(ip_range, '.')
        parts = [string.strip(p) for p in parts]
        if not len(parts) == 4:
            raise Exception("Not a valid ip or range '{0}'.".format(ip_range))
        return parts

    def _parse_range(self, parts):
        ip_range = []
        for part in parts:
            ip_range.append(
                self._split_range(part)
            )
        return tuple(ip_range)

    def _split_range(self, part):
        if part in ['*', '-']:
            return (0, 255)

        if part[0] == '-':
            return (0, int(part[1:]))

        elif part[-1] == '-':
            return (int(part[:-1]), 255)

        else:
            pos = string.find(part, '-')
            if pos == -1:
                return int(part)
            else:
                return (
                    int(part[:pos]),
                    int(part[pos + 1:])
                )

    def _part_in_range(self, ip_part, ip_range):
        if isinstance(ip_range, int):
            return ip_part == ip_range
        else:
            return ip_part >= min(ip_range) and ip_part <= max(ip_range)

    def _in_range(self, address):
        ip_parts = [int(p) for p in self._parse_parts(address)]

        for i in range(len(self._range)):
            if not self._part_in_range(
                ip_parts[i], self._range[i]
            ):
                return False

        return True

    def __contains__(self, address):
        try:
            return self._in_range(address)
        except Exception as e:
            print e.message
            return False

    def __str__(self):
        return str(self._range)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        "Check if address is in range, works only for IPv4"
    )

    parser.add_argument("address", help="IPv4 address.")
    parser.add_argument(
        "ranges", metavar="range", nargs="+", help="IPv4 ranges."
    )

    args = parser.parse_args()

    for r in args.ranges:
        print "{0} in {1} == {2}".format(
            args.address,
            r,
            args.address in IPv4Range(r)
        )
