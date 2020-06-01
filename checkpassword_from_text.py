import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error Fetching: {response.status_code}, Check API and try again')
    return response

def get_password_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    res = request_api_data(first5_char)
    return get_password_leak_count(res, tail)

print('\n')
print('------------------------------------------------------------------------------------')

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times in hacked database, Probably Update Your Password!!')
            print('------------------------------------------------------------------------------------')
        else:
            print(f'Good News!!, {password} NOT Found, You can Used It as Secure  Password!!')
            print('------------------------------------------------------------------------------------')
    return '\n All Done! \n'

with open('./pass.txt', 'r') as file:
    password_file = [word for line in file for word in line.split()]

main(password_file)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

