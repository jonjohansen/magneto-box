# Magneto-Box

### Project Motivation
There is a large community of physicists who study the ionosphere with radar facilities. In
order to make sense of the measurements done with radar, one must know a variety of physical
properties of the medium being investigated. In plasmas, these properties can change as a function of the magnetic field present, so accurate measurements of the magnetic field in regions where studies are being done can be a significant help for the scientific community.
Magnetic fields change how reflective plasmas are to electromagnetic radiation, because the frequency and velocity of electrons in the plasma is proportional to the magnitude of the magnetic field. Magnetometer installations able to provide such a high accuracy are expensive and are easily affected by nearby sources of noise, and so these installations are few and far between. If, however, one was able to produce a cheap, small and easy to create device able to, through basic statistical methods, provide measurements with a “good enough” accuracy, an array of measuring devices could be placed in the area surrounding a radar facility. This would make it possible to create a model of the spatial changes in the magnetic field through the ionosphere, which could potentially significantly assist in modeling the plasma.

![xkcd](magneto-box/maghydrodynam.png)

### Project Concept
The overall goal of the project is to confirm a proof of concept for a microcontroller-based sensor unit that can detect changes in the magnetic field of the Earth. This could be used, if the sensor can detect changes at high enough statistical accuracy to measure low-intensity irregularities caused by the Auroral Electrojet, a transport current in the polar ionosphere. If successful, a network of these units can collect data that could be used to create a three-dimensional model of transport currents around an area, which could be used to remove interference in trans-ionospheric radar measurements, or increase the significance of ionospheric EM-measurements.


### Technology
This project is based on the usage of a LoPy device, but can be used with any other microcontroller that can compile and run Python/Micropython. The device developed uses IoT LoRaWAN to communicate the data it reads, but it is possible to implement or develop other forms of data collection.

#### Busses
The libraries written for the project all function on I2C busses.
### MAG3110
The MAG3110 is a small, low-power digital 3D magnetic sensor with a wide dynamic range to allow operation in PCBs with high extraneous magnetic fields.

When initialized it sets the correct modus of operation as well as defining some
general resources for the sensor. The library features a fetch data function which fetches and returns a tuple containing the data. A set of conversion methods for correctly converting the data from two sets of bytes into an int, as well as from a raw value to the nanotesla, which is the desired unit of measurement. The sensor also features a low accuracy temperature sensor, but this has not been used in our project, as the MPU9265 sensor yields more accurate results. A separate function for printing the data (used for debugging) is the final method of the class.

### MPU9265
The MPU-9265 device combine a 3-axis gyroscope, 3-axis accelerometer and 3-axis compass in the same chip together with an on board Digital Motion Processor capable of processing the complex Motion Fusion algorithms.

When the sensor is initialized it runs the configuration for the MPU and the AK sensors. The configuration takes the sensors out of sleep mode, prepares the right modes for reading continuous output. The sensors reads magnetic field, gyroscope, accelerometer and temperature data continuously. The data is retrieved using a fetching method which takes the
readings from the gyroscope, accelerometer and temperature and packs it into a tuple. The tuple can then be accessed for readings and further calculations. The accelerometer data is also used to calculate the vector of the sensor to guarantee that the magnetic data is correct.

### Lis3dl
The LIS3MDL is an ultra-low-power high-performance three-axis magnetic sensor.

The LIS3MDL sensor has a under-developed library due to an conclusion early on
in the project about the quality of data it outputs. The superior accuracy MAG3110 magnetometer debunked the need for use of this sensor, and the development of this library was stagnated. Thus it only contains basic initialization, and fetching data. It is in any way functional, but does not feature all the conversion and printing functions necessary to integrate it with our project.


### LoRA
jonjon take it away

#### References
* LoPy / Micropython
  * http://docs.micropython.org/en/latest/wipy/library/machine.I2C.html - Micropython I2C library
  *  https://docs.pycom.io/chapter/gettingstarted/connection/lopy.html - Lopy documentation
  * https://github.com/wendlers/mpfshell - Simple shell for Lopy communication
* Sensor documentation
  *  https://www.nxp.com/docs/en/application-note/AN10216.pdf  - Information about I2C bus interface
  * https://www.invensense.com/wp-content/uploads/2015/02/PS-MPU-9250A-01-v1.1.pdf - Product Specification for MPU9250
  * https://www.invensense.com/wp-content/uploads/2015/02/RM-MPU-9250A-00-v1.6.pdf - Register Maps and Descriptions for MPU9250
  * https://www.nxp.com/docs/en/data-sheet/MAG3110.pdf - Data-sheet for MAG3110

* Realtime magnetogram, 24 hour plot by University of Tromsø(UiT) and several other Universities.
  * http://flux.phys.uit.no/Last24/

* LoRa(WAN)
  * https://www.semtech.com/technology/lora