#!/usr/bin/env python3
# vim:tabstop=4:shiftwidth=4:expandtab:ai:
import sys, warnings
import requests

warnings.simplefilter('always')


def main(argv=sys.argv):
    if len(argv) < 3 and len(argv) > 0:
        request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'
        response = requests.post(request_url.format("tableFiller.php"), 
                             data={'tab':'7', 'gp_id':f'{argv[1]}'})
        print(response.text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <id>\n".format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())



