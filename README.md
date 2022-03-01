# MagneticTimeCrystals

## Requirements

```sh
pip3 install -r requirements.txt
```
## Running Models
Choose a model/simulation from the `models/` folder.
* `ising_model_temp_v_magnetisation.py` -- a plot of final magnetisations at a range of temperatures
* `ising_model_video.py` -- a video visualisation of the evolution of the system

# TODO

* Add a magnetic field that favours either spin up or down
* Add ability to export just graphs where parameters change e.g. Magnetisation vs Temperature - would need to find the number of cycles until it roughly reaches equilibrium, this could be used to find critical temperature etc.
* Make independent plotting function outside of simulate()