import enum
import gpg

class SecurityIssues(enum.IntFlag):
	expired = 1
	disabled = 2
	revoked = 4
	invalid = 8
	brokenCrypto = 16
	keyLengthIsTooShort = 32


class SignAlgo(enum.IntEnum):
	RSA_encrypt_sign = 1
	RSA_sign = 3
	ElGamal = 16
	DSA = 17
	ECDSA = 19
	EdDSA = 22
	AEDSA = 24


class HashAlgo(enum.IntEnum):
	sha256 = 8
	sha384 = 9
	sha512 = 10


def isConsideredInsecure(k):
	res = k.invalid * SecurityIssues.invalid | k.disabled * SecurityIssues.disabled | k.expired * SecurityIssues.expired | k.revoked * SecurityIssues.revoked
	for sk in k.subkeys:
		res |= isSubkeyConsideredInsecure(sk)
	return res


def isSubkeyConsideredInsecure(k):
	res = k.invalid * SecurityIssues.invalid | k.disabled * SecurityIssues.disabled | k.expired * SecurityIssues.expired | k.revoked * SecurityIssues.revoked
	try:
		algo = SignAlgo(k.pubkey_algo)
	except ValueError:
		res |= SecurityIssues.brokenCrypto
		return res

	minimumLegths = {
		SignAlgo.RSA_encrypt_sign: 2048,
		SignAlgo.RSA_sign: 2048,
		SignAlgo.ElGamal: 2048,
		SignAlgo.DSA: 2048,
		SignAlgo.ECDSA: 2048
	}

	if algo in minimumLegths and k.length < minimumLegths[algo]:
		res |= SecurityIssues.keyLengthIsTooShort
	return res
