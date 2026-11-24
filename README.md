# Friend-tree growth

Research drafts and exact verification programs by **Christopher D. Long**.

This project studies the growth exponent of the original random friend tree
and the arithmetic of exponents in a related family of local redirection
trees. It contains three manuscripts with different scopes.

## Manuscripts

| Draft | Main results | Files |
| --- | --- | --- |
| **Effective computation and boundary robustness of the random friend-tree exponent** | An exact pressure characterization, a terminating two-sided computation theorem, a uniform boundary-leaf resolvent estimate, robustness under bounded predictable boundary input, and a sharper rational upper bound for the original exponent. | [PDF](friend_tree_growth.pdf) · [LaTeX](friend_tree_growth.tex) |
| **Growth and irrationality in local redirection trees** | An exact CMJ representation, almost-sure power-law growth from every finite tree seed, effective root isolation, and irrationality for every finite algebraic activation parameter. | [PDF](local_redirection_irrationality.pdf) · [LaTeX](local_redirection_irrationality.tex) |
| **Transcendence targets for the friend-tree exponent: exact first-promotion reduction and arithmetic obstructions** | First-promotion arithmetic, critical-certificate noncancellation, signed product martingales, fixed-seed critical divergence, core-comparable critical eigenfunctions, and original mean growth up to constant factors. | [PDF](friend_tree_transcendence_progress.pdf) · [LaTeX](friend_tree_transcendence_progress.tex) |

These are research drafts dated November 23–24, 2026. The repository includes
written proofs, internal dependency audits, and reproducible finite
calculations. It does not claim external peer review or proof-assistant
formalization.

## Original random friend tree

