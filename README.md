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

- [ ] Custom starting shapes of a particular spin e.g. stars/circles
- [ ] Implement oscillations in time (because it is a time crystal)
- [ ] Add ability to simultaneously flip a certain amount of spins  
- [x] Add a magnetic field that favours either spin up or down
- [x] Add ability to export just graphs where parameters change e.g. Magnetisation vs Temperature - would need to find the number of cycles until it roughly reaches equilibrium, this could be used to find critical temperature etc.
- [x] Make independent plotting function outside of simulate()