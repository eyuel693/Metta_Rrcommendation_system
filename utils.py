from hyperon import MeTTa

def initialize_metta(metta_file_path):
    """
    Initialize MeTTa and load the specified knowledge base file.
    """
    metta = MeTTa()
    try:
        with open(metta_file_path, 'r') as f:
            content = f.read()
            print(f"MeTTa file contents: {content[:200]}...")  # Log first 200 chars
            metta.run(content)
            print(f"Loaded MeTTa file: {metta_file_path}")
    except FileNotFoundError:
        print(f"Error: MeTTa file {metta_file_path} not found")
        raise Exception(f"MeTTa file {metta_file_path} not found")
    except Exception as e:
        print(f"Error initializing MeTTa: {str(e)}")
        raise
    return metta

def execute_simple_list(metta, query):
    """
    Execute a MeTTa query and return a flat list of strings.
    """
    try:
        print(f"Executing MeTTa query: {query}")
        results = metta.run(query)
        print(f"Raw MeTTa results: {results}")
        flat_results = []
        def flatten_result(r):
            if r is None:
                return
            if isinstance(r, list):
                for sub_r in r:
                    flatten_result(sub_r)
            elif hasattr(r, 'get_children'):
                children = r.get_children()
                if children:
                    flatten_result(children)
                else:
                    flat_results.append(str(r))
            else:
                flat_results.append(str(r))
        for result in results:
            flatten_result(result)
        unique_results = list(set(flat_results))
        print(f"execute_simple_list query '{query}' returned: {unique_results}")
        if not unique_results:
            print(f"Warning: No results for query '{query}'")
        return unique_results
    except Exception as e:
        print(f"Error in execute_simple_list query '{query}': {str(e)}")
        return []

def execute_query(metta, query):
    """
    Execute a MeTTa query and return structured results (id and title from movie atom).
    """
    try:
        results = execute_simple_list(metta, query)
        if not results:
            print(f"No movies found for query '{query}'")
        parsed = []
        for movie_id in results:
            if not movie_id:
                print(f"Skipping empty movie_id in query '{query}'")
                continue
            movie_query = f'!(match &self (movie {movie_id} $title $genre $director $rating) (movie {movie_id} $title $genre $director $rating))'
            print(f"Fetching movie details for ID: {movie_id}")
            movie_results = metta.run(movie_query)
            print(f"Movie query results for {movie_id}: {movie_results}")
            movie_atom = None
            for result in movie_results:
                if result and hasattr(result, 'get_children'):
                    movie_atom = result
                    break
                elif isinstance(result, list):
                    for sub_result in result:
                        if sub_result and hasattr(sub_result, 'get_children'):
                            movie_atom = sub_result
                            break
                    if movie_atom:
                        break
            if movie_atom and movie_atom.get_children():
                children = movie_atom.get_children()
                title = str(children[1]) if len(children) > 1 else movie_id
                parsed.append({'id': movie_id, 'title': title})
            else:
                print(f"No movie details found for ID: {movie_id}")
                parsed.append({'id': movie_id, 'title': movie_id})
        print(f"execute_query query '{query}' returned: {parsed}")
        return parsed
    except Exception as e:
        print(f"Error in execute_query query '{query}': {str(e)}")
        return []

def get_explanations(metta, user, movies):
    """
    Generate explanations for recommended movies using MeTTa explanation functions.
    """
    explanations = []
    for movie in movies:
        movie_id = movie["id"]
        exp_queries = [
            f'!(explain-genre {user} {movie_id} $explanation)',
            f'!(explain-director {user} {movie_id} $explanation)',
            f'!(explain-collab {user} {movie_id} $explanation)'
        ]
        movie_explanations = []
        for query in exp_queries:
            results = execute_simple_list(metta, query)
            movie_explanations.extend(results)
        explanations.append(movie_explanations if movie_explanations else ["No explanation available."])
    print(f"Explanations for user {user}: {explanations}")
    return explanations

def user_exists(metta, user):
    """
    Check if a user exists in MeTTa by verifying watched movies or preferences.
    """
    watched = execute_simple_list(metta, f'!(watched {user} $movie)')
    preferences = execute_simple_list(metta, f'!(preference {user} $genre)')
    exists = bool(watched or preferences)
    print(f"User {user} exists: {exists}")
    return exists

def add_new_user(metta, user, preferences=[]):
    """
    Add a new user with optional genre preferences.
    """
    for genre in preferences:
        metta.run(f'(preference {user} {genre})')
    print(f"Added new user: {user}")