At each step, choose an existing vertex uniformly, choose one of its
neighbours uniformly, and attach a new vertex to that neighbour. Let `C_n`
be the number of nonleaf vertices. The existence of the deterministic
exponent `mu`, and the initial bracket `0.5650 <= mu <= 0.5665`, are inputs
from [Can Uzay's proof and certificate repository](https://github.com/uzay-eth/friend-tree-exponent).
The model originates in [Krapivsky and Redner (2017)](https://arxiv.org/abs/1706.01514).

The first manuscript establishes the following results using those explicit
inputs.

1. **Exact characterization.** In the inert-parent newborn process, let
   `A_m(s)` be the expected sum of `exp(-s * birth_time)` over genealogical
   generation `m`. The limit `r(s) = lim_m A_m(s)^(1/m)` exists, is positive,
   continuous and strictly decreasing, and has its unique crossing at
   `r(mu) = 1`.
2. **Uniform boundary control.** For the discounted core-count resolvent,
   adding one leaf at the retained root has a bound independent of the size
   and shape of the existing finite component. A subcritical disagreement
   exploration proves this bound.
3. **Effective computability.** A dovetailed search of finite rational lower
   and upper certificates terminates with a bracket of any prescribed
   positive rational width. A rational series for `mu` follows, with a
   certified remainder after each completed stage. No useful running-time
   bound or implemented high-precision solver for this search is claimed.
4. **Boundary robustness.** For each fixed finite bound `Q`, the uniform
   infimum and supremum of continuous-time mean growth over the specified
   predictable root-leaf input policies `0 <= q_t <= Q` both have exponent
   `mu`. This statement is about the explicitly defined boundary policies.
5. **Sharper certificate.** A constant-per-core correction to the upstream
   potential proves

   ```text
   0.5650 <= mu <= 2832242711 / 5000000000 = 0.5664485422.
   ```

   This narrows the upstream interval by about 3.43%. The finite rational
   inequalities and their analytic all-degree extensions are both documented.

The precise proof dependencies are in
[the original-model audit](docs/original_proof_dependencies.md). The numerical
improvement reuses and credits the upstream potential tables; it does not
claim a new independent construction of those tables.

## Local redirection models

The companion paper studies `VAN(omega)`, including `PAN = VAN(0)` and
`DAN = VAN(1)`, for finite `omega >= 0`. These are the models introduced by
[Hartle, Krapivsky, Redner, and Zhang](https://arxiv.org/abs/2604.01540).
Their characteristic equation is

$$
F(s)=\int_0^1 x^s e^{x-1}\,dx
=\frac{(1-s)(s+\omega)}{\omega+(1-\omega)s},\qquad 0<s<1.
$$

The manuscript proves the exact probabilistic identification of the unique
root `alpha_omega`, the almost-sure limit
`C_n / n^alpha_omega -> Z` with `0 < Z < infinity` for every finite tree seed with at least two vertices,
and computability for computable `omega`. For algebraic `omega`, a
Siegel–Shidlovskii specialization proves that `alpha_omega` is irrational.
The characteristic equation is credited to Hartle and coauthors; its
appearance here is not a priority claim.

The [local-model audit](docs/local_model_proof_audit.md) records the
branching-process and arithmetic inputs. The exact example brackets are in
[verification/van_root_checks.json](verification/van_root_checks.json).

## Arithmetic and exact root representations

The third manuscript studies the first proper promotion from the original
inert newborn, including its null stub events. Its exact discounted weights
are

$$
t_n(s)=\frac{(n!)^2}{\prod_{j=1}^n[j^2+(s+2)j+s]},\qquad
\Phi(s)=\sum_{n\ge1}t_n(s)=\mathbb E e^{-s\tau}.
$$

It gives a positive rational reduction, classifies rational telescopes
(they exist exactly at positive integer `s`), and constructs rational
enclosures of width `O_s(M^(-s-5))`. For positive algebraic `s`, writing
`vartheta = (s + sqrt(s^2+4))/2` and `D = [Q(vartheta):Q]`, it proves the
absolute logarithmic height asymptotic

$$
h(t_n(s))=\left(2-\frac2D\right)n\log n+O_s(n).
$$

This determines exactly when the two natural generating functions satisfy
the `E`- and `G`-function arithmetic conditions. The note also states an
equivalent specialization target for transcendence of the local exponents
and checks the scope of the relevant classical `E*`-function theorem.

The continuation then uses the full-environment lower-certificate theorem
to construct signed integer polynomials `P_(m,R,N)`. An explicit omitted
history proves `P_(m,R,N)(mu) > 0`, with quantitative lower bounds and
degree/height bounds. The largest nonnegative roots of explicit product
polynomials form an increasing sequence `xi_h < mu` with `xi_h -> mu`.
The corresponding normalized finite pressure residuals decrease to
`1-r_infty(s)` and remain strictly positive at `mu` before tending to zero.
Their compact convergence is qualitative; no error rate in `h` is proved.
The literal cleared polynomial values grow rather
than become small arithmetic forms. A stronger population-only construction
now settles the normalization issue for its entire family: eliminate all
null rings, remove every common polynomial factor, and divide out all
integer content. The resulting primitive numerators satisfy

$$
p_{m,N}(\mu)>1,\qquad
\min_{1\le m\le N}\log p_{m,N}(\mu)=N\log N+O(N).
$$

Every reachable simple pole has a nonzero residue of prescribed sign.
Thus this is an exact reduced-denominator result, not an artifact of a
coarse denominator clearer. The stronger algebraic-root hierarchy still
converges to `mu`, and each fixed generation coefficient has an explicit
population error `O_(s,m)(N^(-s)(log N)^(s+m-1))`. This error does not
control the subsequent infinite-generation limit defining the pressure.

For the exact pressure, a different iteration has a proved geometric rate:

$$
s_{n+1}=s_n+\frac{63}{400\log2}\log r_\infty(s_n),\qquad
|s_n-\mu|\le(73/82)^n|s_0-\mu|.
$$

This holds throughout the current enclosure and moves monotonically toward
`mu`. It requires exact or certified pressure evaluations; there is no
implemented finite-generation outer error bound for those evaluations.
An equality-safe trisection of the complete strict-certificate searches
also gives a rational series with remainder `O((2/3)^n)` after `n`
completed stages, without a runtime bound for a stage.

Finally, the note restores the exact full-tree beta/Mellin series with
rational coefficients `a_n = E C_n`. Its convergence abscissa is `mu`;
the coefficients retain the entire tree dependence. An exact countable
difference and differential hierarchy, with a finite operator rising-factorial
formula for each coefficient, makes that dependence explicit. No finite
scalar recurrence or finite hypergeometric equation is claimed.
Explicit geometric tails are proved for its
fixed-time generating series and for the full generation resolvent above
a certified upper bound on `mu`. The critical boundary is treated
separately by the directional comparison described below.

### Stronger relations at a fixed discount and in the core-growth class

For the edge-start mean `F_2(t)` and its Laplace transform `M(s)`, define

$$
B_m(s)=\frac1{m!}\int_0^\infty t^m e^{-st}F_2(t)\,dt
       =\frac{(-1)^m}{m!}M^{(m)}(s).
$$

The continuation proves the actual ratio limit

$$
\mu=s-\lim_{m\to\infty}\frac{B_m(s)}{B_{m+1}(s)}
\quad(s>\mu).
$$

At the single rational discount `s=2`, each `B_m` has a positive rational
coefficient series and an explicit rational finite-population tail.
This makes each fixed-index ratio computably enclosable. The new
constant-factor growth theorem also gives an `O_s(m^(-1/2))`
derivative-order error, with a displayed bound in terms of the
core-comparison constants. Those constants have not been numerically
evaluated, so the calculator's individual ratio intervals still do
not by themselves give certified brackets for `mu`.

For the inert generator `L_infty`, let `A_C` consist of functions with
`C <= f <= K_f C` uniformly over all reachable states. Then

$$
\mu=\inf_{f\in\mathcal A_C}\sup_y
       \frac{L_\infty f(y)}{f(y)}.
$$

The continuation now proves attainment of this infimum. There are positive
critical generator eigenfunctions for both the inert and free processes,
uniformly comparable with `C` on states with at least one core.
Consequently the original free-tree mean satisfies

$$
F_2(t)=\Theta(e^{\mu t})\quad(t\ge1),\qquad
\mathbb E C_n=\Theta(n^\mu).
$$

These are two-sided constant-factor bounds, not a limiting amplitude.
The uniform and fixed inert resolvents have two-sided bounds proportional
to `1/(s-mu)` as `s` decreases to `mu`. No meromorphic continuation or
existence of a pole residue is asserted.
The growth class is essential: strictly positive eigenfunctions of the
actual full kernel exist at **every** `s>0`, with no core-ring escape.

Two further exact obstructions delimit proposed reductions. The functions
`C, LC, L^2 C, ...` are linearly independent on finite free trees, ruling
out a finite invariant linear observable space containing `C`. A negative
Hankel determinant rules out a positive real exponential-mixture
representation for `F_2'(t)/2`. These results do not exclude a special
edge-start scalar equation, nonlinear reductions, or other arithmetic
constructions.

### Signed hypergeometric products for the original tree

Fix bipartition signs `sigma_v = ±1`, and write `d_v` for full degrees.
The exact polynomial

$$
P_z(T)=\prod_v\frac{(1+\sigma_v z)_{d_v-1}}{(d_v-1)!}
$$

satisfies `L P_z = 0`: the generator contributions cancel across every
real edge. At fixed population its expectation is `1` for the free edge
and `1+z` for the root-positive inert newborn. Every fixed coefficient is
a true continuous-time martingale; the whole product has this assertion
for real `|z| <= 1`.

Set `J = sum_v sigma_v H_(d_v-1)` and
`S_2 = sum_v H^(2)_(d_v-1)`. Then `J` and `J^2-S_2` are martingales, and

$$
\mathbb E J^2=\mathbb E S_2,\qquad
\mathbb E C\le\mathbb E J^2\le\zeta(2)\mathbb E C.
$$

Thus the original exponent is also the variance-growth exponent of this
signed harmonic martingale in the free model. At every positive integer
`z=k`, `P_k` is a signed integer product of binomial coefficients, supported
on trees whose negative vertices all have degree at most `k`.

For the original free model, a core insertion retains the exact friend
rates while canceling every nonleaf term:

$$
L(x^C P_z)=(x-1)x^C P_z(\Lambda+z\Lambda_\sigma),
\quad
\Lambda_\sigma=\sum_{w\text{ leaf}}\sigma_w\sum_{u\sim w}\frac1{d_u}.
$$

It gives an exact polynomial recurrence for `E[P_z(T_n) C(T_n)]`.
Controlling the remaining neighbor-dependent leaf term is a concrete
target for a critical arithmetic equation; no finite closure is asserted.
The [product-polynomial research note](docs/product_polynomial_targets.md)
records a finite positive-expansion pattern and the precise missing
preservation argument.

These exact cancellations do not yet provide an irrationality argument.
The auxiliary parameter `z` is independent of the critical discount, and
integer state values are averaged with noninteger probabilities. A
comparison process with rational attachment rates preserves all these
product identities, the original two-color Yule law, and any prescribed
finite original prefix, yet has core exponent `1`. An arithmetic transfer
must use additional information in the exact friend attachment rates.

On the original space of bounded functions of full newborn environments,
the critical kernel satisfies

$$
r_{\mathrm{ess}}(\mathcal K_\mu)=r(\mathcal K_\mu)=1.
$$

Every finite full-environment compression is nilpotent. A compact-operator
or finite-determinant reduction therefore requires a justified new space,
quotient, or contribution from infinite population.
An [exact signed renewal reduction](docs/signed_renewal_scope.md) is also
available locally in a generation variable. A new directional disagreement
estimate resolves its fixed-seed boundary gap. For some finite `K`,

$$
\frac1K\le A_m^\infty(\mu)<43\qquad(m\ge0).
$$

Thus `F_mu(z)=sum_m A_m^infinity(mu) z^m` diverges as `z` increases to one,
and the signed germ `B_mu(z)=1-1/F_mu(z)`, continued along the positive
real axis, tends to one. This does not prove that the signed Taylor
series converges up to one: complex zeros of `F_mu` require separate
analysis. Its coefficients also remain infinite kernel values at rational
discounts. The [rational-specialization audit](docs/rational_specialization_audit.md)
states the remaining integer-small-value requirement.

**Irrationality and transcendence of `mu`, and transcendence of the local
exponents, remain unproved.** The transform `Phi` remains just the
first-promotion component, and `Phi(mu)=1` is false. See the
[transcendence dependency audit](docs/transcendence_proof_dependencies.md),
[research targets](docs/RESEARCH_TARGETS.md), and
[exact first-promotion report](verification/first_promotion_checks.json).

## Questions still open in this work

- Irrationality or transcendence of the **original** exponent `mu`.
- Transcendence of the local-model exponents `alpha_omega`.
- A practical, certified arbitrary-precision solver for the original exponent.
- A finite special-function equation for the original exponent with the
  specialization and nonvanishing properties required for an arithmetic proof.
- A limiting mean amplitude, or a positive almost-sure power-law amplitude,
  beyond the proved constant-factor mean bounds for the original process.

The [research targets](docs/RESEARCH_TARGETS.md) distinguish these goals from
the completed arguments. In particular, computability and a positive Mellin
kernel do not by themselves imply irrationality.

## Reproduce the calculations

The quick suite uses Python 3.10 or later and the standard library:

```bash
python3 scripts/run_checks.py
```

The full original-model certificate check also needs a C compiler with
OpenMP and GMP development headers. It fetches hash-pinned upstream files,
builds the certificate in an ignored cache, verifies the upstream
inequalities, and checks the corrected vertex rows:

```bash
python3 scripts/verify_bound.py
```

See [verification instructions](docs/verification.md) for the scope, commands,
dependencies, and reference reports. See [upstream provenance](docs/UPSTREAM.md)
for immutable revisions and file hashes. Re-running the same upstream
checker is described as reproduction, not as an independent implementation.

Build all three manuscripts with a standard LaTeX installation:

```bash
python3 scripts/build_papers.py
```

To build only the transcendence continuation, add `--paper transcendence`.

The build tool writes the PDFs at the repository root and keeps temporary
files in `build/papers/`. It rejects unresolved references and overfull boxes.
The GitHub workflows run these commands when the repository is hosted there;
their presence is not a claim that a remote run has occurred.

## Citation, attribution, and license

Use [CITATION.cff](CITATION.cff) for project metadata and cite the appropriate
manuscript for its mathematical results. Original materials in this project
are under the [MIT license](LICENSE). Downloaded upstream verification code
retains Can Uzay's MIT notice; upstream proof text has its own CC BY 4.0
license and is cited rather than bundled. See
[third-party notices](THIRD_PARTY_NOTICES.md).

AI tools assisted with proof exploration, literature checking, code, and
manuscript preparation. The papers present the arguments and dependencies
explicitly so they can be checked independently.
