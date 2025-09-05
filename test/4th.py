from utils import initialize_metta, get_explanations, execute_simple_list

# Initialize MeTTa
metta = initialize_metta("recommendation.metta")

# Users
users = ["alice", "bob", "eve"]


for user in users:
    # Use simple list for recommendations
    rec_list = execute_simple_list(metta, f'!(recommend-to {user}  $movie) ')
    final_recs = [{'id': m, 'title': m} for m in rec_list]  # convert to dict for explanations

    print(f"\nRecommendations for {user.capitalize()}:")
    if final_recs:
        for r in final_recs:
            print(f"- {r['title']} (ID: {r['id']})")
    else:
        print("No recommendations found.")

    # Explanations
    explanations = get_explanations(metta, user, final_recs)
    print("Explanations:")
    for exp_list in explanations:
        for exp in exp_list:
            print(f"- {exp}")

    # Similar users
    similar_users = execute_simple_list(metta, f'!(similar-users {user} $user)')
    print("Similar users:", similar_users)

# Ratings example
movies = ["the-matrix", "inception", "titanic"]
for movie in movies:
    ratings = execute_simple_list(metta, f'!(get-rating {movie} $score)')
    if ratings:
        print(f"Rating of {movie}: {ratings[0]}")
    else:
        print(f"Rating of {movie}: Not found")
