#coding = utf-8

__author__ = 'zhxfei'


def badge_process(badge):
    desc = [info['description'] for info in badge]
    return ','.join(desc) if len(desc) == 1 else desc

