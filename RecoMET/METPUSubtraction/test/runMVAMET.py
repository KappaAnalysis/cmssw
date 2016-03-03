import sys
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from PhysicsTools.PatAlgos.tools.tauTools import *
from RecoMET.METPUSubtraction.MVAMETConfiguration_cff import runMVAMET

options = VarParsing ('python')
options.register ('globalTag',"76X_mcRun2_asymptotic_RunIIFall15DR76_v1",VarParsing.multiplicity.singleton,VarParsing.varType.string,'input global tag to be used');
options.register ('saveMapForTraining',  False,VarParsing.multiplicity.singleton, VarParsing.varType.bool, 'save internal map from MVAMET to perform own training');
options.register ('inputFile', 'root://xrootd.unl.edu//store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/0232D37A-77BA-E511-B3C5-0CC47A4C8EA8.root', VarParsing.multiplicity.singleton, VarParsing.varType.string, "Path to a testfile")
options.register ("localSqlite", '', VarParsing.multiplicity.singleton, VarParsing.varType.string, "Path to a local sqlite file")
options.register ("reapplyJEC", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Reapply JEC to Jets")
options.register ("isData", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Input is data")
options.parseArguments()

process = cms.Process("MVAMET")

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
jetCollection = "slimmedJets"

if (options.localSqlite == ''):
    process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
    process.GlobalTag.globaltag = options.globalTag
else:
    from RecoMET.METPUSubtraction.localSqlite import loadLocalSqlite
    loadLocalSqlite(process, options.localSqlite) 


if options.reapplyJEC:
    from RecoMET.METPUSubtraction.localSqlite import recorrectJets
    recorrectJets(process, options.isData)
    jetCollection = "patJetsReapplyJEC"


# configure MVA MET
runMVAMET( process, jetCollectionPF = jetCollection)

## set input files
process.source = cms.Source("PoolSource")
process.source.fileNames = cms.untracked.vstring(options.inputFile)
## logger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 50

#! Output and Log                                                                                                                                                            
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.options.allowUnscheduled = cms.untracked.bool(True)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
) 

if options.saveMapForTraining:
    if not hasattr(process, "p"):
        process.p = cms.Path()
    process.load('CommonTools.UtilAlgos.TFileService_cfi')
    process.TFileService.fileName = cms.string('output.root')
    process.TFileService.closeFileFast = cms.untracked.bool(True)
    from RecoMET.METPUSubtraction.mapAnalyzer_cff import MAPAnalyzer
    process.MAPAnalyzer = MAPAnalyzer
    process.MVAMET.saveMap = cms.bool(True)
    process.genZEvent = cms.EDFilter("GenParticleSelector",
        filter = cms.bool(True),
        src = cms.InputTag("prunedGenParticles"),
        cut = cms.string('abs(pdgId()) == 13 && !isDirectPromptTauDecayProductFinalState()'),
        #cut = cms.string('isDirectPromptTauDecayProductFinalState()'),
        stableOnly = cms.bool(False)
    )
    process.skimmvamet = cms.Sequence( process.genZEvent * process.MVAMET * process.MAPAnalyzer)
    process.p *= (process.skimmvamet)

else:
    process.output = cms.OutputModule("PoolOutputModule",
                                      fileName = cms.untracked.string('output_particles.root'),
                                      outputCommands = cms.untracked.vstring(
                                                                             'keep patMETs_MVAMET_MVAMET_MVAMET',
                                                                             'keep *_patJetsReapplyJEC_*_MVAMET'
                                                                             ),        
                                      SelectEvents = cms.untracked.PSet(  SelectEvents = cms.vstring('p'))
                                      )
    process.out = cms.EndPath(process.output)
