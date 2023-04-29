from data import db_session
from data.users import User
from data.jobs import Jobs


db_name = input()
db_session.global_init(db_name)
db_sess = db_session.create_session()

colonists = db_sess.query(User).filter(User.address == "module_1",
                                       User.position.notlike("%engineer%"),
                                       User.speciality.notlike("%engineer%")).all()
for col in colonists:
    print("<Colonist>", col.id, col.surname, col.name)
