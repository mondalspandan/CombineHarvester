#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
#Luca test 2017 commented out --> import CombineHarvester.VHcc.systematics_vhcc_allcr as systs
import CombineHarvester.VHcc.systematics_vhcc_FullRun2_altSplit_cjbjll as systs
import ROOT as R
import glob
import numpy as np
import os
import sys
import argparse
from CombineHarvester.VHcc.LaunchOptComb import computeLimit

def matching_proc(p,s):
  return ((p.bin()==s.bin()) and (p.process()==s.process()) and (p.signal()==s.signal()) 
          and (p.analysis()==s.analysis()) and  (p.era()==s.era()) 
          and (p.channel()==s.channel()) and (p.bin_id()==s.bin_id()) and (p.mass()==s.mass()))

def drop_zero_procs(chob,proc):
  null_yield = not (proc.rate() > 0.)
  if(null_yield):
    chob.FilterSysts(lambda sys: matching_proc(proc,sys)) 
  return null_yield

def drop_zero_systs(syst):
  null_yield = (not (syst.value_u() > 0. and syst.value_d()>0.) ) and syst.type() in 'shape'
  if(null_yield):
    print 'Dropping systematic ',syst.name(),' for region ', syst.bin(), ' ,process ', syst.process(), '. up norm is ', syst.value_u() , ' and down norm is ', syst.value_d()
    #chob.FilterSysts(lambda sys: matching_proc(proc,sys)) 
  return null_yield

def collect_as(coll_type):
  class Collect_as(argparse.Action):
    def __call__(self, parser, namespace, values, options_string=None):
      setattr(namespace, self.dest, coll_type(values))
  return Collect_as
  
parser = argparse.ArgumentParser()
parser.add_argument(
 '--channel', default='all', help="""Which channels to run? Supported options: 'all', 'Zee', 'Zmm', 'Zll', 'Wen', 'Wmn','Wln'""")
parser.add_argument(
 '--output_folder', default='vhcc2017', help="""Subdirectory of ./output/ where the cards are written out to""")
parser.add_argument(
 '--auto_rebin', action='store_true', help="""Rebin automatically?""")
parser.add_argument(
 '--splitJEC', action='store_true', default=False, help="""Split JEC systematics into sources""")
parser.add_argument(
 '--bbb_mode', default=1, type=int, help="""Sets the type of bbb uncertainty setup. 0: no bin-by-bins, 1: autoMCStats""")
parser.add_argument(
 '--zero_out_low', action='store_true', help="""Zero-out lowest SR bins (purely for the purpose of making yield tables""")
