# Copyright 2017 by Adil Iqbal.
# All rights reserved.

"""Provide a tool for testing/demonstrating a Seq object"""

import warnings
from random import Random

from Bio.Seq import Seq
from Bio import Alphabet
from Bio.Alphabet import IUPAC
from Bio.Data import CodonTable
from Bio import BiopythonWarning

random_instance = Random()
anchor_instance = Random()


def testseq(size=30, alphabet=IUPAC.unambiguous_dna, table=1, gc_target=None,
            persistent=True, from_start=True, to_stop=True, stop_symbol="*",
            truncate=True, messenger=False, rand_seed=0):
    """Generate and return a Seq object.

    This function will generate and return a custom Seq object
    using any IUPAC alphabet. These sequences are a faux representation
    of biological data and can be used for testing/demonstration purposes.

    Arguments:
        - size - The number of letters in the generated sequence.
        This preferably accepts an integer value and will attempt
        to convert any input to an integer.
        - alphabet - Any IUPAC alphabet can be used to generate
        the sequence. Defaults to unambiguous DNA.
        - table - An integer value that denotes the NCBI identifier
        of the codon table which will be used in generating the sequence.
        This argument prefers an integer and will attempt to convert
        any input into an integer value.
        - gc_target - The function will attempt to generate a sequence
        with a GC-content equal to the 'gc_target' argument. The argument will
        accept any integer between 0 and 100. Alternatively, if 'gc_target'
        is set to 'None', the 'gc_target' argument will be ignored when
        generating the sequence.
        - persistent - A boolean that, if set to True, will remove
        any stop codons that are generated by chance within the sequence.
        - from_start - A boolean that, if set to True, will ensure
        that the first codon in the generated sequence is a start codon.
        - to_stop - A boolean that, if set to True, will ensure
        that the last codon in the generated sequence is a stop codon.
        - stop_symbol - Single character string that denotes the presence
        of a translated stop codon.  This defaults to the asterisk, "*".
        - truncate - A boolean that, if set to True, will ensure that
        the size of any generated (non-protein) sequence is a multiple of three (3).
        - messenger - A boolean that, if set to True, will ensure that
        any RNA sequence generated will additionally have a 5'-UTR,
        3'-UTR, and a poly-A tail.
        - rand_seed - The seed used to generate the randomized sequence.
        This argument accepts any hashable data value as the seed. If the
        argument is set to None, the sequence will be re-seeded with every
        function call.

    Hey there! We can use the 'testseq' function to quickly generate sequences:

    >>> from Scripts.testseq import testseq
    >>> my_seq = testseq()
    >>> my_seq
    Seq('ATGTCCTCTAATAGTATGGTCGTCTACTGA', IUPACUnambiguousDNA())

    The default size of the generated sequence is 30 letters,
    but you can change that at any time, like so:

    >>> my_seq = testseq(1500)
    >>> len(my_seq)
    1500

    You can generate your sequence using any IUPAC alphabet, like so:

    >>> from Bio.Alphabet import IUPAC
    >>> my_seq = testseq(alphabet=IUPAC.extended_protein)
    >>> my_seq
    Seq('MUQCKTSPOLSNWHTFLFUEYOKVZOYFL*', HasStopCodon(ExtendedIUPACProtein(), '*'))

    You may have noticed that the above sequence starts with Methionine(M) and
    ends in an asterisk(*). That's because of the two arguments 'from_start'
    and 'to_stop' respectively. Curiously, there are no asterisks (or terminators)
    within the sequence either; this is due to the 'persistent' argument.
    The 'from_start', 'to_stop', and 'persistent' arguments are all set to True by default.
    You can read more about what they do in the "Arguments" section above. It's
    useful to note that all three of those arguments involve the use of codon tables!
    When generating your sequence, you can set which codon table you'd like to use:

    >>> my_seq = testseq(table=5)
    >>> my_seq
    Seq('ATGTCCTCTAATAGTATGGTCGTCTACTAA', IUPACUnambiguousDNA())

    Now we can translate our sequence with ease!

    >>> my_seq.translate(table=6)
    Seq('MSSNSMVVYQ', IUPACProtein())

    Oops! We're missing a stop codon. We've generated a sequence using Table 5,
    but translated it using Table 6. Those tables don't share a common stop codon!
    Let's fix that...

    >>> my_seq.translate(table=5)
    Seq('MSSNSMVVY*', HasStopCodon(IUPACProtein(), '*'))

    That's better!

    The 'testseq' function can also attempt to generate sequences with a
    custom GC-content. You can alter your desired GC-content by declaring
    it in the 'gc_target' argument, like so:

    >>> my_seq = testseq(gc_target=60)
    >>> from Bio.SeqUtils import GC
    >>> GC(my_seq)
    50.0

    What happened? Note that in the above example, the sequence is at the
    default size of 30 letters. Since the sequence is generated letter by letter,
    larger sequences will have a tendency to be closer to the desired GC-content
    than smaller sequences. Let's try that again with a much larger sequence:

    >>> my_seq = testseq(size=10000, gc_target=60)
    >>> GC(my_seq)
    61.37613761376138

    Much better! It's also worth noting that the 'gc_target' argument is ignored
    when generating protein sequences.

    Lets revisit the 'size' argument for a moment. You will notice that when
    generating the sequence above, I declared a 'size' of 10000. Lets confirm
    whether that was generated as requested:

    >>> len(my_seq)
    9999

    That may seem like a bug, but it isn't! All non-protein sequences are
    truncated to a multiple of three (3). This is to allow for smooth translation
    from nucleotide to amino-acid alphabets. This behavior is controlled by the
    'truncate' argument, which is set to True by default. Let's see what happens
    when we set it to False:

    >>> my_seq = testseq(10000, truncate=False)
    >>> len(my_seq)
    10000

    The result above seems cleaner, but would result in a 'BiopythonWarning' if
    you translated that sequence. So please be careful when altering the
    'truncate' argument.

    Let us briefly discuss the 'messenger' argument. You can use it to add
    messenger RNA components to a generated RNA sequence. Though, it has
    two caveats. First, the messenger argument is ignored unless an RNA alphabet
    is declared. More importantly though, all mRNA compenents are added to
    the sequence addtionally. Let's look at an example:

    >>> my_seq = testseq(300, alphabet=IUPAC.unambiguous_rna, messenger=True)
    >>> len(my_seq)
    561

    Notice that the sequence requested was 300 letters, however the final length of
    the sequence is 561 letters. Those extra letters are the mRNA components. The
    generated sequence is buried in there, somewhere - and it's exactly 300 letters in size!

    Lastly, lets discuss the sequence generator itself. The sequence is created
    using a pseudo-random number generator which relies on a seed to process
    and spit out random numbers.
    Lets look at an example:

    >>> a = testseq()
    >>> b = testseq()
    >>> a == b
    True

    Since sequence "a" and sequence "b" were both generated using the same seed,
    they ended up being the exact same sequence. We can change that behavior
    to shuffle the seed every time the function is called by setting the
    the 'rand_seed' argument to 'None' (without quotation marks), like so:

    >>> a = testseq(rand_seed=None)
    >>> b = testseq(rand_seed=None)
    >>> a == b
    False

    If you'd like to generate a specific sequence, you can set the
    'rand_seed' argument to any desired hashable data value:

    >>> a = testseq(rand_seed=0.7334)
    >>> b = testseq(rand_seed="Hello World!")
    >>> a == b
    False

    This concludes our discussion. Thanks again for using Biopython!
    Contribution by Adil Iqbal (2017).
    """
    # Set seed, gather data, clean-up logic, validate arguments.
    if rand_seed is None:
        rand_seed = anchor_instance.random()
    random_instance.seed(rand_seed)
    typeof = _SeqType(alphabet)
    if not typeof.rna and messenger:
        warnings.warn("The 'messenger' argument can only be used on RNA alphabets.", BiopythonWarning)
        messenger = False
    if typeof.rna and messenger:
        from_start = True
        to_stop = True
        persistent = True
    if persistent or from_start or to_stop:
        stop_symbol = str(stop_symbol)[0]
        codon_set = _CodonSet(alphabet, table, stop_symbol)
    if gc_target is not None and typeof.protein:
        warnings.warn("The 'gc_target' argument cannot be used with proteins.", BiopythonWarning)
    if gc_target is not None and not typeof.protein:
        gc_target = int(gc_target)
        if gc_target < 0:
            warnings.warn("The 'gc_target' argument must be an integer between 0 and 100."
                          "It's current value '{0}' is invalid and has been set to 0.".format(gc_target),
                          BiopythonWarning)
            gc_target = 0
        if gc_target > 100:
            warnings.warn("The 'gc_target' argument must be an integer between 0 and 100."
                          "It's current value '{0}' is invalid and has been set to 100.".format(gc_target),
                          BiopythonWarning)
            gc_target = 100
        probability_table = _construct_probability_table(alphabet, gc_target)
    size = int(size)
    if not typeof.protein and truncate:
        size -= size % 3
    # Begin generating sequence.
    seq = ""
    for i in range(size):
        if gc_target is not None and not typeof.protein:
            seq += _pick_one(probability_table)
        else:
            roll = random_instance.randint(0, len(alphabet.letters) - 1)
            seq += alphabet.letters[roll]
        if len(seq) >= 3 and len(seq) % 3 == 0 and not typeof.protein and persistent:
            # Replace stop codons with non-stop codons.
            this_codon = seq[-3:]
            if this_codon in codon_set.stop:
                roll = random_instance.randint(0, len(codon_set.nonstop) - 1)
                new_codon = codon_set.nonstop[roll]
                seq = seq[:-3] + new_codon
    # Additional processing of generated sequence.
    x = 3
    if typeof.protein:
        x = 1
    if from_start:
        aug = None
        if typeof.dna:
            aug = "ATG"
        elif typeof.rna:
            aug = "AUG"
        elif typeof.protein:
            aug = "M"
        if aug is not None and aug in codon_set.start:
            start = aug
        else:
            roll = random_instance.randint(0, len(codon_set.start) - 1)
            start = codon_set.start[roll]
        seq = start + seq[x:]
    if to_stop:
        roll = random_instance.randint(0, len(codon_set.stop) - 1)
        stop = codon_set.stop[roll]
        seq = seq[:-x] + stop
    if messenger:
        seq = _add_messenger_parts(seq, size, alphabet, codon_set)
    if typeof.protein and stop_symbol in seq:
        alphabet = Alphabet.HasStopCodon(alphabet, stop_symbol)
    return Seq(seq, alphabet)


