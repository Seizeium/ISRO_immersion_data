import pywhatkit as kit
from datetime import datetime

# Get the current date and time
now = datetime.now()

# Format the time and hour
formatted_time = now.strftime("%M")
formatted_hour = now.strftime("%H")

def remove_first_leading_zero(s):
    if s.startswith('0'):
        return s[1:]
    return s

# Remove the first leading zero and convert to integers
minute = int(remove_first_leading_zero(formatted_time)) + 1
hour = int(remove_first_leading_zero(formatted_hour))

# Parameters
phone_number = "+919405720785"  # Replace with the recipient's phone number in the format "+[country code][number]"
message = "Hello, this is a test message from pywhatkit!"
image_path = r"D:\Athar\Terra_spatial\ISRO_immersion_data\download.jpg"  # Use raw string for the file path
caption = "This is a test image from pywhatkit!"

# Send message
kit.sendwhats_image(phone_number, image_path, caption, hour, minute)

# Print formatted time for debugging
print("Formatted time:", formatted_time)
print("Formatted hour:", formatted_hour)
print("Scheduled hour:", hour)
print("Scheduled minute:", minute)
