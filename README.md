## Decrypting Messages with MCMC
#### Proposed Solution

###### 1. Give formulas for the maximum likelihood estimate of these probabilities as functions of counts of numbers of occurrences of symbols and pairs of symbols. Compute and report these estimated probabilities in a table.

![equation](https://latex.codecogs.com/gif.latex?C%28w%29%20%3D%20%5Ctext%7Bcount%20of%20%7Dw%20%5C%5C%20C%28w_1%2Cw_2%29%20%3D%20%5Ctext%7Bcount%20of%20bigram%20%7D%20w_1%2Cw_2%20%5C%5C%20P%28w%29%20%3D%20%5Cfrac%7BC%28w%29%7D%7BN%7D%20%5C%5C%20P%28w_2%7Cw_1%29%20%3D%20%5Cfrac%7BC%28w_1%2Cw_2%29%7D%7BC%28w_1%29%7D)

Where N is the total number of symbols in text.

##### Unigram probabilities:

| = |  | - | , | ; | : | ! | ? | / | . | ' | " | ( | ) | [ | ] | * | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0.000001 | 0.164806 | 0.000587 | 0.012784 | 0.000367 | 0.000325 | 0.001258 | 0.001005 | 0.000009 | 0.009894 | 0.000000 | 0.000000 | 0.000215 | 0.000215 | 0.000000 | 0.000000 | 0.000096 | 0.000058 | 0.000126 | 0.000047 | 0.000019 | 0.000007 | 0.000017 | 0.000018 | 0.000013 | 0.000062 | 0.000012 | 0.064964 | 0.011106 | 0.019747 | 0.037910 | 0.100489 | 0.017594 | 0.016448 | 0.053650 | 0.055202 | 0.000825 | 0.006548 | 0.030934 | 0.019756 | 0.059025 | 0.060915 | 0.014592 | 0.000747 | 0.047567 | 0.052203 | 0.072558 | 0.020638 | 0.008680 | 0.018974 | 0.001405 | 0.014817 | 0.000765 |


##### Bigram probabilites:

![Transition Matrix](cond.png)

###### 2. Are the latent variables σ(s) for different symbols s independent?

No, they are not independent, *P(σ(s1)=e1,σ(s2)=e1)=0*

###### 3. Write down the joint probability of *e1e2···en* and *s1s2···sn* given *σ*.

The joint probability of *e1e2···en* and *s1s2···sn* given *σ*, is the likelihood:

![equation](https://latex.codecogs.com/gif.latex?P%28e_1%2C...%2Ce_n%20%7C%20%5Csigma%29%20%3D%20P_%7B%5Csigma%5E%7B-1%7D%28e_%7B1%7D%29%7D%5Cprod_%7Bi%3D1%7D%5E%7Bn-1%7D%20P_%7B%5Csigma%5E%7B-1%7D%28e_i%20%7Ce_%7Bi&plus;1%7D%29%7D)

###### 4. What are the proposal distributions and acceptance probabilities?

The proposal distribution is the uniform distribution over the mappings of the symbols.
The acceptance probabilities is:

![equation](https://latex.codecogs.com/gif.latex?P_%7Bacc%7D%28%5Csigma%2C%5Csigma%27%29%20%3D%20min%5C%7B%5Cfrac%7BP%28e_1%2C...%2Ce_n%7C%5Csigma%27%29%7D%7BP%28e_1%2C...%2Ce_n%7C%5Csigma%29%7D%2C1%5C%7D)

###### 5. Report the current decryption of the first 60 symbols after every 100 iterations. 

The sampling procedure is restarted several times and the best result is collected, reducing the dipendency from the random starting point of the inital sampled proposal. 
Giving transition matrix init values equal to 1 avoid zero probabilities, ie to give zero probability of unseen bigrams (Laplace smoothing).

[Reported iterations](reported_iterations.txt)

###### 6. Is the chain mentioned above necessarily ergodic?

No, some probabilities are zero and so there is no guarantee that is possible to reach all the possible states. It is possible to fix it setting all the probabilties equal zero to a small initial value, ensuring a sequence of transitions of non-zero probability from any state to another.



