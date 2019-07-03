import os

CHN_DICT_SR = {
    "Wen": [["vhcc_Wen_1_13TeV2016","Signal Region","1-lepton (e#nu)"]],
    "Wmn": [["vhcc_Wmn_1_13TeV2016","Signal Region","1-lepton (#mu#nu)"]],
    "Zee": [["vhcc_Zee_1_13TeV2016","Signal Region","2-lepton (ee), High V-p_{T}"],["vhcc_Zee_2_13TeV2016","Signal Region","2-lepton (ee), Low V-p_{T}"]],
    "Zmm": [["vhcc_Zmm_1_13TeV2016","Signal Region","2-lepton (#mu#mu), High p_{T}(V)"],["vhcc_Zmm_2_13TeV2016","Signal Region","2-lepton (#mu#mu), Low V-p_{T}"]],
    "Znn": [["vhcc_Znn_1_13TeV2016","Signal Region","0-lepton (#nu#nu)"]]
}



for MODE in ['prefit']:
#    for CHN in ['Zee']:
    for CHN in ['Wen','Wmn','Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              EXTRALABEL = CHN_DICT_SR[CHN][i][2]
              os.system(('./scripts/postFitPlot_vhcc.py' \
                  ' --file=shapes_VZincl_15May.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s' \
#                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --blind --x_blind_min 0.75 --x_blind_max 1.0 --x_title BDT --doVV True' \
                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --x_title "BDT output" --y_title "Events" --mu ", #mu=1" --doVV True' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --log_y --custom_y_range --y_axis_min "5E-3" --keepPreFitSignal True'\
                  ' --channel_label "%(LABEL)s" --extralabel "%(EXTRALABEL)s"' % vars()))


for MODE in ['postfit']:
#    for CHN in ['Zee']:
    for CHN in ['Wen','Wmn','Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              EXTRALABEL = CHN_DICT_SR[CHN][i][2]
              os.system(('./scripts/postFitPlot_vhcc.py' \
                  ' --file=shapes_VZincl_15May.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s' \
#                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --blind --x_blind_min 0.75 --x_blind_max 1.0 --x_title BDT --doVV True' \
                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --x_title "BDT output" --y_title "Events" --mu ", #mu=1.35" --doVV True' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --log_y --custom_y_range --y_axis_min "5E-3" --keepPreFitSignal True'\
                  ' --channel_label "%(LABEL)s" --extralabel "%(EXTRALABEL)s"' % vars()))



# shapes_VZincl_15May.root
#shapes_VZpt300_15May.root
