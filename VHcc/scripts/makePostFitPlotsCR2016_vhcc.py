import os

CHN_DICT_CRHF = {
    "Wen": [
        ["vhcc_Wen_9_13TeV2016","W+c#bar{c} Control Region",-0.4,1.,"1-lepton (e#nu)"],
        ["vhcc_Wen_7_13TeV2016","t#bar{t} Control Region",-0.4,1.,"1-lepton (e#nu)"],
        ["vhcc_Wen_5_13TeV2016","W+b#bar{b} Control Region",-0.4,1.,"1-lepton (e#nu)"]
    ],
    
    "Wmn": [
        ["vhcc_Wmn_9_13TeV2016","W+c#bar{c} Control Region",-0.4,1.,"1-lepton (#mu#nu)"],
        ["vhcc_Wmn_7_13TeV2016","t#bar{t} Control Region",-0.4,1.,"1-lepton (#mu#nu)"],
        ["vhcc_Wmn_5_13TeV2016","Control Region",-0.4,1.,"1-lepton (#mu#nu)"]
    ],
    
    "Zee": [
        ["vhcc_Zee_5_13TeV2016","Z+b#bar{b} Control Region",-0.4,1.,"2-lepton (ee), High V-p_{T}"],
        ["vhcc_Zee_7_13TeV2016","t#bar{t} Control Region",-0.4,1.,"2-lepton (ee), High V-p_{T}"],
        ["vhcc_Zee_9_13TeV2016","Z+c#bar{c} Control Region",-0.4,1.,"2-lepton (ee), High V-p_{T}"],
        ["vhcc_Zee_6_13TeV2016","Z+b#bar{b} Control Region",-0.4,1.,"2-lepton (ee), Low V-p_{T}"],
        ["vhcc_Zee_8_13TeV2016","t#bar{t} Control Region",-0.4,1.,"2-lepton (ee), Low V-p_{T}"],
        ["vhcc_Zee_10_13TeV2016","Z+c#bar{c} Control Region",-0.4,1.,"2-lepton (ee), Low V-p_{T}"]
    ],
 
    "Zmm": [
        ["vhcc_Zmm_5_13TeV2016","Z+b#bar{b} Control Region",-0.4,1.,"2-lepton (#mu#mu), High V-p_{T}"],
        ["vhcc_Zmm_7_13TeV2016","t#bar{t} Control Region",-0.4,1.,"2-lepton (#mu#mu), High V-p_{T}"],
        ["vhcc_Zmm_9_13TeV2016","Z+c#bar{c} Control Region",-0.4,1.,"2-lepton (#mu#mu), High V-p_{T}"],
        ["vhcc_Zmm_6_13TeV2016","Z+b#bar{b} Control Region",-0.4,1.,"2-lepton (#mu#mu), Low V-p_{T}"],
        ["vhcc_Zmm_8_13TeV2016","t#bar{t} Control Region",-0.4,1.,"2-lepton (#mu#mu), Low V-p_{T}"],
        ["vhcc_Zmm_10_13TeV2016","Z+c#bar{c} Control Region",-0.4,1.,"2-lepton (#mu#mu), Low V-p_{T}"]
    ],
 
    "Znn": [
        ["vhcc_Znn_5_13TeV2016","Z+b#bar{b} Control Region",-0.4,1.,"0-lepton (#nu#nu)"],
        ["vhcc_Znn_7_13TeV2016","t#bar{t} Control Region",-0.4,1.,"0-lepton (#nu#nu)"],
        ["vhcc_Znn_9_13TeV2016","Z+c#bar{c} Control Region",-0.4,1.,"0-lepton (#nu#nu)"]
#Luca         ["vhcc_Wen_5_13TeV2016","1-lepton (e), W+b#bar{b} Control Region",-0.4,1.],
#Luca         ["vhcc_Wen_7_13TeV2016","1-lepton (e), t#bar{t} Control Region",-0.4,1.],
#Luca         ["vhcc_Wen_9_13TeV2016","1-lepton (e), W+c#bar{c} Control Region",-0.4,1.],
#Luca         ["vhcc_Wmn_5_13TeV2016","1-lepton (#mu), W+b#bar{b} Control Region",-0.4,1.],
#Luca         ["vhcc_Wmn_7_13TeV2016","1-lepton (#mu), t#bar{t} Control Region",-0.4,1.],
#Luca         ["vhcc_Wmn_9_13TeV2016","1-lepton (#mu), W+c#bar{c} Control Region",-0.4,1.]
    ]
}

