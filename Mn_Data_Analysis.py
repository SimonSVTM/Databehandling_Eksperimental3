
from Data_Computing import Datarefactor as dr
from Data_Computing import PlotterLayout as pl
from Data_Computing import PlotterTypes as pt
from Data_Computing import Statistics as stat
from Data_Computing import Fitter as fitter
from Calibration import Calibration as cal
import numpy as np



data = dr.getNpyData("Manganese", "v3", "Data")
#data = dr.getNpyData("Calibration", "Ra_226", "Data")
print(data)
endtime = data[0][-1]
print(endtime)


def plot(xmin, xmax, guess, state, dt):
    expguess = [295494817, 13433.9]
    linguess =  [100, 40000]

    print('Energy:', xmin * 0.737954998884285 - 0.6469245416508275, ' to ', xmax * 0.737954998884285 - 0.6469245416508275)

    timeNode_root = dr.getTimeNode_root(data, xmin, xmax)

    ax = pl.start_plot(7, 4)
    # 1e9 < time < 1e12
    data_trimmed = timeNode_root.getStateByTime(endtime)

    var = data_trimmed[2]

    def linearGausianSum(X, a, b, A, mu, var):
        return a * X + b + stat.gaussian_sum(X, A, mu, var)

    data_cal = cal.getCalibratedData(data_trimmed, True)
    popt, pcov = fitter.getFit(data_trimmed, var, linearGausianSum, guess,  xmin = xmin, xmax = xmax)
    Emin = cal.channel_to_energy(data_trimmed[0][0])
    Emax = cal.channel_to_energy(data_trimmed[0][-1])

    c_gauss = cal.getGaussianCalMap()
    c_linear = cal.getLinearCalMap()

    popt[0] = c_linear[0](popt[0])
    popt[1] = c_linear[1](popt[1])
    popt[2] = c_gauss[0](popt[2])
    popt[3] = c_gauss[1](popt[3])
    popt[4] = c_gauss[2](popt[4])

    pt.plotAsLine(ax, [[Emin, Emax], [popt[0] * Emin + popt[1], popt[0] * Emax + popt[1]]], label='Background Noise', line_color = 'red')
    pt.plotGaussianWithLine(ax, popt, xmin = cal.channel_to_energy(xmin), xmax = cal.channel_to_energy(xmax), line_color='darkred', label='Transition fit')
    print('Params:', popt)
    print('Sigma:', np.sqrt(np.diag(pcov)))
    pt.plotErrorbars(ax, data_cal, var, marker_size=3)
    pl.setup_plot(ax, xlabel ='Energy [keV]', ylabel ='Efficiency Calibrated Counts ' + state, hasLegend=True, yaxis_sciNotation = True)

    '''
    ax = pl.start_plot(7, 4)
    # 1e9 < time < 1e12
    data_trimmed = timeNode_root.getStateByTime(dt)
    var = data_trimmed[2]

    def linearGausianSum(X, a, b, A, mu, var):
        return a * X + b + stat.gaussian_sum(X, A, mu, var)

    popt, pcov = pt.plotFit(ax, data_trimmed, var, linearGausianSum, guess,  xmin = xmin, xmax = xmax, label='Transition Fit', fit_color='coral')
    pt.plotAsLine(ax, [[Emin, Emax], [popt[0] * Emin + popt[1], popt[0] * Emax + popt[1]]], label='Background Noice', line_color = 'red')
    pt.plotErrorbars(ax, data_trimmed, var, marker_size=3)
    pl.setup_plot(ax, xlabel ='Energy [keV]', ylabel ='Efficiency Calibrated Counts', hasLegend=True)
    '''

    ax = pl.start_plot(7, 4)


    def Gaussian_Jacobian(x, A, mu, var):
        return np.array([1 / abs(A),
                         abs((x - mu)) / abs(var),
                         (x - mu) ** 2 / (2 * var ** 2)]) * stat.gaussian(x, A, mu, var)

    def getGauss_fitError(x, cov, params):
        j = Gaussian_Jacobian(x, params[0], params[1], params[2])
        return j.dot(np.array(cov).dot(np.transpose(j)))



    time = 5 * dt
    times = []
    cumul_counts = []
    vars = []


    counter = 1
    while time < endtime:
        data_trimmed = timeNode_root.getStateByTime(time)
        var = data_trimmed[2]

        popt, pcov = fitter.getFit(data_trimmed, var, linearGausianSum, guess, xmin = xmin, xmax = xmax)
        times.append(time / (1e8))
        cumul_counts.append(sum([stat.gaussian(x, popt[2], popt[3], popt[4]) for x in data_trimmed[0]]))
        var = [getGauss_fitError(x, pcov[2:, 2:], popt[2:]) for x in data_trimmed[0]]
        vars.append(sum(var))

        process = time / endtime * 100
        if process > counter * 5 - 1:
            print(str(int(process)) + '% done')
            counter += 1
        time += dt
    print('100 % Done')


    pt.plotErrorbars(ax, [times, cumul_counts], vars, marker_size=1, label = 'Data')
    popt, pcov = pt.plotFit(ax, [times, cumul_counts], vars, lambda X, N0, tau: N0 *(1 - np.exp(- X / tau)), expguess, fit_color='g', label='Theory fit')

    #popt, pcov = pt.plotFit(ax, [times, cumul_counts], vars, lambda X, a, b: a * X + b, linguess, fit_color='g', label='Line fit')

    pl.setup_plot(ax, xlabel ='Time [s]', ylabel ='Cumulative counts ' + state, hasLegend=True, yaxis_sciNotation = True)

    #ax.ticklabel_format(axis='y', style='sci', scilimits=(5, 5))




