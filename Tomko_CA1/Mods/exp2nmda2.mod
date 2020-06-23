: NMDA synapse firing at onset time
: biexponential timecourse
: Mg block according to Jahr&Stevens
: Including NET_RECEIVE statement
: 2009 Roland Krueppel

COMMENT
synaptic current with exponential rise and decay conductance defined by
        i = g * (v - e)      i(nanoamps), g(micromhos);
        where
         g = 0 for t < onset and
         g=mgblock * amp * ((1-exp(-(t-onset)/tau0))-(1-exp(-(t-onset)/tau2)))
          for t > onset
Mg block according to Jahr and Stevens 1990
		mgblock(v) = 1 / (1 + eta * [Mg] * exp(-gamma * v))
ENDCOMMENT
					       
INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	POINT_PROCESS Exp2nmda2
	RANGE g, R, R0, onset, tau2, tau1, eta, gamma, shift, mg, gmax, e, Fire
	NONSPECIFIC_CURRENT i
}
UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
	(mM) = (milli/liter)
	(umho) = (micromho)
}

PARAMETER {
	tau2 = 40.0 (ms)
	tau1 = 0.33 (ms)
	eta = 0.33 (/mM)
	gamma = 0.06 (/mV)
	shift = 0
	mg = 1 (mM)
	gmax = 1 	 (uS)
	Fire = 0		: 0 precell did not fire, 1 fire in da hood
	
	e=0	 (mV)
}

ASSIGNED {
	v (mV)
	i (nA)
	g (uS)	: conductance
	R
	R0
	lastrelease (ms)	: time of last spike
}

INITIAL {
	lastrelease = -10
	R = 0
	R0 = 0
}

NET_RECEIVE ( weight (microsiemens) ) {
	Fire = 1
}

BREAKPOINT {
	SOLVE release
	g = gmax * R * mgblock(v)
	i = g * (v - e)
}

PROCEDURE release() {
	if ( Fire ) { :&& (abs(t - lastrelease) < 50) ) {
		lastrelease = t
		R0 = R
		Fire = 0
	}
	if ( lastrelease > 0 ) {
		R =  exptable(-(t-lastrelease)/tau2) - exptable(-(t-lastrelease)/tau1) + R0 * exptable(-(t-lastrelease)/tau1)
	}
	
	VERBATIM
	return 0;
	ENDVERBATIM
}

FUNCTION exptable(x) {
	TABLE  FROM -100 TO 0 WITH 2000
	if ( (x < 0) && (x > -100) ) {
		exptable = exp(x)
	} else {
		exptable = 0
	}
}

FUNCTION mgblock(v(mV)) {
	TABLE 
	DEPEND mg, gamma, eta, shift
	FROM -140 TO 80 WITH 1000

	mgblock = (1 / (1 + exp(-gamma * v) * (eta * mg))) + shift
}
