import CombineHarvester.CombineTools.ch as ch

def AddCommonSystematics(cb):
  
  signal = cb.cp().signals().process_set()
  # rateParams
  
  # Theory uncertainties: signal
  cb.cp().AddSyst(cb,
       'pdf_Higgs_qqbar', 'lnN', ch.SystMap('process')
        (['ZH_hbb'],1.016)
        (['WH_hbb'],1.019))

  cb.cp().process(['ggZH_hbb']).AddSyst(cb,
      'pdf_Higgs_gg', 'lnN', ch.SystMap()(1.024))

  cb.cp().process(signal).AddSyst(cb,
      'BR_hbb', 'lnN', ch.SystMap()(1.005))

  cb.cp().process(['ggZH_hbb']).AddSyst(cb,
      'QCDscale_ggZH', 'lnN',ch.SystMap()((1.251,0.811)))
   
  cb.cp().AddSyst(cb,
      'QCDscale_VH', 'lnN', ch.SystMap('process') 
      (['ZH_hbb'], (1.038,0.969)) 
      (['WH_hbb'], (1.005,0.993)))

#Luca  # To be checked:
#Luca  cb.cp().AddSyst(cb,
#Luca      'CMS_vhbb_boost_EWK_13TeV', 'lnN', ch.SystMap('channel','process') 
#Luca      (['Zee','Zmm'],['ZH_hbb'], 1.02)
#Luca      (['Znn'],['ZH_hbb','WH_hbb','ggZH_hbb'],1.02)
#Luca      (['Wen','Wmn'],['WH_hbb','ZH_hbb'],1.02)) 

  # To be checked: LUCAP: IN MY OPINION NEEDS TO BE REMOVED!!!
  #cb.cp().AddSyst(cb,
  #    'CMS_vhbb_boost_QCD_13TeV', 'lnN', ch.SystMap('channel','process') 
  #    (['Zee','Zmm'],['ZH_hbb'], 1.05)
  #    (['Znn'],['ZH_hbb','WH_hbb','ggZH_hbb'],1.05)) 

  # Theory uncertainties: backgrounds -> to be checked!
  cb.cp().AddSyst(cb,
       'pdf_qqbar', 'lnN', ch.SystMap('channel','process') 
        (['Zee','Zmm'],['Zj0b','Zj1b','Zj2b','VVLF','VVHF','VV'], 1.01)
        (['Znn'],['VVLF','VVHF'],1.01)
        (['Wen','Wmn'],['VVLF','VVHF'],1.01)) 

  cb.cp().AddSyst(cb,
       'pdf_gg', 'lnN', ch.SystMap('channel','process')
       (['Zee','Zmm','Znn'],['TT','s_Top','QCD'], 1.01)
       (['Wen','Wmn'], ['s_Top'],1.01))

  cb.cp().AddSyst(cb,
      'QCDscale_ttbar', 'lnN', ch.SystMap('channel','process') 
      #(['Zee','Zmm','Wen','Wmn','Znn'],['s_Top'], 1.06)
       (['Zee','Zmm','Wen','Wmn','Znn'],['TT'],1.06)
      ) 

  #cb.cp().AddSyst(cb,
  #    'QCDscale_VV', 'lnN', ch.SystMap('channel','process') 
  #    (['Zee','Zmm','Wen','Wmn','Znn'],['VVLF','VVHF','VV'], 1.04)) 

#Luca  # measured cross section uncertainties because we don't have SF
#Luca  cb.cp().process(['VV','VVHF','VVLF']).AddSyst(cb,
#Luca      'CMS_vhbb_VV', 'lnN', ch.SystMap()(1.15)) 
#Luca
#Luca  cb.cp().process(['s_Top']).AddSyst(cb,
#Luca      'CMS_vhbb_ST', 'lnN', ch.SystMap()(1.15)) 

