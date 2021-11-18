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

def adjust_shape(proc,nbins):
  new_hist = proc.ShapeAsTH1F();
  new_hist.Scale(proc.rate())
  for i in range(1,new_hist.GetNbinsX()+1-nbins):
    new_hist.SetBinContent(i,0.)
  proc.set_shape(new_hist,True)

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

def drop_znnqcd(chob,proc):
  drop_process =  proc.process()=='QCD' and proc.channel()=='Znn' and proc.bin_id()==5
  if(drop_process):
    chob.FilterSysts(lambda sys: matching_proc(proc,sys)) 
  return drop_process

def drop_LHEweights(chob,proc,sys):
  drop_syst =  (proc.bin_id()==3 or proc.bin_id()==4 or proc.bin_id()==7 or proc.bin_id()==8)
  if(drop_syst):
    chob.FilterSysts(matching_proc(proc,sys)) 
  return drop_syst

def matching_proc(p,s):
  return ((p.bin()==s.bin()) and (p.process()==s.process()) and (p.signal()==s.signal()) 
          and (p.analysis()==s.analysis()) and  (p.era()==s.era()) 
          and (p.channel()==s.channel()) and (p.bin_id()==s.bin_id()) and (p.mass()==s.mass()))


def remove_norm_effect(syst):
  syst.set_value_u(1.0)
  syst.set_value_d(1.0)

def symm(syst,nominal):
  print 'Symmetrising systematic ', syst.name(), ' in region ', syst.bin(), ' for process ', syst.process()
  hist_u = syst.ShapeUAsTH1F()
  hist_u.Scale(nominal.Integral()*syst.value_u())
  hist_d = nominal.Clone()
  hist_d.Scale(2)
  hist_d.Add(hist_u,-1)
  syst.set_shapes(hist_u,hist_d,nominal)
  
  
def symmetrise_syst(chob,proc,sys_name):
  nom_hist = proc.ShapeAsTH1F()
  nom_hist.Scale(proc.rate())
  chob.ForEachSyst(lambda s: symm(s,nom_hist) if (s.name()==sys_name and matching_proc(proc,s)) else None)

def increase_bin_errors(proc):
  print 'increasing bin errors for process ', proc.process(), ' in region ', proc.bin()
  new_hist = proc.ShapeAsTH1F();
  new_hist.Scale(proc.rate())
  for i in range(1,new_hist.GetNbinsX()+1):
    new_hist.SetBinError(i,np.sqrt(2)*new_hist.GetBinError(i))
  proc.set_shape(new_hist,False)

def decrease_bin_errors(proc):
  print 'decreasing bin errors for process ', proc.process(), ' in region ', proc.bin()
  new_hist = proc.ShapeAsTH1F();
  new_hist.Scale(proc.rate())
  for i in range(1,new_hist.GetNbinsX()+1):
    new_hist.SetBinError(i,new_hist.GetBinError(i)/2.0)
  proc.set_shape(new_hist,False)

def drop_noRealShape_systs(proc,syst):
  diff_lim=0.000001
  if syst.type()=='shape' : 
    hist_u = syst.ShapeUAsTH1F()
    hist_d = syst.ShapeDAsTH1F()
    hist_nom = proc.ShapeAsTH1F()
    hist_nom.Scale(1./hist_nom.Integral())
    up_diff=0
    down_diff=0
    #print "SYSTEMATICS = ",syst.name(),syst.process(),syst.bin()
    for i in range(1,hist_u.GetNbinsX()+1):
      if hist_nom.GetBinContent(i)!=0:
        up_diff+=2*(abs(hist_u.GetBinContent(i)-hist_nom.GetBinContent(i)))/(abs(hist_u.GetBinContent(i))+abs(hist_nom.GetBinContent(i)))
        down_diff+=2*(abs(hist_d.GetBinContent(i)-hist_nom.GetBinContent(i)))/(abs(hist_u.GetBinContent(i))+abs(hist_nom.GetBinContent(i)))
      else:
        up_diff+=0
        down_diff+=0
    null_yield = (up_diff<diff_lim and down_diff<diff_lim)
    if(null_yield):
      #print "Uncertainty has no real shape effect. Summed rel. diff. per bin between norm. nominal and up/down shape: ",up_diff, down_diff
      print 'Dropping systematic ',syst.name(),' for region ', syst.bin(), ' ,process ', syst.process(), '. Up diff is ',up_diff , ' and Down diff is ', down_diff
      print('')
    return null_yield  

#def drop_ShapeSameDir_systs(proc,syst):
#  diff_lim=0.03
#  if syst.type()=='shape' : 
#    if ( (syst.value_u() > 1. and syst.value_d() > 1.) or (syst.value_u() < 1. and syst.value_d() < 1.)):
#      null_yield = (min( abs(1-syst.value_u()), abs(1-syst.value_d()) ) > diff_lim)
#      if(null_yield):
#        #print "Uncertainty has no real shape effect. Summed rel. diff. per bin between norm. nominal and up/down shape: ",up_diff, down_diff
#        print 'Dropping systematic ',syst.name(),' for region ', syst.bin(), ' ,process ', syst.process(), '. Up/Down normalisations go in the same direction: up int ', syst.value_u() , ' and down int is ', syst.value_d()
#      return null_yield  

def drop_ShapeSameDir_systs(proc,syst):
  if syst.type()=='shape' : 
    null_yield = ( (syst.value_u() > 1. and syst.value_d() > 1.) or (syst.value_u() < 1. and syst.value_d() < 1.))
    if(null_yield):
      #print "Uncertainty has no real shape effect. Summed rel. diff. per bin between norm. nominal and up/down shape: ",up_diff, down_diff
      print 'Dropping systematic ',syst.name(),' for region ', syst.bin(), ' ,process ', syst.process(), '. Up/Down normalisations go in the same direction: up int ', syst.value_u() , ' and down int is ', syst.value_d()
    return null_yield  


def drop_SameUpDownShapes_systs(proc,syst):
  if proc.bin_id()==1:
    diff_lim=0.001
    if syst.type()=='shape' : 
      hist_u = syst.ShapeUAsTH1F()
      hist_d = syst.ShapeDAsTH1F()
      hist_nom = proc.ShapeAsTH1F()
      hist_nom.Scale(1./hist_nom.Integral())
      up_diff=0
      down_diff=0
      #print "SYSTEMATICS = ",syst.name(),syst.process(),syst.bin()
      for i in range(1,hist_u.GetNbinsX()+1):
        if hist_nom.GetBinContent(i)!=0:
          up_diff+=2*(abs(hist_u.GetBinContent(i)-hist_nom.GetBinContent(i)))/(abs(hist_u.GetBinContent(i))+abs(hist_nom.GetBinContent(i)))
          down_diff+=2*(abs(hist_d.GetBinContent(i)-hist_nom.GetBinContent(i)))/(abs(hist_u.GetBinContent(i))+abs(hist_nom.GetBinContent(i)))
        else:
          up_diff+=0
          down_diff+=0
      null_yield = ((up_diff<diff_lim and down_diff<diff_lim) and (syst.value_u() == syst.value_d()))
      if(null_yield):
        #print "Uncertainty has no real shape effect. Summed rel. diff. per bin between norm. nominal and up/down shape: ",up_diff, down_diff
        print 'Dropping systematic ',syst.name(),' for region ', syst.bin(), ' ,process ', syst.process(), '. Up/Down shapes are exactly the same: up int ', syst.value_u() , ' and down int is ', syst.value_d()
        print ' --> Up diff is ',up_diff , ' and Down diff is ', down_diff
        print('')
      return null_yield  


#    if syst.name()=="CMS_cTagWeight_Stat_2016":
#      print "SYSTEMATICS = ",syst.name(),syst.process(),syst.bin()
#      print("Up: ", hist_u.Integral())
#      print("Nominal: ", hist_nom.Integral())
#      print("Down: ", hist_d.Integral())
#
#    for i in range(1,hist_u.GetNbinsX()+1):
#      if hist_nom.GetBinContent(i)!=0:
#        # sum in each bin of Up-Nom
#        up_diff+=(hist_u.GetBinContent(i)-hist_nom.GetBinContent(i))
#        # sum in each bin of Down-Nom
#        down_diff+=(hist_d.GetBinContent(i)-hist_nom.GetBinContent(i))
#        diff = abs(up_diff)+abs(down_diff)
#      else:
#        up_diff+=0
#        down_diff+=0
#    null_yield = (up_diff<diff_lim and diff>diff_lim)
#    if(null_yield):
#      #print "Uncertainty has no real shape effect. Summed rel. diff. per bin between norm. nominal and up/down shape: ",up_diff, down_diff
#      print 'Dropping systematic ',syst.name(),' for region ', syst.bin(), ' ,process ', syst.process(), '. up int ', hist_u.Integral() , ' and down int is ', hist_d.Integral()
#    return null_yield  


def PrintProc(proc):
  print  proc.channel(), proc.bin_id(), proc.process()

def PrintSyst(syst,proc):
  print  syst.channel(), syst.bin_id(), syst.process(), syst.name(), proc.process()
  
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
 '--CutRjj', default=False, help="""if True assume we are applying the dR(jj)>1.0 cut""")
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
 '--edge',  default=0.5, help="""Set the fraction of the edge of the bin""")

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
      'Wen' : ['WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother','VZcc'],
      'Wmn' : ['WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother','VZcc'],
      'Zmm' : ['ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother','VZcc'],
      'Zee' : ['ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother','VZcc'],
      'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','Wj_ll','Wj_bj','Wj_cj','VVother','VZcc'],
      #'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','Wj_ll','Wj_bj','Wj_cj','VVother','VZcc'],
    }
  else:
    bkg_procs = {
      'Wen' : ['WH_hcc','ZH_hcc','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother','VZcc'],
      'Wmn' : ['WH_hcc','ZH_hcc','s_Top','TT','Wj_ll','Wj_bj','Wj_cj','Zj_ll','Zj_bj','Zj_cj','VVother','VZcc'],
      'Zmm' : ['ZH_hcc','ggZH_hcc','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother','VZcc'],
      'Zee' : ['ZH_hcc','ggZH_hcc','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','VVother','VZcc'],
      'Znn' : ['ZH_hcc','ggZH_hcc','WH_hcc','s_Top','TT','Zj_ll','Zj_bj','Zj_cj','Wj_ll','Wj_bj','Wj_cj','VVother','VZcc'],
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
    'Wen' : ['VZcc'],
    'Wmn' : ['VZcc'],
    'Zmm' : ['VZcc'],
    'Zee' : ['VZcc'],
    'Znn' : ['VZcc']
  }

