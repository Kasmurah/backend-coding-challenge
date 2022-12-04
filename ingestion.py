import argparse
import json
import os
from datetime import datetime
from uuid import uuid4
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from util.osUtil import OSUtil
from sql.schema.client import Client
from sql.schema.talent import Talent
from sql.schema.opening import Opening

OSUtil.load_env(OSUtil.default_prod_env)
engine = sqlalchemy.create_engine(f'sqlite:///{os.getenv("db_path")}'.replace("\\", "/"))

conn = engine.connect()


def main():
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    ArgParser = argparse.ArgumentParser(description="Ingestion")
    ArgParser.add_argument("-p",
                           '--path',
                           action="store",
                           type=str,
                           dest="path",
                           help="Path to the file to be ingested",
                           required=True)

    args = ArgParser.parse_args()
    path = args.path

    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)

    data = clean_data(data)

    client_data = get_client_list(data)

    # check if client exists, if not create
    set_new_clients(session, client_data)

    # check if talent exists, if not create
    talent_data = get_talent_list(data)

    set_new_talents(session, talent_data)

    # check if opening exists, if not create
    opening_data = get_opening_list(data)
    set_new_openings(session, opening_data)


def clean_data(data):
    # TODO I've noticed that the talentID can be empty sometimes. Since I've build this solution as having
    #  the talent_id as the primaty key, I'll be generating a new GUID for each missing data. This is not ideal,
    # since when re-trying the same data, the empty ones will create
    for d in data:
        if d["talentId"] == "":
            d["talentId"] = str(uuid4())
    return data


def get_client_list(data: list):
    client_list = []

    for i in data:
        client_info = {"client_id": i["clientId"],
                       "client_name": i["clientName"],
                       "industry": i["industry"]}
        client_list.append(client_info)

    client_list = [dict(t) for t in {tuple(d.items()) for d in client_list}]
    client_list = sorted(client_list, key=lambda d: d['client_id'])
    return client_list


def get_talent_list(data: list):
    talent_list = []

    for i in data:
        client_info = {"talent_id": i["talentId"],
                       "talent_name": i["talentName"],
                       "talent_grade": i["talentGrade"],
                       "booking_grade": i["bookingGrade"],
                       "operating_unit": i["operatingUnit"],
                       "office_city": i["officeCity"],
                       "office_postal_code": i["officePostalCode"],
                       "job_manager_id": i["jobManagerId"],
                       "job_manager_name": i["jobManagerName"]}
        talent_list.append(client_info)

    talent_list = [dict(t) for t in {tuple(d.items()) for d in talent_list}]
    talent_list = sorted(talent_list, key=lambda d: d['talent_id'])
    return talent_list


def get_opening_list(data: list):
    opening_list = []

    for i in data:
        opening_info = {"id": i["id"],
                        "client_id": i["clientId"],
                        "required_skills": i["requiredSkills"],
                        "optional_skills": i["optionalSkills"],
                        "start_date": i["startDate"],
                        "end_date": i["endDate"],
                        "total_hours": i["totalHours"],
                        "talent_id": i["talentId"],
                        "original_id": i["originalId"]}
        opening_list.append(opening_info)

    opening_list = sorted(opening_list, key=lambda d: d['id'])
    return opening_list


def set_new_clients(session, clients):
    print(f"creating {len(clients)} clients")
    for client in clients:

        # Check if book exists
        existing_client = (
            session.query(Client)
            .filter(Client.id == client["client_id"])
            .one_or_none()
        )

        if existing_client is not None:
            continue

        c = Client(id=client["client_id"], name=client["client_name"], industry=client["industry"])
        session.add(c)

        # Commit to the database
        session.commit()


def set_new_talents(session, talents):
    print(f"creating {len(talents)} talents")
    for talent in talents:

        existing_talent = (
            session.query(Talent)
            .filter(Talent.talent_id == talent["talent_id"])
            .one_or_none()
        )

        if existing_talent is not None:
            continue

        c = Talent(
            talent_id=talent["talent_id"],
            talent_name=talent["talent_name"],
            talent_grade=talent["talent_grade"],
            booking_grade=talent["booking_grade"],
            operating_unit=talent["operating_unit"],
            office_city=talent["office_city"],
            office_postal_code=talent["office_postal_code"],
            job_manager_id=talent["job_manager_id"],
            job_manager_name=talent["job_manager_name"]
        )
        session.add(c)
        session.commit()


def set_new_openings(session, openings):
    print(f"creating {len(openings)} openings")
    for opening in openings:

        # Check if book exists
        existing_opening = (
            session.query(Opening)
            .filter(Opening.id == opening["id"])
            .one_or_none()
        )

        if existing_opening is not None:
            continue

        format = '%m/%d/%Y %I:%M %p'
        #print(f"Opening does not exists: Creating opening {opening['id']}")
        c = Opening(
            id=opening["id"],
            client_id=opening["client_id"],
            required_skills="" if opening["required_skills"] is [] else str(opening["required_skills"]),
            optional_skills="" if opening["optional_skills"] is [] else str(opening["optional_skills"]),
            start_date=datetime.strptime(opening["start_date"], format),
            end_date=datetime.strptime(opening["end_date"], format),
            total_hours=opening["total_hours"],
            talent_id=opening["talent_id"],
            original_id=opening["original_id"])
        session.add(c)

        # Commit to the database
        session.commit()


if __name__ == '__main__':
    main()
