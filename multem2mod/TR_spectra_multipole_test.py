import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess

def create_input(npts, theta, fi, zinf, zsup, polar, lmax, r_ratio):

    #-------------------------------- input file for Sylvia Swiecicki(2017) ---------------------------------

    str = ('           ********************************************\n'
           '           ********INPUT FILE FOR TRANSMISSION*********\n'
           '           ********************************************\n'
           '   KTYPE = 1   KSCAN = 2   KEMB  = 0    LMAX ='+'%2i'%(lmax)+'   NCOMP = 1   NUNIT = 1\n'
           ' ALPHA =    1.000000  BETA =    1.000000   FAB =   60.000000  RMAX =   30.000000\n'
           '  NP ='+'%4i'%(npts)+'  ZINF =  '+
           '%11.8f'%(zinf)
           +'  ZSUP =  '+'%12.9f'%(zsup)+'\n'
           '  THETA/AK(1) =  '+'%11.8f'%(theta)+'     FI/AK(2) =  '+'%11.8f'%(fi)+'   POLAR ='+polar+'     FEIN =   0.00\n'
           '\n'
           'Give information for the "NCOMP" components \n'
           '\n'
           '     IT  = 2\n'
           '     MUMED =   1.00000000   0.00000000     EPSMED=   2.10250000   0.00000000\n'
           '   NPLAN = 1  NLAYER = 1\n'
                                                                                    #AU at 0.7560 um eps = -20.1480000  1.24700000 
                                                                                    #AU at 0.9 um eps = -32.7190000    1.99550000
                                                                                    #AU at 0.65 um eps = -12.9530000   1.12090000
           '       S =   '+'%10.8f'%(r_ratio)+'     MUSPH =   1.00000000   0.00000000     EPSSPH=  '+'%11.8f'%(epssph_re)+'   '+'%11.8f'%(epssph_im)+'\n'
           'xyzDL 0.0  0.0  0.0\n'
           'xyzDR 0.0  0.0  1.0\n'
           '     MUEMBL=   1.00000000   0.00000000    EPSEMBL=   2.10250000   0.00000000\n'
           '     MUEMBR=   1.00000000   0.00000000    EPSEMBR=   2.10250000   0.00000000\n')

    with open('fort.10','w') as f:
        print(str, file=f)


def eval(i):
    create_input(npts, np.arcsin(theta[i])*180/np.pi, fi, zinf, zsup, polar, lmax, r_ratio)
    if os.path.isfile('multem2'):
        my_env = os.environ.copy()
        my_env["OMP_NUM_THREADS"] = "1"
        subprocess.run(['./multem2'],
                       stdout=subprocess.DEVNULL,
                       env=my_env)
    #FREQUENCY   TRANSMITTANCE  Reflectance   Absorbance
    d = np.loadtxt('fort.8').T
    data_arr[i,:] = d[:,1]


