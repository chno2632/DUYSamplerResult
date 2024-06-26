
import datetime
# ADC maximumm value 14 bits? == 16383
with open("SMPLOG3_240523.txt") as datasource:
    rawData = datasource.readlines()

# Part 1. Establish fundamental characteristics
print(type(rawData))
# Calculate Unix time
print(rawData[0], rawData[1], rawData[2])

print("Length of raw data is : " + str(len(rawData)) + " elements")

maxValue = 0
minValue = 16384
print("Here I am")
for i in range(len(rawData)):
    val = int(rawData[i])
    # For all values except timestamps, find min/max
    if val < 16384:
        if val > maxValue:
            maxValue = val
        if val < minValue:
            minValue = val

print("Max value is : " + str(maxValue))
print("Min value is : " + str(minValue))

# Part 2. Separate the raw data file, containing both timestamps and sample values, in to 2 separate lists,
# value[] and time[]
# The 2 lists should have the same length, equal to the number of samples in the raw data file
# Every timestamp belongs to the sample right after the timestamp

# Create timestamp list
# Each timestamp holds the time for the next corresponding sample value
# This means moving the first timestamp to new list at same position index as in the original samplelist
# The next timestamp

index = 0
timeStampInserted = False       # For each timestamp in rawFile a sample value should be inserted
value = []
time = []
for i in range(len(rawData)):
    val = int(rawData[i])
    # For all positions sort out values and timestamps
    if val < 16384:
        value.append(val)
        if timeStampInserted == False:
            time.append(int(0))
        else:
            timeStampInserted = False
    else:
        time.append(val)
        timeStampInserted = True

if len(time) != len(value): print("Something wrong. value and time has not equal lengths!!")

# Part 3. Do some checks of timestamps.
# Check if any disrupts of sampling has occured

# Make a list of index, one index value for all positions not containing zero
timeIndexes = []
for i in range(len(time)):
    unixTime = int(time[i])
    if unixTime != 0:
        timeIndexes.append(i)

print(timeIndexes)
#ts = int("1714313815")

for i in range(len(timeIndexes)):
    ts = int(time[timeIndexes[i]])
    timestamp = datetime.datetime.fromtimestamp(ts)
    print(timestamp.strftime('%Y-%m-%d %H:%M:%S : ') + str(time[timeIndexes[i]]))

# Count if number of samples between timestamps are reasonable close to the sampling rate

numberOfSamples = 0
lastTimeStamp = 0
distanceInTime = 0
distanceInSamples = 0
firstTimeExecuted = True
for i in range(len(rawData)):
    val = int(rawData[i])
    if val < 16384:
        numberOfSamples += 1
    else:
        if firstTimeExecuted:
            lastTimeStamp = val
        print("Number of samples = " + str(numberOfSamples) + " at timestamp " + str(val))
        distanceInTime = val - lastTimeStamp - 1
        distanceInSamples = numberOfSamples
        print("Distance in samples is: " + str(distanceInSamples))
        if firstTimeExecuted:
            firstTimeExecuted = False
            print("Distance in time is: " + str(distanceInTime+1) + " seconds")
        else:
            print("Distance in time is: " + str(distanceInTime) + " seconds")
        numberOfSamples = 0
        lastTimestamp = val
        print("")
#Check if approximation of 1 secnd in between every sample or if any disruption may have occured


#print(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
#unixTime = time[0]
#print(datetime.utcfromtimestamp(unixTime).strftime('%Y-%m-%d %H:%M:%S'))



# Now create timestamps for zero-time