#Luca   #Theory uncertainties: pdf acceptance, to be re-evaluated
#Luca   cb.cp().process(['ZH_hbb']).AddSyst(cb,'CMS_LHE_weights_pdf_ZH', 'lnN', ch.SystMap()(1.01)) 
#Luca   cb.cp().process(['WH_hbb']).AddSyst(cb,'CMS_LHE_weights_pdf_WH', 'lnN', ch.SystMap()(1.01))
#Luca   cb.cp().process(['TT']).AddSyst(cb,    'CMS_LHE_weights_pdf_TT', 'lnN', ch.SystMap()(1.005))
#Luca   cb.cp().process(['Zj0b']).AddSyst(cb,'CMS_LHE_weights_pdf_Zj0b', 'lnN', ch.SystMap()(1.05))
#Luca   cb.cp().process(['Zj1b']).AddSyst(cb,'CMS_LHE_weights_pdf_Zj1b', 'lnN', ch.SystMap()(1.03))
#Luca   cb.cp().process(['Zj2b']).AddSyst(cb,'CMS_LHE_weights_pdf_Zj2b', 'lnN', ch.SystMap()(1.02))
#Luca   cb.cp().process(['Wj0b']).AddSyst(cb,'CMS_LHE_weights_pdf_Wj0b', 'lnN', ch.SystMap()(1.05))
#Luca   cb.cp().process(['Wj1b']).AddSyst(cb,'CMS_LHE_weights_pdf_Wj1b', 'lnN', ch.SystMap()(1.03))
#Luca   cb.cp().process(['Wj2b']).AddSyst(cb,'CMS_LHE_weights_pdf_Wj2b', 'lnN', ch.SystMap()(1.02))
#Luca   
#Luca   cb.cp().process(['VVHF','VV']).AddSyst(cb,'CMS_LHE_weights_pdf_VVHF', 'lnN', ch.SystMap()(1.02))
#Luca   
#Luca   cb.cp().process(['VVLF']).AddSyst(cb,'CMS_LHE_weights_pdf_VVLF', 'lnN', ch.SystMap('channel') 
#Luca                                                                         (['Zee','Zmm','Znn'],1.03)
#Luca                                                                         (['Wen','Wmn'],1.02)) 
#Luca   
#Luca   cb.cp().channel(['Wen','Wmn','Zmm','Zee']).process(['VVHF']).AddSyst(cb,
#Luca       'CMS_LHE_weights_scale_muR_VVHF','shape',ch.SystMap()(1.0))
#Luca 
#Luca   cb.cp().channel(['Wen','Wmn','Zmm','Zee']).process(['VVHF']).AddSyst(cb,
#Luca       'CMS_LHE_weights_scale_muF_VVHF','shape',ch.SystMap()(1.0))
#Luca 
  # cb.cp().process(['VVLF']).AddSyst(cb,
     # 'CMS_LHE_weights_scale_muR_VVLF','shape',ch.SystMap()(1.0))

  # cb.cp().process(['VVLF']).AddSyst(cb,
     # 'CMS_LHE_weights_scale_muF_VVLF','shape',ch.SystMap()(1.0))

  # cb.cp().process(['QCD']).AddSyst(cb,
     # 'CMS_LHE_weights_scale_muR_QCD','shape',ch.SystMap()(1.0))

  # cb.cp().process(['QCD']).AddSyst(cb,
     # 'CMS_LHE_weights_scale_muF_QCD','shape',ch.SystMap()(1.0))

###########################################
### Uncertainties for 2017
###########################################

def AddSystematics2017(cb):
#Luca   cb.cp().AddSyst(cb,'CMS_vhbb_puWeight','shape',ch.SystMap()(1.0))

#Luca  cb.cp().process(['ZH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muR_ZH','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['ZH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muF_ZH','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['WH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muR_WH','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['WH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muF_WH','shape',ch.SystMap()(1.0))
#Luca  
#Luca  cb.cp().process(['ggZH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muR_ggZH','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['ggZH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muF_ggZH','shape',ch.SystMap()(1.0))
#Luca  
#Luca  cb.cp().process(['Zj0b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Zj0b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj0b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Zj0b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj1b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Zj1b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj1b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Zj1b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj2b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Zj2b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj2b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Zj2b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj0b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Wj0b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj0b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Wj0b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj1b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Wj1b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj1b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Wj1b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj2b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Wj2b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj2b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Wj2b','shape',ch.SystMap()(1.0))
#Luca  
#Luca  cb.cp().process(['TT']).AddSyst(cb,'CMS_LHE_weights_scale_muR_TT','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['TT']).AddSyst(cb,'CMS_LHE_weights_scale_muF_TT','shape',ch.SystMap()(1.0))
#Luca
#Luca  cb.cp().process(['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b']).AddSyst(cb,
#Luca                    'CMS_vhbb_vjetnlodetajjrw_13TeV','shape',ch.SystMap()(1.0))

  # SCALE FACTORS RATEPARAM
  
