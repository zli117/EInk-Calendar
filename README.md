# EInk Smart Calendar

## What does it do?
It's a raspberry pi based smart calendar that can tell you the current date, 
weather, and your events on Google calendar.

## Get started
First you need to get a few components:
 * Raspberry pi (2 or 3 or zero) and SD card
 * EInk display: Waveshare 7.5 inch black and white display
 * A 7.5 inch photo frame
 
Then clone this repo and install the dependencies
```bash
pip install -r requirements.txt
```
Also make sure you have at least Python 3.5 installed

Third, you need to get the credentials for Open Weather Map and Google calendar
 * OWM API key:
   * Go to the Weather API page: [link](https://openweathermap.org/api)
   * Subscribe to *5 day / 3 hour forecast*
 * Google credentials:
   * Follow the instructions of this answer on [stackoverflow](https://stackoverflow.com/a/19766913/4434038).
   * Instead of choosing the drive API, choose Calendar API v3 of scope
     `https://www.googleapis.com/auth/calendar.readonly`
   * We will need the client ID, client secrete, refresh token and access token
   
Then hook up the wires as following:
![diagram|1383x1392, 20%](https://raw.githubusercontent.com/Zonglin-Li6565/EInk-Calendar/master/diagram.png)
   
Once you have got all the credentials and hooked up the wires, you can run 
`main.py` without any parameter to create the config file:
```bash
python3 main.py
```
and follow the interact guide to create the config file.

You can specify the config file for later runs as:
```bash
python3 main.py -c <config file path>
```
