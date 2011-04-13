#!/usr/bin/env python
'''
Slideshow Background Generator for Gnome 2.x
Nautilus script file.

Created on 12-04-2011

@author: michal@post.pl
@version: 0.0.2
@license: GPLv3

'''

import os
import sys

BACKGROUND_TMPL = '''<background>%s
</background>'''

START_TMPL = '''
  <starttime>
    <year>%d</year>
    <month>%02d</month>
    <day>%02d</day>
    <hour>%02d</hour>
    <minute>%02d</minute>
    <second>%02d</second>
  </starttime>'''

STATIC_TMPL = '''
  <static>
    <duration>%.2f</duration>
    <file>%s</file>
  </static>'''

TRANSITION_TMPL = '''
  <transition>
    <duration>%.2f</duration>
    <from>%s</from>
    <to>%s</to>
  </transition>'''

APP_TITLE = "Desktop Slideshow Generator"

def gen_background_xml(files, disp_time=3595.0, duration=5.0):
    '''
    Returns '<background>...' string
    files - list of file paths
    disp_time - how long (seconds) to display each picture
    duration - how long each picture transition take
    '''
    start = START_TMPL % (2000, 1, 1, 0, 0, 0)
    content = ''
    files.append(files[0])
    prev_file = None
    for curr_file in files:
        if prev_file:
            content += STATIC_TMPL % (disp_time, prev_file)
            content += TRANSITION_TMPL % (duration, prev_file, curr_file)
        prev_file = curr_file
    return BACKGROUND_TMPL % (start + content)


def error(msg):
    ''' write error message and quit '''
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)


def is_picture(file_path):
    ''' true iff file is a picture '''
    if file_path.lower().endswith('.jpg'):
        return True
    if file_path.lower().endswith('.jpeg'):
        return True
    return False
    

def get_files():
    ''' get list of files from nautilus-script env '''
    out = os.environ['NAUTILUS_SCRIPT_SELECTED_FILE_PATHS'].split('\n')
    out = [ elem for elem in out if is_picture(elem) ]
    return out


def set_background(file_path):
    ''' set gnome background '''
    key = '/desktop/gnome/background/picture_filename'
    cmd = 'gconftool-2 --set %s --type string "%s"' % (key, file_path)
    os.system(cmd)


def main():
    ''' main function for nautilus-script call '''
    files = get_files()
    xml = gen_background_xml(files, disp_time=10)
    xml_path = os.path.expanduser('~/.gnome2/slideshow background.xml')
    ofh = file(xml_path, 'w')
    ofh.write(xml)
    set_background(xml_path)
    ofh.close()

if __name__ == '__main__':
    main()
