import random

ROUNDS = 12

BLOCK_SIZE = 32

def generate_round_keys():
    return [random.randint(0, 2**BLOCK_SIZE - 1) for _ in range(ROUNDS)]

def feistel_function(right, key):
    return right + key

def feistel_encrypt_block(left, right, round_keys):
    for i in range(ROUNDS):
        temp = right
        right = left ^ feistel_function(right, round_keys[i])
        left = temp
    return left, right

def feistel_decrypt_block(left, right, round_keys):
    for i in range(ROUNDS - 1, -1, -1):
        temp = left
        left = right ^ feistel_function(left, round_keys[i])
        right = temp
    return left, right

def encrypt_text(text, round_keys):
    encrypted_blocks = []
    for char in text:

        left = ord(char) >> (BLOCK_SIZE // 2)
        right = ord(char) & ((1 << (BLOCK_SIZE // 2)) - 1)
        left, right = feistel_encrypt_block(left, right, round_keys)
        encrypted_blocks.append((left, right))
    return encrypted_blocks

def decrypt_text(encrypted_blocks, round_keys):
    decrypted_text = ""
    for left, right in encrypted_blocks:
        left, right = feistel_decrypt_block(left, right, round_keys)
        decrypted_text += chr((left << (BLOCK_SIZE // 2)) | right)
    return decrypted_text

if __name__ == "__main__":
    original_text = "Hello its me"
    print("Original Text:", original_text)
    
    round_keys = generate_round_keys()
    
    encrypted_blocks = encrypt_text(original_text, round_keys)
    print("Encrypted Blocks:", encrypted_blocks)
    
    decrypted_text = decrypt_text(encrypted_blocks, round_keys)
    print("Decrypted Text:", decrypted_text)
    
    if decrypted_text == original_text:
        print("Decryption successful! The decrypted text matches the original.")
    else:
        print("Decryption failed. The decrypted text does not match the original.")
