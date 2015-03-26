# lifx
LIFX Python API

My shot at a Python API for the LIFX Bulbs.

###Features:
* Continues to send data until and acknowledge packet is received, up to max_retries (=5)
* Searches and creates a set of bulbs

###Simple Usage:
```python
import lifx
import time

network = lifx.Network()
network.search()

light = network.get_light_by_label('Lounge')
light.off()
time.sleep(5)
light.on()

light.set_light_state(stream=1, hue=30000, saturation=40000, brightness=20000, kelvin=4000, duration=1):

```

###Based on the work of:
* https://github.com/sharph/lifx-python
* https://github.com/derkarnold/pylifx
* https://github.com/arrian/lifx-python