def _construct_probability_table(alphabet, gc_target):
    """Assign a probability of being chosen to each nucleotide based on desired GC-content. (PRIVATE)"""
    gc_nt_total = 2
    if alphabet == IUPAC.ambiguous_dna or alphabet == IUPAC.ambiguous_rna:
        gc_nt_total = 3
    probability_table = []
    total = len(alphabet.letters) - gc_nt_total
    for letter in alphabet.letters:
        if letter in ["G", "C", "S"]:
            value = gc_target / gc_nt_total
        else:
            value = (100 - gc_target) / total
        probability_table.append(_Letter(letter, value))
    sum_ = 0
    for letter in range(len(probability_table)):
        sum_ += probability_table[letter].probability_value
    for letter in range(len(probability_table)):
        probability_table[letter].probability_value /= sum_
    return probability_table


def _pick_one(probability_table):
    """Choose a nucleotide based on its probability of being chosen. (PRIVATE)"""
    roll = random_instance.random()
    index = 0
    while roll > 0:
        roll -= probability_table[index].probability_value
        index += 1
    index -= 1
    return probability_table[index].letter


def _add_messenger_parts(seq, size, alphabet, codon_set):
    """Generate and add the 5' UTR, 3' UTR, and PolyA-Tail to an RNA sequence. (PRIVATE)"""
    utr_size = int(size / 3)
    utr5 = ""
    for i in range(utr_size):
        roll = random_instance.randint(0, len(alphabet.letters) - 1)
        utr5 += alphabet.letters[roll]
        if len(utr5) >= 3 and len(utr5) % 3 == 0:
            # Replace start codons with non-start codons.
            this_codon = utr5[-3:]
            for start_codon in codon_set.start:
                if this_codon == start_codon:
                    roll = random_instance.randint(0, len(codon_set.nonstart) - 1)
                    new_codon = codon_set.nonstart[roll]
                    utr5 = utr5[:-3] + new_codon
                    break
    utr3 = ""
    for i in range(utr_size):
        roll = random_instance.randint(0, len(alphabet.letters) - 1)
        utr3 += alphabet.letters[roll]
    roll = random_instance.randint(50, 101)
    poly_a_tail = "A" * roll
    seq = utr5 + seq + utr3 + poly_a_tail
    while len(seq) % 3 != 0:
        seq = seq[:-1]
    return seq


