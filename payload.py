#!/usr/bin/python2 -O
#  -*- coding:utf-8 -*-

"""
    Set of scripts to open a website in multiple browser and retrieve data
    -- THIS SCRIPT WILL RUN ON THE "VICTIM" HOST (pushed by webshot.py)

    IDEA/TODO
       - multiple browser support
       - start/stop network capture
       - start/stop OS monitoring (process, registry changes...)

    Version: 0.0 - dev / poc Version

    Copyright: Autopsit (N-Labs sprl) 2017
"""
from selenium import webdriver

"""
    Main function
"""
def main():

    browsers = {
    #    "ie" : webdriver.Ie(),
        "firefox" : webdriver.Firefox(),
    }    

    # Take a screenshot with each browser
    for browser in browsers.keys():
    		browsers[browser].get("http://www.autopsit.com")
    		browsers[browser].save_screenshot("%s_screenshot.png" % browser)
    		browsers[browser].quit()
    return

"""
   Call main function
"""
if __name__ == "__main__":
    
    # Create an instance of the Analysis class (called "base") and run main 
    main()

# That's all folks ;)
