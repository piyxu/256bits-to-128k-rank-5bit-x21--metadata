# -------------------------------------------------
# encode.py - 256/128k test
# MIT LICENSE
# MESUT ERTURHAN
# https://github.com/piyxu/256bits-to-128k-rank-4bit-metadata/
# -------------------------------------------------
from math import comb

# --- Kombinasyon Fonksiyonları (n=253 tabanlı) ---

def rank_nk(bits, k_fixed: int):
    n = len(bits)
    rem = k_fixed
    r = 0
    for i, b in enumerate(bits):
        if b == 1:
            z = comb(n - i - 1, rem)
            r += z
            rem -= 1
    return r

C253 = comb(253, 128)
MASK_256 = (1 << 256) - 1

def decode253_with_prefix(bits256, m: int):
    """
    1. Baştaki 3 biti (000) atar.
    2. Kalan 253 biti rank işlemine sokar.
    3. Metadata (m) ile birleştirerek R'yi bulur.
    """
    # İlk 3 biti (000) dilimleyerek atıyoruz, sadece gövdeyi alıyoruz
    body_bits = bits256[0:] 
    
    # Gövde üzerinden rank hesabı (n=253, k=128)
    idx = rank_nk(body_bits, 128)
    
    # R formülü: (Mask * Uzay) + İndeks
    R = m * C253 + idx
    return R

# -------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------

def main():
    try:
        with open("originals.txt") as f_ori, \
             open("encode.txt") as f_enc, \
             open("decode.txt", "w") as f_dec, \
             open("reports.txt", "w") as f_rep:

            ori_lines = [line.strip() for line in f_ori]
            enc_lines = [line.strip() for line in f_enc]

            for idx, (ori, enc) in enumerate(zip(ori_lines, enc_lines)):
                
                # Metadata uzunluğu encode kısmında neyse ona göre ayarlayın (Örn: 1 bit)
                # m = int(enc[0], 2) # Eğer meta_bin = format(m, "01b") ise
                # bits_str = enc[1:]
                
                # Eğer meta 4 bit ise:
                meta_bin = enc[:1] # 01b formatında yazdıysan 1, 04b ise 4 yapın
                bits_str = enc[1:]

                m = int(meta_bin, 2)
                bits256_list = [int(b) for b in bits_str]

                # ---- DECODE İşlemi ----
                R2 = decode253_with_prefix(bits256_list, m)

                # Orijinal 256 bitlik sayıya geri dönüştür
                dec_bits = format(R2 & MASK_256, "0256b")
                f_dec.write(dec_bits + "\n")

                # ---- Karşılaştırma ve Rapor ----
                k_ori = ori.count("1")
                k_enc = bits_str.count("1")
                k_dec = dec_bits.count("1")

                same = "TRUE" if ori == dec_bits else "FALSE"

                f_rep.write(
                    f"{idx:03d}: "
                    f"K_ori={k_ori:3d}  "
                    f"K_enc={k_enc:3d}  "
                    f"K_dec={k_dec:3d}  "
                    f"SAME={same}\n"
                )

        print("Decode (253-bit tabanlı) tamamlandı → decode.txt, reports.txt")
        
    except FileNotFoundError:
        print("Hata: Gerekli dosyalar (originals.txt, encode.txt) bulunamadı.")

if __name__ == "__main__":
    main()