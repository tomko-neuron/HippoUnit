#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _BCMthreshold_reg();
extern void _Exp2SynSTDP_multNNb_globBCM_intscount_precentred_reg();
extern void _Exp2Syn_STDP_BCM_nearest_spike_reg();
extern void _NMDA_CA1_pyr_SC_reg();
extern void _STDPE2Syn_reg();
extern void _cacum_reg();
extern void _cagk_reg();
extern void _cal2_reg();
extern void _can2_reg();
extern void _cat_reg();
extern void _exp2nmda2_reg();
extern void _h_reg();
extern void _kad_reg();
extern void _kaprox_reg();
extern void _kca_reg();
extern void _kdrca1_reg();
extern void _kmb_reg();
extern void _my_exp2syn_reg();
extern void _naxn_reg();
extern void _nmda_reg();
extern void _vecevent_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," BCMthreshold.mod");
fprintf(stderr," Exp2SynSTDP_multNNb_globBCM_intscount_precentred.mod");
fprintf(stderr," Exp2Syn_STDP_BCM_nearest_spike.mod");
fprintf(stderr," NMDA_CA1_pyr_SC.mod");
fprintf(stderr," STDPE2Syn.mod");
fprintf(stderr," cacum.mod");
fprintf(stderr," cagk.mod");
fprintf(stderr," cal2.mod");
fprintf(stderr," can2.mod");
fprintf(stderr," cat.mod");
fprintf(stderr," exp2nmda2.mod");
fprintf(stderr," h.mod");
fprintf(stderr," kad.mod");
fprintf(stderr," kaprox.mod");
fprintf(stderr," kca.mod");
fprintf(stderr," kdrca1.mod");
fprintf(stderr," kmb.mod");
fprintf(stderr," my_exp2syn.mod");
fprintf(stderr," naxn.mod");
fprintf(stderr," nmda.mod");
fprintf(stderr," vecevent.mod");
fprintf(stderr, "\n");
    }
_BCMthreshold_reg();
_Exp2SynSTDP_multNNb_globBCM_intscount_precentred_reg();
_Exp2Syn_STDP_BCM_nearest_spike_reg();
_NMDA_CA1_pyr_SC_reg();
_STDPE2Syn_reg();
