#!/bin/bash

# for Ubuntu 20.04 Amazon-EC2
#cd 
#cd dash_AreaPredict
#gunicorn -w 1 -b 0.0.0.0:8052 dash_AreaPredict:application --daemon

#cd
#cd dash_CasePredict
#gunicorn -w 1 -b 0.0.0.0:8053 dash_CasePredict:application --daemon

#cd
#cd dash_Statistics
#gunicorn -w 1 -b 0.0.0.0:8054 dash_Statistics:application --daemon

# for Mac OS X localhost
cd dash_AreaPredict
gunicorn -w 1 -b 127.0.0.1:8052 dash_AreaPredict:application --daemon

cd ..
cd dash_CasePredict
gunicorn -w 1 -b 127.0.0.1:8053 dash_CasePredict:application --daemon

cd ..
cd dash_Statistics
gunicorn -w 1 -b 127.0.0.1:8054 dash_Statistics:application --daemon

echo 'All Dash Apps start!'
