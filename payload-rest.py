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
import base64
from selenium import webdriver
from bottle import Bottle, route, run, template # REST-API for client / server communication

app = Bottle()

"""
    Take save_screenshot
"""
@app.route("/browse/<b64url>")
def browse(b64url):
    url = base64.b64decode(b64url)
    print("Requested to browse: %s" % url)
    
    browsers = {
    #    "ie" : webdriver.Ie(),
        "firefox" : webdriver.Firefox(),
    }    

    # Take a screenshot with each browser
    for browser in browsers.keys():
            print("Browser %s about to start!\n" % browser)
            browsers[browser].get(url)
            browsers[browser].save_screenshot("%s_screenshot.png" % browser)
            browsers[browser].quit()
            print("Browser %s finished + screenshot saved!\n" % browser)

    return "Done"

run(app, host='0.0.0.0', port=8080, debug=True)
# That's all folks ;)