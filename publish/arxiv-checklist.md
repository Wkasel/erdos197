# arXiv submission checklist

## Prerequisites (you)
1. Register: https://arxiv.org/user/register with wkasel@gmail.com.
2. If prompted for endorsement for math.CO: the endorsement request page
   gives you a code to send to an established arXiv author. (If you know
   anyone with math arXiv papers, that's fastest; the endorsement request
   can also be sent to authors of the cited papers.)
3. Push this repository to GitHub and make it public BEFORE submitting:
   the paper's Data Availability section and the Comments field both
   point to https://github.com/Wkasel/erdos197. (`git push origin main`;
   .venv is untracked, so the push is ~400 files.)
4. Recommended before posting anywhere: one fresh-context adversarial
   referee pass over the final PDF by a model with no project memory
   (feed it the PDF, not summaries), per the audit checklist.

## Submission metadata (copy-paste)
- Title: Structural rigidity in the Erdős–Graham two-set permutation problem
- Authors: Will Kasel
- Category: math.CO (Combinatorics)
- MSC: 05D10 (Ramsey theory), 05A05 (Permutations)
- Abstract: the PDF abstract is ~2,985 characters, over arXiv's 1,920-char
  metadata limit. Use this condensed version for the metadata field (the
  full abstract stays in the PDF):

  > A sequence contains a monotone 3-AP if some three terms, taken in
  > order of position, form an increasing or a decreasing arithmetic
  > progression. Davis, Entringer, Graham and Simmons (1977) proved that
  > every permutation of Z+ contains an increasing 3-AP, constructed a
  > partition of Z+ into three sets each admitting a permutation with no
  > monotone 3-AP, and asked whether two sets suffice; this is problem
  > #197 of the Erdos problem collection. We prove that the canonical
  > candidate -- the dyadic partition, whose first part is S_A, the union
  > of the blocks (2^{k-1}, 2^k] over even k -- fails: S_A admits no
  > permutation of order type omega free of monotone 3-term APs. The
  > proof reduces the infinite problem, unconditionally, to the
  > infeasibility of a finite "order gadget" OG(M) on the interval
  > (M, 2M] (AP-freeness plus fifteen precedence axioms induced by the
  > values 15 and 16) at infinitely many dyadic scales M = 2^{2t-1}, and
  > then proves by hand that a three-axiom core of OG(M) is already
  > inconsistent with AP-freeness for every M = 0 (mod 8), a residue
  > class containing all dyadic scales. The core argument runs on a small
  > toolkit of ladder lemmas (zigzag propagation, phase dichotomy, a
  > transfer lock, and a mirror-flood induction); the mod-8 condition is
  > sharp and enters at exactly one point. Every step is machine-verified
  > at 100 scales up to M = 1024 and independently cross-validated, and a
  > one-command reproduction kit with DRAT certificates accompanies the
  > paper. We also prove supporting structural theorems: an orbit
  > obstruction, a balance law, a tower characterization, and rigidity of
  > contiguous-block play. Problem #197 itself remains open: our theorem
  > eliminates one candidate partition and decides nothing about other
  > two-set partitions.

  (1,756 characters, fits the limit.)
- Comments field: "18 pages. Machine-verification scripts, DRAT
  certificates, and a one-command reproduction kit at
  https://github.com/Wkasel/erdos197"
- License: arXiv non-exclusive license (default) is fine.

## Upload
- Source: upload publish/arxiv-bundle.tar.gz (contains main.tex only;
  arXiv compiles with TeX Live — the file uses only amsmath/amssymb/
  amsthm/geometry/hyperref, all standard).
- Check the arXiv-produced PDF page count (18) and that no references
  show as ?? before pressing Submit.

## After it's announced
- Update publish/erdosproblems-comment.md with the arXiv link, then post
  it at https://www.erdosproblems.com/forum/discuss/197 (and optionally
  the proof-claims thread with a link to the comment).
