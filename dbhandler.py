from peewee import *
import datetime

db = SqliteDatabase('people.db')

class User(Model):
    v_id         = CharField()
    name         = CharField()
    tel_nr       = CharField()
    reg_date     = DateTimeField()
    is_admin     = BooleanField()
    is_confirmed = BooleanField()

    class Meta:
        database = db

class Estate(Model):
    owner = ForeignKeyField(User, related_name='estates')
    reg_date = DateTimeField()
    flat_nr = CharField()
    home_nr = CharField()

    class Meta:
        database = db

class Car(Model):
    owner = ForeignKeyField(User, related_name='cars')
    reg_date = DateTimeField()
    car_nr = CharField()

    class Meta:
        database = db


class DBHandler(object):
    def __init__(self):
        pass

    def createDB(self):
        User.create_table()
        Estate.create_table()
        Car.create_table()

    def userExists(self, v_id):
        return User.select().where(User.v_id == v_id).exists()

    def userIsConfirmed(self, v_id):
        user = User.select().where(User.v_id == v_id).get()
        return user.is_confirmed

    def confirmUser(self, v_id):
        user = User.select().where(User.v_id == v_id).get()
        user.is_confirmed = True
        user.save()

    def setUserAdmin(self, v_id):
        user = User.select().where(User.v_id == v_id).get()
        user.is_admin = True
        user.save()

    def clearUserAdmin(self, v_id):
        user = User.select().where(User.v_id == v_id).get()
        user.is_admin = False
        user.save()

    def createUser(self, v_id_, tel_nr_):
        user = User.create(v_id=v_id_, name="", tel_nr=tel_nr_,
                           reg_date=datetime.datetime.now(),
                           is_admin=False, is_confirmed=False)
        user.save()

    def addEstate(self, v_id_, home_nr_, flat_nr_):
        user = User.select().where(User.v_id == v_id_).get()
        estate = Estate.create(owner=user, flat_nr=flat_nr_, home_nr=home_nr_,
                               reg_date=datetime.datetime.now())
        estate.save()

    def addCar(self, v_id_, car_nr_):
        user = User.select().where(User.v_id == v_id).get()
        car  = Car.create(owner=user, car_nr=car_nr_,
                          reg_date=datetime.datetime.now())
        car.save()
