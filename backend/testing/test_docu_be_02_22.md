# Archicheck Backend Tests
**Author**: Benjamin Müller  
**Date**: 01.02.2022 - 28.02.2022

This document will protocol my testing approaches in regard to testing the archicheck backend. Currently, the
implementation of the database as well as GET and POST requests are done. In the last part of this project, I am 
responsible to keep everything testing related up to date.


### Updating Postman Tests
The main changes are the checks for the timestamp of users first login aswell as the timestamps in fact checks. Because
those have to be changed into an accepted format, also the signatures have to be updated for all of the tests.

Further more the GET requests of the GetFactChecks have to be adapted. There I have to set the improved timestamps and
change the signatures which Postman tests against.


