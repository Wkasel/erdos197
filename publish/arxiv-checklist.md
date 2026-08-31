# arXiv submission checklist

## Prerequisites (you)
1. Register: https://arxiv.org/user/register with wkasel@gmail.com.
2. If prompted for endorsement for math.CO: the endorsement request page
   gives you a code to send to an established arXiv author. (If you know
   anyone with math arXiv papers, that's fastest; the endorsement request
   can also be sent to authors of the cited papers.)
3. Push this repository to GitHub and make it public BEFORE submitting:
   the paper's Data Availability section and the Comments field both
   point to https://github.com/Wkasel/erdos197. Push the `arxiv-v1` tag as
   well, since the Comments field cites it:
   `git push origin main && git push origin arxiv-v1`.
   (.venv is untracked, so the push is ~400 files.)
4. Recommended before posting anywhere: one fresh-context adversarial
   referee pass over the final PDF by a model with no project memory
   (feed it the PDF, not summaries), per the audit checklist.

## Submission metadata (copy-paste)
- Title: Structural rigidity in the Erdős–Graham two-set permutation problem
- Authors: William Kasel
- Category: math.CO (Combinatorics)
- MSC: 05D10 (Ramsey theory), 05A05 (Permutations)
- Abstract: the PDF abstract is now ~1,371 characters, comfortably under
  arXiv's 1,920-character metadata limit. Paste it verbatim from the PDF;
  no condensed version is needed any more (earlier drafts had a ~2,985-char
  abstract that required one). Strip the LaTeX when pasting: write S_A for
  $\SA$, (2^{k-1}, 2^k] for the interval, and M = 0 (mod 8) for the
  congruence.

- Comments field: "21 pages. Machine-verification scripts, DRAT
  certificates, and a one-command reproduction kit at
  https://github.com/Wkasel/erdos197/tree/arxiv-v1"

  (Cite the immutable tag `arxiv-v1`, not `main`: the Comments field is
  part of the permanent record of v1, and `main` will move on. The tag
  points at the exact commit the submitted PDF was built from.)
- License: arXiv non-exclusive license (default) is fine.

## Upload
- Source: upload publish/arxiv-bundle.tar.gz (contains main.tex only;
  arXiv compiles with TeX Live — the file uses only amsmath/amssymb/
  amsthm/geometry/hyperref, all standard).
- Check the arXiv-produced PDF page count (21) and that no references
  show as ?? before pressing Submit.

## After it's announced
- Update publish/erdosproblems-comment.md with the arXiv link, then post
  it at https://www.erdosproblems.com/forum/discuss/197 (and optionally
  the proof-claims thread with a link to the comment).
