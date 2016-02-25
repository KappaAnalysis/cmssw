import FWCore.ParameterSet.Config as cms

from RecoMET.METProducers.PFMET_cfi import pfMet
tauPFMET = pfMet.clone()
tauPFMET.src = cms.InputTag('tauDecayProducts')
tauPFMET.alias = cms.string('tauPFMET')

tauDecayProducts = cms.EDProducer("tauDecayProducts",
                         src = cms.InputTag("slimmedTaus") )

from PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi import patMETs
tauMET = patMETs.clone()
tauMET.computeMETSignificance = cms.bool(True)
tauMET.addGenMET = cms.bool(False)
tauMET.metSource = cms.InputTag("tauPFMET")
tauMET.srcJets = cms.InputTag("slimmedJets")
tauMET.srcLeptons = cms.VInputTag("slimmedElectrons", "slimmedMuons", "slimmedPhotons")

from RecoMET.METProducers.METSignificance_cfi import METSignificance

tausSignificance = METSignificance.clone()
tausSignificance.srcMet = cms.InputTag('tauMET')
tausSignificance.srcPFCandidates = cms.InputTag('tauDecayProducts')
