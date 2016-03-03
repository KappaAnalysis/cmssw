from CRABAPI.RawCommand import crabCommand
from httplib import HTTPException
from CRABClient.ClientExceptions import ClientException
def submit(config):
    try: 
        crabCommand('submit', config = config)
    except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
    except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


datasets = { 
#  "DY2JetsToLLM50" : "/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
#  "DY3JetsToLLM50" : "/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
#  "DY4JetsToLLM50" : "/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
#  "DYJetsToLLM50HT-100to200" : "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
  "DYJetsToLLM50HT-200to400" : "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
  "DYJetsToLLM50HT-400to600" : "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
  "DYJetsToLLM50HT-600toInf" : "/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
  "DYJetsToLLM50" : "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM"
#  "DYJetsToLLM50NLO" : "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM"
}

import sys
from WMCore.Configuration import Configuration
from multiprocessing import Process
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True

config.section_('JobType')
config.JobType.psetName    = 'runMVAMET.py'
config.JobType.pluginName  = 'Analysis'

config.JobType.inputFiles = ['../data/weightfile.root']
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.inputDBS  = 'global' #'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 200000
config.Data.publication = False


config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'
config.Data.outLFNDirBase = '/store/user/rfriese/mvamet/skimming/2016-03-03/'
config.General.workArea = '/nfs/dust/cms/user/rfriese/crab_mvamet_skim-2016-03-03'
config.JobType.pyCfgParams = ["saveMapForTraining=True"]

for nick, sample in datasets.iteritems():
	config.General.requestName = nick
	config.Data.inputDataset = sample
	p = Process(target=submit, args=(config,))
	p.start()
	p.join()
