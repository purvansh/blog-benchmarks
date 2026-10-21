# Eight ways to checksum 2 GiB

Same file, read from page cache so the figure is CPU work rather than disk.
Best of 3. The CPU reports `sha_ni`.

## Run

```bash
dd if=/dev/urandom of=/tmp/hashfile.bin bs=1M count=2048
./bench.sh
```

## Results

| command | throughput | 2 GiB | vs sha256sum |
|---|---|---|---|
| `openssl dgst -sha256` | 966 MB/s | 2.09 s | **5.3x** |
| `b2sum` (BLAKE2b) | 610 MB/s | 3.36 s | 3.3x |
| `openssl dgst -blake2b512` | 603 MB/s | 3.40 s | 3.3x |
| `md5sum` | 536 MB/s | 3.82 s | 2.9x |
| `sha1sum` | 462 MB/s | 4.44 s | 2.5x |
| `sha512sum` | 288 MB/s | 7.11 s | 1.6x |
| `cksum` (CRC32) | 277 MB/s | 7.38 s | 1.5x |
| `sha256sum` | 185 MB/s | 11.05 s | baseline |

`sha256sum` and `openssl dgst -sha256` print the identical digest. Verified
before timing anything:

```
4e2b07bf773090154e22a8af6495ed30  (both)
```

The BLAKE2b pair is the control: where no special instruction exists, the two
projects land within 1% of each other, so the 5.3x on SHA-256 is not openssl
simply being better optimised. coreutils 8.32, OpenSSL 3.0.2.