#Luca  # TT Zll
#Luca  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
#Luca     'SF_TT_high_Zll_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     ([1,3,5,7,9,11,13],1.0))
#Luca
#Luca  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
#Luca     'SF_TT_low_Zll_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     ([2,4,6,8,10,12,14],1.0))
#Luca  
#Luca  # Zj0b Zll
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj0b']).AddSyst(cb,
#Luca     'SF_Zj0b_high_Zll_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     ([1,3,5,7,9,11,13],1.0))
#Luca  
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj0b']).AddSyst(cb,
#Luca     'SF_Zj0b_low_Zll_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     ([2,4,6,8,10,12,14],1.0))
#Luca
#Luca  # Zj1b Zll
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj1b']).AddSyst(cb,
#Luca     'SF_Zj1b_high_Zll_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     ([1,3,5,7,9,11,13],1.0))
#Luca
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj1b']).AddSyst(cb,
#Luca     'SF_Zj1b_low_Zll_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     ([2,4,6,8,10,12,14],1.0))
#Luca
#Luca  # Zj2b Zll
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj2b']).AddSyst(cb,
#Luca     'SF_Zj2b_high_Zll_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     ([1,3,5,7,9,11,13],1.0))
#Luca
#Luca
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj2b']).AddSyst(cb,
#Luca     'SF_Zj2b_low_Zll_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     ([2,4,6,8,10,12,14],1.0))
#Luca
#Luca  # TT Znn
#Luca  cb.cp().channel(['Znn']).process(['TT']).AddSyst(cb,
#Luca     'SF_TT_Znn_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     #([1,3,5,7],1.0))
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Zj0b Znn
#Luca  cb.cp().channel(['Znn']).process(['Zj0b']).AddSyst(cb,
#Luca     'SF_Zj0b_Znn_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     #([1,3,5,7],1.0))
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Zj1b Znn
#Luca  cb.cp().channel(['Znn']).process(['Zj1b']).AddSyst(cb,
#Luca     'SF_Zj1b_Znn_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     #([1,3,5,7],1.0))
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Zj2b Znn
#Luca  cb.cp().channel(['Znn']).process(['Zj2b']).AddSyst(cb,
#Luca     'SF_Zj2b_Znn_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     #([1,3,5,7],1.0))
#Luca     (range(1,8),1.0))
#Luca
#Luca  # TT Wln
#Luca  cb.cp().channel(['Wen','Wmn']).process(['TT']).AddSyst(cb,
#Luca     'SF_TT_Wln_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     #([1,3,5,6,7],1.0))
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Wj0b Wln
#Luca  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj0b']).AddSyst(cb,
#Luca     'SF_Wj0b_Wln_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     #([1,3,5,6,7],1.0))
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Wj1b Wln
#Luca  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj1b']).AddSyst(cb,
#Luca     'SF_Wj1b_Wln_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     #([1,3,5,6,7],1.0))
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Wj2b Wln
#Luca  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj2b']).AddSyst(cb,
#Luca     'SF_Wj2b_Wln_2017', 'rateParam', ch.SystMap('bin_id')
#Luca     #([1,3,5,6,7],1.0))
#Luca     (range(1,8),1.0))
#Luca
#Luca  #Set a sensible range for the rate params
#Luca  for syst in cb.cp().syst_type(["rateParam"]).syst_name_set():
#Luca    cb.GetParameter(syst).set_range(0.0,5.0)
#Luca
  #Experimental uncertainties
  cb.cp().AddSyst(cb,'lumi_13TeV','lnN', ch.SystMap()(1.023))
  
  # cb.cp().channel(['Wen','Wmn']).process(['TT']).AddSyst(cb,
     # 'CMS_vhbb_ptwweights_tt','shape',ch.SystMap()(1.0))

  # cb.cp().channel(['Wen','Wmn']).process(['s_Top','Wj1b','Wj2b'])AddSyst(cb,
     # 'CMS_vhbb_ptwweights_whf','shape',ch.SystMap()(1.0))

  # cb.cp().channel(['Wen','Wmn']).process(['Wj0b']).AddSyst(cb,
     # 'CMS_vhbb_ptwweights_wlf','shape',ch.SystMap()(1.0))

  # cb.cp().channel(['Wen']).AddSyst(cb,
     # 'CMS_vhbb_eff_e_Wln_13TeV','shape',ch.SystMap()(1.0))

  # lepton efficiencies
  
