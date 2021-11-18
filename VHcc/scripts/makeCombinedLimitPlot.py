import ROOT

def redrawBorder():
   # this little macro redraws the axis tick marks and the pad border lines.
   print 'redrawing borders of pad named:' , ROOT.gPad.GetName(), ROOT.gPad.GetTitle()
   ROOT.gPad.Update();
   ROOT.gPad.RedrawAxis();
   l = ROOT.TLine()
   l.SetLineWidth(3)
   l.DrawLine(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax());
   l.DrawLine(ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax());
   l.DrawLine(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax());
   l.DrawLine(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin());


## format is
## channel_name obs exp -2sigma -1sigma +1sigma +2sigma
def parseFile(inputFileName):
    """ return a tuple containing the data """
    
    data = []
    with open (inputFileName) as fIn:
        for line in fIn:
            line = (line.split("#")[0]).strip()
            if line:
                tokens = line.split()
                if len(tokens) < 7:
                    print "cannot parse line: ", line
                    print "each row should have 7 elements"
                    continue
                info = tuple([tokens[0]] + [float(x) for x in tokens[1:]])
                data.append(info)
    return data

### configuration
plot_RunI = False
add_RunI_line = True
add_comb_line = True
logx = False
xmin = 0 if not logx else 5
xmax = 200 if not logx else 400
canv_width  = 800
canv_height = 600
blind     = False
blindComb = False
# twoColLeg = False # non 

##################


inputFileName = '/afs/cern.ch/work/l/lmastrol/ANALYSIS_TOOLS/limit_final/VHccLimits/CMSSW_8_1_0/src/CombineHarvester/VHcc/LimitsPerChannel.txt'
data = parseFile(inputFileName)

# remove all RunI plots if not to be plotted
if not plot_RunI:
    print "Will not plot Run I"
    data = filter( lambda s: not "RunI" in s[0], data)

for d in data:
    print d
plotted_lines = [d[0] for d in data]
print plotted_lines

nlines = len(data)
print "input has " , nlines , "entries"

## each "line" is represented as a unity in the underlying frame

frame = ROOT.TH2D("frame", "", 100, xmin, xmax, nlines, 0, nlines)
c1 = ROOT.TCanvas("c1", "c1", canv_width, canv_height)
c1.SetFrameLineWidth(3)
c1.SetLeftMargin(0.3)
if logx: c1.SetLogx()
frame.SetStats(0)
if not logx: frame.GetXaxis().SetNdivisions(505)
else:
    frame.GetXaxis().SetNoExponent(True)
    frame.GetXaxis().SetMoreLogLabels(True)

### build the plots
graphs_obs = ROOT.TGraphAsymmErrors()
graphs_exp = ROOT.TGraphAsymmErrors()
graphs_2sigma = ROOT.TGraphAsymmErrors()
graphs_1sigma = ROOT.TGraphAsymmErrors()

graphs_obs.SetName('graphs_obs')
graphs_exp.SetName('graphs_exp')
graphs_2sigma.SetName('graphs_2sigma')
graphs_1sigma.SetName('graphs_1sigma')

legend = {
   '0L': '#splitline{0L:}{#scale[0.75]{#splitline{Exp.=%.0f#timesSM}{Obs.=%.0f#timesSM}}}'%(data[0][2],data[0][1]),
   '1L': '#splitline{1L:}{#scale[0.75]{#splitline{Exp.=%.0f#timesSM}{Obs.=%.0f#timesSM}}}'%(data[1][2],data[1][1]),
   '2L': '#splitline{2L:}{#scale[0.75]{#splitline{Exp.=%.0f#timesSM}{Obs.=%.0f#timesSM}}}'%(data[2][2],data[2][1]),
   'comb':'#splitline{Comb.:}{#scale[0.75]{#splitline{Exp.=%.0f#timesSM}{Obs.=%.0f#timesSM}}}'%(data[3][2],data[3][1])
#Luca     '0L' : '0L',
#Luca     '1L' : '1L',
#Luca     '2L' : '2L',
#Luca     'comb' : 'Combined',
}

for idx, line in enumerate(data):

    ycenter = float(nlines) - 0.5 - float(idx)
    print "ADDING " , line
    print "exp centred at x = ", line[1], ", y = ", ycenter

    if line[0] != 'comb':
        if not blind: graphs_obs.SetPoint(graphs_obs.GetN(),       line[1], ycenter)
        else:         graphs_obs.SetPoint(graphs_obs.GetN(),       10000.*xmax, ycenter) 
    else:
        if not blindComb: graphs_obs.SetPoint(graphs_obs.GetN(),       line[1], ycenter)
        else:             graphs_obs.SetPoint(graphs_obs.GetN(),       10000.*xmax, ycenter) 
    graphs_exp.SetPoint(graphs_exp.GetN(),       line[2], ycenter+0.5) ## need to put the point at the top, or dashed line won't be conitnuous
    graphs_2sigma.SetPoint(graphs_2sigma.GetN(), line[2], ycenter)
    graphs_1sigma.SetPoint(graphs_1sigma.GetN(), line[2], ycenter)

    graphs_obs.SetPointError(graphs_obs.GetN()-1,       0,       0,       0.5, 0.5)
    graphs_exp.SetPointError(graphs_exp.GetN()-1,       0,       0,       1, 0)
    graphs_2sigma.SetPointError(graphs_2sigma.GetN()-1, abs(line[3]-line[2]), abs(line[6]-line[2]), 0.5, 0.5)
    graphs_1sigma.SetPointError(graphs_1sigma.GetN()-1, abs(line[4]-line[2]), abs(line[5]-line[2]), 0.5, 0.5)

