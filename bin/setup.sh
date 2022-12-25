#!/bin/bash
echo ""
echo "*************************************"
echo " Setting up Airbnb-Scrap Environment"
echo "*************************************"
echo ""

echo "Checking Python Version - this project was developed using version 3.10.6"
python3 --version
echo ""

if [ -d "/home/$(whoami)/airbnb-scrap/" ];
then
    echo "Removing previous virtual environment"
    rm -r ~/airbnb-scrap
fi

echo ""
echo "Creating a Python virtual environment"
python3 -m venv ~/airbnb-scrap

if [ -f "./requirements.txt" ];
then
    echo "Activating virtual environment and installing dependencies"
    source ~/airbnb-scrap/bin/activate && python3 -m pip install --upgrade pip wheel
    source ~/airbnb-scrap/bin/activate && pip install -r requirements.txt
else
    echo "File requirements.txt not found. No dependencies installed on virtual environment"
fi

source ~/airbnb-scrap/bin/activate

echo ""
echo "*****************************************"
echo " Airbnb-Scrap Environment Setup Complete"
echo "*****************************************"
echo ""
