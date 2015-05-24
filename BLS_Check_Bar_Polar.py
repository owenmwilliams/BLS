import csv
import wx
from pylab import *
from string import lower, join
import numpy as np
from matplotlib.pyplot import figure, show, rc
import matplotlib.cm as cm
import os
import re

class BLS_Parse(wx.Frame):

    def __init__(self,parent,id,title):

        wx.Frame.__init__(self,parent,id,title)

        #Set up frame outline
        vert = wx.BoxSizer(wx.VERTICAL)
        top = wx.BoxSizer(wx.HORIZONTAL)

        #Open csv file and populate an array
        OnOpen(self,e)
        self.master_array = listCsv_Array(self, self.filename)

        #Contruct a tree list out of the Occupational data
        self.tree_occ = wx.TreeCtrl(self,size=(600,250), style = wx.TR_HAS_BUTTONS | wx.TR_MULTIPLE | wx.EXPAND)
        self.root = self.tree_occ.AddRoot("All Occupations")
        treeOccupationBox(self, self.master_array)

        #Construct a tree list out of the Territorial data
        self.tree_terr = wx.TreeCtrl(self,size=(600,250), style = wx.TR_HAS_BUTTONS | wx.TR_MULTIPLE)
        self.root2 = self.tree_terr.AddRoot("All Territories")
        treeTerritoryBox(self, self.master_array)

        #Button with calculate functionality
        calculate_button = wx.Button(self, wx.ID_ANY, "Calculate Data")
        calculate_button.Bind(wx.EVT_BUTTON, self.Calculate)

        #Organize frame elements
        top.Add(self.tree_occ, 1, wx.EXPAND)
        top.Add(self.tree_terr, 1, wx.EXPAND)
        vert.Add(top, 0, wx.EXPAND)
        vert.Add(calculate_button, 0, wx.EXPAND) 
        self.SetSizer(vert)
        self.Fit()
        self.Centre()

    def Calculate(self, event):
        #Get Occupation selections and populate a list
        item_occ = self.tree_occ.GetSelections()
        self.calc_occ_list = listSetup(self, item_occ, self.tree_occ)

        #Get Territory selections and populate a list
        item_terr = self.tree_terr.GetSelections()
        self.calc_terr_list = listSetup(self, item_terr, self.tree_terr)
                
        if self.calc_occ_list != [] and self.calc_terr_list != []:
            #Generate the lists to be used for charts
            chart, other_chart = listGenerateCharts(self, self.calc_occ_list, self.calc_terr_list)

            #Sort the lists generated
            sorted_chart = chart
            sorted_other_chart = other_chart

            #Generate the charts
            figure = GenerateFigure(self, sorted_chart)
            figure.savefig('current.png')
            if sorted_other_chart != []:
                figure_other = GenerateFigure(self, sorted_other_chart)
                figure_other.savefig('current_other.png')
    
def treeOccupationBox(self, array):
        self.SOC_major = []
        count = 11
        while count < 56:
            current = []
            list_value = ((count - 9)/2) - 1
            for i in range(len(array)):
                test_code = str(array[i][3])
                test_code2 = test_code[0:2]
                test_code3 = test_code[3:7]
                count_code = str(count) 
                if test_code3 == '0000' and test_code2 == count_code:
                    if array[i][4] not in self.SOC_major:
                        self.SOC_major.append(array[i][4])
                        self.current_major = self.tree_occ.AppendItem(self.root, array[i][4])
                elif test_code2 == count_code:
                    if array[i][4] not in current:
                        current.append(str(array[i][4]))
                        self.tree_occ.AppendItem(self.current_major, array[i][4])            
            count = count + 2

def treeTerritoryBox(self, array):
        self.terr_list = []
        for i in range(1, len(array)):
            if array[i][2] not in self.terr_list:
                self.terr_list.append(array[i][2])
        for i in range(len(self.terr_list)):
            self.tree_terr.AppendItem(self.root2,self.terr_list[i])

def listSetup(self, selections, tree):
        list_select = []
        for selection in range(len(selections)):
            list_select.append(tree.GetItemText(selections[selection]))
            
        if list_select == []:
            wx.MessageBox('Not enough selections','Error', style = wx.OK)
            
        else:
            for i in range(len(selections)):
                if selections[i] != self.root and selections[i] != self.root2:
                    parents_cull = tree.GetItemParent(selections[i])
                    if tree.GetItemText(parents_cull) in list_select:
                        wx.MessageBox('Category and Subcategory in Same List','Error', style = wx.OK)
                        self.proceed = False
                        return []
                        break
                    else:
                        self.proceed = True
                else:
                    if len(list_select) != 1:
                        wx.MessageBox('Category and Subcategory in Same List','Error', style = wx.OK)
                        self.proceed = False
                        return []
                        break
                    else:
                        self.proceed = True
                        
        if self.proceed == True:
            return list_select

