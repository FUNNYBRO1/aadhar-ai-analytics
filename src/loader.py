import pandas as pd

def load_csv(path, use_chunks=False, chunksize=200000):
    """
    Optimized CSV loader for Aadhaar demographic data.
    """
    try:
        if use_chunks:
            # Chunking useful for very large files to avoid memory crash
            reader = pd.read_csv(path, chunksize=chunksize, low_memory=False)
            chunks = []
            for chunk in reader:
                # Pre-processing dates within chunks is faster
                chunk['date'] = pd.to_datetime(chunk['date'], dayfirst=True, errors='coerce')
                chunks.append(chunk)
            df = pd.concat(chunks, ignore_index=True)
        else:
            df = pd.read_csv(path, low_memory=False)
            df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

        # Drop rows where date is NaT to avoid analyzer errors
        df = df.dropna(subset=['date'])
        
        return df
        
    except FileNotFoundError:
        print(f"Error: File not found at {path}")
        return None