CHN_DICT_CRLF = {
    "Wen": [
        ["vhcc_Wen_3_13TeV2016","W+udsg Control Region",-0.2,1.,"1-lepton (e#nu)"]
    ],
    
    "Wmn": [
        ["vhcc_Wmn_3_13TeV2016","W+udsg Control Region",-0.2,1.,"1-lepton (#mu#nu)"]
    ],
    
    "Zee": [
        ["vhcc_Zee_3_13TeV2016","Z+udsg Control Region",-0.2,1.,"2-lepton (ee), High V-p_{T}"],
        ["vhcc_Zee_4_13TeV2016","Z+udsg Control Region",-0.2,1.,"2-lepton (ee), Low V-p_{T}"]
    ],

    "Zmm": [
        ["vhcc_Zmm_3_13TeV2016","Z+udsg Control Region",-0.2,1.,"2-lepton (#mu#mu), High V-p_{T}"],
        ["vhcc_Zmm_4_13TeV2016","Z+udsg Control Region",-0.2,1.,"2-lepton (#mu#mu), Low V-p_{T}"]
    ],

    "Znn": [
        ["vhcc_Znn_3_13TeV2016","Z+udsg Control Region",-0.2,1.,"0-lepton (#nu#nu)"]
#        ["vhcc_Wen_3_13TeV2016","W+udsg Control Region",-0.2,1.,"1-lepton (e)"],
#        ["vhcc_Wmn_3_13TeV2016","W+udsg Control Region",-0.2,1.,"1-lepton (#mu)"]
    ]
}


for MODE in ['prefit','postfit']:
#for MODE in ['prefit']:
    for CHN in ['Zee','Zmm','Wen','Wmn','Znn']:
#    for CHN in ['Zee','Zmm']:
#    for CHN in ['Znn']:
        for i in range(0,len(CHN_DICT_CRHF[CHN])):
            LABEL = "%s" % CHN_DICT_CRHF[CHN][i][1]
            OUTNAME = "%s" % CHN_DICT_CRHF[CHN][i][0]
            XLOW = CHN_DICT_CRHF[CHN][i][2]
            XHIGH = CHN_DICT_CRHF[CHN][i][3]
            EXTRALABEL = CHN_DICT_CRHF[CHN][i][4]
            os.system(('./scripts/postFitPlot_vhcc.py' \
                       ' --file=shapes_VHincl_15May.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s --no_signal' \
                       ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --cr ' \
                       ' --outname %(OUTNAME)s --mode %(MODE)s --x_title="CvsB_{min}"  --y_title "Events" --lumi="35.9 fb^{-1} (13 TeV)"'\
                       ' --x_axis_min %(XLOW)f --x_axis_max %(XHIGH)f --custom_x_range '\
                       ' --channel_label "%(LABEL)s" --extralabel "%(EXTRALABEL)s"' % vars()))
            
for MODE in ['prefit','postfit']:
#for MODE in ['postfit']:
    for CHN in ['Zee','Zmm','Wen','Wmn','Znn']:
#    for CHN in ['Zee']:
    #for CHN in ['Znn']:
        for i in range(0,len(CHN_DICT_CRLF[CHN])):
              LABEL = "%s" % CHN_DICT_CRLF[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_CRLF[CHN][i][0]
              XLOW = CHN_DICT_CRLF[CHN][i][2]
              XHIGH = CHN_DICT_CRLF[CHN][i][3]
              EXTRALABEL = CHN_DICT_CRLF[CHN][i][4]
              os.system(('./scripts/postFitPlot_vhcc.py' \
                  ' --file=shapes_VHincl_15May.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s --no_signal' \
                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --cr ' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --x_title="CvsL_{min}"  --y_title "Events" --lumi="35.9 fb^{-1} (13 TeV)"'\
                  ' --x_axis_min %(XLOW)f --x_axis_max %(XHIGH)f --custom_x_range '\
                  ' --channel_label "%(LABEL)s" --extralabel "%(EXTRALABEL)s"' % vars()))
