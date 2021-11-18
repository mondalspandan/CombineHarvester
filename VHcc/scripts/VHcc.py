
#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.VHcc.systematics_vhcc as systs
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

  

parser = argparse.ArgumentParser()
parser.add_argument(
 '--channel', default='all', help="""Which channels to run? Supported options: 'all', 'Zee', 'Zmm', 'Zll', 'Wen', 'Wmn','Wln'""")
parser.add_argument(
 '--output_folder', default='vhcc2017', help="""Subdirectory of ./output/ where the cards are written out to""")
parser.add_argument(
 '--auto_rebin', action='store_true', help="""Rebin automatically?""")
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
 '--year', default='2017', help="""Year to produce datacards for (2017 or 2016)""")
parser.add_argument(
 '--extra_folder', default='', help="""Additional folder where cards are""")
parser.add_argument(
 '--rebinning_scheme', default='v2-whznnh-hf-dnn', help="""Rebinning scheme for CR and SR distributions""")
parser.add_argument(
 '--doVV', default=False, help="""if True assume we are running the VZ(cc) analysis""")
parser.add_argument(
 '--mjj',  default=True, help="""if True assume we are running the mjj analysis""")
parser.add_argument(
 '--sr_only',  default=False, help="""if True assume we are running only the signal region""")

args = parser.parse_args()

cb = ch.CombineHarvester()

shapes = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/VHcc/shapes/'

mass = ['125']

chns = []

#Luca if args.channel=="all":
#Luca   chns = ['Wen','Wmn','Zee','Zmm','Znn']
#Luca if 'Zll' in args.channel or 'Zmm' in args.channel:
#Luca   chns.append('Zmm')
#Luca if 'Zll' in args.channel  or 'Zee' in args.channel:
#Luca   chns.append('Zee')
#Luca if 'Wln' in args.channel or 'Wmn' in args.channel:
#Luca   chns.append('Wmn')
#Luca if 'Wln' in args.channel or 'Wen' in args.channel:
#Luca   chns.append('Wen')
#Luca if 'Znn' in args.channel or 'Znn' in args.channel:
#Luca   chns.append('Znn')

if args.channel=="all":
  chns = ['Wen','Wmn','Znn','Zee','Zmm']
if 'Zll' in args.channel or 'Zmm' in args.channel:
  chns.append('Zmm')
if 'Zll' in args.channel  or 'Zee' in args.channel:
  chns.append('Zee')
if 'Wln' in args.channel or 'Wmn' in args.channel or 'Znn' in args.channel:
  chns.append('Wmn')
if 'Wln' in args.channel or 'Wen' in args.channel or 'Znn' in args.channel:
  chns.append('Wen')
if 'Znn' in args.channel:
  chns.append('Znn')


year = args.year
if year is not "2016" and not "2017":
  print "Year ", year, " not supported! Choose from: '2016', '2017'"
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
  bkg_procs = {
    'Wen' : ['WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_blc','Wj_bbc','Wj_cc','VVLF','VVbb','VVcc'],
    'Wmn' : ['WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_blc','Wj_bbc','Wj_cc','VVLF','VVbb','VVcc'],
    'Zmm' : ['ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_blc','Zj_bbc','Zj_cc','VVLF','VVbb','VVcc'],
    'Zee' : ['ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_blc','Zj_bbc','Zj_cc','VVLF','VVbb','VVcc'],
    'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb','s_Top','TT','Zj_ll','Zj_blc','Zj_bbc','Zj_cc','Wj_ll','Wj_blc','Wj_bbc','Wj_cc','VVLF','VVbb','VVcc','QCD'],
    #'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb','s_Top','TT','Zj_ll','Zj_blc','Zj_bbc','Zj_cc','Wj_ll','Wj_blc','Wj_bbc','Wj_cc','VVLF','VVbb','VVcc'],
  }
