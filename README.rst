

==============
CORE-V 180 MCU
==============


An implementation of the CORE-V on the Global Foundries 180 MCU node.


This project group together a set of other repositories (submodules)
to assemble the complete design flow and build the chip.

For the design flow:

* SV2V -- SystemVerilog translator, https://github.com/zachjs/sv2v
* Yosys -- Logical Synthesis, https://github.com/YosysHQ/yosys/
* Coriolis -- Physical P&R, https://github.com/lip6/coriolis/
* GF 180 MCU PDK -- Design Kit (GF), https://github.com/google/gf180mcu-pdk/
* Chips4Makers -- Standard Cell Library, https://gitlab.com/Chips4Makers/c4m-pdk-gf180mcu

For the design:

* CORE-V MCU, https://github.com/openhwgroup/core-v-mcu

The build procedure from a cloned version will be described here.

You can generate the ``GDS`` layout using the Github ``CI``, with the action :
``cv32e40p layout (GDS)``. It will be put into an artifact at the end of the
run. When run for the first time, it will rebuild all the tool and take a
bit less than one hour. On subsequent ones, it should take about 8 minutes.


.. note:: This is only a very early version and only a demonstrator on
	  the RISC-V component only: ``cv32e40p``. Not checks have been
	  performed, it just to setup the design flow for now.


