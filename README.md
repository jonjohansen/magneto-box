# Magneto-Box

### Project Motivation
There is a large community of physicists who study the ionosphere with radar facilities. In
order to make sense of the measurements done with radar, one must know a variety of physical
properties of the medium being investigated. In plasmas, these properties can change as a function of the magnetic field present, so accurate measurements of the magnetic field in regions where studies are being done can be a significant help for the scientific community.
<br>Magnetic fields change how reflective plasmas are to electromagnetic radiation, because the frequency and velocity of electrons in the plasma is proportional to the magnitude of the magnetic field. 
<br>Magnetometer installations able to provide such a high accuracy are expensive and are easily affected by nearby sources of noise, and so these installations are few and far between. 
<br>If, however, one was able to produce a cheap, small and easy to create device able to, through basic statistical methods, provide measurements with a “good enough” accuracy, an array of measuring devices could be placed in the area surrounding a radar facility. This would make it possible to create a model of the spatial changes in the magnetic field through the ionosphere, which could potentially significantly assist in modeling the plasma.

<img src="./img/magnetohydrodynamics.png" width="200">

### Project Concept
The overall goal of the project is to confirm a proof of concept for a microcontroller-based sensor unit that can detect changes in the magnetic field of the Earth. This could be used, if the sensor can detect changes at high enough statistical accuracy to measure low-intensity irregularities caused by the Auroral Electrojet, a transport current in the polar ionosphere. If successful, a network of these units can collect data that could be used to create a three-dimensional model of transport currents around an area, which could be used to remove interference in trans-ionospheric radar measurements, or increase the significance of ionospheric EM-measurements.


### Technology
This project is based on the usage of a LoPy device, but can be used with any other microcontroller that can compile and run Python/Micropython. The device developed uses LoRaWAN to communicate the data to a recieving backend, but it is possible to implement or develop other forms of data communication.

### MAG3110
The [MAG3110](https://www.nxp.com/docs/en/data-sheet/MAG3110.pdf) is a small, low-power digital 3D magnetic sensor with a wide dynamic range to allow operation in PCBs with high extraneous magnetic fields.

When initialized it sets the correct modus operandi as well as defining some
general resources for the sensor. The library features methods of getting singular readings, as well as readings over a timespan (results in higher accuracy), as well as convertion methods for the given data output.

The MAG3110 sensor was found to be heavily dependent on temperature.<br>
For readings about our results and discoveries can be found in our [report](./doc/project_report.pdf) 

### MPU9265
The MPU-9265 device combine a 3-axis gyroscope, 3-axis accelerometer and 3-axis compass in the same chip together with an on board Digital Motion Processor capable of processing the complex Motion Fusion algorithms.

When the sensor is initialized it runs the configuration for the MPU and the AK sensors. The configuration takes the sensors out of sleep mode, prepares the right modes for reading continuous output. <br>The sensors reads magnetic field, gyroscope, accelerometer and temperature data continuously. The data is retrieved using a fetching method which takes the
readings from the gyroscope, accelerometer and temperature and packs it into a tuple. The tuple can then be accessed for readings and further calculations. The accelerometer data is also used to calculate the vector of the sensor to guarantee that the magnetic data is correct.

### LoRA 
This project is set up to use LoRaWAN connection to communicate with Telenors managed [IoT cloud platform MIC](https://docs.telenorconnexion.com/mic/). LoRa protocol functions as a **low power usage** and **long range** wireless connection, resulting in a good way of transporting data from our device in realtime. Telenor offers a library StartIot to route and and setup this connection properly.

### References
#### [**Project report**](./doc/project_report.pdf)
Our project report documenting our development progress, data results and findings. This can be used as a full scale documentation of the project.

#### LoPy / Micropython
* [**Micropython I2C** library documenation](http://docs.micropython.org/en/latest/wipy/library/machine.I2C.html)
* [**LoPy** documentation](https://docs.pycom.io/chapter/gettingstarted/connection/lopy.html)
* [**mpfshell** A simple shell based file explorer for Micropython based devices](https://github.com/wendlers/mpfshell) 

#### Sensor documentation
* [Information about **I2C** bus interface](https://www.nxp.com/docs/en/application-note/AN10216.pdf)
* [Product Specification for **MPU9250** used for **MPU9265**](https://www.invensense.com/wp-content/uploads/2015/02/PS-MPU-9250A-01-v1.1.pdf)
*	[Register Maps and Descriptions for **MPU9250** used for **MPU9265**](https://www.invensense.com/wp-content/uploads/2015/02/RM-MPU-9250A-00-v1.6.pdf)
* [Data-sheet for **MAG3110**](https://www.nxp.com/docs/en/data-sheet/MAG3110.pdf)

#### Realtime magnetograms
* [24 hour plot by **University of Tromsø(UiT)** and several other Universities](http://flux.phys.uit.no/Last24/)

#### LoRa(WAN)
* [**PyCom LoRa library** documentation](https://docs.pycom.io/chapter/firmwareapi/pycom/network/lora.html)
* [Telenor Managed IoT Cloud Platform](https://docs.telenorconnexion.com/mic/)