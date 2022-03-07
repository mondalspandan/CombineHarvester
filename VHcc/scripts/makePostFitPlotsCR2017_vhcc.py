import os

CHN_DICT_CRHF = {
    "Wen": [
#        ["vhcc_Wen_13_13TeV2017","W+Wud Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (e)}}"]   ,      
        ["vhcc_Wen_11_13TeV2017","W+Zcc Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (e)}}"],
        ["vhcc_Wen_9_13TeV2017","W+CC Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (e)}}"],
        ["vhcc_Wen_7_13TeV2017","TTcs Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (e)}}"],
        ["vhcc_Wen_8_13TeV2017","TTud Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (e)}}"],
        ["vhcc_Wen_5_13TeV2017","W+HF Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (e)}}"]
    ],
    
    "Wmn": [
#        ["vhcc_Wmn_13_13TeV2017","W+Wud Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (#mu)}}"],
        ["vhcc_Wmn_11_13TeV2017","W+Zcc Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (#mu)}}"],
        ["vhcc_Wmn_9_13TeV2017","W+CC Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (#mu)}}"],
        ["vhcc_Wmn_7_13TeV2017","TTcs Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (#mu)}}"],
        ["vhcc_Wmn_8_13TeV2017","TTud Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (#mu)}}"],
        ["vhcc_Wmn_5_13TeV2017","W+HF Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (#mu)}}"]
    ],
    
    "Zee": [
        ["vhcc_Zee_5_13TeV2017","Z+HF Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), High V-p_{T}}}"],
        ["vhcc_Zee_7_13TeV2017","TT Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), High V-p_{T}}}"],
        ["vhcc_Zee_9_13TeV2017","Z+CC Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), High V-p_{T}}}"],
        ["vhcc_Zee_11_13TeV2017","Z+Zcc Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), High V-p_{T}}}"],
#        ["vhcc_Zee_13_13TeV2017","Z+Wud Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), High V-p_{T}}}"],
        ["vhcc_Zee_6_13TeV2017","Z+HF Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}}"],
        ["vhcc_Zee_8_13TeV2017","TT Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}}"],
        ["vhcc_Zee_10_13TeV2017","Z+CC Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}}"],
        ["vhcc_Zee_12_13TeV2017","Z+Zcc Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}}"],
#        ["vhcc_Zee_14_13TeV2017","Z+Wud Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}}"],
    ],
 
    "Zmm": [
        ["vhcc_Zmm_5_13TeV2017","Z+HF Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}}"],
        ["vhcc_Zmm_7_13TeV2017","TT Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}}"],
        ["vhcc_Zmm_9_13TeV2017","Z+CC Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}}"],
        ["vhcc_Zmm_11_13TeV2017","Z+Zcc Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}}"],
#        ["vhcc_Zmm_13_13TeV2017","Z+Wud Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}}"],
        ["vhcc_Zmm_6_13TeV2017","Z+HF Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}}"],
        ["vhcc_Zmm_8_13TeV2017","TT Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}}"],
        ["vhcc_Zmm_10_13TeV2017","Z+CC Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}}"],
        ["vhcc_Zmm_12_13TeV2017","Z+Zcc Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}}"],
#        ["vhcc_Zmm_14_13TeV2017","Z+Wud Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}}"],
    ],
 
    "Znn": [
        ["vhcc_Znn_5_13TeV2017","Z+HF Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{0L}}"],
        ["vhcc_Znn_7_13TeV2017","TT Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{0L}}"],
        ["vhcc_Znn_9_13TeV2017","Z+CC Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{0L}}"],
        ["vhcc_Znn_11_13TeV2017","Z+Zcc Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{0L}}"],
#        ["vhcc_Znn_13_13TeV2017","Z+Wud Control Region",-0.4,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{0L}}"]
    ]
}

