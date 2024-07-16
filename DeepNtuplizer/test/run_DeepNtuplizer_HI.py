import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing
### parsing job options 
import sys

options = VarParsing.VarParsing()

options.register('inputScript','',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"input Script")
options.register('outputFile','output',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"output File (w/o .root)")
options.register('maxEvents',-1,VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.int,"maximum events")
options.register('skipEvents', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "skip N events")
options.register('job', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "job number")
options.register('nJobs', 1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "total jobs")
options.register('release','8_0_1', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"release number (w/o CMSSW)")

print("Using release "+options.release)


if hasattr(sys, "argv"):
    options.parseArguments()




# process = cms.Process("DNNFiller")
from Configuration.Eras.Era_Run3_pp_on_PbPb_2023_cff import Run3_pp_on_PbPb_2023
process = cms.Process("DNNFiller", Run3_pp_on_PbPb_2023)


process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:132X_mcRun3_2023_realistic_HI_v10', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.options = cms.untracked.PSet(
   allowUnscheduled = cms.untracked.bool(True),  
   wantSummary=cms.untracked.bool(False)
)

# from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValTTbarPileUpMINIAODSIM

process.source = cms.Source('PoolSource',
    fileNames=cms.untracked.vstring ('root://eoscms.cern.ch//eos/cms//store/group/cmst3/group/hintt/Run3/MC/PbPb2023/Embedded/2024_04_19/POWHEG_5p36TeV_2023Run3/TT_hvq_POWHEG_Hydjet_5p36TeV_TuneCP5_2023Run3_MINIAOD_2024_04_19/240419_231333/0000/POWHEG_TT_hvq_MINIAOD_1.root'),
)

if options.inputScript != '' and options.inputScript != 'DeepNTuples.DeepNtuplizer.samples.TEST':
    process.load(options.inputScript)

numberOfFiles = len(process.source.fileNames)
numberOfJobs = options.nJobs
jobNumber = options.job


process.source.fileNames = process.source.fileNames[jobNumber:numberOfFiles:numberOfJobs]
if options.nJobs > 1:
    print ("running over these files:")
    print (process.source.fileNames)
#process.source.fileNames = ['file:/uscms/home/verzetti/nobackup/CMSSW_8_0_25/src/DeepNTuples/copy_numEvent100.root']

process.source.skipEvents = cms.untracked.uint32(options.skipEvents)
process.maxEvents  = cms.untracked.PSet( 
    input = cms.untracked.int32 (options.maxEvents) 
)


# if int(options.release.replace("_",""))>=840 :
#  bTagInfos = [
#         'pfImpactParameterTagInfos',
#         'pfInclusiveSecondaryVertexFinderTagInfos',
#         'pfDeepCSVTagInfos',
#  ]
# else :
#  bTagInfos = [
#         'pfImpactParameterTagInfos',
#         'pfInclusiveSecondaryVertexFinderTagInfos',
#         'deepNNTagInfos',
#  ]


# if int(options.release.replace("_",""))>=840 :
#  bTagDiscriminators = [
#      'softPFMuonBJetTags',
#      'softPFElectronBJetTags',
#          'pfJetBProbabilityBJetTags',
#          'pfJetProbabilityBJetTags',
#      'pfCombinedInclusiveSecondaryVertexV2BJetTags',
#          'pfDeepCSVJetTags:probudsg', #to be fixed with new names
#          'pfDeepCSVJetTags:probb',
#          'pfDeepCSVJetTags:probc',
#          'pfDeepCSVJetTags:probbb',
#          'pfDeepCSVJetTags:probcc',
#  ]
# else :
#   bTagDiscriminators = [
#      'softPFMuonBJetTags',
#      'softPFElectronBJetTags',
#          'pfJetBProbabilityBJetTags',
#          'pfJetProbabilityBJetTags',
#      'pfCombinedInclusiveSecondaryVertexV2BJetTags',
#          'deepFlavourJetTags:probudsg', #to be fixed with new names
#          'deepFlavourJetTags:probb',
#          'deepFlavourJetTags:probc',
#          'deepFlavourJetTags:probbb',
#          'deepFlavourJetTags:probcc',
#  ]



