# arXiv submission checklist

## Prerequisites (you)
1. Register: https://arxiv.org/user/register with wkasel@gmail.com.
2. If prompted for endorsement for math.CO: the endorsement request page
   gives you a code to send to an established arXiv author. (If you know
   anyone with math arXiv papers, that's fastest; the endorsement request
   can also be sent to authors of the cited papers.)

## Submission metadata (copy-paste)
- Title: Structural rigidity in the Erdős–Graham two-set permutation problem
- Authors: Will Kasel
- Category: math.CO (Combinatorics)
- MSC: 05D10 (Ramsey theory), 05A05 (Permutations)
- Abstract: use the abstract from paper/main.tex verbatim (plain-text it:
  strip TeX macros \Z → Z, \SA → S_A as needed).
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
