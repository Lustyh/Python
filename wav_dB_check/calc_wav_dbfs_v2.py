"""
python calc_wav_dbfs_2.py <wav_file_name> <frequency>
Args:
    wav_file_name: wav file path.
    frequency:
        input: 'all' or integer (if more than one integers, please separate then
                                 by '-').
        default: all
                You can check the spectrum of all frequency.
        If need to check the sensitivity of the specific frequency, please input integers.
        ex: 1000 or 5000 or 1000-5000-100000
"""

import json
import numpy as np
import scipy.io.wavfile as wf
import sys
import matplotlib.pyplot as plt

#plt.close('all')

def dbfft(x, fs, win=None, ref=32768):
    """
    Calculate spectrum in dB scale
    Args:
        x: input signal
        fs: sampling frequency
        win: vector containing window samples (same length as x).
             If not provided, then rectangular window is used by default.
        ref: reference value used for dBFS scale. 32768 for int16 and 1 for float

    Returns:
        freq: frequency vector
        s_db: spectrum in dB scale
    """

    N = len(x)  # Length of input sequence
    # print('[N]:',N)
    if win is None:
        win = np.ones(1, N)
    if len(x) != len(win):
            raise ValueError('Signal and window must be of the same length')
    x = x * win
    # Calculate real FFT and frequency vector
    sp = np.fft.rfft(x)
    freq = np.arange((N / 2) + 1) / (float(N) / fs)

    # Scale the magnitude of FFT by window and factor of 2,
    # because we are using half of FFT spectrum.
    s_mag = 2*np.abs(sp) / np.sum(win)

    # Convert to dBFS
    s_dbfs = 20 * np.log10(s_mag/ref)

    return freq, s_dbfs


