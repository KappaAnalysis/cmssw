#ifndef JMEValidator_neutralCandidatePUIDJets_h
#define JMEValidator_neutralCandidatePUIDJets_h


#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "DataFormats/JetReco/interface/PileupJetIdentifier.h" 
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include <iostream>


class neutralCandidatePUIDJets : public edm::stream::EDProducer<> {

  public:
 
  neutralCandidatePUIDJets(const edm::ParameterSet&);
  ~neutralCandidatePUIDJets(){};
  
  void produce(edm::Event&, const edm::EventSetup&);

  void beginJob();
  void endJob(){};

  private:

  edm::InputTag srcJets_;
  edm::InputTag srcCandidates_;
  std::string   neutralParticlesPVJets_ ;
  std::string   neutralParticlesPUJets_ ;
  std::string   neutralParticlesUnclustered_ ;
  std::string   PUJets_;
  std::string   PVJets_;
  std::string   jetPUIDWP_;

  std::string   jetPUIDMapLabel_ ;

  PileupJetIdentifier::Id jetIdSelection_;

  edm::EDGetTokenT<pat::JetCollection> srcJetsToken_;
  edm::EDGetTokenT<reco::CandidateView> srcCandidatesToken_;

  static std::string   jetPUIDNameLabel_ ;
  static bool stringInJetCollection_ ;

  float jetPUIDCut_ [3][3];

};
#endif

bool neutralCandidatePUIDJets::stringInJetCollection_ = false;
std::string neutralCandidatePUIDJets::jetPUIDNameLabel_ = "";

neutralCandidatePUIDJets::neutralCandidatePUIDJets(const edm::ParameterSet& iConfig){

  // user defined jetPUIDCut cut
  jetPUIDCut_[0][0] = -0.2; jetPUIDCut_[0][1] = -0.3; jetPUIDCut_[0][2] = -0.5; jetPUIDCut_[0][3] = -0.5;
  jetPUIDCut_[1][0] = -0.2; jetPUIDCut_[1][1] = -0.2; jetPUIDCut_[1][2] = -0.5; jetPUIDCut_[1][3] = -0.3;
  jetPUIDCut_[2][0] = -0.2; jetPUIDCut_[2][1] = -0.2; jetPUIDCut_[2][2] = -0.2; jetPUIDCut_[2][3] =  0.1;
  jetPUIDCut_[3][0] = -0.2; jetPUIDCut_[3][1] = -0.2; jetPUIDCut_[3][2] =  0. ; jetPUIDCut_[3][3] =  0.2; 
  

  if(iConfig.existsAs<edm::InputTag >("srcJets"))
    srcJets_ = iConfig.getParameter<edm::InputTag>("srcJets");
  else
    throw cms::Exception("Configuration")<<"[neutralCandidatePUIDJets] no jet collection given \n";

  if(iConfig.existsAs<edm::InputTag >("srcCandidates"))
    srcCandidates_ = iConfig.getParameter<edm::InputTag>("srcCandidates");
  else
    throw cms::Exception("Configuration")<<"[neutralCandidatePUIDJets] no PF candidate collection given \n";

  if(!(srcJets_ == edm::InputTag("")))
    srcJetsToken_ = consumes<pat::JetCollection>(srcJets_);

  if(!(srcCandidates_ == edm::InputTag("")))
    srcCandidatesToken_ = consumes<reco::CandidateView>(srcCandidates_);


  if(iConfig.existsAs<std::string >("neutralParticlesPVJetsLabel"))
    neutralParticlesPVJets_ = iConfig.getParameter<std::string>("neutralParticlesPVJetsLabel");
  else
    neutralParticlesPVJets_ = "neutralPassingPUIDJets";

  if(iConfig.existsAs<std::string >("neutralParticlesPUJetsLabel"))
    neutralParticlesPUJets_ = iConfig.getParameter<std::string>("neutralParticlesPUJetsLabel");
  else
    neutralParticlesPUJets_ = "neutralFailingPUIDJets";

  if(iConfig.existsAs<std::string >("neutralParticlesUnclusteredLabel"))
    neutralParticlesUnclustered_ = iConfig.getParameter<std::string>("neutralParticlesUnclusteredLabel");
  else
    neutralParticlesUnclustered_ = "neutralParticlesUnclustered";

  PUJets_ = "PUJets";
  PVJets_ = "PVJets";

  if(iConfig.existsAs<std::string >("jetPUDIWP")){
    jetPUIDWP_ = iConfig.getParameter<std::string>("jetPUDIWP");
    if(jetPUIDWP_ != "tight" and jetPUIDWP_ != "medium" and jetPUIDWP_ != "loose" and jetPUIDWP_ != "user")
      throw cms::Exception("Configuration") <<"  [neutralCandidatePUIDJets] wrong label for jetPUID working point ";
  }
  else
    jetPUIDWP_ = "user";

  if(jetPUIDWP_ == "tight")
    jetIdSelection_ = PileupJetIdentifier::kTight;
  else if(jetPUIDWP_ == "medium")
    jetIdSelection_ = PileupJetIdentifier::kMedium;
  else if(jetPUIDWP_ == "loose")
    jetIdSelection_ = PileupJetIdentifier::kTight;


  if(iConfig.existsAs<std::string>("jetPUIDMapLabel"))
    jetPUIDMapLabel_ = iConfig.getParameter<std::string>("jetPUIDMapLabel");  
  else
    jetPUIDMapLabel_ = "fullDiscriminant";

  
  produces<edm::PtrVector<reco::Candidate> >(neutralParticlesPVJets_);
  produces<edm::PtrVector<reco::Candidate> >(neutralParticlesPUJets_);
  produces<edm::PtrVector<reco::Candidate> >(neutralParticlesUnclustered_);
  produces<pat::JetCollection>(PUJets_);
  produces<pat::JetCollection>(PVJets_);

}