# jetCorrectionsAK4 = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')

# from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
# updateJetCollection(
#         process,
#         labelName = "DeepFlavour",
#         jetSource = cms.InputTag('slimmedJets'),#'ak4Jets'
#         jetCorrections = jetCorrectionsAK4,
#         pfCandidates = cms.InputTag('packedPFCandidates'),
#         pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
#         svSource = cms.InputTag('slimmedSecondaryVertices'),
#         muSource = cms.InputTag('slimmedMuons'),
#         elSource = cms.InputTag('slimmedElectrons'),
#         btagInfos = bTagInfos,
#         btagDiscriminators = bTagDiscriminators,
#         explicitJTA = False
# )

# if hasattr(process,'updatedPatJetsTransientCorrectedDeepFlavour'):
# 	process.updatedPatJetsTransientCorrectedDeepFlavour.addTagInfos = cms.bool(True) 
# 	process.updatedPatJetsTransientCorrectedDeepFlavour.addBTagInfo = cms.bool(True)
# else:
# 	raise ValueError('I could not find updatedPatJetsTransientCorrectedDeepFlavour to embed the tagInfos, please check the cfg')


# # QGLikelihood
# process.load("DeepNTuples.DeepNtuplizer.QGLikelihood_cfi")
# process.es_prefer_jec = cms.ESPrefer("PoolDBESSource", "QGPoolDBESSource")
# process.load('RecoJets.JetProducers.QGTagger_cfi')
# process.QGTagger.srcJets   = cms.InputTag("selectedUpdatedPatJetsDeepFlavour")
# process.QGTagger.jetsLabel = cms.string('QGL_AK4PFchs')


# from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
# process.ak4GenJetsWithNu = ak4GenJets.clone(src = 'packedGenParticles')
 
#  ## Filter out neutrinos from packed GenParticles
# process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"))
#  ## Define GenJets
# process.ak4GenJetsRecluster = ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNu')
 
 
# process.patGenJetMatchWithNu = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
#     src         = cms.InputTag("selectedUpdatedPatJetsDeepFlavour"),      # RECO jets (any View<Jet> is ok) 
#     matched     = cms.InputTag("ak4GenJetsWithNu"),        # GEN jets  (must be GenJetCollection)              
#     mcPdgId     = cms.vint32(),                      # n/a   
#     mcStatus    = cms.vint32(),                      # n/a   
#     checkCharge = cms.bool(False),                   # n/a   
#     maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
#     #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
#     resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
#     resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
# )

# process.patGenJetMatchRecluster = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
#     src         = cms.InputTag("selectedUpdatedPatJetsDeepFlavour"),      # RECO jets (any View<Jet> is ok) 
#     matched     = cms.InputTag("ak4GenJetsRecluster"),        # GEN jets  (must be GenJetCollection)              
#     mcPdgId     = cms.vint32(),                      # n/a   
#     mcStatus    = cms.vint32(),                      # n/a   
#     checkCharge = cms.bool(False),                   # n/a   
#     maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
#     #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
#     resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
#     resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
# )

# process.genJetSequence = cms.Sequence(process.packedGenParticlesForJetsNoNu*process.ak4GenJetsWithNu*process.ak4GenJetsRecluster*process.patGenJetMatchWithNu*process.patGenJetMatchRecluster)
 
# Heavy-ion settings
from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import PackedPFTowers, hiPuRho, hiSignalGenParticles, allPartons
process.PackedPFTowers = PackedPFTowers.clone()
process.hiPuRho = hiPuRho.clone(
    src = 'PackedPFTowers'
)
process.hiSignalGenParticles = hiSignalGenParticles.clone(
    src = "prunedGenParticles"
)
process.allPartons = allPartons.clone(
    src = 'hiSignalGenParticles'
)
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
process.ak4GenJetsWithNu = ak4GenJets.clone(
    src = 'packedGenParticlesSignal'
)