if __name__ == "__main__":
    plt.figure(figsize=(11,6))

    # 1 for single spectra calc 0 - for several
    regime = 0


    #defining x-axis
    from_sin_theta = 0.0
    to_sin_theta = 1.0
    n_theta = 200

    #input data
    # 900 nm
    # lambda_incident = 900
    # epssph_re = -32.7190000
    # epssph_im = 1.99550000

    # 750 nm
    lambda_incident = 750
    epssph_re = -20.1480000
    epssph_im = 1.24700000

    # 650 nm
    # lambda_incident = 650
    # epssph_re = -12.9530000
    # epssph_im = 1.12090000

    a = 475
    s = 100
    r_ratio = s/a
    npts = 2
    lmax= 7
    polar='S' # S or P
    theta = np.linspace(from_sin_theta, to_sin_theta, n_theta)
    kpts = len(theta)
    fi = 0


    data_arr = np.empty((kpts, 4))

    if regime:
        zinf = lambda_incident/a
        zsup = (lambda_incident+0.01)/a

        # if s_m:
        #     data_arr_with_m = np.empty((2*order+1, kpts, 4))
        #     m = 0
        #     for m_numb in range(-order, order+1, 1):
        #         print(m_numb, 'projection is calculating')
        #         for i in range(kpts):
        #             print(i+1, 'of', kpts)
        #             eval(i)
        #             data_arr_with_m[m, :, :] = data_arr
        #         m += 1


        #     x = np.linspace(from_sin_theta, to_sin_theta, kpts)
        #     # m = 0
        #     # for m_numb in range(-order, order+1, 1):
        #     #     plt.plot(x, data_arr_with_m[m,:,2], label='refl m=%i'%m_numb, lw=0.5)
        #     #     m += 1
        #     # plt.plot(x, data_arr_with_m[0,:,2]+data_arr_with_m[1,:,2]+data_arr_with_m[2,:,2], label='refl total', lw=2.0)
        #     # # plt.plot(x, data_arr_with_m[1,:,2], label='Pz', lw=2.0)
        #     plt.plot(x, data_arr_with_m[0,:,2]+data_arr_with_m[2,:,2], label='Ps', lw=2.0)
        #     # plt.plot(x, data_arr_with_m[0,:,2]-data_arr_with_m[2,:,2], label='Pk', lw=2.0)
        #     plt.ylim(-0.01,1.01)
        #     plt.legend()
        #     plt.tight_layout()
        #     plt.show()
        #     # plt.savefig('')
        #
        # else:
        #     m_numb = -10
        #     for i in range(kpts):
        #
        #         print(i+1, 'of', kpts)
        #         eval(i)
        #
        #     data_arr = data_arr.transpose()
        #     x = np.linspace(from_sin_theta, to_sin_theta, kpts)
        #     # plt.plot(x, data_arr[1], label='trans lmax=%i'%lmax, lw=1.0)
        #     plt.plot(x, data_arr[2], label='refl', lw=1.0)
        #     # plt.plot(x, data_arr[3], label='absorb', lw=1.0)
        #     # plt.plot(x, (data_arr[1]+data_arr[2]+data_arr[3]-1)*1e5, label='(trans+refl_absorb-1)*1e5', lw=0.4)
        #     plt.ylim(-0.01,1.01)
        #     plt.legend()
        #     plt.tight_layout()
        #     plt.show()
        #     # plt.savefig(f'lmax{lmax}__s_ord{s_ord}__order{order}__s_type{s_type}__type{type}.png')
        #

    else:
        #-----------   SYLVIA D. PHYS.R.B FIG.4 P.6 -----------------------------
        lambda_incident_arr = [650, 750, 900]
        epssph_re_arr = [-12.9530000, -20.1480000, -32.7190000]
        espsph_im_arr  = [1.12090000, 1.24700000, 1.99550000]
        data_arr_for_several_calc = np.empty((len(lambda_incident_arr), kpts, 4))
        m_numb = -10
        for n in range(len(lambda_incident_arr)):
            lambda_incident = lambda_incident_arr[n]
            zinf = lambda_incident/a
            zsup = (lambda_incident+0.01)/a
            epssph_re = epssph_re_arr[n]
            epssph_im = espsph_im_arr[n]
            for i in range(kpts):
                print(i+1, 'of', kpts)
                eval(i)
            data_arr_for_several_calc[n, :, :] = data_arr
            # data_arr = data_arr.transpose()
            x = np.linspace(from_sin_theta, to_sin_theta, kpts)
                # plt.plot(x, data_arr[1], label='trans lmax=%i'%lmax, lw=1.0)
            # plt.plot(x, data_arr[2]+n, label='refl', lw=1.0)
            plt.plot(x, data_arr_for_several_calc[n, :, 2] + n, label='refl lambda=%i'%lambda_incident, lw = 2.0)
            # data_arr = np.empty
                # plt.plot(x, (data_arr[1]+data_arr[2]-1)*1e1, label='(trans+refl-1)*1e1', lw=0.4)
            plt.ylim(-0.01,3.01)
            plt.legend()
            plt.tight_layout()
                # plt.show()
                # plt.savefig(f'lmax{lmax}__s_ord{s_ord}__order{order}__s_type{s_type}__type{type}.png')
        plt.show()