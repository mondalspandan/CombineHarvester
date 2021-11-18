import os
import re

#parser = argparse.ArgumentParser()
#parser.add_argument('--indir', default='', help="""Parse the datacards input directory""")
#args = parser.parse_args()

def computeLimit(indir, channels):
    print(indir)

    info_map=[]
    for ch in channels:
        info_vector=('')
        datacard = str(indir+"/"+ch+"/vhcc_"+str(ch)+"_1_13TeV2016.txt")                               
        command_1 = "combine -M AsymptoticLimits -d "+datacard+" --run blind --cminDefaultMinimizerStrategy 0 | grep 'Expected 50.0%' > tmp_opt.txt"
        os.system(command_1)
        limit = '0'
        with open('tmp_opt.txt') as outfile:
            first_line = outfile.readline()
            print(first_line)
            limit = first_line.replace('Expected 50.0%: r < ','')
            limit = limit.replace('\n','')
            print("Our exl. limit is: ",limit)
        info_vector=(ch,limit)
        print(info_vector)
        info_map.append(info_vector)
    return info_map


#Luca  #indir="OptimizeBinSR_2016"
#Luca  indir="OptimizeBinSR_NomShape_2016"
#Luca  channels=['Zee','Zmm','Wen','Wmn','Znn']
#Luca  bins=[120,60,40,30,20,15,12,10,8,6,5,4,3,2]
#Luca  
#Luca  #channels=['Zee']
#Luca  #bins=[120,60,40,30]
#Luca  
#Luca  
#Luca  for ch in channels:
#Luca      print("============================= Start Optimization in "+ch+" channel")
#Luca      for b in bins:
#Luca          print("bin:", b+1)
#Luca  #        datacard = str(indir+"/test_newOpt_nb_"+str(b+1)+"/"+ch+"/vhcc_"+str(ch)+"_1_13TeV2016.txt")
#Luca          datacard = str(indir+"/test_newOpt_NomShape_nb_"+str(b+1)+"/"+ch+"/vhcc_"+str(ch)+"_1_13TeV2016.txt")                               
#Luca          command_1 = "combine -M AsymptoticLimits -d "+datacard+" --run blind --cminDefaultMinimizerStrategy 0 --freezeParameters all| grep 'Expected 50.0%'"
#Luca          os.system(command_1)
#Luca          command_2 = "combine -M AsymptoticLimits -d "+datacard+" --run blind --cminDefaultMinimizerStrategy 0 | grep 'Expected 50.0%'"
#Luca          os.system(command_2)
