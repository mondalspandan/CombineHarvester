import CombineHarvester.CombineTools.ch as ch

def AddCommonSystematics(cb):
  
  signal = cb.cp().signals().process_set()
  # rateParams
  
  # Theory uncertainties: signal
  cb.cp().AddSyst(cb,
                  'pdf_Higgs_qqbar', 'lnN', ch.SystMap('process')
                  (['ZH_hbb','ZH_hcc'],1.016)
                  (['WH_hbb','WH_hcc'],1.019))
  
  cb.cp().process(['ggZH_hbb','ggZH_hbb']).AddSyst(cb,'pdf_Higgs_gg', 'lnN', ch.SystMap()(1.024))
  
  cb.cp().process(signal).AddSyst(cb,'BR_hcc', 'lnN', ch.SystMap()((1.05,0.97)))
  cb.cp().process(['ZH_hcc','WH_hcc','ggZH_hcc']).AddSyst(cb,'BR_hcc', 'lnN', ch.SystMap()((1.05,0.97)))
  cb.cp().process(['ZH_hbb','WH_hbb','ggZH_hbb']).AddSyst(cb,'BR_hbb', 'lnN', ch.SystMap()(1.005))
#Luca   cb.cp().process(['ZH_hbb','WH_hbb','ggZH_hbb']).AddSyst(cb,'BR_hbb', 'lnN', ch.SystMap()(1.20))

  
  cb.cp().process(['ggZH_hbb','ggZH_hcc']).AddSyst(cb,'QCDscale_ggZH', 'lnN',ch.SystMap()((1.251,0.811)))
  
  cb.cp().AddSyst(cb,'QCDscale_VH', 'lnN', ch.SystMap('process') 
                  (['ZH_hbb','ZH_hcc'], (1.038,0.969)) 
                  (['WH_hbb','WH_hcc'], (1.005,0.993)))

  cb.cp().AddSyst(cb,
      'CMS_vhcc_boost_EWK_13TeV', 'lnN', ch.SystMap('channel','process') 
      (['Zee','Zmm'],['ZH_hcc','ZH_hbb'], 1.02)
      (['Znn'],['ZH_hcc','WH_hcc','ggZH_hcc','ZH_hbb','WH_hbb','ggZH_hbb'],1.02)
      (['Wen','Wmn'],['WH_hcc','ZH_hcc','WH_hbb','ZH_hbb'],1.02)) 
  
  # Theory uncertainties: backgrounds -> to be checked!
  cb.cp().AddSyst(cb,
                  'pdf_qqbar', 'lnN', ch.SystMap('channel','process') 
                  (['Zee','Zmm'],['Zj_ll','Zj_blc','Zj_bbc','Zj_cc','VVother''VVcc'], 1.01) 
                  (['Znn'],['VVother','VVcc'],1.01)
                  (['Wen','Wmn'],['VVother','VVcc'],1.01)) 
 
  cb.cp().AddSyst(cb,
                  'pdf_gg', 'lnN', ch.SystMap('channel','process')
                  (['Zee','Zmm','Znn'],['TT','s_Top','QCD'], 1.01)
                  (['Wen','Wmn'], ['s_Top'],1.01))
  
  cb.cp().AddSyst(cb,
                  'QCDscale_ttbar', 'lnN', ch.SystMap('channel','process') 
                  #(['Zee','Zmm','Wen','Wmn','Znn'],['s_Top'], 1.06)
                  (['Zee','Zmm','Wen','Wmn','Znn'],['TT'],1.06)
                  ) 

  # Measured cross section uncertainties because we don't have SF
  cb.cp().process(['VVother']).AddSyst(cb,
      'CMS_vhcc_VV', 'lnN', ch.SystMap()(1.15)) 

  cb.cp().process(['VVcc']).AddSyst(cb,
      'CMS_vhcc_VVcc', 'lnN', ch.SystMap()(1.15)) 

  cb.cp().process(['s_Top']).AddSyst(cb,
      'CMS_vhcc_ST', 'lnN', ch.SystMap()(1.15)) 