if args.mjj:

    # don't fit QCD anywhere for Mjj!
    #Luca bkg_procs['Znn'].remove('QCD')

  if args.rebinning_scheme == 'SR_nb':
    cats = {
      'Zee' : [(1, 'SR_high_Zee'), (2, 'SR_low_Zee')],
      'Zmm' : [(1, 'SR_high_Zmm'), (2, 'SR_low_Zmm')],
      'Wen' : [(1, 'SR_Wenu')],
      'Wmn' : [(1, 'SR_Wmunu')],
      'Znn' : [(1, 'SR_Znn')]
    }
    
  elif args.rebinning_scheme is not 'SR_nb':
    cats = {
      'Zee' : [
        #        (1, 'SR_highKinFit_Zee'), (2, 'SR_lowKinFit_Zee'), (3, 'Zlf_high_Zee'), (4,'Zlf_low_Zee'),
        (1, 'SR_high_Zee'), (2, 'SR_low_Zee'), (3, 'Zlf_high_Zee'), (4,'Zlf_low_Zee'),
#        (3, 'Zlf_high_Zee'), (4,'Zlf_low_Zee'),
        (5, 'Zhf_high_Zee'), (6, 'Zhf_low_Zee'), 
        (7,'ttbar_high_Zee'), (8,'ttbar_low_Zee'),(9,'Zcc_high_Zee'), (10,'Zcc_low_Zee')
        #(5,'Zcc_high_Zee'), (6,'Zcc_low_Zee'),(7,'ttbar_high_Zee'), (8,'ttbar_low_Zee')
      ],
      'Zmm' : [
        #        (1, 'SR_highKinFit_Zmm'), (2, 'SR_lowKinFit_Zmm'), (3, 'Zlf_high_Zmm'), (4,'Zlf_low_Zmm'),
        (1, 'SR_high_Zmm'), (2, 'SR_low_Zmm'), (3, 'Zlf_high_Zmm'), (4,'Zlf_low_Zmm'),
        #(3, 'Zlf_high_Zmm'), (4,'Zlf_low_Zmm'),
        (5, 'Zhf_high_Zmm'), (6, 'Zhf_low_Zmm'), 
        (7,'ttbar_high_Zmm'), (8,'ttbar_low_Zmm'),(9,'Zcc_high_Zmm'), (10,'Zcc_low_Zmm')
        #(5,'Zcc_high_Zmm'), (6,'Zcc_low_Zmm'),(7,'ttbar_high_Zmm'), (8,'ttbar_low_Zmm'),
      ],
      'Wen' : [(1, 'SR_Wenu'), (3,'Wlf_Wenu'), #(5,'Whf_Wenu'), 
               (7,'ttbar_Wenu'), (9,'Wcc_Wenu')],
      'Wmn' : [(1, 'SR_Wmunu'), (3,'Wlf_Wmunu'), #(5,'Whf_Wmunu'), 
               (7,'ttbar_Wmunu'), (9,'Wcc_Wmunu')],
      'Znn' : [(1, 'SR_Znn'), (3,'Vlf_Znn'), (5,'Vhf_Znn'), (7,'ttbar_Znn'), (9,'Vcc_Znn')]
#      'Wen' : [(3,'Wlf_Wenu'), (5,'Whf_Wenu'), (7,'ttbar_Wenu'), (9,'Wcc_Wenu')],
#      'Wmn' : [(3,'Wlf_Wmunu'), (5,'Whf_Wmunu'), (7,'ttbar_Wmunu'), (9,'Wcc_Wmunu')],
#      'Znn' : [(3,'Vlf_Znn'), (5,'Vhf_Znn'), (7,'ttbar_Znn'), (9,'Vcc_Znn')]

    }
    

for chn in chns:
  cb.AddObservations( ['*'], ['vhcc'], ['13TeV'], [chn], cats[chn])
  cb.AddProcesses( ['*'], ['vhcc'], ['13TeV'], [chn], bkg_procs[chn], cats[chn], False)
  cb.AddProcesses( ['*'], ['vhcc'], ['13TeV'], [chn], sig_procs[chn], cats[chn], True)

# Filter QCD from processes in Znn
#cb.FilterProcs(lambda x: x.bin_id()==5 and x.channel()=='Znn' and x.process()=='QCD')
#cb.FilterProcs(lambda x: x.bin_id()==9 and x.channel()=='Znn' and x.process()=='QCD')
# Filter QCD from processis in Wln
  
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
if args.rebinning_scheme == 'zll-rebin':
  binning=np.linspace(0.0,0.9,num=8)
  print 'binning in ZCC-CR fitting variable (Jet_CvsB):',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([9,10]).VariableRebin(binning)


if args.rebinning_scheme == 'LFTT1b_v0': # rebinning for H-analysis

  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([3,4]).VariableRebin(binning)
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([3]).VariableRebin(binning)

  print 'binning in TT CRs: [0., 1.0] for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([7,8]).VariableRebin([0., 1.0])
  print 'binning in TT CRs: [0., 1.0] for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([7]).VariableRebin([0., 1.0])


if args.rebinning_scheme == 'LF1b_v1': # rebinning for H-analysis

  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([3,4]).VariableRebin(binning)
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([3]).VariableRebin(binning)

  print 'binning in TT CRs: [0., 1.0] for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([7,8]).VariableRebin([0., 1.0])
  print 'binning in TT CRs: [0., 1.0] for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([7]).VariableRebin([0., 1.0])

#  print 'binning in HF CRs: [0., 0.133333, 0.266666, 0.399999, 0.533332, 0.666667, 0.733334, 0.8, 0.866667, 0.933334, 1.0] for Zll channels'
#  cb.cp().channel(['Zee','Zmm']).bin_id([5,6]).VariableRebin([0.133333, 0.266666, 0.399999, 0.533332, 0.666667, 0.733334, 0.8, 0.866667, 0.933334, 1.0])
#  print 'binning in HF CRs: [0., 0.133333, 0.266666, 0.399999, 0.533332, 0.666667, 0.733334, 0.8, 0.866667, 0.933334, 1.0] for Wln,Znn channels'
#  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([5]).VariableRebin([0., 0.133333, 0.266666, 0.399999, 0.533332, 0.666667, 0.733334, 0.8, 0.866667, 0.933334, 1.0])
#
   
  #============= 2016 ANALYSIS
  if year=='2016':
    if not args.doVV:
      print("Rebinning signal regions of 2016 VH analyis")
      #'VH_SR_Wenu'
#      cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.073, 0.147, 0.220, 0.293, 0.367, 0.440, 0.513, 0.587, 0.660, 0.697, 0.733, 0.770, 0.807, 0.843, 0.880, 1.000])
      cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.073, 0.147, 0.220, 0.293, 0.367, 0.440, 0.513, 0.587, 0.660, 0.697, 0.733, 0.770, 0.807, 1.000])
      #'VH_SR_Wmunu'                                       
#      cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
      cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.713, 0.750, 0.788, 0.825, 1.000])
      #"VH_SR_Znn"
      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.077, 0.153, 0.230, 0.306, 0.383, 0.459, 0.536, 0.612, 0.689, 0.727, 0.765, 0.803, 0.842, 0.880, 1.000])
      #cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.230, 0.306, 0.383, 0.459, 0.536, 0.612, 0.689, 0.727, 0.765, 0.803, 0.842, 0.880, 1.000])
      #cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.153, 0.230, 0.306, 0.383, 0.459, 0.536, 0.612, 0.689, 0.727, 0.765, 0.803, 0.842, 0.880, 1.000])
      #"VH_SR_high_Zee"
#      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.088, 0.176, 0.264, 0.352, 0.440, 0.528, 0.616, 0.704, 0.748, 0.792, 0.836, 0.880, 1.000])
      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.088, 0.176, 0.264, 0.352, 0.440, 0.528, 0.616, 0.704, 0.792, 0.836, 0.880, 1.000])
      #"VH_SR_high_Zmm"
      #Luca cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.149, 0.224, 0.298, 0.373, 0.447, 0.522, 0.596, 0.671, 0.745, 0.783, 0.820, 1.000])
      cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.149, 0.224, 0.298, 0.373, 0.447, 0.522, 0.596, 0.671, 0.745, 0.820, 1.000])
      #"VH_SR_low_Zee"
#      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.750, 0.788, 0.825, 0.863, 1.000])
      #"VH_SR_low_Zmm"
      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.068, 0.137, 0.205, 0.273, 0.342, 0.410, 0.478, 0.547, 0.615, 0.683, 0.718, 0.752, 0.786, 0.820, 1.000])
    else:
      print("Rebinning signal regions of 2016 VZ analyis")
      #"VZ_SR_Znn"
      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.063, 0.127, 0.190, 0.253, 0.317, 0.380, 0.443, 0.507, 0.570, 0.633, 0.665, 0.697, 0.728, 0.760, 1.000])
#      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.127, 0.190, 0.253, 0.317, 0.380, 0.443, 0.507, 0.570, 0.633, 0.665, 0.697, 0.728, 0.760, 1.000])
      #"VZ_SR_low_Zee"
      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.084, 0.167, 0.251, 0.335, 0.418, 0.502, 0.585, 0.669, 0.711, 0.753, 0.795, 0.836, 0.878, 0.920, 1.000])
      #"VZ_SR_low_Zmm"
      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
#Luca       #"VZ_SR_high_Zee"
#Luca       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.131, 0.263, 0.394, 0.526, 0.657, 0.723, 0.789, 0.8545, 0.920, 0.960, 1.000 ])
#Luca       #"VZ_SR_high_Zmm"
#Luca       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.084, 0.167, 0.251, 0.335, 0.418, 0.502, 0.585, 0.669, 0.753, 0.836, 0.920, 1.000])
#Luca       #"VZ_SR_Wenu"
#Luca       cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.105, 0.210, 0.315, 0.420, 0.525, 0.630, 0.735, 0.840, 0.920, 0.960, 1.000])
#Luca #      #"VZ_SR_Wmunu"
#Luca       cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.123, 0.246, 0.369, 0.491, 0.614, 0.737, 0.860, 0.930, 0.965, 1.000])
#
#
#      #"VZ_SR_Znn"
#      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.063, 0.127, 0.190, 0.253, 0.317, 0.380, 0.443, 0.507, 0.570, 0.633, 0.665, 0.697, 0.728, 0.760, 1.000])
#      #"VZ_SR_low_Zee"
 
