import pickle
from pathlib import Path


def pickled(func):
    import hashlib

    def wrapper(*args, **kwargs):
        # Pickle arguments
        pickled_args = pickle.dumps({"args": args, "kwargs": kwargs})
        # Create md5 hash of the pickled object
        md5_hashed_args = hashlib.md5(str(pickled_args).encode('utf-8')).hexdigest()

        # Check existence of cached response
        pickle_filepath = Path(f"/tmp/pickled_functions/{md5_hashed_args}.pkl")
        pickle_filepath.parent.mkdir(parents=True, exist_ok=True)
        try:
            print(f"\033[96m*** Searching for cached response for '{func.__name__}()\033[0m'")
            result = pickle.load(open(pickle_filepath, "rb"))
            print(f"\033[92m*** Using cached response for '{func.__name__}()'\033[0m")
        except (OSError, IOError) as e:
            print(f"\033[93m*** No cache available. Executing '{func.__name__}()'\033[0m")
            result = func(*args, **kwargs)
            pickle.dump(result, open(pickle_filepath, "wb"))
        return result

    return wrapper