void neutralCandidatePUIDJets::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){

  edm::Handle<pat::JetCollection> jetCollection;
  iEvent.getByToken(srcJetsToken_,jetCollection);

  edm::Handle<reco::CandidateView> candCollection;
  iEvent.getByToken(srcCandidatesToken_,candCollection);

  std::auto_ptr<edm::PtrVector<reco::Candidate> > neutralParticlesPVJets(new edm::PtrVector<reco::Candidate>);
  std::auto_ptr<edm::PtrVector<reco::Candidate> > neutralParticlesPUJets(new edm::PtrVector<reco::Candidate>);
  std::auto_ptr<edm::PtrVector<reco::Candidate> > neutralParticlesUnclustered(new edm::PtrVector<reco::Candidate>);

  std::auto_ptr<pat::JetCollection> PUJets(new pat::JetCollection);
  std::auto_ptr<pat::JetCollection> PVJets(new pat::JetCollection);

  // loop on jets
  for(auto jet : *jetCollection){
    // look if the value is embedded in pat jets
    if(!stringInJetCollection_)
    {
      if(jetPUIDWP_ != "user")
      {
        for(size_t iJet = 0; iJet < jet.userIntNames().size(); iJet++)
        {
          if(jet.userIntNames().at(iJet).find(jetPUIDMapLabel_) != std::string::npos)
          {
            stringInJetCollection_ = true;
            jetPUIDNameLabel_ = jet.userIntNames().at(iJet);
          }
        }
        if(stringInJetCollection_ == false)
          throw cms::Exception("neutralCandidatePUIDJets")<<" user int related to jetPUID not found ";      
      }
      else
      {
        for(size_t iJet = 0; iJet < jet.userFloatNames().size(); iJet++)
        {
          if(jet.userFloatNames().at(iJet).find(jetPUIDMapLabel_) != std::string::npos)
          {
            stringInJetCollection_ = true;
            jetPUIDNameLabel_ = jet.userFloatNames().at(iJet);
          }
        }
        if(stringInJetCollection_ == false)
          throw cms::Exception("neutralCandidatePUIDJets")<<" user float related to jetPUID not found ";      	
      }
    }

    // evaluate PU JET ID
    bool isPassingPUID = false;
    if(jetPUIDWP_ != "user")
    {
      isPassingPUID = PileupJetIdentifier::passJetId(jet.userInt(jetPUIDNameLabel_), jetIdSelection_);
    }
    else
    {

      int ptBin = 0; 
      int etaBin = 0;
      if ( jet.pt() >= 10. && jet.pt() < 20. ) ptBin = 1;
      if ( jet.pt() >= 20. && jet.pt() < 30. ) ptBin = 2;
      if ( jet.pt() >= 30.                     ) ptBin = 3;
      if ( std::abs(jet.eta()) >= 2.5  && std::abs(jet.eta()) < 2.75) etaBin = 1; 
      if ( std::abs(jet.eta()) >= 2.75 && std::abs(jet.eta()) < 3.0 ) etaBin = 2; 
      if ( std::abs(jet.eta()) >= 3.0  && std::abs(jet.eta()) < 5.0 ) etaBin = 3; 
      isPassingPUID = jet.userFloat(jetPUIDNameLabel_) > jetPUIDCut_[ptBin][etaBin] ? true : false ;

    }
    if(isPassingPUID)
      PVJets->push_back(jet);
    else
      PUJets->push_back(jet);
    // loop on constituents
    for( auto particle : jet.getJetConstituents())
    {
      if(particle->charge() != 0) continue;
      if(isPassingPUID)
        neutralParticlesPVJets->push_back(particle);
      else
        neutralParticlesPUJets->push_back(particle);
    }
  }

  
  // loop on pfParticles to determine if unclustered Neutral
  size_t indexColl = 0;
  for(reco::CandidateView::const_iterator itCand = candCollection->begin(); itCand != candCollection->end(); itCand++)
  {
    assert(itCand->charge() == 0);

    bool clustered = false;
    for(edm::PtrVector<reco::Candidate>::const_iterator iParticle = neutralParticlesPUJets->begin();  iParticle != neutralParticlesPUJets->end(); iParticle++)
    {
      if( itCand->p4() == iParticle->get()->p4())
      {
        clustered = true;
        break;
      }
    }
    for(edm::PtrVector<reco::Candidate>::const_iterator iParticle = neutralParticlesPVJets->begin();  iParticle != neutralParticlesPVJets->end(); iParticle++)
    {
      if( itCand->p4() == iParticle->get()->p4())
      {
        clustered = true;
        break;
      }
    }
    
    if(!clustered)
    {
      neutralParticlesUnclustered->push_back(edm::Ptr<reco::Candidate>(candCollection, indexColl));
    }
    indexColl++;
  }

  
  iEvent.put(neutralParticlesPVJets,neutralParticlesPVJets_);
  iEvent.put(neutralParticlesPUJets,neutralParticlesPUJets_);
  iEvent.put(neutralParticlesUnclustered,neutralParticlesUnclustered_);
  iEvent.put(PUJets,PUJets_);
  iEvent.put(PVJets,PVJets_);

}

DEFINE_FWK_MODULE(neutralCandidatePUIDJets);
