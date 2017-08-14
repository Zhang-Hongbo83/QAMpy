import numpy as np
import matplotlib.pylab as plt
from dsp import  equalisation, modulation, impairments
from dsp.signal_quality import cal_evm



fb = 40.e9
os = 2
fs = os*fb
N = 10**6
theta = np.pi/2.35
M = 32
QAM = modulation.QAMModulator(M)
snr = 25
muCMA = 1e-3
muRDE = 1.e-3
ntaps = 11
t_pmd = 20.e-12
#Ncma = N//4//os -int(1.5*ntaps)
Ncma = 10000
Nrde = N//2//os -int(1.5*ntaps)

S, symbols, bits = QAM.generate_signal(N, snr,  baudrate=fb, samplingrate=fs, PRBSorder=(15,23))

SS = impairments.apply_PMD_to_field(S, theta, t_pmd, fs)

E_m, wx_m, wy_m, err_m, err_rde_m = equalisation.FS_MCMA_MRDE(SS, Ncma, Nrde, ntaps, os, muCMA, muRDE, M)
E_s, wx_s, wy_s, err_s, err_rde_s = equalisation.FS_MCMA_SBD(SS, Ncma, Nrde, ntaps, os, muCMA, muRDE, M)
E, wx, wy, err, err_rde = equalisation.FS_MCMA_MDDMA(SS, Ncma, Nrde, ntaps, os, muCMA, muRDE, M)
#E, wx, wy, err, err_rde = equalisation.FS_CMA_RDE(SS, Ncma, Nrde, ntaps, os, muCMA, muRDE, M)
print("equalised")


evmX = cal_evm(S[0,::2], M)
evmY = cal_evm(S[1,::2], M)
evmEx = cal_evm(E[0], M)
evmEy = cal_evm(E[1], M)
evmEx_m = cal_evm(E_m[0], M)
evmEy_m = cal_evm(E_m[1], M)
evmEx_s = cal_evm(E_s[0], M)
evmEy_s = cal_evm(E_s[1], M)

#sys.exit()
plt.figure()
plt.subplot(221)
plt.title('Recovered MCMA/MDDMA')
plt.plot(E[0].real, E[0].imag, 'r.' ,label=r"$EVM_x=%.1f\%%$"%(evmEx*100))
plt.plot(E[1].real, E[1].imag, 'g.', label=r"$EVM_y=%.1f\%%$"%(100*evmEy))
plt.legend()
plt.subplot(222)
plt.title('Recovered MCMA/MRDE')
plt.plot(E_m[1].real, E_m[1].imag, 'g.', label=r"$EVM_y=%.1f\%%$"%(100*evmEy_m))
plt.plot(E_m[0].real, E_m[0].imag, 'r.' ,label=r"$EVM_x=%.1f\%%$"%(evmEx_m*100))
plt.legend()
plt.subplot(223)
plt.title('Recovered MCMA/SBD')
plt.plot(E_s[1].real, E_s[1].imag, 'g.', label=r"$EVM_y=%.1f\%%$"%(100*evmEy_s))
plt.plot(E_s[0].real, E_s[0].imag, 'r.' ,label=r"$EVM_x=%.1f\%%$"%(evmEx_s*100))
plt.legend()
plt.subplot(224)
plt.title('Original')
plt.plot(S[0,::2].real, S[0,::2].imag, 'r.', label=r"$EVM_x=%.1f\%%$"%(100*evmX))
plt.plot(S[1,::2].real, S[1,::2].imag, 'g.', label=r"$EVM_y=%.1f\%%$"%(100*evmY))
plt.legend()

plt.figure()
plt.subplot(331)
plt.title('CMA/MDDMA Taps')
plt.plot(wx[0,:], 'r')
plt.plot(wx[1,:], '--r')
plt.plot(wy[0,:], 'g')
plt.plot(wy[1,:], '--g')
plt.subplot(332)
plt.title('CMA/MDDMA error cma')
plt.plot(abs(err[0]), color='r')
plt.plot(abs(err[1])- 10, color='g')
plt.subplot(333)
plt.title('CMA/MDDMA error MDDMA')
plt.plot(abs(err_rde[0]), color='r')
plt.plot(abs(err_rde[1])-10, color='g')
plt.subplot(334)
plt.title('MCMA/MRDE Taps')
plt.plot(wx_m[0,:], 'r')
plt.plot(wx_m[1,:], '--r')
plt.plot(wy_m[0,:], 'g')
plt.plot(wy_m[1,:], '--g')
plt.subplot(335)
plt.title('MCMA/MRDE error cma')
plt.plot(abs(err_m[0]), color='r')
plt.plot(abs(err_m[1])- 10, color='g')
plt.subplot(336)
plt.title('MCMA/MRDE error rde')
plt.plot(abs(err_rde_m[0]), color='r')
plt.plot(abs(err_rde_m[1])-10, color='g')
plt.subplot(337)
plt.title('MCMA/SBD Taps')
plt.plot(wx_s[0,:], 'r')
plt.plot(wx_s[1,:], '--r')
plt.plot(wy_s[0,:], 'g')
plt.plot(wy_s[1,:], '--g')
plt.subplot(338)
plt.title('MCMA/SBD error cma')
plt.plot(abs(err_s[0]), color='r')
plt.plot(abs(err_s[1])- 10, color='g')
plt.subplot(339)
plt.title('MCMA/SBD error rde')
plt.plot(abs(err_rde_s[0]), color='r')
plt.plot(abs(err_rde_s[1])-10, color='g')
plt.show()


