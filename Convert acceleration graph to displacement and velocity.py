
import pandas as pd
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
from warnings import resetwarnings
import matplotlib.pyplot as plt

# Load the earthquake data from Excel
data = pd.read_excel('/content/data1.xlsx', sheet_name='eu_175_1')

# Assume the first column is time (s) and the second column is acceleration (m/s^2)
time = data.iloc[:, 0]
acceleration = data.iloc[:, 1]*9.81

# Initialize an empty list to store the velocities
velocities = []

# Iterate over each row in the data and calculate the velocity
for i in range(len(data)):
    velocity = integrate.simps(acceleration[:i+1], time[:i+1])
    velocities.append(velocity)

# Print the velocities
print(velocities)

plt.plot(time, velocities, label='Velocity (m/s)')

# Initialize an empty list to store the displacement
displacements = []

# Iterate over each row in the data and calculate the displacement
for i in range(len(data)):
    displacement = integrate.simps(velocities[:i+1], time[:i+1])
    displacements.append(displacement)

plt.plot(time, displacements , label='displacement (m)')

plt.plot(time, acceleration , label='displacement (m)')

max_displacement = max(abs(d) for d in displacements)
max_velocity = max(abs(v) for v in velocities)
max_accelation = max(abs(a) for a in acceleration)

print ("PGA:",max_accelation,"PGV:",max_velocity,"PGD:",max_displacement)

"""part 2"""

# Get the absolute values of acceleration
abs_acceleration = abs(acceleration)

# Find the third and fifth highest absolute acceleration values
sorted_acceleration = sorted(abs_acceleration, reverse=True)
third_highest = sorted_acceleration[2]
fifth_highest = sorted_acceleration[4]

# Print the third and fifth highest absolute acceleration values
print("Third highest absolute acceleration:", third_highest)
print("Fifth highest absolute acceleration:", fifth_highest)

"""part2 mode 2"""

acc = []
for i in range (1,len(abs_acceleration)-1):
  a = abs_acceleration[i-1]
  b = abs_acceleration[i]
  c = abs_acceleration[i+1]
  if b>a and b>c :
    acc.append(b)

# Find the third and fifth highest absolute acceleration values
sorted_acc = sorted(acc, reverse=True)
third_highesta = sorted_acc[2]
fifth_highestb = sorted_acc[4]

# Print the third and fifth highest absolute acceleration values
print("Third highest absolute acceleration:", third_highesta)
print("Fifth highest absolute acceleration:", fifth_highestb)

vel = []
abs_velocity = [abs(v) for v in velocities]
for i in range (1,len(abs_velocity)-1):
  e = abs_velocity[i-1]
  f = abs_velocity[i]
  g = abs_velocity[i+1]
  if f>e and f>g :
    vel.append(f)

# Find the third and fifth highest absolute velocity values
sorted_vel = sorted(vel, reverse=True)
third_highestc = sorted_vel[2]
fifth_highestd = sorted_vel[4]

# Print the third and fifth highest absolute velocity values
print("Third highest absolute velocity:", third_highestc)
print("Fifth highest absolute velocity:", fifth_highestd)

dis = []
abs_dispacement = [abs(d) for d in displacements]
for i in range (1,len(abs_dispacement)-1):
  h = abs_dispacement[i-1]
  l = abs_dispacement[i]
  j = abs_dispacement[i+1]
  if l>h and l>j :
    dis.append(l)

# Find the third and fifth highest absolute displacments values
sorted_dis = sorted(dis, reverse=True)
third_highestf = sorted_dis[2]
fifth_highestg = sorted_dis[4]

# Print the third and fifth highest absolute displacements values
print("Third highest absolute displacements:", third_highestf)
print("Fifth highest absolute displacements:", fifth_highestg)

#calcuating the filing step
first_dis = displacements[0]
last_dis = displacements[-1]
fs = last_dis-first_dis
fs_abs = abs(fs)
print ("fs:",fs_abs)

"""plt"""

pgam =[max_accelation]
pgvm =[max_velocity]
pgdm =[max_displacement]
thirdam = [third_highesta]
fifthm = [fifth_highestb]
fsm = [fs_abs]

# Create a Pandas dataframe for the earthquake data
df_data = pd.DataFrame({'Time (s)': time, 'Acceleration (m/s^2)': acceleration, 'Velocity (m/s)': velocities, 'Displacement (m)': displacements, } )
df_dataa = pd.DataFrame({'PGA': pgam ,'PGV': pgvm  , 'PDG':pgdm ,'Third highest absolute acceleration': thirdam  ,'Fifth highest absolute acceleration':fifthm ,'filing step': fsm})

!pip install xlsxwriter

# Create a Pandas Excel writer object
writer = pd.ExcelWriter('II-III - Africa3.xls', engine='xlsxwriter')

# Write the earthquake data to the first sheet
df_data.to_excel(writer, sheet_name='Data', index=False)
df_dataa.to_excel(writer, sheet_name='Data1', index=False)

# Create a new sheet for the plots
workbook = writer.book
worksheet = workbook.add_worksheet('Plots')

# Create a chart object for the velocity plot
chart_acc = workbook.add_chart({'type': 'line'})
chart_acc.add_series({
    'name': 'Acceleration (m/s)',
    'categories': ['Data', 0, 0, len(data), 0],
    'values': ['Data', 0, 1, len(data), 1],
})
chart_acc.set_title({'name': 'Acceleration vs Time'})
chart_acc.set_x_axis({'name': 'Time (s)'})
chart_acc.set_y_axis({'name': 'Acceleration (m/s^2)'})

# Create a chart object for the velocity plot
chart_vel = workbook.add_chart({'type': 'line'})
chart_vel.add_series({
    'name': 'Velocity (m/s)',
    'categories': ['Data', 0, 0, len(data), 0],
    'values': ['Data', 0, 2, len(data), 2],
})
chart_vel.set_title({'name': 'Velocity vs Time'})
chart_vel.set_x_axis({'name': 'Time (s)'})
chart_vel.set_y_axis({'name': 'Velocity (m/s)'})

# Create a chart object for the displacement plot
chart_disp = workbook.add_chart({'type': 'line'})
chart_disp.add_series({
    'name': 'Displacement (m)',
    'categories': ['Data', 0, 0, len(data), 0],
    'values': ['Data', 0, 3, len(data), 3],
})
chart_disp.set_title({'name': 'Displacement vs Time'})
chart_disp.set_x_axis({'name': 'Time (s)'})
chart_disp.set_y_axis({'name': 'Displacement (m)'})

# Insert the charts into the worksheet
worksheet.insert_chart('A1', chart_acc)
worksheet.insert_chart('A20', chart_vel)
worksheet.insert_chart('A40', chart_disp)

# Save the Excel file
writer.save()
