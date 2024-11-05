## Glossary

- **Model**
  A model for $L_{FO}$ is a pair $\mathcal{M} = \langle \mathcal{D}, \mathcal{I} \rangle$ where:
    - $D$ is a non-empty set of *objects*
    - $I$ is an interpretation function, where
      - $I(c) \in D$ for each individual constant symbol $c$
      - $I(P) \subseteq D^n$ for each $n$-ary predicate symbol $P$

- **Assignment Function**
  An assignment function, say $g$, maps variables (like $x, y, z$) to elements in the domain $D$. When we evaluate expressions, the assignment function can vary, changing the values of these variables as needed for quantification or substitution.

- **Interpretation**
  An interpretation of a first-order language $L_{FO}$ consists of a model $\mathcal{M}$ and an assignment function $g$ that assigns elements of the domain to variables. The interpretation specifies the meaning of the symbols in the language, such as constants, predicates, and functions, by mapping them to elements of the domain and defining how they interact with each other.

- **Assignment vs Interpretation**
  The interpretation function is fixed within a given model, meaning it does not change across different evaluataions or assignemnts of variables. Inversely, when we evaluate expressions, the assignemnt function can vary (changing the values of these variables as needed for quantification or substitution).

- **Variant**
  (of an assignment function)

  $g[\alpha]h$ "h is an $\alpha$-variant of $g$"
  
  Given assignment $g$ and variables $\alpha$, $h$ is an $\alpha$-variant of $g$ if $h$ and $g$ agree on all variables except those in $\alpha$ ($h(B) = g(B)$ for all $B \in \text{dom}(g) \setminus \alpha$).

  I.e., if $h$ and $g$ are dicts, they have all the same entries except for those whose key is in $\alpha$, where one dict may have a different value for that key or may not have that key at all.

  Where $d$ is an object in $D$, $h$ is the $d/x$-variant of $g$ iff $g[x]h$ ($g$ and $h$ map to all the same things except for key $x$) and $h(x) = d$.

  I.e., $h$ is the $d/x$-variant of $g$ means $h$ is the dict $g$ with the added entry of $x: d$.

  Alternatively denoted as $h = g[x \mapsto d]$ or $h = g[x/d]$.

- **Semantic Entailment of Sentences in Modal Logic**
  $\Vdash_{M, g} \phi$ means formula $\phi$ is true in model $M$ under assignment $g$.

  $\Vdash_{M, g|} P(t)$ iff $[t]_{M, g} \in I(P)$

  $[t]_{M, g} \in I(P)$ means term $t$ is in the extension of predicate $P$ in model $M$ under assignment $g$.

  $$
  [t]_{M, g} = \begin{cases}
    I(t) & \text{if $t$ is a constant} \\
    g(t) & \text{if $t$ is a variable}
  \end{cases}
  $$

- **Semantic Entailment of Existentially Quantified Formulas**
  $\Vdash_{M, g} \exists x \phi$ iff there is some $d \in D$ such that $\Vdash_{M, g[x \mapsto d]} \phi$.

  I.e., there is some variant $h = g[x \mapsto d]$ such that $\Vdash_{M, h} \phi$.

- **Semantic Entailment of Universally Quantified Formulas**
  $\Vdash_{M, g} \forall x \phi$ iff for all $d \in D$, $\Vdash_{M, g[x \mapsto d]} \phi$.

  I.e., for all variants $h = g[x \mapsto d]$, $\Vdash_{M, h} \phi$.

- **Free for Substitution**
  Let $[t/x]\phi$ ("$t$ for $x$ in $\phi$") be the result of substituting all *free* occurrences of $x$ in $\phi$ with $t$.

  $[a/x] P(x)$ is $P(a)$.

  $[y/x] P(x)$ is $P(y)$.

  Does not work on free variables, so $[a/x] \exists x P(x)$ is just $\exists x P(x)$.

  It is ill-advised to substitute inside the scope of a quantifier $Q$ in $\phi$ if doing so would create a new binding where that binding wouldn't have been present before (I.e., don't introduce new bindings).

  $[x/y] \exists x P(x, y)$ is $\exists x P(x, x)$. This is bad because we've introduced a bound variable in the place of a free variables (i.e., introduced a new binding/mapping that did not exist before).

