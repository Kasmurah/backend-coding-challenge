import os

import pandas as pd
import sqlalchemy
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from util.osUtil import OSUtil
from sql.schema.talent import Talent, TalentOut
from sql.schema.opening import Opening, OpeningOut
from fastapi_pagination import Page, paginate, add_pagination

app = FastAPI()
add_pagination(app)
OSUtil.load_env(OSUtil.default_prod_env)
engine = sqlalchemy.create_engine(f'sqlite:///{os.getenv("db_path")}'.replace("\\", "/"))


@app.get("/talents/", response_model=Page[TalentOut])
def get_talents():

    Session = sessionmaker()
    Session.configure(bind=engine)
    with Session() as conn:
        results = conn.query(Talent).all()
    return paginate(results)


@app.get("/talent/{talent_id}")
def get_talent_item(talent_id: str):
    query = "select * from talent where talent_id = '{0}'".format(talent_id)
    conn = engine.connect()
    df = pd.read_sql(query, conn)
    return df

@app.get("/openings/", response_model=Page[OpeningOut])
def get_openings():
    Session = sessionmaker()
    Session.configure(bind=engine)
    with Session() as conn:
        results = conn.query(Opening).order_by('original_id').all()
    return paginate(results)



