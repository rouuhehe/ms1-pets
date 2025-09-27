import random
# import boto3
# import os
from faker import Faker
from sqlalchemy.orm import Session
from app.db import session
from app.models import AdoptionCenter, AdoptionStatus, AdoptionState, Pet, Vaccine
from dotenv import load_dotenv

fake = Faker("es_ES")

NUM_CENTERS = 200
NUM_PETS = 20000
CHUNK_SIZE = 500
'''
load_dotenv()
S3_BASE_URL = os.getenv("S3_BASE_URL")

s3 = boto3.client(
    "s3",
    region_name=None,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
)
S3_BUCKET = os.getenv("S3_BUCKET")
'''
SPECIES_BREEDS = {
    "Dog": [
        "Labrador Retriever", "German Shepherd", "Golden Retriever", "French Bulldog", "Bulldog",
        "Beagle", "Poodle", "Rottweiler", "Yorkshire Terrier", "Dachshund",
        "Boxer", "Doberman Pinscher", "Shih Tzu", "Great Dane", "Siberian Husky",
        "Cocker Spaniel", "Chihuahua", "Maltese", "Pomeranian", "Border Collie",
        "Basset Hound", "Akita", "Australian Shepherd", "Boston Terrier", "Weimaraner",
        "Newfoundland", "Dalmatian", "Whippet", "Samoyed", "Bull Terrier",
        "Staffordshire Bull Terrier", "Cane Corso", "Belgian Malinois", "Chow Chow", "Papillon",
        "Jack Russell Terrier", "Alaskan Malamute", "Shiba Inu", "Irish Setter", "Greyhound",
        "Saint Bernard", "Lhasa Apso", "Bloodhound", "Collie", "Vizsla",
        "Portuguese Water Dog", "Chinese Crested", "Pekingese", "Scottish Terrier", "Havanese",
        "Mixed", "Cruzado"
    ],
    "Cat": [
        "Siamese", "Persian", "Maine Coon", "Sphynx", "Bengal",
        "British Shorthair", "Ragdoll", "Abyssinian", "Birman", "Oriental Shorthair",
        "Russian Blue", "Scottish Fold", "Norwegian Forest Cat", "American Shorthair", "Savannah",
        "Devon Rex", "Cornish Rex", "Turkish Angora", "Manx", "Tonkinese",
        "Himalayan", "Balinese", "Singapura", "Selkirk Rex", "Ocicat",
        "Egyptian Mau", "Burmese", "Chartreux", "Japanese Bobtail", "Korat",
        "LaPerm", "Somali", "Exotic Shorthair", "Nebelung", "American Curl",
        "Pixie-Bob", "Bombay", "Cymric", "Snowshoe", "Munchkin",
        "Chantilly-Tiffany", "Turkish Van", "Serengeti", "Peterbald", "Toyger",
        "Mixed", "Cruzado"
    ],
    "Rabbit": [
        "Lop", "Dutch", "Lionhead", "Rex", "Mini Rex", "Angora", "Harlequin", "Flemish Giant",
        "English Spot", "Holland Lop", "Netherland Dwarf", "Silver Marten", "Mixed", "Cruzado"
    ],
    "Bird": [
        "Parrot", "Canary", "Cockatiel", "Budgerigar", "Lovebird", "Macaw", "Cockatoo",
        "African Grey", "Finch", "Conure", "Parakeet", "Lorikeet", "Mixed", "Cruzado"
    ]
}

VACCINE_TYPES = {
    "Dog": [
        "Rabies",
        "Parvovirus",
        "Distemper",
        "Hepatitis (Adenovirus)",
        "Leptospirosis",
        "Parainfluenza",
        "Bordetella (Kennel Cough)",
        "Canine Influenza",
        "Lyme Disease",
        "Coronavirus",
    ],
    "Cat": [
        "Rabies",
        "Feline Panleukopenia (Distemper)",
        "Feline Herpesvirus (Rhinotracheitis)",
        "Calicivirus",
        "Feline Leukemia Virus (FeLV)",
        "Chlamydia",
        "Bordetella",
    ],
    "Rabbit": [
        "Myxomatosis",
        "Rabbit Hemorrhagic Disease Virus (RHDV1)",
        "Rabbit Hemorrhagic Disease Virus 2 (RHDV2)",
        "Pasteurellosis",
    ],
    "Bird": [
        "Polyomavirus",
        "Psittacosis (Chlamydia psittaci)",
        "Pacheco’s Disease (Herpesvirus)",
        "Avian Influenza",
        "Newcastle Disease",
    ]
}

species_cache = {}

'''
def get_image(species):
    folder = f"images/{species.lower()}s/"

    if folder not in species_cache:
        response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=folder)
        files = [obj["Key"] for obj in response.get("Contents", [])
                 if obj["Key"].endswith((".jpg", ".jpeg", ".png"))]
        species_cache[folder] = files

    files = species_cache[folder]
    if not files:
        return f"{S3_BASE_URL}/images/{folder}100.jpg"

    chosen = random.choice(files)
    return f"{S3_BASE_URL}/{chosen}"
'''


def seed_massive():
    session.init_db()
    db: Session = session.SessionLocal()

    centers = []
    for i in range(NUM_CENTERS):
        center = AdoptionCenter(
            name=fake.company(),
            address=fake.address(),
            city=fake.city(),
            lat=float(fake.latitude()),
            lon=float(fake.longitude()),
        )
        db.add(center)
        centers.append(center)

        if (i + 1) % CHUNK_SIZE == 0:
            db.commit()
            print(f"{i + 1} centros insertados...")

    db.commit()

    pets = []
    for i in range(NUM_PETS):
        species = random.choice(list(SPECIES_BREEDS.keys()))
        breed = random.choice(SPECIES_BREEDS[species])
        birth_date = fake.date_between(start_date="-15y", end_date="today")
        image_url = f"https://placedog.net/500/400?id={i%240}"
        #if image_url is None:
        #    image_url = f"/static/images/{species.lower()}s/100.jpg"

        pet = Pet(
            name=fake.first_name(),
            species=species,
            breed=breed,
            birth_date=birth_date,
            adoption_center_id=random.choice(centers).id,
            image_url=image_url,
        )
        db.add(pet)
        pets.append(pet)

        if (i + 1) % CHUNK_SIZE == 0:
            db.commit()
            print(f"{i+1} mascotas insertadas...")

    db.commit()

    for i, pet in enumerate(pets):
        status = AdoptionStatus(
            pet_id=pet.id,
            state=random.choice(list(AdoptionState)),
        )
        db.add(status)

        vaccines_for_species = VACCINE_TYPES.get(pet.species, [])
        if vaccines_for_species:
            num_vaccines = random.randint(0, min(4, len(vaccines_for_species)))
            chosen_vaccines = random.sample(vaccines_for_species, num_vaccines)
            for vt in chosen_vaccines:
                vaccine = Vaccine(
                    pet_id=pet.id,
                    type=vt,
                    date=fake.date_between(start_date=pet.birth_date, end_date="today"),
                )
                db.add(vaccine)

        if (i + 1) % CHUNK_SIZE == 0:
            db.commit()
            print(f"Estados/vacunas generados para {i + 1} mascotas")

    db.commit()
    db.close()
    print(f"Se generaron {NUM_CENTERS} centros, {NUM_PETS} mascotas, estados y vacunas.")


if __name__ == "__main__":
    seed_massive()
