from collections.abc import Iterable

import cramjam
from cryptography.fernet import Fernet
from temporalio.api.common.v1 import Payload
from temporalio.converter import PayloadCodec


class CompressionCodex(PayloadCodec):
    async def encode(self, payloads: Iterable[Payload]) -> list[Payload]:
        return [
            Payload(
                metadata={
                    "encoding": b"binary/snappy",
                },
                data=(bytes(cramjam.snappy.compress(p.SerializeToString()))),
            )
            for p in payloads
        ]

    async def decode(self, payloads: Iterable[Payload]) -> list[Payload]:
        ret: list[Payload] = []
        for p in payloads:
            if p.metadata.get("encoding", b"").decode() != "binary/snappy":
                ret.append(p)
                continue
            ret.append(Payload.FromString(bytes(cramjam.snappy.decompress(p.data))))
        return ret


class EncryptionCodec(PayloadCodec):
    def __init__(self, secret_key: bytes):
        # On initialise l'outil de chiffrement avec ta clé secrète.
        # Cette clé doit être stockée en sécurité (ex: Secret Manager sur GCP).
        self.fernet = Fernet(secret_key)

    async def encode(self, payloads: Iterable[Payload]) -> list[Payload]:
        return [
            Payload(
                metadata={
                    # On change l'étiquette pour bien identifier le chiffrement
                    "encoding": b"binary/encrypted",
                },
                # On chiffre les octets de la donnée
                data=self.fernet.encrypt(p.SerializeToString()),
            )
            for p in payloads
        ]

    async def decode(self, payloads: Iterable[Payload]) -> list[Payload]:
        ret: list[Payload] = []
        for p in payloads:
            # Si la donnée n'a pas notre étiquette, on la laisse passer
            if p.metadata.get("encoding", b"").decode() != "binary/encrypted":
                ret.append(p)
                continue
            # Si c'est chiffré, on déchiffre puis on désérialise
            decrypted_data = self.fernet.decrypt(p.data)
            ret.append(Payload.FromString(decrypted_data))

        return ret
