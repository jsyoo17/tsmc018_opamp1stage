Installation process refers to https://pyspice.fabrice-salvaire.fr/ and its github discourse

Installation of LTSPICE and NGSPICE is not included because you can just download it from the links below
https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html
https://ngspice.sourceforge.io/download.html

[PySpice Installation For Windows]
1. install pyspice in windows cmd: 'pip install pyspice'
2. install ngspice dll in windows cmd: 'pyspice-post-installation --install-ngspice-dll
3. add to PATH: {'dll-vs' directory path} for example: 'C:/Users/{username}/AppData/Local/Programs/Python/Python39/Lib/site-packages/PySpice/Spice/NgSpice/Spice64_dll/dll-vs'
4. check install in windows cmd: pyspice-post-installation --check-install

[Gmin Stepping]
* Pyspice regards ngspice gmin stepping as error not warning
* To use gmin stepping, refer to https://github.com/PySpice-org/PySpice/pull/313/
* Run gminsteperror.py file. If 'shared.py' file is changed as the link above, the file will run fine

[Some Unverified Solutions to Pyspice Errors]
* add other paths that causes warning messages to PATH
* install ngspice and add ngspice bin folder to PATH
* install visual studio if it is not installed
* there seems to be problem (usually when including lib files) if there is spacing within path names
