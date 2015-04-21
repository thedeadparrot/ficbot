FicBot
=======

[![Travis Build Status](https://travis-ci.org/thedeadparrot/ficbot.svg?branch=master)](https://travis-ci.org/thedeadparrot/ficbot)

I call it FicBot, but it really is generalizable to any sort of English (and possibly even non-English text). It's mostly a very simple implementation of using ngrams to generate text from a corpus of data and a chance for me to play around with a few different technologies. You can see it in action [on Twitter](https://twitter.com/generatedficbot), [on Tumblr](http://ficbot.tumblr.com/), and [on its own website](http://ficbot.herokuapp.com/).

Installation
-------------

First off, you're going to want to set up (at least one) [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) in order to run the code here. I highly recommend using `virtualenvwrapper` (which is mentioned in the article) as an easy interface for managing virtual environments.

Pull down this whole git repository using git clone:

```
git clone https://github.com/thedeadparrot/ficbot.git
```


Model Generation
----------------

To generate models, ensure that you have a directory at the top level named `corpus/` that contains all the `.txt` files you would like to use to train the model.

1. `make install_dependencies` to install all the dependencies.
2. Run `python generation_script.py -r` from the top level directory to generate the model and view some sample generated text. 
3. You can optionally do things like generate different types of models, feed in the starting text you want to use, generate more text than is the default, etc.


Bots
-----

There are two provided bots, a Twitter bot and a Tumblr bot. They are both extremely simple and will only post generated text to their own timelines. 

1. Set up apps on [Twitter](https://apps.twitter.com/) and [Tumblr](https://www.tumblr.com/oauth/apps) with OAuth credentials.
2. Make sure for all accounts that you have all four credentials you need: consumer key, consumer secret, access token, and access token secret. The consumer key and consumer secret belong to the app, but the access token and access token secret belong to the user. There are guides online on how to generate the access token and access token secret for Twitter if you need to.
3. Rename `config_sample.json` to `config.json` and fill in the `REPLACE ME` text with the credentials you have.
4. If you are running a Tumblr, make sure to fill in the `blog_name` field in `config.json` with the user name of the blog you want to update.
5. If you haven't generated the model file (`model.pkl`), make sure you have done so. `python generation_script.py -ro` will generate the model for you. You might get an error like `IOError: [Errno 2] No such file or directory: 'model.pkl'` if you don't.
5. Test out your bots by running `python twitterbot.py` or `python tumblrbot.py`.


Website
---------

The website is running on [Flask](http://flask.pocoo.org/), a nice Python microframework. Feel free to modify the templates in the `templates` directory or the static files in the `static` directory. The very tiny amount of server code lives in `web.py`.

To run locally:

1. Type in `guinicorn web:app` while in the top level directory.
2. View the website at `http://localhost:8000`
3. Click the `Generate Text` button to view it in action.


Tests
-----

I need to write more of them, but they are a thing that exists! You can view them in the `tests/` directory.

1. Make sure to grab the test dependencies with `make install_test_dependencies`
2. Run them with `make run_tests`.