#Luca   if year=='2017':
#Luca     if not args.doVV:
#Luca       print("Rebinning signal regions of 2017 VH analyis")
#Luca       #'VH_SR_Wenu'
#Luca #      cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#Luca       cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
#Luca       #'VH_SR_Wmunu'                                       
#Luca #      cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#Luca       cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
#Luca       #"VH_SR_Znn"
#Luca #      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.078, 0.157, 0.235, 0.313, 0.391, 0.470, 0.548, 0.626, 0.704, 0.743, 0.783, 0.822, 0.861, 0.900, 1.000])
#Luca       cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.078, 0.157, 0.235, 0.313, 0.391, 0.470, 0.548, 0.626, 0.704, 0.743, 0.783, 0.822, 1.000])
#Luca  #     cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.157, 0.235, 0.313, 0.391, 0.470, 0.548, 0.626, 0.704, 0.743, 0.783, 0.822, 1.000])
#Luca       #cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.400, 0.470, 0.548, 0.626, 0.704, 0.743, 0.783, 0.822, 0.861, 0.900, 1.000])
#Luca       #"VH_SR_high_Zee"
#Luca #      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#Luca       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.750, 0.788, 0.825, 0.863, 1.000])
#Luca       #"VH_SR_high_Zmm"
#Luca       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.072, 0.143, 0.215, 0.287, 0.358, 0.430, 0.502, 0.573, 0.645, 0.717, 0.753, 0.788, 0.824, 0.860, 1.000])
#Luca       #"VH_SR_low_Zee"
#Luca       cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.095, 0.189, 0.284, 0.379, 0.474, 0.521, 0.568, 0.616, 0.663, 0.711, 0.758, 0.805, 0.853, 0.900, 1.000])
#Luca       #"VH_SR_low_Zmm"
#Luca       cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.147, 0.220, 0.293, 0.367, 0.440, 0.513, 0.587, 0.660, 0.697, 0.733, 0.770, 0.807, 0.843, 0.880, 1.000])
#Luca     else:
#Luca       print("Rebinning signal regions of 2017 VZ analyis")
#Luca       #'VZ_SR_Wenu'
#Luca       cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.106, 0.212, 0.265, 0.318, 0.371, 0.424, 0.476, 0.529, 0.582, 0.635, 0.688, 0.741, 0.794, 0.847, 0.900, 1.000])
#Luca       #'VZ_SR_Wmunu'                                       
#Luca  #     cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.088, 0.175, 0.263, 0.350, 0.438, 0.526, 0.570, 0.613, 0.657, 0.701, 0.745, 0.789, 0.832, 0.876, 0.920, 1.000])
#Luca       cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.088, 0.175, 0.263, 0.350, 0.438, 0.526, 0.570, 0.613, 0.657, 0.701, 0.745, 0.789, 0.832, 0.876, 1.000])
#Luca       #"VZ_SR_Znn"
#Luca #      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.070, 0.140, 0.210, 0.280, 0.350, 0.420, 0.490, 0.560, 0.630, 0.700, 0.735, 0.770, 0.805, 0.840, 1.000])
#Luca       cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.070, 0.140, 0.210, 0.280, 0.350, 0.420, 0.490, 0.560, 0.630, 0.700, 0.735, 1.000])
#Luca #      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.140, 0.210, 0.280, 0.350, 0.420, 0.490, 0.560, 0.630, 0.700, 0.735, 1.000])
#Luca       #"VZ_SR_high_Zee"
#Luca       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.092, 0.184, 0.276, 0.368, 0.460, 0.552, 0.644, 0.690, 0.736, 0.782, 0.828, 0.874, 0.920, 1.000])
#Luca       #"VZ_SR_high_Zmm"
#Luca #      cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.096, 0.191, 0.287, 0.382, 0.478, 0.573, 0.621, 0.669, 0.717, 0.764, 0.812, 0.860, 1.000])
#Luca       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.096, 0.191, 0.287, 0.382, 0.478, 0.573, 0.621, 0.669, 0.717, 0.764, 0.812, 1.000])
#Luca       #"VZ_SR_low_Zee"
#Luca       cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.067, 0.133, 0.200, 0.267, 0.333, 0.400, 0.467, 0.533, 0.600, 0.667, 0.700, 0.733, 0.767, 0.800, 1.000])
#Luca       #"VZ_SR_low_Zmm"
#Luca       cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.068, 0.137, 0.205, 0.273, 0.342, 0.410, 0.478, 0.547, 0.615, 0.683, 0.718, 0.752, 0.786, 0.820, 1.000])
      
 
  if year=='2018':
    if not args.doVV:
      print("Rebinning signal regions of 2018 VH analyis")
      #'VH_SR_Wenu'
      #      cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.088, 0.175, 0.263, 0.350, 0.438, 0.526, 0.570, 0.613, 0.657, 0.701, 0.745, 0.789, 0.832, 0.876, 0.920, 1.000])
      cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.088, 0.175, 0.263, 0.350, 0.438, 0.526, 0.570, 0.613, 0.657, 0.701, 0.745, 0.789, 0.832, 0.876, 1.000])
      #'VH_SR_Wmunu'                                       
      #      cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.084, 0.167, 0.251, 0.335, 0.418, 0.502, 0.585, 0.627, 0.669, 0.711, 0.753, 0.795, 0.836, 0.878, 0.920, 1.000])
      cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.084, 0.167, 0.251, 0.335, 0.418, 0.502, 0.585, 0.627, 0.669, 0.711, 0.753, 0.795, 0.836, 0.878, 1.000])
      #"VH_SR_Znn"
      #cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.750, 0.788, 0.825, 1.000])
      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.750, 0.788, 0.825, 1.000])        
      #cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.750, 0.825, 0.900, 1.000])
      #"VH_SR_high_Zee"
      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.072, 0.143, 0.215, 0.287, 0.358, 0.430, 0.502, 0.573, 0.645, 0.717, 0.788, 0.824, 0.860, 1.000])
      #"VH_SR_high_Zmm"
      cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.073, 0.147, 0.220, 0.293, 0.367, 0.440, 0.513, 0.587, 0.660, 0.733, 0.807, 0.843, 0.880, 1.000])
      #"VH_SR_low_Zee"
      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.072, 0.143, 0.215, 0.287, 0.358, 0.430, 0.502, 0.573, 0.645, 0.717, 0.788, 0.824, 0.860, 1.000])
      #"VH_SR_low_Zmm"
      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.077, 0.153, 0.230, 0.306, 0.383, 0.459, 0.536, 0.612, 0.689, 0.765, 0.803, 0.842, 0.880, 1.000])

 
    else:
      print("Rebinning signal regions of 2018 VZ analyis baseline with optimization carried out on inclusive shapes")
#      #"VZ_SR_Wenu"
#      #cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.117, 0.234, 0.351, 0.469, 0.586, 0.703, 0.820, 1.000])
#      #"VZ_SR_Wmunu"
#      #cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.096, 0.191, 0.287, 0.382, 0.478, 0.573, 0.669, 0.764, 0.860, 1.000])
#      #"VZ_SR_Znn"
#      #cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.039, 0.078, 0.117, 0.156, 0.195, 0.234, 0.273, 0.312, 0.351, 0.390, 0.429, 0.468, 0.507, 0.546, 0.585, 0.624, 0.663, 0.702, 0.741, 0.780, 1.000])
#      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.078, 0.156, 0.234, 0.312, 0.390, 0.468, 0.507, 0.585, 0.663, 0.741, 1.000])
#      #cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.039, 0.078, 0.117, 0.156, 0.195, 0.234, 0.273, 0.312, 0.351, 0.390, 0.429, 0.468, 0.507, 0.585, 0.663, 0.741, 1.000])                                                           
#      #"VZ_SR_high_Zee"
#      #cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])   
#      #cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.075,  0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])   
#      #cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])   
#      #"VZ_SR_high_Zmm"
#      #cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([  0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#      cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.863, 1.000])
#      #cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.863, 1.000])
#      #cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.863, 1.000])
#      #"VZ_SR_low_Zee"
#      #cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
#      #cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#      #"VZ_SR_low_Zmm"
#      #cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.038, 0.077, 0.115, 0.153, 0.192, 0.230, 0.268, 0.307, 0.345, 0.383, 0.422, 0.460, 0.498, 0.537, 0.575, 0.613, 0.652, 0.690, 0.728, 0.767, 0.805, 0.843, 0.882, 0.920, 1.000])
#      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.115, 0.153, 0.192, 0.230, 0.268, 0.307, 0.345, 0.383, 0.422, 0.460, 0.498, 0.537, 0.575, 0.613, 0.652, 0.690, 0.728, 0.767, 0.805, 0.843, 0.882, 1.000])
#      #cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.153, 0.230, 0.307, 0.383, 0.460, 0.537, 0.613, 0.652, 0.690, 0.728, 0.767, 0.805, 0.843, 0.882, 1.000])
      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.115, 0.153, 0.192, 0.230, 0.268, 0.307, 0.345, 0.383, 0.422, 0.460, 0.498, 0.537, 0.575, 0.613, 0.652, 0.690, 0.728, 0.767, 0.805, 0.843, 0.882, 0.920, 1.000])



if args.rebinning_scheme == 'LFTT1b_vFinalAK15Pt300': # rebinning for H-analysis
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([3,4]).VariableRebin(binning)
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([3]).VariableRebin(binning)
  
  print 'binning in TT CRs: [0., 1.0] for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([7,8]).VariableRebin([0., 1.0])
  print 'binning in TT CRs: [0., 1.0] for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([7]).VariableRebin([0., 1.0])

#  if year=='2017':
#    print 'binning in HF CRs: [0., 0.6, 0.666666666666, 0.7333333333333, 0.8, 0.866666666666, 0.933333333333, 1.0] for Znn channel'
#    cb.cp().channel(['Znn']).bin_id([5]).VariableRebin([0., 0.6, 0.666666666666, 0.7333333333333, 0.8, 0.866666666666, 0.933333333333, 1.0])

#    print 'binning in HF CRs: [0., 1.0] for Znn channel'
#    cb.cp().channel(['Znn']).bin_id([5]).VariableRebin([0., 1.0])

   
  #============= 2016 ANALYSIS
  if year=='2016':
    if not args.doVV:
      print("Keep same bins as VHcc_binsDict.py in VH 2016 SRs")
#      cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.036, 0.072, 0.108, 0.143, 0.179, 0.215, 0.251, 0.287, 0.323, 0.358, 0.394, 0.430, 0.466, 0.502, 0.537, 0.573, 0.609, 0.645, 0.681, 0.717, 0.753, 0.788, 0.824, 0.860, 1.000 ])
      cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.036, 0.072, 0.108, 0.143, 0.179, 0.215, 0.251, 0.287, 0.323, 0.358, 0.394, 0.430, 0.466, 0.502, 0.537, 0.573, 0.609, 0.645, 0.681, 0.717, 0.753, 0.788, 0.824, 1.000 ])
#      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.054, 0.108, 0.162, 0.216, 0.271, 0.325, 0.379, 0.433, 0.487, 0.541, 0.595, 0.649, 0.704, 0.758, 0.812, 0.866, 0.920, 1.000 ])
      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.054, 0.108, 0.162, 0.216, 0.271, 0.325, 0.379, 0.433, 0.487, 0.541, 0.595, 0.649, 0.704, 0.758, 0.866, 1.000 ])
    else:
      print("Rebinning 2L Low-Vpt in VZ 2016 SRs")
#      #"VZ_SR_low_Zee"
#      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.084, 0.167, 0.251, 0.335, 0.418, 0.502, 0.585, 0.669, 0.711, 0.753, 0.795, 0.836, 0.878, 0.920, 1.000])
      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.108, 0.143, 0.179, 0.215, 0.251, 0.287, 0.323, 0.358, 0.394, 0.430, 0.466, 0.502, 0.537, 0.573, 0.609, 0.645, 0.681, 0.717, 0.753, 0.788, 0.824, 0.860, 1.000])
#      #"VZ_SR_low_Zmm"
#      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.075, 0.150, 0.225, 0.300, 0.375, 0.450, 0.525, 0.600, 0.675, 0.750, 0.788, 0.825, 0.863, 1.000])
      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.098, 0.130, 0.163, 0.195, 0.228, 0.260, 0.292, 0.325, 0.358, 0.390, 0.422, 0.455, 0.488, 0.520, 0.552, 0.585, 0.618, 0.650, 0.682, 0.715, 0.748, 0.780, 1.000])
##      #"VZ_SR_high_Zmm"
##      cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.076, 0.114, 0.152, 0.190, 0.229, 0.267, 0.305, 0.343, 0.381, 0.419, 0.457, 0.495, 0.533, 0.571, 0.610, 0.648, 0.686, 0.724, 0.762, 0.800, 1.000])
#      cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.076, 0.114, 0.152, 0.190, 0.229, 0.267, 0.305, 0.343, 0.381, 0.419, 0.457, 0.495, 0.533, 0.571, 0.610, 0.648, 0.686, 0.724, 0.762, 1.000])


  if year=='2017':
    if not args.doVV:
      print("Keep same bins as VHcc_binsDict.py in VH 2017 SRs")