#Luca  # Lepton shapes buggy in shapes/AT/UNBLINDINGVHbb, using lnN
#Luca  # cb.cp().channel(['Wmn']).AddSyst(cb,'CMS_vhbb_eff_m_Wln_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().channel(['Wmn']).AddSyst(cb,'CMS_vhbb_eff_m_Wln_13TeV','lnN',ch.SystMap()(1.02))
#Luca
#Luca  # cb.cp().channel(['Wen']).AddSyst(cb,'CMS_vhbb_eff_e_Wln_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().channel(['Wen']).AddSyst(cb,'CMS_vhbb_eff_e_Wln_13TeV','lnN',ch.SystMap()(1.02))
#Luca
#Luca  # cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_Zll_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_Zll_13TeV','lnN',ch.SystMap()(1.04))
#Luca
#Luca  # cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhbb_eff_e_Zll_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhbb_eff_e_Zll_13TeV','lnN',ch.SystMap()(1.04))

  # cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhbb_eff_e_trigger_Zll_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhbb_eff_e_MVAID_Zll_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().channel(['Wen','Zee']).AddSyst(cb,'CMS_vhbb_eff_e_tracker_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_trigger_Zll_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_MVAID_Zll_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().channel(['Wmn','Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_tracker_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_ISO_Zll_13TeV','shape',ch.SystMap()(1.0))

#Luca  # met efficiencies
#Luca  cb.cp().channel(['Znn']).AddSyst(cb,'CMS_vhbb_trigger_MET_13TeV','lnN',ch.SystMap()(1.005))

#Luca  # VpT reweightings
#Luca  cb.cp().process(['TT']).AddSyst(cb,'CMS_vhbb_topptreweighting_13TeV','shape',ch.SystMap()(1.0))
#Luca  
#Luca  cb.cp().channel(['Wen','Wmn']).process(['Wj0b']).AddSyst(cb,
#Luca      'CMS_vhbb_ptwweights_wlf_13TeV','shape',ch.SystMap()(1.0))
#Luca
#Luca  cb.cp().channel(['Wen','Wmn']).process(['Wj1b','Wj2b','s_Top']).AddSyst(cb,
#Luca      'CMS_vhbb_ptwweights_whf_13TeV','shape',ch.SystMap()(1.0))

  # cb.cp().AddSyst(cb,
     # 'CMS_vhbb_EWK_Zll','shape',ch.SystMap('channel','bin_id','process')
     # (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb'],1.0))
  
#Luca  #Jet energy scale
#Luca  cb.cp().AddSyst(cb,'CMS_res_j_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_res_j_reg_13TeV','shape',ch.SystMap()(1.0))
 
  # inclusive in pt/eta
  # cb.cp().AddSyst(cb,'CMS_scale_j_13TeV','shape',ch.SystMap()(1.0))
  # cb.FilterSysts(lambda x: (x.bin_id()==2 or x.bin_id()==1) and x.name()=='CMS_scale_j_13TeV')

#Luca  # split as JET/MET recommends
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpDataMC_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtRef_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtBB_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtEC1_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtEC2_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtHF_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeBal_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeJEREC1_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeJEREC2_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeJERHF_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeFSR_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeStatFSR_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeStatEC_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeStatHF_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativePtBB_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativePtHF_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativePtEC1_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativePtEC2_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_AbsoluteScale_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_AbsoluteMPFBias_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_AbsoluteStat_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_SinglePionECAL_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_SinglePionHCAL_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_Fragmentation_13TeV','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_FlavorQCD_13TeV','shape',ch.SystMap()(1.0))

  #b-tagging uncertainties
  
  # inclusive in pt/eta
  # cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV','shape',ch.SystMap()(1.0))
  # cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV','shape',ch.SystMap()(1.0))
  
