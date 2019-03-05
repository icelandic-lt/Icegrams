
from random import randint

from icegrams import Ngrams
from icegrams.ngrams import (
    BitArray, MonotonicList, PartitionedMonotonicList
)


def test_compressed_list():
    """ Test the compressed list classes """
    ba = BitArray()
    ba.append(10, 4)
    ba.append(3, 2)
    ba.append(0, 7)
    ba.append(1, 1)
    ba.append(100, 7)
    ba.append(100, 8)
    ba.append(1000, 10)
    ba.append(1000000, 20)
    ba.append(1000000000, 30)
    ba.append(0, 1)
    ba.finish()
    assert ba.get(0, 4) == 10
    assert ba.get(4, 2) == 3
    assert ba.get(6, 7) == 0
    assert ba.get(13, 1) == 1
    assert ba.get(14, 7) == 100
    assert ba.get(21, 8) == 100
    assert ba.get(29, 10) == 1000
    assert ba.get(39, 20) == 1000000
    assert ba.get(59, 30) == 1000000000
    assert ba.get(89, 1) == 0
    try:
        ba.get(90, 1)
        assert False, "Should have raised IndexError"
    except IndexError:
        pass
    except:
        assert False, "Should have raised IndexError"
    assert len(ba) == (90 + 7) // 8

    for _ in range(100):
        test_list = [randint(0,2000000) for _ in range(randint(1,1000))]

        test_list.sort()
        ml = MonotonicList()
        ml.compress(test_list)
        for i in range(len(test_list)):
            assert ml[i] == test_list[i]

    # Test single-element list
    ml = MonotonicList()
    ml.compress([17])
    assert ml[0] == 17


def test_partitioned_list():
    pl = PartitionedMonotonicList()
    pl.compress([i for i in range(18000)])
    assert pl[177] == 177
    assert pl[2177] == 2177
    assert pl[4177] == 4177
    assert pl[7177] == 7177
    assert pl[12177] == 12177
    assert pl[14177] == 14177
    assert pl[16177] == 16177
    pl.compress([i*17 for i in range(1380000)])
    assert pl[199] == 199*17
    assert pl[2199] == 2199*17
    assert pl[4199] == 4199*17
    assert pl[7199] == 7199*17
    assert pl[12177] == 12177*17
    assert pl[14177] == 14177*17
    assert pl[16177] == 16177*17
    assert pl[120177] == 120177*17
    assert pl[140177] == 140177*17
    assert pl[160177] == 160177*17
    assert pl[343085] == 343085*17
    assert pl[1343085] == 1343085*17
    b = pl.to_bytes()
    pl = PartitionedMonotonicList(b)
    assert pl[199] == 199*17
    assert pl[2199] == 2199*17
    assert pl[4199] == 4199*17
    assert pl[7199] == 7199*17
    assert pl[12177] == 12177*17
    assert pl[14177] == 14177*17
    assert pl[16177] == 16177*17
    assert pl[120177] == 120177*17
    assert pl[140177] == 140177*17
    assert pl[160177] == 160177*17
    assert pl[343085] == 343085*17
    assert pl[1343085] == 1343085*17


def test_trigrams():
    n = Ngrams()
    assert n.freq('hálfur', 'millimetri', 'að') == 2
    assert n.freq("xxx", "yyy", "zzz") == 1
    assert n.freq("Hann", "var", "zzz") == 1