#### set the styles
graphs_2sigma.SetFillColor(ROOT.kOrange)
graphs_1sigma.SetFillColor(ROOT.kGreen+1)
graphs_2sigma.SetLineColor(ROOT.kOrange)
graphs_1sigma.SetLineColor(ROOT.kGreen+1)
graphs_2sigma.SetFillStyle(1001)
graphs_1sigma.SetFillStyle(1001)

graphs_obs.SetLineColor(ROOT.kBlack)
graphs_exp.SetLineColor(ROOT.kBlue+1)
graphs_exp.SetLineStyle(7)
graphs_obs.SetLineWidth(2)
graphs_exp.SetLineWidth(2)
graphs_obs.SetMarkerColor(ROOT.kBlack)
graphs_exp.SetMarkerColor(ROOT.kBlue+1)
graphs_obs.SetMarkerStyle(8)
graphs_exp.SetMarkerStyle(0)
graphs_obs.SetMarkerSize(1.0)
graphs_exp.SetMarkerSize(0.0)

frame.GetXaxis().SetTitleFont(43)
frame.GetYaxis().SetTitleFont(43)
frame.GetXaxis().SetLabelFont(43)
frame.GetYaxis().SetLabelFont(43)
frame.GetXaxis().SetTitleSize(22.5)
frame.GetYaxis().SetTitleSize(30)
frame.GetXaxis().SetLabelSize(25)
frame.GetYaxis().SetLabelSize(25)
frame.SetTitle(";95% CL on #mu(#sigma_{VH(H#rightarrow c#bar{c})});")

######
## set the bin name
for idx, line in enumerate(data):
    nbin = nlines - idx
    name = line[0]
    frame.GetYaxis().SetBinLabel(nbin, legend[name])

#    frame.GetYaxis().SetBinLabel(nbin, legend[name] if name in legend else name)

    frame.GetYaxis().CenterTitle(True);
    
frame.Draw()
graphs_2sigma.Draw('2same')
graphs_1sigma.Draw('2same')
graphs_exp.Draw('PZsame')
graphs_obs.Draw('PZsame')
ROOT.gPad.Update();
ROOT.gPad.RedrawAxis();
if not logx: redrawBorder()

### in case Run I is plotted, print a line below it
if plot_RunI and add_RunI_line:
    idxRun1 = 0
    for idx, line in enumerate(data):
        if data[0] == 'comb_RunI':
            idxRun1 = idx
            break
    if idxRun1 < len(data):
        ycenter = float(nlines) - 0.5 - float(idxRun1) - 0.5
        line = ROOT.TLine(xmin, ycenter, xmax, ycenter)
        # line.SetLineStyle(7)
        line.SetLineColor(ROOT.kBlack)
        line.SetLineWidth(2)
        line.Draw()

if 'comb' in plotted_lines and add_comb_line:
    ## I assume the combined is always at the bottom
    line2 = ROOT.TLine(xmin, 1, xmax, 1)
    line2.SetLineStyle(7)
    line2.SetLineColor(ROOT.kBlack)
    line2.SetLineWidth(2)
    line2.Draw()

# ## the tlegend
# if twoColLeg:
#     leg = ROOT.TLegend(0.58, 0.85, 0.98, 0.98)
#     leg.SetNColumns(2)
#     leg.SetBorderSize(0)
#     leg.SetFillStyle(0)
#     leg.SetTextFont(43)
#     leg.SetTextSize(18)
#     leg.SetHeader('95% CL upper limits')
#     leg.AddEntry(graphs_obs,"Observed","lp")
#     leg.AddEntry(graphs_1sigma, "68% expected", "f")
#     leg.AddEntry(graphs_exp, "Median expected", "lp")
#     leg.AddEntry(graphs_2sigma, "95% expected", "f")

# else:
if not logx:
    if plot_RunI: leg = ROOT.TLegend(0.58, 0.25, 0.98, 0.39)
    else:         leg = ROOT.TLegend(0.58, 0.28, 0.98, 0.42)
else:
    leg = ROOT.TLegend(0.585351, 0.114839, 0.934849, 0.224516)

leg.SetLineColor(ROOT.kWhite)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(43)
leg.SetTextSize(18)
leg.SetHeader('95% CL upper limits')
leg.AddEntry(graphs_obs,"Observed","lp")
leg.AddEntry(graphs_exp, "Median expected", "lp")
leg.AddEntry(graphs_1sigma, "68% expected", "f")
leg.AddEntry(graphs_2sigma, "95% expected", "f")
leg.Draw()

#### the CMS text
yoffset = (1.5*nlines/100.)

xtext = c1.GetUxmin() if not logx else xmin
CMStext = ROOT.TLatex(xtext, c1.GetUymax() + yoffset, "CMS")
# CMStext.SetNDC(True)
CMStext.SetTextFont(63)
CMStext.SetTextSize(33)
CMStext.Draw()

#### channel text
xtext = c1.GetUxmax()*1 if not logx else xmax
chan_text = ROOT.TLatex(xtext, c1.GetUymax() + yoffset, "pp#rightarrow VH(H#rightarrow c#bar{c})")
# CMStext.SetNDC(True)
chan_text.SetTextColor(4)
chan_text.SetTextAlign(31)
chan_text.SetTextFont(53)
chan_text.SetTextSize(33-6)
chan_text.Draw()


c1.Update()
raw_input()
oname = 'combined_VHcc_SM_plot.pdf' if plot_RunI else 'combined_VHcc_SM_plot_noRunI.pdf'
if logx:
    oname = oname.replace('.pdf', '_logx.pdf')
c1.Print(oname, 'pdf')
