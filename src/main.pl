n(0..10).
substance(s1). cost(s1, 50). efficacy(s1, 40).
substance(s2). cost(s2, 50). efficacy(s2, 50).
substance(s3). cost(s3, 10). efficacy(s3, 1).

relative_efficacy(s1, s2, -20).
relative_efficacy(s1, s3, 0).
relative_efficacy(s2, s3, 10).
relative_efficacy(X, X, 0) :- substance(X).
relative_efficacy(X, Y, E) :- relative_efficacy(Y, X, E).

1 { ammount(X, Y) : n(Y) } 1 :- substance(X).

total_cost(TC) :- TC = #sum{ C * Y, X : substance(X), ammount(X, Y), cost(X, C) }.
bonus_efficacy(X, E) :- relative_efficacy(X, Y, E), ammount(Y, A), A > 0.
total_efficacy(TE) :- BaseEfficacy = #sum{ E * Y, X : substance(X), ammount(X, Y), efficacy(X, E) },
                      BonusEfficacy = #sum{ E * Y, X : substance(X), ammount(X, Y), bonus_efficacy(X, E) }, TE = BaseEfficacy + BonusEfficacy.

:- not #sum{ A, X : substance(X), ammount(X, A) } == 10.

#minimize{ TC : total_cost(TC) }.
#maximize{ TE : total_efficacy(TE) }.

#show ammount/2.
#show total_cost/1.
#show total_efficacy/1.