- **Entailment in Modal Logic**
  For any set of formulas $A$ and formula $\psi$:

  $A \Vdash \psi$ iff for all models $M$ and every assignment $g$:

  If $\Vdash_{M, g} \phi$ for all $\phi \in A$, then $\Vdash_{M, g} \psi$.


- **Truth**
  Refers to the concept of truth values, typically denoted as either True or False in classical logic.

- **Functional**
  This means that the complex statement’s truth is a result of a function or operation applied to the simpler parts. The logical operators (AND, OR, NOT, etc.) each act like functions that take in truth values and output a single truth value based on a set rule.

- **Truth-Functional Language (TFL)**
  Truth value of a complex proposition (or compound statement) is a **function** of the truth values of its simpler, component propositions. In other words, the truth value of a compound statement is **determined entirely** by the truth values of its parts and the specific logical operators (like AND, OR, NOT) that connect them. This "truth-functional" property makes reasoning in truth-functional logic highly predictable, as each compound statement's truth value can be systematically derived from its components.

- **Atomic Formulas**
  The simplest, indivisible statement that can be evaluated as either true or false. It consists of a predicate applied to a specific number of terms (constants, variables, or functions) without any logical connectives or quantifiers. It can also include an equality relation between two terms. Atomic formulas are the building blocks of more complex formulas in FOL, formed by applying logical operators (like AND, OR, NOT) and quantifiers to these atomic statements. They have no internal logical structure in terms of connectives or quantifiers and are evaluated as units (true or false) based on the interpretation of the predicate and terms in the domain.

- **Main Logical Operator (MLO)**
  The primary logical operator in a formula, which determines the overall structure and truth value of the formula. In a compound statement, the MLO is the operator that connects the simpler parts of the statement (like AND, OR, NOT, etc.). It is the operator that is evaluated first when determining the truth value of a complex formula.

- **Sentence Letters**
  Propositional variables or atomic propositions that represent whole statements with a truth value without involving predicates, functions, or quantifiers. These sentence letters are the basic building blocks of propositional logic (also called truth-functional logic or TFL) and are used as simple placeholders for statements that can either be true or false. While sentence letters are central to propositional logic, they occasionally carry over to First-Order Logic (FOL) to provide basic, indivisible statements. These statements do not describe relationships or properties involving objects in a domain but instead act as true/false values assigned directly, much like in propositional logic.

- **Validity**
  An FOL Sentence $A$ is a *validity* iff $A$ is true in every interpretation; i.e., $\Vdash A$. 
    - Validities are to FOL what tautologies are to TFL. 
    - They are sentences that are true under all possible interpretations, regardless of the specific objects, predicates, or functions involved. 
    - In other words, a sentence is valid if it holds true universally, regardless of the specific details of the interpretation. Validity is a key concept in logic, as it represents a kind of statement that is necessarily true based on the logical structure of the sentence itself.
    - To show that $A$ is not a validity, it suffices to find an interpretation in which $A$ is false.

- **Contradiction**
  $A$ is a *contradiction* iff $A$ is false in every interpretation; i.e., $\Vdash \neg A$.
    - To show that $A$ is not a contradiction, it suffices to find an interpretation in which $A$ is true.

- **Valid**
  $A_1, A_2, ..., A_n \therefore B$ is *valid in FOL* iff there is no interpretation in which all of the premises are true and the conclusion is false; i.e., $A_1, A_2, ..., A_n \Vdash B$. It is **Invalid** otherwise.

- **Equivalent**
  Two FOL Sentences $A$ and $B$ are *equivalent* iff they are true in exactly the same interpretations as each other; i.e., both $A \Vdash B$ and $B \Vdash A$.
    - To show that $A$ and $B$ are not logically equivalent, it suffices to find an interpretation in which one is true and the other is false.

- **Jointly Satisfiable**
  A set of FOL Sentences $A_1, A_2, ..., A_n$ is *jointly satisfiable* iff some interpretation makes all of them true; i.e., there is an interpretation $I$ such that $I \Vdash A_1, A_2, ..., A_n$. They are **Jointly Unsatisfiable** if there is no such interpretation.

- **Semantic Entailment in FOL**
  $A_1, A_2, ..., A_n \Vdash B$ iff every interpretation that makes all of $A_1, A_2, ..., A_n$ true also makes $B$ true.
    - This is a stronger notion than logical entailment in TFL, as it requires that the entailment holds under all possible interpretations of the FOL sentences.
    - To show that $A_1, A_2, ..., A_n \not \Vdash B$, it suffices to find an interpretation in which all of the premises are true and the conclusion is false.

