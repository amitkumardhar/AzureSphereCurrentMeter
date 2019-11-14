# AzureSphereCurrentMeter
CurrentMeter using AvnetMT3620 and Azure IOT hub

The code to run can be found by cloning https://github.com/Avnet/AvnetAzureSphereStarterKitReferenceDesign and applying the patch currentMeter.patch

The file receive.py can be used to recieve events from IoT hub using azure SDK for python and store in MongoDB.
Pre-requisites: 
pip install --pre azure-eventhub
pip install pymongo
