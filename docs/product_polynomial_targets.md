# A finite positive expansion after signed cancellation

This note records a possible next proof target for the **original free friend
tree**. The coefficient positivity below is verified only through population
9. No positivity, real-rootedness, or interlacing theorem for arbitrary
population is asserted, and no irrationality conclusion follows.

## The parameter q

Let

\[
a_n(z)=\mathbb E[P_z(T_n)C(T_n)],\qquad q=1-z^2.
\]

Swapping the two initial edge labels reverses every bipartition sign and
preserves the process law. Thus \(a_n(z)\) is an even polynomial with rational
coefficients. Write \(A_n(q)=a_n(z)\) after the substitution \(z^2=1-q\).
In particular \(A_n(1)=\mathbb EC(T_n)\).

For every \(n\geq3\), the constant coefficient of \(A_n(q)\) is exactly
one. There is also a useful direct divisibility proof. The induced core is
a tree, so \(C-1\) counts its edges. Whenever \(C\geq2\), at least one
core vertex of each sign occurs; hence \(P_z\) contains the factor
\((1+z)(1-z)=q\). Since \(\mathbb EP_z=1\),

\[
a_n(z)-1=\mathbb E[P_z(T_n)(C(T_n)-1)]
\]

is divisible by \(q\). Its expectation is even, proving
\(A_n(q)=1+qH_n(q)\) for some rational polynomial \(H_n\).
This argument does **not** establish that the coefficients of \(H_n\)
are nonnegative.

## Exact finite values

The following are coefficient transforms of the exact original-process
polynomials in the committed [insertion report](../verification/product_insertion_checks.json),
computed by `python3 scripts/check_product_insertions.py --check` through
population 9. Substitute each `z^(2k)` by `(1-q)^k` to reproduce them.

| Population \(n\) | \(A_n(q)\) |
|---|---|
| 3 | \(1\) |
| 4 | \(1+\frac13q\) |
| 5 | \(1+\frac7{12}q\) |
| 6 | \(1+\frac{569}{720}q+\frac1{144}q^2\) |
| 7 | \(1+\frac{25109}{25920}q+\frac{269}{12960}q^2\) |
| 8 | \(1+\frac{4904693}{4354560}q+\frac{1050547}{26127360}q^2+\frac{3011}{26127360}q^3\) |
| 9 | \(1+\frac{662550827}{522547200}q+\frac{401836811}{6270566400}q^2+\frac{2898241}{6270566400}q^3\) |

The tilted promotion polynomials \(V_n(q)=n(A_{n+1}(q)-A_n(q))\)
also have nonnegative coefficients in the available range:

| Population \(n\) before the birth | \(V_n(q)\) |
|---|---|
| 2 | \(2\) |
| 3 | \(q\) |
| 4 | \(q\) |
| 5 | \(\frac{149}{144}q+\frac5{144}q^2\) |
| 6 | \(\frac{925}{864}q+\frac{179}{2160}q^2\) |
| 7 | \(\frac{686381}{622080}q+\frac{508243}{3732480}q^2+\frac{3011}{3732480}q^3\) |
| 8 | \(\frac{73987667}{65318400}q+\frac{149705531}{783820800}q^2+\frac{2175601}{783820800}q^3\) |

These tables are finite evidence, not an inductive argument.

## An exact positive operator identity in another variable

Set

\[
t=\frac{1-z}{1+z},\qquad q=\frac{4t}{(1+t)^2},\qquad
R_T(t)=(1+t)^{n-2}P_z(T).
\]

The rational substitution gives the polynomial identity

\[
R_T(t)=\prod_v\prod_{j=1}^{d_v-1}
\frac{(j+\sigma_v)+(j-\sigma_v)t}{j}.
\]

Every factor has nonnegative coefficients in \(t\). Define

\[
B_n(t)=\mathbb E[C(T_n)R_{T_n}(t)]
      =(1+t)^{n-2}A_n\!\left(\frac{4t}{(1+t)^2}\right).
\]

Color reversal makes \(B_n\) palindromic with respect to degree \(n-2\).
Writing \(A_n(q)=\sum_j b_{n,j}q^j\), one obtains

\[
B_n(t)=\sum_j4^jb_{n,j}t^j(1+t)^{n-2-2j}.
\]

Thus the proposed nonnegativity of the \(q\)-coefficients is precisely
nonnegativity in the usual gamma basis for this palindromic polynomial.

For a tree \(T\), put
\(\Lambda_\pm(T)=\sum_{w:\,d_w=1,\,\sigma_w=\pm1}h_T(w)\).
The exact attachment identity is

\[
B_{n+1}(t)=(1+t)B_n(t)
 +\frac2n\mathbb E\!\left[
 R_{T_n}(t)(\Lambda_+(T_n)+t\Lambda_-(T_n))\right].
\]

Indeed, attachment at \(w\) multiplies \(R_T(t)\) by
\([(d_w+\sigma_w)+(d_w-\sigma_w)t]/d_w\). The terms multiplying
the existing core count sum to \((1+t)B_n\), by product harmonicity.
At a leaf the extra factor is \(2\) or \(2t\), yielding the displayed
promotion term. This proves positivity of its ordinary \(t\)-coefficients,
but does not prove gamma-positivity or a root-preservation property.

## Why a preservation proof must retain adjacency information

There is no nonnegative statewise expansion in \(q\) to average. For
example, on the five-vertex star, the color-symmetrized tilted promotion
polynomial is

\[
q\left(1+\frac{z^2}{6}\right)
=\frac76q-\frac16q^2.
\]

The negative coefficient disappears only after the appropriate full-process
averaging. Likewise, an unbalanced six-vertex double star has symmetrized
product \(q(7/6-q/6)\).

Even the complete single-state polynomial \(P_z\), together with \(C\)
and the color counts, does not determine the next core insertion. Consider
the following two seven-vertex trees, with \(\sigma_0=-1\) and the
remaining signs fixed by their edges:

\[
\begin{aligned}
E(T_1)&=\{01,02,23,04,45,56\},\\
E(T_2)&=\{01,02,03,34,45,56\}.
\end{aligned}
\]

Both have colored degree multisets

\[
\{d_v:\sigma_v=+1\}=\{1,1,2,2\},\qquad
\{d_v:\sigma_v=-1\}=\{1,2,3\},
\]

so both have \(C=4\), the same color counts, and

\[
P_z(T_1)=P_z(T_2)=q^2(1-z/2).
\]

Their leaf rates differ:

\[
(\Lambda_+(T_1),\Lambda_-(T_1))=(5/6,1/2),\qquad
(\Lambda_+(T_2),\Lambda_-(T_2))=(2/3,1/2).
\]

Consequently their color-symmetrized core insertion drifts are respectively

\[
q^2\left(\frac76+\frac16q\right),\qquad
q^2\left(\frac{13}{12}+\frac1{12}q\right).
\]

They differ despite having identical core insertion polynomials before the
birth. Therefore the exact operator identity above does not reduce
statewise to an operator on \(P_z\), \(R_T\), or \(P_zC\) alone.

The missing step is a preservation or positive-expansion argument for the
**averaged pair** consisting of the core insertion and its adjacency-dependent
leaf term. Such an argument would establish a new structural theorem; the
finite tables and the nonnegative ordinary \(t\)-coefficients do not supply it.
