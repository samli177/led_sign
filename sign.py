#!/usr/bin/python
#-*- coding: UTF-8 -*-
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-

import sys, getopt
import time
import alphasign

def main(argv):
    text = 'Welcome to MakersLink'
    port = '/dev/ttyUSB0'
    color = alphasign.colors.GREEN 
    mode = alphasign.modes.ROTATE
    init = False

    try:
        # FIXME: change to "require argument" for mode when implementing
        opts, args = getopt.getopt(argv,"t:o:mc:i",["text=","port=", "color=", "mode", "init"])
    except getopt.GetoptError:
        print 'sign.py -t <text> -o <port> -m <mode> -c <color>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'sign.py -t <text> -p <port> -m <mode> -c <color>'
            sys.exit()
        elif opt in ("-t", "--text"):
            text = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-m", "--mode"):
            mode = alphasign.modes.HOLD 
            # FIXME: map input-string to mode code
        elif opt in ("-c", "--color"):
            color = alphasign.colors.rgb(arg)
            # FIXME: map input-string to color code
        elif opt in ("-i", "--init"):
            init = True

    # debug prints
    print "Text:", text
    print "Port:", port
    print "Color:", color
    print "Mode:", mode


    # add color tag to text
    text = '%s' + text
    
    # replace special characters that sign can't handle
    text = text.replace(chr(195)+chr(165), chr(134))    #å
    text = text.replace(chr(195)+chr(164), chr(132))    #ä
    text = text.replace(chr(195)+chr(182), chr(148))    #ö
    text = text.replace(chr(195)+chr(133), chr(143))    #Å
    text = text.replace(chr(195)+chr(132), chr(142))    #Ä
    text = text.replace(chr(195)+chr(150), chr(153))    #Ö

    # connect to sign
    sign = alphasign.Serial(port)
    sign.connect()

    if init:
        print "Clearing memory"
        sign.clear_memory()
    
    # create logical objects to work with
    counter_str = alphasign.String(size=14, label="1")
    counter_txt = alphasign.Text(text % color, label="A", mode=mode)

    # allocate memory for these objects on the sign
    if init:
        print "Allocating memoty"
        sign.allocate((counter_str, counter_txt))

    # tell sign to only display the coutner text
    if init:
        print "Setting run sequence"
        sign.set_run_sequence((counter_txt,))

    # write objects
    print "Writing objects"
    for obj in (counter_str, counter_txt):
        sign.write(obj)

if __name__ == "__main__":
    main(sys.argv[1:])