parser.add_argument(
 '--Zmm_fwk', default='AT', help="""Framework the Zmm inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Zee_fwk', default='AT', help="""Framework the Zee inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Wmn_fwk', default='AT', help="""Framework the Wmn inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Wen_fwk', default='AT', help="""Framework the Wen inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Znn_fwk', default='AT', help="""Framework the Znn inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--year', default='2017', help="""Year to produce datacards for (2018, 2017 or 2016)""")
parser.add_argument(
 '--extra_folder', default='', help="""Additional folder where cards are""")
parser.add_argument(
 '--rebinning_scheme', default='', help="""Rebinning scheme for CR and SR distributions""")
parser.add_argument(
 '--doVV', default=False, help="""if True assume we are running the VZ(cc) analysis""")
parser.add_argument(
 '--vjetsNLO', default=False, help="""if True assume we are running with V+jets NLO samples""")
parser.add_argument(
 '--mjj',  default=True, help="""if True assume we are running the mjj analysis""")
parser.add_argument(
 '--doHbb',  default=False, help="""if True assume producing the datacards with VHbb as signal process""")
parser.add_argument(
 '--doKinFit',  default=False, help="""if True enable BDT with KinFit in 2L channels""")
parser.add_argument(
 '--nBinSR',  default=15, help="""Set the number of bins in the SRs""")
parser.add_argument(
  '--bins_vec', nargs='+', type=float, default=[0.,0.5,1.0], help="""Set the binning vector""")

args = parser.parse_args()

cb = ch.CombineHarvester()

shapes = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/VHcc/shapes/'

mass = ['125']

chns = []

if args.channel=="all":
  chns = ['Wen','Wmn','Znn','Zee','Zmm']
if 'Zll' in args.channel or 'Zmm' in args.channel:
  chns.append('Zmm')
if 'Zll' in args.channel or 'Zee' in args.channel:
  chns.append('Zee')
if 'Wln' in args.channel or 'Wmn' in args.channel or 'Znn' in args.channel:
  chns.append('Wmn')
if 'Wln' in args.channel or 'Wen' in args.channel or 'Znn' in args.channel:
  chns.append('Wen')
if 'Znn' in args.channel:
  chns.append('Znn')


year = args.year
if year is not "2016" and not "2017" and not "2018":
  print "Year ", year, " not supported! Choose from: '2016', '2017', '2018'"
  sys.exit()

input_fwks = {
  'Wen' : args.Wen_fwk, 
  'Wmn' : args.Wmn_fwk,
  'Zee' : args.Zee_fwk,
  'Zmm' : args.Zmm_fwk,
  'Znn' : args.Znn_fwk
}

for chn in chns:
  if not input_fwks[chn]=='AT':
    print "Framework ", input_fwks[chn], "not supported! Choose from: 'AT'"
    sys.exit()

folder_map = {
  'AT'  : 'AT/'+args.extra_folder
}

input_folders = {
  'Wen' : folder_map[input_fwks['Wen']],
  'Wmn' : folder_map[input_fwks['Wmn']],
  'Zee' : folder_map[input_fwks['Zee']],
  'Zmm' : folder_map[input_fwks['Zmm']],
  'Znn' : folder_map[input_fwks['Znn']]
}

if not args.doVV:
  if not args.doHbb:
    bkg_procs = {
      'Wen' : ['WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother','VVcc'],
      'Wmn' : ['WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother','VVcc'],
      'Zmm' : ['ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother','VVcc'],
      'Zee' : ['ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother','VVcc'],
      'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','Wj_ll','Wj_bj','Wj_cj','VVother','VVcc'],
    }
  else:
    bkg_procs = {
      'Wen' : ['WH_hcc','ZH_hcc','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother','VVcc'],
      'Wmn' : ['WH_hcc','ZH_hcc','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother','VVcc'],
      'Zmm' : ['ZH_hcc','ggZH_hcc','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother','VVcc'],
      'Zee' : ['ZH_hcc','ggZH_hcc','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother','VVcc'],
      'Znn' : ['ZH_hcc','ggZH_hcc','WH_hcc','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','Wj_ll','Wj_bj','Wj_cj','VVother','VVcc'],
    }
    print bkg_procs
else:
    bkg_procs = {
    'Wen' : ['WH_hcc','ZH_hcc','WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother'],
    'Wmn' : ['WH_hcc','ZH_hcc','WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother'],
    'Zmm' : ['ZH_hcc','ggZH_hcc','ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother'],
    'Zee' : ['ZH_hcc','ggZH_hcc','ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother'],
    'Znn' : ['ZH_hcc','ggZH_hcc','WH_hcc','ZH_hbb','ggZH_hbb','WH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','Wj_ll','Wj_bj','Wj_cj','VVother'],
  }

if not args.doVV:
  if not args.doHbb:
    sig_procs = {
      'Wen' : ['WH_hcc','ZH_hcc'],
      'Wmn' : ['WH_hcc','ZH_hcc'],
      'Zmm' : ['ZH_hcc','ggZH_hcc'],
      'Zee' : ['ZH_hcc','ggZH_hcc'],
      'Znn' : ['ZH_hcc','ggZH_hcc','WH_hcc']
    }
  else:
    sig_procs = {
      'Wen' : ['WH_hbb','ZH_hbb'],
      'Wmn' : ['WH_hbb','ZH_hbb'],
      'Zmm' : ['ZH_hbb','ggZH_hbb'],
      'Zee' : ['ZH_hbb','ggZH_hbb'],
      'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb']
    }
    
else:
  sig_procs = {
    'Wen' : ['VVcc'],
    'Wmn' : ['VVcc'],
    'Zmm' : ['VVcc'],
    'Zee' : ['VVcc'],
    'Znn' : ['VVcc']
  }

if args.mjj:

    # don't fit QCD anywhere for Mjj!
    #Luca bkg_procs['Znn'].remove('QCD')

  cats = {
    'Zee' : [(1, 'SR_high_Zee'), (2, 'SR_low_Zee')],
    'Zmm' : [(1, 'SR_high_Zmm'), (2, 'SR_low_Zmm')],
    'Wen' : [(1, 'SR_Wenu')],
    'Wmn' : [(1, 'SR_Wmunu')],
    'Znn' : [(1, 'SR_Znn')]
  }  
        

for chn in chns:
  cb.AddObservations( ['*'], ['vhcc'], ['13TeV'], [chn], cats[chn])
  cb.AddProcesses( ['*'], ['vhcc'], ['13TeV'], [chn], bkg_procs[chn], cats[chn], False)
  cb.AddProcesses( ['*'], ['vhcc'], ['13TeV'], [chn], sig_procs[chn], cats[chn], True)

