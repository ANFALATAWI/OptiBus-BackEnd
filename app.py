from flask import Flask, jsonify, request
import random
import copy

app = Flask(__name__)

"""
dict['userId']={{(start,end)}
"""
usersAtStation={}
usersAtBus={}
route=[1,2,3,4,5]

def calculateRoute(currentStop):



    if (len(usersAtBus) == 0 and len(usersAtStation) == 0):
        print("bus is stoping")
        return currentStop

    else:
        print("else")

        busyStations = list(map(lambda i: i[1][0], usersAtStation.items()))

        # By bus riders
        requestedStations = list(map(lambda i: i[1][1], usersAtBus.items()))

        print("busyStations: " + str(busyStations))
        print("requestedStations: " + str(requestedStations))

        mySet = busyStations + requestedStations




        for i in range(currentStop + 1, currentStop + 6):
            print("i = "+ str(i % 6))
            if ((i % 6) in mySet):
                print("bus is moving to" + str(i % 6))
                return (i % 6)





def handlePassengers(currentStop):
    temp = copy.deepcopy(usersAtStation)
    print("handling passenger at station"+ str(currentStop))
    for user in temp:
        if(usersAtStation[user][0] == currentStop):
            print("user is taking the bus: "+str(usersAtStation[user]))
            usersAtBus[user] = usersAtStation.pop(user)

    temp = copy.deepcopy(usersAtBus)

    for user in temp:
        if(usersAtBus[user][1] == currentStop):
            print("user is leaving the bus: " + str(usersAtBus[user]))
            usersAtBus.pop(user)

    pass


@app.route('/driver')
def handleDriver():
    stopID = int(request.args.get('stopID'))
    handlePassengers(stopID)

    goToID = {"stopID":calculateRoute(stopID)}
    print("users at station: " + str(usersAtStation))
    print("users at bus: " + str(usersAtBus))
    return jsonify(goToID)


@app.route('/user')
def handleUser():
    currentStation = int(request.args.get('currentStation'))
    destinationStation = int(request.args.get('destinationStation'))
    userID = str(request.args.get('userID'))
    usersAtStation[userID] = (currentStation, destinationStation)
    print("users at station: " + str(usersAtStation))
    print("users at bus: " + str(usersAtBus))
    return "hi"

@app.route('/bus')
def handleBus():

    json = {"skip":bool(random.getrandbits(1))}
    return jsonify(json)

