## Glossary

- **antecedent**  
  The sentence on the left side of a conditional.

- **anti-symmetry**  
  The property a relation $R$ has iff for no two different $x$ and $y$, $R(x, y)$ and $R(y, x)$ both hold.

- **argument**  
  A connected series of sentences, divided into premises and conclusion.

- **atomic sentence**  
  An expression used to represent a basic sentence; a sentence letter in TFL, or a predicate symbol followed by names in FOL.

- **biconditional**  
  The symbol $\leftrightarrow$, used to represent words and phrases that function like the English phrase "if and only if"; or a sentence formed using this connective.

- **bound variable**  
  An occurrence of a variable in a formula which is in the scope of a quantifier followed by the same variable.

- **complete truth table**  
  A table that gives all the possible truth values for a sentence (of TFL) or sentences in TFL, with a line for every possible valuation of all sentence letters.

- **completeness**  
  A property held by logical systems if and only if $\models$ implies $\vdash$.

- **conclusion**  
  The last sentence in an argument.

- **conclusion indicator**  
  A word or phrase such as "therefore" used to indicate that what follows is the conclusion of an argument.

- **conditional**  
  The symbol $\rightarrow$, used to represent words and phrases that function like the English phrase "if...then..."; a sentence formed by using this symbol.

- **conjunct**  
  A sentence joined to another by a conjunction.

- **conjunction**  
  The symbol $\land$, used to represent words and phrases that function like the English word "and"; or a sentence formed using that symbol.

- **conjunctive normal form (CNF)**  
  A sentence which is a conjunction of disjunctions of atomic sentences or negated atomic sentences.

- **connective**  
  A logical operator in TFL used to combine sentence letters into larger sentences.

- **consequent**  
  The sentence on the right side of a conditional.

- **consistency**  
  Sentences are jointly consistent iff the contradiction $\bot$ cannot be proved from them.

- **contingent sentence**  
  A sentence that is neither a necessary truth nor a necessary falsehood; a sentence that in some case is true and in some other case, false.

- **contradiction (of FOL)**  
  A sentence of FOL that is false in every interpretation.

- **contradiction (of TFL)**  
  A sentence that has only Fs in the column under the main logical operator of its complete truth table; a sentence that is false on every valuation.

- **disjunct**  
  A sentence joined to another by a disjunction.

- **disjunction**  
  The connective $\lor$, used to represent words and phrases that function like the English word "or" in its inclusive sense; or a sentence formed by using this connective.

- **disjunctive normal form (DNF)**  
  A sentence which is a disjunction of conjunctions of atomic sentences or negated atomic sentences.

- **domain**  
  The collection of objects assumed for a symbolization in FOL, or that gives the range of the quantifiers in an interpretation.

  It represents the set of all elements that can be quantified over or that the variables in the logical system can refer to within a given model.

  When formally defining a model in FOL, it is written as:

  $$
  M := \langle D, I \rangle
  $$

  where $D$ is the domain of discourse or 'universe', a non-empty set of objects, and $I$ is the interpretation function which maps constants, functions, and predicates to elements, functions, and relations over $D$.

- **domain expansion**  
  Domain Expansion (or Domain Extension) refers to the process of enlaring the domain $D$ to include additional elements. A new interpretation may need to be defined for predicates, functions, and constants, extending their meaning to the new elements in the domain.

  In formal terms, if $M := \langle D, I \rangle$ is a model, and we want to extend the domain to a new domain $D'$ (where $D \subset D'$), we would create an extended model:
  
  $$
  M' := \langle D', I' \rangle
  $$
  
  where $I'$ is an extension of $I$ that interprets the additional elements in $D'$ as well. 
  
  This approach allows FOL statements to be evaluated within a larger context without altering the original structure's properties within $D$. 

- **empty predicate**  
  A predicate that applies to no object in the domain.

- **equivalence (in FOL)**  
  A property held by pairs of sentences of FOL if and only if the sentences have the same truth value in every interpretation.

- **equivalence (in TFL)**  
  A property held by pairs of sentences if and only if the complete truth table for those sentences has identical columns under the two main logical operators, i.e., if the sentences have the same truth value on every valuation.

- **existential quantifier**  
  The symbol $\exists$ of FOL used to symbolize existence; $\exists x F(x)$ is true iff at least one member of the domain is $F$.

- **formula**  
  An expression of FOL built according to the inductive rules.

- **free variable**  
  An occurrence of a variable in a formula which is not a bound variable.

- **functional completeness**  
  Property of a collection of connectives which holds iff every possible truth table is the truth table of a sentence involving only those connectives.

- **inconsistency**  
  Sentences are inconsistent iff the contradiction $\bot$ can be proved from them.

- **interpretation**  
  A specification of a domain together with the objects the names pick out and which objects the predicates are true of.

