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
