import csv
import random

def main():
    print("[*] Generating Netflix recommendation dataset...")
    
    # 30 Movies with titles, genres, and realistic descriptive text
    movies = [
        # Sci-Fi / Action
        (1, "Inception", "Sci-Fi|Action", "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."),
        (2, "The Matrix", "Sci-Fi|Action", "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."),
        (3, "Interstellar", "Sci-Fi|Drama", "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival on a dying Earth."),
        (4, "Blade Runner 2049", "Sci-Fi|Action", "A new blade runner, LAPD Officer K, unearths a long-buried secret that has the potential to plunge what's left of society into chaos."),
        (5, "Star Wars: A New Hope", "Sci-Fi|Action", "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station."),
        
        # Drama / Romance
        (6, "The Shawshank Redemption", "Drama", "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion."),
        (7, "The Godfather", "Drama|Crime", "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."),
        (8, "Forrest Gump", "Drama|Romance", "The history of the United States from the 1950s to the '70s unfolds from the perspective of an Alabama man with an IQ of 75."),
        (9, "Titanic", "Drama|Romance", "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."),
        (10, "The Notebook", "Romance|Drama", "A poor yet passionate young man falls in love with a rich young woman, giving her a sense of freedom, but they are soon separated because of their social differences."),
        
        # Comedy
        (11, "Superbad", "Comedy", "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry."),
        (12, "The Hangover", "Comedy", "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing."),
        (13, "Step Brothers", "Comedy", "Two aimless, middle-aged slacker stepbrothers are forced to live together when their parents marry, creating hilarious domestic chaos."),
        (14, "Anchorman", "Comedy", "Ron Burgundy is San Diego's top-rated newsman in the male-dominated broadcasting of the 1970s, until an ambitious woman is hired."),
        (15, "Dumb and Dumber", "Comedy", "After a woman leaves a briefcase at the airport terminal, two extremely dimwitted friends go on a cross-country road trip to return it."),
        
        # Thriller / Horror
        (16, "The Silence of the Lambs", "Thriller|Crime", "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer."),
        (17, "Seven", "Thriller|Crime", "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives."),
        (18, "Shutter Island", "Thriller|Mystery", "In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane."),
        (19, "The Conjuring", "Horror|Mystery", "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse."),
        (20, "Get Out", "Horror|Thriller", "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception reaches a boiling point."),
        
        # Action / Crime
        (21, "The Dark Knight", "Action|Crime|Drama", "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."),
        (22, "Pulp Fiction", "Crime|Drama", "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."),
        (23, "Gladiator", "Action|Drama", "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery."),
        (24, "Die Hard", "Action|Thriller", "An NYPD officer tries to save his wife and several others taken hostage by German terrorists during a Christmas party at the Nakatomi Plaza in Los Angeles."),
        (25, "Kill Bill: Vol. 1", "Action|Crime", "After waking from a four-year coma, a former assassin wreaks vengeance on the team of assassins who betrayed her.")
    ]
    
    with open("movies.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Movie_ID", "Title", "Genres", "Description"])
        writer.writerows(movies)
        
    # Generate user ratings
    # Simulate 100 users, each rating 5 to 15 movies.
    # Group users into tastes:
    # Group A: likes Sci-Fi/Action (Inception, Matrix, Star Wars, Dark Knight...)
    # Group B: likes Romance/Drama (Titanic, Notebook, Forrest Gump...)
    # Group C: likes Comedy (Superbad, Hangover, Step Brothers...)
    # Group D: likes Thriller/Horror (Seven, Silence of the Lambs, Conjuring...)
    
    ratings = []
    
    for uid in range(1, 101):
        taste = random.choice(["A", "B", "C", "D"])
        num_ratings = random.randint(6, 12)
        
        if taste == "A": # Sci-Fi/Action lovers
            fav_movies = [1, 2, 3, 4, 5, 21, 23, 24]
            dislike_movies = [9, 10, 11, 12, 13]
        elif taste == "B": # Romance/Drama lovers
            fav_movies = [6, 7, 8, 9, 10, 3]
            dislike_movies = [2, 4, 19, 24, 25]
        elif taste == "C": # Comedy lovers
            fav_movies = [11, 12, 13, 14, 15, 8]
            dislike_movies = [16, 17, 18, 19, 21]
        else: # Thriller/Horror lovers
            fav_movies = [16, 17, 18, 19, 20, 21, 22]
            dislike_movies = [9, 10, 12, 13, 15]
            
        # Draw rated movies
        all_movie_ids = list(range(1, 26))
        rated_movie_ids = random.sample(all_movie_ids, num_ratings)
        
        for mid in rated_movie_ids:
            if mid in fav_movies:
                rating = random.choices([4, 5], weights=[0.3, 0.7])[0]
            elif mid in dislike_movies:
                rating = random.choices([1, 2, 3], weights=[0.5, 0.4, 0.1])[0]
            else:
                rating = random.choices([3, 4, 5], weights=[0.4, 0.5, 0.1])[0]
                
            ratings.append([uid, mid, rating])
            
    with open("user_ratings.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["User_ID", "Movie_ID", "Rating"])
        writer.writerows(ratings)
        
    print(f"[+] Successfully generated {len(movies)} movies and {len(ratings)} user ratings in user_ratings.csv.")

if __name__ == "__main__":
    main()
