from BallRoomBayesNet import BallroomBayesNet

#takes in textfile w/ a sequence of M1, M2, and S sensor readings 
#returns m and n parameters and list of dictionaries w/ sensors readings
def read_text_file(filename):
    text_file = open(filename, 'r')
    lines = text_file.readlines()
    line0 = lines[0].strip().replace(" ", "")
    #write number of rows and columns to a tuple
    mn_coords = (int(line0[0]), int(line0[1]))

    bayes_data = {"size": mn_coords, "sensor_readings": []}

    timestep = 0
    for i in range(1, len(lines)):
        line = lines[i].strip().replace(" ", "")
        if line[0] == "1":
            m1 = True
        else:
            m1 = False

        if line[1] == "1":
            m2 = True
        else:
            m2 = False

        s = (int(line[2]), int(line[3]))

        bayes_data["sensor_readings"].append({"timestep": timestep, "m1": m1, "m2": m2, "s": s})

        timestep += 1

    return bayes_data

def main():
    fileName = input("Enter file name: ")
    data = read_text_file(fileName)
    ballroom = BallroomBayesNet(*data["size"], debug=False)

    for sensorData in data["sensor_readings"]:
        print("Observation | M1: " + str(sensorData["m1"]) + ", M2: " + str(sensorData["m2"])
        + ", Sound location: " + str(sensorData["s"]))
        print("Monkey's predicted current location at time step " + str(sensorData["timestep"]))
        ballroom.get_distrib_over_all_C(sensorData["m1"], sensorData["m2"], *sensorData["s"])
    

if __name__ == "__main__":
    main()

    