else:
  bkg_procs = {
    'Wen' : ['WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_blc','Wj_bbc','Wj_cc','VVLF','VVbb'],
    'Wmn' : ['WH_hbb','ZH_hbb','s_Top','TT','Wj_ll','Wj_blc','Wj_bbc','Wj_cc','VVLF','VVbb'],
    'Zmm' : ['ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_blc','Zj_bbc','Zj_cc','VVLF','VVbb'],
    'Zee' : ['ZH_hbb','ggZH_hbb','s_Top','TT','Zj_ll','Zj_blc','Zj_bbc','Zj_cc','VVLF','VVbb'],
    'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb','s_Top','TT','Zj_ll','Zj_blc','Zj_bbc','Zj_cc','Wj_ll','Wj_blc','Wj_bbc','Wj_cc','VVLF','VVbb','QCD'],
    #'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb','s_Top','TT','Zj_ll','Zj_blc','Zj_bbc','Zj_cc','Wj_ll','Wj_blc','Wj_bbc','Wj_cc','VVLF','VVbb'],
  }

if not args.doVV:
  sig_procs = {
    'Wen' : ['WH_hcc','ZH_hcc'],
    'Wmn' : ['WH_hcc','ZH_hcc'],
    'Zmm' : ['ZH_hcc','ggZH_hcc'],
    'Zee' : ['ZH_hcc','ggZH_hcc'],
    'Znn' : ['ZH_hcc','ggZH_hcc','WH_hcc']
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
    bkg_procs['Znn'].remove('QCD')
    
    if not args.sr_only:
      cats = {
        'Zee' : [
          (1, 'SR_high_Zee'), (2, 'SR_low_Zee'), (3, 'Zlf_high_Zee'), (4,'Zlf_low_Zee'),
          (5, 'Zhf_high_Zee'), (6, 'Zhf_low_Zee'), (7,'ttbar_high_Zee'), (8,'ttbar_low_Zee')
          ],
        'Zmm' : [
          (1, 'SR_high_Zmm'), (2, 'SR_low_Zmm'), (3, 'Zlf_high_Zmm'), (4,'Zlf_low_Zmm'),
          (5, 'Zhf_high_Zmm'), (6, 'Zhf_low_Zmm'), (7,'ttbar_high_Zmm'), (8,'ttbar_low_Zmm')
          ],
        'Wen' : [
          (1, 'SR_Wenu'), (3,'Wlf_Wenu'), (5,'Whf_Wenu'), (7,'ttbar_Wenu')
          ],
        'Wmn' : [
          (1, 'SR_Wmunu'), (3,'Wlf_Wmunu'), (5,'Whf_Wmunu'), (7,'ttbar_Wmunu')
          ],
        'Znn' : [
          (1, 'SR_Znn'), (3,'Vlf_Znn'), (5,'Vhf_Znn'), (7,'ttbar_Znn')
          ]
        }
    else:
      cats = {
        'Zee' : [
          (1, 'SR_high_Zee'), (2, 'SR_low_Zee')
          ],
        'Zmm' : [
          (1, 'SR_high_Zmm'), (2, 'SR_low_Zmm')
          ],
        'Wen' : [
          (1, 'SR_Wenu')
          ],
        'Wmn' : [
          (1, 'SR_Wmunu')
           ],
        'Znn' : [
          (1, 'SR_Znn')
          ]
        }
      
for chn in chns:
  cb.AddObservations( ['*'], ['vhcc'], ['13TeV'], [chn], cats[chn])
  cb.AddProcesses( ['*'], ['vhcc'], ['13TeV'], [chn], bkg_procs[chn], cats[chn], False)
  cb.AddProcesses( ['*'], ['vhcc'], ['13TeV'], [chn], sig_procs[chn], cats[chn], True)

# Filter QCD from processes in Znn
cb.FilterProcs(lambda x: x.bin_id()==1 and x.channel()=='Znn' and x.process()=='QCD')
  
systs.AddCommonSystematics(cb)
if year=='2016':
  systs.AddSystematics2016(cb)
if year=='2017':
  systs.AddSystematics2017(cb)


if args.bbb_mode==0:
  cb.AddDatacardLineAtEnd("* autoMCStats -1")
elif args.bbb_mode==1:
  cb.AddDatacardLineAtEnd("* autoMCStats 0")



for chn in chns:
  file = shapes + input_folders[chn] + "/vhcc_"+chn+"-"+year+".root"
  if input_fwks[chn] == 'AT':
    cb.cp().channel([chn]).backgrounds().ExtractShapes(
      file, 'BDT_$BIN_$PROCESS', 'BDT_$BIN_$PROCESS_$SYSTEMATIC')
    cb.cp().channel([chn]).signals().ExtractShapes(
      file, 'BDT_$BIN_$PROCESS', 'BDT_$BIN_$PROCESS_$SYSTEMATIC')

# play with rebinning (and/or cutting) of the shapes
if args.doVV:
  binning=np.linspace(75.0,105.0,num=6)
  print 'binning centred around Z-mass in SR (Mjj):',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([1,2]).VariableRebin(binning)


if args.rebinning_scheme == 'zll-rebin':
  binning=np.linspace(0.0,1.0,num=16)
  print 'binning in TT-CR,HF-CR fitting variable (Jet_CvsB):',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([5,6,7,8]).VariableRebin(binning)

  binning=np.linspace(0.05,1.0,num=16)
  print 'binning in LF-CR fitting variable (Jet_CvsL):',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([3,4]).VariableRebin(binning)

   
if args.rebinning_scheme == 'zll-fix': # all channels: 1bin in TT/LF, 2bins in HF
  #binning=np.linspace(50.0,200.0,num=6)
  #print 'binning in SR fitting variable (mjj):',binning,'for Zll channels'
  #cb.cp().channel(['Zee','Zmm']).bin_id([1,2]).VariableRebin(binning)

  #Luca binning=np.linspace(0.0,1.0,num=5)
  #Luca print 'binning in TT-CR fitting variable (Jet_CvsB):',binning,'for Zll channels'
  #Luca cb.cp().channel(['Zee','Zmm']).bin_id([7,8]).VariableRebin(binning)

  binning=np.linspace(0.0,1.0,num=2)
  print 'binning in TT-CR fitting variable (Jet_CvsB):',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([8]).VariableRebin(binning)
  
  binning=np.linspace(0.0,1.0,num=2)
  print 'binning in TT-CR fitting variable (Jet_CvsB):',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([7]).VariableRebin(binning)
  
  binning=np.linspace(0.0,1.0,num=4)
  print 'binning in HF-CR fitting variable (Jet_CvsB):',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([5,6]).VariableRebin(binning)

  binning=np.linspace(0.05,0.4,num=2)
  print 'binning in LF-CR fitting variable (Jet_CvsL):',binning,'for Zll channels'
  cb.cp().channel(['Zee','Zmm']).bin_id([3,4]).VariableRebin(binning)

if args.rebinning_scheme == 'znn-rebin': # all channels: 1bin in TT/LF, 2bins in HF

  binning=np.linspace(0.0,1.0,num=11) 
  print 'binning in CR for LF,TT fitting variable:',binning,'for Znn channelrs'
  cb.cp().bin_id([3,7]).VariableRebin(binning)
  
  binning=np.linspace(0.0,1.0,num=6)
  print 'binning in CR for HF fitting variable:',binning,'for Znn channels'
  cb.cp().channel(['Znn']).bin_id([5]).VariableRebin(binning) 
   

cb.FilterProcs(lambda x: drop_zero_procs(cb,x))
cb.FilterSysts(lambda x: drop_zero_systs(x))
#AUTHORIZED PERSON ONLY!! Drop QCD in Z+HF CR
cb.FilterProcs(lambda x: drop_znnqcd(cb,x))

if args.doVV:
    cb.FilterSysts(lambda x: x.name() in "CMS_vhbb_VV")

cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_ll']).RenameSystematic(cb,'CMS_vhbb_vjetnlodetajjrw_13TeV','CMS_Wj_ll_vhbb_vjetnlodetajjrw_13TeV')
cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_blc']).RenameSystematic(cb,'CMS_vhbb_vjetnlodetajjrw_13TeV','CMS_Wj_blc_vhbb_vjetnlodetajjrw_13TeV')
cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_bbc']).RenameSystematic(cb,'CMS_vhbb_vjetnlodetajjrw_13TeV','CMS_Wj_bbc_vhbb_vjetnlodetajjrw_13TeV')
cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj_cc']).RenameSystematic(cb,'CMS_vhbb_vjetnlodetajjrw_13TeV','CMS_Wj_cc_vhbb_vjetnlodetajjrw_13TeV')
cb.cp().channel(['Zee','Zmm','Znn']).process(['Zj_ll']).RenameSystematic(cb,'CMS_vhbb_vjetnlodetajjrw_13TeV','CMS_Zj_ll_vhbb_vjetnlodetajjrw_13TeV')
cb.cp().channel(['Zee','Zmm','Znn']).process(['Zj_blc']).RenameSystematic(cb,'CMS_vhbb_vjetnlodetajjrw_13TeV','CMS_Zj_blc_vhbb_vjetnlodetajjrw_13TeV')
cb.cp().channel(['Zee','Zmm','Znn']).process(['Zj_bbc']).RenameSystematic(cb,'CMS_vhbb_vjetnlodetajjrw_13TeV','CMS_Zj_bbc_vhbb_vjetnlodetajjrw_13TeV')
cb.cp().channel(['Zee','Zmm','Znn']).process(['Zj_cc']).RenameSystematic(cb,'CMS_vhbb_vjetnlodetajjrw_13TeV','CMS_Zj_cc_vhbb_vjetnlodetajjrw_13TeV')
#Luca cb.cp().signals().RenameSystematic(cb,'CMS_res_j_reg_13TeV','CMS_signal_resolution_13TeV')
#Luca cb.cp().channel(['Wen','Wmn','Znn']).RenameSystematic(cb,'CMS_res_j_reg_13TeV','CMS_NoKinFit_res_j_reg_13TeV')
#Luca cb.cp().channel(['Zee','Zmm']).RenameSystematic(cb,'CMS_res_j_reg_13TeV','CMS_KinFit_res_j_reg_13TeV')


cb.SetGroup('signal_theory',['pdf_Higgs.*','BR_hbb','QCDscale_ggZH','QCDscale_VH','CMS_vhbb_boost.*','.*LHE_weights.*ZHcc*','.*LHE_weights.*WHcc*','.*LHE_weights.*ggZHcc*'])
cb.SetGroup('bkg_theory',['pdf_qqbar','pdf_gg','CMS_vhbb_VV','CMS_vhbb_ST','.*LHE_weights.*ZHbb*','.*LHE_weights.*WHbb*','.*LHE_weights.*ggZHbb*','.*LHE_weights.*TT.*','.*LHE_weights.*VV.*','.*LHE_weights.*Zj_ll.*','LHE_weights.*Zj_blc.*','LHE_weights.*Zj_bbc.*','LHE_weights.*Zj_cc.*','LHE_weights.*Wj_ll.*','LHE_weights.*Wj_blc.*','LHE_weights.*Wj_bbc.*','LHE_weights.*Wj_cc.*','LHE_weights.*s_Top.*','LHE_weights.*QCD.*'])
cb.SetGroup('sim_modelling',['CMS_vhbb_ptwweights.*','CMS_vhbb_vjetnlodetajjrw.*'])
cb.SetGroup('jes',['CMS_scale_j.*'])
cb.SetGroup('jer',['CMS_res_j.*','CMS_signal_resolution.*'])
cb.SetGroup('btag',['.*bTagWeight.*JES.*','.*bTagWeight.*HFStats.*','.*bTagWeight.*LF_.*','.*bTagWeight.*cErr.*'])
cb.SetGroup('mistag',['.*bTagWeight.*LFStats.*','.*bTagWeight.*HF_.*'])
cb.SetGroup('lumi',['lumi_13TeV','.*puWeight.*'])
cb.SetGroup('lep_eff',['.*eff_e.*','.*eff_m.*'])
cb.SetGroup('met',['.*MET.*'])



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


if 'Znn' in chns:
  #writer.WriteCards("Znn",cb.cp().FilterAll(lambda x: not (x.channel()=='Znn' or ( (x.channel() in ['Wmn','Wen']) and x.bin_id() in [3,4,5,6,7,8]))))
  if args.mjj:
    writer.WriteCards("Znn",cb.cp().channel(['Znn']))
    writer.WriteCards("Znn",cb.cp().bin_id([3,7]).channel(['Wmn','Wen']))
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
