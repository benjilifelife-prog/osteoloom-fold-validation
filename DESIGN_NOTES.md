# Osteoloom construct — design notes and provenance

## The question

The Osteoloom pitch asserts that flexible linkers allow each fused module to
fold independently, and that the NT and CT domains continue to drive
pH-triggered assembly with four modules inserted between them. Neither claim
was tested. This project tests them computationally.

**Hypothesis:** inserting RGD, LL-37, and a BMP-2 knuckle epitope between the
spidroin terminal domains does not disrupt the folds of NT, CT, or the inserted
modules themselves.

## Component provenance

| Segment | Length | Source | Confidence |
|---|---|---|---|
| His-tag + thrombin site | 20 aa | pET28a standard | Standard vector sequence |
| NT domain | 137 aa | PDB 3LR2 — MaSp1 N-terminal domain, *Euprosthenops australis* | Deposited sequence |
| eADF4 C module | 35 aa | eADF4(C16) literature — ADF-4, *Araneus diadematus* | Published module |
| RGD tag | 11 aa | eADF4(C16)-RGD construct, `GGSGGRGDSPG` | Published tag |
| LL-37 | 37 aa | Human cathelicidin, full-length mature peptide | Confirmed, two sources |
| BMP-2 knuckle epitope | 20 aa | BMP-2 residues 73–92 | Confirmed |
| CT domain | 126 aa | PDB 2KHM — ADF-3 C-terminal domain, *Araneus diadematus*, T7-tag artifact stripped | Deposited sequence, manually trimmed |
| Linker | 15 aa | (GGGGS)×3, standard flexible linker | Design choice |

**Sequence check:** computed MW of the NT domain is 14.2 kDa, matching the
14,183.71 Da formula weight reported for the NMR structure of that domain.

## Design decisions and their reasons

**Chimeric architecture — state this explicitly.** The backbone is *A.
diadematus* ADF-4; the NT domain is *E. australis* MaSp1; the CT domain is *A.
diadematus* ADF-3. Published eADF4(C16) constructs carry no terminal domains at
all. This is a chimera assembled from three sources. Chimeric minispidroins are
standard practice, but the pitch should not imply eADF4(C16) comes with NT and
CT attached.

**Statherin eliminated.** Its mineral-binding activity depends on
phosphorylated serines. *E. coli* does not phosphorylate, so the peptide would
be inert in this system — the same reasoning the pitch used to rule out
full-length BMP-2.

**BMP-2 knuckle epitope chosen over OGP.** The knuckle epitope derives from a
β-strand region of folded BMP-2. Removed from its parent protein it may not
retain that conformation, which makes it a question a structure prediction can
actually address. OGP is short and largely unstructured, so a prediction would
say little.

**RGD placement departs from the published construct.** The published
eADF4(C16)-RGD fuses the tag C-terminally. This design places it internally,
between the repeat core and LL-37, per the original gene order. This is a
deliberate departure and should be noted.

**Linker held constant at (GGGGS)×3.** Fixed here so linker length is not a
confounding variable. Varying it is a separate experiment.

## Why sub-constructs rather than the full protein

The full-length construct is 986 aa / 86.6 kDa, and roughly 570 of those
residues are the repetitive C module. That region is intrinsically disordered
in solution, and repetitive spidroin sequences are poorly represented in
sequence databases, so the MSA will be shallow and the prediction
low-confidence across most of the chain. Folding the whole thing and reporting
it would be uninterpretable for the majority of residues.

Instead: fold each domain alone to establish a baseline, then fold it in
context and compare. The comparison is the result; a single prediction is not.

| Construct | Length | Purpose |
|---|---|---|
| `01_NT_alone` | 137 aa | Control — NT baseline fold |
| `02_CT_alone` | 126 aa | Control — CT baseline fold |
| `03_LL37_alone` | 37 aa | Control — expected amphipathic helix |
| `04_BMP2k_alone` | 20 aa | Control — baseline for the knuckle epitope |
| `05_NT_junction` | 222 aa | Does NT still fold with repeat core attached? |
| `06_C_cassette` | 324 aa | **Core test** — do RGD, LL-37, BMP2k and CT hold their conformations when strung together? |
| `07_mini_full` | 566 aa | Tractable whole-protein proxy (C4 instead of C16) |

## What to measure

Per-residue pLDDT for each domain alone versus in context. A drop in the
context prediction is the signal that the fusion disrupts folding. Also check
PAE between domain blocks in `06_C_cassette`: high inter-domain PAE means the
model places the domains independently, which is the expected behaviour for
genuinely flexible linkers.

