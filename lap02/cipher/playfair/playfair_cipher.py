class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key: str):
        key = key.upper().replace("J", "I")
        key = ''.join(filter(str.isalpha, key))
        seen = set()
        new_key = ""

        for ch in key:
            if ch not in seen and ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
                seen.add(ch)
                new_key += ch

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for ch in alphabet:
            if ch not in seen:
                new_key += ch

        matrix = [list(new_key[i:i + 5]) for i in range(0, 25, 5)]
        return matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        raise ValueError(f"Letter '{letter}' not found in matrix.")

    def preprocess_plaintext(self, text: str):
        text = text.upper().replace("J", "I")
        text = ''.join(filter(str.isalpha, text))
        pairs = []
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i + 1] if i + 1 < len(text) else "X"
            if a == b:
                pairs.append((a, "X"))
                i += 1
            else:
                pairs.append((a, b))
                i += 2
        return pairs

    def playfair_encrypt(self, plaintext: str, matrix):
        pairs = self.preprocess_plaintext(plaintext)
        encrypted = ""

        for a, b in pairs:
            row1, col1 = self.find_letter_coords(matrix, a)
            row2, col2 = self.find_letter_coords(matrix, b)

            if row1 == row2:
                encrypted += matrix[row1][(col1 + 1) % 5]
                encrypted += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted += matrix[(row1 + 1) % 5][col1]
                encrypted += matrix[(row2 + 1) % 5][col2]
            else:
                encrypted += matrix[row1][col2]
                encrypted += matrix[row2][col1]

        return encrypted

    def playfair_decrypt(self, cipher_text: str, matrix):
        cipher_text = cipher_text.upper()
        if len(cipher_text) % 2 != 0:
            cipher_text += 'X'  # Thêm X nếu chuỗi lẻ
        decrypted = ""

        for i in range(0, len(cipher_text), 2):
            a = cipher_text[i]
            b = cipher_text[i + 1]
            row1, col1 = self.find_letter_coords(matrix, a)
            row2, col2 = self.find_letter_coords(matrix, b)

            if row1 == row2:
                decrypted += matrix[row1][(col1 - 1) % 5]
                decrypted += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted += matrix[(row1 - 1) % 5][col1]
                decrypted += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted += matrix[row1][col2]
                decrypted += matrix[row2][col1]

        return decrypted

    def clean_decrypted_text(self, decrypted: str):
        result = ""
        i = 0
        while i < len(decrypted):
            if (i + 2 < len(decrypted) and decrypted[i] == decrypted[i + 2] and decrypted[i + 1] == "X"):
                result += decrypted[i]
                i += 2
            else:
                result += decrypted[i]
                i += 1

        if result.endswith("X"):
            result = result[:-1]

        return result