########################################################################################################################################
### Uncertainties for 2016
########################################################################################################################################
def AddSystematics2016(cb, splitJEC=False):


####################### SCALE FACTORS RATEPARAM
  
  # TT Zll
  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
     'SF_TT_high_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
     'SF_TT_low_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # Zj_ll Zll
  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).AddSyst(cb,
     'SF_Zj_ll_high_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).AddSyst(cb,
     'SF_Zj_ll_low_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # Zj_blc Zll
  cb.cp().channel(['Zee','Zmm']).process(['Zj_blc']).AddSyst(cb,
     'SF_Zj_blc_high_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj_blc']).AddSyst(cb,
     'SF_Zj_blc_low_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # Zj_bbc Zll
  cb.cp().channel(['Zee','Zmm']).process(['Zj_bbc']).AddSyst(cb,
     'SF_Zj_bbc_high_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj_bbc']).AddSyst(cb,
     'SF_Zj_bbc_low_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # Zj_cc Zll
  cb.cp().channel(['Zee','Zmm']).process(['Zj_cc']).AddSyst(cb,
     'SF_Zj_cc_high_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj_cc']).AddSyst(cb,
     'SF_Zj_cc_low_Zll_2016', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # TT Znn
  cb.cp().channel(['Znn']).process(['TT']).AddSyst(cb,
     'SF_TT_Znn_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Zj_ll Znn
  cb.cp().channel(['Znn']).process(['Zj_ll']).AddSyst(cb,
     'SF_Zj_ll_Znn_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Zj_blc Znn
  cb.cp().channel(['Znn']).process(['Zj_blc']).AddSyst(cb,
     'SF_Zj_blc_Znn_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Zj_bbc Znn
  cb.cp().channel(['Znn']).process(['Zj_bbc']).AddSyst(cb,
     'SF_Zj_bbc_Znn_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Zj_cc Znn
  cb.cp().channel(['Znn']).process(['Zj_cc']).AddSyst(cb,
     'SF_Zj_cc_Znn_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # TT Wln
  cb.cp().channel(['Wen','Wmn']).process(['TT']).AddSyst(cb,
     'SF_TT_Wln_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Wj_ll Wln
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_ll']).AddSyst(cb,
     'SF_Wj_ll_Wln_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Wj_blc Wln
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_blc']).AddSyst(cb,
     'SF_Wj_blc_Wln_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Wj_bbc Wln
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_bbc']).AddSyst(cb,
     'SF_Wj_bbc_Wln_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Wj_cc Wln
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_cc']).AddSyst(cb,
     'SF_Wj_cc_Wln_2016', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))


  #Set a sensible range for the rate params
  for syst in cb.cp().syst_type(["rateParam"]).syst_name_set():
    cb.GetParameter(syst).set_range(0.0,5.0)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%% EXPERIMENTAL UNCERTAINTIES

  cb.cp().AddSyst( cb,'lumi_13TeV_2016','lnN', ch.SystMap()(1.025))
 
#============= lepton efficiencies

  cb.cp().channel(['Wmn']).AddSyst(cb,'CMS_vhcc_eff_m_Wln_13TeV_2016','lnN',ch.SystMap()(1.02))
  cb.cp().channel(['Wen']).AddSyst(cb,'CMS_vhcc_eff_e_Wln_13TeV_2016','lnN',ch.SystMap()(1.02))
  cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhcc_eff_m_Zll_13TeV_2016','lnN',ch.SystMap()(1.04))
  cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhcc_eff_e_Zll_13TeV_2016','lnN',ch.SystMap()(1.04))

#=============  met efficiencies
  cb.cp().channel(['Znn']).AddSyst(cb,'CMS_vhcc_trigger_MET_13TeV_2016','lnN',ch.SystMap()(1.02))


  
########################################################################################################################################
### Uncertainties for 2017
########################################################################################################################################
def AddSystematics2017(cb, splitJEC=False):


####################### SCALE FACTORS RATEPARAM
  
  # TT Zll
  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
     'SF_TT_high_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
     'SF_TT_low_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # Zj_ll Zll
  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).AddSyst(cb,
     'SF_Zj_ll_high_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).AddSyst(cb,
     'SF_Zj_ll_low_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # Zj_blc Zll
  cb.cp().channel(['Zee','Zmm']).process(['Zj_blc']).AddSyst(cb,
     'SF_Zj_blc_high_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj_blc']).AddSyst(cb,
     'SF_Zj_blc_low_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # Zj_bbc Zll
  cb.cp().channel(['Zee','Zmm']).process(['Zj_bbc']).AddSyst(cb,
     'SF_Zj_bbc_high_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj_bbc']).AddSyst(cb,
     'SF_Zj_bbc_low_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # Zj_cc Zll
  cb.cp().channel(['Zee','Zmm']).process(['Zj_cc']).AddSyst(cb,
     'SF_Zj_cc_high_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj_cc']).AddSyst(cb,
     'SF_Zj_cc_low_Zll_2017', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8,10],1.0))

  # TT Znn
  cb.cp().channel(['Znn']).process(['TT']).AddSyst(cb,
     'SF_TT_Znn_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Zj_ll Znn
  cb.cp().channel(['Znn']).process(['Zj_ll']).AddSyst(cb,
     'SF_Zj_ll_Znn_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Zj_blc Znn
  cb.cp().channel(['Znn']).process(['Zj_blc']).AddSyst(cb,
     'SF_Zj_blc_Znn_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Zj_bbc Znn
  cb.cp().channel(['Znn']).process(['Zj_bbc']).AddSyst(cb,
     'SF_Zj_bbc_Znn_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Zj_cc Znn
  cb.cp().channel(['Znn']).process(['Zj_cc']).AddSyst(cb,
     'SF_Zj_cc_Znn_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # TT Wln
  cb.cp().channel(['Wen','Wmn']).process(['TT']).AddSyst(cb,
     'SF_TT_Wln_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Wj_ll Wln
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_ll']).AddSyst(cb,
     'SF_Wj_ll_Wln_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Wj_blc Wln
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_blc']).AddSyst(cb,
     'SF_Wj_blc_Wln_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Wj_bbc Wln
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_bbc']).AddSyst(cb,
     'SF_Wj_bbc_Wln_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))

  # Wj_cc Wln
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_cc']).AddSyst(cb,
     'SF_Wj_cc_Wln_2017', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7,9],1.0))


  #Set a sensible range for the rate params
  for syst in cb.cp().syst_type(["rateParam"]).syst_name_set():
    cb.GetParameter(syst).set_range(0.0,5.0)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%% EXPERIMENTAL UNCERTAINTIES

  cb.cp().AddSyst( cb,'lumi_13TeV_2017','lnN', ch.SystMap()(1.023))

 
#============= lepton efficiencies

  cb.cp().channel(['Wmn']).AddSyst(cb,'CMS_vhcc_eff_m_Wln_13TeV_2017','lnN',ch.SystMap()(1.02))
  cb.cp().channel(['Wen']).AddSyst(cb,'CMS_vhcc_eff_e_Wln_13TeV_2017','lnN',ch.SystMap()(1.02))
  cb.cp().channel(['Zmm']).AddSyst(cb,'CMS_vhcc_eff_m_Zll_13TeV_2017','lnN',ch.SystMap()(1.04))
  cb.cp().channel(['Zee']).AddSyst(cb,'CMS_vhcc_eff_e_Zll_13TeV_2017','lnN',ch.SystMap()(1.04))

#=============  met efficiencies
  cb.cp().channel(['Znn']).AddSyst(cb,'CMS_vhcc_trigger_MET_13TeV_2017','lnN',ch.SystMap()(1.02))