## Honest limitations to state in the write-up

- AlphaFold predicts structure, not whether a protein expresses solubly. The
  pitch's biggest technical risk — inclusion-body formation — is not addressed
  by this work.
- Low pLDDT in the repeat region is an expected property of a disordered
  sequence, not evidence of a design flaw.
- A prediction is a hypothesis about structure, not a measurement. Circular
  dichroism would be the experimental test.

## Open items

- Verify whether the leading `GS` on the NT sequence and the stripped
  `MASMTGGQQMGRGS` on CT are cloning artifacts; confirm against the original
  papers before finalising.
- Confirm the eADF4 C module sequence against the primary Scheibel-group
  publication rather than a secondary description.

## Prediction settings

ColabFold v1.6.3 (AlphaFold2 + MMseqs2), Google Colab, NVIDIA T4.
These settings are held identical across every construct; the project's
conclusions rest on comparing predictions, so a changed setting between
runs would void the comparison.

| Parameter | Value |
|---|---|
| `num_relax` | 0 (no Amber relaxation) |
| `template_mode` | none |
| `msa_mode` | mmseqs2_uniref_env |
| `pair_mode` | unpaired_paired |
| `model_type` | auto |
| `num_recycles` | 3 |
| `max_msa` | auto |
| `num_seeds` | 1 for monomer controls; >=3 for repeat-containing constructs |
| `use_dropout` | off |

Note that `model_type: auto` is a rule, not a fixed model: it selects
`alphafold2_ptm` for monomers and `alphafold2_multimer_v3` for complexes,
and `num_recycles` auto-adjusts to 20 for multimers. The dimer constructs
therefore run under a different model than the monomers by design, and
pLDDT values should not be compared across that boundary -- only within it.

`num_seeds` is raised for constructs containing the repeat core because
seed variance is large in low-confidence regions; reporting a single seed
there would overstate precision.

## Results

| Construct | pLDDT (rank 1) | pTM | Model spread | MSA depth |
|---|---|---|---|---|
| `01_NT_alone` | 86.34 | 0.807 | 84.0-86.4 (2.4) | 404 |
| `02_CT_alone` | 85.70 | 0.751 | 83.0-85.7 (2.7) | 394 |
| `03_LL37_alone` | 87.80 | 0.464 | 75.4-87.8 (12.4) | 3 |
| `04_BMP2k_alone` | 63.00 | 0.047 | 59.7-63.0 (3.3) | ~2100 |
| `08_C4_alone` | 35.30 | 0.121 | 33.0-35.3 (2.3) | 2 |

### 01_NT_alone

Folds with high confidence, consistent with the deposited NMR structure. The
first seven residues (`GSGNSHT`) are the only disordered stretch at that end,
rising from pLDDT 31.8 at G1 to 86.3 by W10; excluding the first five residues
raises the mean to 88.10. This is consistent with the leading `GS` being a
cloning scar rather than native sequence, and partially closes that open item.

### 02_CT_alone

Scores comparably to NT despite being modelled as a
cd ~/osteoloom-fold-validation && cat >> DESIGN_NOTES.md << 'EOF'

## Results

| Construct | pLDDT (rank 1) | pTM | Model spread | MSA depth |
|---|---|---|---|---|
| `01_NT_alone` | 86.34 | 0.807 | 84.0-86.4 (2.4) | 404 |
| `02_CT_alone` | 85.70 | 0.751 | 83.0-85.7 (2.7) | 394 |
| `03_LL37_alone` | 87.80 | 0.464 | 75.4-87.8 (12.4) | 3 |
| `04_BMP2k_alone` | 63.00 | 0.047 | 59.7-63.0 (3.3) | ~2100 |
| `08_C4_alone` | 35.30 | 0.121 | 33.0-35.3 (2.3) | 2 |

### 01_NT_alone

Folds with high confidence, consistent with the deposited NMR structure. The
first seven residues (`GSGNSHT`) are the only disordered stretch at that end,
rising from pLDDT 31.8 at G1 to 86.3 by W10; excluding the first five residues
raises the mean to 88.10. This is consistent with the leading `GS` being a
cloning scar rather than native sequence, and partially closes that open item.

### 02_CT_alone

Scores comparably to NT despite being modelled as a monomer, which suggests the
CT fold is largely self-sufficient without its partner chain. The lower pTM
(0.751 vs 0.807) and a low-confidence extended N-terminal arm in the model are
both consistent with a domain missing half of its native assembly -- in
spidroin CT domains that region participates in the dimer interface. This is a
specific, testable prediction for `10_CT_dimer`: the arm should order when the
second chain is present.