- **invalid**  
  A property of arguments that holds when the conclusion is not a consequence of the premises; the opposite of valid.

- **joint possibility**  
  A property possessed by some sentences when they are all true in a single case.

- **main logical operator**  
  The operator used last in the construction of a sentence (of TFL) or a formula of FOL.

- **metalanguage**  
  The language logicians use to talk about the object language. In this textbook, the metalanguage is English, supplemented by certain symbols like metavariables and technical terms like "valid".

- **metavariables**  
  A variable in the metalanguage that can represent any sentence in the object language.

- **model**  
  A model $M$ for a set of sentences $\Gamma$ is a pair $\langle D, I \rangle$ where $D$ is a non-empty set and $I$ is an interpretation function that assigns meanings to the constants, functions, and predicates in $\Gamma$.

  A model is a way of making the sentences true or false.

- **monadic predicate**
  A predicate that takes only one argument.

- **name**  
  A symbol of FOL used to pick out an object of the domain.

- **necessary equivalence**  
  A property held by a pair of sentences that, in every case, are either both true or both false.

- **necessary falsehood**  
  A sentence that is false in every case.

- **necessary truth**  
  A sentence that is true in every case.

- **negation**  
  The symbol $\neg$, used to represent words and phrases that function like the English word "not".

- **object language**  
  A language that is constructed and studied by logicians. In this textbook, the object languages are TFL and FOL.

- **predicate**  
  A symbol of FOL used to symbolize a property or relation.

- **premise**  
  A sentence in an argument other than the conclusion.

- **premise indicator**  
  A word or phrase such as "because" used to indicate that what follows is the premise of an argument.

- **provable equivalence**  
  A property held by pairs of statements if and only if there is a derivation which takes you from each one to the other one.

- **reflexivity**  
  The property a relation $R$ has iff for any $x$, $R(x, x)$ holds.

- **satisfiability (in FOL)**  
  A property held by a sentence of FOL if and only if some interpretation makes all the sentences true.

- **satisfiability (in TFL)**  
  A property held by sentences if and only if the complete truth table for those sentences contains one line on which all the sentences are true, i.e., if some valuation makes all the sentences true.

- **scope**  
  The subformula of a sentence (of TFL) or a formula of FOL for which the main logical operator is the operator.

- **sentence (of FOL)**  
  A formula of FOL which has no free variables.

- **sentence (of TFL)**  
  A string of symbols in TFL that can be built up according to the inductive rules.

- **sentence letter**  
  A letter used to represent a basic sentence in TFL.

- **set equality**
  For two sets $A$ and $B$, $A = B$ if and only if every element of $A$ is an element of $B$ and every element of $B$ is an element of $A$.

  In formal terms, $A = B$ if and only if $\forall x (x \in A \leftrightarrow x \in B)$.

  Alternatively, $A = B$ if and only if $A \subseteq B$ and $B \subseteq A$.

- **sound**  
  A property of arguments that holds if the argument is valid and has all true premises.

- **soundness**  
  A property held by logical systems if and only if $\vdash$ implies $\models$.

- **substitution instance**  
  The result of replacing every free occurrence of a variable in a formula with a name.

- **symbolization key**  
  A list that shows which English sentences are represented by which sentence letters in TFL.

- **symmetry**  
  The property a relation $R$ has iff it is the case that whenever $R(x, y)$ holds, so does $R(y, x)$.

- **tautology**  
  A sentence that has only Ts in the column under the main logical operator of its complete truth table; a sentence that is true on every valuation.

- **term**  
  Either a name or a variable.

- **theorem**  
  A sentence that can be proved without any premises.

- **transitivity**  
  The property a relation $R$ has iff it is the case that whenever $R(x, y)$ and $R(y, z)$ then also $R(x, z)$.

- **truth value**  
  One of the two logical values sentences can have: True and False.

- **truth-functional connective**  
  An operator that builds larger sentences out of smaller ones and fixes the truth value of the resulting sentence based only on the truth value of the component sentences.

- **universal quantifier**  
  The symbol $\forall$ of FOL used to symbolize generality; $\forall x F(x)$ is true iff every member of the domain is $F$.

- **valid**  
  A property of arguments where the conclusion is a consequence of the premises.

- **validity (of arguments in FOL)**  
  A property held by arguments; an argument is valid if and only if no interpretation makes all premises true and the conclusion false.

- **validity (of arguments in TFL)**  
  A property held by arguments if and only if the complete truth table for the argument contains no rows where the premises are all true and the conclusion false.

- **valuation**  
  An assignment of truth values to particular sentence letters.

- **variable**  
  A symbol of FOL used following quantifiers and as placeholders in atomic formulas; lowercase letters between $s$ and $z$.
