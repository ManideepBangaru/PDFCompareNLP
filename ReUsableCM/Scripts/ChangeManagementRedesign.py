# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 12:55:33 2019

@author: 760406
"""

#%reset -f

# importing all the required modules
import PyPDF2
import pandas as pd
import numpy as np
import re
import copy
import os
import datetime
import subprocess
import fitz
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import rpy2.robjects as robjects

r = robjects.r

LoansNotRun = []

g = globals()

RPath = 'C:/Program Files/R/R-3.5.2/bin/'
MPath = 'D:/Projects/ReUsableCM/'
ScriptsPath = '%sScripts/'%MPath
PrePath = '%sInput_pre/'%MPath
PostPath = '%sInput_post/'%MPath
ExtractedpdfsPath = '%sPDFsExtracted/'%MPath
output = '%sResults/'%MPath
summaryPath = '%sSummaries/'%MPath

fileNameBfr = PrePath + '85304012_Pre_Modification.pdf'
fileNameAfr = PostPath + '85304012_Post_Modification.pdf'
B = '85304012'

#Removing page 1 0f 1 from text
regex1 = r"([a-zA-Z]+) (\d+) ([a-zA-Z]+) (\d+)"
regex2 = r"(\(([a-zA-Z]+) (\d+) ([a-zA-Z]+) (\d+)\))"
regex3 = r"(\( ([a-zA-Z]+) (\d+) ([a-zA-Z]+) (\d+) \))"
regex4 = r"(\d+) Page ([a-zA-Z]+) (\d+)"
    
def MatchReg(page):
    try:
        re.search(regex2,page).end()
        match = re.search(regex2,page)
        starting = match.start()
        ending = match.end()
    except:
            try:
                re.search(regex3,page).end()
                match = re.search(regex3,page)
                starting = match.start()
                ending = match.end()
            except:
                try:
                    re.search(regex4,page).end()
                    match = re.search(regex4,page)
                    starting = match.start()
                    ending = match.end()
                except:
                    match = re.search(regex1,page)
                    starting = match.start()
                    ending = match.end()
    return starting,ending

def PageCorrectionList1(Page):
    temp = Page.split('.')
    for rot in range(len(temp)):
        temp[rot] = temp[rot].strip()
        if rot == 0:
            pass
        elif len(temp[rot])==1:
            temp[rot-1] = temp[rot-1]+'.'+temp[rot]
            temp[rot] = ''
    temp = [i for i in temp if i]
    return temp

def PageCorrectionList2(page):
    global tempList,lis
    tempList = page.strip().split('.')
    tempList = [i.strip() for i in tempList]
    tempList = [i for i in tempList if i]
    lis = []
    while len(tempList) != 0:
        if len(tempList[0].split(' '))>1:
            lis.append(tempList[0])
            tempList.pop(0)
        elif len(lis) == 0:
            lis = [tempList[0]]
            tempList.pop(0)
        else:
            lis[len(lis)-1] = lis[len(lis)-1] + '.' + tempList[0]
            tempList.pop(0)
    lis = [ele.strip() for ele in lis]
    return lis

def check(sentence,Page2):
    if sentence in Page2:
        return 1
    else:
        return 0

def splitPageFinder1(df):
    global MatchPageNum
    finlis = []
    for i in range(len(df)):
        actpage = df['PageBfr'].iloc[i]
        bfrpage = actpage-1
        afrpage = actpage+1
        
        actpageContents = PageCorrectionList2(g['bfr_%s'%actpage])
        bfrpageContents = PageCorrectionList2(g['afr_%s'%bfrpage])
        afrpageContents = PageCorrectionList2(g['afr_%s'%afrpage])
        
        bfrCntlis = [1 if i in bfrpageContents else 0 for i in actpageContents]
        afrCntlis = [1 if i in afrpageContents else 0 for i in actpageContents]
        
        try:
            bfrPer = len(bfrCntlis)/sum(bfrCntlis)
        except:
            bfrPer = 0
            
        try:
            afrPer = len(afrCntlis)/sum(afrCntlis)
        except:
            afrPer = 0
        
        if bfrPer>afrPer:
            MatchPageNum = bfrpage
        elif afrPer>bfrPer:
            MatchPageNum = afrpage
        else:
            MatchPageNum = 'NotFound'
        
        finlis.append(MatchPageNum)
    return finlis

def splitPageFinder2(df):
    global MatchPageNum
    finlis = []
    for i in range(len(df)):
        actpage = df['PageAfr'].iloc[i]
        bfrpage = actpage-1
        afrpage = actpage+1
        
        actpageContents = PageCorrectionList2(g['afr_%s'%actpage])
        bfrpageContents = PageCorrectionList2(g['bfr_%s'%bfrpage])
        afrpageContents = PageCorrectionList2(g['bfr_%s'%afrpage])
        
        bfrCntlis = [1 if i in bfrpageContents else 0 for i in actpageContents]
        afrCntlis = [1 if i in afrpageContents else 0 for i in actpageContents]
        
        try:
            bfrPer = len(bfrCntlis)/sum(bfrCntlis)
        except:
            bfrPer = 0
            
        try:
            afrPer = len(afrCntlis)/sum(afrCntlis)
        except:
            afrPer = 0
        
        if bfrPer>afrPer:
            MatchPageNum = bfrpage
        elif afrPer>bfrPer:
            MatchPageNum = afrpage
        else:
            MatchPageNum = 'NotFound'
        
        finlis.append(MatchPageNum)
    return finlis

def splitPageFinder(df):
    global MatchPageNum
    finlis = []
    for i in range(len(df)):
        actpage = df['PageBfr'].iloc[i]
        bfrpage = actpage-1
        afrpage = actpage+1
        
        actpageContents = PageCorrectionList2(g['bfr_%s'%actpage])
        bfrpageContents = PageCorrectionList2(g['afr_%s'%bfrpage])
        afrpageContents = PageCorrectionList2(g['afr_%s'%afrpage])
        
        bfrCntlis = [1 if i in bfrpageContents else 0 for i in actpageContents]
        afrCntlis = [1 if i in afrpageContents else 0 for i in actpageContents]
        
        try:
            bfrPer = len(bfrCntlis)/sum(bfrCntlis)
        except:
            bfrPer = 0
            
        try:
            afrPer = len(afrCntlis)/sum(afrCntlis)
        except:
            afrPer = 0
        
        if bfrPer>afrPer:
            MatchPageNum = bfrpage
        elif afrPer>bfrPer:
            MatchPageNum = afrpage
        else:
            MatchPageNum = 'NotFound'
        
        finlis.append(MatchPageNum)
    return finlis

def Highlighter1(openFileName,PageNum,Text,outputPath,OutputFileName,LoanNumber):
    doc = fitz.open(openFileName)
    page = doc[PageNum-1]
    if len(page.searchFor(Text,hit_max=1000)) != 0:
        return 0,page.searchFor(Text,hit_max=1000)
    else:
        return 1,None

def cleanFlag(text):
    if text.find('[[[') >= 0:
        return 1
    else:
        return 0

def listThrower(text):
    global lisCnt
    remTextList = []
    lisCnt = 0    
    while len(page.searchFor(text,hit_max=1000)) == 0 and lisCnt<=100:
        lisCnt = lisCnt + 1
        wordsList = text.split(' ')
        wordsListAfrRm = wordsList[:-1]
        text = ' '.join(wordsListAfrRm)
        remTextList = remTextList + (wordsList[-1:])
    remTextList.reverse()
    try:
        if remTextList[0] in ["*"]:
            remTextList = remTextList[1:]
        elif remTextList[0].find("(\x93") >= 0:
            remTextList = remTextList[1:]
        elif remTextList[0].find("$") >= 0:
            if remTextList[0][remTextList[0].find("$")-1] == '.' :
                remTextList[0] = remTextList[0][:remTextList[0].find("$")] + ' ' + remTextList[0][remTextList[0].find("$")+1:]
        elif remTextList[0][-2] == '.':
            remTextList[0] = remTextList[0][0:-2]    
    except:
        remTextList = []
    leftOverText = ' '.join(remTextList)
    return text,leftOverText


try:
    RPath = 'C:/Program Files/R/R-3.5.2/bin/'
    MPath = 'D:/Projects/ReUsableCM/'
    ScriptsPath = '%sScripts/'%MPath
    PrePath = '%sInput_pre/'%MPath
    PostPath = '%sInput_post/'%MPath
    ExtractedpdfsPath = '%sPDFsExtracted/'%MPath
    output = '%sResults/'%MPath
    
#    args = [fileNameBfr,fileNameAfr,ExtractedpdfsPath,B,'1']
#    subprocess.call(["%srscript.exe"%RPath, "%spdfreader.R"%ScriptsPath] + args,shell=True)
    
    robjects.globalenv['args'] = robjects.vectors.StrVector([fileNameBfr,fileNameAfr,ExtractedpdfsPath,B,'1'])
    r.source(ScriptsPath + "pdfreader.R")
    
    PDFextract = pd.read_csv('%s%s_%sExtracted.csv'%(ExtractedpdfsPath,B,'1'),encoding = 'unicode_escape')
    
    BfrPages = len(PDFextract[pd.isnull(PDFextract['textBfr'])!=True])
    AfrPages = len(PDFextract[pd.isnull(PDFextract['textAfr'])!=True])
    
    for i in range(len(PDFextract['textBfr'])):
        try:
            g['bfr_%s'%(i+1)] = PDFextract['textBfr'].iloc[i]
            g['bfr_%s'%(i+1)] = copy.deepcopy(g['bfr_%s'%(i+1)].replace('\r\r\n',' '))
            g['bfr_%s'%(i+1)] = ' '.join(g['bfr_%s'%(i+1)].split())
            g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)].strip()
            try:
                barCodeIdentify = re.search(r'\*%s(.*)?\* \*.*?\* (\d+) (\d+)/(\d+)'%B,g['bfr_%s'%(i+1)])
                g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)][:barCodeIdentify.start()].strip()
                del barCodeIdentify
            except:
                try:
                    barCodeIdentify = re.search(r'\*%s(.*)?\* \*.*?\*'%B,g['bfr_%s'%(i+1)])
                    g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)][:barCodeIdentify.start()].strip()
                    del barCodeIdentify
                except:
                    pass
                
            g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)].replace('',"'")
            g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)].replace('\x95','')
        except:
            pass
    
    for i in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()):
        try:
            g['afr_%s'%(i+1)] = PDFextract['textAfr'].iloc[i]
            g['afr_%s'%(i+1)] = copy.deepcopy(g['afr_%s'%(i+1)].replace('\r\r\n',' '))
            g['afr_%s'%(i+1)] = ' '.join(g['afr_%s'%(i+1)].split())
            g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)].strip()
            try:
                barCodeIdentify = re.search(r'\*%s(.*)?\* \*.*?\* (\d+) (\d+)/(\d+)'%B,g['afr_%s'%(i+1)])
                g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)][:barCodeIdentify.start()].strip()
                del barCodeIdentify
            except:
                try:
                    barCodeIdentify = re.search(r'\*%s(.*)?\* \*.*?\*'%B,g['afr_%s'%(i+1)])
                    g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)][:barCodeIdentify.start()].strip()
                    del barCodeIdentify
                except:
                    pass
                
            g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)].replace('',"'")
            g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)].replace('\x95','')
        except:
            pass
    
    docpage = ['afr_%s'%(i+1) for i in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum())]
    pagenum = [i+1 for i in range(len(docpage))]
    afr_df = pd.DataFrame({'DocPageNameAfr':docpage,'TextAfr':None,'PageNumAfr':pagenum})
    for i in range(len(afr_df)):
        afr_df['TextAfr'].iloc[i] = g['afr_%s'%(i+1)]
    
    docpage = ['bfr_%s'%(i+1) for i in range(len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum())]
    pagenum = [i+1 for i in range(len(docpage))]
    bfr_df = pd.DataFrame({'DocPageNameBfr':docpage,'TextBfr':None,'PageNumBfr':pagenum})
    for i in range(len(bfr_df)):
        bfr_df['TextBfr'].iloc[i] = g['bfr_%s'%(i+1)] 

    PageAfr = []
    PageBfr = []
    MatchinPerc = []
    for i in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()):
        for j in range(len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum()):
            print(i,j)
            PageAfr.append(i)
            PageBfr.append(j)
            vect = TfidfVectorizer(min_df=1)
            tfidf = vect.fit_transform([afr_df['TextAfr'].iloc[i],bfr_df['TextBfr'].iloc[j]])
            MatchMatrix = (tfidf * tfidf.T).A
            MatchinPerc.append(MatchMatrix[0][1])

    MatchMatrixdf = pd.DataFrame({'PageAfr':PageAfr,'PageBfr':PageBfr,'Perc':MatchinPerc})
    MatchMatrixdf['PageAfr'] = MatchMatrixdf['PageAfr'] + 1 
    MatchMatrixdf['PageBfr'] = MatchMatrixdf['PageBfr'] + 1
    
    PageAfr = []
    PageBfr = []
    MatchinPerc = []
    TakenPage = []
    PagesConsd = np.unique(MatchMatrixdf['PageAfr'])
    for i in range(len(PagesConsd)):
        if i<150:
            temp = MatchMatrixdf[(MatchMatrixdf['PageAfr'] == PagesConsd[i])]
            temp = temp[~temp['PageBfr'].isin(TakenPage)]
            PageAfr.append(PagesConsd[i])
            try:
                if max(temp['Perc']) < 0.60:
                    PageBfr.append(None)
                    MatchinPerc.append(None)
                else:
                    if PagesConsd[i] == temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0]:
                        PageBfr.append(temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0])
                        MatchinPerc.append(temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0])
                        TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0])
                    else:
                        tempMatch = temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0]
                        tempMatchPerc = temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0]
                        RestTemp = MatchMatrixdf[(MatchMatrixdf['PageBfr'] > PagesConsd[i])]
                        RestTemp = RestTemp[RestTemp['PageBfr']==tempMatch]
                        ExpMatch = RestTemp[(RestTemp['PageBfr'] == tempMatch) & (RestTemp['PageBfr'] == tempMatch)]['Perc'].iloc[0]
                        ExpMatchPerc = RestTemp[(RestTemp['PageAfr'] == tempMatch) & (RestTemp['PageBfr'] == tempMatch)]['Perc'].iloc[0]
                        try:
                            if ExpMatchPerc > tempMatchPerc:
                                if PagesConsd[i] not in TakenPage:
                                    PageBfr.append(PagesConsd[i])
                                    MatchinPerc.append(temp[temp['PageBfr'] == PagesConsd[i]]['Perc'].iloc[0])
                                    TakenPage.append(PagesConsd[i])
                            else:
                                PageBfr.append(temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0])
                                MatchinPerc.append(temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0])
                                TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0])
                        except:
                            PageAfr.append(tempMatch)
                            MatchinPerc.append(tempMatchPerc)
                            TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
            except:
                PageBfr.append(None)
                MatchinPerc.append(None)
        else:
            break

    FinalMatchPage = pd.DataFrame({'PageAfr':PageAfr,'PageBfr':PageBfr,'MathPerc':MatchinPerc})
    
    
    PageAfr = []
    PageBfr = []
    MatchinPerc = []
    for i in range(len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum()):
        for j in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()):
            print(i,j)
            PageBfr.append(i)
            PageAfr.append(j)
            vect = TfidfVectorizer(min_df=1)
            tfidf = vect.fit_transform([bfr_df['TextBfr'].iloc[i],afr_df['TextAfr'].iloc[j]])
            MatchMatrix = (tfidf * tfidf.T).A
            MatchinPerc.append(MatchMatrix[0][1])

    MatchMatrixdf2 = pd.DataFrame({'PageBfr':PageBfr,'PageAfr':PageAfr,'Perc':MatchinPerc})
    MatchMatrixdf2['PageBfr'] = MatchMatrixdf2['PageBfr'] + 1 
    MatchMatrixdf2['PageAfr'] = MatchMatrixdf2['PageAfr'] + 1
        
    PageAfr = []
    PageBfr = []
    MatchinPerc = []
    TakenPage = []
    PagesConsd = np.unique(MatchMatrixdf2['PageBfr'])
    for i in range(len(PagesConsd)):
        if i<150:
            temp = MatchMatrixdf2[(MatchMatrixdf2['PageBfr'] == PagesConsd[i])]
            temp = temp[~temp['PageAfr'].isin(TakenPage)]
            PageBfr.append(PagesConsd[i])
            try:
                if max(temp['Perc']) < 0.60:
                    PageAfr.append(None)
                    MatchinPerc.append(None)
                else:
                    if PagesConsd[i] == temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0]:
                        PageAfr.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
                        MatchinPerc.append(temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0])
                        TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
                    else:
                        tempMatch = temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0]
                        tempMatchPerc = temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0]
                        RestTemp = MatchMatrixdf[(MatchMatrixdf['PageAfr'] > PagesConsd[i])]
                        RestTemp = RestTemp[RestTemp['PageAfr']==tempMatch].reset_index(drop=True)
                        try:
                            ExpMatch = RestTemp[(RestTemp['PageBfr'] == tempMatch) & (RestTemp['PageAfr'] == tempMatch)]['PageAfr'].iloc[0]
                            ExpMatchPerc = RestTemp[(RestTemp['PageBfr'] == tempMatch) & (RestTemp['PageAfr'] == tempMatch)]['Perc'].iloc[0]
                            if ExpMatchPerc > tempMatchPerc:
                                if PagesConsd[i] not in TakenPage:
                                    PageAfr.append(PagesConsd[i])
                                    MatchinPerc.append(temp[temp['PageAfr'] == PagesConsd[i]]['Perc'].iloc[0])
                                    TakenPage.append(PagesConsd[i])
                            else:
                                PageAfr.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
                                MatchinPerc.append(temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0])
                                TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
                        except:
                            PageAfr.append(tempMatch)
                            MatchinPerc.append(tempMatchPerc)
                            TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
            except:
                PageAfr.append(None)
                MatchinPerc.append(None)
        else:
            break

    FinalMatchPage2 = pd.DataFrame({'PageBfr':PageBfr,'PageAfr':PageAfr,'MathPerc':MatchinPerc})
    
    tempDielamma = FinalMatchPage2[FinalMatchPage2['PageAfr'].isnull()==True]
    try:
        splitList = splitPageFinder(tempDielamma)
        tempDielamma['SplitPage'] = splitList
    except:
        pass
    
    if len(tempDielamma) > 0:
        try:
            if len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum() < len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum():
                FinalMatchPage = pd.merge(FinalMatchPage,tempDielamma[['PageBfr','SplitPage']],left_on=['PageAfr'],right_on = ['SplitPage'],how='left')
                del FinalMatchPage['SplitPage']
                FinalMatchPage.rename(columns={'PageBfr_x':'PageBfr','PageBfr_y':'SplitPage'},inplace=True)
        except:
            pass
        

    FinalDecisionDF = pd.DataFrame({'PageSentence':[0],'PageAfr':[0],'decision':[0]})
    
    for sd in range(len(FinalMatchPage['PageAfr'])):
        try:
            if sd==0:
                g['afr_%s'%(sd+1)] = g['afr_%s'%(sd+1)].strip()
            if sd!=0:
                g['afr_%s'%(sd+1)] = g['afr_%s'%(sd+1)].strip() 
                if len(g['afr_%s'%(sd+1)].split('.')[0].split(' ')) == 1:# and len(g['afr_%s'%(sd+1)].split('.')[0].split(' ')[0])==1:
                    g['afr_%s'%(sd)] = g['afr_%s'%(sd)] +  str(g['afr_%s'%(sd+1)].split('.')[0].split(' ')[0]) + '.'
#                else:
#                    g['afr_%s'%(sd)] = g['afr_%s'%(sd)] + ' ' + str(g['afr_%s'%(sd+1)].split('.')[0].split(' ')[0]) + '.'
        except:
            pass
    
    for sd in range(len(FinalMatchPage['PageBfr'])):
        try:
            if sd==0:
                g['bfr_%s'%(sd+1)] = g['bfr_%s'%(sd+1)].strip()
            if sd!=0:
                g['bfr_%s'%(sd+1)] = g['bfr_%s'%(sd+1)].strip() 
                if len(g['bfr_%s'%(sd+1)].split('.')[0].split(' ')) == 1:# and len(g['bfr_%s'%(sd+1)].split('.')[0].split(' ')[0])==1:
                    g['bfr_%s'%(sd)] = g['bfr_%s'%(sd)] +  str(g['bfr_%s'%(sd+1)].split('.')[0].split(' ')[0]) + '.'
#                else:
#                    g['bfr_%s'%(sd)] = g['bfr_%s'%(sd)] + ' ' + str(g['bfr_%s'%(sd+1)].split('.')[0].split(' ')[0]) + '.'
        except:
            pass
        

    try:
        len(FinalMatchPage['SplitPage'])
        for i,j,k in zip(FinalMatchPage['PageAfr'],FinalMatchPage['PageBfr'],FinalMatchPage['SplitPage']):
            try:
                i = int(i)
                if (np.isnan(j) != True):
                    j = int(j)
                    MasterAfr = PageCorrectionList2(g['afr_%s'%i])
                    MasterBfr = PageCorrectionList2(g['bfr_%s'%j])
                    
                    if len(MasterAfr[0].split(' ')) == 1:
                        MasterAfr.pop(0)
                    if len(MasterBfr[0].split(' ')) == 1:
                        MasterBfr.pop(0)
                    
                    g['MasterAfr_%s'%i] = PageCorrectionList2(g['afr_%s'%i])
                    g['MasterBfr_%s'%j]= PageCorrectionList2(g['bfr_%s'%j])
                    
                    if len(g['MasterAfr_%s'%i][0].split(' ')) == 1:
                        g['MasterAfr_%s'%i].pop(0)
                    if len(g['MasterAfr_%s'%i][0].split(' ')) == 1:
                        g['MasterAfr_%s'%i].pop(0)
                    
                    
                    if i==1:
                        MasterAfrAfr = PageCorrectionList2(g['afr_%s'%(i+1)])
                        MasterAfrAfrT = [''.join(i.split()) for i in MasterAfrAfr]
                    elif (i>1) and (i<len(MasterAfr)-1) :
                        MasterAfrAfr = PageCorrectionList2(g['afr_%s'%(i+1)])
                        MasterAfrAfrT = [''.join(i.split()) for i in MasterAfrAfr]
                        MasterAfrBfr = PageCorrectionList2(g['afr_%s'%(i-1)])
                        MasterAfrBfrT = [''.join(i.split()) for i in MasterAfrBfr]
                    else:
                        MasterAfrBfr = PageCorrectionList2(g['afr_%s'%(i-1)])
                        MasterAfrBfrT = [''.join(i.split()) for i in MasterAfrBfr]
                    
                    if j==1:
                        MasterBfrAfr = PageCorrectionList2(g['bfr_%s'%(j+1)])
                        MasterBfrAfrT = [''.join(i.split()) for i in MasterBfrAfr]
                    elif (j>1) and (j<len(MasterBfr)-1) :
                        MasterBfrAfr = PageCorrectionList2(g['bfr_%s'%(j+1)])
                        MasterBfrAfrT = [''.join(i.split()) for i in MasterBfrAfr]
                        MasterBfrBfr = PageCorrectionList2(g['bfr_%s'%(j-1)])
                        MasterBfrBfrT = [''.join(i.split()) for i in MasterBfrBfr]
                    else:
                        MasterBfrBfr = PageCorrectionList2(g['bfr_%s'%(j-1)])
                        MasterBfrBfrT = [''.join(i.split()) for i in MasterBfrBfr]
                    
                    MasterAfrT = [''.join(i.split()) for i in MasterAfr]
                    MasterBfrT = [''.join(i.split()) for i in MasterBfr]
                                
                    if i==1 and j==1: 
                        res1 = [check(conAfr,MasterBfrT) for conAfr in MasterAfrT]
                        res2 = [check(conAfr,MasterBfrAfrT) for conAfr in MasterAfrT]
                        res = ['Matched' if ress>0 else 'NotMatched' for ress in list(np.array(res1)+np.array(res2))]
                        temp = pd.DataFrame({'PageSentence':MasterAfr,'PageAfr':i,'decision':res})
                        FinalDecisionDF = pd.concat([FinalDecisionDF,temp],axis=0).reset_index(drop=True)
                        FinalDecisionDF = FinalDecisionDF.loc[1:]
                    else:
                        res1 = [check(conAfr,MasterBfrT) for conAfr in MasterAfrT]    
                        res2 = [check(conAfr,MasterBfrBfrT) for conAfr in MasterAfrT]
                        res3 = [check(conAfr,MasterBfrAfrT) for conAfr in MasterAfrT]
                        res = ['Matched' if ress>0 else 'NotMatched' for ress in list(np.array(res1)+np.array(res2)+np.array(res3))]
                        temp = pd.DataFrame({'PageSentence':MasterAfr,'PageAfr':i,'decision':res})
                        FinalDecisionDF = pd.concat([FinalDecisionDF,temp],axis=0).reset_index(drop=True)
                else:
                    MasterAfr = PageCorrectionList2(g['afr_%s'%i])
                    temp = pd.DataFrame({'PageSentence':MasterAfr,'PageAfr':i,'decision':'Newly Added Page'})
                    FinalDecisionDF = pd.concat([FinalDecisionDF,temp],axis=0).reset_index(drop=True)
            except:
                pass
        FinalDecisionDF = FinalDecisionDF.reset_index(drop=True)    
    except:
        for i,j in zip(FinalMatchPage['PageAfr'],FinalMatchPage['PageBfr']):
            try:
                i = int(i)
                if (np.isnan(j) != True):
                    j = int(j)
                    MasterAfr = PageCorrectionList2(g['afr_%s'%i])
                    MasterBfr = PageCorrectionList2(g['bfr_%s'%j])
                    
                    g['MasterAfr_%s'%i] = PageCorrectionList2(g['afr_%s'%i])
                    g['MasterBfr_%s'%j]= PageCorrectionList2(g['bfr_%s'%j])
                    
                    if len(MasterAfr[0].split(' ')) == 1:
                        MasterAfr.pop(0)
                    if len(MasterBfr[0].split(' ')) == 1:
                        MasterBfr.pop(0)
                    
                    g['MasterAfr_%s'%i] = PageCorrectionList2(g['afr_%s'%i])
                    g['MasterBfr_%s'%j]= PageCorrectionList2(g['bfr_%s'%j])
                    
                    if len(g['MasterAfr_%s'%i][0].split(' ')) == 1:
                        g['MasterAfr_%s'%i].pop(0)
                    if len(g['MasterAfr_%s'%i][0].split(' ')) == 1:
                        g['MasterAfr_%s'%i].pop(0)
                    
                    if i==1:
                        MasterAfrAfr = PageCorrectionList2(g['afr_%s'%(i+1)])
                        MasterAfrAfrT = [''.join(i.split()) for i in MasterAfrAfr]
                    elif (i>1) and (i<len(MasterAfr)-1) :
                        MasterAfrAfr = PageCorrectionList2(g['afr_%s'%(i+1)])
                        MasterAfrAfrT = [''.join(i.split()) for i in MasterAfrAfr]
                        MasterAfrBfr = PageCorrectionList2(g['afr_%s'%(i-1)])
                        MasterAfrBfrT = [''.join(i.split()) for i in MasterAfrBfr]
                    else:
                        MasterAfrBfr = PageCorrectionList2(g['afr_%s'%(i-1)])
                        MasterAfrBfrT = [''.join(i.split()) for i in MasterAfrBfr]
                    
                    if j==1:
                        MasterBfrAfr = PageCorrectionList2(g['bfr_%s'%(j+1)])
                        MasterBfrAfrT = [''.join(i.split()) for i in MasterBfrAfr]
                    elif (j>1) and (j<len(MasterBfr)-1) :
                        MasterBfrAfr = PageCorrectionList2(g['bfr_%s'%(j+1)])
                        MasterBfrAfrT = [''.join(i.split()) for i in MasterBfrAfr]
                        MasterBfrBfr = PageCorrectionList2(g['bfr_%s'%(j-1)])
                        MasterBfrBfrT = [''.join(i.split()) for i in MasterBfrBfr]
                    else:
                        MasterBfrBfr = PageCorrectionList2(g['bfr_%s'%(j-1)])
                        MasterBfrBfrT = [''.join(i.split()) for i in MasterBfrBfr]
                    
                    MasterAfrT = [''.join(i.split()) for i in MasterAfr]
                    MasterBfrT = [''.join(i.split()) for i in MasterBfr]
                                
                    if i==1 and j==1: 
                        res1 = [check(conAfr,MasterBfrT) for conAfr in MasterAfrT]
                        res2 = [check(conAfr,MasterBfrAfrT) for conAfr in MasterAfrT]
                        res = ['Matched' if ress>0 else 'NotMatched' for ress in list(np.array(res1)+np.array(res2))]
                        temp = pd.DataFrame({'PageSentence':MasterAfr,'PageAfr':i,'decision':res})
                        FinalDecisionDF = pd.concat([FinalDecisionDF,temp],axis=0).reset_index(drop=True)
                        FinalDecisionDF = FinalDecisionDF.loc[1:]
                    else:
                        res1 = [check(conAfr,MasterBfrT) for conAfr in MasterAfrT]    
                        res2 = [check(conAfr,MasterBfrBfrT) for conAfr in MasterAfrT]
                        res3 = [check(conAfr,MasterBfrAfrT) for conAfr in MasterAfrT]
                        res = ['Matched' if ress>0 else 'NotMatched' for ress in list(np.array(res1)+np.array(res2)+np.array(res3))]
                        temp = pd.DataFrame({'PageSentence':MasterAfr,'PageAfr':i,'decision':res})
                        FinalDecisionDF = pd.concat([FinalDecisionDF,temp],axis=0).reset_index(drop=True)
                else:
                    MasterAfr = PageCorrectionList2(g['afr_%s'%i])
                    temp = pd.DataFrame({'PageSentence':MasterAfr,'PageAfr':i,'decision':'Newly Added Page'})
                    FinalDecisionDF = pd.concat([FinalDecisionDF,temp],axis=0).reset_index(drop=True)
            except:
                pass
        FinalDecisionDF = FinalDecisionDF.reset_index(drop=True)    
        
    ### READ IN PDF
    tempFinal = FinalDecisionDF[FinalDecisionDF['decision']=='NotMatched'].reset_index(drop=True)

    lis = []
    for i in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()):
        if i<len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum():
            try:
                if g['afr_%s'%(i+1)].endswith('.'):
                    continue
                else:
                    if i < (len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()) and (i!=len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum() - 1):
                        text = g['MasterBfr_%s'%(i+1)][-1] + ' ' + g['MasterBfr_%s'%(i+2)][0]
                        lis.append(text)
            except:
                pass
    
    lis = [''.join(i.split()) for i in lis]
    

    for i in range(len(tempFinal)):
        if i!=len(tempFinal)-1 and tempFinal['decision'].iloc[i] != 'Matched':
            TextToSearch = tempFinal['PageSentence'].iloc[i] + ' ' + tempFinal['PageSentence'].iloc[i+1]
            TextToSearch = ''.join(TextToSearch.split())
            val = TextToSearch in lis
            if val == False:
                continue
            else:
                tempFinal['decision'].iloc[i] = 'Matched'
                tempFinal['decision'].iloc[i+1] = 'Matched'
        elif i==len(tempFinal)-1:
            TextToSearch = tempFinal['PageSentence'].iloc[i]
            TextToSearch = ''.join(TextToSearch.split())
            val = TextToSearch in lis
            if val == False:
                continue
            else:
                tempFinal['decision'].iloc[i] = 'Matched'
    
    temp = tempFinal[tempFinal['decision']=='Matched']
    
    if len(temp)!=0:
        for i in temp['PageSentence']:
            if i in temp['PageSentence']:
                FinalDecisionDF[FinalDecisionDF['PageSentence']==i]['decision'] = 'Matched'
            else:
                continue
    
    TotalDfCntAfr = len(FinalDecisionDF)    
            
    tempFinal = FinalDecisionDF[FinalDecisionDF['decision']!='Matched']
    
    tempFinal['BarFlag'] = tempFinal['PageSentence'].apply(lambda x : cleanFlag(x))
    tempFinal = tempFinal[tempFinal['BarFlag'] != 1]
    tempFinal.reset_index(drop=True,inplace=True)
    del tempFinal['BarFlag']
    
    tempFinal['comb1'] = None
    for i in range(len(tempFinal)):
        if i<len(tempFinal)-1:
            tempFinal['comb1'].iloc[i] = tempFinal['PageSentence'].iloc[i] + ' ' + tempFinal['PageSentence'].iloc[i+1]
        else:
            tempFinal['comb1'].iloc[i] = tempFinal['PageSentence'].iloc[i]
    
    lis = []   
    for i in range(len(PDFextract['textBfr'])-PDFextract['textBfr'].isnull().sum()):
        if i<len(PDFextract['textBfr'])-PDFextract['textBfr'].isnull().sum()-2:
            try:
                text = g['MasterBfr_%s'%(i+1)][-1] + ' ' + g['MasterBfr_%s'%(i+2)][0]
                lis.append(text)
            except:
                pass 
    
    lisRem = [i.split('.')[0] for i in lis]    
    tempFinal['comb1_Match'] = tempFinal['comb1'].isin(lis)
    
    Altak = []
    for i in range(len(tempFinal['comb1_Match'])):
        if i not in Altak and i < len(tempFinal['comb1_Match'])-1:
            if tempFinal['comb1_Match'].iloc[i] == True:
                tempFinal['comb1_Match'].iloc[i+1] = True
                tempFinal['decision'].iloc[i] = 'Matched'
                tempFinal['decision'].iloc[i+1] = 'Matched'
                Altak.append(i+1)
        else:
            if tempFinal['comb1_Match'].iloc[i] == True:
                tempFinal['decision'].iloc[i] = 'Matched'
        
    tempFinal = tempFinal[tempFinal['decision'] == 'NotMatched'].reset_index(drop=True)
    
    for i in range(len(tempFinal)):
        pageAfr = tempFinal['PageAfr'].iloc[i]
        pageBfr = FinalMatchPage[FinalMatchPage['PageAfr']==pageAfr]['PageBfr'].iloc[0]
        pageBfrAfr = pageBfr + 1
        pageBfrBfr = pageBfr - 1
        txt = ''.join(tempFinal['PageSentence'].iloc[i].split(' '))
        try:
            pageBfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfr]]
            pageBfrlis = [i.split('.')[0] for i in pageBfrlis]
            pageBfrAfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfrAfr]]
            pageBfrAfrlis = [i.split('.')[0] for i in pageBfrAfrlis]
            pageBfrBfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfrBfr]]
            pageBfrBfrlis = [i.split('.')[0] for i in pageBfrBfrlis]
            if txt in str(pageBfrlis):
                tempFinal['decision'].iloc[i] = 'Matched'
            if txt in str(pageBfrAfrlis):
                tempFinal['decision'].iloc[i] = 'Matched'
            if txt in str(pageBfrBfrlis):
                tempFinal['decision'].iloc[i] = 'Matched'
            
            if tempFinal['decision'].iloc[i] == 'NotMatched':
                if txt.split('.')[0] in str(pageBfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
                if txt.split('.')[0] in str(pageBfrAfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
                if txt.split('.')[0] in str(pageBfrBfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
            
            lisRemRem = [''.join(i.split(' ')) for i in lisRem]
            if txt.split('.')[0] in str(lisRemRem):
                tempFinal['decision'].iloc[i] = 'Matched'
            
        except:
            try:
                pageBfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfr]]
                pageBfrlis = [i.split('.')[0] for i in pageBfrlis]
                pageBfrBfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfrBfr]]
                pageBfrBfrlis = [i.split('.')[0] for i in pageBfrBfrlis]
                if txt in str(pageBfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
                if txt in str(pageBfrBfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
                
                if tempFinal['decision'].iloc[i] == 'NotMatched':
                    if txt.split('.')[0] in str(pageBfrlis):
                        tempFinal['decision'].iloc[i] = 'Matched'
                    if txt.split('.')[0] in str(pageBfrBfrlis):
                        tempFinal['decision'].iloc[i] = 'Matched'
                lisRemRem = [''.join(i.split(' ')) for i in lisRem]
                
                if txt.split('.')[0] in str(lisRemRem):
                    tempFinal['decision'].iloc[i] = 'Matched'
                
            except:
                pass
                
    tempFinal = tempFinal[tempFinal['decision'] == 'NotMatched'].reset_index(drop=True)         

    tempFinal['CleanFlag'] = None
    tempFinal['TextInstances'] = None
    for i,j,k in zip(tempFinal['PageAfr'],tempFinal['PageSentence'],range(len(tempFinal))):
        tempFinal['CleanFlag'].iloc[k],tempFinal['TextInstances'].iloc[k] = Highlighter1(fileNameAfr,i,j,output,'Changes_',B)    
    
    tempFinalNotdetected = tempFinal[tempFinal['TextInstances'].isnull()==True].reset_index(drop=True)
    tempFinal = tempFinal[tempFinal['TextInstances'].isnull()!=True].reset_index(drop=True)
    
    for i in range(len(tempFinalNotdetected)):
        print(i)
        doc = fitz.open(fileNameAfr)
        page = doc[int(tempFinalNotdetected['PageAfr'].iloc[i]-1)]
        text1 = tempFinalNotdetected['PageSentence'].iloc[i]
    
        whilei = 0
        remtext = 'ab'
        while len(remtext) != 0:
            if whilei == 0:
                newtext,remtext = listThrower(text1)
                whilei = whilei + 1
                textIns = page.searchFor(newtext,hit_max=1000)
            elif whilei <= 100:
                newtext,remtext = listThrower(remtext)
                textIns = textIns + page.searchFor(newtext,hit_max=1000)
            else:
                textIns = 'Not Highlighted'
        tempFinalNotdetected['TextInstances'].iloc[i] = textIns
        doc.close()
    
    g['AfrNotDetected_%s'%B] = tempFinalNotdetected[tempFinalNotdetected['TextInstances'] == 'Not Highlighted']
    tempFinalNotdetected = tempFinalNotdetected[tempFinalNotdetected['TextInstances'] != 'Not Highlighted']
    tempFinalNotdetected.reset_index(drop=True,inplace=True)
    tempFinal['CleanFlag'] = 0
    tempFinalNotdetected['CleanFlag'] = 1
    tempFinal = pd.concat([tempFinal,tempFinalNotdetected],axis = 0)
    tempFinal.reset_index(drop=True,inplace=True)
    
    NtFndCntAfr = len(g['AfrNotDetected_%s'%B]) + len(tempFinal)
    
    for i in range(len(tempFinal)):
        print(i)
        if i==0:
            g['doc%s'%i] = fitz.open(fileNameAfr)
            page = g['doc%s'%i][int(tempFinal['PageAfr'].iloc[i])-1]
            for inst in tempFinal['TextInstances'].iloc[i]:
                highlight = page.addHighlightAnnot(inst)
            g['doc%s'%i].save(output+'test%s_%s_AfterChangeDoc.pdf'%(i,B))
            g['doc%s'%i].close()
        else:
            g['doc%s'%(i-1)] = fitz.open(output+'test%s_%s_AfterChangeDoc.pdf'%(i-1,B))
            page = g['doc%s'%(i-1)][int(tempFinal['PageAfr'].iloc[i])-1]
            for inst in tempFinal['TextInstances'].iloc[i]:
                highlight = page.addHighlightAnnot(inst)
            g['doc%s'%(i-1)].save(output+'test%s_%s_AfterChangeDoc.pdf'%(i,B))
            g['doc%s'%(i-1)].close()
    
    TotalDfFCntAfr = TotalDfCntAfr - NtFndCntAfr        
    
    ResultFiles = os.listdir(output)
    ResultFiles = [i for i in ResultFiles if B in i]
    ResultFiles = [i for i in ResultFiles if i.find('%s'%B)>=0 and i.find('AfterChangeDoc')>=0]
    ResultFiles = [i for i in ResultFiles if i != 'test%s_%s_AfterChangeDoc.pdf'%(len(tempFinal)-1,B)]
    for i in ResultFiles:
        os.remove(output+i)
        
    tempFinal1 = copy.deepcopy(tempFinal[['PageSentence', 'PageAfr']])
    tempFinal1['DocumentNo'] = 'B'
    
#        tempFinal[['PageSentence','PageAfr','CleanFlag']].to_csv('afrDetectedNotDetected_%s.csv'%B,index=False)
    
################################### Let's get to the vice versa------------------------------------------
# clear the environment first
#sys.modules[__name__].__dict__.clear()

    Rpath = 'C:/Program Files/R/R-3.5.2/bin/'
    MPath = 'D:/Projects/ReUsableCM/'
    ScriptsPath = '%sScripts/'%MPath
    PrePath = '%sInput_post/'%MPath
    PostPath = '%sInput_pre/'%MPath
    ExtractedpdfsPath = '%sPDFsExtracted/'%MPath
    output = '%sResults/'%MPath

    #Removing page 1 0f 1 from text
    regex1 = r"([a-zA-Z]+) (\d+) ([a-zA-Z]+) (\d+)"
    regex2 = r"(\(([a-zA-Z]+) (\d+) ([a-zA-Z]+) (\d+)\))"
    regex3 = r"(\( ([a-zA-Z]+) (\d+) ([a-zA-Z]+) (\d+) \))"
    regex4 = r"(\d+) Page ([a-zA-Z]+) (\d+)"
        
#    args = [fileNameAfr,fileNameBfr,ExtractedpdfsPath,B,'2']
#    subprocess.call(["%srscript.exe"%RPath, "%spdfreader.R"%ScriptsPath] + args,shell=True)
    
    robjects.globalenv['args'] = robjects.vectors.StrVector([fileNameAfr,fileNameBfr,ExtractedpdfsPath,B,'2'])
    r.source(ScriptsPath + "pdfreader.R")
    
    PDFextract = pd.read_csv('%s%s_%sExtracted.csv'%(ExtractedpdfsPath,B,'2'),encoding = 'unicode_escape')
    
    for i in range(len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum()):
        try:
            g['bfr_%s'%(i+1)] = PDFextract['textBfr'].iloc[i]
            g['bfr_%s'%(i+1)] = copy.deepcopy(g['bfr_%s'%(i+1)].replace('\r\r\n',' '))
            g['bfr_%s'%(i+1)] = ' '.join(g['bfr_%s'%(i+1)].split())
            g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)].strip()
            try:
                barCodeIdentify = re.search(r'\*%s(.*)?\* \*.*?\* (\d+) (\d+)/(\d+)'%B,g['bfr_%s'%(i+1)])
                g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)][:barCodeIdentify.start()].strip()
                del barCodeIdentify
            except:
                try:
                    barCodeIdentify = re.search(r'\*%s(.*)?\* \*.*?\*'%B,g['bfr_%s'%(i+1)])
                    g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)][:barCodeIdentify.start()].strip()
                    del barCodeIdentify
                except:
                    pass
                
            g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)].replace('',"'")
            g['bfr_%s'%(i+1)] = g['bfr_%s'%(i+1)].replace('\x95','')
        except:
            pass
    
    for i in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()):
        try:
            g['afr_%s'%(i+1)] = PDFextract['textAfr'].iloc[i]
            g['afr_%s'%(i+1)] = copy.deepcopy(g['afr_%s'%(i+1)].replace('\r\r\n',' '))
            g['afr_%s'%(i+1)] = ' '.join(g['afr_%s'%(i+1)].split())
            g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)].strip()
            try:
                barCodeIdentify = re.search(r'\*%s(.*)?\* \*.*?\* (\d+) (\d+)/(\d+)'%B,g['afr_%s'%(i+1)])
                g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)][:barCodeIdentify.start()].strip()
                del barCodeIdentify
            except:
                try:
                    barCodeIdentify = re.search(r'\*%s(.*)?\* \*.*?\*'%B,g['afr_%s'%(i+1)])
                    g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)][:barCodeIdentify.start()].strip()
                    del barCodeIdentify
                except:
                    pass
        except:
            pass
            
        g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)].replace('',"'")
        g['afr_%s'%(i+1)] = g['afr_%s'%(i+1)].replace('\x95','')
    
    docpage = ['afr_%s'%(i+1) for i in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum())]
    pagenum = [i+1 for i in range(len(docpage))]
    afr_df = pd.DataFrame({'DocPageNameAfr':docpage,'TextAfr':None,'PageNumAfr':pagenum})
    for i in range(len(afr_df)):
        afr_df['TextAfr'].iloc[i] = g['afr_%s'%(i+1)]
    
    docpage = ['bfr_%s'%(i+1) for i in range(len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum())]
    pagenum = [i+1 for i in range(len(docpage))]
    bfr_df = pd.DataFrame({'DocPageNameBfr':docpage,'TextBfr':None,'PageNumBfr':pagenum})
    for i in range(len(bfr_df)):
        bfr_df['TextBfr'].iloc[i] = g['bfr_%s'%(i+1)] 

    PageAfr = []
    PageBfr = []
    MatchinPerc = []
    for i in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()):
        for j in range(len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum()):
            print(i,j)
            PageAfr.append(i)
            PageBfr.append(j)
            vect = TfidfVectorizer(min_df=1)
            tfidf = vect.fit_transform([afr_df['TextAfr'].iloc[i],bfr_df['TextBfr'].iloc[j]])
            MatchMatrix = (tfidf * tfidf.T).A
            MatchinPerc.append(MatchMatrix[0][1])

    MatchMatrixdf = pd.DataFrame({'PageAfr':PageAfr,'PageBfr':PageBfr,'Perc':MatchinPerc})
    MatchMatrixdf['PageAfr'] = MatchMatrixdf['PageAfr'] + 1 
    MatchMatrixdf['PageBfr'] = MatchMatrixdf['PageBfr'] + 1
    
    PageAfr = []
    PageBfr = []
    MatchinPerc = []
    TakenPage = []
    PagesConsd = np.unique(MatchMatrixdf['PageAfr'])
    for i in range(len(PagesConsd)):
        if i<150:
            temp = MatchMatrixdf[(MatchMatrixdf['PageAfr'] == PagesConsd[i])]
            temp = temp[~temp['PageBfr'].isin(TakenPage)]
            PageAfr.append(PagesConsd[i])
            try:
                if max(temp['Perc']) < 0.60:
                    PageBfr.append(None)
                    MatchinPerc.append(None)
                else:
                    if PagesConsd[i] == temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0]:
                        PageBfr.append(temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0])
                        MatchinPerc.append(temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0])
                        TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0])
                    else:
                        tempMatch = temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0]
                        tempMatchPerc = temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0]
                        RestTemp = MatchMatrixdf[(MatchMatrixdf['PageBfr'] > PagesConsd[i])]
                        RestTemp = RestTemp[RestTemp['PageBfr']==tempMatch]
                        ExpMatch = RestTemp[(RestTemp['PageBfr'] == tempMatch) & (RestTemp['PageBfr'] == tempMatch)]['Perc'].iloc[0]
                        ExpMatchPerc = RestTemp[(RestTemp['PageAfr'] == tempMatch) & (RestTemp['PageBfr'] == tempMatch)]['Perc'].iloc[0]
                        try:
                            if ExpMatchPerc > tempMatchPerc:
                                if PagesConsd[i] not in TakenPage:
                                    PageBfr.append(PagesConsd[i])
                                    MatchinPerc.append(temp[temp['PageBfr'] == PagesConsd[i]]['Perc'].iloc[0])
                                    TakenPage.append(PagesConsd[i])
                            else:
                                PageBfr.append(temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0])
                                MatchinPerc.append(temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0])
                                TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageBfr'].iloc[0])
                        except:
                            PageAfr.append(tempMatch)
                            MatchinPerc.append(tempMatchPerc)
                            TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
            except:
                PageBfr.append(None)
                MatchinPerc.append(None)
        else:
            break

    FinalMatchPage = pd.DataFrame({'PageAfr':PageAfr,'PageBfr':PageBfr,'MathPerc':MatchinPerc})
    
    
    PageAfr = []
    PageBfr = []
    MatchinPerc = []
    for i in range(len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum()):
        for j in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()):
            print(i,j)
            PageBfr.append(i)
            PageAfr.append(j)
            vect = TfidfVectorizer(min_df=1)
            tfidf = vect.fit_transform([bfr_df['TextBfr'].iloc[i],afr_df['TextAfr'].iloc[j]])
            MatchMatrix = (tfidf * tfidf.T).A
            MatchinPerc.append(MatchMatrix[0][1])

    MatchMatrixdf2 = pd.DataFrame({'PageBfr':PageBfr,'PageAfr':PageAfr,'Perc':MatchinPerc})
    MatchMatrixdf2['PageBfr'] = MatchMatrixdf2['PageBfr'] + 1 
    MatchMatrixdf2['PageAfr'] = MatchMatrixdf2['PageAfr'] + 1
        
    PageAfr = []
    PageBfr = []
    MatchinPerc = []
    TakenPage = []
    PagesConsd = np.unique(MatchMatrixdf2['PageBfr'])
    for i in range(len(PagesConsd)):
        if i<150:
            temp = MatchMatrixdf2[(MatchMatrixdf2['PageBfr'] == PagesConsd[i])]
            temp = temp[~temp['PageAfr'].isin(TakenPage)]
            PageBfr.append(PagesConsd[i])
            try:
                if max(temp['Perc']) < 0.60:
                    PageAfr.append(None)
                    MatchinPerc.append(None)
                else:
                    if PagesConsd[i] == temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0]:
                        PageAfr.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
                        MatchinPerc.append(temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0])
                        TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
                    else:
                        tempMatch = temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0]
                        tempMatchPerc = temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0]
                        RestTemp = MatchMatrixdf[(MatchMatrixdf['PageAfr'] > PagesConsd[i])]
                        RestTemp = RestTemp[RestTemp['PageAfr']==tempMatch].reset_index(drop=True)
                        try:
                            ExpMatch = RestTemp[(RestTemp['PageBfr'] == tempMatch) & (RestTemp['PageAfr'] == tempMatch)]['PageAfr'].iloc[0]
                            ExpMatchPerc = RestTemp[(RestTemp['PageBfr'] == tempMatch) & (RestTemp['PageAfr'] == tempMatch)]['Perc'].iloc[0]
                            if ExpMatchPerc > tempMatchPerc:
                                if PagesConsd[i] not in TakenPage:
                                    PageAfr.append(PagesConsd[i])
                                    MatchinPerc.append(temp[temp['PageAfr'] == PagesConsd[i]]['Perc'].iloc[0])
                                    TakenPage.append(PagesConsd[i])
                            else:
                                PageAfr.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
                                MatchinPerc.append(temp[temp['Perc'] == max(temp['Perc'])]['Perc'].iloc[0])
                                TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
                        except:
                            PageAfr.append(tempMatch)
                            MatchinPerc.append(tempMatchPerc)
                            TakenPage.append(temp[temp['Perc'] == max(temp['Perc'])]['PageAfr'].iloc[0])
            except:
                PageAfr.append(None)
                MatchinPerc.append(None)
        else:
            break

    FinalMatchPage2 = pd.DataFrame({'PageBfr':PageBfr,'PageAfr':PageAfr,'MathPerc':MatchinPerc})
    
    if (len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum() > len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum()):
           tempDielamma = FinalMatchPage[FinalMatchPage['MathPerc'].isnull()==True]
           try:
               splitList = splitPageFinder2(tempDielamma)
               tempDielamma['SplitPage'] = splitList
           except:
               pass
    else:
        tempDielamma = FinalMatchPage[FinalMatchPage['MathPerc'].isnull()==True]
        try:
            splitList = splitPageFinder1(tempDielamma)
            tempDielamma['SplitPage'] = splitList
        except:
            pass
    
    if len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum() < len(PDFextract['textBfr'])-pd.isnull(PDFextract['textBfr']).sum():
        try:
            FinalMatchPage = pd.merge(FinalMatchPage,tempDielamma[['PageBfr','SplitPage']],left_on=['PageAfr'],right_on = ['SplitPage'],how='left')
            del FinalMatchPage['SplitPage']
            FinalMatchPage.rename(columns={'PageBfr_x':'PageBfr','PageBfr_y':'SplitPage'},inplace=True)
        except:
            pass
    else:
        try:
            FinalMatchPage = pd.merge(FinalMatchPage,tempDielamma[['PageAfr','SplitPage']],left_on=['PageAfr'],right_on = ['PageAfr'],how='left')
            FinalMatchPage.rename(columns={'PageAfr_x':'PageAfr'},inplace=True)
        except:
            pass
    
    try:            
        FinalMatchPage['PageBfr'] = [i if np.isnan(i)!=True else j for i,j in zip(FinalMatchPage['PageBfr'],FinalMatchPage['SplitPage'])]
        FinalDecisionDF = pd.DataFrame({'PageSentence':[0],'PageAfr':[0],'decision':[0]})
    except:
        pass
    
    for sd in range(len(FinalMatchPage['PageAfr'])):
        try:
            if sd==0:
                g['afr_%s'%(sd+1)] = g['afr_%s'%(sd+1)].strip()
            if sd!=0:
                g['afr_%s'%(sd+1)] = g['afr_%s'%(sd+1)].strip() 
                if len(g['afr_%s'%(sd+1)].split('.')[0].split(' ')) == 1:# and len(g['afr_%s'%(sd+1)].split('.')[0].split(' ')[0])==1:
                    g['afr_%s'%(sd)] = g['afr_%s'%(sd)] +  str(g['afr_%s'%(sd+1)].split('.')[0].split(' ')[0]) + '.'
#                else:
#                    g['afr_%s'%(sd)] = g['afr_%s'%(sd)] + ' ' + str(g['afr_%s'%(sd+1)].split('.')[0].split(' ')[0]) + '.'
        except:
            pass
    
    for sd in range(len(FinalMatchPage['PageBfr'])):
        try:
            if sd==0:
                g['bfr_%s'%(sd+1)] = g['bfr_%s'%(sd+1)].strip()
            if sd!=0:
                g['bfr_%s'%(sd+1)] = g['bfr_%s'%(sd+1)].strip() 
                if len(g['bfr_%s'%(sd+1)].split('.')[0].split(' ')) == 1:# and len(g['bfr_%s'%(sd+1)].split('.')[0].split(' ')[0])==1:
                    g['bfr_%s'%(sd)] = g['bfr_%s'%(sd)] +  str(g['bfr_%s'%(sd+1)].split('.')[0].split(' ')[0]) + '.'
#                else:
#                    g['bfr_%s'%(sd)] = g['bfr_%s'%(sd)] + ' ' + str(g['bfr_%s'%(sd+1)].split('.')[0].split(' ')[0]) + '.'
        except:
            pass
    

    for i,j in zip(FinalMatchPage['PageAfr'],FinalMatchPage['PageBfr']):
            i = int(i)
            try:
                print(i,j)
                print('1st try')
                if (np.isnan(j) != True):
                    j = int(j)
                    MasterAfr = PageCorrectionList2(g['afr_%s'%i])
                    MasterBfr = PageCorrectionList2(g['bfr_%s'%j])
                    
                    g['MasterAfr_%s'%i] = PageCorrectionList2(g['afr_%s'%i])
                    g['MasterBfr_%s'%j]= PageCorrectionList2(g['bfr_%s'%j])
                    
                    if len(MasterAfr[0].split(' ')) == 1:
                        MasterAfr.pop(0)
                    if len(MasterBfr[0].split(' ')) == 1:
                        MasterBfr.pop(0)
                    
                    g['MasterAfr_%s'%i] = PageCorrectionList2(g['afr_%s'%i])
                    g['MasterBfr_%s'%j]= PageCorrectionList2(g['bfr_%s'%j])
                    
                    if len(g['MasterAfr_%s'%i][0].split(' ')) == 1:
                        g['MasterAfr_%s'%i].pop(0)
                    if len(g['MasterAfr_%s'%i][0].split(' ')) == 1:
                        g['MasterAfr_%s'%i].pop(0)
                    
                    if i==1:
                        MasterAfrAfr = PageCorrectionList2(g['afr_%s'%(i+1)])
                        MasterAfrAfrT = [''.join(i.split()) for i in MasterAfrAfr]
                    elif (i>1) and (i<len(MasterAfr)-1) :
                        MasterAfrAfr = PageCorrectionList2(g['afr_%s'%(i+1)])
                        MasterAfrAfrT = [''.join(i.split()) for i in MasterAfrAfr]
                        MasterAfrBfr = PageCorrectionList2(g['afr_%s'%(i-1)])
                        MasterAfrBfrT = [''.join(i.split()) for i in MasterAfrBfr]
                    else:
                        MasterAfrBfr = PageCorrectionList2(g['afr_%s'%(i-1)])
                        MasterAfrBfrT = [''.join(i.split()) for i in MasterAfrBfr]
                    
                    if j==1:
                        MasterBfrAfr = PageCorrectionList2(g['bfr_%s'%(j+1)])
                        MasterBfrAfrT = [''.join(i.split()) for i in MasterBfrAfr]
                    elif (j>1) and (j<len(MasterBfr)-1) :
                        MasterBfrAfr = PageCorrectionList2(g['bfr_%s'%(j+1)])
                        MasterBfrAfrT = [''.join(i.split()) for i in MasterBfrAfr]
                        MasterBfrBfr = PageCorrectionList2(g['bfr_%s'%(j-1)])
                        MasterBfrBfrT = [''.join(i.split()) for i in MasterBfrBfr]
                    else:
                        MasterBfrBfr = PageCorrectionList2(g['bfr_%s'%(j-1)])
                        MasterBfrBfrT = [''.join(i.split()) for i in MasterBfrBfr]
                    
                    MasterAfrT = [''.join(i.split()) for i in MasterAfr]
                    MasterBfrT = [''.join(i.split()) for i in MasterBfr]
                                
                    if i==1 and j==1: 
                        res1 = [check(conAfr,MasterBfrT) for conAfr in MasterAfrT]
                        res2 = [check(conAfr,MasterBfrAfrT) for conAfr in MasterAfrT]
                        res = ['Matched' if ress>0 else 'NotMatched' for ress in list(np.array(res1)+np.array(res2))]
                        temp = pd.DataFrame({'PageSentence':MasterAfr,'PageAfr':i,'decision':res})
                        FinalDecisionDF = pd.concat([FinalDecisionDF,temp],axis=0).reset_index(drop=True)
                        FinalDecisionDF = FinalDecisionDF.loc[1:]
                        FinalDecisionDF.reset_index(drop=True,inplace=True)
#                                print('1st if')
                    else:
                        res1 = [check(conAfr,MasterBfrT) for conAfr in MasterAfrT]    
                        res2 = [check(conAfr,MasterBfrBfrT) for conAfr in MasterAfrT]
                        res3 = [check(conAfr,MasterBfrAfrT) for conAfr in MasterAfrT]
                        res = ['Matched' if ress>0 else 'NotMatched' for ress in list(np.array(res1)+np.array(res2)+np.array(res3))]
                        temp = pd.DataFrame({'PageSentence':MasterAfr,'PageAfr':i,'decision':res})
                        FinalDecisionDF = pd.concat([FinalDecisionDF,temp],axis=0).reset_index(drop=True)
#                                print('1st else')
                else:
                    MasterAfr = PageCorrectionList2(g['afr_%s'%i])
                    temp = pd.DataFrame({'PageSentence':MasterAfr,'PageAfr':i,'decision':'Newly Added Page'})
                    FinalDecisionDF = pd.concat([FinalDecisionDF,temp],axis=0).reset_index(drop=True)
#                            print('2nd else')
            except:
                pass
    
    ### READ IN PDF
    tempFinal = FinalDecisionDF[FinalDecisionDF['decision']=='NotMatched'].reset_index(drop=True)

    lis = []
    for i in range(len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()):
        if i<len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum():
            try:
                if g['afr_%s'%(i+1)].endswith('.'):
                    continue
                else:
                    if (i < len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum()) and (i!=len(PDFextract['textAfr'])-pd.isnull(PDFextract['textAfr']).sum() - 1):
                        text = g['MasterBfr_%s'%(i+1)][-1] + ' ' + g['MasterBfr_%s'%(i+2)][0]
                        lis.append(text)
            except:
                pass
            
    
    lis = [''.join(i.split()) for i in lis]
        
    
    for i in range(len(tempFinal)):
        if i!=len(tempFinal)-1 and tempFinal['decision'].iloc[i] != 'Matched':
            TextToSearch = tempFinal['PageSentence'].iloc[i] + ' ' + tempFinal['PageSentence'].iloc[i+1]
            TextToSearch = ''.join(TextToSearch.split())
            val = TextToSearch in lis
            if val == False:
                continue
            else:
                tempFinal['decision'].iloc[i] = 'Matched'
                tempFinal['decision'].iloc[i+1] = 'Matched'
        elif i==len(tempFinal)-1:
            TextToSearch = tempFinal['PageSentence'].iloc[i]
            TextToSearch = ''.join(TextToSearch.split())
            val = TextToSearch in lis
            if val == False:
                continue
            else:
                tempFinal['decision'].iloc[i] = 'Matched'
    
    temp = tempFinal[tempFinal['decision']=='Matched']
    
    if len(temp)!=0:
        for i in temp['PageSentence']:
            if i in temp['PageSentence']:
                FinalDecisionDF[FinalDecisionDF['PageSentence']==i]['decision'] = 'Matched'
            else:
                continue
    
    TotalDfCntBfr = len(FinalDecisionDF)
    
    tempFinal = FinalDecisionDF[FinalDecisionDF['decision']!='Matched']    
    
    tempFinal['BarFlag'] = tempFinal['PageSentence'].apply(lambda x : cleanFlag(x))
    tempFinal = tempFinal[tempFinal['BarFlag'] != 1]
    tempFinal.reset_index(drop=True,inplace=True)
    del tempFinal['BarFlag']
    
    tempFinal['comb1'] = None
    for i in range(len(tempFinal)):
        if i<len(tempFinal)-1:
            tempFinal['comb1'].iloc[i] = tempFinal['PageSentence'].iloc[i] + ' ' + tempFinal['PageSentence'].iloc[i+1]
        else:
            tempFinal['comb1'].iloc[i] = tempFinal['PageSentence'].iloc[i]
     
    lis = []   
    for i in range(len(PDFextract['textBfr'])-PDFextract['textBfr'].isnull().sum()):
        if i<len(PDFextract['textBfr'])-PDFextract['textBfr'].isnull().sum()-2:
            text = g['MasterBfr_%s'%(i+1)][-1] + ' ' + g['MasterBfr_%s'%(i+2)][0]
            lis.append(text) 
    
    lisRem = [i.split('.')[0] for i in lis]    
    tempFinal['comb1_Match'] = tempFinal['comb1'].isin(lis)
    
    Altak = []
    for i in range(len(tempFinal['comb1_Match'])):
        if i not in Altak and i < len(tempFinal['comb1_Match'])-1:
            if tempFinal['comb1_Match'].iloc[i] == True:
                tempFinal['comb1_Match'].iloc[i+1] = True
                tempFinal['decision'].iloc[i] = 'Matched'
                tempFinal['decision'].iloc[i+1] = 'Matched'
                Altak.append(i+1)
        else:
            if tempFinal['comb1_Match'].iloc[i] == True:
                tempFinal['decision'].iloc[i] = 'Matched'
    
    tempFinal = tempFinal[tempFinal['decision'] == 'NotMatched'].reset_index(drop=True)
    
    for i in range(len(tempFinal)):
        pageAfr = tempFinal['PageAfr'].iloc[i]
        pageBfr = FinalMatchPage[FinalMatchPage['PageAfr']==pageAfr]['PageBfr'].iloc[0]
        pageBfrAfr = pageBfr + 1
        pageBfrBfr = pageBfr - 1
        txt = ''.join(tempFinal['PageSentence'].iloc[i].split(' '))
        try:
            pageBfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfr]]
            pageBfrlis = [i.split('.')[0] for i in pageBfrlis]
            pageBfrAfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfrAfr]]
            pageBfrAfrlis = [i.split('.')[0] for i in pageBfrAfrlis]
            pageBfrBfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfrBfr]]
            pageBfrBfrlis = [i.split('.')[0] for i in pageBfrBfrlis]
            if txt in str(pageBfrlis):
                tempFinal['decision'].iloc[i] = 'Matched'
            if txt in str(pageBfrAfrlis):
                tempFinal['decision'].iloc[i] = 'Matched'
            if txt in str(pageBfrBfrlis):
                tempFinal['decision'].iloc[i] = 'Matched'
            
            if tempFinal['decision'].iloc[i] == 'NotMatched':
                if txt.split('.')[0] in str(pageBfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
                if txt.split('.')[0] in str(pageBfrAfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
                if txt.split('.')[0] in str(pageBfrBfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
            
            lisRemRem = [''.join(i.split(' ')) for i in lisRem]
            if txt.split('.')[0] in str(lisRemRem):
                tempFinal['decision'].iloc[i] = 'Matched'
            
        except:
            try:
                pageBfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfr]]
                pageBfrlis = [i.split('.')[0] for i in pageBfrlis]
                pageBfrBfrlis = [''.join(i.split(' ')) for i in g['MasterBfr_%s'%pageBfrBfr]]
                pageBfrBfrlis = [i.split('.')[0] for i in pageBfrBfrlis]
                if txt in str(pageBfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
                if txt in str(pageBfrBfrlis):
                    tempFinal['decision'].iloc[i] = 'Matched'
                
                if tempFinal['decision'].iloc[i] == 'NotMatched':
                    if txt.split('.')[0] in str(pageBfrlis):
                        tempFinal['decision'].iloc[i] = 'Matched'
                    if txt.split('.')[0] in str(pageBfrBfrlis):
                        tempFinal['decision'].iloc[i] = 'Matched'
                lisRemRem = [''.join(i.split(' ')) for i in lisRem]
                
                if txt.split('.')[0] in str(lisRemRem):
                    tempFinal['decision'].iloc[i] = 'Matched'
                
            except:
                pass
                
    tempFinal = tempFinal[tempFinal['decision'] == 'NotMatched'].reset_index(drop=True)
    
    tempFinal['CleanFlag'] = None
    tempFinal['TextInstances'] = None
    for i,j,k in zip(tempFinal['PageAfr'],tempFinal['PageSentence'],range(len(tempFinal))):
        tempFinal['CleanFlag'].iloc[k],tempFinal['TextInstances'].iloc[k] = Highlighter1(fileNameAfr,i,j,output,'Changes_',B)    
    
    tempFinal['BarFlag'] = tempFinal['PageSentence'].apply(lambda x : cleanFlag(x))
    tempFinal = tempFinal[tempFinal['BarFlag'] != 1]
    
    tempFinalNotdetected = tempFinal[tempFinal['TextInstances'].isnull()==True].reset_index(drop=True)
    tempFinal = tempFinal[tempFinal['TextInstances'].isnull()!=True].reset_index(drop=True)
    
    for i in range(len(tempFinalNotdetected)):
        print(i)
        doc = fitz.open(fileNameBfr)
        page = doc[int(tempFinalNotdetected['PageAfr'].iloc[i]-1)]
        text1 = tempFinalNotdetected['PageSentence'].iloc[i]
    
        whilei = 0
        remtext = 'ab'
        while len(remtext) != 0:
            if whilei == 0:
                newtext,remtext = listThrower(text1)
                whilei = whilei + 1
                textIns = page.searchFor(newtext,hit_max=1000)
            elif whilei <= 100:
                newtext,remtext = listThrower(remtext)
                textIns = textIns + page.searchFor(newtext,hit_max=1000)
            else:
                textIns = 'Not Highlighted'
        tempFinalNotdetected['TextInstances'].iloc[i] = textIns
        doc.close()
    
    g['bfrNotDetected_%s'%B] = tempFinalNotdetected[tempFinalNotdetected['TextInstances'] == 'Not Highlighted']
    tempFinalNotdetected = tempFinalNotdetected[tempFinalNotdetected['TextInstances'] != 'Not Highlighted']
    tempFinalNotdetected.reset_index(drop=True,inplace=True)
    tempFinalNotdetected['CleanFlag'] = 1
    tempFinal = pd.concat([tempFinal,tempFinalNotdetected],axis = 0)
    tempFinal.reset_index(drop=True,inplace=True)
    
    NtFndCntBfr = len(g['bfrNotDetected_%s'%B]) + len(tempFinal)
    
    for i in range(len(tempFinal)):
        print(i)
        if i==0:
            g['doc%s'%i] = fitz.open(fileNameBfr)
            page = g['doc%s'%i][int(tempFinal['PageAfr'].iloc[i])-1]
            for inst in tempFinal['TextInstances'].iloc[i]:
                highlight = page.addHighlightAnnot(inst)
            g['doc%s'%i].save(output+'test%s_%s_BeforeChangeDoc.pdf'%(i,B))
            g['doc%s'%i].close()
        else:
            g['doc%s'%(i-1)] = fitz.open(output+'test%s_%s_BeforeChangeDoc.pdf'%(i-1,B))
            page = g['doc%s'%(i-1)][int(tempFinal['PageAfr'].iloc[i])-1]
            for inst in tempFinal['TextInstances'].iloc[i]:
                highlight = page.addHighlightAnnot(inst)
            g['doc%s'%(i-1)].save(output+'test%s_%s_BeforeChangeDoc.pdf'%(i,B))
            g['doc%s'%(i-1)].close()
    
    TotalDfFCntBfr = TotalDfCntBfr - NtFndCntBfr        
    
    ResultFiles = os.listdir(output)
    ResultFiles = [i for i in ResultFiles if B in i]
    ResultFiles = [i for i in ResultFiles if i.find('%s'%B)>=0 and i.find('BeforeChangeDoc')>=0]
    ResultFiles = [i for i in ResultFiles if i != 'test%s_%s_BeforeChangeDoc.pdf'%(len(tempFinal)-1,B)]
    for i in ResultFiles:
        os.remove(output+i)
    
    tempFinal2 = copy.deepcopy(tempFinal[['PageSentence', 'PageAfr']])
    tempFinal2['DocumentNo'] = 'A'

except:
    LoansNotRun.append(B)

Description = ['Total Num of Pages in Doc B','Total Num of Pages in Doc A','Total Sentences present in Doc B','Total sentences present in Doc A','Total Matched sentences present in B compared with A','Total Matched sentences present in A compared with B','Total UnMatched sentences present in B compared with A','Total UnMatched sentences present in A compared with B','% Similarity']
Summary = [AfrPages,BfrPages,TotalDfCntAfr,TotalDfCntBfr,TotalDfFCntAfr,TotalDfFCntBfr,NtFndCntAfr,NtFndCntBfr,(TotalDfFCntAfr+TotalDfFCntBfr)/(TotalDfCntBfr+TotalDfCntAfr)*100]
g['summary_%s'%B] = pd.DataFrame({'Description':Description,'Summary (in Nos)':Summary})
g['summary_%s'%B].to_csv(summaryPath+'summary_%s.csv'%B,index=False)
tempFinalComp = pd.concat([tempFinal1,tempFinal2],axis=0).reset_index(drop=True)
tempFinalComp.to_csv(summaryPath+'%s_NotMatchedData.csv'%B,index=False)
#tempFinal1.to_csv(summaryPath+'%s_Postchanges.csv'%B,index=False)
#tempFinal2.to_csv(summaryPath+'%s_Prechanges.csv'%B,index=False)
