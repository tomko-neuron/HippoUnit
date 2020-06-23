NEURON {
	POINT_PROCESS Exp2Syn_STDP_BCM_nearest_spike
	RANGE tau1, tau2, e, i, dtau, ptau
	RANGE wMax 	:hard bound 
	POINTER d, p	: depression/potentiation factor (additive, non-saturating)
	NONSPECIFIC_CURRENT i
	RANGE g, tpost, start, tpre, pathway, id
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

DEFINE EpspTimes 10000

PARAMETER {
	tau1=.1 (ms) <1e-9,1e9>
	tau2 = 10 (ms) <1e-9,1e9>
	e=0	(mV)
	dtau = 36 (ms) 			: depression effectiveness time constant (time it takes to fall from 1->0.37)
	ptau = 26 (ms) 			: Lin et al. (Eur J Neurosci 2006) dtau 36 ms, ptau 26 ms, Bi & Poo (1998, 2001) dtau 34 ms, ptau 17 ms
	wMax = 0.1 (uS)		: hard upper bound 
	start = 0 (ms)		: synapses are allowed to start changing after start ms
	pathway = -1
	id = -1
}

ASSIGNED {
	v (mV)
	i (nA)
	g (uS)
	factor
	tpost (ms)
	tpre (ms)
	presyntime[EpspTimes] (ms)	: array to store epsp times
	counter						: to count epsps until first post-AP comes
	total (uS)
	flagOLD
	d							: depression factor (multiplicative to prevent < 0)
	p							: potentiation factor (multiplicative)
}

STATE {
	A (uS)
	B (uS)
}

INITIAL {
	LOCAL tp
	total = 0
	if (tau1/tau2 > .9999) {
		tau1 = .9999*tau2
	}
	A = 0
	B = 0
	tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
	factor = -exp(-tp/tau1) + exp(-tp/tau2)
	factor = 1/factor
	tpost = -1
	tpre = -1

	FROM i=0 TO EpspTimes-1 {
		presyntime[i]=-1
	}
	counter = 0
	
:flag is an implicit argument to NET_RECEIVE. It is an integer, zero by default but a nonzero value can be specified via the second argument to :net_send(). net_send() is used to launch self-events. A self-event comes back to the mechanism that launched it, no NetCon required. 
	net_send(0, 1)
	flagOLD = 1
}

BREAKPOINT { 
	SOLVE state METHOD cnexp
	g = B - A
	i = g*(v - e)
}

DERIVATIVE state {
	A' = -A/tau1
	B' = -B/tau2
}

NET_RECEIVE(w (uS), wE (uS), tpre (ms), X) {
	INITIAL { wE = w  tpre = -1	 X=0 }
	
	if (flag == 0) { : presynaptic spike  (after last post so depress)
		:printf("presynaptic spike: id=%g entry flag=%g t=%g wInitial=%g wE=%g tpre=%g tpost=%g counter=%g\n", id, flag, t, w, wE, tpre, tpost, counter)
		A = A + wE*factor
		B = B + wE*factor
		tpre = t
		presyntime[counter] = tpre
		counter = counter + 1
		flagOLD = 0
	}
	else if (flag == 2){
		:printf("postsynaptic spike: id=%g entry flag=%g flagOLD=%g t=%g tpost=%g\n", id, flag, flagOLD, t, tpost)
		FOR_NETCONS(w1, wE1, tpres, X1){
			:printf("entry FOR_NETCONS w1=%g wE1=%g tpres=%g X1=%g\n", w1, wE1, tpres, X1)
			if (flagOLD == 0){
				if (tpost == -1){ :postsynaptic spike after the first presynaptic spike (no postsynaptic spike before presynaptic spike)
					FROM i=0 TO counter-1 {
						:printf("id=%g i=%g presyntime[i]=%g potentiation\n", id, i, presyntime[i])
						X1 = p*exp((presyntime[i] - t)/ptau)
						wE1 = wE1*(1+X1)
						presyntime[i] = -1
						:printf("id=%g wE=%g\n", id, wE1)
						if (wE1 > wMax){	:hard bounds 
							wE1 = wMax
						}
					}
					tpres = -1
					counter = 0
				}
				else{
					FROM i=0 TO counter-1 {
						if ((presyntime[i] - tpost) > (t - presyntime[i])){
							:printf("id=%g i=%g presyntime[i]=%g potentiation\n", id, i, presyntime[i])
							X1 = p*exp((presyntime[i] - t)/ptau)
							wE1 = wE1*(1+X1)
							:printf("id=%g wE=%g\n", id, wE1)
							if (wE1 > wMax){	:hard bounds 
								wE1 = wMax
							}
							presyntime[i] = -1
						}
						else {
							:printf("id=%g i=%g presyntime[i]=%g depression\n", id, i, presyntime[i])
							X1 = d*exp((tpost - presyntime[i])/dtau)
							wE1 = wE1*(1-X1)
							:printf("id=%g wE=%g\n", id, wE1)
							if (wE1<0) {	:hard bounds 
								wE1 = 0
							}
							presyntime[i] = -1
						}						
					}
					tpres = -1
					counter = 0
				}
				tpost = t
				flagOLD = 2
			}
		}
	}
	WATCH (v > -37) 2
}