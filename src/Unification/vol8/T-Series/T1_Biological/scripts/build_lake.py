# vol5/T-Series/T1_Biological/scripts/build_lake.py
import urllib.request
import gzip
import os

# The True Sovereign Endpoints for the Spellman 1998 Cell Cycle
# Targeting the primary GPL59 microarray platforms based on FTP structure
URL_ALPHA = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSEnnn/GSE22/matrix/GSE22-GPL59_series_matrix.txt.gz"
URL_CDC15 = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSEnnn/GSE23/matrix/GSE23_series_matrix.txt.gz"

MATRIX_DIR = "../lake/raw_matrices"

def download_and_extract(url, filename):
    print(f"[*] Pulling Sovereign Biological Data: {filename}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    out_path = os.path.join(MATRIX_DIR, filename)
    
    try:
        # Download the compressed matrix
        with urllib.request.urlopen(req, timeout=45) as response:
            compressed_data = response.read()
            
        # Decompress in memory and save as a clean text file
        decompressed_data = gzip.decompress(compressed_data).decode('utf-8')
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(decompressed_data)
            
        print(f"[+] Successfully ingested and unpacked {filename}.")
        
    except Exception as e:
        print(f"[-] FATAL ERROR pulling {filename}: {e}")

def build_lake():
    print("===============================================================")
    print(" 🧬 INITIALIZING T1_BIOLOGICAL (Yeast Temporal Cycles)")
    print("===============================================================")
    
    os.makedirs(MATRIX_DIR, exist_ok=True)
    
    # Download the Alpha-factor arrest time-series
    download_and_extract(URL_ALPHA, "GSE22_alpha_matrix.txt")
    
    # Download the CDC15 block/release time-series
    download_and_extract(URL_CDC15, "GSE23_cdc15_matrix.txt")
    
    print("\n[*] T1 Raw Matrices acquired. Ready for temporal interval extraction.")

if __name__ == "__main__":
    build_lake()