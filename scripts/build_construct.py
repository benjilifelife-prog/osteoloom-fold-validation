"""
Osteoloom fusion construct assembly.

Builds the full-length engineered spidroin and the sub-construct set used for
structure prediction. Every segment below is traceable to a source recorded in
DESIGN_NOTES.md -- nothing here is invented.
"""

# ---- Component sequences (sources in DESIGN_NOTES.md) ----

# pET28a-style N-terminal His-tag + thrombin site
HIS_TAG = "MGSSHHHHHHSSGLVPRGSH"

# MaSp1 N-terminal domain, Euprosthenops australis (PDB 3LR2, 137 aa as deposited).
# NOTE: leading "GS" is almost certainly a cloning scar, not native sequence.
NT = ("GSGNSHTTPWTNPGLAENFMNSFMQGLSSMPGFTASQLDDMSTIAQSMVQSIQSLAAQGRTS"
      "PNKLQALNMAFASSMAEIAASEEGGGSLSTKTSSIASAMSNAFLQTTGVVNQPFINEITQLV"
      "SMFAQAGMNDVSA")

# eADF4 "C" module, Araneus diadematus ADF-4. eADF4(C16) = 16 copies.
C_MODULE = "GSSAAAAAAAASGPGGYGPENQGPSGPGGYGPGGP"

# RGD tag as published in eADF4(C16)-RGD
RGD = "GGSGGRGDSPG"

# Human cathelicidin LL-37 (37 aa)
LL37 = "LLGDFFRKSKEKIGKEFKRIVQRIKDFLRNLVPRTES"

# BMP-2 knuckle epitope, residues 73-92 (20 aa)
BMP2_KNUCKLE = "KIPKASSVPTELSAISTLYL"

# ADF-3 C-terminal non-repetitive domain, Araneus diadematus (PDB 2KHM).
# Deposited chain is 140 aa including an "MASMTGGQQMGRGS" T7-tag artifact,
# stripped here to leave the 126-aa domain.
CT = ("MGAASAAVSVGGYGPQSSSAPVASAAASRLSSPAASSRVSSAVSSLVSSGPTNQAALSNTIS"
      "SVVSQVSASNPGLSGCDVLVQALLEVVSALVSILGSSSIGQINYGASAQYTQMVGQSVAQAL"
      "AG")

# Flexible linker: (GGGGS)x3
L = "GGGGS" * 3


def repeat_core(n):
    """n copies of the eADF4 C module."""
    return C_MODULE * n


def full_construct(n_modules=16):
    """Full-length design: His-NT-(C)n-RGD-LL37-BMP2k-CT with linkers."""
    return (HIS_TAG + NT + L + repeat_core(n_modules) + L + RGD + L
            + LL37 + L + BMP2_KNUCKLE + L + CT)


# ---- Sub-constructs for folding ----
# Controls establish what each domain does alone; test constructs ask whether
# that changes in context. Without the controls there is no comparison.

CONSTRUCTS = {
    # Controls: each domain in isolation
    "01_NT_alone":        NT,
    "02_CT_alone":        CT,
    "03_LL37_alone":      LL37,
    "04_BMP2k_alone":     BMP2_KNUCKLE,

    # Test 1: N-terminal junction -- does NT still fold with repeat core attached?
    "05_NT_junction":     NT + L + repeat_core(2),

    # Test 2: the functional cassette -- the central question of the project.
    # Do RGD, LL-37, BMP2k and CT each hold their isolated conformation when
    # strung together with flexible linkers?
    "06_C_cassette":      repeat_core(2) + L + RGD + L + LL37 + L
                          + BMP2_KNUCKLE + L + CT,

    # Test 3: tractable proxy for the whole protein (C4 instead of C16)
    "07_mini_full":       full_construct(n_modules=4),
}


def write_fasta(path, entries):
    with open(path, "w") as fh:
        for name, seq in entries.items():
            fh.write(f">{name}|{len(seq)}aa\n")
            for i in range(0, len(seq), 60):
                fh.write(seq[i:i + 60] + "\n")


if __name__ == "__main__":
    write_fasta("osteoloom_constructs.fasta", CONSTRUCTS)

    # Average residue mass is a bad estimator for silk (Gly/Ala rich), so
    # compute the real monoisotopic-average MW from residue masses.
    RESIDUE_MASS = {
        "A": 71.08, "R": 156.19, "N": 114.10, "D": 115.09, "C": 103.14,
        "E": 129.12, "Q": 128.13, "G": 57.05, "H": 137.14, "I": 113.16,
        "L": 113.16, "K": 128.17, "M": 131.19, "F": 147.18, "P": 97.12,
        "S": 87.08, "T": 101.10, "W": 186.21, "Y": 163.18, "V": 99.13,
    }

    def mw_kda(seq):
        return (sum(RESIDUE_MASS[a] for a in seq) + 18.02) / 1000

    full = full_construct(16)
    print(f"Full-length construct eADF4(C16) version: {len(full)} aa "
          f"({mw_kda(full):.1f} kDa)\n")
    print(f"{'construct':<20} {'length':>9} {'MW':>9}")
    print("-" * 40)
    for name, seq in CONSTRUCTS.items():
        print(f"{name:<20} {len(seq):>6} aa {mw_kda(seq):>6.1f} kDa")
