import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#here we try to implement a monodimensional Kalman filter where we try to infer
#the data inside the building though the realation: T_in(t) = T_in(t-1) - U[T_in(t-1) - T_out(t)]

#The T_in are the average temperature of the whole building, while the T_out is the average temp
#of Torre Pellice recorded over the years. To make the Kalman filter work, we have both mean and variance
#of T_out and we assume it collected by a sensor that has uncertainty = variance

#The model treats the temps as Gaussians and try to do a linear interpolation, but no good result is expected
#since the temperature is not a linear qt


df = pd.read_csv("hourly_mean.csv")

####### BUILDING PARAMETERS ###########
short_side_legth = 10.74
building_height = 8.2
long_side_length = 39.61
wall_area = short_side_legth*building_height*2 + long_side_length*building_height*2
U_val = 0.35 #W/m^2*K
#wall composition
brick_density = 1700 #Kg/m^3
brick_Cs = 800 #J/Kg*K
brick_thickness = 0.1 #m
XPS_density = 35 #Kg/m^3
XPS_Cs = 1400 #J/Kg*K
XPS_thickness = 0.35 #m 
concrete_density = 1400 #Kg/m^3
concrete_Cs = 1000 #J/Kg*K
concrete_thickness = 0.1 #m

brick_mass = brick_density*(wall_area*brick_thickness)
XPS_mass = XPS_density*(wall_area*XPS_thickness)
concrete_mass = concrete_density*(wall_area*concrete_thickness)

#%% Kalman filter with correct U-value and building parameters
building_mass = brick_mass + XPS_mass + concrete_mass
mean_Cs = (brick_Cs + XPS_Cs + concrete_Cs)/3

T_in = 7 #x
T_in_predict = np.random.uniform(0,1) #x_hat
T_in_real = np.random.uniform(0,1) #z
T_out = 4 #t
var_Tin = np.random.uniform(0,1) # P
var_Tin_predict = np.random.uniform(0,1) #P_hat
var_Tout = np.random.uniform(0,1)
Q = np.random.uniform(0,1) #Q will be a Gaussian variable resulting from the merging of T_out and T_in
y = 0

"""
Now the model for the themic exchange is:
    T_in(t) = T_in(t-1) + U_val*build_area*[T_in(t-1) - T_out(t)]/(building_mass*building_Cs/3600)
    U_val*build_area*[T_in(t-1) - T_out(t)] = (W/m^2*K)*m^2*K = W
    (building_mass*building_Cs) = Kg*(J/[Kg*K]) = J/K
    W = J/3600
"""

T_in_history = []
T_in_predict_history = []

for i in range(len(df)):
    #PREDICTION stage:
    T_in_predict = T_in - U_val*wall_area*(T_in - T_out)/(building_mass*mean_Cs/3600)
    var_Tout = df["Variance_Temperature_out"][i]
    Q = var_Tout*var_Tin/(var_Tout + var_Tin)
    var_Tin_predict = var_Tin + Q

    #UPDATE stage:
    T_in_real = df["Temperature_in"][i]
    y = T_in_real - T_in_predict
    K = var_Tin_predict/(var_Tout + var_Tin_predict)
    T_in = T_in_predict + K*y
    var_Tin = (1 - K)*var_Tin_predict
    
    #save data
    T_in_history.append(T_in)
    T_in_predict_history.append(T_in_predict)
    

plt.figure()
plt.plot(df["Temperature_in"], color = 'g', label = 'Real values')
plt.plot(T_in_history, color = 'r', label = 'Predict step')
plt.plot(T_in_predict_history, color = 'b', label = 'Update step')
#plt.plot(df["Temperature_in"], color = 'g', label = 'Real values')
plt.legend()
plt.xlabel('Time steps')
plt.ylabel('Temperature [C]')
plt.title("Kalman filter - T_in(t) - hourly prediction")
plt.show()

"""
NOTA: it's working, but there are some nans in the external temperature which has to be filtered
IMPORTANT: the filter has to be filtered over all the year to check the correct functionality, but it seems
working
"""

#%% Kalman filter pacco

#random initialization:
T_in = 16 #x
T_in_predict = np.random.uniform(0,1) #x_hat
T_in_real = np.random.uniform(0,1) #z
T_out = 4 #t
var_Tin = np.random.uniform(0,1) # P
var_Tin_predict = np.random.uniform(0,1) #P_hat
var_Tout = np.random.uniform(0,1)
Q = np.random.uniform(0,1) #Q will be a Gaussian variable resulting from the merging of T_out and T_in
y = 0

for i in range(len(df)):
    #PREDICTION stage:
    T_in_predict = T_in - U_val*(T_in - T_out)
    var_Tout = df["Variance_Temperature_out"][i]
    Q = var_Tout*var_Tin/(var_Tout + var_Tin)
    var_Tin_predict = var_Tin + Q

    #UPDATE stage:
    T_in_real = df["Temperature_in"][i]
    y = T_in_real - T_in_predict
    K = var_Tin_predict/(var_Tout + var_Tin_predict)
    T_in = T_in_predict + K*y
    var_Tin = (1 - K)*var_Tin_predict
    
    
################### NOTA:
"""
Il filtro al momento fa un po' cagare perhce' le variazioni di temperatura sono abbastanza grosse.
La relazione della variazione comunque non e' giusta e andrebbe modificata, perche' usare l'U value in questo 
modo e' sbagliato.
la relazione corretta sarebbe:
    T_in(t) = T_in(t-1) - U_val*AreaPareti*[T_in(t-1) - Tout(t)]/(massa_pareti*CaloreSpecificoMura)
In questo modo tutte le unita' di misura coincidono e non si mischiano mere con pere.
Ora cio' che rimane da fare e' trovare:
    Area_pareti
    U_val
    Massa_pareti
    Calore specifico mura
"""