def plotHist(isCalibrated):
    print('Plotting Histogram')

    ax = pl.start_plot(7, 4)
    histdata = dr.convertToHistogram(data, column=1,xmin = 0, xmax=10000)
    vars = histdata[2]
    pt.plotErrorbars(ax, histdata, vars, marker_size=2, isCalibrated=isCalibrated, marker_color = 'darkorange')
    pl.setup_plot(ax, title='Test', xlabel='Energy [keV]', ylabel='Efficiency Calibrated Counts', xmin=0, xmax=10000, log_scale = True)
    ax.set_xticks(np.arange(0, 10000, 200))


def runGuesses(dt):
    #Photopeak:
    xmin = 1100
    xmax = 1200
    guess = [-1.46362345e+00,  1.81344846e+03,  1e+08,  1.14645192e+03, 1.51588102e+01]
    state = '$N_{10}$'
    plot(xmin, xmax, guess, state, dt)

    #Others:
    xmin = 2420
    xmax = 2480
    guess = [-1.46362345e+00,  1.81344846e+03,  1e+08,  2.45310163e+03, 1.51588102e+01]
    state = '$N_{31}$'
    plot(xmin, xmax, guess, state, dt)

    xmin = 3560
    xmax = 3640
    guess = [-1.46362345e+00,  1.81344846e+03,  1e+05,  3600, 1.51588102e+01]
    state = '$N_{30}$'
    plot(xmin, xmax, guess, state, dt)

    xmin = 3950
    xmax = 4050
    guess = [-1.46362345e+00,  1.81344846e+03,  1e+08,  4000, 1.51588102e+01]
    state = '$N_{40}$'
    plot(xmin, xmax, guess, state, dt)

    xmin = 2800
    xmax = 2940
    guess = [-1.46362345e+00,  1.81344846e+03,  1e+08,  2850, 1.51588102e+01]
    state = '$N_{41}$'
    plot(xmin, xmax, guess, state, dt)

    xmin = 4499
    xmax = 4625
    guess = [-1.46362345e+00,  1.81344846e+03,  1e+08,  4567, 1.51588102e+01]
    state = '$N_{60}$'
    plot(xmin, xmax, guess, state, dt)

    xmin = 3340
    xmax = 3475
    guess = [-1.46362345e+00,  1.81344846e+03,  1e+08,  3420, 1.51588102e+01]
    state = '$N_{61}$'
    plot(xmin, xmax, guess, state, dt)

    xmin = 3450
    xmax = 3580
    guess = [-1.46362345e+00,  1.81344846e+03,  1e+05,  3550, 1.51588102e+01]
    state = '$N_{71}$'
    plot(xmin, xmax, guess, state, dt)

def runWierdGuesses(dt):
    xmin = 1900
    xmax = 2060
    guess = [-1.46362345e+00, 1.81344846e+03, 1e+08, 1980, 1.51588102e+01]
    state = '$p_1$'

    plot(xmin, xmax, guess, state, dt)
    xmin = 2900
    xmax = 3150
    guess = [-1.46362345e+00, 1.81344846e+03, 1e+08, 3012, 1.51588102e+01]
    state = '$p_2$'
    plot(xmin, xmax, guess, state, dt)

    xmin = 3450
    xmax = 3580
    guess = [-1.46362345e+00, 1.81344846e+03, 1e+08, 3525, 1.51588102e+01]
    state = '$p_3$'
    plot(xmin, xmax, guess, state, dt)

dt = 1e10

#runWierdGuesses(dt)
runGuesses(dt)
#plotHist(True)

pl.show_plot()