# Create unsubtracted reco jets
from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cff import ak4PFJets, patJetCorrFactors, patJetPartonMatch, patJetGenJetMatch, patJetPartons, patJetFlavourAssociation, patJets
process.ak4PFMatchingForakCs0PFJets = ak4PFJets.clone(
    src = 'packedPFCandidates',
    rParam = 0.4
)
process.ak4PFMatchingForakCs0PFpatJetCorrFactors = patJetCorrFactors.clone(
    src = 'ak4PFMatchingForakCs0PFJets',
    payload = 'AK4PF'
)
process.ak4PFMatchingForakCs0PFpatJetPartonMatch = patJetPartonMatch.clone(
    src = 'ak4PFMatchingForakCs0PFJets',
    matched = 'hiSignalGenParticles',
    maxDeltaR = 0.4
)
process.ak4PFMatchingForakCs0PFpatJetGenJetMatch = patJetGenJetMatch.clone(
    src = 'ak4PFMatchingForakCs0PFJets',
    matched = 'ak4GenJetsWithNu',
    maxDeltaR = 0.4
)
process.ak4PFMatchingForakCs0PFpatJetPartons = patJetPartons.clone(
    particles = 'hiSignalGenParticles',
    partonMode = 'Pythia8'
)
process.ak4PFMatchingForakCs0PFpatJetFlavourAssociation =  patJetFlavourAssociation.clone(
    jets = 'ak4PFMatchingForakCs0PFJets',
    rParam = 0.4,
    bHadrons = cms.InputTag("ak4PFMatchingForakCs0PFpatJetPartons","bHadrons"),
    cHadrons = cms.InputTag("ak4PFMatchingForakCs0PFpatJetPartons","cHadrons"),
    partons = cms.InputTag("ak4PFMatchingForakCs0PFpatJetPartons","physicsPartons"),
    leptons = cms.InputTag("ak4PFMatchingForakCs0PFpatJetPartons","leptons")
)
process.ak4PFMatchingForakCs0PFpatJets = patJets.clone(
    JetFlavourInfoSource = 'ak4PFMatchingForakCs0PFpatJetFlavourAssociation',
    JetPartonMapSource = 'ak4PFMatchingForakCs0PFpatJetFlavourAssociation',
    genJetMatch = 'ak4PFMatchingForakCs0PFpatJetGenJetMatch',
    genPartonMatch = 'ak4PFMatchingForakCs0PFpatJetPartonMatch',
    jetCorrFactorsSource = ['ak4PFMatchingForakCs0PFpatJetCorrFactors'],
    jetSource = 'ak4PFMatchingForakCs0PFJets',
    addBTagInfo = False,
    addDiscriminators = False,
    addAssociatedTracks = False,
    useLegacyJetMCFlavour = False
)

