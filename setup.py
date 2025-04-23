def xor_decrypt_and_execute(encrypted_file, key):
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = bytearray([byte ^ key for byte in encrypted_data])


    temp_file = "__temp__.py"
    with open(temp_file, 'wb') as f:
        f.write(decrypted_data)


    import subprocess
    subprocess.run(["python", temp_file])


    import os
    os.remove(temp_file)

if __name__ == "__main__":
    encrypted_file = "encst.py"
    key = 123

    xor_decrypt_and_execute(encrypted_file, key)
