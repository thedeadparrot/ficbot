Ficbot 
=======

[![Travis Build Status](https://travis-ci.org/thedeadparrot/ficbot.svg?branch=master)](https://travis-ci.org/thedeadparrot/ficbot)

Model Generation
----------------
1. `make install_dependencies`
2. Run `python generation_script.py` to generate text

Scraping
--------
1. install python-dev, libssl-dev and libffi-dev, libxml2-dev libxslt1-dev
2. `pip install -r requirements.txt`

TODO:
- get all this heroku-ized - config variables set by environment rather than config file
- get things scheduled
- seed the Tumblr bot with better starting text
- tests
- documentation
- write a simple flask frontend?