CHN_DICT_CRLF = {
    "Wen": [
        ["vhcc_Wen_3_13TeV2017","W+LF Control Region",-0.2,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (e)}}"]
    ],
    
    "Wmn": [
        ["vhcc_Wmn_3_13TeV2017","W+LF Control Region",-0.2,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{1L (#mu)}}"]
    ],
    
    "Zee": [
        ["vhcc_Zee_3_13TeV2017","Z+LF Control Region",-0.2,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), High V-p_{T}}}"],
        ["vhcc_Zee_4_13TeV2017","Z+LF Control Region",-0.2,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}}"]
    ],

    "Zmm": [
        ["vhcc_Zmm_3_13TeV2017","Z+LF Control Region",-0.2,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}}"],
        ["vhcc_Zmm_4_13TeV2017","Z+LF Control Region",-0.2,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}}"]
    ],

    "Znn": [
        ["vhcc_Znn_3_13TeV2017","Z+LF Control Region",-0.2,1.,"#splitline{#scale[1.2]{Preliminary}}{#splitline{Resolved-jet}{0L}}"]
    ]
}



#Luca CHN_DICT_CRHF = {
#Luca     "Wen": [
#Luca         ["vhcc_Wen_9_13TeV2016","W+CC Control Region",-0.4,1.,"#splitline{Resolved-jet}{1L (e)}"],
#Luca         ["vhcc_Wen_7_13TeV2016","TT Control Region",-0.4,1.,"#splitline{Resolved-jet}{1L (e)}"],
#Luca         ["vhcc_Wen_5_13TeV2016","W+HF Control Region",-0.4,1.,"#splitline{Resolved-jet}{1L (e)}"]
#Luca     ],
#Luca     
#Luca     "Wmn": [
#Luca         ["vhcc_Wmn_9_13TeV2016","W+CC Control Region",-0.4,1.,"#splitline{Resolved-jet}{1L (#mu)}"],
#Luca         ["vhcc_Wmn_7_13TeV2016","TT Control Region",-0.4,1.,"#splitline{Resolved-jet}{1L (#mu)}"],
#Luca         ["vhcc_Wmn_5_13TeV2016","W+HF Control Region",-0.4,1.,"#splitline{Resolved-jet}{1L (#mu)}"]
#Luca     ],
#Luca     
#Luca     "Zee": [
#Luca         ["vhcc_Zee_5_13TeV2016","Z+HF Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (ee), High V-p_{T}}"],
#Luca         ["vhcc_Zee_7_13TeV2016","TT Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (ee), High V-p_{T}}"],
#Luca         ["vhcc_Zee_9_13TeV2016","Z+CC Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (ee), High V-p_{T}}"],
#Luca         ["vhcc_Zee_6_13TeV2016","Z+HF Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}"],
#Luca         ["vhcc_Zee_8_13TeV2016","TT Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}"],
#Luca         ["vhcc_Zee_10_13TeV2016","Z+CC Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}"]
#Luca     ],
#Luca  
#Luca     "Zmm": [
#Luca         ["vhcc_Zmm_5_13TeV2016","Z+HF Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}"],
#Luca         ["vhcc_Zmm_7_13TeV2016","TT Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}"],
#Luca         ["vhcc_Zmm_9_13TeV2016","Z+CC Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}"],
#Luca         ["vhcc_Zmm_6_13TeV2016","Z+HF Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}"],
#Luca         ["vhcc_Zmm_8_13TeV2016","TT Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}"],
#Luca         ["vhcc_Zmm_10_13TeV2016","Z+CC Control Region",-0.4,1.,"#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}"]
#Luca     ],
#Luca  
#Luca     "Znn": [
#Luca         ["vhcc_Znn_5_13TeV2016","Z+HF Control Region",-0.4,1.,"#splitline{Resolved-jet}{0L}"],
#Luca         ["vhcc_Znn_7_13TeV2016","TT Control Region",-0.4,1.,"#splitline{Resolved-jet}{0L}"],
#Luca         ["vhcc_Znn_9_13TeV2016","Z+CC Control Region",-0.4,1.,"#splitline{Resolved-jet}{0L}"]
#Luca     ]
#Luca }
#Luca 
#Luca CHN_DICT_CRLF = {
#Luca     "Wen": [
#Luca         ["vhcc_Wen_3_13TeV2016","W+LF Control Region",-0.2,1.,"#splitline{Resolved-jet}{1L (e)}"]
#Luca     ],
#Luca     
#Luca     "Wmn": [
#Luca         ["vhcc_Wmn_3_13TeV2016","W+LF Control Region",-0.2,1.,"#splitline{Resolved-jet}{1L (#mu)}"]
#Luca     ],
#Luca     
#Luca     "Zee": [
#Luca         ["vhcc_Zee_3_13TeV2016","Z+LF Control Region",-0.2,1.,"#splitline{Resolved-jet}{2L (ee), High V-p_{T}}"],
#Luca         ["vhcc_Zee_4_13TeV2016","Z+LF Control Region",-0.2,1.,"#splitline{Resolved-jet}{2L (ee), Low V-p_{T}}"]
#Luca     ],
#Luca 
#Luca     "Zmm": [
#Luca         ["vhcc_Zmm_3_13TeV2016","Z+LF Control Region",-0.2,1.,"#splitline{Resolved-jet}{2L (#mu#mu), High V-p_{T}}"],
#Luca         ["vhcc_Zmm_4_13TeV2016","Z+LF Control Region",-0.2,1.,"#splitline{Resolved-jet}{2L (#mu#mu), Low V-p_{T}}"]
#Luca     ],
#Luca 
#Luca     "Znn": [
#Luca         ["vhcc_Znn_3_13TeV2016","Z+LF Control Region",-0.2,1.,"#splitline{Resolved-jet}{0L}"]
#Luca     ]
#Luca }


