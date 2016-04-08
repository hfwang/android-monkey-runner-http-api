# HTTP API for Android Monkeyrunner

Connect your phone to your computer, and interact with it over HTTP.

## Usage

First install dependencies:

```bash
$ ./pip_install.sh
```

Then use monkey runner to start the server:

```bash
$ /path/to/android-sdk/tools/monkeyrunner server.py
```

This will start the monkeyrunner server on port 8080, you can see what the current screen looks like by loading http://localhost:8080/screenshot

Otherwise you can interact with your phone via HTTP POSTs.

TODO: Add more documentation