#Luca  # differential in pt/eta
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBJES_13TeV_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHF_13TeV_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLF_13TeV_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats1_13TeV_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats1_13TeV_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBHFStats2_13TeV_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBLFStats2_13TeV_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr1_13TeV_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightDeepBcErr2_13TeV_pt4_eta2','shape',ch.SystMap()(1.0))

  # EXCLUDE PROBLEMATIC NUISANCES for 2017 shapes
  cb.FilterSysts(lambda x: 
                        x.channel() in ['Wen','Wmn'] and 
                        x.process() in ['s_Top','TT','Wj0b','Wj1b','Wj2b','Zj0b','Zj1b','Zj2b','VVHF','VVLF','WH_hbb','ZH_hbb'] and 
                        #x.bin_id() in [1,3,5,6,7] and 
                        x.bin_id() in [1,2,3,4,5,6,7] and 
                        x.name() in 'CMS_scale_j_PileUpPtBB_13TeV'
                        )
 

###########################################
### Uncertainties for 2016
###########################################

def AddSystematics2016(cb):
#Luca  cb.cp().AddSyst(cb,
#Luca      'CMS_vhbb_puWeight_2016','shape',ch.SystMap()(1.0))
#Luca
#Luca  cb.cp().process(['ZH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muR_ZH','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['ZH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muF_ZH','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['WH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muR_WH','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['WH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muF_WH','shape',ch.SystMap()(1.0))
#Luca  
#Luca  cb.cp().process(['ggZH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muR_ggZH','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['ggZH_hbb']).AddSyst(cb,'CMS_LHE_weights_scale_muF_ggZH','shape',ch.SystMap()(1.0))
#Luca  
#Luca  cb.cp().process(['Zj0b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Zj0b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj0b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Zj0b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj1b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Zj1b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj1b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Zj1b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj2b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Zj2b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Zj2b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Zj2b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj0b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Wj0b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj0b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Wj0b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj1b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Wj1b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj1b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Wj1b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj2b']).AddSyst(cb,'CMS_LHE_weights_scale_muR_Wj2b','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['Wj2b']).AddSyst(cb,'CMS_LHE_weights_scale_muF_Wj2b','shape',ch.SystMap()(1.0))
#Luca  
#Luca  cb.cp().process(['TT']).AddSyst(cb,'CMS_LHE_weights_scale_muR_TT','shape',ch.SystMap()(1.0))
#Luca  cb.cp().process(['TT']).AddSyst(cb,'CMS_LHE_weights_scale_muF_TT','shape',ch.SystMap()(1.0))
#Luca
#Luca  cb.cp().process(['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b']).AddSyst(cb,
#Luca                  'CMS_vhbb_vjetnlodetajjrw_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca
#Luca  
#Luca  # SCALE FACTORS RATEPARAM
#Luca  
#Luca  # TT Zll
#Luca  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
#Luca     'SF_TT_high_Zll_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     ([1,3,5,7,9,11,13],1.0))
#Luca
#Luca  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
#Luca     'SF_TT_low_Zll_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     ([2,4,6,8,10,12,14],1.0))
#Luca
#Luca  # Zj0b Zll
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj0b']).AddSyst(cb,
#Luca     'SF_Zj0b_high_Zll_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     ([1,3,5,7,9,11,13],1.0))
#Luca
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj0b']).AddSyst(cb,
#Luca     'SF_Zj0b_low_Zll_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     ([2,4,6,8,10,12,14],1.0))
#Luca
#Luca  # Zj1b Zll
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj1b']).AddSyst(cb,
#Luca     'SF_Zj1b_high_Zll_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     ([1,3,5,7,9,11,13],1.0))
#Luca
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj1b']).AddSyst(cb,
#Luca     'SF_Zj1b_low_Zll_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     ([2,4,6,8,10,12,14],1.0))
#Luca
#Luca  # Zj2b Zll
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj2b']).AddSyst(cb,
#Luca     'SF_Zj2b_high_Zll_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     ([1,3,5,7,9,11,13],1.0))
#Luca
#Luca  cb.cp().channel(['Zee','Zmm']).process(['Zj2b']).AddSyst(cb,
#Luca     'SF_Zj2b_low_Zll_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     ([2,4,6,8,10,12,14],1.0))
#Luca
#Luca  # TT Znn
#Luca  cb.cp().channel(['Znn']).process(['TT']).AddSyst(cb,
#Luca     'SF_TT_Znn_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Zj0b Znn
#Luca  cb.cp().channel(['Znn']).process(['Zj0b']).AddSyst(cb,
#Luca     'SF_Zj0b_Znn_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Zj1b Znn
#Luca  cb.cp().channel(['Znn']).process(['Zj1b']).AddSyst(cb,
#Luca     'SF_Zj1b_Znn_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Zj2b Znn
#Luca  cb.cp().channel(['Znn']).process(['Zj2b']).AddSyst(cb,
#Luca     'SF_Zj2b_Znn_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     (range(1,8),1.0))
#Luca
#Luca  # TT Wln
#Luca  cb.cp().channel(['Wen','Wmn']).process(['TT']).AddSyst(cb,
#Luca     'SF_TT_Wln_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Wj0b Wln
#Luca  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj0b']).AddSyst(cb,
#Luca     'SF_Wj0b_Wln_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Wj1b Wln
#Luca  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj1b']).AddSyst(cb,
#Luca     'SF_Wj1b_Wln_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     (range(1,8),1.0))
#Luca
#Luca  # Wj2b Wln
#Luca  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj2b']).AddSyst(cb,
#Luca     'SF_Wj2b_Wln_2016', 'rateParam', ch.SystMap('bin_id')
#Luca     (range(1,8),1.0))
#Luca
#Luca
#Luca  #Set a sensible range for the rate params
#Luca  for syst in cb.cp().syst_type(["rateParam"]).syst_name_set():
#Luca    cb.GetParameter(syst).set_range(0.0,5.0)

  #Experimental uncertainties
  cb.cp().AddSyst( cb,'lumi_13TeV_2016','lnN', ch.SystMap()(1.025))
  
  # cb.cp().channel(['Wen','Wmn']).process(['TT']).AddSyst(cb,
     # 'CMS_vhbb_ptwweights_tt','shape',ch.SystMap()(1.0))

  # cb.cp().channel(['Wen','Wmn']).process(['s_Top','Wj1b','Wj2b'])AddSyst(cb,
     # 'CMS_vhbb_ptwweights_whf','shape',ch.SystMap()(1.0))

  # cb.cp().channel(['Wen','Wmn']).process(['Wj0b']).AddSyst(cb,
     # 'CMS_vhbb_ptwweights_wlf','shape',ch.SystMap()(1.0))

  # cb.cp().channel(['Wen']).AddSyst(cb,
     # 'CMS_vhbb_eff_e_Wln_13TeV','shape',ch.SystMap()(1.0))
 
