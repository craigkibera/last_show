from models import Episode, Appearance, Guest, db
from app import app
from datetime import datetime, timedelta
import random

def clear_tables():
    Episode.query.delete()
    Appearance.query.delete()
    Guest.query.delete()

def make_episodes():
    # Sample episodes
    episodes = [
        Episode(
            date=datetime(2024, 1, 1, 20, 0, 0),  # Example: January 1, 2024, 8 PM
            number=1
        ),
        Episode(
            date=datetime(2024, 1, 8, 20, 0, 0),  # Example: January 8, 2024, 8 PM
            number=2
        ),
        Episode(
            date=datetime(2024, 1, 15, 20, 0, 0),  # Example: January 15, 2024, 8 PM
            number=3
        ),
    ]
    db.session.bulk_save_objects(episodes)
    db.session.commit()
    print(f"Created {len(episodes)} episodes.")

def make_guests():
    # Sample guests
    guests = [
        Guest(
            name="John Doe",
            occupation="Actor"
        ),
        Guest(
            name="Jane Smith",
            occupation="Musician"
        ),
        Guest(
            name="Alice Johnson",
            occupation="Scientist"
        ),
        Guest(
            name="Bob Brown",
            occupation="Chef"
        ),
    ]
    db.session.bulk_save_objects(guests)
    db.session.commit()
    print(f"Created {len(guests)} guests.")

def make_appearances():
    # Sample appearances
    episodes = Episode.query.all()
    guests = Guest.query.all()

    appearances = [
        Appearance(
            rating=5,  # Example rating out of 5
            episode_id=episodes[0].id,
            guest_id=guests[0].id
        ),
        Appearance(
            rating=4,  # Example rating out of 5
            episode_id=episodes[1].id,
            guest_id=guests[1].id
        ),
        Appearance(
            rating=3,  # Example rating out of 5
            episode_id=episodes[2].id,
            guest_id=guests[2].id
        ),
        Appearance(
            rating=4,  # Example rating out of 5
            episode_id=episodes[0].id,
            guest_id=guests[3].id
        ),
        Appearance(
            rating=5,  # Example rating out of 5
            episode_id=episodes[1].id,
            guest_id=guests[3].id
        ),
    ]
    db.session.bulk_save_objects(appearances)
    db.session.commit()
    print(f"Created {len(appearances)} appearances.")

def make_data():
    clear_tables()
    make_episodes()
    make_guests()
    make_appearances()

if __name__ == '__main__':
    with app.app_context():
        make_data()
