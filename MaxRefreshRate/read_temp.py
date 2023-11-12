import serial
import mysql.connector
import keyboard
import re

# MySQL connection settings
config = {
    'user': 'root',
    'password': 'root1234',
    'host': 'localhost',
    'database': 'stress_data'
}


def calculate_stress_level(temperature):
    if temperature < 16:
        return 'Low'
    elif temperature > 28:
        return 'High'
    else:
        return 'Normal'

def extract_numeric_value(data):
    # Extract numeric part from the data string
    numeric_part = re.search(r'[-+]?\d*\.\d+|\d+', data)
    if numeric_part:
        return float(numeric_part.group())
    else:
        return None
        

def read_temperature_and_store():
    try:
        # Establishing a connection to the Arduino's serial port
        # Replace with your Arduino's serial port

        while True:
            # Wait for the Enter Plant sample name

            plant_sample_name = input("Enter Plant sample name : ")
            input(
                "Point the thermal camera to measure temperature and press enter to read...")
            #keyboard.wait('enter')

            ser = serial.Serial('COM5', 115200)  # connect to nodemcu

            # Reading one line of temperature data
            temperature = float(ser.readline().strip())
            print(temperature)
            # Calculating the stress level based on the temperature
            stress_level = calculate_stress_level(temperature)

            
            print("Sample Name : ", plant_sample_name, " Temp : ",
                  temperature, " stress level : ", stress_level)

            


            ser.close()  # disconnect from nodemcu

            
            # Establishing a connection to the MySQL database
            conn = mysql.connector.connect(**config)

            # Creating a cursor object to execute queries
            cursor = conn.cursor()

            # Inserting data into the table
            query = "INSERT INTO plants_temp (plant_temp, plant_stress_level,plant_sample_name) VALUES (%s, %s, %s)"
            values = (temperature, stress_level, plant_sample_name)
            cursor.execute(query, values)

            # Committing the changes to the database
            conn.commit()

            print("Data inserted successfully!")

            # Closing the cursor and connection
            cursor.close()
            conn.close()

            print("\n")

    except (serial.SerialException, ValueError) as error:
        print(f"Error reading temperature: {error}")

    except mysql.connector.Error as error:
        print(f"Error inserting data: {error}")

    finally:
        ser.close()


read_temperature_and_store()