# This file only reserved for separate database operation
from user import app as user_app
from film_categories import app as categories_app
from films import app as film_app
from reconmend_engine import app as recommend_app
import os
from threading import Thread, Event
from waitress import serve
import signal

# Create event objects to signal thread termination
stop_event = Event()

def run_user_auth():
    try:
        serve(user_app, host='0.0.0.0', port=int(os.environ.get('USER_PORT', 5002)), threads=4) # Added threads for better responsiveness
    except Exception as e:
      print(f"User auth stopped due to exception: {e}")
    finally:
      stop_event.set() # Signal that the thread is stopping


def run_categories_api():
    try:
        serve(categories_app, host='0.0.0.0', port=int(os.environ.get('CATEGORIES_PORT', 5001)), threads=4) # Added threads for better responsiveness
    except Exception as e:
      print(f"Categories API stopped due to exception: {e}")
    finally:
      stop_event.set()  # Signal that the thread is stopping
      
def run_film_api():
    try:
        serve(film_app, host='0.0.0.0', port=int(os.environ.get('FILM_PORT', 5010)), threads=4) # Added threads for better responsiveness
    except Exception as e:
      print(f"Film API stopped due to exception: {e}")
    finally:
      stop_event.set()  # Signal that the thread is stopping

def run_recommend_api():
    try:
        serve(recommend_app, host='0.0.0.0', port=int(os.environ.get('RECOMMEND_PORT', 5011)), threads=4) # Added threads for better responsiveness
    except Exception as e:
      print(f"Recommend API stopped due to exception: {e}")
    finally:
      stop_event.set()  # Signal that the thread is stopping

def handle_shutdown(signum, frame):
    print("Shutting down servers...")
    stop_event.set()
    # Optionally, add a timeout here to wait for threads to finish, or use a more robust solution than Event()


if __name__ == "__main__":
    # Handle SIGINT (Ctrl+C) and SIGTERM (kill command)
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    user_thread = Thread(target=run_user_auth)
    categories_thread = Thread(target=run_categories_api)
    film_thread = Thread(target=run_film_api)
    recommend_thread = Thread(target=run_recommend_api)

    user_thread.start()
    categories_thread.start()
    film_thread.start()
    recommend_thread.start()

    # These can't be wait to be done because they are always on application
    user_thread.join()
    categories_thread.join()
    film_thread.join()
    recommend_thread.join()

    print("Servers stopped successfully.")