# =============================================================================
# Main Code
# =============================================================================
def main():
    # print(sys.argv)
    if len(sys.argv) < 2:
        print ('usage:')
        print ('=> ' + sys.argv[0] + ' <wav_file_name> <frequency>')
        exit()
    elif len(sys.argv) == 2:
        check_frequency = 'all'
    elif len(sys.argv) == 3:
        try: 
            check_frequency = sys.argv[2]
            if sys.argv[2] != 'all':
                check_frequency = sys.argv[2].split('-')
        except:
            print ('usage:')
            print ('=> ' + sys.argv[0] + ' <wav_file_name> <frequency>')
            exit()
		
    # Load the file
    fs, signal = wf.read(sys.argv[1])
    # print('fs->')
    # print(fs)
    # print(f"singal:\n{signal}")
    
    try:
        chanel_size = int(str(np.size(signal, 1))[0])
    except:
        chanel_size = 1
    #F = 32768
    #F = 65536
    F = 96000
    # print('chanel_sie:',chanel_size)
    if chanel_size == 1:
        signal_type = type(signal[0])
    else:
        signal_type = type(signal[0][0])
    if signal_type is np.int32 or signal_type is np.int16:
        ref = 32768
    elif signal_type is np.float32:
        ref = 1

    if chanel_size == 1:
        if signal_type is np.float32 or signal_type is np.int16:
            signal_ch0 = signal
        elif signal_type is np.int32:
            signal_ch0 = []
            signal = np.fromstring(signal, np.dtype([('ch0_fraction', np.int16), ('ch0_integer', np.int16)]))
            for x in range(0, len(signal)):
                ch0_value = float(signal[x][0])/F + signal[x][1]
                signal_ch0.append(ch0_value)

    elif chanel_size == 2:
        if signal_type is np.float32 or signal_type is np.int16:
            signal_ch0 = signal[:, 0]
            signal_ch1 = signal[:, 1]
        elif signal_type is np.int32:
            signal_ch0 = []
            signal_ch1 = []
            signal = np.fromstring(signal, np.dtype([('ch0_fraction', np.int16), ('ch0_integer', np.int16), 
                                                     ('ch1_fraction', np.int16), ('ch1_integer', np.int16)]))
            for x in range(0, len(signal)):
                ch0_value = float(signal[x][0])/F + signal[x][1]
                ch1_value = float(signal[x][2])/F + signal[x][3]
                signal_ch0.append(ch0_value)
                signal_ch1.append(ch1_value)

    elif chanel_size == 3:
        if signal_type is np.float32 or signal_type is np.int16:
            signal_ch0 = signal[:, 0]
            signal_ch1 = signal[:, 1]
            signal_ch2 = signal[:, 2]
        elif signal_type is np.int32:
            signal_ch0 = []
            signal_ch1 = []
            signal_ch2 = []
            signal = np.fromstring(signal, np.dtype([('ch0_fraction', np.int16), ('ch0_integer', np.int16), 
                                                     ('ch1_fraction', np.int16), ('ch1_integer', np.int16), 
                                                     ('ch2_fraction', np.int16), ('ch2_integer', np.int16)]))		
            for x in range(0, len(signal)):
                ch0_value = float(signal[x][0])/F + signal[x][1]
                ch1_value = float(signal[x][2])/F + signal[x][3]
                ch2_value = float(signal[x][4])/F + signal[x][5]
                signal_ch0.append(ch0_value)
                signal_ch1.append(ch1_value)
                signal_ch2.append(ch2_value)

    elif chanel_size == 4:
        if signal_type is np.float32 or signal_type is np.int16:
            signal_ch0 = signal[:, 0]
            signal_ch1 = signal[:, 1]
            signal_ch2 = signal[:, 2]
            signal_ch3 = signal[:, 3]
        elif signal_type is np.int32:
            signal_ch0 = []
            signal_ch1 = []
            signal_ch2 = []
            signal_ch3 = []
            signal = np.fromstring(signal, np.dtype([('ch0_fraction', np.int16), ('ch0_integer', np.int16), 
                                                     ('ch1_fraction', np.int16), ('ch1_integer', np.int16), 
                                                     ('ch2_fraction', np.int16), ('ch2_integer', np.int16), 
                                                     ('ch3_fraction', np.int16), ('ch3_integer', np.int16)]))		
            for x in range(0, len(signal)):
                ch0_value = float(signal[x][0])/F + signal[x][1]
                ch1_value = float(signal[x][2])/F + signal[x][3]
                ch2_value = float(signal[x][4])/F + signal[x][5]
                ch3_value = float(signal[x][6])/F + signal[x][7]
                signal_ch0.append(ch0_value)
                signal_ch1.append(ch1_value)
                signal_ch2.append(ch2_value)
                signal_ch3.append(ch3_value)
            
# =============================================================================
# Calculate Sensitivity for each chanel
# =============================================================================
    #N = 8192
    #N = F/2
    N = 48000
    if np.size(signal, 0) < N:
        N = np.size(signal, 0)
    
    win = np.hanning(N)
    freq, s_dbfs_1 = dbfft(signal_ch0[0:N], fs, win, ref)
    if chanel_size == 2:
        freq, s_dbfs_2 = dbfft(signal_ch1[0:N], fs, win, ref)
    elif chanel_size == 3:
        freq, s_dbfs_2 = dbfft(signal_ch1[0:N], fs, win, ref)
        freq, s_dbfs_3 = dbfft(signal_ch2[0:N], fs, win, ref)
    elif chanel_size == 4:
        freq, s_dbfs_2 = dbfft(signal_ch1[0:N], fs, win, ref)
        freq, s_dbfs_3 = dbfft(signal_ch2[0:N], fs, win, ref)
        freq, s_dbfs_4 = dbfft(signal_ch3[0:N], fs, win, ref)
    