#Luca  # lepton efficiencies
#Luca  # cb.cp().channel(['Wmn']).AddSyst(cb,'CMS_vhbb_eff_m_Wln_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().channel(['Wmn']).AddSyst(cb,'CMS_vhbb_eff_m_Wln_13TeV_2016','lnN',ch.SystMap()(1.02))
#Luca
#Luca  # cb.cp().channel(['Wen']).AddSyst(cb,'CMS_vhbb_eff_e_Wln_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().channel(['Wen']).AddSyst(cb,'CMS_vhbb_eff_e_Wln_13TeV_2016','lnN',ch.SystMap()(1.02))
#Luca
#Luca  # cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_Zll_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_Zll_13TeV_2016','lnN',ch.SystMap()(1.04))
#Luca
#Luca  # cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhbb_eff_e_Zll_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhbb_eff_e_Zll_13TeV_2016','lnN',ch.SystMap()(1.04))
#Luca
#Luca  # cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhbb_eff_e_trigger_Zll_13TeV','shape',ch.SystMap()(1.0))
#Luca  # cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhbb_eff_e_MVAID_Zll_13TeV','shape',ch.SystMap()(1.0))
#Luca  # cb.cp().channel(['Wen','Zee']).AddSyst(cb,'CMS_vhbb_eff_e_tracker_13TeV','shape',ch.SystMap()(1.0))
#Luca  # cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_trigger_Zll_13TeV','shape',ch.SystMap()(1.0))
#Luca  # cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_MVAID_Zll_13TeV','shape',ch.SystMap()(1.0))
#Luca  # cb.cp().channel(['Wmn','Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_tracker_13TeV','shape',ch.SystMap()(1.0))
#Luca  # cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhbb_eff_m_ISO_Zll_13TeV','shape',ch.SystMap()(1.0))
#Luca
#Luca  # met efficiencies
#Luca  cb.cp().channel(['Znn']).AddSyst(cb,'CMS_vhbb_trigger_MET_13TeV_2016','lnN',ch.SystMap()(1.02))
#Luca
#Luca  # VpT reweightings
#Luca  cb.cp().process(['TT']).AddSyst(cb,'CMS_vhbb_topptreweighting_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca
#Luca  cb.cp().channel(['Wen','Wmn']).process(['Wj0b']).AddSyst(cb,'CMS_vhbb_ptwweights_wlf_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca
#Luca  cb.cp().channel(['Wen','Wmn']).process(['Wj1b' 'Wj2b' 's_Top']).AddSyst(cb,'CMS_vhbb_ptwweights_whf_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca
#Luca#  cb.cp().AddSyst(cb,
#Luca#      'CMS_vhbb_EWK_Zll','shape',ch.SystMap('channel','bin_id','process')
#Luca#      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb'],1.0))
#Luca  
#Luca  #Jet energy scale
#Luca  cb.cp().AddSyst(cb,'CMS_res_j_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  # cb.cp().AddSyst(cb,'CMS_res_j_reg_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  
#Luca  # cb.cp().AddSyst(cb,'CMS_scale_j_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca
#Luca  # split as JET/MET recommends
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpDataMC_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtRef_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtBB_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtEC1_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtEC2_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_PileUpPtHF_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeBal_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeJEREC1_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeJEREC2_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeJERHF_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeFSR_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeStatFSR_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeStatEC_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativeStatHF_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativePtBB_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativePtHF_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativePtEC1_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_RelativePtEC2_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_AbsoluteScale_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_AbsoluteMPFBias_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_AbsoluteStat_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_SinglePionECAL_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_SinglePionHCAL_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_Fragmentation_13TeV_2016','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_scale_j_FlavorQCD_13TeV_2016','shape',ch.SystMap()(1.0))
      