NT and CT were predicted from near-identical alignment depths (404 vs 394
sequences), so the comparison between them is not confounded by MSA depth.

### 03_LL37_alone

LL-37 predicts as a single continuous alpha-helix with high local confidence
(pLDDT 87.8) but low global confidence (pTM 0.464) and high inter-model
variance (75.4-87.8). The divergence is expected for an isolated helical
peptide with no tertiary contacts: pLDDT reports that residue positions are
well-determined relative to their neighbours, which is trivially true of a
helix, while pTM reports confidence in a global topology that does not exist
here. pLDDT alone should not be read as evidence that the conformation is
biologically determined. The large inter-model spread is consistent with a
peptide that is disordered in aqueous solution and helical only in
membrane-mimetic environments.

Critically, the MSA for this construct contained only 3 sequences
(`max_seq=3`), against 404 and 394 for NT and CT. A 37-residue fragment
excised from its parent protein has almost no standalone homologs to align
against, so this prediction ran effectively in single-sequence mode. The
confident helix therefore does not reflect evolutionary coupling -- there was
none available -- but the model's learned sequence-to-structure prior acting
on an amphipathic pattern. The large inter-model spread is consistent with
that: with no alignment to constrain them, the five models diverge.

This control's value is as a baseline for the same segment inside
`06_C_cassette`, not as a result in its own right.

### 04_BMP2k_alone

The excised knuckle epitope returns no defined conformation: pLDDT 63.0 and
pTM 0.047 for the top model, with all five models in close agreement
(59.7-63.0, pTM 0.046-0.055) and an extended, non-compact backbone.

Critically, this is not an artefact of a sparse alignment. The MSA for this
construct was the deepest of any run in the project (`max_seq=512,
max_extra_seq=1590`, ~2100 sequences), reflecting BMP-2's membership in the
widely conserved TGF-beta superfamily. AlphaFold therefore had substantial
coevolutionary information available and still placed the fragment in no
defined structure, consistently across five models.

The contrast with `03_LL37_alone` is instructive: LL-37 was predicted
confidently (pLDDT 87.8) from an MSA of 3 sequences, while the knuckle epitope
was predicted unconfidently from ~2100. Alignment depth does not determine
confidence; the segment's intrinsic structural propensity does.

This supports the reasoning given above for selecting the knuckle epitope over
OGP: in BMP-2 the segment is a beta-strand, and beta-strands require partner
strands to pair with. Excised, there is nothing to pair against.

Design implication: the osteogenic component of this construct may be
conformationally undefined. BMP-2 receptor engagement depends on the knuckle
presenting a specific conformation, and the flexible (GGGGS)x3 linkers
flanking it in the cassette offer no structural constraint. Whether the
region becomes more defined in context is the sharpest question for
`06_C_cassette`: if its local pLDDT and PAE remain at this level when linked,
that is a genuine weakness in the design rather than an artefact of
truncation.

### 08_C4_alone

Four copies of the eADF4 C module, folded in isolation, return no structure:
pLDDT 35.3 and pTM 0.121 for the top model, with all five models in tight
agreement (33.0-35.3) and a fully extended, non-compact backbone. This is the
lowest-confidence prediction in the project by a wide margin.

Three independent signals agree. Beyond pLDDT and pTM, the recycle tolerances
never converged (6.06, 10.7, 9.99 across recycles 1-3, against 0.121 for
`01_NT_alone`), meaning the model was still moving the structure by
Angstrom-scale distances at the final recycle rather than settling on an
answer.

The MSA contained only 2 sequences (`max_seq=2`). Spidroin repeats are
low-complexity -- poly-alanine blocks and GPGGY motifs -- and such regions are
routinely masked in sequence databases, so there was little to align against.

This does not undermine the result. `03_LL37_alone` provides the necessary
control: with an MSA of 3 sequences it returned pLDDT 87.8. An empty alignment
therefore does not force a low-confidence prediction; AlphaFold will commit
when the sequence carries strong structural propensity. C4 has comparable
alignment depth and returns 34. The difference lies in the sequence, not in
the available data.

No confident beta-sheet was predicted. The repeats form beta-crystallites in
spun silk, so a confident beta prediction would have indicated the model was
reporting the solid-state conformation; it reported the solution state
(disordered) instead, which is the expected and correct behaviour for a
single-chain prediction in the absence of assembly.

This result supports the decision recorded above not to fold the full-length
986-residue construct: roughly 570 of those residues are repeat core, and this
is what that region predicts as.