for MODE in ['prefit']: #,'postfit']:
#for MODE in ['prefit']:
    for CHN in ['Zee','Zmm','Wen','Wmn','Znn']:
#    for CHN in ['Znn']:
#    for CHN in ['Wmn','Wen','Znn']:
#    for CHN in ['Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_CRHF[CHN])):
            LABEL = "%s" % CHN_DICT_CRHF[CHN][i][1]
            OUTNAME = "%s" % CHN_DICT_CRHF[CHN][i][0]
            XLOW = CHN_DICT_CRHF[CHN][i][2]
            XHIGH = CHN_DICT_CRHF[CHN][i][3]
            EXTRALABEL = CHN_DICT_CRHF[CHN][i][4]
            os.system(('../../../scripts/postFitPlot_vhcc_alt.py' \
                       ' --file=shapes.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s --outdir="Prefit/" --no_signal ' \
                       ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --cr --doVWud 1' \
                       ' --outname %(OUTNAME)s --mode %(MODE)s --x_title="CvsB_{min}"  --y_title "Events" --lumi="41.5 fb^{-1} (13 TeV)"'\
                       ' --x_axis_min %(XLOW)f --x_axis_max %(XHIGH)f --custom_x_range '\
                       ' --channel_label "%(LABEL)s" --extralabel "%(EXTRALABEL)s"' % vars()))
            
for MODE in ['prefit']: #,'postfit']:
#for MODE in ['prefit']:
    for CHN in ['Zee','Zmm','Wen','Wmn','Znn']:
#    for CHN in ['Zee','Zmm']:
#    for CHN in ['Wmn','Wen','Znn']:
#    for CHN in ['Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_CRLF[CHN])):
              LABEL = "%s" % CHN_DICT_CRLF[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_CRLF[CHN][i][0]
              XLOW = CHN_DICT_CRLF[CHN][i][2]
              XHIGH = CHN_DICT_CRLF[CHN][i][3]
              EXTRALABEL = CHN_DICT_CRLF[CHN][i][4]
              os.system(('../../../scripts/postFitPlot_vhcc_alt.py' \
                  ' --file=shapes.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s --outdir="Prefit/" --no_signal' \
                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --cr --doVWud 1' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --x_title="CvsL_{min}"  --y_title "Events" --lumi="41.5 fb^{-1} (13 TeV)"'\
                  ' --x_axis_min %(XLOW)f --x_axis_max %(XHIGH)f --custom_x_range '\
                         ' --channel_label "%(LABEL)s" --extralabel "%(EXTRALABEL)s"' % vars()))

