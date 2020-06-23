TITLE nap

COMMENT
Sodium Channels in AP Initiation of CA1 Pyramidal Neurons (Royeck et al. 2008)
ENDCOMMENT

NEURON {
	SUFFIX nap
	USEION na READ ena WRITE ina
	RANGE  gbar, timestauh, timestaum, shifttaum, shifttauh, thegna
	GLOBAL minf, mtau 

}

PARAMETER {
	gbar = .0052085   	(mho/cm2)
	
	:q10m=3.1
	:q10h=2.3
	
	timestauh=1
	timestaum=1
	shifttaum=1
	shifttauh=1
	
	
	eNa = 55 	(mV)		:Golomb et al.
	ena		(mV)            : must be explicitly def. in hoc
	celsius (degC)
	v 		(mV)
}


UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(pS) = (picosiemens)
	(um) = (micron)
} 

ASSIGNED {
	ina 		(mA/cm2)
	thegna		(mho/cm2)
	minf 		:hinf 		
	mtau (ms)	:htau (ms) 	
}
 

STATE { m }


UNITSOFF

BREAKPOINT {
    SOLVE states METHOD cnexp
	mtau = 1
	minf = (1/(1+exp(-(v+52.3)/6.8))) :midpoint -56.3, slope 7.4	        		
	
	thegna =gbar*m       

	ina = thegna * (v - eNa)
	} 

INITIAL {

	mtau = 1
	minf = (1/(1+exp(-(v+52.3)/6.8))) :midpoint - 52.3 slope 6.8	5.5	        	
	m=minf  

}

DERIVATIVE states {   
  
	mtau = 1
	minf = (1/(1+exp(-(v+52.3)/6.8))) :midpoint - 52.3 (47) slope 6.8	         	
	m' = (minf-m)/mtau


}



UNITSON