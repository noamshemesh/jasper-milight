# jasper-milight
Jasper module to turn on, turn off, set to white and dim your lights. supporting all 4 groups

#### INSTALLATION
1. clone this repository to a machine with [jasper](http://jasperproject.github.io/) installed
1. run `pip install -r jasper-milight/requirements.txt` to install requirements (you may need root privileges)
1. copy `jasper-milight/Light.py` to `$JASPER_HOME/client/modules` (replace $JASPER_HOME with jasper home if not set)

#### CONFIGURATION
1. add to your `~/.jasper/profile.yml` the following configuration:
   ```
   milight:
     ip: <your controller ip> [required]
     port: 8899
     wait_duration: 200
     bulb_type: ['rgbw']
   ```
written values are the defaults.