# Create HIN subtracted reco jets
from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cff import akCs4PFJets, patJetPartonAssociationLegacy, patJetFlavourAssociationLegacy
process.akCs0PFJets = akCs4PFJets.clone(
    src = 'packedPFCandidates',
    useModulatedRho = False,
    rParam = 0.4
)
process.akCs0PFpatJetCorrFactors = patJetCorrFactors.clone(
    src = 'akCs0PFJets',
    payload = 'AK4PF'
)
process.akCs0PFpatJetPartonMatch = patJetPartonMatch.clone(
    src = 'akCs0PFJets',
    matched = 'hiSignalGenParticles',
    maxDeltaR = 0.4
)
process.akCs0PFpatJetGenJetMatch = patJetGenJetMatch.clone(
    src = 'akCs0PFJets',
    matched = 'ak4GenJetsWithNu',
    maxDeltaR = 0.4
)
process.akCs0PFpatJetPartonAssociationLegacy = patJetPartonAssociationLegacy.clone(
    jets = 'akCs0PFJets'
)
process.akCs0PFpatJetFlavourAssociationLegacy = patJetFlavourAssociationLegacy.clone(
    srcByReference = 'akCs0PFpatJetPartonAssociationLegacy'
)
process.akCs0PFpatJetPartons = patJetPartons.clone(
    particles = 'hiSignalGenParticles',
    partonMode = 'Pythia8'
)
from RecoBTag.ImpactParameter.pfImpactParameterTagInfos_cfi import pfImpactParameterTagInfos
process.akCs0PFpfImpactParameterTagInfos = pfImpactParameterTagInfos.clone(
    jets = 'akCs0PFJets',
    candidates = 'packedPFCandidates',
    primaryVertex = 'offlineSlimmedPrimaryVertices'
)
from RecoBTag.SecondaryVertex.pfSecondaryVertexTagInfos_cfi import pfSecondaryVertexTagInfos
process.akCs0PFpfSecondaryVertexTagInfos = pfSecondaryVertexTagInfos.clone(
    trackIPTagInfos = 'akCs0PFpfImpactParameterTagInfos'
)
from RecoBTag.Combined.pfDeepCSVTagInfos_cfi import pfDeepCSVTagInfos
process.akCs0PFpfDeepCSVTagInfos = pfDeepCSVTagInfos.clone(
    svTagInfos = 'akCs0PFpfSecondaryVertexTagInfos'
)
from RecoBTag.Combined.pfDeepCSVJetTags_cfi import pfDeepCSVJetTags
process.akCs0PFpfDeepCSVJetTags = pfDeepCSVJetTags.clone(
    src = 'akCs0PFpfDeepCSVTagInfos'
)
from RecoBTag.ImpactParameter.pfJetProbabilityBJetTags_cfi import pfJetProbabilityBJetTags
process.akCs0PFpfJetProbabilityBJetTags = pfJetProbabilityBJetTags.clone(
    tagInfos = ['akCs0PFpfImpactParameterTagInfos']
)
process.akCs0PFpatJets = patJets.clone(
    JetFlavourInfoSource = 'akCs0PFpatJetFlavourAssociation',
    JetPartonMapSource = 'akCs0PFpatJetFlavourAssociationLegacy',
    genJetMatch = 'akCs0PFpatJetGenJetMatch',
    genPartonMatch = 'akCs0PFpatJetPartonMatch',
    jetCorrFactorsSource = ['akCs0PFpatJetCorrFactors'],
    jetSource = 'akCs0PFJets',
    discriminatorSources = [cms.InputTag('akCs0PFpfDeepCSVJetTags','probb'), cms.InputTag('akCs0PFpfDeepCSVJetTags','probc'), cms.InputTag('akCs0PFpfDeepCSVJetTags','probudsg'), cms.InputTag('akCs0PFpfDeepCSVJetTags','probbb'), cms.InputTag('akCs0PFpfJetProbabilityBJetTags')],
    addAssociatedTracks = False,
)
# -------------
process.ak4PFMatchingForakCs0PFJets.jetPtMin = process.akCs0PFJets.jetPtMin
process.akCs0PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
process.ak4PFMatchedForakCs0PFpatJets = cms.EDProducer("JetMatcherDR", source = cms.InputTag("akCs0PFpatJets"), matched = cms.InputTag("ak4PFMatchingForakCs0PFpatJets"))
process.akCs0PFpatJets.embedPFCandidates = True

# Start of b-tagging sequence ----------------
from RecoBTag.ImpactParameter.pfImpactParameterTagInfos_cfi import pfImpactParameterTagInfos
process.pfImpactParameterTagInfos = pfImpactParameterTagInfos.clone(
    jets = "akCs0PFpatJets",
    candidates = "packedPFCandidates",
    primaryVertex = "offlineSlimmedPrimaryVertices"
)
from RecoBTag.SecondaryVertex.pfSecondaryVertexTagInfos_cfi import pfSecondaryVertexTagInfos
process.pfSecondaryVertexTagInfos = pfSecondaryVertexTagInfos.clone()
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import inclusiveCandidateVertexFinder, candidateVertexMerger, candidateVertexArbitrator, inclusiveCandidateSecondaryVertices
process.inclusiveCandidateVertexFinder = inclusiveCandidateVertexFinder.clone(
    tracks = "packedPFCandidates",
    minHits = 0,
    minPt = 0.8,
    primaryVertices = "offlineSlimmedPrimaryVertices"
)
process.candidateVertexMerger = candidateVertexMerger.clone()
process.candidateVertexArbitrator = candidateVertexArbitrator.clone(
    tracks = "packedPFCandidates",
    primaryVertices = "offlineSlimmedPrimaryVertices"
)
process.inclusiveCandidateSecondaryVertices = inclusiveCandidateSecondaryVertices.clone()
from RecoBTag.SecondaryVertex.pfInclusiveSecondaryVertexFinderTagInfos_cfi import pfInclusiveSecondaryVertexFinderTagInfos
process.pfInclusiveSecondaryVertexFinderTagInfos = pfInclusiveSecondaryVertexFinderTagInfos.clone()