#      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.035, 0.071, 0.106, 0.142, 0.177, 0.213, 0.248, 0.284, 0.319, 0.355, 0.390, 0.425, 0.461, 0.496, 0.532, 0.567, 0.603, 0.638, 0.674, 0.709, 0.745, 0.780, 1.000])

    else:
      print("Rebinning 2L Low-Vpt in VZ 2017 SRs")
      #"VZ_SR_low_Zee"
      #cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.035, 0.070, 0.105, 0.140, 0.175, 0.210, 0.245, 0.280, 0.315, 0.350, 0.385, 0.420, 0.455, 0.490, 0.525, 0.560, 0.595, 0.630, 0.665, 0.700, 0.735, 0.770, 0.805, 0.840, 1.000])
      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.105, 0.140, 0.175, 0.210, 0.245, 0.280, 0.315, 0.350, 0.385, 0.420, 0.455, 0.490, 0.525, 0.560, 0.595, 0.630, 0.665, 0.700, 0.735, 0.770, 0.805, 0.840, 1.000])
      #"VZ_SR_low_Zmm"
      #cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.033, 0.065, 0.098, 0.130, 0.163, 0.195, 0.228, 0.260, 0.292, 0.325, 0.358, 0.390, 0.422, 0.455, 0.488, 0.520, 0.552, 0.585, 0.618, 0.650, 0.682, 0.715, 0.748, 0.780, 1.000])
      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.098, 0.130, 0.163, 0.195, 0.228, 0.260, 0.292, 0.325, 0.358, 0.390, 0.422, 0.455, 0.488, 0.520, 0.552, 0.585, 0.618, 0.650, 0.682, 0.715, 0.748, 0.780, 1.000])
      #"VZ_SR_high_Zmm"
      #cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.036, 0.071, 0.107, 0.143, 0.178, 0.214, 0.250, 0.285, 0.321, 0.357, 0.392, 0.428, 0.463, 0.499, 0.535, 0.570, 0.606, 0.642, 0.677, 0.713, 0.749, 0.784, 0.820, 1.000])
      cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.036, 0.071, 0.107, 0.143, 0.178, 0.214, 0.250, 0.285, 0.321, 0.357, 0.392, 0.428, 0.463, 0.499, 0.535, 0.570, 0.606, 0.642, 0.677, 0.713, 0.749, 1.000])
      #"VZ_SR_high_Zmm"
      #cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.032, 0.063, 0.095, 0.127, 0.158, 0.190, 0.222, 0.253, 0.285, 0.317, 0.348, 0.380, 0.412, 0.443, 0.475, 0.507, 0.538, 0.570, 0.602, 0.633, 0.665, 0.697, 0.728, 0.760, 1.000])
      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.032, 0.063, 0.095, 0.127, 0.158, 0.190, 0.222, 0.253, 0.285, 0.317, 0.348, 0.380, 0.412, 0.443, 0.475, 0.507, 0.538, 0.570, 0.602, 0.633, 0.665, 0.697, 0.728, 1.000])
      #"VZ_SR_Wen"
      #cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.033, 0.067, 0.100, 0.133, 0.167, 0.200, 0.233, 0.267, 0.300, 0.333, 0.367, 0.400, 0.433, 0.467, 0.500, 0.533, 0.567, 0.600, 0.633, 0.667, 0.700, 0.733, 0.767, 0.800, 1.000])
      cb.cp().channel(['Wen']).bin_id([1]).VariableRebin([ 0.000, 0.033, 0.067, 0.100, 0.133, 0.167, 0.200, 0.233, 0.267, 0.300, 0.333, 0.367, 0.400, 0.433, 0.467, 0.500, 0.533, 0.567, 0.600, 0.633, 0.667, 0.700, 0.733, 0.767, 1.000])
      #"VZ_SR_Wnn"
      #cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.032, 0.063, 0.095, 0.127, 0.158, 0.190, 0.222, 0.253, 0.285, 0.317, 0.348, 0.380, 0.412, 0.443, 0.475, 0.507, 0.538, 0.570, 0.602, 0.633, 0.665, 0.697, 0.728, 0.760, 1.000])
      cb.cp().channel(['Wmn']).bin_id([1]).VariableRebin([ 0.000, 0.032, 0.063, 0.095, 0.127, 0.158, 0.190, 0.222, 0.253, 0.285, 0.317, 0.348, 0.380, 0.412, 0.443, 0.475, 0.507, 0.538, 0.570, 0.602, 0.633, 0.665, 0.697, 0.728, 1.000 ])
      #"VZ_SR_Znn"
      #cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.034, 0.068, 0.103, 0.137, 0.171, 0.205, 0.239, 0.273, 0.308, 0.342, 0.376, 0.410, 0.444, 0.478, 0.513, 0.547, 0.581, 0.615, 0.649, 0.683, 0.718, 0.752, 0.786, 0.820, 1.000])
      #cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.034, 0.068, 0.103, 0.137, 0.171, 0.205, 0.239, 0.273, 0.308, 0.342, 0.376, 0.410, 0.444, 0.478, 0.513, 0.547, 0.581, 0.615, 0.649, 0.683, 0.718, 0.752, 0.786, 1.000])


  if year=='2018':
     if not args.doVV:
       print("Merge 2nd-last and 3rd-last bin in 2L High-Vpt in VH 2018 SRs to mitigate stat. fluctuations")
 #      #"VH_SR_high_Zee"
 #      cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.037, 0.073, 0.110, 0.147, 0.183, 0.220, 0.257, 0.293, 0.330, 0.367, 0.403, 0.440, 0.477, 0.513, 0.550, 0.587, 0.623, 0.660, 0.697, 0.733, 0.770, 0.807, 0.843, 0.880, 1.000])
       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.037, 0.073, 0.110, 0.147, 0.183, 0.220, 0.257, 0.293, 0.330, 0.367, 0.403, 0.440, 0.477, 0.513, 0.550, 0.587, 0.623, 0.660, 0.697, 0.733, 0.770, 0.807, 0.880, 1.000])
 #      #"VH_SR_high_Zmm"
 #      cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.037, 0.073, 0.110, 0.147, 0.183, 0.220, 0.257, 0.293, 0.330, 0.367, 0.403, 0.440, 0.477, 0.513, 0.550, 0.587, 0.623, 0.660, 0.697, 0.733, 0.770, 0.807, 0.843, 0.880, 1.000])
       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.037, 0.073, 0.110, 0.147, 0.183, 0.220, 0.257, 0.293, 0.330, 0.367, 0.403, 0.440, 0.477, 0.513, 0.550, 0.587, 0.623, 0.660, 0.697, 0.733, 0.770, 0.807, 0.880, 1.000])

     else:
       print("Rebinning signal regions of 2018 VZ analyis with vFinal")
       print("Rebinning SRs of 2018 VZ analyis with optimization carried out on inclusive shapes")
       #"VZ_SR_low_Zee"
       cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#       cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
       #"VZ_SR_low_Zmm"
       cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.115, 0.153, 0.192, 0.230, 0.268, 0.307, 0.345, 0.383, 0.422, 0.460, 0.498, 0.537, 0.575, 0.613, 0.652, 0.690, 0.728, 0.767, 0.805, 0.843, 0.882, 0.920, 1.000])
#       cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.115, 0.153, 0.192, 0.230, 0.268, 0.307, 0.345, 0.383, 0.422, 0.460, 0.498, 0.537, 0.575, 0.613, 0.652, 0.690, 0.728, 0.767, 0.805, 0.843, 0.882, 1.000])
       #"VZ_SR_high_Zee"
##       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
#       #"VZ_SR_high_Zmm"
##       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
#       #"VZ_SR_Znn"
#       cb.cp().channel(['Znn']).bin_id([2]).VariableRebin([ 0.000, 0.078, 0.156, 0.234, 0.390,  0.546,  0.780, 1.000])


if args.rebinning_scheme == 'LFTT1b_vFinalIncl': # rebinning for H-analysis
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([3,4]).VariableRebin(binning)
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([3]).VariableRebin(binning)

  print 'binning in TT CRs: [0., 1.0] for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([7,8]).VariableRebin([0., 1.0])
  print 'binning in TT CRs: [0., 1.0] for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([7]).VariableRebin([0., 1.0])

  if year=='2016':
     if not args.doVV:
       print("ok")
     else:
 #      #"VZ_SR_low_Zee"
 #      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.042, 0.084, 0.125, 0.167, 0.209, 0.251, 0.293, 0.335, 0.376, 0.418, 0.460, 0.502, 0.544, 0.585, 0.627, 0.669, 0.711, 0.753, 0.795, 0.836, 0.878, 0.920, 1.000 ])
       cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.125, 0.167, 0.209, 0.251, 0.293, 0.335, 0.376, 0.418, 0.460, 0.502, 0.544, 0.585, 0.627, 0.669, 0.711, 0.753, 0.795, 0.836, 0.878, 1.000 ])
 #      #"VZ_SR_low_Zmm"
 #      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000 ])
       cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000 ])

  if year=='2017':
     if not args.doVV:
       print("ok")
     else:
 #      #"VZ_SR_low_Zee"
 #      cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.000, 0.033, 0.067, 0.100, 0.133, 0.167, 0.200, 0.233, 0.267, 0.300, 0.333, 0.367, 0.400, 0.433, 0.467, 0.500, 0.533, 0.567, 0.600, 0.633, 0.667, 0.700, 0.733, 0.767, 0.800, 1.000 ])
       cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.100, 0.133, 0.167, 0.200, 0.233, 0.267, 0.300, 0.333, 0.367, 0.400, 0.433, 0.467, 0.500, 0.533, 0.567, 0.600, 0.633, 0.667, 0.700, 0.733, 0.767, 0.800, 1.000 ])
 #      #"VZ_SR_low_Zmm"
 #      cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.000, 0.034, 0.068, 0.103, 0.137, 0.171, 0.205, 0.239, 0.273, 0.308, 0.342, 0.376, 0.410, 0.444, 0.478, 0.513, 0.547, 0.581, 0.615, 0.649, 0.683, 0.718, 0.752, 0.786, 0.820, 1.000 ])
       cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.103, 0.137, 0.171, 0.205, 0.239, 0.273, 0.308, 0.342, 0.376, 0.410, 0.444, 0.478, 0.513, 0.547, 0.581, 0.615, 0.649, 0.683, 0.718, 0.752, 0.786, 0.820, 1.000 ])
 #      #"VZ_SR_low_Znn"
 #      cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.035, 0.070, 0.105, 0.140, 0.175, 0.210, 0.245, 0.280, 0.315, 0.350, 0.385, 0.420, 0.455, 0.490, 0.525, 0.560, 0.595, 0.630, 0.665, 0.700, 0.735, 0.770, 0.805, 0.840, 1.000 ])
       cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.035, 0.070, 0.105, 0.140, 0.175, 0.210, 0.245, 0.280, 0.315, 0.350, 0.385, 0.420, 0.455, 0.490, 0.525, 0.560, 0.595, 0.630, 0.665, 0.700, 0.735, 0.770, 0.805, 1.000 ])

  if year=='2018':
     if not args.doVV:
       #"VH_SR_high_Zee"
#       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.036, 0.072, 0.108, 0.143, 0.179, 0.215, 0.251, 0.287, 0.323, 0.358, 0.394, 0.430, 0.466, 0.502, 0.537, 0.573, 0.609, 0.645, 0.681, 0.717, 0.753, 0.788, 0.824, 0.860, 1.000 ])
       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.036, 0.072, 0.108, 0.143, 0.179, 0.215, 0.251, 0.287, 0.323, 0.358, 0.394, 0.430, 0.466, 0.502, 0.537, 0.573, 0.609, 0.645, 0.681, 0.717, 0.753, 0.788, 0.824, 1.000 ])
       #"VH_SR_high_Zmm"
#       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.037, 0.073, 0.110, 0.147, 0.183, 0.220, 0.257, 0.293, 0.330, 0.367, 0.403, 0.440, 0.477, 0.513, 0.550, 0.587, 0.623, 0.660, 0.697, 0.733, 0.770, 0.807, 0.843, 0.880, 1.000 ])
       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.037, 0.073, 0.110, 0.147, 0.183, 0.220, 0.257, 0.293, 0.330, 0.367, 0.403, 0.440, 0.477, 0.513, 0.550, 0.587, 0.623, 0.660, 0.697, 0.733, 0.770, 0.807, 0.843, 1.000 ])
       #"VH_SR_Znn"
#       cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000 ])
       cb.cp().channel(['Znn']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000 ])

     else:
       #"VZ_SR_low_Zee"
       cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
#       cb.cp().channel(['Zee']).bin_id([2]).VariableRebin([ 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
       #"VZ_SR_low_Zmm"
       cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.115, 0.153, 0.192, 0.230, 0.268, 0.307, 0.345, 0.383, 0.422, 0.460, 0.498, 0.537, 0.575, 0.613, 0.652, 0.690, 0.728, 0.767, 0.805, 0.843, 0.882, 0.920, 1.000])
#       cb.cp().channel(['Zmm']).bin_id([2]).VariableRebin([ 0.115, 0.153, 0.192, 0.230, 0.268, 0.307, 0.345, 0.383, 0.422, 0.460, 0.498, 0.537, 0.575, 0.613, 0.652, 0.690, 0.728, 0.767, 0.805, 0.843, 0.882, 1.000])
       #"VZ_SR_high_Zee"
#       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
       cb.cp().channel(['Zee']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])
