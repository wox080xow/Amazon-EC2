#!/bin/bash

cd
cd dash_AreaPredict
gunicorn -w 1 -b 0.0.0.0:8052 dash_AreaPredict:application --daemon

cd
cd dash_CasePredict
gunicorn -w 1 -b 0.0.0.0:8053 dash_CasePredict:application --daemon

cd
cd dash_Statistics
gunicorn -w 1 -b 0.0.0.0:8054 dash_Statistics:application --daemon

