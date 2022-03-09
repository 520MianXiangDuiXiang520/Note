package fuzz

import (
    `bytes`
    `encoding/hex`
    `testing`
)

func FuzzHex(f *testing.F) {
    for _, seed := range [][]byte{{}, {0}, {9}, {0xa}, {0xf}, {1, 2, 3, 4}} {
        f.Add(seed)
    }
    f.Fuzz(func(t *testing.T, in []byte) {
        enc := hex.EncodeToString(in)
        out, err := hex.DecodeString(enc)
        if err != nil {
            t.Fatalf("%v: decode: %v", in, err)
        }
        if !bytes.Equal(in, out) {
            t.Fatalf("%v: not equal after round trip: %v", in, out)
        }
    })
}
