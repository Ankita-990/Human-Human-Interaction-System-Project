import serial
import csv
import time

esp_port = 'COM6'
baud = 9600
fileName = r"E:\ankita\ankita_giroti_project_files\dataset\emg_val_status56.csv"

ser = serial.Serial(esp_port, baud)
print("Connected to ESP32 at port " + esp_port)

sample = 7000
line = 0

prompt = input("Start collecting data (y/n): ")
if prompt == 'y':
    print("Wait for 1 second....")
    time.sleep(1)
    print("Start collecting EMG data")
    
    # To print data with label and status
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["EMG Value", "Status"])  # Write header
        
        while line < sample:
            raw_data = ser.readline().decode('utf-8').strip()
#             data_str = raw_data.decode('utf-8').strip()
            
            # Split "value,status" format
            if ',' in raw_data:
                value, status = raw_data.split(',', 1) 
                print(value + ',' + status)
                print()
                writer.writerow([value, status])
                line += 1
    
    
    # # To print data without label and sensor
    # # Open CSV file in append mode to avoid overwriting previous data
    # with open(fileName, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow("EMG Value")

    #     while line < sample:
    #         getData = ser.readline()
    #         dataString = getData.decode('utf-8').strip()  # Decode and strip whitespace/newlines
            
    #         # Convert reading into a list before writing it to CSV
    #         reading = [dataString]
    #         print(reading)
    #         writer.writerow(reading)  # Write as a new row
            
    #         line += 1
            
    #     print("Data Collection Completed")
        
else:
    print("Don't have to print anything!")




# #             time.sleep(0.005)


