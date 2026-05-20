import csv
import random

def main():
    print("[*] Generating music acoustic features dataset...")
    
    headers = [
        "Song_ID", "Genre", "Tempo", "Chroma_STFT", "Spectral_Centroid", 
        "Spectral_Bandwidth", "Rolloff", "Zero_Crossing_Rate", 
        "MFCC_1", "MFCC_2", "MFCC_3", "MFCC_4", "MFCC_5"
    ]
    
    genres = ["Classical", "Jazz", "Pop", "Rock", "Hip-Hop"]
    records = []
    
    # Generate 1000 songs (200 per genre)
    for g in genres:
        for idx in range(1, 201):
            song_id = f"{g[:3].upper()}{idx:03d}"
            
            # Synthesize distinct profiles for each genre
            if g == "Classical":
                tempo = random.normalvariate(80.0, 10.0)
                chroma = random.uniform(0.15, 0.3)
                centroid = random.normalvariate(1000.0, 200.0)
                bandwidth = random.normalvariate(1200.0, 150.0)
                rolloff = random.normalvariate(2000.0, 300.0)
                zcr = random.normalvariate(0.04, 0.01)
                mfcc_1 = random.normalvariate(-250.0, 30.0)
                mfcc_2 = random.normalvariate(150.0, 15.0)
                mfcc_3 = random.normalvariate(-20.0, 8.0)
                mfcc_4 = random.normalvariate(15.0, 5.0)
                mfcc_5 = random.normalvariate(-5.0, 4.0)
                
            elif g == "Jazz":
                tempo = random.normalvariate(105.0, 15.0)
                chroma = random.uniform(0.28, 0.38)
                centroid = random.normalvariate(1800.0, 250.0)
                bandwidth = random.normalvariate(1900.0, 180.0)
                rolloff = random.normalvariate(3500.0, 400.0)
                zcr = random.normalvariate(0.08, 0.015)
                mfcc_1 = random.normalvariate(-180.0, 25.0)
                mfcc_2 = random.normalvariate(110.0, 12.0)
                mfcc_3 = random.normalvariate(10.0, 7.0)
                mfcc_4 = random.normalvariate(25.0, 6.0)
                mfcc_5 = random.normalvariate(5.0, 5.0)
                
            elif g == "Pop":
                tempo = random.normalvariate(120.0, 12.0)
                chroma = random.uniform(0.38, 0.48)
                centroid = random.normalvariate(2500.0, 300.0)
                bandwidth = random.normalvariate(2400.0, 200.0)
                rolloff = random.normalvariate(5200.0, 500.0)
                zcr = random.normalvariate(0.12, 0.02)
                mfcc_1 = random.normalvariate(-90.0, 20.0)
                mfcc_2 = random.normalvariate(85.0, 10.0)
                mfcc_3 = random.normalvariate(-15.0, 8.0)
                mfcc_4 = random.normalvariate(35.0, 6.0)
                mfcc_5 = random.normalvariate(-8.0, 5.0)
                
            elif g == "Rock":
                tempo = random.normalvariate(125.0, 15.0)
                chroma = random.uniform(0.35, 0.44)
                centroid = random.normalvariate(2200.0, 250.0)
                bandwidth = random.normalvariate(2200.0, 180.0)
                rolloff = random.normalvariate(4600.0, 450.0)
                zcr = random.normalvariate(0.11, 0.02)
                mfcc_1 = random.normalvariate(-110.0, 20.0)
                mfcc_2 = random.normalvariate(90.0, 10.0)
                mfcc_3 = random.normalvariate(-30.0, 8.0)
                mfcc_4 = random.normalvariate(20.0, 6.0)
                mfcc_5 = random.normalvariate(-20.0, 5.0)
                
            else: # Hip-Hop
                tempo = random.normalvariate(98.0, 8.0)
                chroma = random.uniform(0.40, 0.50)
                centroid = random.normalvariate(2400.0, 280.0)
                bandwidth = random.normalvariate(2300.0, 190.0)
                rolloff = random.normalvariate(5000.0, 480.0)
                zcr = random.normalvariate(0.10, 0.018)
                mfcc_1 = random.normalvariate(-100.0, 18.0)
                mfcc_2 = random.normalvariate(95.0, 10.0)
                mfcc_3 = random.normalvariate(-5.0, 6.0)
                mfcc_4 = random.normalvariate(38.0, 5.0)
                mfcc_5 = random.normalvariate(-3.0, 4.0)
                
            # Clean numeric constraints
            tempo = max(40.0, round(tempo, 1))
            chroma = max(0.0, min(1.0, round(chroma, 4)))
            centroid = max(100.0, round(centroid, 1))
            bandwidth = max(100.0, round(bandwidth, 1))
            rolloff = max(200.0, round(rolloff, 1))
            zcr = max(0.0, min(1.0, round(zcr, 4)))
            mfcc_1 = round(mfcc_1, 2)
            mfcc_2 = round(mfcc_2, 2)
            mfcc_3 = round(mfcc_3, 2)
            mfcc_4 = round(mfcc_4, 2)
            mfcc_5 = round(mfcc_5, 2)
            
            records.append([
                song_id, g, tempo, chroma, centroid, 
                bandwidth, rolloff, zcr, 
                mfcc_1, mfcc_2, mfcc_3, mfcc_4, mfcc_5
            ])
            
    # Shuffle for train-test split health
    random.shuffle(records)
    
    with open("music_features.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)
        
    print(f"[+] Successfully generated {len(records)} song features in music_features.csv.")

if __name__ == "__main__":
    main()
