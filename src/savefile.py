"""Save-file container: header, compression, load / save."""

import gzip
import os
import struct
import zlib
from datetime import datetime

from .binary import UserProfile
from .constants import DEFAULT_PROFILE_VERSION, HEADER_SIZE


class UserProfileHeader:
    __slots__ = ("magic", "profile_version", "body_length", "payload_length")

    def __init__(self, magic=0, profile_version=DEFAULT_PROFILE_VERSION,
                 body_length=0, payload_length=0):
        self.magic = magic
        self.profile_version = profile_version
        self.body_length = body_length
        self.payload_length = payload_length

    @classmethod
    def parse(cls, data: bytes):
        if len(data) < HEADER_SIZE:
            raise ValueError(f"payload too small for header: {len(data)} bytes")
        return cls(*struct.unpack("<IIII", data[:HEADER_SIZE]))

    def serialize(self) -> bytes:
        return struct.pack("<IIII", self.magic, self.profile_version,
                           self.body_length, self.payload_length)

    def refresh_lengths(self, body_len: int):
        self.body_length = body_len
        self.payload_length = HEADER_SIZE + body_len


def compress(payload: bytes, kind: str) -> bytes:
    """Wrap a payload in the container format it was originally loaded from."""
    if kind == "plain":
        return payload
    if kind == "deflate":
        co = zlib.compressobj(level=6, wbits=-15)
        return co.compress(payload) + co.flush()
    if kind == "gzip":
        return gzip.compress(payload, mtime=0)
    if kind == "zlib":
        co = zlib.compressobj(level=6, wbits=15)
        return co.compress(payload) + co.flush()
    raise ValueError(f"unknown container kind {kind!r}")


class ProfileFile:
    """A loaded .dat save: container wrapper + header + parsed UserProfile."""

    def __init__(self, path: str):
        self.path = path
        with open(path, "rb") as f:
            raw = f.read()
        if len(raw) < 32:
            raise ValueError(f"File is only {len(raw)} bytes — too small.")

        errors = []
        for wrapper, payload in self._candidates(raw):
            try:
                header, profile = self._parse_payload(payload)
            except Exception as e:
                errors.append(f"{wrapper}: {type(e).__name__}: {e}")
                continue
            self.wrapper, self.header, self.profile = wrapper, header, profile
            return

        raise ValueError(
            "No wrapper produced a valid UserProfile.\nTried:\n  "
            + "\n  ".join(errors))

    @staticmethod
    def _candidates(raw: bytes):
        """Yield (wrapper name, payload) for each way the file might be packed."""
        try:
            yield ("deflate", zlib.decompress(raw, -15))
        except zlib.error:
            pass
        try:
            yield ("gzip", gzip.decompress(raw))
        except (OSError, EOFError):
            pass
        try:
            yield ("zlib", zlib.decompress(raw))
        except zlib.error:
            pass
        yield ("plain", raw)

    @staticmethod
    def _parse_payload(payload: bytes):
        if len(payload) < HEADER_SIZE:
            raise ValueError(f"payload {len(payload)} bytes < header")
        header = UserProfileHeader.parse(payload)
        body = payload[HEADER_SIZE:]
        if header.payload_length != len(payload):
            raise ValueError(
                f"header.payload_length={header.payload_length} "
                f"!= actual {len(payload)}")
        if header.body_length != len(body):
            raise ValueError(
                f"header.body_length={header.body_length} "
                f"!= actual {len(body)}")
        return header, UserProfile.deserialize(body, version=header.profile_version)

    def _encode(self) -> bytes:
        """Serialize, verify the result round-trips, and compress."""
        body = self.profile.serialize()
        self.header.refresh_lengths(len(body))
        payload = self.header.serialize() + body

        h2 = UserProfileHeader.parse(payload)
        if h2.body_length != len(body) or h2.payload_length != len(payload):
            raise ValueError("header length fields failed to round-trip")
        p2 = UserProfile.deserialize(payload[HEADER_SIZE:],
                                     version=self.header.profile_version)
        if p2.serialize() != body:
            raise ValueError("body failed to round-trip")

        return compress(payload, self.wrapper)

    def save(self):
        """Overwrite the original file, keeping a one-time .bak of it."""
        compressed = self._encode()
        tmp = self.path + ".tmp"
        bak = self.path + ".bak"
        with open(tmp, "wb") as f:
            f.write(compressed)
        if os.path.exists(self.path) and not os.path.exists(bak):
            try:
                os.replace(self.path, bak)
            except OSError:
                pass
        os.replace(tmp, self.path)

    def save_as(self, out_path: str):
        with open(out_path, "wb") as f:
            f.write(self._encode())


def try_load(path: str):
    """Return (ProfileFile, None) or (None, error message)."""
    try:
        return ProfileFile(path), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
