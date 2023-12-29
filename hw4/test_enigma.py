import pytest
from machine import Enigma
from components import Rotor, Reflector, Plugboard
from unittest.mock import patch, Mock

@pytest.fixture
def rotor1(rotor2):
    return Rotor("III", "V", next_rotor=rotor2)

@pytest.fixture
def rotor2(rotor3):
    return Rotor("II", "E", next_rotor=rotor3)

@pytest.fixture
def rotor3():
    return Rotor("I", "A")

@pytest.fixture
def rotor4(rotor2):
    return Rotor("V", "T", next_rotor=rotor2)

@pytest.fixture
def rotor5(rotor3):
    return Rotor("III", "R", prev_rotor=rotor3)

@pytest.fixture
def rotor7(rotor2):
    return Rotor("III", "Q", next_rotor=rotor2)
 

def test_rotor_init1(rotor3): # Tests when given rotor num is valid
    assert rotor3.rotor_num == 'I'
    assert rotor3.wiring == {'backward': 'UWYGADFPVZBECKMTHXSLRINQOJ', 'forward': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'}
    assert rotor3.notch == 'Q'
    assert rotor3.window == "A"
    assert rotor3.offset == 0
    assert rotor3.next_rotor == None
    assert rotor3.prev_rotor == None
    
def test_rotor_init2(): # Tests when given rotor num is invalid
    with pytest.raises(ValueError):
        Rotor("YV", "R")
        
def test_rotor_repr(rotor2):
    assert rotor2.__repr__() == "Wiring:\n{'forward': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'backward': 'AJPCZWRLFBDKOTYUQGENHXMIVS'}\nWindow: E"
    
def test_step1(rotor3):
    rotor3.step()
    assert rotor3.window == "B"
    assert rotor3.offset == 1
    rotor3.step()
    assert rotor3.window == "C"
    assert rotor3.offset == 2
    


def test_step2(rotor3):
    rotor3.step()
    assert rotor3.window == "B"
    rotor3.step()
    assert rotor3.window == "C"
    assert rotor3.offset == 2
        
def test_step3(rotor3):
    rotor3.step()
    assert rotor3.window == "B"
    rotor3.step()
    assert rotor3.window == "C"
    assert rotor3.offset == 2
    with pytest.raises(AttributeError):
        rotor3.next_rotor.step()
        
def test_step3(rotor3):
    rotor3.step()
    assert rotor3.window == "B"
    rotor3.step()
    assert rotor3.window == "C"
    assert rotor3.offset == 2
    with pytest.raises(AttributeError):
        rotor3.next_rotor.step()
        
def test_step4(rotor6):
    rotor6.step()
    assert rotor6.window == "R"
    assert rotor6.offset == 17
    rotor6.step()
    assert rotor6.window == "S"
    assert rotor6.offset == 18

def test_step_two_rotors1(rotor2):
    rotor2.step()
    assert rotor2.next_rotor.window == "B"
    assert rotor2.offset == 5
    
def test_step_two_rotors2(rotor2):
    rotor2.step()
    assert rotor2.next_rotor.window == "B"
    rotor2.step()
    assert rotor2.next_rotor.window == "B"
    assert rotor2.offset == 6
    
    
def test_step_three_rotors1(rotor1):
    rotor1.step()
    assert rotor1.next_rotor.next_rotor.window == "B"
    rotor1.step()
    assert rotor1.window == "X"
    assert rotor1.offset == 23
    
def test_step_three_rotors2(rotor1):
    rotor1.step()
    assert rotor1.next_rotor.next_rotor.window == "B"
    rotor1.step()
    assert rotor1.window == "X"
    assert rotor1.offset == 23
    
def test_step_double1(rotor4):
    rotor4.step()
    assert rotor4.next_rotor.next_rotor.window == "B"
    assert rotor4.offset == 20
    
def test_step_double2(rotor4):
    rotor4.step()
    assert rotor4.next_rotor.next_rotor.window == "B"
    rotor4.step()
    assert rotor4.window == "V"
    assert rotor4.offset == 21
    
def test_step_double3(rotor7):
    rotor7.step()
    assert rotor7.next_rotor.next_rotor.window == "B"
    rotor7.step()
    assert rotor7.window == "S"
    assert rotor7.offset == 18
    
def test_encode_letter1(rotor1, capfd): # Tests when index is a letter
    rotor1.encode_letter(index='L', forward=True, return_letter=True, printit=True)
    s = capfd.readouterr()
    assert s.out == "Rotor III: input = G, output = C\n"
    
def test_encode_letter2(rotor1, capfd): # Tests when wiring is backward
    rotor1.encode_letter(index=3, forward=False, return_letter=True, printit=True)
    s = capfd.readouterr()
    assert s.out == "Rotor III: input = Y, output = O\n"
    
def test_encode_letter3(rotor1, capfd): # Tests when printit is True
    rotor1.encode_letter(index=3, forward=True, return_letter=True, printit=True)
    s = capfd.readouterr()
    assert s.out == "Rotor III: input = Y, output = Q\n"

    
def test_encode_letter4(rotor1): # Tests when forward is True and there exists a next rotor
    a = rotor1.encode_letter(index=102, forward=True, return_letter=True, printit=True)
    assert a == 17
    
def test_encode_letter5(rotor5): # Tests when forward is False and there exists a previous rotor
    a = rotor5.encode_letter(index=3, forward=False, return_letter=True, printit=True)
    assert a == 3

def test_encode_letter6(rotor1): # Tests when forward is True or there doesn't exists a previous rotor and return letter is True
    a = rotor1.encode_letter(index='Q', forward=True, return_letter=True, printit=True)
    assert a == 24

def test_encode_letter7(rotor1, capfd): # Tests when forward is True or there doesn't exists a previous rotor and return letter is False
    a = rotor1.encode_letter(index=3, forward=True, return_letter=False, printit=True)
    assert a == 4
    s = capfd.readouterr()
    assert s.out == "Rotor III: input = Y, output = Q\n"
    
def test_encode_letter8(rotor1, capfd): # Tests when printit is False
    rotor1.encode_letter(index=3, forward=True, return_letter=True, printit=False)
    s = capfd.readouterr()
    assert s.out == ""
        
def test_encode_letter9(rotor1, capfd): # Tests when forward is True or there doesn't exists a previous rotor and return letter is True
    assert rotor1.encode_letter(index='Q', forward='E', return_letter=True, printit=False) == 24
    s = capfd.readouterr()
    assert s.out == ""

def test_encode_letter10(rotor1, capfd): # Tests when forward is True or there doesn't exists a previous rotor and return letter is False
    a = rotor1.encode_letter(index=234, forward=True, return_letter=False, printit=False)
    assert a == 0
    s = capfd.readouterr()
    assert s.out == ""
    assert rotor1.offset == 21
    assert rotor1.wiring['forward'][(21+234)%26] == 'M'
    
def test_encode_letter11(rotor1, capfd): # Tests when forward is True or there doesn't exists a previous rotor and return letter is True
    with pytest.raises(TypeError):
        rotor1.encode_letter(index='QE', forward=False, return_letter=True, printit=False)
    s = capfd.readouterr()
    assert s.out == ""

def test_encode_letter12(rotor8, capfd): # Tests when forward is False and there exists a previous rotor
    rotor8.encode_letter(index=323, forward=False, return_letter=True, printit=True)
    s = capfd.readouterr()
    assert s.out == "Rotor III: input = G, output = S\n"


@pytest.fixture
def rotor6():
    return Rotor("I", "Q")
  
@pytest.fixture
def rotor8(rotor9, rotor10):
    return Rotor("III", "V", prev_rotor=rotor9,  next_rotor=rotor10)
    
@pytest.fixture
def rotor9():
    return Rotor("II", "K")
    
@pytest.fixture
def rotor10():
    return Rotor("V", "N")

def test_change_setting(rotor1):
    rotor1.change_setting("l")
    assert rotor1.window == "L" and rotor1.offset == 11
    
def test_change_setting2(rotor1):
    rotor1.change_setting("O")
    assert rotor1.window == "O" 
    assert rotor1.offset == 14

def test_change_setting3(rotor1):
    with pytest.raises(ValueError):
        rotor1.change_setting("4")
    
def test_change_setting4(rotor1):
    with pytest.raises(AttributeError):
        rotor1.change_setting(4)

    
# ----- 15 tests above ------


@pytest.fixture
def reflector():
    return Reflector()

def test_reflector_init(reflector):
    assert reflector.wiring == {'A':'Y', 'B':'R', 'C':'U', 'D':'H', 'E':'Q', 'F':'S', 'G':'L', 'H':'D',
                       'I':'P', 'J':'X', 'K':'N', 'L':'G', 'M':'O', 'N':'K', 'O':'M', 'P':'I',
                       'Q':'E', 'R':'B', 'S':'F', 'T':'Z', 'U': 'C', 'V':'W', 'W':'V', 'X':'J',
                       'Y':'A', 'Z':'T'
                      }


def test_reflector_repr(reflector):
    assert reflector.__repr__() == "Reflector wiring: \n{'A': 'Y', 'B': 'R', 'C': 'U', 'D': 'H', 'E': 'Q', 'F': 'S', 'G': 'L', 'H': 'D', 'I': 'P', 'J': 'X', 'K': 'N', 'L': 'G', 'M': 'O', 'N': 'K', 'O': 'M', 'P': 'I', 'Q': 'E', 'R': 'B', 'S': 'F', 'T': 'Z', 'U': 'C', 'V': 'W', 'W': 'V', 'X': 'J', 'Y': 'A', 'Z': 'T'}"
    
    
# ----- 17 tests above ------

@pytest.fixture
def plugboard1():
    return Plugboard([])

@pytest.fixture
def plugboard2():
    return Plugboard(['GF', 'ZX'])

def test_plugbaord_init1(plugboard1):
    assert len(plugboard1.swaps) == 0

def test_plugboard_init2(plugboard2):
    assert plugboard2.swaps['F'] == 'G' 
    assert plugboard2.swaps['G'] == 'F'
    assert plugboard2.swaps['Z'] == 'X'
    assert plugboard2.swaps['X'] == 'Z'
    
def test_plugboard_repr1(plugboard1):
    assert plugboard1.__repr__() == ''
    
def test_plugboard_repr2(plugboard2):
    assert plugboard2.__repr__() == 'Z <-> X\nG <-> F' or plugboard2.__repr__() == 'G <-> F\nZ <-> X'
    
def test_update_swaps1(plugboard2, capfd): # Tests when length of new_swaps is greater than 6
    plugboard2.update_swaps(['RI', 'EW', 'RT', 'PA', 'QW', 'KM', 'PO'], replace=True)
    s = capfd.readouterr()
    assert plugboard2.swaps == {}
    assert s.out == 'Only a maximum of 6 swaps is allowed.\n'
    
def test_update_swaps2(plugboard2): # Tests when replace is False and new_swaps length is less than 6
    plugboard2.update_swaps(new_swaps=['RI', 'EW', 'DT', 'PA'], replace=False)
    assert plugboard2.swaps['I'] == 'R'
    assert plugboard2.swaps['R'] == 'I'
    assert plugboard2.swaps['E'] == 'W'
    assert plugboard2.swaps['W'] == 'E'
    assert plugboard2.swaps['T'] == 'D'
    assert plugboard2.swaps['D'] == 'T'
    assert plugboard2.swaps['P'] == 'A'
    assert plugboard2.swaps['A'] == 'P'
    assert plugboard2.swaps['G'] == 'F'
    assert plugboard2.swaps['F'] == 'G'
    assert plugboard2.swaps['Z'] == 'X'
    assert plugboard2.swaps['X'] == 'Z'

    
def test_update_swaps4(plugboard2): # Tests when replace is False and new_swaps length is less than 6
    plugboard2.update_swaps(new_swaps=['AB', 'AC', 'DT', 'PA'], replace=False)
    assert plugboard2.swaps['A'] == 'P'
    assert plugboard2.swaps['B'] == 'A'
    assert plugboard2.swaps['A'] == 'P'
    assert plugboard2.swaps['C'] == 'A'

    assert plugboard2.swaps['T'] == 'D'
    assert plugboard2.swaps['D'] == 'T'
    assert plugboard2.swaps['P'] == 'A'
    assert plugboard2.swaps['A'] == 'P'
    assert plugboard2.swaps['G'] == 'F'
    assert plugboard2.swaps['F'] == 'G'
    assert plugboard2.swaps['Z'] == 'X'
    assert plugboard2.swaps['X'] == 'Z'
    
def test_update_swaps3(plugboard2): # Tests when replace is True and new_swaps is None
    plugboard2.update_swaps(new_swaps=None, replace=True)
    assert plugboard2.swaps == {}
    
def test_update_swaps5(plugboard2): # Tests when replace is True and new_swaps is None
    plugboard2.update_swaps(new_swaps=['IU'], replace=False)
    assert plugboard2.swaps == {'F': 'G', 'G': 'F','X':'Z', 'Z': 'X', 'I': 'U', 'U': 'I'}

    
# ------- 24 test above ------

@pytest.fixture
def enigma():
    return Enigma(key='AAA', swaps=None, rotor_order=['I', 'II', 'III'])

@pytest.fixture
def enigma2():
    return Enigma(key='ABC', swaps=['AB', 'CD', 'EF', 'GH', 'IJ', 'KL'], rotor_order=['I', 'II', 'III'])

def test_enigma_init():
    with pytest.raises(ValueError):
        Enigma(key='AA', swaps=None, rotor_order=['I', 'II', 'III'])

def test_enigma_repr(enigma2):
    assert enigma2.__repr__() == "Keyboard <-> Plugboard <->  Rotor I <-> Rotor  II <-> Rotor  III <-> Reflector \nKey:  + ABC"

def test_encipher(enigma):
    assert enigma.encipher('HELLOTHERE') == "ILBDARTYDC"
    assert enigma.encipher('HELLOTHERE') == "XTEYNWWZSP"
    assert enigma.encipher('HELLOTHERE') == "WPSBRKQKHO"
    
def test_encipher2(enigma):
    assert enigma.encipher("HELLO THERE") == "ILBDARTYDC"
    assert enigma.encipher("HELLO THERE") == "XTEYNWWZSP"
    
    
def test_encipher3(enigma):
    with patch("machine.Enigma.encode_decode_letter") as mock_encode:
        mock_encode.return_value = "H"
        assert enigma.encipher('HELLOTHERE') == "HHHHHHHHHH"
    
def test_encipher4(enigma):
    with patch("machine.Enigma.encode_decode_letter") as mock_encode:
        mock_encode.return_value = "H"
        assert enigma.encipher('hellOTHEre') == "HHHHHHHHHH"
        
def test_encipher5(enigma):
    assert enigma.encipher('OSDNFL KDSAJFH sdf sdfjs dfjkhs HALSJKDHFASDXVNSADBCVNBCNVBCN') == "TXJSGIEUKTSBGNPRUMZOKODCTURACWYRBMQYIJOCUTYIMRQUHKHMHPTY"

def test_encipher6(enigma):
    with pytest.raises(ValueError):
        enigma.encipher('OSDNFL KDSAJFH LKQJHX MNFB SLDFHAL,,SJKDHFASDXVNSA,DBCVNBCNVBCN') == "ILBDARTYDC"

def test_encipher7(enigma):
    with patch("machine.Enigma.encode_decode_letter") as mock_encode:
        mock_encode.return_value = "H"
        assert enigma.encipher("HELLO THERE") == "HHHHHHHHHH"
        assert enigma.encipher("HELLO THERE") == "HHHHHHHHHH"

def test_encipher8(enigma):
    with pytest.raises(ValueError):
        enigma.encipher('OS123KDHFASDXVNSADBCVNBCNVBCN')
        
def test_encipher9(enigma):
    assert enigma.encipher('HEL LOTH ERE') == "ILBDARTYDC"
    assert enigma.encipher('HEL LOTH ERE') == "XTEYNWWZSP"

def test_encipher10(enigma2):
    assert enigma2.encipher('OSDNFL KDSAJFH sdf sdfjs dfjkhs HALSJKDHFASDXVNSADBCVNBCNVBCN') == "IJRGRORMFCLTSBKLZONPPJZQUCUSVGXORZTSSBTEZYBRNOFUPOBSRZDQ"

def test_encipher11(enigma2):
    with pytest.raises(ValueError):
        enigma2.encipher('OSDNFL KDSAJFH LKQJHX MNFB SLDFHAL,,SJKDHFASDXVNSA') 


# when breakingthings, weird inputs, somethings should not b, 3rd trying to rotate 4th, there doesn't exist a 4th rotor for step
    
def test_decipher1(enigma):
    assert enigma.decipher('I LBDARTYD C ') == "HELLOTHERE"
    assert enigma.decipher("I LBDARTYD C ") == "BRAFMFECII"
    
def test_decipher2(enigma):
    assert enigma.decipher('ilbda RTYDC') == "HELLOTHERE"
    
def test_decipher3(enigma2):
    enigma2.decipher('ilbda RTYDC') == "OATPLAXECA"
    
def test_decipher4(enigma):
    with pytest.raises(ValueError):
        enigma.decipher('I LBDART.YD C ') == "HELLOTHERE"
        
def test_decipher5(enigma2):
    assert enigma2.decipher('I LBDARTYD C ') == "OATPLAXECA"
    assert enigma2.decipher('I LBDA RTYD C ') == "QMXPIDWCQO"


    
def test_encode_decode_letter1(enigma): # if letter is not a letter from a-z or A-Z
    with pytest.raises(ValueError):
        enigma.encode_decode_letter('2')

def test_encode_decode_letter12(enigma): # Mock step, if letter is not a letter from a-z or A-Z
    enigma.r_rotor.step = Mock()
    with pytest.raises(ValueError):
        enigma.encode_decode_letter('2')
    assert enigma.r_rotor.step.call_count == 0
    
    # need to mock encode_letter

        

def test_encode_decode_letter2(enigma): # Tests when letter isn't in swaps
    assert enigma.encode_decode_letter("T") == "O"
    
def test_encode_decode_letter21(enigma): # Mock step, if letter is a letter from a-z or A-Z, final_letter is not in swaps
    enigma.r_rotor.step = Mock()
    with patch("components.Rotor.encode_letter") as mock_encode:
        mock_encode.return_value = 11
        assert enigma.r_rotor.step.call_count == 0
        assert enigma.encode_decode_letter("T") == "L"
        assert enigma.reflector.wiring["T"] == 'Z'
        assert enigma.l_rotor.encode_letter(25, forward=False) == 11

def test_encode_decode_letter3(enigma2): # Tests when letter is in swaps
    assert enigma2.encode_decode_letter("A") == "W"
    
def test_encode_decode_letter4(enigma2): # Tests when letter is in swaps
    assert enigma2.encode_decode_letter("Z") == "V"
    assert enigma2.encode_decode_letter("B") == "X"
    assert enigma2.encode_decode_letter("C") == "W"
    assert enigma2.encode_decode_letter("D") == "P"
    assert enigma2.encode_decode_letter("E") == "I"
    assert enigma2.encode_decode_letter("F") == "X"
    
def test_set_rotor_position1(enigma, capfd):
    enigma.set_rotor_position(position_key=4)
    s = capfd.readouterr()
    assert s.out == 'Please provide a three letter position key such as AAA.\n'

def test_set_rotor_position2(enigma, capfd):
    enigma.set_rotor_position(position_key='LEW', printIt=True)
    assert enigma.key == 'LEW'
    assert enigma.l_rotor.window == 'L'
    assert enigma.m_rotor.window == 'E'
    assert enigma.r_rotor.window == 'W'
    s = capfd.readouterr()
    assert s.out == 'Rotor position successfully updated. Now using LEW.\n'
    
def test_set_rotor_position3(enigma, capfd):
    enigma.set_rotor_position(position_key='LEW', printIt=False)
    assert enigma.key == 'LEW'
    assert enigma.l_rotor.window == 'L'
    assert enigma.m_rotor.window == 'E'
    assert enigma.r_rotor.window == 'W'
    s = capfd.readouterr()
    assert s.out == ''
    
def test_set_rotor_position4(enigma, capfd):
    enigma.l_rotor.change_setting = Mock()
    enigma.m_rotor.change_setting = Mock()
    enigma.r_rotor.change_setting = Mock()

    enigma.set_rotor_position(position_key='LEW', printIt=False)
    enigma.l_rotor.change_setting.assert_called_once_with('L')
    enigma.m_rotor.change_setting.assert_called_once_with('E')
    enigma.r_rotor.change_setting.assert_called_once_with('W')
    assert enigma.key == 'LEW'
    s = capfd.readouterr()
    assert s.out == ''

def test_set_rotor_order1(enigma):
    enigma.set_rotor_order(['I', 'II', 'III'])
    assert enigma.l_rotor.rotor_num == 'I'
    assert enigma.m_rotor.rotor_num == 'II'
    assert enigma.r_rotor.rotor_num == 'III'
    
    assert enigma.m_rotor.prev_rotor.rotor_num == 'III'
    assert enigma.l_rotor.prev_rotor.rotor_num == 'II'
    
    
def test_set_plugs(enigma):
    enigma.set_plugs(swaps=['AB', 'CD'], replace=False, printIt=False)
    assert enigma.plugboard.swaps == {"A": "B", "B": "A", "C": "D", "D": "C"}
    
def test_set_plugs2(enigma, capfd):
    enigma.set_plugs(swaps=['AB', 'CD'], replace=False, printIt=True)
    s = capfd.readouterr()
    assert s.out == "Plugboard successfully updated. New swaps are:\nA <-> B\nC <-> D\n"
    
def test_set_plugs3(enigma, capfd):
    enigma.plugboard.update_swaps = Mock()
    enigma.set_plugs(swaps=['AB', 'CD'], replace=True, printIt=True)
    enigma.plugboard.update_swaps.assert_called_once_with(['AB', 'CD'], True)
    s = capfd.readouterr()
    assert s.out == "Plugboard successfully updated. New swaps are:\n\n"