#       #"VZ_SR_high_Zmm"
#       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 0.900, 1.000])
       cb.cp().channel(['Zmm']).bin_id([1]).VariableRebin([ 0.000, 0.038, 0.075, 0.113, 0.150, 0.188, 0.225, 0.263, 0.300, 0.338, 0.375, 0.413, 0.450, 0.488, 0.525, 0.563, 0.600, 0.638, 0.675, 0.713, 0.750, 0.788, 0.825, 0.863, 1.000])


if args.rebinning_scheme == 'All1b': # rebinning for H-analysis
  binning=np.linspace(0.0,1.0,num=2)
  print 'binning in SRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([1,2]).VariableRebin(binning)
  binning=np.linspace(0.0,1.0,num=2)
  print 'binning in SRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([1]).VariableRebin(binning)
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([3,4]).VariableRebin(binning)
  binning=np.linspace(0.0,0.4,num=2)
  print 'binning in LF CRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([3]).VariableRebin(binning)
  binning=np.linspace(0.0,1.0,num=2)
  print 'binning in HF,CC,TT CRs:',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([5,6,7,8,9,10]).VariableRebin(binning)
  binning=np.linspace(0.0,1.0,num=2)
  print 'binning in HF,CC,TT CRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([5,7,9]).VariableRebin(binning)


nBinSR = args.nBinSR
print("===> Rebinning the SR with number of bins = ",nBinSR)
if args.rebinning_scheme == 'SR_nb': # rebinning for H-analysis
  binning=np.linspace(0.0,1.0,int(nBinSR))
  print 'binning in SRs:',binning,'for Zll channels'
  #cb.cp().channel(['Zee']).bin_id([1,2]).VariableRebin([0., 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
  cb.cp().channel(['Zee','Zmm']).bin_id([1,2]).VariableRebin(binning)
  binning=np.linspace(0.0,1.0,int(nBinSR))
  print 'binning in SRs:',binning,'for Wln,Znn channels'
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([1]).VariableRebin(binning)

edge = args.edge
if args.rebinning_scheme == 'SR_Scan': # rebinning for H-analysis
  cb.cp().channel(['Zee']).bin_id([1,2]).VariableRebin([0., float(edge), 1.0])
  cb.cp().channel(['Wen','Wmn','Znn']).bin_id([1]).VariableRebin([0., float(edge), 1.0])

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
#luca
#cb.ForEachProc(lambda x: cb.FilterSysts(lambda y: drop_noRealShape_systs(x,y) if matching_proc(x,y) else None))
#cb.ForEachProc(lambda x: cb.FilterSysts(lambda y: drop_ShapeSameDir_systs(x,y) if matching_proc(x,y) else None))
#cb.ForEachProc(lambda x: cb.FilterSysts(lambda y: drop_SameUpDownShapes_systs(x,y) if matching_proc(x,y) else None))


#AUTHORIZED PERSON ONLY!! Drop QCD in Z+HF CR
#Luca cb.FilterProcs(lambda x: drop_znnqcd(cb,x))

#Luca if args.doVV:
#cb.FilterSysts(lambda x: x.name()=="CMS_vhcc_VZcc")
    

### decrease bin statistical errors
#Luca cb.cp().channel(['Zee','Zmm']).process(['Zj_bbc','Zj_blc','Zj_ll']).ForEachProc(lambda x: decrease_bin_errors(x))

cb.cp().RenameSystematic(cb,'CMS_scale_j_Absolute','CMS_scale_j_Absolute_13TeV')
cb.cp().RenameSystematic(cb,'CMS_scale_j_BBEC1','CMS_scale_j_BBEC1_13TeV')
cb.cp().RenameSystematic(cb,'CMS_scale_j_EC2','CMS_scale_j_EC2_13TeV')
cb.cp().RenameSystematic(cb,'CMS_scale_j_FlavorQCD','CMS_scale_j_FlavorQCD_13TeV')
cb.cp().RenameSystematic(cb,'CMS_scale_j_HF','CMS_scale_j_HF_13TeV')
cb.cp().RenameSystematic(cb,'CMS_scale_j_RelativeBal','CMS_scale_j_RelativeBal_13TeV')

if year=='2016':
  cb.cp().RenameSystematic(cb,'CMS_j_PtCReg_Scale','CMS_j_PtCReg_Scale_2016')
  cb.cp().RenameSystematic(cb,'CMS_j_PtCReg_Smear','CMS_j_PtCReg_Smear_2016')

#  cb.cp().RenameSystematic(cb,'CMS_vhcc_puBackupWeight_2016','CMS_vhcc_puWeight_2016')
  cb.cp().RenameSystematic(cb,'CMS_PrefireWeight','CMS_PrefireWeight_13TeV_2016')
  cb.cp().RenameSystematic(cb,'CMS_PUIDWeight_13TeV_2016','CMS_vhcc_puJetId_2016')
  cb.cp().channel(['Wen','Wmn','Znn']).RenameSystematic(cb,'CMS_METUnclustEn','CMS_res_met_13TeV_2016')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_JES','CMS_cTagWeight_JES_2016')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_JER','CMS_cTagWeight_JER_2016')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_JEC','CMS_cTagWeight_JEC_2016')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_PU','CMS_cTagWeight_PU_2016')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_EleId','CMS_cTagWeight_EleId_2016')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_MuId','CMS_cTagWeight_MuId_2016')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_Absolute_2016','CMS_scale_j_Absolute_2016_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_BBEC1_2016','CMS_scale_j_BBEC1_2016_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_EC2_2016','CMS_scale_j_EC2_2016_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_HF_2016','CMS_scale_j_HF_2016_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_RelativeSample_2016','CMS_scale_j_RelativeSample_2016_13TeV')