# =============================================================================
#   Print the sensitivity of spesific freqency
# =============================================================================
    dbfs_ch0 = []
    if chanel_size == 2:
        dbfs_ch1 = []
    elif chanel_size == 3:
        dbfs_ch1 = []
        dbfs_ch2 = []
    elif chanel_size == 4:
        dbfs_ch1 = []
        dbfs_ch2 = []
        dbfs_ch3 = []
    for x in range(len(check_frequency)):
        dbfs_ch0.append(-300.0)
        if chanel_size == 2:
            dbfs_ch0.append(-300.0)
            dbfs_ch1.append(-300.0)
        elif chanel_size == 3:
            dbfs_ch1.append(-300.0)
            dbfs_ch2.append(-300.0)
        elif chanel_size == 4:
            dbfs_ch1.append(-300.0)
            dbfs_ch2.append(-300.0)
            dbfs_ch3.append(-300.0)
    
    if sys.argv[2] != 'all':
        for x in range(0, len(freq)):
            for y in range(len(check_frequency)):
                if freq[x] > int(check_frequency[y])-10 and freq[x] < int(check_frequency[y])+10:
#                    print 'freq: %f, sensitivity:%f' %(freq[x], s_dbfs_2[x])
                    dbfs_ch0[y] = s_dbfs_1[x] if s_dbfs_1[x] > dbfs_ch0[y] else dbfs_ch0[y]
                    if chanel_size == 2:
                        dbfs_ch1[y] = s_dbfs_2[x] if s_dbfs_2[x] > dbfs_ch1[y] else dbfs_ch1[y]
#                        print 'freq: %f, sensitivity_ch1:%f, sensitivity_ch1:%f' %(freq[x], s_dbfs_1[x], s_dbfs_2[x])
                    elif chanel_size == 4:
                        dbfs_ch1[y] = s_dbfs_2[x] if s_dbfs_2[x] > dbfs_ch1[y] else dbfs_ch1[y]
                        dbfs_ch2[y] = s_dbfs_3[x] if s_dbfs_3[x] > dbfs_ch2[y] else dbfs_ch2[y]
                        dbfs_ch3[y] = s_dbfs_4[x] if s_dbfs_4[x] > dbfs_ch3[y] else dbfs_ch3[y]
        
        result = []
        for x in range(len(check_frequency)):
            tmp = [{'Channel_No': 1, 'Sensitivity': dbfs_ch0[x]}]
            if chanel_size == 2:
                tmp += [{'Channel_No': 2, 'Sensitivity': dbfs_ch1[x]}]
            elif chanel_size == 4:
                tmp += [{'Channel_No': 2, 'Sensitivity': dbfs_ch1[x]},
                        {'Channel_No': 3, 'Sensitivity': dbfs_ch2[x]}, 
                        {'Channel_No': 4, 'Sensitivity': dbfs_ch3[x]}]
            result += [{'OutputSensitivity': tmp, 'Frequency': int(check_frequency[x])}]
        result = {'CalResult': result}
        
        encodedjson =  json.dumps(result)
        print(encodedjson)
        
        
    else:
        ## Save spectrum data
        file_name = '%s_dBFS_result.txt' %(sys.argv[1].split('.wav')[0])
        f = open(file_name, 'w')
        result = '\"freq\"\t\"ch 1\"'
        if chanel_size == 2:
            result += '\t\"ch 2\"'
        elif chanel_size == 3:
            result += '\t\"ch 2\"\t\"ch 3\"'
        elif chanel_size == 4:
            result += '\t\"ch 2\"\t\"ch 3\"\t\"ch 4\"'
        f.write(result)
        for x in range(0, len(freq)):
            result = '\n' + str(float('{0:.2f}'.format(freq[x]))) + '\t' + str(float('{0:.2f}'.format(s_dbfs_1[x])))
            if chanel_size == 2:
                result += '\t' +  str(float('{0:.2f}'.format(s_dbfs_2[x])))
            elif chanel_size == 3:
                result += '\t' +  str(float('{0:.2f}'.format(s_dbfs_2[x]))) + '\t' +  str(float('{0:.2f}'.format(s_dbfs_3[x])))
            elif chanel_size == 4:
                result += '\t' +  str(float('{0:.2f}'.format(s_dbfs_2[x]))) + '\t' +  str(float('{0:.2f}'.format(s_dbfs_3[x]))) + '\t' +  str(float('{0:.2f}'.format(s_dbfs_4[x])))
            f.write(result)
        f.close()
        print(file_name)
    
    exit()

if __name__ == "__main__":
    main()