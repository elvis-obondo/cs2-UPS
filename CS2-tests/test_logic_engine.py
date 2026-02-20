from CS2.logic_engine import calculate_tradeup

fillers2 = [0.056358762,0.0564528,0.06628476287,0.0634557683,0.0546782,0.04367547635,0.0668368,0.068736247,0.0634846918]
fillers1 = [0.026358762,0.0164528,0.03628476287,0.0334557683,0.0546782,0.01367547635,0.0368368,0.028736247,0.0634846918]
anchor = 0.074
t_max = 0.7
def test_sampletradeup():

    assert calculate_tradeup(fillers1,anchor,t_max) == 0.0268774455824
    assert calculate_tradeup(fillers2,anchor,t_max) == 0.0429774455824
