import argparse

from tgbot.utils.cli import cli


def parse_args():
    parser = argparse.ArgumentParser(prog='Telegram Bot', description='Admin Telegram bot')
    parser.add_argument('-m', '--mode', dest='mode', required=True, type=str, default='polling',
                        help='Start mode (webhook or polling)')
    return parser.parse_args()

# import os
# import pwd
#
# import configargparse
#
# parser = configargparse.ArgumentParser(auto_env_var_prefix='APP_')
# parser.add_argument('-u', '--user', type=pwd.getpwnam)
# parser.add_argument('-s', '--cookie-secret')
#
# if __name__ == '__main__':
#     arguments = parser.parse_args()
#     os.environ.clear()
#     cli(arguments)


if __name__ == '__main__':
    argv = parse_args()
    cli(argv)