class _SeqType(object):
    """Evaluate alphabet to determine Seq type and return boolean values. (PRIVATE)"""

    def __init__(self, alphabet):
        self.dna = isinstance(alphabet, Alphabet.DNAAlphabet)
        self.rna = isinstance(alphabet, Alphabet.RNAAlphabet)
        self.protein = isinstance(alphabet, Alphabet.ProteinAlphabet)
        if self.dna is True and self.rna is False and self.protein is False:
            pass
        elif self.rna is True and self.dna is False and self.protein is False:
            pass
        elif self.protein is True and self.dna is False and self.rna is False:
            pass
        else:
            raise TypeError("Not a valid IUPAC alphabet.")


class _CodonSet(object):
    """Populate lists of codons from appropriate codon table. Return lists. (PRIVATE)"""

    def __init__(self, alphabet=IUPAC.unambiguous_dna, table=1, stop_symbol="*"):
        self.alphabet = alphabet
        self.table = table
        self.stop_symbol = stop_symbol
        self.typeof = _SeqType(self.alphabet)
        self.table = self._get_codon_table()
        self.start = self.table.start_codons
        self.stop = self.table.stop_codons
        self.nonstop = self._get_non_codons(self.stop)
        self.nonstart = self._get_non_codons(self.start)
        if self.typeof.protein:
            self._translate_codon_sets()
        del self.alphabet, self.table, self.stop_symbol, self.typeof

    def _get_codon_table(self):
        """Retrieve codon data from Bio.Data.CodonTable. (PRIVATE)"""
        if self.alphabet == IUPAC.unambiguous_dna or self.typeof.protein:
            codon_table = CodonTable.unambiguous_dna_by_id[self.table]
        elif self.alphabet == IUPAC.ambiguous_dna:
            codon_table = CodonTable.ambiguous_dna_by_id[self.table]
        elif self.alphabet == IUPAC.unambiguous_rna:
            codon_table = CodonTable.unambiguous_rna_by_id[self.table]
        elif self.alphabet == IUPAC.ambiguous_rna:
            codon_table = CodonTable.ambiguous_rna_by_id[self.table]
        else:
            codon_table = CodonTable.unambiguous_dna_by_id[self.table]
        return codon_table

    def _get_non_codons(self, exceptions):
        """Return a list of all codons in a table that are not exception codons. (PRIVATE)"""
        if self.typeof.rna:
            letters = IUPAC.unambiguous_rna.letters
        else:
            letters = IUPAC.unambiguous_dna.letters
        non_codons = []
        for nt1 in letters:
            for nt2 in letters:
                for nt3 in letters:
                    codon = nt1 + nt2 + nt3
                    for exception_codon in exceptions:
                        if codon == exception_codon:
                            break
                    else:
                        non_codons.append(codon)
        return non_codons

    def _translate_codon_sets(self):
        """Replace all codons in codon sets with corresponding amino acids. (PRIVATE)"""
        def translate_set(codon_set):
            amino_acids = []
            for codon in codon_set:
                if codon_set == self.stop:
                    translation = self.stop_symbol
                else:
                    translation = Seq(codon, IUPAC.unambiguous_dna).translate(table=self.table.id)._data
                this_amino_acid = translation
                amino_acids.append(this_amino_acid)
            return amino_acids

        self.start = translate_set(self.start)
        self.stop = translate_set(self.stop)
        self.nonstop = translate_set(self.nonstop)
        self.nonstart = translate_set(self.nonstart)


class _Letter(object):
    """Pair a letter with its probability of being chosen. (PRIVATE)"""

    def __init__(self, letter=None, value=None):
        self.letter = letter
        self.probability_value = value

    def __repr__(self):
        return "<" + str(self.letter) + " : " + str(self.probability_value) + ">"


if __name__ == "__main__":
    print("Running doctests...")
    import doctest
    doctest.testmod()
    print("Done")
