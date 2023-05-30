import argparse

import scaner


def get_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Host")
    parser.add_argument('-t', action="store_true", help="Enables TCP")
    parser.add_argument('-u', action="store_true", help="Enables UDP")
    parser.add_argument("-p", dest="ports", nargs=2, metavar=('N1', 'N2'), help="Range of scanning ports")
    return parser


def main():
    parser = get_argparse()
    args = parser.parse_args()

    scaner.start_scaner(args.host, 'u' if args.u else 't', args.ports)


if __name__ == '__main__':
    main()