- **placeholder**
  If some interpretation makes all of $A_1, A_2, ..., A_n$ true and $B$ false, then:
    - $A_1, A_2, ..., A_n \not \Vdash B$
    - $A_1, A_2, ..., A_n \therefore B$ is **Invalid**
    - $A_1, A_2, ..., A_n$ and $\neg B$ are **Jointly Satisfiable**
    - $A_1, A_2, ..., A_n$ does not **Semantically Entail** $B$ in FOL

- **Counter Model** (Counter Interpretation)
  An interpretation that makes all the premises of an argument true and the conclusion false. It is used to show that an argument is invalid or that a set of sentences does not semantically entail another sentence.

- **Operator Precedence**
  1. Parentheses
  2. Predicates (Atomic Formulas)
  3. Negation
  4. Quantifiers
  5. Equality
  6. Conjunction
  7. Disjunction
  8. Conditional
  9. Biconditional


- **Interpretations**
  We defined a valuation in TFL as any assignment of truth and falsity to sentence letters. In FOL, we are going to define an interpretation as consisting of four things:

  1. the specification of a domain;
  2. for each sentence letter we care to consider, a truth value;
  3. for each name that we care to consider, an assignment of exactly one object within the domain;
  4. for each predicate that we care to consider (apart from ‘=’), a specification of what things (in what order) the predicate is to be true of.


- **Sentences in FOL**
  1. atomic sentences
  2. sentences whose main logical operator is a sentential connective
  3. sentences whose main logical operator is a quantifier

- **Atomic Sentences**
  - **Sentence Letters**: the interpretation specifies a truth value for each sentence letter.
  - $P(a)$ should be true just in case $P(x)$ is true of $a$ which is Aristotle.
  - $P(b)$ should be false just in case $P(x)$ is false of $b$ which is Beyoncé.
  - For an $n$-place predicate $R$, and $n$ names $a_1, a_2, ..., a_n$, the sentence $R(a_1, a_2, ..., a_n)$ is true in an interpretation iff $R$ is true of the objects named by $a_1, a_2, ..., a_n$ (in that order) in that interpretation.
  - $a = b$ is true in an interpretation iff $a$ and $b$ name the very same object in that interpretation.

- **When MLO is a Sentential Connective**
  - **Negation**: $\neg A$ is true in an interpretation iff $A$ is false in that interpretation.
  - **Conjunction**: $A \land B$ is true in an interpretation iff both $A$ and $B$ are true in that interpretation.
  - **Disjunction**: $A \lor B$ is true in an interpretation iff at least one of $A$ and $B$ is true in that interpretation.
  - **Conditional**: $A \to B$ is true in an interpretation iff either $A$ is false or $B$ is true in that interpretation.
  - **Biconditional**: $A \leftrightarrow B$ is true in an interpretation iff either both $A$ and $B$ are true or both $A$ and $B$ are false in that interpretation.
    - Alternatively, $A \leftrightarrow B$ is true in an interpretation iff $A$ and $B$ have the same truth value in that interpretation.

  **Examples**

  > $a = a \land P(a)$

  Predicates (atomic formulas) are evaluated first.

  > $a = a \land true$

  Equality has next highest precedence. $a = a$ is true.

  > $true \land true$

  Conjunction has next highest precedence. Both sides are true.

  > $true$

  *Conclusion*: $a = a \land P(a)$ is true.

- **MLO is a Quantifier**
  - The interpretation $I[d/c]$ is just like the interpretation $I$, except that the name $c$ is assigned the object $d$.
  - An object $d$ **satifies** a formula $A(\ldots, x, x, \ldots)$ in an interpretation $I$ iff $A(\ldots, c, c, \ldots)$ is true in the interpretation $I[d/c]$.
  - **Universal Quantifier**: $\forall x A(\ldots, x, x, \ldots)$ is true in an interpretation iff every object in the domain satisfies $A(\ldots, x, x, \ldots)$.
  - **Existential Quantifier**: $\exists x A(\ldots, x, x, \ldots)$ is true in an interpretation iff there is *some* (at least one) object that satisfies $A(\ldots, x, x, \ldots)$.
    - I.e., $A(\ldots, c, c, \ldots)$ is true in the interpretation $I[d/c]$ for some object $d$ in the domain.

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