from RecoBTag.Combined.pfDeepCSVTagInfos_cfi import pfDeepCSVTagInfos
process.pfDeepCSVTagInfos = pfDeepCSVTagInfos.clone(
    svTagInfos = "pfSecondaryVertexTagInfos"
)
from RecoBTag.FeatureTools.pfDeepFlavourTagInfos_cfi import pfDeepFlavourTagInfos
process.pfDeepFlavourTagInfosSlimmedDeepFlavour = pfDeepFlavourTagInfos.clone(
    fallback_puppi_weight = True,
    fallback_vertex_association = True,
    jets = cms.InputTag("akCs0PFpatJets"),
    unsubjet_map = cms.InputTag("ak4PFMatchedForakCs0PFpatJets"),
    puppi_value_map = cms.InputTag(""),
    secondary_vertices = cms.InputTag("inclusiveCandidateSecondaryVertices"),
    shallow_tag_infos = cms.InputTag("pfDeepCSVTagInfos"),
    vertex_associator = cms.InputTag(""),
    vertices = cms.InputTag("offlineSlimmedPrimaryVertices")
)
from RecoBTag.FeatureTools.pfParticleTransformerAK4TagInfos_cfi import pfParticleTransformerAK4TagInfos
process.pfParticleTransformerAK4TagInfosSlimmedDeepFlavour = pfParticleTransformerAK4TagInfos.clone(
    fallback_puppi_weight = True,
    fallback_vertex_association = True,
    jets = cms.InputTag("akCs0PFpatJets"),
    unsubjet_map = cms.InputTag("ak4PFMatchedForakCs0PFpatJets"),
    puppi_value_map = cms.InputTag(""),
    secondary_vertices = cms.InputTag("inclusiveCandidateSecondaryVertices"),
    vertex_associator = cms.InputTag(""),
    vertices = cms.InputTag("offlineSlimmedPrimaryVertices")
)

from RecoBTag.ONNXRuntime.pfDeepFlavourJetTags_cfi import pfDeepFlavourJetTags
process.pfDeepFlavourJetTagsSlimmedDeepFlavour = pfDeepFlavourJetTags.clone(
    src = cms.InputTag("pfDeepFlavourTagInfosSlimmedDeepFlavour")
)
from RecoBTag.ONNXRuntime.pfParticleTransformerAK4JetTags_cfi import pfParticleTransformerAK4JetTags
process.pfParticleTransformerAK4JetTagsSlimmedDeepFlavour = pfParticleTransformerAK4JetTags.clone(
    src = cms.InputTag("pfParticleTransformerAK4TagInfosSlimmedDeepFlavour")
)

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
updateJetCollection(
    process,
    jetSource = cms.InputTag('akCs0PFpatJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    btagDiscriminators = ['pfCombinedSecondaryVertexV2BJetTags', 'pfDeepCSVDiscriminatorsJetTags:BvsAll', 'pfDeepCSVDiscriminatorsJetTags:CvsB', 'pfDeepCSVDiscriminatorsJetTags:CvsL'], ## to add discriminators,
    btagPrefix = 'TEST',
)
process.updatedPatJets.addJetCorrFactors = False
process.updatedPatJets.discriminatorSources = cms.VInputTag(
    cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probb"), cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probbb"),   cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probc"),
    cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probg"), cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","problepb"), cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probuds"),
    cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probb"), cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probbb"),   cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probc"),
    cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probg"), cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","problepb"), cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probuds"),
)
# End of b-tagging sequence ----------------

