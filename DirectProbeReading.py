import time, datetime, serial, string, codecs, csv

ser = serial.Serial('COM5',9600,timeout=3)

ch = [0]*15
m = [0]*15
b = [0]*15
outlist = [0]*15
n = 0
while True:
  # dat is the data gathered over the USB. 15 channels of voltages comma separated 
  # in a single string.
  dat = ser.readline()
  if dat:
    # filedate sets a variable for today's date 
    filedate = datetime.date.today()
    # n is the line number in the .csv document. It is incremented every data cycle.
    n = n + 1
    # When there is data over serial a .csv file is opened with the name scheme of
    # "MCUdat(today's date).csv" such that a new file is created every day.
    
    with open('DirectVoltageReading'+str(filedate)+'.csv', 'a') as csvfile:
      # chvolwriter separates the string of voltages (dat) into 15 indexed positions,
      # prepends the date and time into index 0, and the line number into index 16. The
      # list is then appended to the most recent vlotage .csv file in the current 
      # directory, where the raw voltages are stored separately.
      chvolwriter = csv.writer(csvfile, delimiter=',', quotechar='|', lineterminator='\n')
      chvolwriter.writerow([str(datetime.datetime.now()) + "," + dat + "," + str(n)])
      print str(datetime.datetime.now()) + ", " + dat
    
    # chlist splits the voltage string (dat) into a list of separate voltages.
    chlist = dat.split(",")
    # the for loop then converts the list into another list (ch) of floating
    # point integers to be calibrated.
    for i in range (0,15):
      ch[i] = float(chlist[i])   
    
    # cal reads in the calibration values from "Probe Calibration Variables.txt"
    cal = open("Probe Calibration Variables.txt","r")
    # callist creates a nested list from the .txt file.
    callist = cal.readlines()
    
    # the for loop takes the index 0 values from callist, and converts them to a
    # list of floating point calibration slope values (m).
    for i in range (0,15):
      m[i] = float(callist[i].split("\t")[0])

    # the for loop takes the index 1 values from callist, and converts them to a
    # list of floating point calibration intercept values (b).
    for i in range (0,15):
      b[i] = float(callist[i].split("\t")[1])
    
    # the for loop creats a list (outlist) of floating point calibrated probe readings 
    # (m*ch +b) in the formof y = mx + b.
    for i in range (0,15):
      outlist[i] = round(m[i]*ch[i] + b[i],4)
    
    # outlist is converted to a string of comma separated variables (out) to be written
    # to a .csv file.
    out = str(outlist).strip("[]")

    with open('DirectProbeReading'+str(filedate)+'.csv', 'a') as csvfile:
      # chwriter separates the string of calibrated probe readings (out) into 15 indexed
      # positions, prepends the date and time into index 0, and the line number into
      # index 16. The list is then appended to the most recent calibrated probe reading 
      # .csv file in the current directory to be accessed by the DirectProbeReading 
      # Mathematica GUI script.
      chcalwriter = csv.writer(csvfile, delimiter=',', quotechar='|', lineterminator='\n')
      chcalwriter.writerow([str(datetime.datetime.now()) + "," + out + "," + str(n)])
      print str(datetime.datetime.now()) + ", " + out