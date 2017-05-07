# MusiQ
## Spice your party up with a collaborative music queue

### About

This is a small tool to collaborate playlist generation during your small parties.
It is currently a work in progress and will hopefully be more or less worked out by
May 12th.

### Dependencies

* Python3.x (We will never support Python 2)
* A running installation of MPD or Mopidy (or any other MPD compliant Server)
* Flask
* python-mpd2

### Installation

For now simply run `pip install -r requirements.txt` and run the (currently named)
`rest_interface.py` and you should be up in running.

### Usage

(Start Mopidy)
```
export FLASK_APP=/path/to/rest_interface.py
flask run --host=0.0.0.0
```
