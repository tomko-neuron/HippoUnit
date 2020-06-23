: simple first-order model of calcium dynamics
: Modified on Feb 22th 2018 based on Boening et al 2014.

NEURON {
	SUFFIX cadyn_new
	USEION ca READ cai,ica WRITE cai 
	RANGE  ca 
	GLOBAL depth,cainf,taur 
     
}

UNITS {
	(molar) = (1/liter)		
	(mM)    = (milli/liter)
	(um)	= (micron) 
	(mA)    = (milliamp)
	(msM)	= (ms mM)  
	FARADAY = (faraday) (coul)
}

PARAMETER {
	depth	= .1	(um)		
	taur    =  200  (ms)	: rate of calcium removal for stress conditions
	cainf	= 50e-6 (mM)	: changed oct2
	cai		        (mM)
}

ASSIGNED {
	ica		      (mA/cm2)
	diam          (um)
	VSR           (um)
	B             (mM*cm2/mA) 
	drive_channel (mM/ms)
}

STATE {
	ca (mM) 
}

BREAKPOINT {
	SOLVE state METHOD euler
}

DERIVATIVE state {
	drive_channel =  - ica * B

	if (drive_channel <= 0.) {
		: cannot pump inward
		drive_channel = 0.
	}
    : Differential equation
    ca' = drive_channel/18 + (cainf -ca)/taur*11
    : Initial Value
	cai = ca
}

INITIAL {
: if diameter gets less than double the depth, 
: the surface to volume ratio (here volume to surface ratio VSR)
: cannot be less than 1/(0.25diam) (instead of diam/(d*(diam-d)) )
	if (2*depth >= diam) {
		VSR = 0.25 * diam 
	} else {
		VSR = depth * ( 1 - depth/diam)
	}

	B  = (1e4) / (2*FARADAY*VSR)
	ca = cainf
}
