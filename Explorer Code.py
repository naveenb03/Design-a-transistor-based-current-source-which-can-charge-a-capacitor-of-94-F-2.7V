from matplotlib import pyplot as plt
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Doc.ExampleTools import find_libraries

# Define the LTSpice library path
ltspice_lib_path = 'C:/Program Files/LTC/LTspiceXVII/lib'

# Define the LTSpice schematic file path
ltspice_sch_path = 'current_source_simulation.asc'

# Define the circuit parameters
input_voltage = 2.7
capacitance = 94e-6

# Define the resistor values for the two different constant currents
resistor_values = [8000, 2670]

# Define the PySpice simulation parameters
simulation_time = 10e-3
time_step = 1e-5

# Load the LTSpice library
spice_library = SpiceLibrary(ltspice_lib_path)

# Load the LTSpice schematic file
circuit = Circuit(ltspice_sch_path)

# Set the input voltage value
circuit.V1.dc_value = input_voltage

# Set the capacitor value
circuit.C1.capacitance = capacitance

# Loop over the two resistor values and set the resistor values and the corresponding output names
output_names = []
for i, resistor_value in enumerate(resistor_values):
    resistor_name = 'R{}'.format(i + 1)
    output_name = 'V(C{})'.format(i + 1)
    circuit[resistor_name].resistance = resistor_value
    output_names.append(output_name)

# Set up the PySpice simulation
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.options['ts'] = time_step
simulator.options['tstop'] = simulation_time

# Run the PySpice simulation and obtain the waveforms
waveforms = simulator.transient(outputs=output_names)

# Extract the time array and the voltage and current arrays for each output
time = waveforms.time
voltage_arrays = [waveforms.get(output_name) for output_name in output_names]

# Plot the waveforms
fig, axs = plt.subplots(len(resistor_values), 1, sharex=True, figsize=(8, 6))
for i, voltage_array in enumerate(voltage_arrays):
    axs[i].plot(time, voltage_array, label='Ic = {} uA'.format((i + 1) * 250))
    axs[i].set_ylabel('Voltage (V)')
    axs[i].legend()
axs[-1].set_xlabel('Time (s)')

plt.show()