def listGenerateCharts(self, list_2, list_1):

    total_unaccounted = []
    no_data = []
    percentages = []
    labels = []
    explode = []
        
    for i in range(len(list_1)):
        for j in range(len(list_2)):
            for k in range(len(self.master_array)):    
                if list_1[i] == self.master_array[k][2] and list_2[j] == self.master_array[k][4]:
                    if self.master_array[k][6] == '**':
                        no_data.append(self.master_array[j][2])
                        no_data.append(self.master_array[j][4])
                    elif self.master_array[k][4] not in labels:
                        if self.master_array[k][10] == '*'or self.master_array[k][10] == '#':
                            explode.append(0)
                            percentages.append(int(self.master_array[k][6]))
                            labels.append(self.master_array[k][4])
                        else:
                            percentages.append(int(self.master_array[k][6]))
                            labels.append(self.master_array[k][4])
                            explode.append(int(self.master_array[k][10]))
                    else:
                        for h in range(len(labels)):
                            if self.master_array[k][4] == labels[h]:
                                percentages[h] = percentages[h] + int(self.master_array[k][6])
                                if self.master_array[k][10] != '*' and self.master_array[k][10] != '#':
                                    if explode[h] == 0:
                                        explode[h] = int(self.master_array[k][10])
                                    else:
                                        explode[h] = (explode[h] + int(self.master_array[k][10]))/2
                                            
    perc_final = CalculatePercentages(self, percentages)

    main_list, other_list = SeparateMain_Other(self, perc_final, explode, labels)
   
    return main_list, other_list

def CalculatePercentages(self, perc_list):
    percentages_list = []
    total = sum(perc_list)
    for i in range(len(perc_list)):
        employed = float(perc_list[i])
        curr_perc = (employed/total*100)
        percentages_list.append(round(curr_perc, 2))
    return percentages_list
    
def SeparateMain_Other(self, list_1, list_2, list_3):
    other_perc = []
    other_labels = []
    other_explode = []
    main_perc = []
    main_labels = []
    main_explode = []
    for i in range(len(list_1)):
        curr_label = list_3[i]
        curr_explode = list_2[i]
        if list_1[i] <= 1.25:
            other_perc.append(list_1[i])
            other_explode.append(list_2[i])
            other_labels.append(list_3[i])
        else:
            main_perc.append(list_1[i])
            main_explode.append(list_2[i])
            main_labels.append(list_3[i])
    if len(other_perc) <= 5:
        for item in range(len(other_perc)):
            main_perc.append(other_perc[item])
            main_explode.append(other_explode[item])
            main_labels.append(other_labels[item])
        other_perc = []
        other_labels = []
        other_explode = []    
    elif other_perc != []:
        main_perc.append(round(sum(other_perc),2))
        main_explode.append(round(float(sum(other_explode)/len(other_explode))))
        main_labels.append("Others")
        other_sum = sum(other_perc)
        for i in range(len(other_perc)):
            other_perc[i] = round(float(other_perc[i]/other_sum*100), 2)
    main = zip(main_perc, main_labels, main_explode)
    other = zip(other_perc, other_labels, other_explode)

    return main, other

def listChartSort(self, array):
    sort_1 = sorted(array, key=lambda perc: perc[0])
    final_sort = []
    length = len(sort_1)-1
    for i in range(len(sort_1)/2):
        final_sort.append(sort_1[i])
        curr = length - i
        final_sort.append(sort_1[curr])
    if len(sort_1) % 2 != 0:
        final_sort.append(sort_1[len(sort_1)/2])

    return final_sort

def GenerateFigure(self, given_list):
    color = []
    for i in range(len(given_list)):
        current = round(given_list[i][2],1)
        float_curr = float(current/1000000)
        color.append(float_curr)
    start = 0
    theta = []
    radii = []
    width = []
    for i in range(len(given_list)):
        theta.append(start)
        if given_list[i][2] == 0:
            radii.append(0)
        else:
            radii.append(given_list[i][2])
        curr_wid = given_list[i][0]/100*2*np.pi
        width.append(curr_wid)
        start = start + curr_wid

    figwidth = 45.0
    figheight = 45.0
    fig = figure(figsize=(figwidth, figheight))
                
    ax = fig.add_axes([0.2,0.2,0.55,0.55], polar = True, aspect = 'equal')
    ax.axis('off')

    for i in range(len(given_list)):
            ax.annotate(given_list[i], xy = [theta[i]+float(width[i]/2), max(radii)], size = float(given_list[i][0]/2)+18.0, rotation = int((theta[i]+float(width[i]/2))/(2*np.pi)*360), va='center', ha='center')
    bars = ax.bar(theta, radii, width=width, bottom =0.0)
    for r,bar in zip(color, bars):
        bar.set_alpha(0.5)
        bar.set_facecolor(cm.jet(r/0.1))
    return fig

def listCsv_Array(self, csvFILE):
    bls_data = csv.reader(open(csvFILE, "rb"), delimiter = ';', quotechar = '"')

    self.master_list = []
    for row in bls_data:
        for cell in range(len(row)):
            self.master_list.append(row[cell])

    self.master_array = []
    i = 0
    j = 22
    while j < len(self.master_list)+1:
        current = []
        for k in range(i,j):
            current.append(self.master_list[k])
        self.master_array.append(current)
        i = i + 22
        j = j + 22

    return self.master_array

def OnOpen(self,e):
    """ Open a file"""
    self.dirname = ''
    dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
        self.filename = dlg.GetFilename()
        self.dirname = dlg.GetDirectory()
    dlg.Destroy()

class MyApp(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        
        # This catches events when the app is asked to activate by some other
        # process
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)
        
    def OnInit(self):
        frame = BLS_Parse(None,-1,'BLS Data Parsing')
        frame.Show(True)
        frame.Centre
        return True

    def BringWindowToFront(self):
        try: # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass

    def OnActivate(self, event):
        # if this is an activate event, rather than something else, like iconize.
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()

app = MyApp(False)
app.MainLoop()