bTagDiscriminators = [
    'pfDeepFlavourJetTagsSlimmedDeepFlavour:probb',
    'pfDeepFlavourJetTagsSlimmedDeepFlavour:probbb',
    'pfDeepFlavourJetTagsSlimmedDeepFlavour:probc',
    'pfDeepFlavourJetTagsSlimmedDeepFlavour:probg',
    'pfDeepFlavourJetTagsSlimmedDeepFlavour:problepb',
    'pfDeepFlavourJetTagsSlimmedDeepFlavour:probuds',
    'pfParticleTransformerAK4JetTagsSlimmedDeepFlavour:probb',
    'pfParticleTransformerAK4JetTagsSlimmedDeepFlavour:probbb',
    'pfParticleTransformerAK4JetTagsSlimmedDeepFlavour:probc',
    'pfParticleTransformerAK4JetTagsSlimmedDeepFlavour:probg',
    'pfParticleTransformerAK4JetTagsSlimmedDeepFlavour:problepb',
    'pfParticleTransformerAK4JetTagsSlimmedDeepFlavour:probuds',
]
# ------------------------------------------------------------#

srcJets = cms.InputTag('updatedPatJets')
process.unsubJetMap = cms.EDProducer("JetMatcherDR", source = srcJets, matched = cms.InputTag("ak4PFMatchingForakCs0PFpatJets"))
process.jetTask = cms.Task(
    process.PackedPFTowers,
    process.hiPuRho,
    process.hiSignalGenParticles,
    process.allPartons,
    process.ak4GenJetsWithNu,
    process.ak4PFMatchingForakCs0PFJets,
    process.ak4PFMatchingForakCs0PFpatJetCorrFactors,
    process.ak4PFMatchingForakCs0PFpatJetPartonMatch,
    process.ak4PFMatchingForakCs0PFpatJetGenJetMatch,
    process.ak4PFMatchingForakCs0PFpatJetPartons,
    process.ak4PFMatchingForakCs0PFpatJetFlavourAssociation,
    process.ak4PFMatchingForakCs0PFpatJets,
    process.akCs0PFJets,
    process.akCs0PFpatJetCorrFactors,
    process.akCs0PFpatJetPartonMatch,
    process.akCs0PFpatJetGenJetMatch,
    process.akCs0PFpatJetPartonAssociationLegacy,
    process.akCs0PFpatJetFlavourAssociationLegacy,
    process.akCs0PFpatJetPartons,
    process.akCs0PFpfImpactParameterTagInfos,
    process.akCs0PFpfSecondaryVertexTagInfos,
    process.akCs0PFpfDeepCSVTagInfos,
    process.akCs0PFpfDeepCSVJetTags,
    process.akCs0PFpfJetProbabilityBJetTags,
    process.akCs0PFpatJets,
    process.ak4PFMatchedForakCs0PFpatJets,
    process.ak4PFMatchedForakCs0PFpatJets,
    process.pfImpactParameterTagInfos,
    process.pfSecondaryVertexTagInfos,
    process.inclusiveCandidateVertexFinder,
    process.candidateVertexMerger,
    process.candidateVertexArbitrator,
    process.inclusiveCandidateSecondaryVertices,
    process.pfInclusiveSecondaryVertexFinderTagInfos,
    process.pfDeepCSVTagInfos,
    process.pfDeepFlavourTagInfosSlimmedDeepFlavour,
    process.pfParticleTransformerAK4TagInfosSlimmedDeepFlavour,
    process.pfDeepFlavourJetTagsSlimmedDeepFlavour,
    process.pfParticleTransformerAK4JetTagsSlimmedDeepFlavour,
    process.updatedPatJets,
    process.unsubJetMap
)


outFileName = options.outputFile + '_' + str(options.job) +  '.root'
print ('Using output file ' + outFileName)

process.TFileService = cms.Service("TFileService", 
                                   fileName = cms.string(outFileName))

# DeepNtuplizer
process.load("DeepNTuples.DeepNtuplizer.DeepNtuplizer_cfi")

process.deepntuplizer.jets = cms.InputTag('selectedUpdatedPatJetsDeepFlavour');
process.deepntuplizer.bDiscriminators = bTagDiscriminators 

process.deepntuplizer.unsubjet_map = "unsubJetMap"
process.deepntuplizer.genParticles = "hiSignalGenParticles"
process.deepntuplizer.SVs = "inclusiveCandidateSecondaryVertices"

if int(options.release.replace("_",""))>=840 :
   process.deepntuplizer.tagInfoName = cms.string('pfDeepCSV')

process.p = cms.Path(process.deepntuplizer)
process.p.associate(process.jetTask)