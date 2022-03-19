import argparse

from tgbot.utils.cli import cli


def parse_args():
    parser = argparse.ArgumentParser(prog='Telegram Bot', description='Admin Telegram bot')
    parser.add_argument('-m', '--mode', dest='mode', required=True, type=str, default='polling',
                        help='Start mode (webhook or polling)')
    parser.add_argument('-c', '--certificate', dest='cert', required=False, type=str,
                        choices=('self-singer', 'verified',), default='self-singer',
                        help='SSL certificate type (self-singer or verified)')
    return parser.parse_args()


if __name__ == '__main__':
    argv = parse_args()
    cli(argv)
