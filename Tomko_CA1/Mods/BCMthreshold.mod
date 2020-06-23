COMMENT

This is a mechanism for computing sliding BCM threshold based on recent spike count (Benuskova et al. PNAS 2001, Benuskova and Abraham JCNS 2007):

alpha_scount_d = alpha_d * scount for depression
alpha_scount_p = alpha_p * scount for potentiation

The averaged postsynaptic activity scount expresses the weighted
average of the postsynaptic spike count, with the most recent
spikes entering the sum with bigger weight than previous
ones. 

output = 1, if there is a postsynaptic spike
at a given time, output = 0, otherwise.

alpha_d, alpha_p are scaling constants.

scounttau is the averaging time constant for calculation of alpha_scount.

The mechanism should be inserted into soma to calculate the value of alpha_scount and thereby of d and p for all synaptic point processes which use d, p as POINTER variables.
At the hoc level d and p have to be set up as POINTER variables to allow the synaptic point process to know the d and p value. Here is an example
for setting up POINTER variables for a synaptic object syn: 

setpointer syn.d, d_BCMthreshold
setpointer syn.p, p_BCMthreshold

ENDCOMMENT

NEURON {
	POINT_PROCESS BCMthreshold
	RANGE d0, p0, scount0, scounttau, alpha_d, alpha_p
	RANGE d, p, tspike, alpha_scount_d, alpha_scount_p, scount
}

UNITS {
	(mV) = (millivolt)
}

PARAMETER {
	
	d0		: initial value for the depression factor (additive, non-saturating)
	p0		: initial value for the potentiation factor (additive, non-saturating)

	scounttau  		: averaging time constant for postsynaptic spike count, e.g. 12000 ms
	alpha_d			: scaling constant
	alpha_p			: scaling constant
	
	scount0 		: initial scount = 0 
	boltzman = 1	: initial boltzman = 0 (from Luba)

}

ASSIGNED {
	v (mV)
	flagOLD
	
	alpha_scount_d	: scount scaled by alpha_d - sliding (scount-dependent) modification threshold for depression
	alpha_scount_p	: scount scaled by alpha_p - sliding (scount-dependent) modification threshold for potentiation
	d			: depression factor (multiplicative to prevent < 0)
	p			: potentiation factor (multiplicative)
	boltzfactor 	: from Luba
	pf				: from Luba
	output			: from Luba
	tspike (ms)
}
STATE {
	scount			: counter for postsynaptic spikes
}
INITIAL {
	
	tspike = 0 :-100000
	
:flag is an implicit argument to NET_RECEIVE. It is an integer, zero by default but a nonzero value can be specified via the second argument to
:net_send(). net_send() is used to launch self-events. A self-event comes back to the mechanism that launched it, no NetCon required. 

	net_send(0, 1)
	flagOLD = 1
	scount = scount0
	d = d0		
	p = p0
	alpha_scount_d = alpha_d * scount
	alpha_scount_p = alpha_p * scount
	boltzfactor = exp( - 1.0 / scounttau)
	if(boltzman == 0) {pf = 1.0 / (1 - boltzfactor)} else {pf = 1.0}
	output = 0
}

BREAKPOINT { 
	:if (output > 0) {printf("entry time=%g output=%g\n", t, output)}
	scount = scount  + output*output/pf
	SOLVE state METHOD cnexp								:credit to Steffen Platschek
  	pf = pf * boltzfactor + 1.0
  	alpha_scount_d = alpha_d * scount							:scount scaled by alpha
	alpha_scount_p = alpha_p * scount							:scount scaled by alpha
	
	if (alpha_scount_d > 0) {
		d = d0 * alpha_scount_d
	} else {
		d = d
	}
	
	if (alpha_scount_p > 0) {
		p = p0 / alpha_scount_p
	} else {
		p = p
	}
	
	:d = d0
	:p = p0
    output = 0
}

DERIVATIVE state{
	scount' = -scount / pf
}

:The items in the argument list in the NET_RECEIVE statement of a synaptic mechanism are actually the elements of a
:weight vector. The first element, which is called nc.weight[0],
:corresponds to the first item in the NT_RECEIVE argument list--w--which remains constant during a simulation.
:The second element is called nc.weight[1], and it corresponds to wE.
:The value of this second element DOES change as a consequence of STDP.

NET_RECEIVE(w) {		:w is actually not needed for computations
	INITIAL {w=0}

:When a presynaptic spike occurs, the mechanism receives an event with flag == 0. 
:The printf statements are purely for diagnostic purposes and can be commented out.

	if (flag == 0) {
		output = 0 			:no postsynaptic spike
	} else if (flag == 2) { 	: postsynaptic spike
		tspike = t				: just in case one needs time of the spike
		output = 1				:postsynaptic spike 
		:printf("output=%g at time t=tspike=%g\n", scount, tspike)
	} else { : flag == 1 from INITIAL block

		:printf("entry flag=%g t=%g\n", flag, t)

:WATCH (var > thresh) flagvalue is used in a NET_RECEIVE block to specify a condition in the postsynaptic cell
:that will generate a self-event with latency 0 and a specified flag value. Generally, WATCH is used to make NEURON
:monitor a variable for threshold crossing, and generates a self event with the specified flag value when the threshold
:is crossed. If the postsynaptic cell is a biophysical model cell, var is usually local membrane potential (or cai or some
:other concentration); if the postsynaptic cell is an artificial spiking cell, var is one of that cell's state variables.
:But WATCH could in principle be anything, such as the total number of spikes that a cell has fired, or perhaps even t (time)

		WATCH (v > -37) 2 :This mechanism watches postsynaptic membrane potential at the location of the mechanism
						:When a postsynaptic spike occurs, the mechanism receives an event with flag == 2
	}
}