#  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZJets_Low_13TeV_2016')
#  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZJets_High_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zc_Low_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zb_Low_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zl_Low_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zc_High_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zb_High_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zl_High_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).process(['TT']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_TT_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).process(['s_Top']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_s_Top_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).process(['VVother']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_VVother_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).process(['VZcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_VZcc_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).process(['ggZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ggZH_hbb_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).process(['ZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZH_hbb_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).process(['ggZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ggZH_hcc_13TeV_2016')
  cb.cp().channel(['Zee','Zmm']).process(['ZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZH_hcc_13TeV_2016')

#  cb.cp().channel(['Wen','Wmn']).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZJets_13TeV_2016')
#  cb.cp().channel(['Wen','Wmn']).process(['Wj_cj','Wj_bj','Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_WJets_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).bin_id([1,3,5,7,9]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zc_High_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).bin_id([1,3,5,7,9]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zb_High_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).bin_id([1,3,5,7,9]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zl_High_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['Wj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Wc_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['Wj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Wb_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Wl_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['TT']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_TT_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['s_Top']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_s_Top_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['VVother']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_VVother_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['VZcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_VZcc_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['WH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_WH_hbb_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['ZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZH_hbb_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['WH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_WH_hcc_13TeV_2016')
  cb.cp().channel(['Wen','Wmn']).process(['ZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZH_hcc_13TeV_2016')

#  cb.cp().channel(['Znn']).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZJets_13TeV_2016')
#  cb.cp().channel(['Znn']).process(['Wj_cj','Wj_bj','Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_WJets_13TeV_2016')
  cb.cp().channel(['Znn']).bin_id([1,3,5,7,9]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zc_High_13TeV_2016')
  cb.cp().channel(['Znn']).bin_id([1,3,5,7,9]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zb_High_13TeV_2016')
  cb.cp().channel(['Znn']).bin_id([1,3,5,7,9]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Zl_High_13TeV_2016')
  cb.cp().channel(['Znn']).process(['Wj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Wc_13TeV_2016')
  cb.cp().channel(['Znn']).process(['Wj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Wb_13TeV_2016')
  cb.cp().channel(['Znn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_Wl_13TeV_2016')
  cb.cp().channel(['Znn']).process(['TT']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_TT_13TeV_2016')
  cb.cp().channel(['Znn']).process(['s_Top']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_s_Top_13TeV_2016')
  cb.cp().channel(['Znn']).process(['VVother']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_VVother_13TeV_2016')
  cb.cp().channel(['Znn']).process(['VZcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_VZcc_13TeV_2016')
  cb.cp().channel(['Znn']).process(['WH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_WH_hbb_13TeV_2016')
  cb.cp().channel(['Znn']).process(['ZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZH_hbb_13TeV_2016')
  cb.cp().channel(['Znn']).process(['ggZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ggZH_hbb_13TeV_2016')
  cb.cp().channel(['Znn']).process(['WH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_WH_hcc_13TeV_2016')
  cb.cp().channel(['Znn']).process(['ZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ZH_hcc_13TeV_2016')
  cb.cp().channel(['Znn']).process(['ggZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2016','CMS_PostCTagWeight_ggZH_hcc_13TeV_2016')

  #rename of PDF systematics uncertainties to match conventions
  cb.cp().process(['ggZH_hbb','ggZH_hcc']).RenameSystematic(cb,'CMS_LHE_pdf_ggZH', 'CMS_LHE_weights_pdf_ggZH_2016') 
  cb.cp().process(['ZH_hbb','ZH_hcc']).RenameSystematic(cb,'CMS_LHE_pdf_ZH', 'CMS_LHE_weights_pdf_ZH_2016') 
  cb.cp().process(['WH_hbb','WH_hcc']).RenameSystematic(cb,'CMS_LHE_pdf_WH', 'CMS_LHE_weights_pdf_WH_2016') 
  cb.cp().process(['Zj_ll']).RenameSystematic(cb,'CMS_LHE_pdf_Zj_ll', 'CMS_LHE_weights_pdf_Zj_2016') 
  cb.cp().process(['Zj_bj']).RenameSystematic(cb,'CMS_LHE_pdf_Zj_bj', 'CMS_LHE_weights_pdf_Zj_2016') 
  cb.cp().process(['Zj_cj']).RenameSystematic(cb,'CMS_LHE_pdf_Zj_cj', 'CMS_LHE_weights_pdf_Zj_2016') 
  cb.cp().process(['Wj_ll']).RenameSystematic(cb,'CMS_LHE_pdf_Wj_ll', 'CMS_LHE_weights_pdf_Wj_2016') 
  cb.cp().process(['Wj_bj']).RenameSystematic(cb,'CMS_LHE_pdf_Wj_bj', 'CMS_LHE_weights_pdf_Wj_2016') 
  cb.cp().process(['Wj_cj']).RenameSystematic(cb,'CMS_LHE_pdf_Wj_cj', 'CMS_LHE_weights_pdf_Wj_2016') 
  cb.cp().process(['TT']).RenameSystematic(cb,'CMS_LHE_pdf_TT','CMS_LHE_weights_pdf_TT_2016')
  cb.cp().process(['s_Top']).RenameSystematic(cb,'CMS_LHE_pdf_ST','CMS_LHE_weights_pdf_ST_2016')
  cb.cp().process(['VVother']).RenameSystematic(cb,'CMS_LHE_pdf_VVother','CMS_LHE_weights_pdf_VV_2016')
  cb.cp().process(['VZcc']).RenameSystematic(cb,'CMS_LHE_pdf_VZcc','CMS_LHE_weights_pdf_VV_2016')
  
  #rename of Renormalization/Factorization scale systematics uncertainties to match conventions
  cb.cp().process(['ZH_hbb','ZH_hcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_ZH','CMS_LHE_weights_scale_muR_ZH_2016')
  cb.cp().process(['WH_hbb','WH_hcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_WH','CMS_LHE_weights_scale_muR_WH_2016')
  cb.cp().process(['ggZH_hbb','ggZH_hcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_ggZH','CMS_LHE_weights_scale_muR_ggZH_2016')
  cb.cp().process(['ZH_hbb','ZH_hcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_ZH','CMS_LHE_weights_scale_muF_ZH_2016')
  cb.cp().process(['WH_hbb','WH_hcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_WH','CMS_LHE_weights_scale_muF_WH_2016')
  cb.cp().process(['ggZH_hbb','ggZH_hcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_ggZH','CMS_LHE_weights_scale_muF_ggZH_2016')
  cb.cp().process(['TT']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_TT','CMS_LHE_weights_scale_muR_TT_2016')
  cb.cp().process(['TT']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_TT','CMS_LHE_weights_scale_muF_TT_2016')
  cb.cp().process(['s_Top']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_ST','CMS_LHE_weights_scale_muR_ST_2016')
  cb.cp().process(['s_Top']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_ST','CMS_LHE_weights_scale_muF_ST_2016')
  cb.cp().process(['VVother']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_VVother','CMS_LHE_weights_scale_muR_VV_2016')
  cb.cp().process(['VZcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_VZcc','CMS_LHE_weights_scale_muR_VV_2016')
  cb.cp().process(['VVother']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_VVother','CMS_LHE_weights_scale_muF_VV_2016')
  cb.cp().process(['VZcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_VZcc','CMS_LHE_weights_scale_muF_VV_2016')
  cb.cp().process(['Zj_ll']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Zj_ll', 'CMS_LHE_weights_scale_muR_Zj_2016') 
  cb.cp().process(['Zj_bj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Zj_bj', 'CMS_LHE_weights_scale_muR_Zj_2016') 
  cb.cp().process(['Zj_cj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Zj_cj', 'CMS_LHE_weights_scale_muR_Zj_2016') 
  cb.cp().process(['Wj_ll']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Wj_ll', 'CMS_LHE_weights_scale_muR_Wj_2016') 
  cb.cp().process(['Wj_bj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Wj_bj', 'CMS_LHE_weights_scale_muR_Wj_2016') 
  cb.cp().process(['Wj_cj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Wj_cj', 'CMS_LHE_weights_scale_muR_Wj_2016') 
  cb.cp().process(['Zj_ll']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Zj_ll', 'CMS_LHE_weights_scale_muF_Zj_2016') 
  cb.cp().process(['Zj_bj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Zj_bj', 'CMS_LHE_weights_scale_muF_Zj_2016') 
  cb.cp().process(['Zj_cj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Zj_cj', 'CMS_LHE_weights_scale_muF_Zj_2016') 
  cb.cp().process(['Wj_ll']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Wj_ll', 'CMS_LHE_weights_scale_muF_Wj_2016') 
  cb.cp().process(['Wj_bj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Wj_bj', 'CMS_LHE_weights_scale_muF_Wj_2016') 
  cb.cp().process(['Wj_cj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Wj_cj', 'CMS_LHE_weights_scale_muF_Wj_2016') 


  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2016','CMS_vhcc_dRjjReweight_fit_Zll_Zc_2016')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2016','CMS_vhcc_dRjjReweight_fit_Zll_Zc_Low_2016')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2016','CMS_vhcc_dRjjReweight_fit_Zll_Zc_High_2016')
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Wln_2016','CMS_vhcc_dRjjReweight_fit_Wln_Wc_2016')
  cb.cp().channel(['Znn']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Znn_2016','CMS_vhcc_dRjjReweight_fit_Znn_Zc_2016')

  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2016','CMS_vhcc_dRjjReweight_fit_Zll_Zb_2016')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2016','CMS_vhcc_dRjjReweight_fit_Zll_Zb_Low_2016')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2016','CMS_vhcc_dRjjReweight_fit_Zll_Zb_High_2016')
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Wln_2016','CMS_vhcc_dRjjReweight_fit_Wln_Wb_2016')
  cb.cp().channel(['Znn']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Znn_2016','CMS_vhcc_dRjjReweight_fit_Znn_Zb_2016')

  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2016','CMS_vhcc_dRjjReweight_fit_Zll_Zlight_2016')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2016','CMS_vhcc_dRjjReweight_fit_Zll_Zlight_Low_2016')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2016','CMS_vhcc_dRjjReweight_fit_Zll_Zlight_High_2016')
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Wln_2016','CMS_vhcc_dRjjReweight_fit_Wln_Wlight_2016')
  cb.cp().channel(['Znn']).process(['Zj_ll']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Znn_2016','CMS_vhcc_dRjjReweight_fit_Znn_Zlight_2016')

#  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2016','CMS_vhcc_dRjjReweight_Flavour_DYZj_cj_2016')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2016','CMS_vhcc_dRjjReweight_Flavour_DYZj_bj_2016')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2016','CMS_vhcc_dRjjReweight_Flavour_DYZj_cj_Low_2016')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2016','CMS_vhcc_dRjjReweight_Flavour_DYZj_bj_High_2016')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2016','CMS_vhcc_dRjjReweight_Flavour_DYZj_cj_Low_2016')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2016','CMS_vhcc_dRjjReweight_Flavour_DYZj_bj_High_2016')

  cb.cp().channel(['Znn']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2016','CMS_vhcc_dRjjReweight_Flavour_Znnj_cj_2016')
  cb.cp().channel(['Znn']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2016','CMS_vhcc_dRjjReweight_Flavour_Znnj_bj_2016')

  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_JEC_2016','CMS_cTagWeight_JEC_Low_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_JES_2016','CMS_cTagWeight_JES_Low_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_JER_2016','CMS_cTagWeight_JER_Low_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_PU_2016','CMS_cTagWeight_PU_Low_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_EleId_2016','CMS_cTagWeight_EleId_Low_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_MuId_2016','CMS_cTagWeight_MuId_Low_2016')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_muR','CMS_cTagWeight_muR_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_muF','CMS_cTagWeight_muF_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecDYJets','CMS_cTagWeight_XSecDYJets_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecST','CMS_cTagWeight_XSecST_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecWJets','CMS_cTagWeight_XSecWJets_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecTTbar','CMS_cTagWeight_XSecTTbar_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_Stat_2016','CMS_cTagWeight_Stat_2016_Low')


if year=='2017':
  cb.cp().RenameSystematic(cb,'CMS_j_PtCReg_Scale','CMS_j_PtCReg_Scale_2017')
  cb.cp().RenameSystematic(cb,'CMS_j_PtCReg_Smear','CMS_j_PtCReg_Smear_2017')

##  cb.cp().RenameSystematic(cb,'CMS_vhcc_puBackupWeight_2017','CMS_vhcc_puWeight_2017')
  cb.cp().RenameSystematic(cb,'CMS_PrefireWeight','CMS_PrefireWeight_13TeV_2017')
  cb.cp().RenameSystematic(cb,'CMS_PUIDWeight_13TeV_2017','CMS_vhcc_puJetId_2017')
  cb.cp().channel(['Wen','Wmn','Znn']).RenameSystematic(cb,'CMS_METUnclustEn','CMS_res_met_13TeV_2017')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_JEC','CMS_cTagWeight_JEC_2017')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_JES','CMS_cTagWeight_JES_2017')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_JER','CMS_cTagWeight_JER_2017')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_PU','CMS_cTagWeight_PU_2017')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_EleId','CMS_cTagWeight_EleId_2017')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_MuId','CMS_cTagWeight_MuId_2017')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_Absolute_2017','CMS_scale_j_Absolute_2017_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_BBEC1_2017','CMS_scale_j_BBEC1_2017_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_EC2_2017','CMS_scale_j_EC2_2017_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_HF_2017','CMS_scale_j_HF_2017_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_RelativeSample_2017','CMS_scale_j_RelativeSample_2017_13TeV')

#  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZJets_Low_13TeV_2017')
#  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZJets_High_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zc_Low_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zb_Low_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zl_Low_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zc_High_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zb_High_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zl_High_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).process(['TT']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_TT_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).process(['s_Top']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_s_Top_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).process(['VVother']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_VVother_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).process(['VZcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_VZcc_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).process(['ggZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ggZH_hbb_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).process(['ZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZH_hbb_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).process(['ggZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ggZH_hcc_13TeV_2017')
  cb.cp().channel(['Zee','Zmm']).process(['ZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZH_hcc_13TeV_2017')

#  cb.cp().channel(['Wen','Wmn']).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZJets_13TeV_2017')
#  cb.cp().channel(['Wen','Wmn']).process(['Wj_cj','Wj_bj','Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_WJets_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).bin_id([1,3,5,7,9]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zc_High_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).bin_id([1,3,5,7,9]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zb_High_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).bin_id([1,3,5,7,9]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zl_High_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['Wj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Wc_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['Wj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Wb_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Wl_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['TT']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_TT_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['s_Top']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_s_Top_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['VVother']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_VVother_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['VZcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_VZcc_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['WH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_WH_hbb_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['ZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZH_hbb_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['WH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_WH_hcc_13TeV_2017')
  cb.cp().channel(['Wen','Wmn']).process(['ZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZH_hcc_13TeV_2017')

#  cb.cp().channel(['Znn']).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZJets_13TeV_2017')
#  cb.cp().channel(['Znn']).process(['Wj_cj','Wj_bj','Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_WJets_13TeV_2017')
  cb.cp().channel(['Znn']).bin_id([1,3,5,7,9]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zc_High_13TeV_2017')
  cb.cp().channel(['Znn']).bin_id([1,3,5,7,9]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zb_High_13TeV_2017')
  cb.cp().channel(['Znn']).bin_id([1,3,5,7,9]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Zl_High_13TeV_2017')
  cb.cp().channel(['Znn']).process(['Wj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Wc_13TeV_2017')
  cb.cp().channel(['Znn']).process(['Wj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Wb_13TeV_2017')
  cb.cp().channel(['Znn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_Wl_13TeV_2017')
  cb.cp().channel(['Znn']).process(['TT']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_TT_13TeV_2017')
  cb.cp().channel(['Znn']).process(['s_Top']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_s_Top_13TeV_2017')
  cb.cp().channel(['Znn']).process(['VVother']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_VVother_13TeV_2017')
  cb.cp().channel(['Znn']).process(['VZcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_VZcc_13TeV_2017')
  cb.cp().channel(['Znn']).process(['WH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_WH_hbb_13TeV_2017')
  cb.cp().channel(['Znn']).process(['ZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZH_hbb_13TeV_2017')
  cb.cp().channel(['Znn']).process(['ggZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ggZH_hbb_13TeV_2017')
  cb.cp().channel(['Znn']).process(['WH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_WH_hcc_13TeV_2017')
  cb.cp().channel(['Znn']).process(['ZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ZH_hcc_13TeV_2017')
  cb.cp().channel(['Znn']).process(['ggZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2017','CMS_PostCTagWeight_ggZH_hcc_13TeV_2017')


  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2017','CMS_vhcc_dRjjReweight_fit_Zll_Zc_2017')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2017','CMS_vhcc_dRjjReweight_fit_Zll_Zc_Low_2017')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2017','CMS_vhcc_dRjjReweight_fit_Zll_Zc_High_2017')
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Wln_2017','CMS_vhcc_dRjjReweight_fit_Wln_Wc_2017')
  cb.cp().channel(['Znn']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Znn_2017','CMS_vhcc_dRjjReweight_fit_Znn_Zc_2017')

  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2017','CMS_vhcc_dRjjReweight_fit_Zll_Zb_2017')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2017','CMS_vhcc_dRjjReweight_fit_Zll_Zb_Low_2017')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2017','CMS_vhcc_dRjjReweight_fit_Zll_Zb_High_2017')
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Wln_2017','CMS_vhcc_dRjjReweight_fit_Wln_Wb_2017')
  cb.cp().channel(['Znn']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Znn_2017','CMS_vhcc_dRjjReweight_fit_Znn_Zb_2017')

  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2017','CMS_vhcc_dRjjReweight_fit_Zll_Zlight_2017')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2017','CMS_vhcc_dRjjReweight_fit_Zll_Zlight_Low_2017')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2017','CMS_vhcc_dRjjReweight_fit_Zll_Zlight_High_2017')
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Wln_2017','CMS_vhcc_dRjjReweight_fit_Wln_Wlight_2017')
  cb.cp().channel(['Znn']).process(['Zj_ll']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Znn_2017','CMS_vhcc_dRjjReweight_fit_Znn_Zlight_2017')

#  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2017','CMS_vhcc_dRjjReweight_Flavour_DYZj_cj_2017')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2017','CMS_vhcc_dRjjReweight_Flavour_DYZj_bj_2017')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2017','CMS_vhcc_dRjjReweight_Flavour_DYZj_cj_Low_2017')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2017','CMS_vhcc_dRjjReweight_Flavour_DYZj_bj_High_2017')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2017','CMS_vhcc_dRjjReweight_Flavour_DYZj_cj_Low_2017')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2017','CMS_vhcc_dRjjReweight_Flavour_DYZj_bj_High_2017')

  cb.cp().channel(['Znn']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2017','CMS_vhcc_dRjjReweight_Flavour_Znnj_cj_2017')
  cb.cp().channel(['Znn']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2017','CMS_vhcc_dRjjReweight_Flavour_Znnj_bj_2017')


  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_JEC_2017','CMS_cTagWeight_JEC_Low_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_JES_2017','CMS_cTagWeight_JES_Low_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_JER_2017','CMS_cTagWeight_JER_Low_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_PU_2017','CMS_cTagWeight_PU_Low_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_EleId_2017','CMS_cTagWeight_EleId_Low_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_MuId_2017','CMS_cTagWeight_MuId_Low_2017')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_muR','CMS_cTagWeight_muR_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_muF','CMS_cTagWeight_muF_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecDYJets','CMS_cTagWeight_XSecDYJets_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecST','CMS_cTagWeight_XSecST_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecWJets','CMS_cTagWeight_XSecWJets_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecTTbar','CMS_cTagWeight_XSecTTbar_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_Stat_2017','CMS_cTagWeight_Stat_2017_Low')



if year=='2018':
  cb.cp().RenameSystematic(cb,'CMS_j_PtCReg_Scale','CMS_j_PtCReg_Scale_2018')
  cb.cp().RenameSystematic(cb,'CMS_j_PtCReg_Smear','CMS_j_PtCReg_Smear_2018')

#  cb.cp().RenameSystematic(cb,'CMS_vhcc_puBackupWeight_2018','CMS_vhcc_puWeight_2018')
  cb.cp().RenameSystematic(cb,'CMS_PUIDWeight_13TeV_2018','CMS_vhcc_puJetId_2018')
  cb.cp().channel(['Wen','Wmn','Znn']).RenameSystematic(cb,'CMS_METUnclustEn','CMS_res_met_13TeV_2018')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_HEMIssue_13TeV_2018','CMS_scale_j_HEMIssue_2018_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_JEC','CMS_cTagWeight_JEC_2018')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_JES','CMS_cTagWeight_JES_2018')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_JER','CMS_cTagWeight_JER_2018')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_PU','CMS_cTagWeight_PU_2018')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_EleId','CMS_cTagWeight_EleId_2018')
  cb.cp().RenameSystematic(cb,'CMS_cTagWeight_MuId','CMS_cTagWeight_MuId_2018')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_Absolute_2018','CMS_scale_j_Absolute_2018_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_BBEC1_2018','CMS_scale_j_BBEC1_2018_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_EC2_2018','CMS_scale_j_EC2_2018_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_HF_2018','CMS_scale_j_HF_2018_13TeV')
  cb.cp().RenameSystematic(cb,'CMS_scale_j_RelativeSample_2018','CMS_scale_j_RelativeSample_2018_13TeV')

#  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZJets_Low_13TeV_2018')
#  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZJets_High_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zc_Low_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zb_Low_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zl_Low_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zc_High_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zb_High_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([1,3,5,7,9]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zl_High_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).process(['TT']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_TT_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).process(['s_Top']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_s_Top_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).process(['VVother']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_VVother_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).process(['VZcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_VZcc_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).process(['ggZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ggZH_hbb_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).process(['ZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZH_hbb_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).process(['ggZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ggZH_hcc_13TeV_2018')
  cb.cp().channel(['Zee','Zmm']).process(['ZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZH_hcc_13TeV_2018')

#  cb.cp().channel(['Wen','Wmn']).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZJets_13TeV_2018')
#  cb.cp().channel(['Wen','Wmn']).process(['Wj_cj','Wj_bj','Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_WJets_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).bin_id([1,3,5,7,9]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zc_High_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).bin_id([1,3,5,7,9]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zb_High_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).bin_id([1,3,5,7,9]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zl_High_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['Wj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Wc_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['Wj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Wb_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Wl_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['TT']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_TT_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['s_Top']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_s_Top_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['VVother']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_VVother_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['VZcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_VZcc_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['WH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_WH_hbb_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['ZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZH_hbb_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['WH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_WH_hcc_13TeV_2018')
  cb.cp().channel(['Wen','Wmn']).process(['ZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZH_hcc_13TeV_2018')

#  cb.cp().channel(['Znn']).process(['Zj_cj','Zj_bj','Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZJets_13TeV_2018')
#  cb.cp().channel(['Znn']).process(['Wj_cj','Wj_bj','Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_WJets_13TeV_2018')
  cb.cp().channel(['Znn']).bin_id([1,3,5,7,9]).process(['Zj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zc_High_13TeV_2018')
  cb.cp().channel(['Znn']).bin_id([1,3,5,7,9]).process(['Zj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zb_High_13TeV_2018')
  cb.cp().channel(['Znn']).bin_id([1,3,5,7,9]).process(['Zj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Zl_High_13TeV_2018')
  cb.cp().channel(['Znn']).process(['Wj_cj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Wc_13TeV_2018')
  cb.cp().channel(['Znn']).process(['Wj_bj']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Wb_13TeV_2018')
  cb.cp().channel(['Znn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_Wl_13TeV_2018')
  cb.cp().channel(['Znn']).process(['TT']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_TT_13TeV_2018')
  cb.cp().channel(['Znn']).process(['s_Top']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_s_Top_13TeV_2018')
  cb.cp().channel(['Znn']).process(['VVother']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_VVother_13TeV_2018')
  cb.cp().channel(['Znn']).process(['VZcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_VZcc_13TeV_2018')
  cb.cp().channel(['Znn']).process(['WH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_WH_hbb_13TeV_2018')
  cb.cp().channel(['Znn']).process(['ZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZH_hbb_13TeV_2018')
  cb.cp().channel(['Znn']).process(['ggZH_hbb']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ggZH_hbb_13TeV_2018')
  cb.cp().channel(['Znn']).process(['WH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_WH_hcc_13TeV_2018')
  cb.cp().channel(['Znn']).process(['ZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ZH_hcc_13TeV_2018')
  cb.cp().channel(['Znn']).process(['ggZH_hcc']).RenameSystematic(cb,'CMS_PostCTagWeight_13TeV_2018','CMS_PostCTagWeight_ggZH_hcc_13TeV_2018')


  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2018','CMS_vhcc_dRjjReweight_fit_Zll_Zc_2018')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2018','CMS_vhcc_dRjjReweight_fit_Zll_Zc_Low_2018')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2018','CMS_vhcc_dRjjReweight_fit_Zll_Zc_High_2018')
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Wln_2018','CMS_vhcc_dRjjReweight_fit_Wln_Wc_2018')
  cb.cp().channel(['Znn']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Znn_2018','CMS_vhcc_dRjjReweight_fit_Znn_Zc_2018')

  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2018','CMS_vhcc_dRjjReweight_fit_Zll_Zb_2018')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2018','CMS_vhcc_dRjjReweight_fit_Zll_Zb_Low_2018')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2018','CMS_vhcc_dRjjReweight_fit_Zll_Zb_High_2018')
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Wln_2018','CMS_vhcc_dRjjReweight_fit_Wln_Wb_2018')
  cb.cp().channel(['Znn']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Znn_2018','CMS_vhcc_dRjjReweight_fit_Znn_Zb_2018')

  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2018','CMS_vhcc_dRjjReweight_fit_Zll_Zlight_2018')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2018','CMS_vhcc_dRjjReweight_fit_Zll_Zlight_Low_2018')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_ll']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Zll_2018','CMS_vhcc_dRjjReweight_fit_Zll_Zlight_High_2018')
  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Wln_2018','CMS_vhcc_dRjjReweight_fit_Wln_Wlight_2018')
  cb.cp().channel(['Znn']).process(['Zj_ll']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_fit_Znn_2018','CMS_vhcc_dRjjReweight_fit_Znn_Zlight_2018')

#  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2018','CMS_vhcc_dRjjReweight_Flavour_DYZj_cj_2018')
#  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2018','CMS_vhcc_dRjjReweight_Flavour_DYZj_bj_2018')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2018','CMS_vhcc_dRjjReweight_Flavour_DYZj_cj_Low_2018')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2018','CMS_vhcc_dRjjReweight_Flavour_DYZj_bj_High_2018')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_cj']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2018','CMS_vhcc_dRjjReweight_Flavour_DYZj_cj_Low_2018')
  cb.cp().channel(['Zee','Zmm']).process(['Zj_bj']).bin_id([1,3,5,7,9]).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2018','CMS_vhcc_dRjjReweight_Flavour_DYZj_bj_High_2018')

  cb.cp().channel(['Znn']).process(['Zj_cj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_cj_2018','CMS_vhcc_dRjjReweight_Flavour_Znnj_cj_2018')
  cb.cp().channel(['Znn']).process(['Zj_bj']).RenameSystematic(cb,'CMS_vhcc_dRjjReweight_Flavour_Zj_bj_2018','CMS_vhcc_dRjjReweight_Flavour_Znnj_bj_2018')


  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_JEC_2018','CMS_cTagWeight_JEC_Low_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_JES_2018','CMS_cTagWeight_JES_Low_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_JER_2018','CMS_cTagWeight_JER_Low_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_PU_2018','CMS_cTagWeight_PU_Low_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_EleId_2018','CMS_cTagWeight_EleId_Low_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_MuId_2018','CMS_cTagWeight_MuId_Low_2018')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_muR','CMS_cTagWeight_muR_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_muF','CMS_cTagWeight_muF_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecDYJets','CMS_cTagWeight_XSecDYJets_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecST','CMS_cTagWeight_XSecST_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecWJets','CMS_cTagWeight_XSecWJets_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_XSecTTbar','CMS_cTagWeight_XSecTTbar_Low')
  cb.cp().channel(['Zee','Zmm']).bin_id([2,4,6,8,10]).RenameSystematic(cb,'CMS_cTagWeight_Stat_2018','CMS_cTagWeight_Stat_2018_Low')


if year=='2017' or year=='2018':
  #rename of PDF systematics uncertainties to match conventions
  cb.cp().process(['ggZH_hbb','ggZH_hcc']).RenameSystematic(cb,'CMS_LHE_pdf_ggZH', 'CMS_LHE_weights_pdf_ggZH') 
  cb.cp().process(['ZH_hbb','ZH_hcc']).RenameSystematic(cb,'CMS_LHE_pdf_ZH', 'CMS_LHE_weights_pdf_ZH') 
  cb.cp().process(['WH_hbb','WH_hcc']).RenameSystematic(cb,'CMS_LHE_pdf_WH', 'CMS_LHE_weights_pdf_WH') 
  cb.cp().process(['Zj_ll']).RenameSystematic(cb,'CMS_LHE_pdf_Zj_ll', 'CMS_LHE_weights_pdf_Zj') 
  cb.cp().process(['Zj_bj']).RenameSystematic(cb,'CMS_LHE_pdf_Zj_bj', 'CMS_LHE_weights_pdf_Zj') 
  cb.cp().process(['Zj_cj']).RenameSystematic(cb,'CMS_LHE_pdf_Zj_cj', 'CMS_LHE_weights_pdf_Zj') 
  cb.cp().process(['Wj_ll']).RenameSystematic(cb,'CMS_LHE_pdf_Wj_ll', 'CMS_LHE_weights_pdf_Wj') 
  cb.cp().process(['Wj_bj']).RenameSystematic(cb,'CMS_LHE_pdf_Wj_bj', 'CMS_LHE_weights_pdf_Wj') 
  cb.cp().process(['Wj_cj']).RenameSystematic(cb,'CMS_LHE_pdf_Wj_cj', 'CMS_LHE_weights_pdf_Wj') 
  cb.cp().process(['TT']).RenameSystematic(cb,'CMS_LHE_pdf_TT','CMS_LHE_weights_pdf_TT')
  cb.cp().process(['s_Top']).RenameSystematic(cb,'CMS_LHE_pdf_ST','CMS_LHE_weights_pdf_ST')
  cb.cp().process(['VVother']).RenameSystematic(cb,'CMS_LHE_pdf_VVother','CMS_LHE_weights_pdf_VV')
  cb.cp().process(['VZcc']).RenameSystematic(cb,'CMS_LHE_pdf_VZcc','CMS_LHE_weights_pdf_VV')
  
  #rename of Renormalization/Factorization scale systematics uncertainties to match conventions
  cb.cp().process(['VVother']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_VVother','CMS_LHE_weights_scale_muR_VV')
  cb.cp().process(['VZcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_VZcc','CMS_LHE_weights_scale_muR_VV')
  cb.cp().process(['VVother']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_VVother','CMS_LHE_weights_scale_muF_VV')
  cb.cp().process(['VZcc']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_VZcc','CMS_LHE_weights_scale_muF_VV')
  cb.cp().process(['Zj_ll']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Zj_ll', 'CMS_LHE_weights_scale_muR_Zj') 
  cb.cp().process(['Zj_bj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Zj_bj', 'CMS_LHE_weights_scale_muR_Zj') 
  cb.cp().process(['Zj_cj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Zj_cj', 'CMS_LHE_weights_scale_muR_Zj') 
  cb.cp().process(['Wj_ll']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Wj_ll', 'CMS_LHE_weights_scale_muR_Wj') 
  cb.cp().process(['Wj_bj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Wj_bj', 'CMS_LHE_weights_scale_muR_Wj') 
  cb.cp().process(['Wj_cj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muR_Wj_cj', 'CMS_LHE_weights_scale_muR_Wj') 
  cb.cp().process(['Zj_ll']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Zj_ll', 'CMS_LHE_weights_scale_muF_Zj') 
  cb.cp().process(['Zj_bj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Zj_bj', 'CMS_LHE_weights_scale_muF_Zj') 
  cb.cp().process(['Zj_cj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Zj_cj', 'CMS_LHE_weights_scale_muF_Zj') 
  cb.cp().process(['Wj_ll']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Wj_ll', 'CMS_LHE_weights_scale_muF_Wj') 
  cb.cp().process(['Wj_bj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Wj_bj', 'CMS_LHE_weights_scale_muF_Wj') 
  cb.cp().process(['Wj_cj']).RenameSystematic(cb,'CMS_LHE_weights_scale_muF_Wj_cj', 'CMS_LHE_weights_scale_muF_Wj') 

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



##cb.ForEachProc(lambda x: cb.FilterSysts(lambda y: y.name()=="CMS_LHE_weights_pdf_ggZH" if y.bin_id()==3 ))
#cb.FilterSysts(lambda y: y.name()=="CMS_LHE_weights_pdf_ggZH" and (y.bin_id()==3 or y.bin_id()==4 or y.bin_id()==7 or y.bin_id()==8))

#Luca #Correlate the Zll and Wln lepton efficiencies uncertainties:
#Luca cb.cp().channel(['Wmn']).RenameSystematic(cb,'CMS_vhcc_eff_m_Wln_13TeV_2016','CMS_vhcc_eff_m_13TeV_2016')
#Luca cb.cp().channel(['Zmm']).RenameSystematic(cb,'CMS_vhcc_eff_m_Zll_13TeV_2016','CMS_vhcc_eff_m_13TeV_2016')
#Luca cb.cp().channel(['Wen']).RenameSystematic(cb,'CMS_vhcc_eff_e_Wln_13TeV_2016','CMS_vhcc_eff_e_13TeV_2016')
#Luca cb.cp().channel(['Zee']).RenameSystematic(cb,'CMS_vhcc_eff_e_Zll_13TeV_2016','CMS_vhcc_eff_e_13TeV_2016')

#Luca if year=="2016":
#Luca   print('Renaming the systematics associated to the lepton efficiency')
#Luca   cb.cp().channel(['Wen']).RenameSystematic(cb,'CMS_Lep_SF','CMS_Lep_SF_Wen_13TeV_2016')
#Luca   cb.cp().channel(['Wmn']).RenameSystematic(cb,'CMS_Lep_SF','CMS_Lep_SF_Wmn_13TeV_2016')
#Luca   cb.cp().channel(['Zee']).RenameSystematic(cb,'CMS_Lep_SF','CMS_Lep_SF_Zee_13TeV_2016')
#Luca   cb.cp().channel(['Zmm']).RenameSystematic(cb,'CMS_Lep_SF','CMS_Lep_SF_Zmm_13TeV_2016')



if args.doVV:
  cb.SetGroup('signal_theory',['CMS_LHE_weights_pdf_VV','.*LHE_weights.*VV'])
  cb.SetGroup('bkg_theory',['pdf_Higgs.*','pdf_qqbar','pdf_gg','CMS_LHE_weights_pdf_VV','CMS_vhbb_ST','.*LHE_weights.*ZHbb.*','.*LHE_weights.*WHbb.*','.*LHE_weights.*ggZHbb.*','.*LHE_weights.*TT.*','.*LHE_weights.*VV','.*LHE_weights.*Zj_ll.*','LHE_weights.*Zj_bj.*','LHE_weights.*Zj_cj.*','LHE_weights.*Wj_ll.*','LHE_weights.*Wj_bj.*','LHE_weights.*Wj_cj.*','LHE_weights.*s_Top.*','LHE_weights.*QCD.*','.*LHE_weights.*ZHcc.*','.*LHE_weights.*WHcc.*','.*LHE_weights.*ggZHcc.*','BR_hcc','QCDscale_ggZH','QCDscale_VH',])
else:
  cb.SetGroup('signal_theory',['pdf_Higgs.*','BR_hcc','QCDscale_ggZH','QCDscale_VH','.*LHE_weights.*ZHcc.*','.*LHE_weights.*WHcc.*','.*LHE_weights.*ggZHcc.*'])
  cb.SetGroup('bkg_theory',['pdf_qqbar','pdf_gg','CMS_LHE_weights_pdf_VV*','CMS_vhbb_ST','.*LHE_weights.*ZHbb.*','.*LHE_weights.*WHbb.*','.*LHE_weights.*ggZHbb.*','.*LHE_weights.*TT.*','.*LHE_weights.*VV.*','.*LHE_weights.*Zj_ll.*','LHE_weights.*Zj_bj.*','LHE_weights.*Zj_cj.*','LHE_weights.*Wj_ll.*','LHE_weights.*Wj_bj.*','LHE_weights.*Wj_cj.*','LHE_weights.*s_Top.*','LHE_weights.*QCD.*'])
  
cb.SetGroup('sim_modelling',['CMS_vhcc_ptwweights_13TeV_.*','CMS_vhcc_ptzweights_13TeV_.*','CMS_vhcc_topptWeight_13TeV_.*','.*vhcc_vjetnlodetajjrw.*','heavyFlavHadFrac_mismodelling.*'])
cb.SetGroup('jes',['CMS_scale_j.*'])
cb.SetGroup('jer',['CMS_res_j_13TeV.*'])
cb.SetGroup('ctag',['CMS_cTagWeight.*'])
cb.SetGroup('lumi',['lumi_13TeV.*','.*puWeight.*'])
cb.SetGroup('lep_eff',['.*eff_e.*','.*eff_m.*','.*PrefireWeight.*'])
cb.SetGroup('jet_puId',['.*puJetId.*'])
cb.SetGroup('met',['.*MET.*','.*met.*'])

#To rename processes:
#cb.cp().ForEachObj(lambda x: x.set_process("WH_lep") if x.process()=='WH_hbb' else None)


rebin = ch.AutoRebin().SetBinThreshold(0.).SetBinUncertFraction(1.0).SetRebinMode(1).SetPerformRebin(True).SetVerbosity(1)

#binning=np.linspace(0.2,1.0,num=13)
#print binning


if args.auto_rebin:
  rebin.Rebin(cb, cb)
  
#Luca if args.zero_out_low:
#Luca   range_to_drop = {'Wen':[[1,0,0.5]],'Wmn':[[1,0,0.5]],'Znn':[[1,0,0.5]],'Zee':[[1,0,0.5],[2,0,0.5]],'Zmm':[[1,0,0.5],[2,0,0.5]]} #First number is bin_id, second number lower bound of range to drop, third number upper bound of range to drop
#Luca   for chn in chns:
#Luca     for i in range(len(range_to_drop[chn])):
#Luca       cb.cp().channel([chn]).bin_id([range_to_drop[chn][i][0]]).ZeroBins(range_to_drop[chn][i][1],range_to_drop[chn][i][2])
      
ch.SetStandardBinNames(cb)


if args.rebinning_scheme == 'SR_nb' :
  writer=ch.CardWriter("OptimizeBinSR_NomShape_" + year +"/"+args.output_folder + "nb_"+str(nBinSR)+"/$TAG/$BIN"+year+".txt",
                       "OptimizeBinSR_NomShape_" + year +"/"+args.output_folder + "nb_"+str(nBinSR)+"/$TAG/vhcc_input_$BIN"+year+".root")

elif args.rebinning_scheme == 'SR_Scan':
  writer=ch.CardWriter("OptimizeBinSR_NomShape_" + year +"/"+args.output_folder + "edge_"+str(edge)+"/$TAG/$BIN"+year+".txt",
                       "OptimizeBinSR_NomShape_" + year +"/"+args.output_folder + "edge_"+str(edge)+"/$TAG/vhcc_input_$BIN"+year+".root")
  
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

if args.rebinning_scheme == 'SR_nb':
    writer.WriteCards("Znn",cb.cp().bin_id([1]).channel(['Znn']))
    writer.WriteCards("Wen",cb.cp().bin_id([1]).channel(['Wen']))
    writer.WriteCards("Wmn",cb.cp().bin_id([1]).channel(['Wmn']))
    writer.WriteCards("Zee",cb.cp().bin_id([1,2]).channel(['Zee']))
    writer.WriteCards("Wmm",cb.cp().bin_id([1,2]).channel(['Zmm']))

else:
  if 'Znn' in chns:
    #writer.WriteCards("Znn",cb.cp().FilterAll(lambda x: not (x.channel()=='Znn' or ( (x.channel() in ['Wmn','Wen']) and x.bin_id() in [3,4,5,6,7,8]))))
    if args.mjj:
      writer.WriteCards("Znn",cb.cp().channel(['Znn']))
      writer.WriteCards("Znn",cb.cp().bin_id([3,5,7,9]).channel(['Wmn','Wen']))
      #Luca writer.WriteCards("Znn_CRonly",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Znn','Wmn','Wen']))
    else:
      writer.WriteCards("Znn",cb.cp().channel(['Znn']))
      writer.WriteCards("Znn",cb.cp().bin_id([5,6,7,8]).channel(['Wmn','Wen']))
      writer.WriteCards("Znn_CRonly",cb.cp().bin_id([3,7]).channel(['Znn']))
      #Luca writer.WriteCards("Znn_CRonly",cb.cp().bin_id([5,6,7,8]).channel(['Wmn','Wen']))
    
      #Zll and Wln:
  if 'Wen' in chns and 'Wmn' in chns:
    writer.WriteCards("Wln",cb.cp().channel(['Wen','Wmn']))
    #Luca writer.WriteCards("Wln_CRonly",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Wen','Wmn']))

  if 'Zee' in chns and 'Zmm' in chns:
    writer.WriteCards("Zll",cb.cp().channel(['Zee','Zmm']))
    #Luca writer.WriteCards("Zll_CRonly",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Zee','Zmm']))
