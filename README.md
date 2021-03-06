![password-stretcher](https://user-images.githubusercontent.com/20261699/117364575-14a5d980-ae8c-11eb-815d-32827cc5297b.png)

**Generate disgusting quantities of passwords from websites, files, or stdin.** Compliments [password-smelter](https://github.com/thetechromancer/password-smelter).

## Installation
~~~
$ pip install password-stretcher
~~~

## Basics:
`password-stretcher` mutates a list of words, prioritizing the most probable mutations and spreading them evenly across all of the input. By default, output is capped at 100 million words or 1000x times the input, whichever is larger.

### Aren't hashcat rules better?
Hashcat rules are great for quickly covering the most probable mutations of a password. `password-stretcher` can cover them all. This is useful if you KNOW or HEAVILY SUSPECT that the password is a variation of a specific word or list of words, but you haven't been able to crack it using hashcat rules.

When enabling `--leet` or `--capswap` mutations, you can be sure that `password-stretcher` will generate **every possible mutation**. Even when you `--limit` the results, it will prioritize the most probable ones. Here, you can see that enabling both `--leet` and `--capswap` on a single word ("pass") results in 96 mutations, beginning with the simplest and gradually increasing in complexity:
~~~
$ echo pass | password-stretcher --leet --capswap | tr '\n' ' '
[+] Reading input wordlist... read 1 words 
[*] Output capped at 100,000,000 words
[+] Mutations allowed per word:
       leet            7,071
       capitalization  14,142
[+] 96 words written (480B)    
pass PASS Pass pAss PAss paSs PaSs pASs PASs pasS PasS pAsS PAsS paSS
PaSS pASS p@ss P@SS P@ss P@Ss p@Ss p@sS P@sS p@SS pas5 PAS5 Pas5 pAs5
PAs5 paS5 PaS5 pAS5 p@s5 P@S5 P@s5 p@S5 pas$ PAS$ Pas$ pAs$ PAs$ paS$
PaS$ pAS$ p@s$ P@S$ P@s$ p@S$ pa5s PA5S Pa5s Pa5S pA5s PA5s pa5S pA5S
p@5s P@5S P@5s p@5S pa55 PA55 Pa55 pA55 p@55 P@55 pa5$ PA5$ Pa5$ pA5$
p@5$ P@5$ pa$s PA$S Pa$s Pa$S pA$s PA$s pa$S pA$S p@$s P@$S P@$s p@$S
pa$5 PA$5 Pa$5 pA$5 p@$5 P@$5 pa$$ PA$$ Pa$$ pA$$ p@$$ P@$$
~~~

<br>

## Example 1: Generate 10 million passwords from three words
~~~
$ echo -e 'normal\nenglish\nwords' | password-stretcher --leet --capswap --permutations 2 --limit 10M
[+] Reading input wordlist... read 3 words 
[*] Input wordlist after permutations: 12
[+] Mutations allowed per word:
       leet            645
       capitalization  1,290
words
WORDS
Words
w0rds
W0RDS
...
normal
NORMAL
Normal
n0rmal
N0RMAL
...
english
ENGLISH
English
3nglish
3NGLISH
...
englishenglish
englishwords
englishnormal
wordsenglish
wordswords
wordsnormal
normalenglish
normalwords
normalnormal
...
~~~

## Example 2: Generate 10 million passwords from a website
~~~
$ password-stretcher -i 'https://wikipedia.org' --leet --limit 10M > wordlist.txt
[+] Spidered 291 pages
[+] Reading input wordlist... read 172,629 words.
[*] Output capped at 10,000,000 words
[+] Mutations allowed per word:
     - leet:           57
[+] 9,792,383 words written (152.36MB)
~~~

## Example 3: Generate passwords from a codebase
~~~
$ egrep -h -RIio '\b[a-z]+\b' 2>/dev/null | password-stretcher --cap > wordlist.txt
~~~

## Example 4: Pair with hashcat rules because yes
~~~
$ echo password | password-stretcher --capswap --leet | hashcat -r OneRuleToRuleThemAll.rule ...
~~~

## Usage:
~~~
$ password-stretcher --help
usage: password-stretcher [-h] [-i  [...]] [--limit LIMIT] [-L] [-c] [-C] [-p] [-dd] [-P INT] [--minlength 8] [--maxlength 8] [--mincharsets 3]
                          [--charsets {numeric,loweralpha,upperalpha,special} [{numeric,loweralpha,upperalpha,special} ...]] [--regex '$[a-z]*^'] [--spider-depth SPIDER_DEPTH]
                          [--user-agent USER_AGENT]

FETCH THE PASSWORD STRETCHER

optional arguments:
  -h, --help            show this help message and exit
  -i  [ ...], --input  [ ...]
                        input website or wordlist(s) (default: STDIN)
  --limit LIMIT         limit length of output (default: max(100M, 1000x input))

mangling options:
  -L, --leet            "leetspeak" mutations
  -c, --cap             common upper/lowercase variations
  -C, --capswap         all possible case combinations
  -p, --pend            append/prepend common digits & special characters
  -dd, --double         double each word (e.g. "Pass" --> "PassPass")
  -P INT, --permutations INT
                        max permutation depth (careful! massive output)

password complexity filters:
  --minlength 8         minimum password length
  --maxlength 8         maximum password length
  --mincharsets 3       must have this many character sets
  --charsets {numeric,loweralpha,upperalpha,special} [{numeric,loweralpha,upperalpha,special} ...]
                        must include these character sets
  --regex '$[a-z]*^'    custom regex

spider options:
  --spider-depth SPIDER_DEPTH
                        maximum website spider depth (default: 1)
  --user-agent USER_AGENT
                        user-agent for web spider
~~~