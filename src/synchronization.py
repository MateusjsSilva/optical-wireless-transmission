from config import START_SEQUENCE, END_SEQUENCE

def check_parity(bits, parity_type='even'):
    """
    Verifica a paridade dos bits. Se for 'even', a soma de bits 1 deve ser par; se 'odd', deve ser ímpar.
    """
    num_ones = sum(bits)
    if parity_type == 'even':
        return num_ones % 2 == 0
    elif parity_type == 'odd':
        return num_ones % 2 != 0
    return False

def find_sequence(bits, sequence, start=0):
    seq_len = len(sequence)
    for i in range(start, len(bits) - seq_len + 1):
        if bits[i:i + seq_len] == sequence:
            return i
    return -1

def decode_message(bits):
    """
    Decodifica uma mensagem a partir dos bits. Esse exemplo assume ASCII para bytes de 8 bits.
    """
    if len(bits) % 8 != 0:
        return None, "Erro: número de bits não é múltiplo de 8."

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        char = chr(int("".join(map(str, byte)), 2))
        chars.append(char)
    
    message = ''.join(chars)
    return message, "Mensagem decodificada com sucesso"

def calculate_checksum(bits):
    """
    Calcula o checksum como a soma de todos os bits em grupos de 8 (ou menos, se não for múltiplo).
    """
    checksum = sum(bits) % 256
    return checksum

def check_checksum(bits):
    """
    Verifica o checksum dos bits recebidos, comparando com o último byte como checksum.
    """
    if len(bits) < 8:
        return False
    data_bits = bits[:-8]
    received_checksum = int("".join(map(str, bits[-8:])), 2)
    calculated_checksum = calculate_checksum(data_bits)
    return received_checksum == calculated_checksum