# Filter QCD from processes in Znn
cb.FilterProcs(lambda x: x.bin_id()==5 and x.channel()=='Znn' and x.process()=='QCD')
cb.FilterProcs(lambda x: x.bin_id()==9 and x.channel()=='Znn' and x.process()=='QCD')
  
systs.AddCommonSystematics(cb)
if year=='2016':
  systs.AddSystematics2016(cb, args.splitJEC)
if year=='2017':
  systs.AddSystematics2017(cb, args.splitJEC)
if year=='2018':
  systs.AddSystematics2018(cb, args.splitJEC)


if args.bbb_mode==0:
  cb.AddDatacardLineAtEnd("* autoMCStats -1")
elif args.bbb_mode==1:
  cb.AddDatacardLineAtEnd("* autoMCStats 0")

# BDT_VH_SR_lowKinFit_Zee_s_Top_CMS_cTagWeight_XSecWJetsUp

for chn in chns:
  file = shapes + input_folders[chn] + "/vhcc_"+chn+"-"+year+".root"
  if input_fwks[chn] == 'AT':
    cb.cp().channel([chn]).backgrounds().bin_id([3,4,5,6,7,8,9,10]).ExtractShapes(
      file, 'BDT_$BIN_$PROCESS', 'BDT_$BIN_$PROCESS_$SYSTEMATIC')
    cb.cp().channel([chn]).signals().bin_id([3,4,5,6,7,8,9,10]).ExtractShapes(
      file, 'BDT_$BIN_$PROCESS', 'BDT_$BIN_$PROCESS_$SYSTEMATIC')
    if not args.doVV:
      cb.cp().channel([chn]).backgrounds().bin_id([1,2]).ExtractShapes(
        file, 'BDT_VH_$BIN_$PROCESS', 'BDT_VH_$BIN_$PROCESS_$SYSTEMATIC')
      cb.cp().channel([chn]).signals().bin_id([1,2]).ExtractShapes(
        file, 'BDT_VH_$BIN_$PROCESS', 'BDT_VH_$BIN_$PROCESS_$SYSTEMATIC')
      if args.doKinFit and (chn=='Zee' or chn=='Zmm'):
        cb.cp().channel([chn]).backgrounds().bin_id([1,2]).ExtractShapes(
        file, 'BDT_VH_$BIN_$PROCESS', 'BDT_VH_$BIN_$PROCESS_$SYSTEMATIC')
        cb.cp().channel([chn]).signals().bin_id([1,2]).ExtractShapes(
        file, 'BDT_VH_$BIN_$PROCESS', 'BDT_VH_$BIN_$PROCESS_$SYSTEMATIC')
    if args.doVV:
      cb.cp().channel([chn]).backgrounds().bin_id([1,2]).ExtractShapes(
        file, 'BDT_VZ_$BIN_$PROCESS', 'BDT_VZ_$BIN_$PROCESS_$SYSTEMATIC')
      cb.cp().channel([chn]).signals().bin_id([1,2]).ExtractShapes(
        file, 'BDT_VZ_$BIN_$PROCESS', 'BDT_VZ_$BIN_$PROCESS_$SYSTEMATIC')

# play with rebinning (and/or cutting) of the shapes

nBinSR = args.nBinSR
if args.rebinning_scheme == 'SR_nb': # rebinning for H-analysis
  print("===> Rebinning the SR with number of bins = ",nBinSR)
  binning=np.linspace(0.0,1.0,int(nBinSR))
  print 'binning in SRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([1,2]).VariableRebin(binning)
  binning=np.linspace(0.0,1.0,int(nBinSR))
  print 'binning in SRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([1]).VariableRebin(binning)

bins_vec = args.bins_vec
if args.rebinning_scheme == 'SR_Scan': # rebinning for H-analysis
  print("Binning Vector", bins_vec)
  cb.cp().channel(['Zee','Zmm']).bin_id([1,2]).VariableRebin(bins_vec)
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([1]).VariableRebin(bins_vec)

if args.rebinning_scheme == 'rebinSRonly': # rebinning for H-analysis
  binning=np.linspace(0.0,1.0,int(nBinSR))
  print 'binning in SRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([1,2]).VariableRebin(binning)
  binning=np.linspace(0.0,1.0,int(nBinSR))
  print 'binning in SRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([1]).VariableRebin(binning)
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([3,4]).VariableRebin(binning)
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([3]).VariableRebin(binning)

  
cb.FilterProcs(lambda x: drop_zero_procs(cb,x))
cb.FilterSysts(lambda x: drop_zero_systs(x))




