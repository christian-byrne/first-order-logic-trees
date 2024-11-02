BNF for first-order logic

```bnf
<expr> ::= <expr> → <disjunct>
         | <disjunct>

<disjunct> ::= <disjunct> ∨ <conjunct>
             | <conjunct>

<conjunct> ::= <conjunct> ∧ <quantified>
             | <quantified>

<quantified> ::= (<quantifier><variable>)+ <scope>

<scope> ::= <negation> 
          | <predicate>
          | (<expr>)

<quantifier> ::= ∀ | ∃

<negation> ::= ¬<scope>

<predicate> ::= <relation>(<term>, <term>, ...)
             | <term> = <term>
             | <term> ≠ <term>
             | True
             | False

<term> ::= <function>(<term>, <term>, ...)
          | <constant>
          | <variable>
          | (<expr>)

<relation> ::= P | Q | R | ...

<variable> ::= x | y | z | ...

<constant> ::= a | b | c | ...

<function> ::= f | g | h | ...
```





