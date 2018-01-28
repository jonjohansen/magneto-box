# magneto-box

### Milestone 1: Project concept
#### Things to include in the concept:
* An overall direction of the project
* Team members roles
* Idea of scope and complexity
* Identifies potential (usage, market, . . . )
* A basis to start with technical choices


### Concept
The overall goal of the project is to confirm a proof of concept for a microcontroller-based sensor unit that can detect changes in the magnetic field of the Earth. This could be used, if the sensor can detect changes at high enough statistical accuracy to measure low-intensity irregularities caused by the Auroral Electrojet, a transport current in the polar ionosphere. If successful, a network of these units can collect data that could be used to create a three-dimensional model of transport currents around an area, which could be used to remove interference in trans-ionospheric radar measurements, or increase the significance of ionospheric EM-measurements.

In order to show a proof of concept, we will attempt to create a magnetogram for for Tromsø, and compare measurements to the university’s high-accuracy magnetogram. (http://flux.phys.uit.no/Last24/Last24_tro2a.gif). If we can obtain sub-10nT resolution as well as a high degree of adherence to the “official” magnetogram, some professors in the physics department of the University of Tromsø have expressed interest in creating a similar unit in order to get high-resolution models of the geomagnetic field.




### Team members & role:
* Torbjørn Tveito
_Physics student(?)_. Calculations and data-analytics and provide knowledge and insight of ionospheric effects, statistical signal analysis, and general magnetic theory.
* Anton Garri Fagerbakk
_Comp.Sci student_. Development and configuration of software.   
* Jon Helge Johansen
_Comp.Sci student_. Development and configuration of software. 

These roles are not definitive.

### Potential
If successful the box will aid in collecting magnetic field data in a cheap fashion. The market for this will be for corporations (???), organizations, and/or anyone doing research, but could also be sold commercially as prices for the boxes would be low. For example the new Eiscat3d field in Skibotndalen will cost the Norwegian government 288 M NOK. These boxes will be much cheaper, and can be used to improve accuracy and significance of radar results. Similar projects have been suggested by the physics department of the University of Tromsø, but have been turned down due to high costs.

### Technology
The technology we are looking to use are IoT magnetic field sensors accessing the LoRaWAN network. We will build a prototype box which will be put somewhere in nature.
This means that we will have to modify and use technology which are key for operating LoRaWAN IoT devices.

### Challenges
One of the challenges is configuring the device to find out the highest rate of data we can transport, without having the cost of measuring and transporting data surpass the main idea of how long each device should be left unattended.

A large part of the development iteration will focus on reducing the cost of both measuring and transporting data in terms of power and bandwidth. Most likely a balance between enough data to remove statistical anomalies and preserving battery life time will be one of the things we hope to find a solution to.

Another challenge with these types of measurements are the interference caused by almost anything. Configuring protocols for being able to measure data without any interference from the device itself will probably prove a challenge we are going to have to face. 


