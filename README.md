# Shade
Software for SHADE experiment, BEXUS Cycles 12.
SHADE (SDR Helix Antenna Deployment Experiment) from the Aristotle University of Thessaloniki, Greece – the first Greek-built experiment to be launched on BEXUS.

The BEXUS (Balloon EXperiments for University Students) is a stratospheric balloon launched as part of the REXUS/BEXUS programme. Both BEXUS balloons lifted from SSC’s Esrange Space Centre in Arctic Sweden. 

Supported by German Aerospace Center (DLR), European Space Agency (ESA), the Swedish National Space Agency (SNSA), ZARM.

In different terminals run the ground and a master (there are different edition) programs.

	[+] Run ground program with one argument.
        [+] The argument indicates the ELinkManager IP
        [+] e.g python ground.py 195.168.0.1

        [+] For Testing purposes use 'local' as argument
        [+] to simulate a connection locally
        [+] e.g python ground.py local

	[+] Run master program with one argument.
        [+] The argument indicates the ground IP
        [+] e.g python master_esrange.py 195.168.0.1

        [+] For Testing purposes use 'local' as argument
        [+] to simulate a connection locally
        [+] e.g python master_esrange.py local

Editions of master:
	a) master_esrange.py: 
		simulates the full experiment procedure
	b) simulation_master_dmc_datamanager.py : 
		simulates only the DMC procedure
	c) simulation_master_adc_datamanager.py : 
		simulates only the ADC procedure
	d) simulation_master_heat_datamanager.py : 
		simulates only the HEAT procedure
	e) simulation_master_tx_datamanager.py : 
		simulates only the TX procedure

Available Commands from 'ground' terminal, when the other terminal is executed:
	a) master_esrange.py:
	    [+] DEP # to ask for deploy
            [+] DEP_CONF # to confirm for deploy - after DEP
            [+] DEP_AB # to abort deployment - after DEP
            [+] DEP_SUCS # to declare the successful deployment
            [+] DEP_RETRY #to retry the deployment
            [+] DMC_AWAKE # to wake up DMC
            [+] RET # to ask for retrieve
            [+] RET_CONF # to confirm for retrieve - after RET
            [+] RET_AB # to abort retrieve - after RET            
            [+] RET_SUCS # to declare the successful retrieve
            [+] RET_RETRY #to retry the retrieve
            [+] ADC_MAN #to change in manual ADC control
            [+] SET # set antenna's base in a specific step - operation of manual ADC only
            [+] SCAN # antenna's base turn 360 n back - operation of manual ADC only
            [+] ADC_AUTO #to recall auto mode of ADC control
            [+] HEAT_SLEEP #to force close the heating control
            [+] HEAT_AWAKE #to recall auto mode of heating control
	    [+] TX_SLEEP #to force close the transmission
            [+] TX_AWAKE #to recall auto mode of transmission
            [+] PRE #to transmit data from file with predetermined data
            [+] KILL #to kill program 
            
	b) simulation_master_dmc_datamanager.py :
	    [+] DEP # to ask for deploy
            [+] DEP_CONF # to confirm for deploy - after DEP
            [+] DEP_AB # to abort deployment - after DEP
            [+] DEP_SUCS # to declare the successful deployment
            [+] DEP_RETRY #to retry the deployment
            [+] DMC_AWAKE # to wake up DMC
            [+] RET # to ask for retrieve
            [+] RET_CONF # to confirm for retrieve - after RET
            [+] RET_AB # to abort retrieve - after RET            
            [+] RET_SUCS # to declare the successful retrieve
            [+] RET_RETRY #to retry the retrieve
            [+] KILL #to kill program 

	c) simulation_master_adc_datamanager.py : 
	    [+] ADC_MAN #to change in manual ADC control
            [+] SET # set antenna's base in a specific step - operation of manual ADC only
            [+] SCAN # antenna's base turn 360 n back - operation of manual ADC only
            [+] ADC_AUTO #to recall auto mode of ADC control
            [+] KILL #to kill program 
           
	d) simulation_master_heat_datamanager.py : 
	    [+] HEAT_SLEEP #to force close the heating control
            [+] HEAT_AWAKE #to recall auto mode of heating control
            [+] KILL #to kill program 

	e) simulation_master_tx_datamanager.py : 
	    [+] TX_SLEEP #to force close the transmission
            [+] TX_AWAKE #to recall auto mode of transmission
            [+] PRE #to transmit data from file with predetermined data
            [+] KILL #to kill program 
            
            

            
