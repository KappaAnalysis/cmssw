import FWCore.ParameterSet.Config as cms
from CondCore.DBCommon.CondDBSetup_cfi import *

def loadLocalSqlite(process, sqliteFilename, tag = 'JetCorrectorParametersCollection_Fall15_25nsV2_MC_AK4PFchs'):
    process.load("CondCore.DBCommon.CondDBCommon_cfi")
    process.jec = cms.ESSource("PoolDBESSource",
          DBParameters = cms.PSet(
            messageLevel = cms.untracked.int32(0)
            ),
          timetype = cms.string('runnumber'),
          toGet = cms.VPSet(
          cms.PSet(
                record = cms.string('JetCorrectionsRecord'),
                tag    = cms.string(tag),
                label  = cms.untracked.string('AK4PFchs')
                ),
          ), 
          connect = cms.string('sqlite:' + sqliteFilename)
    )
    ## add an es_prefer statement to resolve a possible conflict from simultaneous connection to a global tag
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

def recorrectJets(process, isData = False):
    ## https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CorrPatJets
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated
    process.patJetCorrFactorsReapplyJEC = patJetCorrFactorsUpdated.clone(
    src = cms.InputTag("slimmedJets"),
      levels = ['L1FastJet', 'L2Relative', 'L3Absolute'],
      payload = 'AK4PFchs' ) # Make sure to choose the appropriate levels and payload here!
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
    process.patJetsReapplyJEC = patJetsUpdated.clone(
      jetSource = cms.InputTag("slimmedJets"),
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
      )
    if(isData):
        process.patJetCorrFactorsReapplyJEC.levels = ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']
    if( not hasattr(process, "p")):
        process.p = cms.Path() 
    process.p += cms.Sequence( process.patJetCorrFactorsReapplyJEC + process. patJetsReapplyJEC )