#Luca  #Need to filter the uncertainty for processes it doesn't make sense for:
#Luca  #cb.FilterSysts(lambda x: x.process()=='Zj1b' and x.bin_id()==7 and x.name()=='CMS_scale_j_FlavorQCD_13TeV')
#Luca
#Luca  #b-tagging uncertainties
#Luca  
#Luca  # differential in pt/eta
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightJES_13TeV_2016_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHF_13TeV_2016_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLF_13TeV_2016_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats1_13TeV_2016_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats1_13TeV_2016_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightHFStats2_13TeV_2016_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightLFStats2_13TeV_2016_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr1_13TeV_2016_pt4_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt0_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt0_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt0_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt1_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt1_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt1_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt2_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt2_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt2_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt3_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt3_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt3_eta2','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt4_eta0','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt4_eta1','shape',ch.SystMap()(1.0))
#Luca  cb.cp().AddSyst(cb,'CMS_bTagWeightcErr2_13TeV_2016_pt4_eta2','shape',ch.SystMap()(1.0))

  # EXCLUDE PROBLEMATIC NUISANCES for 2016 shapes
  # cb.FilterSysts(lambda x: 
  #                       x.name() in 'CMS_res_j_13TeV_2016'
  #                       )
#Luca  cb.FilterSysts(lambda x: 
#Luca                        x.process() in ['VVLF'] and 
#Luca                        x.type() in 'shape'
#Luca                        )
