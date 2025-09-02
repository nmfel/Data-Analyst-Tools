import re
import emoji
import pandas as pd

input_file = "input lokasi file asli"
output_file = "input lokasi file output"

def datacleansing(text):
    if pd.isna(text):  # Handle NaN values
        return ""
    text = str(text).lower()
    text = re.sub('[^0-9a-zA-Z]+',' ',text)
    text = re.sub('\n',' ',text) #Menghilangkan new line pada data
    text = re.sub('rt',' ',text) #Menghilangkan kata-kata retweet
    text = re.sub('user',' ',text) #Menghilangkan kata-kata user
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) #Menghilangkan  URL
    text = re.sub(' +',' ',text) #Menghilangkan ekstra spasi
    text = re.sub(r'[^\x00-\x7f]',r' ',text) #Menghilangkan non-ascii
    text = emoji.replace_emoji(text, replace='') #Menghilangkan emoji
    return text.strip()

# Baca file CSV
print("Membaca file CSV...")
df = pd.read_csv(input_file)
print(f"Total data: {len(df)} baris")

# Tampilkan kolom yang tersedia dan minta user memilih
print(f"\nKolom yang tersedia: {list(df.columns)}")
text_column = input("Masukkan nama kolom yang berisi teks yang akan dibersihkan: ").strip()

# Validasi kolom yang dipilih
while text_column not in df.columns:
    print(f"Kolom '{text_column}' tidak ditemukan!")
    print(f"Kolom yang tersedia: {list(df.columns)}")
    text_column = input("Masukkan nama kolom yang benar: ").strip()

print(f"Menggunakan kolom: {text_column}")

# Proses setiap baris dengan progress
print("Memproses data...")
cleaned_texts = []
for i, text in enumerate(df[text_column]):
    cleaned = datacleansing(text)
    cleaned_texts.append(cleaned)
    if (i + 1) % 100 == 0:  # Progress setiap 100 data
        print(f"Diproses: {i + 1}/{len(df)}")

# Buat DataFrame baru hanya dengan cleaned text
cleaned_df = pd.DataFrame({'cleaned_text': cleaned_texts})

# Simpan ke file CSV baru
cleaned_df.to_csv(output_file, index=False)
print(f"Hasil disimpan ke: {output_file}")

# Tampilkan contoh hasil
print("\nContoh hasil:")
for i in range(min(3, len(cleaned_texts))):
    print(f"Cleaned:  {cleaned_texts[i]}")
    print("-" * 50)


