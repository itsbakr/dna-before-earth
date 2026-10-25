# Draft email (not sent)

**To:** Caren Marzban (University of Washington), Raju Viswanathan, Ulvi Yurtsever
**Subject:** Question about the prediction intervals in "Earth before life" (Biology Direct 2014, 9:1)

Dear Dr Marzban, Dr Viswanathan and Dr Yurtsever,

I am preparing a re-analysis of Sharov's (2006) genome-complexity clock, and your 2014 paper is central to
it. Before citing your results I want to make sure I understand them correctly, and I would be grateful for
your help with one point.

Applying equations (5) to (9) as printed to Sharov's five points (eukaryotes at 2.05 Gya and mammals at
0.125 Gya, which matches your sample variance of 1.86), I get the following:

- Ordinary least squares. With residual variance SSR/(n−2) and 1.96, the lower edge of the 95% prediction
  band reaches log10(1 bp) at about 8.15 Gya; with a t-quantile on 3 df, at about 7.43 Gya. Figure 2 shows
  about 7.0 Gya.
- λ = 1.14. With equation (9) as printed (last term multiplied by σ_b²), the lower edge reaches 0 at about
  5.6 Gya. I can only reach 4.5 Gya with λ of about 1.31. If the last term uses σ_w² instead, the
  threshold is about 1.42.
- The corrected point estimate reaches 4.5 Gya at λ ≈ 2.68, which matches your "about 2.7".

Could you tell me whether equation (9)'s final term [(βλ)² + V(βλ)]σ_b² is as intended? In particular,
should it involve the measurement-error variance σ_w² rather than σ_b², given that the text describes the
case of a known X? If it is not too much trouble, the code used for Figure 2 would help me reproduce it
exactly.

My reproduction code is public at https://github.com/itsbakr/dna-before-earth (`scripts/run_wp5.py`,
part 3), and I will acknowledge any help in the paper. Thank you for your time.

With best regards,
[Name]
[Affiliation]