if year=='2016':
  cb.cp().RenameSystematic(cb,'CMS_PrefireWeight','CMS_PrefireWeight_13TeV_2016')
if year=='2017':
  cb.cp().RenameSystematic(cb,'CMS_PrefireWeight','CMS_PrefireWeight_13TeV_2017')

cb.cp().process(['TT']).RenameSystematic(cb,'CMS_LHE_pdf_TT','CMS_LHE_pdf_ttbar')
cb.cp().process(['TT']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_TT','CMS_LHE_weights_scale_muR_ttbar')
cb.cp().process(['TT']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_TT','CMS_LHE_weights_scale_muF_ttbar')
#cb.cp().process(['VVother']).RenameSystematic(cb,'CMS_LHE_weights_pdf_VVother','CMS_LHE_weights_pdf_vvother')
cb.cp().process(['VVother']).RenameSystematic(cb,'CMS_LHE_pdf_VVother','CMS_LHE_pdf_vvother')
#cb.cp().process(['VVcc']).RenameSystematic(cb,'CMS_LHE_weights_pdf_VVcc','CMS_LHE_weights_pdf_vzcc')
cb.cp().process(['VVcc']).RenameSystematic(cb,'CMS_LHE_pdf_VVcc','CMS_LHE_pdf_vzcc')
cb.cp().channel(['Wen','Wmn','Zmm','Zee']).process(['VVother']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_VVother','CMS_LHE_weights_scale_muR_vvother')
cb.cp().channel(['Wen','Wmn','Zmm','Zee']).process(['VVcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_VVcc','CMS_LHE_weights_scale_muR_vzcc')
cb.cp().channel(['Wen','Wmn','Zmm','Zee']).process(['VVother']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_VVother','CMS_LHE_weights_scale_muF_vvother')
cb.cp().channel(['Wen','Wmn','Zmm','Zee']).process(['VVcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_VVcc','CMS_LHE_weights_scale_muF_vzcc')

if args.vjetsNLO:
  cb.FilterSysts(lambda x: x.name()=="CMS_Wj_0hf_vhcc_vjetnlodetajjrw_13TeV_2016")
  cb.FilterSysts(lambda x: x.name()=="CMS_Wj_1hf_vhcc_vjetnlodetajjrw_13TeV_2016")
  cb.FilterSysts(lambda x: x.name()=="CMS_Wj_2hf_vhcc_vjetnlodetajjrw_13TeV_2016") 
  cb.FilterSysts(lambda x: x.name()=="CMS_Zj_0hf_vhcc_vjetnlodetajjrw_13TeV_2016")
  cb.FilterSysts(lambda x: x.name()=="CMS_Zj_1hf_vhcc_vjetnlodetajjrw_13TeV_2016")
  cb.FilterSysts(lambda x: x.name()=="CMS_Zj_2hf_vhcc_vjetnlodetajjrw_13TeV_2016") 
  #cb.FilterSysts(lambda x: x.name()=="CMS_vhcc_topptWeight_13TeV_2016") 
  cb.FilterSysts(lambda x: x.name()=="CMS_vhcc_ptwweights_13TeV_2016") 
  cb.FilterSysts(lambda x: x.name()=="CMS_vhcc_ptzweights_13TeV_2016") 
  cb.FilterSysts(lambda x: x.name()=="CMS_vhcc_vjetnlodetajjrw_13TeV_2016") 
  

if args.doVV:
  cb.SetGroup('signal_theory',['CMS_LHE_weights_pdf_VVcc','.*LHE_weights.*VVcc'])
  cb.SetGroup('bkg_theory',['pdf_Higgs.*','pdf_qqbar','pdf_gg','CMS_LHE_weights_pdf_VVother','CMS_vhbb_ST','.*LHE_weights.*ZHbb*','.*LHE_weights.*WHbb*','.*LHE_weights.*ggZHbb*','.*LHE_weights.*TT.*','.*LHE_weights.*VVother','.*LHE_weights.*Zj_ll.*','LHE_weights.*Zj_bj.*','LHE_weights.*Zj_cj.*','LHE_weights.*Wj_ll.*','LHE_weights.*Wj_bj.*','LHE_weights.*Wj_cj.*','LHE_weights.*s_Top.*','LHE_weights.*QCD.*','.*LHE_weights.*ZHcc*','.*LHE_weights.*WHcc*','.*LHE_weights.*ggZHcc*','BR_hcc','QCDscale_ggZH','QCDscale_VH',])
else:
  cb.SetGroup('signal_theory',['pdf_Higgs.*','BR_hcc','QCDscale_ggZH','QCDscale_VH','.*LHE_weights.*ZHcc*','.*LHE_weights.*WHcc*','.*LHE_weights.*ggZHcc*'])
  cb.SetGroup('bkg_theory',['pdf_qqbar','pdf_gg','CMS_LHE_weights_pdf_VV*','CMS_vhbb_ST','.*LHE_weights.*ZHbb*','.*LHE_weights.*WHbb*','.*LHE_weights.*ggZHbb*','.*LHE_weights.*TT.*','.*LHE_weights.*VV*','.*LHE_weights.*Zj_ll.*','LHE_weights.*Zj_bj.*','LHE_weights.*Zj_cj.*','LHE_weights.*Wj_ll.*','LHE_weights.*Wj_bj.*','LHE_weights.*Wj_cj.*','LHE_weights.*s_Top.*','LHE_weights.*QCD.*'])
  
cb.SetGroup('sim_modelling',['CMS_vhcc_ptwweights_13TeV_.*','CMS_vhcc_ptzweights_13TeV_.*','CMS_vhcc_topptWeight_13TeV_.*','.*vhcc_vjetnlodetajjrw.*','heavyFlavHadFrac_mismodelling.*'])
cb.SetGroup('jes',['CMS_scale_j.*'])
cb.SetGroup('jer',['CMS_res_j_13TeV.*'])
cb.SetGroup('ctag',['CMS_cTagWeight.*'])
cb.SetGroup('lumi',['lumi_13TeV.*','.*puWeight.*'])
cb.SetGroup('lep_eff',['.*eff_e.*','.*eff_m.*'])
cb.SetGroup('met',['.*MET.*'])

rebin = ch.AutoRebin().SetBinThreshold(0.).SetBinUncertFraction(1.0).SetRebinMode(1).SetPerformRebin(True).SetVerbosity(1)

#binning=np.linspace(0.2,1.0,num=13)
#print binning


if args.auto_rebin:
  rebin.Rebin(cb, cb)
        
ch.SetStandardBinNames(cb)


if args.rebinning_scheme == 'SR_nb' :
  writer=ch.CardWriter("OptimizeBinSR_NomShape_" + year +"/"+args.output_folder + "nb_"+str(nBinSR)+"/$TAG/$BIN"+year+".txt",
                       "OptimizeBinSR_NomShape_" + year +"/"+args.output_folder + "nb_"+str(nBinSR)+"/$TAG/vhcc_input_$BIN"+year+".root")

elif args.rebinning_scheme == 'SR_Scan':
  outdir = "OptimizeBinSR_NomShape_" + year +"/"+args.output_folder + "SR_Scan"
  writer=ch.CardWriter(outdir+"/$TAG/$BIN"+year+".txt", outdir+"/$TAG/vhcc_input_$BIN"+year+".root")
  
else:
  writer=ch.CardWriter("output/" + args.output_folder + year + "/$TAG/$BIN"+year+".txt",
                       "output/" + args.output_folder + year +"/$TAG/vhcc_input_$BIN"+year+".root")
writer.SetWildcardMasses([])
writer.SetVerbosity(0);
                
#Combined:
writer.WriteCards("cmb",cb);
#Luca writer.WriteCards("cmb_CRonly",cb.cp().bin_id([3,4,5,6,7,8]));

#Per channel:
for chn in chns:
  writer.WriteCards(chn,cb.cp().channel([chn]))


writer.WriteCards("Znn",cb.cp().bin_id([1]).channel(['Znn']))
writer.WriteCards("Wen",cb.cp().bin_id([1]).channel(['Wen']))
writer.WriteCards("Wmn",cb.cp().bin_id([1]).channel(['Wmn']))
writer.WriteCards("Zee",cb.cp().bin_id([1,2]).channel(['Zee']))
writer.WriteCards("Wmm",cb.cp().bin_id([1,2]).channel(['Zmm']))



info_map=computeLimit(outdir,['Zee'])
print info_map

for i in range(0,len(info_map)):
  if info_map[i][0] is 'Zee':
    print('printing electron channel')
    print("Info from scanner = ",info_map[i][0], float(info_map[i][1]), bins_vec)
    outFzee = open("results_opt_Zee.txt", "a+")
    print >> outFzee,"Info from scanner = ",info_map[i][0], float(info_map[i][1]), bins_vec
  if info_map[i][0] is 'Zmm':
    print('printing muon channel')
    print("Info from scanner = ",info_map[i][0], float(info_map[i][1]), bins_vec)
    outFzmm = open("results_opt_Zmm.txt", "a+")
    print >> outFzmm,"Info from scanner = ",info_map[i][0], float(info_map[i][1]), bins_vec
