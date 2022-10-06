# Building Optimization and Prediction 

The project aims at imporving the energy performance of an existing building by optimizing its design parameters and providing a tool that is able to predict
temperature and consumptions, using neural networks.

The following parameters are optimized, using NSGA-II genetic algorithm, in order to reduce the total consumption of the building:
- Insulation Thickness
- Air Changes per Hour (ACH)
- Window Shading Control
- Window Glazing
- 
Influx-DB was used as database and visualziation tool of the simulation data coming from EnergyPlus.  

Afterwards, the energy signature of the building was calculate through univariate and multivariate regression.

Future indoor temperature and building consumptions were predicted using the following models:
- Linear Kalman Filter
- Unscented Kalman Filter
- Artificial Neural Network
- LSTM Neural Network

TensorFlow was used as the library for neural networks creation and training.
